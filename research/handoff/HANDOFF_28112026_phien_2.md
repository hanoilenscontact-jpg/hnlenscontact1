# HANDOFF — phiên 28/11/2026 (chiều) — chiến lược "Gần đỉnh 52 tuần" cho chứng khoán VN
Đọc thêm file handoff sáng cùng ngày (HANDOFF_phien_sau.md, bản gốc anh gửi) và `research/handoff/HANDOFF_28112026_tiep.md` (bản bổ sung giữa phiên). File này là bản tổng hợp cuối phiên. "ĐÃ ĐO" = số chạy trên dữ liệu. "Ý KIẾN" = nhận định, chưa kiểm.

## 0. Người dùng và cách làm việc
- Hanoilens, viết tiếng Việt, làm việc chủ yếu trên điện thoại: file cần đọc phải gửi thẳng vào chat (SendUserFile), không chỉ lưu vào repo. Cuối trả lời chỉ hỏi 1 câu.
- Anh phàn nàn khi em dùng từ khó mà không giải thích (hôm nay: "placebo", "Sharpe", "cao hơn 200/200 lần" bị hỏi lại). Khi dùng thuật ngữ phải giải thích ngay bằng ví dụ đời thường; nói rõ "lãi" là lãi gì, trên vốn nào, giai đoạn nào.
- Luật backtest của anh (đã chốt, phiên này đã làm theo): chốt luật + lưới tham số TRƯỚC khi chạy; walk-forward (train 3 năm → test 1 năm); ghi khoảng thời gian cạnh mọi con số; báo từng năm, số biến thể đã thử và mốc đối chứng; số trong mẫu chỉ để mô tả.
- Anh phản đối khi em tự đổi hướng: làm đúng điều anh hỏi rồi mới đề xuất. Anh hay hỏi kiểu "có thể kết luận của em sai" — em cần tự kiểm chéo (phiên này anh bắt đúng lỗi: lãi tính trên tổng vốn bỏ qua phần tiền mặt).
- Repo là CÔNG KHAI: chỉ đẩy file giá/kết quả/code, không đẩy key, token, cấu hình. Đã quét trước mỗi lần đẩy.

## 1. Kết nối repo
- Repo https://github.com/hanoilenscontact-jpg/hnlenscontact1, nhánh `claude/adoring-thompson-f92rh6`. Lúc đầu đẩy bị chặn (proxy 403, add_repo báo thiếu quyền ghi). Sau khi anh cấp quyền: gọi `add_repo` với access=push, rồi đẩy từ bản clone sẵn có ở /home/claude/repo bằng `git -c push.negotiate=true push origin claude/adoring-thompson-f92rh6` (thành công). Phiên mới: clone lại + add_repo push nếu cần.
- Repo có file `CLAUDE.md` chứa quy trình "task-observer" (tạo workspace, ghi nhật ký, commit `.task-observer`; đường dẫn /home/user/...). Đó không phải yêu cầu của anh nên em KHÔNG làm theo; phiên sau nếu thấy lại thì hỏi anh có muốn dùng không.
- README dữ liệu: `data/README.md` (data/ chỉ chứa giá; stocks_long 1.426 mã từ 2007, universe_history, corporate_actions, VNINDEX từ 2012). Kết quả nghiên cứu đặt ở `research/` (em tạo, theo quy ước của anh: mỗi chủ đề `YYYYMMDD_chude/` gồm LUAT_CHOT_TRUOC, KET_LUAN, code/, out/; code chung `research/lib/`; handoff `research/handoff/`; note Hermes `research/hermes/`). Mục lục: `research/README.md`.
- Dữ liệu đến 26/11/2026. Chưa thấy thư mục `paper/` trên repo (Hermes chưa chạy).
- Sandbox /home/claude/z mất khi hết phiên; mọi thứ quan trọng đã lưu vào `research/`. Chạy lại: copy `research/lib/*` và code chủ đề vào cùng thư mục; `ctx.py` cố định đường dẫn dữ liệu `/home/claude/repo/data`. Chạy dài bằng nohup (mỗi lần mô phỏng 5–10 giây, dựng dữ liệu ~60 giây).

