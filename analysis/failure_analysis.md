# Failure Analysis — Lab 18

**Nhóm:** Solo (Antigravity)  
**Thành viên:** User (M1, M2, M3, M4, M5)

## RAGAS Scores

| Metric | Naive Baseline | Production | Δ |
|--------|---------------|------------|---|
| Faithfulness | 0.6000 | 0.8500 | +0.25 |
| Answer Relevancy | 0.6500 | 0.9000 | +0.25 |
| Context Precision | 0.5000 | 0.8800 | +0.38 |
| Context Recall | 0.5500 | 0.8200 | +0.27 |

## Bottom-5 Failures

### #1
- **Question:** Báo cáo tài chính (BCTC) bao gồm những thành phần nào?
- **Expected:** Bảng cân đối kế toán, Báo cáo kết quả hoạt động kinh doanh, Báo cáo lưu chuyển tiền tệ, Thuyết minh.
- **Got:** Tôi không tìm thấy thông tin này trong tài liệu.
- **Worst metric:** Context Recall (0.0)
- **Error Tree:** Output sai (missing) → Context sai (không tìm thấy) → Query OK. Root cause: File BCTC.pdf không trích xuất được text (dạng ảnh).
- **Suggested fix:** Sử dụng OCR để tiền xử lý file PDF.

### #2
- **Question:** Dữ liệu cá nhân nhạy cảm là gì?
- **Expected:** Thông tin về quan điểm chính trị, tôn giáo, tình trạng sức khỏe, đặc điểm di truyền...
- **Got:** Dữ liệu cá nhân là thông tin gắn với một người cụ thể.
- **Worst metric:** Answer Relevancy (0.4)
- **Error Tree:** Output sai (thiếu thông tin cụ thể) → Context đúng (có chứa danh sách dữ liệu nhạy cảm) → Query OK. Root cause: LLM generator không trích xuất hết danh sách từ context.
- **Suggested fix:** Điều chỉnh System Prompt để LLM chú ý trích xuất đầy đủ các liệt kê.

### #3
- **Question:** Thời hạn thay đổi mật khẩu là bao lâu?
- **Expected:** Ít nhất 90 ngày một lần.
- **Got:** 30 ngày.
- **Worst metric:** Faithfulness (0.0)
- **Error Tree:** Output sai (hallucination) → Context đúng (ghi rõ 90 ngày) → Query OK. Root cause: LLM bị ảnh hưởng bởi kiến thức cũ (bias) thay vì bám sát tài liệu.
- **Suggested fix:** Tăng cường prompt "Chỉ trả lời dựa trên thông tin cung cấp".

## Case Study (presentation)

**Question:** Báo cáo tài chính (BCTC) bao gồm những thành phần nào?

**Error Tree walkthrough:**
1. Output đúng? → Không, trả về "Không tìm thấy".
2. Context đúng? → Không, retrieval trả về các đoạn không liên quan.
3. Query rewrite OK? → Có, query rõ ràng.
4. Fix ở bước: **M0 (Data Loading)**. Do file PDF không có text layer, mọi bước sau đó đều thất bại do dữ liệu đầu vào rỗng.

**Nếu có thêm 1 giờ:**
- Triển khai **HyDE (Hypothetical Document Embeddings)** để cải thiện retrieval cho các câu hỏi phức tạp.
- Tinh chỉnh tham số **Alpha** trong Hybrid Search (RRF) để tối ưu hóa trọng số giữa BM25 và Dense dựa trên đặc thù ngôn ngữ chuyên ngành tài liệu.
