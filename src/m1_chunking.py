"""
Module 1: Advanced Chunking Strategies
=======================================
Implement semantic, hierarchical, và structure-aware chunking.
So sánh với basic chunking (baseline) để thấy improvement.

Test: pytest tests/test_m1.py
"""

import os, sys, glob, re
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (DATA_DIR, HIERARCHICAL_PARENT_SIZE, HIERARCHICAL_CHILD_SIZE,
                    SEMANTIC_THRESHOLD)


@dataclass
class Chunk:
    text: str
    metadata: dict = field(default_factory=dict)
    parent_id: str | None = None


def load_documents(data_dir: str = DATA_DIR) -> list[dict]:
    """Load all markdown/text/pdf files from data/."""
    docs = []
    # Load .md files
    for fp in sorted(glob.glob(os.path.join(data_dir, "*.md"))):
        with open(fp, encoding="utf-8") as f:
            docs.append({"text": f.read(), "metadata": {"source": os.path.basename(fp)}})
    
    # Load .pdf files
    for fp in sorted(glob.glob(os.path.join(data_dir, "*.pdf"))):
        try:
            import pdfplumber
            with pdfplumber.open(fp) as pdf:
                text = ""
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n\n"
                if text:
                    docs.append({"text": text, "metadata": {"source": os.path.basename(fp)}})
                else:
                    print(f"Warning: No text extracted from {fp}")
        except Exception as e:
            print(f"Error loading {fp}: {e}")

            
    return docs



# ─── Baseline: Basic Chunking (để so sánh) ──────────────


def chunk_basic(text: str, chunk_size: int = 500, metadata: dict | None = None) -> list[Chunk]:
    """
    Basic chunking: split theo paragraph (\\n\\n).
    Đây là baseline — KHÔNG phải mục tiêu của module này.
    (Đã implement sẵn)
    """
    metadata = metadata or {}
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for i, para in enumerate(paragraphs):
        if len(current) + len(para) > chunk_size and current:
            chunks.append(Chunk(text=current.strip(), metadata={**metadata, "chunk_index": len(chunks)}))
            current = ""
        current += para + "\n\n"
    if current.strip():
        chunks.append(Chunk(text=current.strip(), metadata={**metadata, "chunk_index": len(chunks)}))
    return chunks


# ─── Strategy 1: Semantic Chunking ───────────────────────


def chunk_semantic(text: str, threshold: float = SEMANTIC_THRESHOLD,
                   metadata: dict | None = None) -> list[Chunk]:
    """
    Split text by sentence similarity — nhóm câu cùng chủ đề.
    Tốt hơn basic vì không cắt giữa ý.
    """
    metadata = metadata or {}
    import re
    import numpy as np
    from sentence_transformers import SentenceTransformer

    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n\n', text) if s.strip()]
    if not sentences:
        return []

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(sentences)

    def cosine_sim(a, b):
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0
        return np.dot(a, b) / (norm_a * norm_b)

    chunks = []
    current_group = [sentences[0]]
    for i in range(1, len(sentences)):
        sim = cosine_sim(embeddings[i-1], embeddings[i])
        if sim < threshold:
            chunks.append(Chunk(text=" ".join(current_group), metadata={**metadata, "chunk_index": len(chunks), "strategy": "semantic"}))
            current_group = []
        current_group.append(sentences[i])

    if current_group:
        chunks.append(Chunk(text=" ".join(current_group), metadata={**metadata, "chunk_index": len(chunks), "strategy": "semantic"}))
    return chunks


# ─── Strategy 2: Hierarchical Chunking ──────────────────


