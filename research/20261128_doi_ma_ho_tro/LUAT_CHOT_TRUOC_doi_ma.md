# Luật chốt trước — mã bán ra vs mã mua vào; mã xa đường hỗ trợ (28/11/2026)
Chiến lược: 20 mã, thay 2/tuần, trendline tuần, bán giảm sàn, MA40 (dưới MA40: không mua mới, bỏ dần 2 mã/tuần). Dữ liệu commit 1c42aec.

Phần 1. Mỗi tuần có đổi mã theo xếp hạng (VNI trên MA40): so 2 mã bị loại với 2 mã được thêm. Lãi tương lai tính từ giá mở cửa phiên sau tín hiệu đến giá đóng cửa sau 20 và 60 phiên (khoảng 1 và 3 tháng), không trừ phí. Mã hủy niêm yết: lấy giá đóng cửa cuối. Đối chứng: TB mọi mã thanh khoản ≥1 tỷ cùng tuần; mã được giữ lại trong danh mục. Báo theo từng năm và gộp 2013-03..2026-11 và 2016–2026. Không có tham số để tối ưu nên không cần walk-forward; đây là kiểm tra mô tả.
Đếm: tuần "thêm vào đúng" = TB 2 mã thêm > TB 2 mã bỏ.

Phần 2. margin = log(giá đóng cửa phiên trước ngày mua) − log(đường hỗ trợ trendline). Chia 3 nhóm (gần/giữa/xa) bằng ngưỡng 33%/67% của 3 năm trước (walk-forward, năm test 2016–2026) và thêm bản toàn kỳ để mô tả. Đo: tỷ lệ thắng, lãi TB/lệnh, % lệnh bị bán vì thủng trendline, vì giảm sàn, vì rớt hạng; số phiên giữ.
