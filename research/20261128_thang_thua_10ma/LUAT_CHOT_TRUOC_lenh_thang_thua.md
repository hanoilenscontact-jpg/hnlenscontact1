# Luật chốt trước — lệnh thắng vs lệnh thua, và danh mục 10 mã (28/11/2026)

Chốt TRƯỚC khi chạy. Dữ liệu: repo commit 1c42aec. Chiến lược nền: G2 (20 mã, thay 2 mã yếu nhất/tuần, trendline tuần, bán giảm sàn), KHÔNG lọc MA, để có nhiều lệnh nhất.

## Phần 1 — Phân biệt lệnh thắng/thua
Lệnh = 1 lần mua đến lần bán của 1 mã (giá mở cửa phiên sau tín hiệu, đã trừ phí 0,15% mỗi chiều). Thắng = lãi ròng > 0.

12 đặc điểm tại thời điểm tín hiệu (CHỈ dùng thông tin biết trước khi mua):
1. dist: giá/đỉnh 52 tuần  2. rank: thứ hạng điểm khi vào  3. ret4, 4. ret13, 5. ret26: lãi 4/13/26 tuần trước
6. vol26: độ dao động lãi tuần 26 tuần  7. liq: giá trị giao dịch TB 20 phiên (log)
8. gap: giá mở cửa ngày mua so với đóng cửa phiên trước  9. margin: khoảng cách giá tới đường hỗ trợ trendline (log)
10. vni_ma40: VN-Index cách MA40 bao nhiêu %  11. vni_ret4: VN-Index 4 tuần trước  12. san: biên độ sàn (7/10/15%)

Đặc điểm SAU khi mua (chỉ mô tả, không dùng để chọn mã vào): lãi ngày 5, sụt tối đa 10 phiên đầu, lãi từ ngày 5 đến lúc bán, số phiên giữ.

Walk-forward cấp lệnh: với mỗi năm test Y (2016–2026), dùng lệnh vào trong 3 năm Y-3..Y-1 để (a) chia 3 nhóm bằng ngưỡng 33%/67% của đặc điểm, (b) xác định nhóm có lãi TB thấp nhất ("nhóm xấu"). Sang năm Y: lãi TB của lệnh rơi vào nhóm xấu (theo ngưỡng của train) so với phần còn lại. Gộp 11 năm test.
Tiêu chí "có tín hiệu thật": lãi TB nhóm xấu thấp hơn phần còn lại khi gộp 11 năm test VÀ đúng dấu ở ít nhất 8/11 năm. 12 đặc điểm được thử, nên kỳ vọng ngẫu nhiên có ~1,4 đặc điểm đạt tiêu chí này. Nếu không đặc điểm nào vượt xa mức đó → kết luận "không phân biệt được".
Hạn chế phải ghi: cấp lệnh chưa tính việc ô trống được lấp bằng mã khác; các lệnh chồng lấn thời gian nên t-stat chỉ để tham khảo.

## Phần 2 — Danh mục tập trung
Lưới duy nhất (6 lần chạy): N mã ∈ {10 (thay 1/tuần), 10 (thay 2/tuần), 20 (thay 2/tuần, đối chứng)} × {không lọc, MA40 không mua mới + bỏ dần 2 mã}. Mọi quy tắc khác như G2. Mỗi vị thế = 1/N vốn. Tiền mặt lãi 0 và báo thêm bản gửi 5%/năm.
Báo: từng năm, 2016–2026 và 3/2013–11/2026 (trong mẫu), lãi/năm, Sharpe, sụt max, vốn dùng TB, và số mã khác nhau từng nắm giữ. Không tối ưu thêm N.
