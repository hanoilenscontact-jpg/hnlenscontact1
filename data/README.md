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