def chunk_hierarchical(text: str, parent_size: int = HIERARCHICAL_PARENT_SIZE,
                       child_size: int = HIERARCHICAL_CHILD_SIZE,
                       metadata: dict | None = None) -> tuple[list[Chunk], list[Chunk]]:
    """
    Parent-child hierarchy: retrieve child (precision) → return parent (context).
    """
    metadata = metadata or {}
    parents = []
    children = []

    paragraphs = text.split("\n\n")
    current_parent_text = ""
    p_idx = 0

    for para in paragraphs:
        if len(current_parent_text) + len(para) > parent_size and current_parent_text:
            pid = f"{metadata.get('source', 'doc')}_p{p_idx}"
            parent = Chunk(text=current_parent_text.strip(), metadata={**metadata, "chunk_type": "parent", "parent_id": pid})
            parents.append(parent)

            # Split parent into children
            for c_idx, i in enumerate(range(0, len(current_parent_text), child_size)):
                child_text = current_parent_text[i:i+child_size].strip()
                if child_text:
                    children.append(Chunk(text=child_text, metadata={**metadata, "chunk_type": "child", "child_index": c_idx}, parent_id=pid))
            
            current_parent_text = ""
            p_idx += 1
        current_parent_text += para + "\n\n"

    if current_parent_text.strip():
        pid = f"{metadata.get('source', 'doc')}_p{p_idx}"
        parent = Chunk(text=current_parent_text.strip(), metadata={**metadata, "chunk_type": "parent", "parent_id": pid})
        parents.append(parent)
        for c_idx, i in enumerate(range(0, len(current_parent_text), child_size)):
            child_text = current_parent_text[i:i+child_size].strip()
            if child_text:
                children.append(Chunk(text=child_text, metadata={**metadata, "chunk_type": "child", "child_index": c_idx}, parent_id=pid))

    return parents, children


# ─── Strategy 3: Structure-Aware Chunking ────────────────


def chunk_structure_aware(text: str, metadata: dict | None = None) -> list[Chunk]:
    """
    Parse markdown headers → chunk theo logical structure.
    """
    metadata = metadata or {}
    import re
    sections = re.split(r'(^#{1,3}\s+.+$)', text, flags=re.MULTILINE)
    
    chunks = []
    current_header = "Intro"
    current_content = ""
    
    for part in sections:
        if re.match(r'^#{1,3}\s+', part):
            if current_content.strip():
                chunks.append(Chunk(
                    text=f"{current_header}\n{current_content}".strip(),
                    metadata={**metadata, "section": current_header, "strategy": "structure", "chunk_index": len(chunks)}
                ))
            current_header = part.strip()
            current_content = ""
        else:
            current_content += part

    if current_content.strip():
        chunks.append(Chunk(
            text=f"{current_header}\n{current_content}".strip(),
            metadata={**metadata, "section": current_header, "strategy": "structure", "chunk_index": len(chunks)}
        ))
    return chunks


# ─── A/B Test: Compare All Strategies ────────────────────


def compare_strategies(documents: list[dict]) -> dict:
    """
    Run all strategies on documents and compare.
    """
    results = {}
    strategies = {
        "basic": lambda t, m: chunk_basic(t, metadata=m),
        "semantic": lambda t, m: chunk_semantic(t, metadata=m),
        "hierarchical": lambda t, m: chunk_hierarchical(t, metadata=m)[1], # only children
        "structure": lambda t, m: chunk_structure_aware(t, metadata=m)
    }

    print(f"{'Strategy':<15} | {'Chunks':<6} | {'Avg Len':<8} | {'Min':<5} | {'Max':<5}")
    print("-" * 50)

    for name, func in strategies.items():
        all_strategy_chunks = []
        for doc in documents:
            chunks = func(doc["text"], doc["metadata"])
            all_strategy_chunks.extend(chunks)
        
        lengths = [len(c.text) for c in all_strategy_chunks]
        if not lengths:
            stats = {"count": 0, "avg": 0, "min": 0, "max": 0}
        else:
            stats = {
                "count": len(lengths),
                "avg": int(sum(lengths) / len(lengths)),
                "min": min(lengths),
                "max": max(lengths)
            }
        results[name] = stats
        print(f"{name:<15} | {stats['count']:<6} | {stats['avg']:<8} | {stats['min']:<5} | {stats['max']:<5}")

    return results



if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")
    results = compare_strategies(docs)
    for name, stats in results.items():
        print(f"  {name}: {stats}")
