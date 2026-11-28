"""
CHAY THU TREN GIAY (paper trade) - "Gan dinh 52 tuan", 20 ma, thay 2 ma yeu nhat/tuan, trendline tuan,
ban giam san, loc VN-Index MA40 tuan (duoi MA40: khong mua moi, bo dan 2 ma/tuan).
Khong dat lenh that. Cung logic voi backtest 'G2 MA40 bo dan 2 ma' (research/20261128_loc_MA40_VNI).

Cach chay moi ngay sau khi du lieu gia dong cua da cap nhat (xem HERMES_PAPER_TRADE.md):
  python3 paper_v2.py --data data --out paper
Chay lai qua khu de kiem tra (khong gui tin nhan): --start 2012-01-02 --out /tmp/replay --no-msg --asof 2026-11-26
"""
import argparse, json, os, sys
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factor_lab as fl
from vn_gate import swing_gate

N, K_REPL, MIN_VALUE, FEE, LOT = 20, 2, 1e9, 0.0015, 100
LIMIT = {"HOSE": 0.07, "HNX": 0.10, "UPCOM": 0.15}

ap = argparse.ArgumentParser()
ap.add_argument("--data", required=True)
ap.add_argument("--out", default="paper")
ap.add_argument("--start", default="2026-12-04")
ap.add_argument("--asof", default=None)
ap.add_argument("--capital", type=float, default=1e9)
ap.add_argument("--no-msg", action="store_true")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True); os.makedirs(f"{a.out}/messages", exist_ok=True)
fl.END = a.asof or "2100-01-01"

# ---------------- du lieu ----------------
idx = pd.read_csv(f"{a.data}/VNINDEX.csv", parse_dates=["date"]).sort_values("date").drop_duplicates("date").set_index("date")["close"][:fl.END]
days = idx["2012-01-01":].index
wk_full = idx.resample("W-FRI").last().dropna()
weeks = wk_full["2012-01-01":].index
ok40_all = (wk_full >= wk_full.rolling(40).mean()).reindex(weeks).fillna(True)
ma40_all = wk_full.rolling(40).mean().reindex(weeks)
C, HI, LIQ, TL, O, CL, unit = {}, {}, {}, {}, {}, {}, {}
for f in sorted(os.listdir(f"{a.data}/stocks_long")):
    if not f.endswith(".csv"): continue
    d = fl.load(f"{a.data}/stocks_long/{f}")
    if len(d) < 60: continue
    s = f[:-4]
    w = d.resample("W-FRI").agg({"high": "max", "low": "min", "close": "last"}).dropna()
    C[s], HI[s] = w["close"], w["high"]
    LIQ[s] = d["value"].rolling(20).mean().resample("W-FRI").last()
    TL[s] = swing_gate(w, k=2)
    O[s], CL[s] = d["open"], d["close"]
    unit[s] = 1000 if d["close"].max() < 1000 else 1
R = lambda D: pd.DataFrame(D).reindex(weeks)
C, HI, LIQ, TL = R(C), R(HI), R(LIQ), R(TL)
O = pd.DataFrame(O).reindex(days); CL = pd.DataFrame(CL).reindex(days); CF = CL.ffill()
last_day = CL.apply(lambda s: s.last_valid_index())
sc = C / HI.rolling(52, min_periods=52).max()
elig = (LIQ >= MIN_VALUE) & C.notna()
rank_all = sc.where(elig).rank(axis=1, ascending=False)
uni = pd.read_csv(f"{a.data}/universe_history.csv")
sanof = {r.symbol: str(r.exchange).strip().upper() for r in uni.itertuples()}
lim = lambda s: LIMIT.get(sanof.get(s, "HOSE"), 0.07)
san = lambda s: sanof.get(s, "?")
pos = {d: i for i, d in enumerate(days)}
hol_file = f"{a.out}/holidays.txt"
holidays = set(pd.to_datetime([l.strip() for l in open(hol_file) if l.strip()])) if os.path.exists(hol_file) else set()
wk_label = lambda d: d + pd.Timedelta(days=4 - d.weekday())

def is_week_end(D):
    i = pos[D]
    if i + 1 < len(days):
        return wk_label(days[i + 1]) != wk_label(D)
    if D.weekday() == 4: return True
    rest = [D + pd.Timedelta(days=k) for k in range(1, 5 - D.weekday())]
    return all(x in holidays for x in rest)          # cac ngay con lai trong tuan deu nghi le

