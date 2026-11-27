# Luật chốt trước — bộ lọc VN-Index dưới MA tuần (28/11/2026)

Chốt TRƯỚC khi chạy, không sửa sau khi thấy kết quả.

- Chiến lược gốc (giữ nguyên mọi quy tắc trong handoff mục 3):
  - G2: 1 danh mục 20 mã, mỗi tuần thay 2 mã yếu nhất, trendline tuần + bán giảm sàn.
  - A+D: 4 phần vốn, review 4 tuần/phần, trendline tuần + bán giảm sàn (đối chứng phụ).
- Bộ lọc: cuối tuần (thứ 6), nếu giá đóng cửa tuần của VN-Index < trung bình L tuần gần nhất
  thì mục tiêu = không cầm mã nào: bán hết ATO phiên sau (mở ở sàn thì treo, thử lại), không mua mới.
  Khi VN-Index đóng tuần trở lại trên MA thì mua lại theo danh mục mục tiêu tuần đó.
  Tiền mặt lãi 0 (không tính lãi gửi).
- Lưới tham số (duy nhất): L ∈ {không lọc, 30, 40, 50} tuần → 4 biến thể mỗi chiến lược gốc.
- Walk-forward: train 3 năm dương lịch liền trước → chọn L có Sharpe cao nhất → áp cho năm test kế tiếp.
  Năm test: 2016–2026 (dữ liệu bắt đầu 3/2013, nên cửa sổ train đầu là 2013–2015).
- Báo cáo: từng năm; số gộp ghi rõ khoảng thời gian; mốc đối chứng = chiến lược không lọc, VN-Index,
  và VN-Index có cùng bộ lọc (để biết lợi ích đến từ chọn mã hay chỉ từ né thị trường).
- Số MA40/MA50 cố định trên toàn kỳ = số trong mẫu, chỉ để mô tả.
