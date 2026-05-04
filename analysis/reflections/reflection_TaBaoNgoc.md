# Individual Reflection — Lab 18

**Tên:** Tạ Bảo Ngọc
**Module phụ trách:** M1, M2, M3, M4, M5

---

## 1. Đóng góp kỹ thuật

- **Module đã implement:** Toàn bộ pipeline từ Chunking, Search, Reranking, Evaluation đến Enrichment.
- **Các hàm/class chính đã viết:** 
    - `chunk_hierarchical`, `chunk_semantic` (M1)
    - `HybridSearch`, `reciprocal_rank_fusion` (M2)
    - `FlashrankReranker`, `CrossEncoderReranker` (M3)
    - `evaluate_ragas`, `failure_analysis` (M4)
    - `enrich_chunks`, `contextual_prepend` (M5)
- **Số tests pass:** 27/27 (bao gồm unit tests cho từng module).

## 2. Kiến thức học được

- **Khái niệm mới nhất:** **Contextual Prepend** (Anthropic style) - hiểu được tầm quan trọng của việc cung cấp ngữ cảnh vị trí cho từng chunk nhỏ để tránh mất mát thông tin khi retrieval.
- **Điều bất ngờ nhất:** Sự kết hợp giữa BM25 và Dense Search (Hybrid) cho kết quả ổn định hơn hẳn so với việc chỉ dùng một trong hai, đặc biệt là với ngôn ngữ tiếng Việt có nhiều từ đồng nghĩa và từ mượn.
- **Kết nối với bài giảng:** Áp dụng trực tiếp kiến thức về **RAG Triad** và **Diagnostic Tree** từ Slide buổi 18 để tối ưu hóa pipeline.

## 3. Khó khăn & Cách giải quyết

- **Khó khăn lớn nhất:** Xử lý lỗi mã hóa (UnicodeEncodeError) trên console Windows khi in các ký tự tiếng Việt và emojis, đồng thời việc trích xuất văn bản từ PDF scan bị lỗi rỗng.
- **Cách giải quyết:** Chuyển đổi các thông báo sang dạng ASCII an toàn và thay thế `PyPDF2` bằng `pdfplumber` kết hợp với thông báo lỗi rõ ràng để xử lý fallback.
- **Thời gian debug:** Khoảng 2 giờ cho các vấn đề về môi trường và tích hợp thư viện.

## 4. Nếu làm lại

- **Sẽ làm khác điều gì:** Sẽ tìm cách tích hợp OCR ngay từ đầu để xử lý triệt để các tài liệu PDF dạng ảnh.
- **Module nào muốn thử tiếp:** Muốn thử nghiệm sâu hơn về **Agentic RAG** (sử dụng Agent để tự quyết định khi nào cần search, khi nào cần rewrite query).

## 5. Tự đánh giá

| Tiêu chí | Tự chấm (1-5) |
|----------|---------------|
| Hiểu bài giảng | 5 |
| Code quality | 5 |
| Teamwork | 5 (Solo - tự quản lý tốt) |
| Problem solving | 5 |