# ---------------- trang thai ----------------
SP = f"{a.out}/state.json"
if os.path.exists(SP):
    st = json.load(open(SP))
else:
    st = dict(start=a.start, capital=a.capital, last_day=None, cash=a.capital, equity_last=a.capital, hold={}, cur=[], prev_target=[],
              pend_sell=[], pend_buy=[], stopped=[], plan=None, vni0=None)
start = pd.Timestamp(st["start"])
cur, prev_t = set(st["cur"]), set(st["prev_target"])
pend_sell, pend_buy, stopped = set(st["pend_sell"]), set(st["pend_buy"]), set(st["stopped"])
hold = st["hold"]          # sym -> dict(shares, d_in, px_in)
cash, eq_last = st["cash"], st["equity_last"]
plan = st["plan"]

def csv_append(path, rows, cols):
    if not rows: return
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(path, mode="a", header=not os.path.exists(path), index=False)

ORD, TRD, EQ = [], [], []
pct = lambda x: f"{x*100:+.1f}%"
vnd = lambda x: f"{x/1e6:,.0f} triệu"
todo = [d for d in days if d >= start and (st["last_day"] is None or d > pd.Timestamp(st["last_day"]))]
if a.asof: todo = [d for d in todo if d <= pd.Timestamp(a.asof)]

