# Kết luận: mã bán ra vs mã mua vào; mã xa đường hỗ trợ (28/11/2026)
Chiến lược: 20 mã, thay 2/tuần, trendline, bán giảm sàn, MA40 bỏ dần. Luật chốt trước: LUAT_CHOT_TRUOC_doi_ma.md. Bảng đầy đủ: swap_out.txt. Đây là kiểm tra mô tả, không tạo biến thể chiến lược mới (tổng vẫn ~45).

## 1. Mã thêm vào vs mã bị bỏ (ĐÃ ĐO; lãi tính từ giá mở cửa phiên sau tín hiệu, chưa trừ phí)
| 2016–2026 (372 tuần đổi mã) | Sau 20 phiên (~1 tháng) | Sau 60 phiên (~3 tháng) |
|---|---|---|
| 2 mã thêm vào | +3,16% | +6,88% |
| 2 mã bị bỏ | +0,17% | +1,96% |
| Mã được giữ lại | +2,09% | +5,10% |
| TB mọi mã thanh khoản ≥1 tỷ | +0,61% | +2,30% |
| Số tuần mã thêm > mã bỏ | 57% | 55% |
3/2013–11/2026 gần như giống hệt (thêm +3,19% / bỏ +0,18% sau 20 phiên).
- Mã thêm vào thắng mã bị bỏ khoảng 3%/tháng, lớn hơn nhiều so với phí đổi mã (~0,3% khứ hồi). Mã bị bỏ còn kém TB thị trường → luật bỏ 2 mã yếu nhất là đúng hướng.
- Năm luật sai (sau 20 phiên, mã thêm kém mã bỏ): 2022 (−9,2% vs −4,7%), 2023 (−1,1% vs +0,2%), 2026 (−1,6% vs +0,9%). Đều là giai đoạn thị trường yếu/hồi phục — khớp với phát hiện trước: tín hiệu gần đỉnh yếu đi khi thị trường xấu.
- Tỷ lệ tuần "đúng" chỉ 55–57%: thắng nhờ độ lớn, không phải nhờ đúng thường xuyên.

## 2. Mã xa đường hỗ trợ lúc mua (ĐÃ ĐO; ngưỡng walk-forward từ 3 năm trước, năm test 2016–2026, 1.310 lệnh)
Toàn kỳ, "gần" ≈ cách hỗ trợ dưới 13%, "xa" ≈ trên 34% (trong mẫu, để hình dung).
| Nhóm | Số lệnh | Thắng | Lãi TB/lệnh | Giữ TB (phiên) | Bán vì thủng trendline | Bán vì giảm sàn | Bán vì rớt hạng |
|---|---|---|---|---|---|---|---|
| Gần | 456 | 44,1% | +3,7% | 27 | 53% | 21% | 22% |
| Giữa | 405 | 44,0% | +3,9% | 27 | 26% | 25% | 42% |
| Xa | 449 | 39,2% | +2,9% | 17 | 12% | 42% | 43% |
- Mã xa đường hỗ trợ thắng ít hơn khoảng 5 điểm %, lãi TB thấp hơn ~0,8%/lệnh, và kém nhóm gần ở 9/11 năm (ngoại lệ 2025, 2026).
- Điểm đáng chú ý: mã xa hiếm khi bị bán vì thủng trendline (12%) — vì đường hỗ trợ ở quá xa dưới giá nên trendline gần như không bảo vệ được — mà bị bán vì giảm sàn (42%) và giữ ngắn hơn nhiều (17 vs 27 phiên). Tức là mã tăng nóng, lúc đổ thì đổ mạnh.
- Mã gần đường hỗ trợ bị bán vì thủng trendline nhiều nhất (53%) nhưng vẫn có lãi TB cao nhất — trendline cắt sớm nên lỗ nhỏ.

## Ý KIẾN (chưa kiểm)
- Phần 2 khớp với kết quả walk-forward cấp lệnh trước (10/11 năm). Đây là giả thuyết mạnh nhất tìm được, nhưng mới đo cấp lệnh. Bước tiếp: mô phỏng cả danh mục với MỘT quy tắc chốt trước (ví dụ: không mua mã cách hỗ trợ trên ngưỡng 67% của 3 năm trước, lấy mã kế tiếp), đo walk-forward từng năm.
- Phần 1 ủng hộ luật thay 2 mã/tuần hiện tại; không nên sửa.