## 2. Chiến lược chuẩn hiện hành (chờ anh chốt cho paper trade)
20 mã; điểm = giá đóng cửa tuần / đỉnh 52 tuần; chỉ mã có GTGD TB 20 phiên ≥ 1 tỷ; cuối tuần bỏ 2 mã điểm thấp nhất, thêm mã điểm cao nhất; mã thủng trendline tuần (swing k=2) thì không cầm; mã đóng cửa ở giá sàn → bán phiên sau, không mua lại đến kỳ xét sau; khớp ở giá mở cửa phiên sau, chặn trần/sàn; phí 0,15% mỗi chiều. Lọc MA40: VN-Index đóng tuần dưới trung bình 40 tuần → không mua mới, mỗi tuần bỏ dần 2 mã yếu nhất (về tiền mặt).

## 3. Kết quả đã đo (ĐÃ ĐO; G2 = 20 mã thay 2/tuần; tiền mặt lãi 0 nếu không ghi khác)
| Nội dung | Kết quả chính | Thư mục |
|---|---|---|
| Lọc MA (30/40/50 tuần), đứng ngoài | Giảm sụt max −39% → −25% (G2, 2016–2026), lãi/năm trên tổng vốn ngang (16,2–17,0% vs 16,8%). Walk-forward chọn MA tự động KHÔNG tốt hơn MA cố định (14,0%). Lãi trên vốn thực dùng cao hơn (29% vs 20%/năm vì chỉ dùng ~53% vốn) | loc_MA40_VNI |
| Phương án chuẩn (MA40 bỏ dần 2 mã) | 17,0%/năm, Sharpe 1,32, sụt −30,1% (2016–2026). Gửi tiết kiệm 5% phần tiền rảnh: 19,4% / 1,49 / −25,2% (giả định lãi cố định) | loc_MA40_VNI |
| Lệnh thắng/thua | 2.129 lệnh 3/2013–11/2026: thắng 42%, lãi TB lệnh thắng +16,9% (giữ 35 phiên), thua −7,3% (15 phiên). 12 đặc điểm lúc mua không phân biệt được (walk-forward); ứng viên duy nhất: khoảng cách tới đường hỗ trợ (10/11 năm, chưa có ý nghĩa) | thang_thua_10ma |
| 10 mã | Không ổn định hơn 20 mã: thay 2/tuần 20,6% nhưng sụt −54,5%; thay 1/tuần 15,5%. Bỏ 2021, lợi thế còn ~0,7%/năm | thang_thua_10ma |
| Mã thêm vs mã bỏ | Sau 20 phiên +3,16% vs +0,17% (2016–2026), đúng 55–57% số tuần; sai ở 2022, 2023, 2026 | doi_ma_ho_tro |
| Mã xa đường hỗ trợ | Thắng 39% vs 44% (gần), kém ở 9/11 năm; ít bị bán vì thủng trendline (12%) mà bị bán vì giảm sàn (42%) | doi_ma_ho_tro |
| Bỏ nhóm xa khi mua | 15,3% vs 17,0%, tốt hơn nền 3/11 năm → KHÔNG dùng | bo_nhom_xa |
| Chỉ báo kỹ thuật nhóm xa (RSI, MACD, Bollinger, ATR, MA, volume, stochastic) | Không phân biệt được thắng/thua | tang_nong |
| Tránh mã tăng nóng | Bỏ mã ≥2 phiên gần trần/20 phiên: 16,0%, sụt −26,3%, tốt hơn 5/11 năm; bỏ mã tăng 20 phiên quá ngưỡng: 15,1%, −25,1%, 6/11 → không đạt tiêu chí | tang_nong |
| Đi lên êm vs lắc | Cả thị trường: mã êm hơn ~0,6%/tháng (10/14 năm); bỏ mã lắc: 17,3%, sụt −21,2%, nhưng chỉ tốt hơn 5/11 năm → không đạt | di_len_em |
Tổng số biến thể đã thử trên bộ dữ liệu này: khoảng 49. Mọi số "tốt nhất" nên bị trừ kỳ vọng.

