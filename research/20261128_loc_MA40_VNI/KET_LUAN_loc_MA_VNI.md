# Kết luận: VN-Index dưới MA tuần thì đứng ngoài — có tốt hơn không? (28/11/2026)

Luật chốt trước: xem `LUAT_CHOT_TRUOC_regime.md`. Code: `regime_filter.py`, `regime_wf.py`. Dữ liệu: repo commit 1c42aec (27/11).

## Cách làm
- Cuối tuần (thứ 6), nếu VN-Index đóng cửa tuần dưới trung bình L tuần → bán hết ATO phiên sau, không mua. Trở lại trên MA → mua lại danh mục tuần đó. Tiền mặt lãi 0.
- L ∈ {không lọc, 30, 40, 50} tuần, áp lên 2 chiến lược: G2 (thay 2 mã/tuần) và A+D (4 phần vốn). 8 lần chạy mới.
- Walk-forward (WF): mỗi năm, nhìn 3 năm trước, chọn L có Sharpe cao nhất, áp cho năm sau. Năm test 2016–2026.
- Sharpe = lãi chia cho độ dao động (càng cao càng "êm"). Sụt max = mức tụt lớn nhất từ đỉnh vốn xuống đáy.

## ĐÃ ĐO — G2, lãi từng năm (%)
| Năm | Không lọc | MA30 | MA40 | MA50 | WF | WF chọn | VNI | VNI+MA40 |
|---|---|---|---|---|---|---|---|---|
| 2016 | 21.2 | 12.9 | 10.9 | 9.8 | 21.2 | không lọc | 14.8 | 14.5 |
| 2017 | 59.5 | 59.5 | 59.5 | 59.5 | 59.5 | không lọc | 48.0 | 48.0 |
| 2018 | -4.8 | 6.3 | 3.2 | 1.0 | -4.8 | không lọc | -9.3 | -3.5 |
| 2019 | 24.2 | 16.0 | 13.9 | 12.8 | 16.0 | 30 | 7.7 | -7.7 |
| 2020 | 45.0 | 33.0 | 33.5 | 34.4 | 33.0 | 30 | 14.9 | 19.6 |
| 2021 | 73.1 | 73.1 | 73.1 | 73.1 | 73.1 | 30 | 35.7 | 35.7 |
| 2022 | -27.5 | -13.9 | -13.9 | -13.9 | -27.5 | không lọc | -32.8 | -8.1 |
| 2023 | -4.4 | -5.6 | -3.8 | -7.8 | -7.8 | 50 | 12.2 | -1.0 |
| 2024 | 23.1 | 17.2 | 18.4 | 22.1 | 18.4 | 40 | 12.1 | 4.3 |
| 2025 | 27.1 | 21.9 | 21.9 | 19.2 | 21.9 | 40 | 40.9 | 32.7 |
| 2026 (đến 26/11) | -12.5 | -7.1 | -10.4 | -10.8 | -12.5 | không lọc | -8.7 | -10.0 |

Gộp 2016–2026 (11 năm test):
| G2 | Lãi/năm | Sharpe | Sụt max |
|---|---|---|---|
| Không lọc | 16.8% | 1.19 | -38.7% |
| MA30 cố định | 17.0% | 1.37 | -25.4% |
| MA40 cố định | 16.2% | 1.32 | -24.5% |
| MA50 cố định | 15.4% | 1.25 | -27.6% |
| Walk-forward | 14.0% | 1.06 | -39.1% |
| VN-Index | 10.0% | 0.61 | -45.3% |
| VN-Index + MA40 | 9.8% | 0.76 | -30.5% |

A+D, gộp 2016–2026: không lọc 13.3% / Sharpe 0.97 / sụt −39.0%; MA40 12.8% / 1.05 / −24.6%; WF 12.8% / 1.00 / −27.6%.

Thời gian đứng ngoài (3/2013–11/2026): MA30 33% số tuần, 61 lần chuyển; MA40 32%, 49 lần; MA50 30%, 47 lần.

## Đọc kết quả
1. (ĐÃ ĐO) Lọc MA cố định giảm sụt max rõ: −39% → −25% đến −28%, cả 3 mức L, cả 2 chiến lược. Lãi/năm gần như không đổi (±1%). Lợi chủ yếu ở 2018 và 2022.
2. (ĐÃ ĐO) Cái giá: mất lãi ở năm thị trường lắc (2016, 2019, 2020, 2025: mất 5–12%/năm). 2023 vẫn lỗ dù có lọc.
3. (ĐÃ ĐO) Walk-forward KHÔNG xác nhận: G2 WF 14.0%/Sharpe 1.06 — kém cả bản không lọc. Lý do: sau 3 năm tăng 2019–2021, bộ lọc trông "tốn tiền" nên WF chọn không lọc đúng năm 2022 (−27.5%).
4. (ĐÃ ĐO) VN-Index tự áp MA40 cũng giảm sụt từ −45% xuống −30% → phần lớn lợi ích là né thị trường xấu, không riêng gì chiến lược gần đỉnh 52 tuần.
5. (ĐÃ ĐO) MA30/40/50 cho kết quả gần nhau → không có mức "đặc biệt".

## Ý KIẾN (chưa kiểm)
- Số MA cố định là trong mẫu: ý tưởng lọc VNI<MA40 ra đời từ bảng dist_high trên chính dữ liệu này. Chỉ dùng để mô tả.
- Nếu tính lãi tiền gửi ~5%/năm cho ~32% thời gian cầm tiền, ước chừng cộng thêm ~1,5%/năm (phép nhân thô, chưa chạy).
- Nếu muốn dùng, nên coi đây là công cụ giảm sụt vốn (chốt trước một mức, ví dụ MA40, không tối ưu lại), không phải công cụ tăng lãi.

