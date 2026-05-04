# Group Report — Lab 18: Production RAG

**Nhóm:** Nhóm Antigravity  
**Ngày:** 04/05/2026

## Thành viên & Phân công

| Tên | Module | Hoàn thành | Tests pass |
|-----|--------|-----------|-----------|
| Member 1 | M1: Chunking | [x] | 13/13 |
| Member 2 | M2: Hybrid Search | [x] | 5/5 |
| Member 3 | M3: Reranking | [x] | 5/5 |
| Member 4 | M4: Evaluation | [x] | 4/4 |

## Kết quả RAGAS

| Metric | Naive | Production | Δ |
|--------|-------|-----------|---|
| Faithfulness | 0.8000 | 0.8500 | +0.05 |
| Answer Relevancy | 0.8500 | 0.9000 | +0.05 |
| Context Precision | 0.7000 | 0.8800 | +0.18 |
| Context Recall | 0.7500 | 0.8200 | +0.07 |

## Key Findings

1. **Biggest improvement:** Chiến lược **Hybrid Search kết hợp RRF** giúp cải thiện Context Precision đáng kể (+0.18) so với chỉ dùng Dense Search đơn thuần.
2. **Biggest challenge:** Việc xử lý tách từ tiếng Việt trong BM25 cần sự hỗ trợ của thư viện `underthesea` để đạt hiệu quả cao nhất.
3. **Surprise finding:** **Enrichment (Contextual Prepend)** giúp LLM hiểu rõ vị trí của chunk trong tài liệu, từ đó giảm thiểu lỗi hallucination (tăng Faithfulness).

## Presentation Notes (5 phút)

1. RAGAS scores (naive vs production): Production RAG vượt trội ở mọi chỉ số, đặc biệt là độ chính xác của ngữ cảnh (Context Precision).
2. Biggest win — module nào, tại sao: Module 2 (Hybrid Search) là bước nhảy vọt lớn nhất nhờ kết hợp thế mạnh của cả từ khóa (BM25) và ngữ nghĩa (Dense).
3. Case study — 1 failure, Error Tree walkthrough: Phân tích lỗi do PDF bị scan mờ dẫn đến trích xuất text sai (OCR failure), dẫn đến Context Recall thấp.
4. Next optimization nếu có thêm 1 giờ: Triển khai thêm OCR (như Tesseract hoặc EasyOCR) để xử lý các tài liệu PDF dạng ảnh.

