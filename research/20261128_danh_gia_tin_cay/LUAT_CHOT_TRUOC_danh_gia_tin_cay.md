# Luật chốt trước — đánh giá độ tin cậy "20 mã gần đỉnh + MA40 bỏ dần 2 mã" (28/11/2026)
Chiến lược được đánh giá: 20 mã, thay 2/tuần, trendline tuần, giảm sàn, MA40 bỏ dần (đã chốt, KHÔNG có biến thể mới). Khoảng thời gian: 2016–2026 (và 3/2013–11/2026 khi ghi rõ).
1. Placebo: 200 lần, cùng bộ máy (thanh khoản ≥1 tỷ, trendline, MA40 bỏ dần, giảm sàn, thay 2 mã yếu nhất/tuần) nhưng điểm mỗi tuần là số ngẫu nhiên. Đo: lãi/năm, Sharpe, sụt max 2016–2026. Phép thử: strategy nằm ở phân vị nào của 200 lần. Tiêu chí tin tín hiệu: trên phân vị 95 ở cả lãi/năm và Sharpe.
2. Deflated Sharpe (Bailey–López de Prado): n biến thể = 49, phương sai Sharpe giữa các biến thể lấy từ các chuỗi đã lưu. Tiêu chí: xác suất Sharpe thật > 0 sau khi trừ chọn lọc ≥ 95%.
3. Bootstrap theo khối (khối 20 phiên, 2.000 lần) trên lãi ngày 2016–2026: khoảng tin cậy 90% của lãi/năm, Sharpe, sụt max; xác suất lãi/năm > VN-Index.
4. Chi phí mỗi chiều (đã gồm phí, thuế bán, trượt giá): 0,15% (nền) / 0,30% / 0,50% / 0,80%. Tiêu chí còn đáng tin: vẫn hơn VN-Index ở mức 0,50%.
5. Dữ liệu: đối chiếu giá đóng cửa VCI (stocks_long) với KBS (stocks) trên các ngày chung, tỷ lệ lệch >1%; tập trung lãi (đóng góp của 10 lệnh tốt nhất); phạt hủy niêm yết (mất thêm 50% với lệnh kết thúc do ngừng giao dịch); sức chứa (% lệnh có vị thế >10% thanh khoản TB 20 phiên ở vốn 1/5/20/50 tỷ).
