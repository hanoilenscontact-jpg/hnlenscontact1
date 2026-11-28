# lib — code dùng chung
- `vn_gate.py`, `factor_lab.py`, `daily_exec.py`, `exit_rules.py`: từ handoff phiên trước (mô phỏng khớp lệnh ATO, trần/sàn, trendline).
- `er2.py`: `simulate` có ghi tỷ lệ vốn đang dùng. `er3.py`: thêm ghi từng lệnh (mã, ngày vào/ra, giá, lý do bán). Đặt `er3.N` = số mã.
- `ctx.py` dựng bảng tuần/ngày (đường dẫn dữ liệu cố định `/home/claude/repo/data`, sửa nếu clone chỗ khác); `ctx_funcs.py` thêm cờ VN-Index > MA40 và hàm chọn mã G (N, k, shrink).
- Chạy: copy lib và code của chủ đề vào cùng một thư mục, `python3 <file>.py` (chạy nền bằng nohup, mỗi lần 2–4 phút).
