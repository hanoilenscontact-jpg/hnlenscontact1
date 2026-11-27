# Data giá chứng khoán VN — xuất cho kiểm tra "công thị trường"

Xuất ngày 2026-11-26. Repo PUBLIC, chỉ chứa file giá — KHÔNG có key/token.

## data/VNINDEX.csv
VN-Index giá ngày. Cột: date,open,high,low,close,volume (giá điểm, volume cổ phiếu).
Phạm vi: **2012-01-03 → 2026-11-26** (gộp 2 nguồn: backfill VCI đến 13/11 + price_db hàng ngày đến 26/11).
Lưu ý: yêu cầu từ 28/07/2000 nhưng KHÔNG có nguồn local nào có data trước 2012 — chỉ xuất được từ 2012.

## data/stocks/<MA>.csv
Giá ngày của từng mã, từ price_db (`/data/.hermes/scripts/price_db`) — dữ liệu fetch từ KBS API,
cập nhật hằng ngày (cron 19:30). Cột: date,open,high,low,close,volume.
- **341 mã** — toàn bộ mã còn trong universe KBS.
- Lịch sử bắt đầu **2020-01-01** (giới hạn của nguồn KBS, không phải 2000).
- **30 mã bị KBS gỡ khỏi universe từ 26/11/2026** (small/mid cap) nên KHÔNG có trong xuất này:
  ELE HOA KCJ NAM RHC SEC SFD SFE TLC TLE TTJ TWG VCH VCV VHI VKP VNN VPK VPM VRO WCT WGC XTL YEN ZGC ZIG ZJL ZNG ZPC ZTC.
- **Mã hủy niêm yết: KHÔNG có** — price_db chỉ chứa mã đang trong universe hiện tại của KBS.
- Điều chỉnh chia tách/cổ tức: update_price_db có logic phát hiện corporate action (|Δclose| > 10% → fetch lại full)
  nhưng KHÔNG có nhãn cột nào xác nhận từng dòng đã điều chỉnh. Người kiểm tra nên tự cross-check
  các ngày cổ_div/split với giá để tránh lệch cơ sở.

## data/v6_signals.csv
Lịch sử tín hiệu V6 đã phát: date,symbol (mỗi dòng 1 tín hiệu mua, chon=1).
Phạm vi: **2026-11-13 → 2026-11-25** (hệ V6 mới bắt đầu chạy từ 13/11/2026) — 17 tín hiệu.


## Update 2026-11-27: dữ liệu toàn thị trường (thêm 4 nhóm file)

- `universe_history.csv`: 1521 mã ({'dang_giao_dich': 1295, 'huy_dang_ky_gd': 97, 'chuyen_san': 65, 'huy_bat_buoc': 64}) — nguồn Vietstock corporateaz API + 30 mã KBS gỡ.
  first_date/last_date lấy từ data thật; mã không fetch được data để trống.
- `stocks_delisted/`: 159 file (226 mã hủy/chuyển từ Vietstock + 30 mã KBS gỡ; 94 mã VCI không serve giá → chỉ có trong universe).
  Giá 2020-01-01 → phiên cuối (VCI).
- `stocks_long/`: 1426 file, lịch sử từ ~2007-11-15 (hoặc ngày GD đầu) → 2026-11-26 (raw VCI gap-chart API, countBack=10000).
- `corporate_actions.csv`: 9998 sự kiện / 1237 mã (ex_date, type, ratio). Type: DIV=co_tuc_tien, ISS=phat_hanh_quyen hoặc cổ tức bằng cổ phiếu (VCI không phân biệt rõ 2 loại trong event_code).
  GIỚI HẠN: nguồn là VCI events, chỉ trả ~50 sự kiện gần nhất/mã — với mã ít sự kiện có thể phủ sâu; mã nhiều giao dịch nội bộ sẽ chỉ có từ ~2022 trở lại. KHÔNG phải lịch sử đầy đủ 2020-2026.
- 95 mã không fetch được giá nào (niêm yết mới chưa GD, hoặc VCI rỗng): xem universe_history first_date trống.

**Điều chỉnh giá (README quan trọng):** giá stocks_long/stocks_delisted từ VCI gap-chart ("gap-chart" = bỏ gap cổ tức/split) — so khớp giá hiện tại với price_db KBS là khớp, tức có dấu hiệu đã điều chỉnh. NHƯNG không có nhãn điều chỉnh từng dòng — để kiểm tra chính xác, đối chiếu với corporate_actions.csv (đặc biệt 71 mã có phiên nhảy >15,5%).
