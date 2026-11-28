# Luật chốt trước — không mua nhóm xa đường hỗ trợ; mã xa thắng vs thua (28/11/2026)
Chiến lược nền: 20 mã, thay 2/tuần, trendline, bán giảm sàn, MA40 bỏ dần (chuẩn hiện hành).

Phần 1 (1 biến thể): khi THÊM mã mới (kể cả lúc lấp đầy lại), bỏ qua ứng viên có margin > ngưỡng, lấy ứng viên xếp hạng kế tiếp. Mã đang giữ không bị ảnh hưởng.
margin tuần t = log(giá đóng cửa tuần t) − đường hỗ trợ trendline đang áp cho tuần t.
Ngưỡng năm Y = phân vị 67% margin lúc vào lệnh của chiến lược nền trong 3 năm Y-3..Y-1 (walk-forward). 2013–2015 chưa đủ 3 năm → không lọc. Báo năm test 2016–2026, từng năm, so với chiến lược nền và VN-Index. Tiền mặt lãi 0, thêm bản gửi 5%.

Phần 2: lệnh nhóm "xa" (theo ngưỡng walk-forward ở trên, 2016–2026) của chiến lược nền. So lệnh thắng vs thua bằng 8 đặc điểm tính trên 10 và 20 phiên TRƯỚC ngày mua (chỉ dùng giá đến phiên trước ngày mua):
r10, r20: lãi 10/20 phiên; vol20: độ lệch chuẩn lãi ngày 20 phiên; maxup20: lãi 1 phiên lớn nhất trong 20 phiên; ntran20: số phiên tăng ≥ 90% biên độ (gần trần) trong 20 phiên; vratio: giá trị GD TB 10 phiên / TB 60 phiên; up20: tỷ lệ phiên tăng trong 20 phiên; ext10: giá / trung bình 10 phiên.
Walk-forward như cũ: train 3 năm (lệnh nhóm xa, dùng cả 2013–2015 cho train) → chia 3 nhóm, tìm nhóm xấu nhất → kiểm năm sau. Tiêu chí: đúng dấu ≥ 8/11 năm. 8 đặc điểm → ngẫu nhiên kỳ vọng ~0,9 đạt. Số lệnh mỗi năm test nhỏ (~40) nên kết quả yếu.