for D in todo:
    i = pos[D]; prev = days[i - 1]; msgs = []
    px_vnd = lambda s, p: p * unit.get(s, 1)
    # ---- 1. ap dung ke hoach tuan truoc (dau phien thuc hien) ----
    if plan:
        stopped = set(); tg = set(plan["target"])
        pend_sell = set(hold) - tg; pend_buy = tg - set(hold); plan = None
    # ---- 2. ma ngung giao dich / het du lieu ----
    for s in list(hold):
        ld = last_day.get(s)
        if ld is not None and D > ld + pd.Timedelta(days=7):
            p = CF.at[ld, s]; h = hold.pop(s)
            cash += h["shares"] * px_vnd(s, p) * (1 - FEE); pend_sell.discard(s)
            TRD.append([s, h["d_in"], h["px_in"], str(ld.date()), p, h["shares"], p / h["px_in"] - 1 - 2 * FEE, "ngung giao dich/het du lieu"])
            msgs.append(f"⚠️ {s}: không còn dữ liệu giá sau {ld:%d/%m/%Y} → coi như bán ở giá đóng cửa cuối ({p}).")
    # ---- 3. khop lenh ATO (gia mo cua) ----
    fills = []
    for s in sorted(pend_sell):
        if s not in hold: pend_sell.discard(s); continue
        px, ref = O.at[D, s], CF.at[prev, s]
        if pd.isna(px) or px <= ref * (1 - lim(s)) * 1.003:
            ORD.append([str(D.date()), "CHUA_KHOP_BAN", s, px, 0, "mo cua o gia san/khong co gia - thu lai phien sau"]); fills.append(f"⏳ BÁN {s}: chưa khớp (mở cửa ở giá sàn), thử lại phiên sau"); continue
        h = hold.pop(s); cash += h["shares"] * px_vnd(s, px) * (1 - FEE); pend_sell.discard(s)
        r = px / h["px_in"] - 1 - 2 * FEE
        TRD.append([s, h["d_in"], h["px_in"], str(D.date()), px, h["shares"], r, "ban theo ke hoach/giam san"])
        ORD.append([str(D.date()), "KHOP_BAN", s, px, h["shares"], ""])
        fills.append(f"✅ BÁN {s} ({san(s)}): {h['shares']:,} cp giá mở cửa {px} → lãi/lỗ cả lệnh {pct(r)}")
    slot = eq_last / N
    for s in sorted(pend_buy):
        if s in stopped: pend_buy.discard(s); continue
        px, ref = O.at[D, s], CF.at[prev, s]
        if pd.isna(px) or pd.isna(ref) or px >= ref * (1 + lim(s)) * 0.997:
            ORD.append([str(D.date()), "CHUA_KHOP_MUA", s, px, 0, "mo cua o gia tran/khong co gia - thu lai phien sau"]); fills.append(f"⏳ MUA {s}: chưa khớp (mở cửa ở giá trần), thử lại phiên sau"); continue
        per = px_vnd(s, px) * (1 + FEE)
        sh = int(min(slot, cash) // per // LOT * LOT)
        if sh <= 0:
            ORD.append([str(D.date()), "KHONG_DU_VON", s, px, 0, "khong du von de mua 1 lo"]); pend_buy.discard(s); continue
        cash -= sh * per; hold[s] = dict(shares=sh, d_in=str(D.date()), px_in=float(px)); pend_buy.discard(s)
        ORD.append([str(D.date()), "KHOP_MUA", s, px, sh, ""])
        fills.append(f"✅ MUA {s} ({san(s)}): {sh:,} cp giá mở cửa {px} (~{vnd(sh*px_vnd(s,px))})")
    if fills: msgs.append(f"KẾT QUẢ KHỚP LỆNH (paper) phiên {D:%d/%m/%Y}:\n" + "\n".join(fills))
    # ---- 4. dinh gia cuoi phien ----
    eq = cash + sum(h["shares"] * px_vnd(s, CF.at[D, s]) for s, h in hold.items())
    if st["vni0"] is None: st["vni0"] = float(idx[D])
    EQ.append([str(D.date()), round(eq), round(cash), len(hold), float(idx[D]), eq / st["capital"] - 1, idx[D] / st["vni0"] - 1])
    eq_last = eq
    # ---- 5. quy tac giam san (ban phien sau) ----
    fl_sell = []
    for s in list(hold):
        c, cp = CL.at[D, s], CF.at[prev, s]
        if pd.notna(c) and pd.notna(cp) and c <= cp * (1 - lim(s)) * 1.003:
            pend_sell.add(s); stopped.add(s); pend_buy.discard(s)
            fl_sell.append(f"• {s} ({san(s)}) đóng cửa ở giá sàn {c} (giá vốn {hold[s]['px_in']}, {pct(c/hold[s]['px_in']-1)}) → BÁN ở giá mở cửa phiên sau, không mua lại cho đến kỳ xét tuần sau")
            ORD.append([str(D.date()), "TIN_HIEU_BAN_GIAM_SAN", s, c, hold[s]["shares"], ""])
    if fl_sell: msgs.append(f"⚠️ BÁN DO GIẢM SÀN – tín hiệu phiên {D:%d/%m/%Y}:\n" + "\n".join(fl_sell))
    # ---- 6. review cuoi tuan ----
    if is_week_end(D):
        t = wk_label(D)
        if t not in sc.index: t = sc.index[-1]
        s_ = sc.loc[t][elig.loc[t]].dropna()
        ok40 = bool(ok40_all.loc[t]); removed, reason = set(), {}
        if len(s_) < 2 * N:
            cur = set()
        else:
            cur = {x for x in cur if x in s_.index}
            if ok40:
                if not cur: cur = set(s_.nlargest(N).index)
                else:
                    removed = set(s_[list(cur)].nsmallest(K_REPL).index); cur -= removed
                    for x in s_.sort_values(ascending=False).index:
                        if len(cur) >= N: break
                        cur.add(x)
            elif cur:
                removed = set(s_[list(cur)].nsmallest(K_REPL).index); cur -= removed
        tl = TL.loc[t]; tgt = {x for x in cur if tl.get(x, 0) == 1}
        if not ok40: tgt &= prev_t
        sells, buys = sorted(set(hold) - tgt), sorted(tgt - set(hold), key=lambda x: rank_all.at[t, x] if x in rank_all.columns else 999)
        def why(x):
            if x in removed: return "rớt hạng: nằm trong 2 mã điểm thấp nhất danh mục"
            if x not in cur: return "không còn đủ điều kiện (thanh khoản dưới 1 tỷ/phiên hoặc thiếu dữ liệu)"
            if tl.get(x, 0) != 1: return "thủng trendline tuần (giá đóng cửa tuần dưới đường hỗ trợ)"
            return "VN-Index dưới MA40: không mua mới"
        regime = (f"VN-Index {idx[D]:,.2f} đang {'TRÊN' if ok40 else 'DƯỚI'} MA40 tuần ({ma40_all.loc[t]:,.2f}) → " +
                  ("chế độ bình thường: thay 2 mã yếu nhất, lấp đủ 20 mã" if ok40 else "chế độ THẬN TRỌNG: không mua mới, mỗi tuần bỏ dần 2 mã yếu nhất"))
        if sells or buys:
            L = [f"📊 PAPER TRADE – tín hiệu cuối tuần {D:%d/%m/%Y} (đặt mua/bán ở giá mở cửa phiên giao dịch kế tiếp)", regime, ""]
            if sells:
                L.append(f"BÁN ({len(sells)}):")
                for x in sells:
                    h = hold[x]; c = CF.at[D, x]
                    L.append(f"• {x} ({san(x)}) – {why(x)}. Đang giữ {h['shares']:,} cp, giá vốn {h['px_in']}, giá đóng cửa {c} ({pct(c/h['px_in']-1)})")
            if buys:
                L.append(f"MUA MỚI ({len(buys)}):")
                for x in buys:
                    c = CF.at[D, x]; sh = int((eq / N) // (px_vnd(x, c) * (1 + FEE)) // LOT * LOT)
                    L.append(f"• {x} ({san(x)}) – hạng #{int(rank_all.at[t, x])}, giá đóng cửa {c} = {sc.at[t, x]*100:.1f}% đỉnh 52 tuần; mua ~{sh:,} cp (~{vnd(sh*px_vnd(x,c))})")
            keep = sorted(set(hold) & tgt)
            L.append(f"GIỮ NGUYÊN ({len(keep)}): " + ", ".join(keep))
            L.append("Lưu ý: giá lấy từ dữ liệu đã điều chỉnh cổ tức/chia tách nên có thể lệch nhẹ so với bảng giá thật; đây chỉ là paper trade để theo dõi, chưa phải lệnh thật.")
            msgs.append("\n".join(L))
        for x in sells: ORD.append([str(D.date()), "TIN_HIEU_BAN_TUAN", x, CF.at[D, x], hold[x]["shares"], why(x)])
        for x in buys: ORD.append([str(D.date()), "TIN_HIEU_MUA_TUAN", x, CF.at[D, x], 0, f"hang {int(rank_all.at[t, x])}"])
        plan = dict(after=str(D.date()), target=sorted(tgt)); prev_t = set(tgt)
    # ---- 7. ghi tin nhan ----
    if msgs and not a.no_msg:
        open(f"{a.out}/messages/{D:%Y-%m-%d}_tin_nhan.txt", "w").write("\n\n".join(msgs) + "\n")
    if todo and D == todo[-1] and not a.no_msg:
        top = sorted(hold.items(), key=lambda kv: -kv[1]["shares"] * px_vnd(kv[0], CF.at[D, kv[0]]))
        rep = [f"Báo cáo paper trade {D:%d/%m/%Y}: giá trị {vnd(eq)} ({pct(eq/st['capital']-1)} từ {start:%d/%m/%Y}); VN-Index cùng kỳ {pct(idx[D]/st['vni0']-1)}; đang giữ {len(hold)} mã, tiền mặt {vnd(cash)}."]
        rep += [f"• {s}: {h['shares']:,} cp, vốn {h['px_in']}, giờ {CF.at[D,s]} ({pct(CF.at[D,s]/h['px_in']-1)})" for s, h in top]
        open(f"{a.out}/messages/bao_cao_ngay_{D:%Y-%m-%d}.txt", "w").write("\n".join(rep) + "\n")
    st["last_day"] = str(D.date())

# ---------------- luu ----------------
st.update(cash=cash, equity_last=eq_last, hold=hold, cur=sorted(cur), prev_target=sorted(prev_t), pend_sell=sorted(pend_sell),
          pend_buy=sorted(pend_buy), stopped=sorted(stopped), plan=plan)
json.dump(st, open(SP, "w"), ensure_ascii=False, indent=1)
csv_append(f"{a.out}/orders.csv", ORD, ["ngay", "loai", "ma", "gia", "so_cp", "ghi_chu"])
csv_append(f"{a.out}/trades.csv", TRD, ["ma", "ngay_vao", "gia_vao", "ngay_ra", "gia_ra", "so_cp", "lai_lo_rong", "ly_do"])
csv_append(f"{a.out}/equity.csv", EQ, ["ngay", "gia_tri", "tien_mat", "so_ma", "vnindex", "lai_luy_ke", "vnindex_luy_ke"])
pd.DataFrame([dict(ma=s, san=san(s), ngay_vao=h["d_in"], gia_vao=h["px_in"], so_cp=h["shares"], gia_dong_cua=CF.at[days[-1] if not a.asof else pd.Timestamp(st["last_day"]), s])
              for s, h in hold.items()]).to_csv(f"{a.out}/holdings.csv", index=False)
print("xong", st["last_day"], "| ngay xu ly:", len(todo), "| dang giu:", len(hold), "| gia tri:", round(eq_last))
