# Luật chốt trước — chỉ báo kỹ thuật nhóm xa; tránh mã tăng nóng (28/11/2026)
Nền: 20 mã, thay 2/tuần, trendline, giảm sàn, MA40 bỏ dần. Năm test 2016–2026.

Phần A — 8 chỉ báo trên lệnh nhóm xa (cùng 449+ lệnh, giá đến phiên trước ngày mua):
rsi14 (RSI 14 phiên, Wilder); macdh (MACD 12/26/9 histogram chia giá); pctb (Bollinger %B 20 phiên, 2 độ lệch chuẩn); atr (ATR14 chia giá); d_ma20, d_ma50 (giá/MA − 1); vr5 (khối lượng TB 5 phiên / TB 20 phiên); stoch (Stochastic %K 14).
Walk-forward như trước (3 nhóm, nhóm xấu từ 3 năm train, đúng dấu ≥ 8/10 năm). Ngẫu nhiên kỳ vọng ~0,9/8.

Phần B — 2 biến thể danh mục, áp cho MỌI mã mua mới (bỏ qua, lấy mã hạng kế tiếp; mã đang giữ không bị ảnh hưởng). Chỉ báo tính đến phiên cuối tuần tín hiệu:
B1 "phiên trần": bỏ mã có ≥ 2 phiên tăng ≥ 90% biên độ trong 20 phiên gần nhất (mức cố định, chốt trước, không tối ưu).
B2 "tăng nóng": bỏ mã có lãi 20 phiên > phân vị 67% lãi 20 phiên lúc vào lệnh của chiến lược nền trong 3 năm trước (walk-forward).
Báo từng năm, gộp 2016–2026, Sharpe, sụt max, bản gửi 5%; so với nền và VN-Index. Tiêu chí dùng: lãi/năm hơn nền VÀ tốt hơn ≥ 7/11 năm.
