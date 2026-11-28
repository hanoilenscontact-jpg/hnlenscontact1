# Đánh giá độ tin cậy: 20 mã gần đỉnh 52 tuần + MA40 bỏ dần 2 mã (28/11/2026)
Luật chốt trước: LUAT_CHOT_TRUOC_danh_gia_tin_cay.md. Chiến lược: 20 mã, thay 2/tuần, trendline tuần, bán giảm sàn, MA40 bỏ dần. Khoảng thời gian ghi cạnh từng số. Không có biến thể mới (vẫn khoảng 49).

## Kết luận một dòng
Tín hiệu "gần đỉnh" có thật (hơn hẳn chọn ngẫu nhiên). Nhưng 17%/năm KHÔNG nên dùng làm kỳ vọng: sau chi phí thực tế, ước chừng 8–13%/năm; 3 năm gần nhất thua VN-Index; dữ liệu 2013–2021 bị thiên lệch sống sót chưa đo được. Chưa đủ cơ sở dùng tiền thật.

## ĐÃ ĐO (2016–2026 nếu không ghi khác)
1. Placebo 200 lần (cùng thanh khoản, trendline, MA40, giảm sàn, mức đổi mã, nhưng điểm là số ngẫu nhiên): lãi/năm placebo 5/50/95% = 1,6% / 4,8% / 7,5% (cao nhất 10,4%); Sharpe 0,21 / 0,51 / 0,76 (cao nhất 1,00). Chiến lược 17,0% và Sharpe 1,32 cao hơn cả 200/200 lần. Chiến lược hơn placebo trung vị ở 8/11 năm (thua ở 2022, 2023, 2026). Chỉ 1% placebo vượt VN-Index (10,0%).
2. Deflated Sharpe (trừ kỳ vọng vì đã thử ~49 biến thể): 99,8%. Bootstrap theo khối 20 phiên, 2.000 lần: lãi/năm khoảng tin cậy 90% = 7,5% .. 17,0% .. 27,5%; Sharpe 0,65 .. 1,33 .. 2,05; sụt max −38% .. −24% .. −17%; xác suất hơn VN-Index cùng mẫu 87%; xác suất sụt max sâu hơn −40%: 3,4%.
3. Lãi dồn vào ít lệnh: 1.310 lệnh, lãi TB +3,48%/lệnh, trung vị −1,33%. 10 lệnh tốt nhất = 28% tổng lãi; 65 lệnh (5%) = 98% tổng lãi; bỏ 65 lệnh này lãi TB còn +0,08%/lệnh. Các lệnh lãi lớn nhất (TCM +196%, CTP +186%, TGG +154%...) có biên độ giá ngày trong giới hạn sàn; thanh khoản trung bình 2–120 tỷ/phiên.
4. Thiên lệch sống sót: stocks_long không có mã nào kết thúc dữ liệu trước 2022 (số mã kết thúc: 2022: 1, 2023: 4, 2024: 39, 2025: 18, 2026: 77). Mã hủy niêm yết trước 2022 bị thiếu hoàn toàn nên 2013–2021 (giai đoạn lãi cao nhất) bị thổi phồng bởi mã sống sót; mức thổi phồng chưa đo được.
5. Theo giai đoạn (lãi/năm: chiến lược | VN-Index | placebo trung vị): 2016–2019: 22,4% | 13,5% | 2,3%. 2020–2022: 25,6% | 1,6% | 16,5%. 2023–2026: 5,8% | 13,1% | −1,4%. 2024–2026 (giai đoạn có dữ liệu mã hủy): 10,2% | 13,5% | −1,9%. Sharpe 2023–2026: 0,52 (VN-Index 0,78); 2024–2026: 0,87 (VN-Index 0,79).
6. Chi phí mỗi chiều (nền 0,15% chưa gồm thuế bán 0,1% và trượt giá), lãi/năm | Sharpe | sụt max: 0,15%: 17,0% | 1,32 | −30,1%; 0,30%: 14,9% | 1,18 | −32,1%; 0,50%: 12,1% | 0,98 | −34,7%; 0,80%: 8,1% | 0,69 | −38,4% (VN-Index 10,0% | 0,61 | −45,3%).
7. Sức chứa (G2 không lọc, 1.714 lệnh): vốn 1 tỷ → vị thế 50 triệu, 0% lệnh vượt 10% thanh khoản TB 20 phiên; 5 tỷ → 31%; 20 tỷ → 61%; 50 tỷ → 76%. Thanh khoản TB mã lúc mua: phân vị 10% = 1,3 tỷ, 25% = 2,0 tỷ, 50% = 5,9 tỷ.
8. Dữ liệu: đối chiếu giá VCI với KBS (294 mã, 319.678 ngày chung, 2022+, sau quy đổi đơn vị nghìn đồng): lệch trung vị 0,02%; 3,1% số ngày lệch >1%; 11/294 mã lệch có hệ thống (cách điều chỉnh khác nhau). 0,6% số phiên 2016+ có biến động vượt biên độ +2 điểm % (chủ yếu điều chỉnh giá).

## Ý KIẾN (chưa kiểm)
- Kỳ vọng thận trọng 8–13%/năm sau chi phí 0,3–0,5% mỗi chiều, sụt vốn −30% đến −40%: là suy ra từ mục 5–6, không phải số đo trực tiếp.
- Phần "hơn VN-Index" mong manh: 3 năm gần nhất thua, và phần lớn lợi thế trước đó có thể là thiên lệch sống sót.
- Rủi ro đuôi: lãi phụ thuộc vài mã tăng gấp đôi trong vài tuần; một vài năm không bắt được là mất lợi thế.
- Đề xuất tiêu chí dừng cho paper trade (chờ anh chốt): sau 12 tháng, nếu lãi ròng sau chi phí 0,4% mỗi chiều thấp hơn VN-Index quá 5 điểm % VÀ không hơn placebo, bỏ; sụt max paper vượt −35% thì dừng.
