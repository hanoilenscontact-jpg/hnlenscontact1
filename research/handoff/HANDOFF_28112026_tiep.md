# Handoff bổ sung 28/11/2026 (nối tiếp HANDOFF_phien_sau.md 28/11 sáng)
Mọi phép thử đều chốt luật trước (file LUAT_CHOT_TRUOC_*.md trong từng thư mục), walk-forward năm test 2016–2026, số liệu ghi rõ khoảng thời gian. Tổng số biến thể đã thử trên bộ dữ liệu này: khoảng 49. Số "tốt nhất" nên bị trừ kỳ vọng.

## Kết quả (ĐÃ ĐO)
1. Lọc MA40 (loc_MA40_VNI): VN-Index dưới MA40 → đứng ngoài giảm sụt max −39% → −25% (G2, 2016–2026), lãi/năm trên tổng vốn ngang. Walk-forward chọn L tự động KHÔNG tốt hơn MA cố định. Phương án "không mua mới + bỏ dần 2 mã/tuần dưới MA40": 17,0%/năm, Sharpe 1,32, sụt −30,1%; gửi 5% phần tiền rảnh: 19,4%/1,49/−25,2%. Lãi trên vốn thực dùng cao hơn rõ.
2. Lệnh thắng/thua + 10 mã (thang_thua_10ma): 2.129 lệnh, thắng 42%, lãi TB +16,9% vs −7,3%. 12 đặc điểm lúc mua không phân biệt được thắng/thua (walk-forward). 10 mã không ổn định hơn 20 mã; hơn chủ yếu nhờ 2021 và thay 2 mã/tuần, sụt max −50% đến −55%.
3. Đổi mã (doi_ma_ho_tro): mã thêm vào hơn mã bị bỏ ~3%/tháng (+3,16% vs +0,17% sau 20 phiên); luật sai ở 2022, 2023, 2026. Mã xa đường hỗ trợ: thắng 39% vs 44%, kém ở 9/11 năm, ít bị bán vì thủng trendline (12%) mà bị bán vì giảm sàn (42%).
4. Bỏ nhóm xa đường hỗ trợ (bo_nhom_xa): lãi 15,3% vs 17,0%, tốt hơn nền 3/11 năm → không dùng. Chỉ báo kỹ thuật trong nhóm xa (RSI, MACD, Bollinger...) không phân biệt được (tang_nong/tech).
5. Tránh mã tăng nóng (tang_nong): B1 bỏ mã ≥2 phiên gần trần/20 phiên: 16,0%, sụt −26,3%, 5/11 năm; B2 bỏ mã tăng 20 phiên quá ngưỡng: 15,1%, sụt −25,1%, 6/11 năm. Không đạt tiêu chí.
6. Độ êm (di_len_em): cả thị trường, mã đi êm (ER60) hơn mã lắc ~0,6%/tháng, 10/14 năm; bỏ mã lắc trong danh mục: 17,3%, sụt −21,2%, nhưng chỉ tốt hơn 5/11 năm → không đạt tiêu chí.

## Chưa làm / quyết định mở
- Anh chưa chốt phương án chạy thử trên giấy từ 4/12 (đề xuất: 20 mã + MA40 bỏ dần 2 mã/tuần; có thể chạy song song thêm bản có luật bỏ mã lắc). Chưa sửa paper_trade.py và note Hermes.
- Lỗi mô phỏng chưa sửa: mã bán vì giảm sàn có thể được mua lại tuần sau khi VN-Index dưới MA40.
- Tiền mặt gửi 5% là giả định cố định cả kỳ, chưa trừ thuế/phí.
- Hermes: chưa thấy thư mục paper/ trên repo (kiểm ngày 28/11).
