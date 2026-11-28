# Kết luận: lệnh thắng/thua và danh mục 10 mã (28/11/2026)
Luật chốt trước: LUAT_CHOT_TRUOC_lenh_thang_thua.md. Chiến lược nền G2 (20 mã, không lọc). 2.129 lệnh từ 3/2013 đến 11/2026, đã trừ phí 0,15% mỗi chiều. Toàn bộ bảng số: win_loss_out.txt và nvar_out.txt.

## 1. Lệnh thắng vs thua (ĐÃ ĐO)
- Thắng 42,4% số lệnh; lãi TB mỗi lệnh +2,95%, trung vị −1,26%. Lệnh thắng lãi TB +16,9% (giữ TB 35 phiên); lệnh thua −7,3% (giữ TB 15 phiên). Tức là kiểu "thua nhiều lần nhỏ, thắng ít lần lớn".
- Tỷ lệ thắng theo năm: 2018 28%, 2022 31%, 2026 27% (các năm thị trường xấu) so với 2017 58%.
- Trước khi mua: trong 12 đặc điểm, lệnh thắng và thua gần như giống hệt nhau (trung vị gần bằng nhau; chỉ "margin" có p=0,04 trong mẫu, không đáng tin vì thử 12 cái).
- Walk-forward cấp lệnh (train 3 năm → test 1 năm, 2016–2026): đặc điểm duy nhất đúng dấu ở 10/11 năm là margin (mã đang cách xa đường hỗ trợ trendline thì kém hơn: nhóm xấu +2,04% vs +3,14% còn lại, chênh −1,1%, t=−1,12 → độ lớn chưa có ý nghĩa). liq 8/11 năm. 10 đặc điểm còn lại ≤7/11. Kỳ vọng ngẫu nhiên khoảng 1,4 đặc điểm đạt ≥8/11; thực tế 2. Kết luận: KHÔNG phân biệt được lệnh thắng/thua từ thông tin lúc mua. margin là giả thuyết duy nhất đáng thử tiếp (chưa chứng minh).
- Sau khi mua (chỉ mô tả): lệnh thua đã âm sớm (ngày 5: −1,6% vs +4,0%; sụt 10 phiên đầu −5,4% vs −0,6%) nhưng phần lớn là do luật bán tự động cắt sớm lệnh xấu. Mã giảm >8% sau 5 ngày: lãi TB từ ngày 5 đến lúc bán vẫn +1,2% (mã tăng 4–8%: +4,0%) → chưa thấy bằng chứng cắt lỗ sớm hơn có ích. Thiên lệch: lệnh bán trước ngày 5 bị loại khỏi bảng này.
- Hạn chế: cấp lệnh chưa tính ô trống được lấp bằng mã khác; lệnh chồng lấn thời gian.

## 2. Danh mục 10 mã (ĐÃ ĐO, 2016–2026, tiền mặt lãi 0 / gửi 5%)
| | Lãi/năm | Sharpe | Sụt max | Gửi 5%: lãi / Sharpe / sụt |
|---|---|---|---|---|
| 10 mã, thay 1/tuần | 15,5% | 0,98 | −49,6% | 16,8% / 1,05 / −48,0% |
| 10 mã, thay 2/tuần | 20,6% | 1,15 | −54,5% | 21,5% / 1,19 / −53,4% |
| 20 mã, thay 2/tuần | 16,8% | 1,19 | −38,7% | 18,2% / 1,28 / −36,7% |
| 10 mã thay 2/tuần + MA40 bỏ dần | 17,7% | 1,11 | −42,8% | 19,8% / 1,23 / −39,0% |
| 20 mã thay 2/tuần + MA40 bỏ dần | 17,0% | 1,32 | −30,1% | 19,4% / 1,49 / −25,2% |
(thêm bản 10 mã thay 1/tuần + MA40: 14,9% / 1,01 / −43,0%)
Kết luận: 10 mã KHÔNG ổn định hơn. Lãi cao hơn chỉ ở bản thay 2 mã/tuần; bản thay 1 mã/tuần thấp hơn 20 mã. Sụt max sâu hơn −49% đến −55%. Phần hơn đến chủ yếu từ năm 2021 (+130% so với +73%).
Số biến thể tổng: khoảng 39 + 6 = 45 (+ phép thử đặc điểm cấp lệnh).
Kiểm tra bỏ năm 2021 (lãi TB/năm của 10 năm còn lại trong 2016–2026, tiền mặt lãi 0): 10 mã thay 2/tuần 12,8%; 20 mã thay 2/tuần 12,1%; 10 mã thay 1/tuần 7,7%. Năm 10 mã (thay 2) hơn 20 mã: 6/11 năm. Tức là lợi thế của 10 mã gần như chỉ còn 0,7%/năm khi bỏ 2021, với mức sụt vốn lớn hơn nhiều.