Số biến thể đã thử trên bộ dữ liệu này: khoảng 30 (phiên trước) + 8 (phiên này) = khoảng 38.

---
## Bổ sung 28/11 (sau góp ý của anh): lãi trên vốn đã dùng + phương án "bỏ dần 2 mã"

Phương án mới (chốt trước, 1 biến thể, MA40 cố định, k=2): VN-Index dưới MA40 → không mua mã mới (kể cả mã quay lại trên trendline), mỗi tuần bán 2 mã điểm thấp nhất đang cầm, vẫn giữ luật trendline và giảm sàn. Trên MA40 → G2 bình thường, lấp lại đủ 20 mã.

"Vốn dùng TB" = trung bình % vốn đang nằm trong cổ phiếu mỗi phiên. "Lãi trên vốn dùng" = lãi/năm chỉ tính trên phần tiền đang cầm cổ phiếu, chỉ tính những phiên có cầm.

| G2, 2016–2026 | Lãi/năm trên tổng vốn | Sharpe | Sụt max | Vốn dùng TB | Lãi/năm trên vốn dùng |
|---|---|---|---|---|---|
| Không lọc | 16.8% | 1.19 | -38.7% | 75% | 19.8% |
| MA40 bán hết | 16.2% | 1.32 | -24.5% | 53% | 29.0% |
| MA40 bỏ dần 2 mã | 17.0% | 1.32 | -30.1% | 57% | 25.0% |

| G2, 3/2013–11/2026 (trong mẫu) | Tổng vốn | Sharpe | Sụt max | Vốn dùng | Trên vốn dùng |
|---|---|---|---|---|---|
| Không lọc | 19.3% | 1.28 | -38.7% | 75% | 24.4% |
| MA40 bán hết | 17.3% | 1.31 | -24.5% | 54% | 31.3% |
| MA40 bỏ dần 2 mã | 18.2% | 1.32 | -30.1% | 59% | 29.1% |

Từng năm (lãi trên tổng vốn % | vốn dùng TB %):
| Năm | Không lọc | MA40 bán hết | MA40 bỏ dần 2 mã |
|---|---|---|---|
| 2013 | 25.4 / 74 | 21.3 / 72 | 25.2 / 73 |
| 2014 | 27.6 / 71 | 38.1 / 63 | 32.9 / 68 |
| 2015 | 29.4 / 78 | 4.2 / 36 | 8.1 / 51 |
| 2016 | 21.2 / 82 | 10.9 / 58 | 16.0 / 60 |
| 2017 | 59.5 / 85 | 59.5 / 85 | 59.5 / 85 |
| 2018 | -4.8 / 72 | 3.2 / 33 | -0.5 / 36 |
| 2019 | 24.2 / 78 | 13.9 / 58 | 21.6 / 64 |
| 2020 | 45.0 / 74 | 33.5 / 30 | 37.7 / 39 |
| 2021 | 73.1 / 84 | 73.1 / 84 | 74.3 / 83 |
| 2022 | -27.5 / 59 | -13.9 / 20 | -17.6 / 22 |
| 2023 | -4.4 / 71 | -3.8 / 33 | -6.2 / 39 |
| 2024 | 23.1 / 73 | 18.4 / 66 | 22.7 / 73 |
| 2025 | 27.1 / 77 | 21.9 / 68 | 21.0 / 73 |
| 2026 | -12.5 / 68 | -10.4 / 49 | -10.7 / 56 |

Sửa lại kết luận: câu "không làm lãi cao hơn" chỉ đúng khi tính trên TỔNG vốn với tiền mặt lãi 0. Tính trên vốn thực sự dùng thì bộ lọc hiệu quả hơn rõ (29% so với 20%/năm, 2016–2026). Lợi thế này chỉ thành tiền thật nếu phần tiền mặt được dùng vào việc khác (gửi tiết kiệm, hoặc tăng tỷ trọng khi trên MA).
Ghi chú kỹ thuật: mã bị bán vì giảm sàn vẫn có thể mua lại ở tuần sau nếu còn trong danh mục mục tiêu (cách mô phỏng cũ, chưa sửa).
Số biến thể tổng cộng: khoảng 39.

---
## Bổ sung 2: tiền mặt rảnh gửi tiết kiệm 5%/năm (chốt trước 1 mức duy nhất, tính lãi theo ngày lịch)

| G2, 2016–2026 | Tiền mặt lãi 0%: lãi/năm / Sharpe / sụt max | Gửi 5%: lãi/năm / Sharpe / sụt max |
|---|---|---|
| Không lọc | 16.8% / 1.19 / -38.7% | 18.2% / 1.28 / -36.7% |
| MA40 bán hết | 16.2% / 1.32 / -24.5% | 18.8% / 1.51 / -19.5% |
| MA40 bỏ dần 2 mã | 17.0% / 1.32 / -30.1% | 19.4% / 1.49 / -25.2% |

3/2013–11/2026 (trong mẫu): không lọc 20.7%, MA40 bán hết 19.9%, MA40 bỏ dần 2 mã 20.5%.
Từng năm 2022: không lọc -26.1%, bán hết -10.6%, bỏ dần -14.5%. Từng năm 2023: -3.0 / -0.7 / -3.3. 2026: -11.3 / -8.4 / -9.0.
Giả định: lãi 5% cố định cả kỳ (thực tế lãi gửi VN thấp hơn ở 2020–2021), không tính thuế, không phí rút. Số biến thể tổng: khoảng 39 (lãi gửi chỉ là cách tính lại, không phải biến thể mới).
