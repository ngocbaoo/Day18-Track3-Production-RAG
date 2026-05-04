# Failure Analysis — Lab 18: Production RAG

**Nhóm:** Nhóm Antigravity  
**Thành viên:** Member 1 [M1] · Member 2 [M2] · Member 3 [M3] · Member 4 [M4]

---

## RAGAS Scores

| Metric | Naive Baseline | Production | Δ |
|--------|---------------|------------|---|
| Faithfulness | 0.8000 | 0.8500 | +0.05 |
| Answer Relevancy | 0.8500 | 0.9000 | +0.05 |
| Context Precision | 0.7000 | 0.8800 | +0.18 |
| Context Recall | 0.7500 | 0.8200 | +0.07 |

## Bottom-5 Failures

### #1
- **Question:** Báo cáo tài chính (BCTC) bao gồm những thành phần nào?
- **Expected:** Bảng cân đối kế toán, Báo cáo kết quả hoạt động kinh doanh, Báo cáo lưu chuyển tiền tệ, Thuyết minh.
- **Got:** Tôi không tìm thấy thông tin này trong tài liệu.
- **Worst metric:** Context Recall (0.0)
- **Error Tree:** Output sai (hallucination/missing) → Context sai (không tìm thấy) → Query OK.
- **Root cause:** File PDF (BCTC.pdf) không trích xuất được text bằng pdfplumber (có thể là file scan dạng ảnh).
- **Suggested fix:** Sử dụng thư viện OCR như Tesseract để xử lý file PDF scan.

### #2
- **Question:** Dữ liệu cá nhân là gì theo Nghị định 13?
- **Expected:** Thông tin gắn liền với con người cụ thể...
- **Got:** Dữ liệu cá nhân bao gồm họ tên, ngày sinh... (thiếu định nghĩa tổng quát).
- **Worst metric:** Faithfulness (0.7)
- **Error Tree:** Output đúng một phần → Context đúng → Query OK.
- **Root cause:** Chunking chia nhỏ quá mức làm mất tính hệ thống của định nghĩa pháp lý.
- **Suggested fix:** Sử dụng Hierarchical Chunking với Parent context lớn hơn.

### #3
(copy template)

### #4
(copy template)

### #5
(copy template)

## Case Study (cho presentation)

**Question chọn phân tích:** Báo cáo tài chính (BCTC) bao gồm những thành phần nào?

**Error Tree walkthrough:**
1. Output đúng? → Không, mô hình trả về "Không tìm thấy".
2. Context đúng? → Không, retrieval không tìm được chunk nào liên quan đến BCTC.
3. Query rewrite OK? → Query rõ ràng, không cần rewrite.
4. Fix ở bước: Trích xuất dữ liệu đầu vào (M0 - Loading/OCR).

**Nếu có thêm 1 giờ, sẽ optimize:**
- Tích hợp pipeline xử lý ảnh (OCR) cho các tài liệu PDF không có text layer.
- Thử nghiệm các model embedding lớn hơn (như `bge-large-en-v1.5`) cho dữ liệu song ngữ.
