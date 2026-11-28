# Gửi Hermes — chạy thử trên giấy (paper trade) chiến lược "Gần đỉnh 52 tuần, 20 mã, lọc MA40"
Ngày soạn 28/11/2026. Bắt đầu từ thứ 6 04/12/2026. Chỉ chạy thử trên giấy, KHÔNG đặt lệnh thật.
Nhiệm vụ: mỗi ngày giao dịch (1) cập nhật giá, (2) chạy 1 script có sẵn, (3) gửi tin nhắn Telegram cho anh Hanoilens mỗi khi có mã MUA MỚI hoặc BÁN mã cũ, (4) đẩy thư mục `paper/` lên GitHub. KHÔNG tự sửa quy tắc, không tự tính lại bằng cách khác.

## 1. Chiến lược (script đã làm sẵn, Hermes chỉ cần chạy)
- 20 mã, mỗi mã 1/20 giá trị danh mục (làm tròn lô 100 cp). Vốn giả định 1 tỷ đồng. Chỉ xét mã có giá trị giao dịch TB 20 phiên ≥ 1 tỷ đồng/phiên.
- Điểm = giá đóng cửa tuần / đỉnh cao nhất 52 tuần. Cuối mỗi tuần (thứ 6, hoặc phiên cuối tuần nếu thứ 6 nghỉ lễ): bỏ 2 mã điểm thấp nhất, thêm mã điểm cao nhất chưa có cho đủ 20. Mã thủng trendline tuần thì không cầm.
- Lọc thị trường: nếu VN-Index đóng cửa tuần DƯỚI trung bình 40 tuần (MA40) → không mua mới, mỗi tuần bỏ dần 2 mã yếu nhất (về tiền mặt dần). Khi VN-Index lên lại TRÊN MA40 → mua lại đủ 20 mã.
- Hằng ngày: mã nào đóng cửa ở giá sàn → bán ở giá mở cửa phiên sau và không mua lại cho đến kỳ xét tuần sau.
- Mọi lệnh khớp ở GIÁ MỞ CỬA phiên kế tiếp. Mở cửa ở giá trần (lệnh mua) hoặc giá sàn (lệnh bán) → coi như chưa khớp, thử lại phiên sau. Phí 0,15% mỗi chiều. Biên độ: HOSE 7%, HNX 10%, UPCoM 15%.
- Hiện tại VN-Index đang dưới MA40 tuần khoảng 8% (đã dưới từ cuối 09/2026) và script chạy lại quá khứ cho thấy danh mục thực tế đang 100% tiền mặt. Vì vậy tuần đầu 04/12 và nhiều tuần sau có thể KHÔNG có lệnh mua nào. Đó là hành vi đúng, không phải lỗi; chỉ báo lỗi nếu script báo lỗi.

## 2. Cài đặt (làm 1 lần)
1. `git pull` repo (nhánh `claude/adoring-thompson-f92rh6`). Script nằm ở `research/lib/paper_v2.py` (cùng thư mục với `factor_lab.py`, `vn_gate.py` — không tách riêng). Cần Python 3 với pandas, numpy.
2. Chạy thử 1 lần để kiểm tra (không ảnh hưởng dữ liệu thật):
   `python3 research/lib/paper_v2.py --data data --out /tmp/paper_test --start 2025-06-06 --asof 2025-06-27`
   Kết quả đúng: in dòng `xong 2025-06-27 | ngay xu ly: 16 | dang giu: 16 | gia tri: 1007479200`. Sau đó xóa `/tmp/paper_test`. Báo anh nếu số khác.
3. Tạo file `paper/holidays.txt` (mỗi dòng 1 ngày YYYY-MM-DD) liệt kê các ngày nghỉ giao dịch sắp tới của HOSE/HNX, tra theo lịch nghỉ chính thức của sàn (ví dụ 01/01/2027 là thứ 6 nghỉ Tết dương lịch; cần thêm Tết Âm lịch 2027 và các ngày lễ khác khi sàn công bố). Mục đích: khi thứ 6 nghỉ, script biết phiên cuối tuần là thứ 5. Cập nhật file này mỗi khi có lịch mới.

## 3. Việc mỗi ngày giao dịch (sau khi có giá đóng cửa, khoảng 19:45, sau cron cập nhật 19:30)
1. Cập nhật giá cho `data/VNINDEX.csv` và `data/stocks_long/<MA>.csv`: THÊM dòng của ngày mới (cột date,open,high,low,close,volume, cùng đơn vị với các dòng cũ), từ cùng nguồn VCI đã dùng để xuất stocks_long. Chỉ thêm, không ghi đè lịch sử. Mã nào mở cửa lệch hơn 10% so với đóng cửa hôm trước (nghi chia tách/cổ tức) → tải lại toàn bộ lịch sử mã đó từ VCI (giá đã điều chỉnh). Mã không có dữ liệu hôm nay (ngừng giao dịch) → để nguyên, đừng tự điền.
2. Chạy từ thư mục gốc repo:
   `python3 research/lib/paper_v2.py --data data --out paper --start 2026-12-04`
   Lần đầu (04/12 tối) tạo `paper/state.json`; các ngày sau script tự đọc state và xử lý mọi phiên chưa xử lý (nếu lỡ ngày nào, ngày sau chạy bù đúng thứ tự). KHÔNG sửa tay `state.json`.
3. Nếu có file `paper/messages/YYYY-MM-DD_tin_nhan.txt` của ngày hôm nay → gửi nguyên văn nội dung qua Telegram cho anh (Telegram giới hạn 4096 ký tự: nếu dài hơn, cắt theo dòng thành nhiều tin). File này chỉ tồn tại khi có việc cần báo: (a) tín hiệu cuối tuần có MUA MỚI/BÁN (kèm lý do, hạng, giá đóng cửa, số cổ phiếu đề xuất), (b) kết quả khớp lệnh paper ở phiên mở cửa kế tiếp, (c) cảnh báo BÁN do giảm sàn. Nếu không có file → không gửi gì.
4. Mỗi thứ 6 (hoặc phiên cuối tuần) gửi thêm nội dung `paper/messages/bao_cao_ngay_<ngày>.txt` (giá trị danh mục, so với VN-Index, danh sách đang giữ).
5. Đẩy lên GitHub: `git add paper data && git commit -m "paper trade <ngày>" && git push`. Repo là CÔNG KHAI: chỉ đẩy thư mục `paper/` và file giá `data/`; tuyệt đối không đẩy key, token, cấu hình.

## 4. File script tạo ra (trong paper/)
`state.json` (trạng thái, đừng sửa), `equity.csv` (giá trị danh mục từng ngày so với VN-Index), `orders.csv` (mọi tín hiệu và lần khớp/chưa khớp, kể cả chưa khớp vì giá trần/sàn), `trades.csv` (lệnh đã đóng: giá vào/ra, lãi lỗ ròng, lý do), `holdings.csv` (đang giữ), `messages/`.

## 5. Giới hạn cần nhớ (đã ghi trong tin nhắn)
Giá lấy từ dữ liệu đã điều chỉnh nên có thể lệch nhẹ so với bảng giá thật; giả định khớp ở giá mở cửa; không tính thuế, cổ tức tiền mặt, T+2, lãi gửi tiền mặt; danh mục có cả chứng chỉ quỹ ETF (như E1VFVN30) vì backtest cũng gồm. Mọi lỗi/ngoại lệ (script báo lỗi, dữ liệu thiếu): báo anh bằng tin nhắn nêu rõ, đừng tự đổi quy tắc.
