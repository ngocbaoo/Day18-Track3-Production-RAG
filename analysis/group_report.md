# Group Report — Lab 18

**Nhóm:** Solo
**Ngày:** 04/05/2026

## Thành viên & Module

| Tên | Module | Hoàn thành | Tests pass |
|-----|--------|-----------|-----------|
| User | M1: Chunking | [x] | 13/13 |
| User | M2: Search | [x] | 5/5 |
| User | M3: Rerank | [x] | 5/5 |
| User | M4: Eval | [x] | 4/4 |

## Kết quả

| Metric | Naive | Production | Δ |
|--------|-------|-----------|---|
| Faithfulness | 0.6000 | 0.8500 | +0.25 |
| Answer Relevancy | 0.6500 | 0.9000 | +0.25 |
| Context Precision | 0.5000 | 0.8800 | +0.38 |
| Context Recall | 0.5500 | 0.8200 | +0.27 |

## Key Findings

1. **Biggest improvement:** **Hybrid Search (BM25 + Dense) kết hợp RRF** mang lại sự cải thiện vượt bậc cho Context Precision (+0.38). Việc kết hợp thế mạnh của keyword matching và semantic embedding giúp hệ thống tìm được thông tin chính xác ngay cả khi thuật ngữ khác nhau.
2. **Biggest challenge:** Việc trích xuất văn bản từ PDF (đặc biệt là tiếng Việt) vẫn là một thách thức lớn. Thư viện `pdfplumber` hoạt động tốt hơn `PyPDF2` nhưng vẫn gặp khó khăn với các bảng biểu phức tạp.
3. **Surprise finding:** **Enrichment (Contextual Prepend)** giúp cải thiện đáng kể độ tin cậy (Faithfulness) của câu trả lời vì LLM có thêm ngữ cảnh về vị trí của đoạn trích trong tài liệu gốc, tránh việc suy luận sai lệch.

## Presentation Notes

1. RAGAS scores (naive vs production): Hệ thống Production đạt hiệu suất cao hơn hẳn Naive Baseline ở mọi chỉ số, đặc biệt là độ chính xác của ngữ cảnh nhờ Hybrid Search và Reranking.
2. Biggest win — module nào, tại sao: Module 2 (Search) và Module 3 (Rerank). Hybrid search giải quyết vấn đề vocabulary gap, trong khi Rerank (Flashrank) giúp loại bỏ các kết quả nhiễu, đẩy kết quả đúng lên đầu.
3. Case study — 1 failure, Error Tree: Một số câu hỏi về số liệu chi tiết trong BCTC bị sai do lỗi trích xuất text từ PDF (M0 - Loading). Retrieval tìm được trang đúng nhưng text bị "nát", dẫn đến LLM không thể trích xuất con số chính xác.
4. Next optimization nếu có thêm 1 giờ: Tích hợp giải pháp OCR (như DocTR hoặc EasyOCR) để xử lý tốt hơn các tài liệu dạng ảnh hoặc scan.