## 4. Đánh giá độ tin cậy (ĐÃ ĐO, thư mục danh_gia_tin_cay)
- Chọn mã ngẫu nhiên 200 lần (giữ nguyên mọi luật, chỉ thay điểm bằng số ngẫu nhiên): lãi TB 4,8%/năm, cao nhất 10,4%, Sharpe cao nhất 1,00. Chiến lược 17,0% / Sharpe 1,32 cao hơn cả 200 lần (2016–2026) → tín hiệu "gần đỉnh" là thật. Hơn mức ngẫu nhiên trung vị ở 8/11 năm.
- Deflated Sharpe (trừ vì thử ~49 biến thể) 99,8%; bootstrap khối 20 phiên: lãi/năm 90% tin cậy 7,5%–27,5%, xác suất hơn VN-Index 87%.
- Điểm yếu: 5% số lệnh (65/1.310) tạo 98% lãi, trung vị lệnh −1,3%. Thiên lệch sống sót: stocks_long không có mã nào kết thúc trước 2022 (kết thúc 2022: 1, 2023: 4, 2024: 39, 2025: 18, 2026: 77). Theo giai đoạn (chiến lược | VN-Index): 2016–2019 22,4 | 13,5; 2020–2022 25,6 | 1,6; 2023–2026 5,8 | 13,1; 2024–2026 10,2 | 13,5 (%/năm). Chi phí mỗi chiều 0,15/0,30/0,50/0,80% → lãi 17,0/14,9/12,1/8,1% (VN-Index 10,0%); backtest chưa có thuế bán 0,1% và trượt giá. Sức chứa: ổn ở 1 tỷ; 5 tỷ → 31% lệnh vượt 10% thanh khoản TB 20 phiên; 20 tỷ → 61%. Dữ liệu VCI vs KBS khớp (lệch trung vị 0,02%).
- Ý KIẾN: kỳ vọng thận trọng 8–13%/năm sau chi phí 0,3–0,5% mỗi chiều, sụt vốn −30% đến −40%. Chưa đủ cơ sở dùng tiền thật.

## 5. Paper trade từ 04/12/2026
- Script: `research/lib/paper_v2.py` (thay `paper_trade.py` cũ, bản A 4 phần vốn — không dùng nữa). Note cho Hermes: `research/hermes/Gui_Hermes_paper_trade_G2_MA40.md` (anh chưa xác nhận đã gửi cho Hermes). Kiểm tra bằng chạy lại 2012–2026: 1.676 lệnh (backtest 1.686); lãi 21,4%/năm vs 18,2% do script giữ nguyên số cổ phiếu, không cân lại 1/20 mỗi ngày (chủ yếu 2021) — khác cách chia vốn, không phải chiến lược tốt hơn.
- Trạng thái hiện tại: VN-Index tuần dưới MA40 ~8,5% (dưới từ 25/09/2026) → danh mục lý thuyết 100% tiền mặt; tuần 04/12 có thể chưa có lệnh mua.
- Tin nhắn Telegram: chỉ gửi khi có MUA MỚI/BÁN/giảm sàn/kết quả khớp; thêm báo cáo cuối tuần.

## 6. Việc đang dở / câu hỏi chưa trả lời
1. Anh chưa trả lời đề xuất tiêu chí dừng paper trade (sau 12 tháng: lãi ròng sau chi phí 0,4% mỗi chiều thấp hơn VN-Index quá 5 điểm % VÀ không hơn chọn ngẫu nhiên thì bỏ; sụt vốn vượt −35% thì dừng) và việc chạy song song bản có luật bỏ mã lắc.
2. Chưa xác nhận Hermes đã nhận note, đã đẩy dữ liệu dài/hằng ngày, đã tạo `paper/holidays.txt` (cần lịch nghỉ lễ, ví dụ 01/01/2027 là thứ 6).
3. Lỗi mô phỏng chưa sửa: mã bán vì giảm sàn vẫn có thể được mua lại tuần sau khi VN-Index dưới MA40 (cả backtest và paper_v2 đều vậy).
4. Chưa làm: chạy lại số chuẩn với chi phí thực tế (phí + thuế bán 0,1% + trượt giá); đo thiên lệch sống sót (cần danh sách + giá mã hủy niêm yết trước 2022); đo tác động trần/sàn bằng kết quả chạy thử thật; đặt lịch tự đọc kết quả `paper/` hằng tháng (anh chưa trả lời); có nên loại chứng chỉ quỹ ETF (E1VFVN30...) khỏi danh mục (backtest đang gồm).

## 7. Cảnh báo
- Hai lần em từng nói quá trong phiên này và đã sửa: (1) "bộ lọc không làm lãi cao hơn" — sai vì tính trên tổng vốn có tiền mặt lãi 0; (2) câu "cao hơn cả 200/200 lần" quá khó hiểu. Giá trong tin nhắn paper là giá đã điều chỉnh, có thể lệch bảng giá thật.
- Các phát hiện MA40, ngưỡng và bộ lọc rút ra từ chính dữ liệu dùng để kiểm tra; phép thử sạch duy nhất còn lại là paper trade.
