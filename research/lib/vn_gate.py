"""
Cong thi truong (market gate) theo trendline dinh/day - kiem tra hieu qua tren VN-Index va co phieu.

Quy tac (theo bai Tori Trades, Dinh nghia 3.1-3.2, ban long/flat):
- Dinh/day (swing) bac k tren nen TUAN: tuan t la day neu Low_t <= Low cua k tuan truoc va k tuan sau.
  Chi duoc biet chac sau k tuan (xac nhan o t+k) -> khong dung thong tin tuong lai.
- Duong ho tro: noi 2 day da xac nhan gan nhat (thang log). Neu 2 day khong di len -> nam ngang o day cuoi.
- Duong khang cu: noi 2 dinh gan nhat. Neu 2 dinh khong di xuong -> nam ngang o dinh cuoi.
- Dang cam tien -> MO cong khi gia dong cua tuan vuot len tren duong khang cu (+delta).
- Dang mo cong -> DONG cong khi gia dong cua tuan thung duoi duong ho tro (-delta).
- Tin hieu chot cuoi tuan t, ap dung cho loi nhuan tuan t+1.

So sanh voi: nam giu, duong trung binh 40 tuan (~10 thang), momentum 52 tuan (long/flat).

Chay:
  python vn_gate.py --index data/VNINDEX.csv
  python vn_gate.py --index data/VNINDEX.csv --stocks-dir data/stocks
CSV can cot: date, high, low, close (ten cot khong phan biet hoa thuong).
"""
import argparse, glob, os
import numpy as np
import pandas as pd

COST_PER_SIDE = 0.0015   # 0.15% moi chieu = 0.3% khu hoi (muc anh dang dung cho Hermes)
WEEKS_PER_YEAR = 52


# ---------- du lieu ----------
def load_daily(path):
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    ren = {"time": "date", "tradingdate": "date", "price": "close"}
    df = df.rename(columns={k: v for k, v in ren.items() if k in df.columns})
    df["date"] = pd.to_datetime(df["date"])
    for c in ("high", "low", "close"):
        if c not in df.columns:
            df[c] = df["close"]
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", ""), errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("date").drop_duplicates("date")
    return df.set_index("date")[["high", "low", "close"]]


def to_weekly(d):
    w = d.resample("W-FRI").agg({"high": "max", "low": "min", "close": "last"}).dropna()
    return w


# ---------- quy tac trendline ----------
def swing_gate(w, k=3, delta=0.0):
    """Tra ve Series 0/1 (1 = cong mo, duoc cam co phieu) chot tai cuoi moi tuan."""
    H, L, C = np.log(w["high"].values), np.log(w["low"].values), np.log(w["close"].values)
    n = len(C)
    highs, lows = [], []          # pivot da xac nhan: (chi so, log gia)
    state = np.zeros(n)
    s = 0
    for i in range(n):
        t = i - k                  # tuan t chi duoc xac nhan tai tuan i = t + k
        if t - k >= 0:
            win_h = H[t - k:t + k + 1]
            win_l = L[t - k:t + k + 1]
            if H[t] >= win_h.max():
                highs.append((t, H[t]))
            if L[t] <= win_l.min():
                lows.append((t, L[t]))
        if s == 0 and len(highs) >= 1:
            res = line(highs, i, want="down")
            if C[i] > res + delta:
                s = 1
        elif s == 1 and len(lows) >= 1:
            sup = line(lows, i, want="up")
            if C[i] < sup - delta:
                s = 0
        state[i] = s
    return pd.Series(state, index=w.index)


def line(piv, i, want):
    """Gia tri duong noi 2 pivot gan nhat tai tuan i. Neu doc sai huong -> nam ngang o pivot cuoi."""
    if len(piv) == 1:
        return piv[-1][1]
    (t1, y1), (t2, y2) = piv[-2], piv[-1]
    m = (y2 - y1) / (t2 - t1)
    if (want == "up" and m <= 0) or (want == "down" and m >= 0):
        return y2
    return y2 + m * (i - t2)


def sma_gate(w, n=40):
    return (w["close"] > w["close"].rolling(n).mean()).astype(float)


def mom_gate(w, n=52):
    return (w["close"] > w["close"].shift(n)).astype(float)


# ---------- danh gia ----------
def run(ret, gate, cash_rate=0.0):
    """ret: loi nhuan tuan; gate: trang thai chot cuoi tuan -> ap dung tuan sau."""
    pos = gate.shift(1).fillna(0)
    switches = pos.diff().abs().fillna(pos.iloc[0])
    r = pos * ret + (1 - pos) * cash_rate / WEEKS_PER_YEAR - switches * COST_PER_SIDE
    return r, pos, switches


def stats(r, pos=None, switches=None):
    r = r.dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / WEEKS_PER_YEAR
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    vol = r.std() * np.sqrt(WEEKS_PER_YEAR)
    dd = (eq / eq.cummax() - 1).min()
    out = {"Lai/nam": cagr, "Dao dong/nam": vol,
           "Sharpe": (r.mean() * WEEKS_PER_YEAR) / vol if vol > 0 else np.nan,
           "Sut max": dd}
    if pos is not None:
        out["% thoi gian cam hang"] = pos.mean()
        out["So lan mua/ban"] = int(switches.sum())
    return out


def period_loss(r, start, end):
    x = r[start:end]
    if len(x) < 4:
        return np.nan
    eq = (1 + x).cumprod()
    return (eq / eq.cummax() - 1).min()


def trades(r_pos, pos):
    """Thong ke tung lenh: lai/lo moi lan cam hang."""
    res, cur = [], None
    for p, rr in zip(pos.values, r_pos.values):
        if p == 1:
            cur = (1 + rr) * (cur if cur is not None else 1)
        elif cur is not None:
            res.append(cur - 1); cur = None
    if cur is not None:
        res.append(cur - 1)
    res = np.array(res)
    if len(res) == 0:
        return {}
    win, loss = res[res > 0], res[res <= 0]
    return {"So lenh": len(res), "Ti le thang": len(win) / len(res),
            "Lai TB lenh thang": win.mean() if len(win) else np.nan,
            "Lo TB lenh thua": loss.mean() if len(loss) else np.nan}


# ---------- bao cao VN-Index ----------
CRISES = [("2007-03-01", "2009-03-31", "2007-09"),
          ("2018-04-01", "2018-12-31", "2018"),
          ("2022-01-01", "2022-12-31", "2022"),
          ("2025-03-01", "2025-05-31", "thue quan 2025")]
SUBPERIODS = [("2012-01-01", "2017-12-31"), ("2018-01-01", "2022-12-31"), ("2023-01-01", "2030-12-31")]


def index_report(w, cash_rate=0.0):
    ret = w["close"].pct_change().fillna(0)
    rules = {"Nam giu": pd.Series(1.0, index=w.index),
             "TB 40 tuan": sma_gate(w),
             "Momentum 52 tuan": mom_gate(w)}
    for k in (2, 3, 4):
        rules[f"Trendline k={k}"] = swing_gate(w, k=k)
    rows, crisis, sub, tr = {}, {}, {}, {}
    for name, g in rules.items():
        if name == "Nam giu":
            r, pos, sw = ret, pd.Series(1.0, index=w.index), pd.Series(0.0, index=w.index)
        else:
            r, pos, sw = run(ret, g, cash_rate)
        rows[name] = stats(r, pos, sw)
        crisis[name] = {lab: period_loss(r, a, b) for a, b, lab in CRISES}
        sub[name] = {f"{a[:4]}-{min(int(b[:4]), w.index[-1].year)}": stats(r[a:b])["Sharpe"] for a, b in SUBPERIODS}
        if name.startswith("Trendline"):
            tr[name] = trades(pos * ret, pos)
    return pd.DataFrame(rows).T, pd.DataFrame(crisis).T, pd.DataFrame(sub).T, pd.DataFrame(tr).T, rules


# ---------- bao cao co phieu ----------
def stock_report(w_index, stocks_dir, k=3, min_weeks=104, cash_rate=0.0):
    """Ro co phieu chia deu. So sanh: khong loc / loc bang cong VN-Index / loc bang trendline tung ma / ca hai."""
    mkt_gate = swing_gate(w_index, k=k).shift(1)
    rets, own = {}, {}
    for f in sorted(glob.glob(os.path.join(stocks_dir, "*.csv"))):
        w = to_weekly(load_daily(f))
        if len(w) < min_weeks:
            continue
        sym = os.path.basename(f)[:-4]
        rets[sym] = w["close"].pct_change()
        own[sym] = swing_gate(w, k=k).shift(1)
    R = pd.DataFrame(rets).reindex(w_index.index)
    G = pd.DataFrame(own).reindex(w_index.index)
    M = mkt_gate.reindex(w_index.index).fillna(0)
    avail = R.notna()
    variants = {
        "Ro chia deu, khong loc": avail.astype(float),
        "Chi cam khi cong VN-Index mo": avail.mul(M, axis=0),
        "Chi cam ma tren trendline cua chinh no": avail & (G == 1),
        "Ca hai cong": avail.mul(M, axis=0).astype(bool) & (G == 1),
    }
    out, crisis = {}, {}
    nstocks = avail.sum(axis=1).replace(0, np.nan)
    for name, held in variants.items():
        held = held.astype(float)
        wgt = held.div(nstocks, axis=0).fillna(0)          # moi ma chiem 1/N von, phan khong cam = tien mat
        r = (wgt * R.fillna(0)).sum(axis=1) + (1 - wgt.sum(axis=1)) * cash_rate / WEEKS_PER_YEAR
        turnover = wgt.diff().abs().sum(axis=1).fillna(0)
        r = r - turnover * COST_PER_SIDE
        r = r[nstocks.notna()]
        st = stats(r)
        st["% von dang cam hang"] = wgt.sum(axis=1)[nstocks.notna()].mean()
        out[name] = st
        crisis[name] = {lab: period_loss(r, a, b) for a, b, lab in CRISES}
    return pd.DataFrame(out).T, pd.DataFrame(crisis).T, len(rets)


def fmt(df):
    d = df.copy()
    for c in d.columns:
        if c in ("Sharpe", "So lan mua/ban", "So lenh"):
            d[c] = d[c].map(lambda x: "" if pd.isna(x) else (f"{x:.2f}" if isinstance(x, float) and not float(x).is_integer() else f"{int(x)}"))
        else:
            d[c] = d[c].map(lambda x: "" if pd.isna(x) else f"{x*100:.1f}%")
    return d.to_string()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", required=True)
    ap.add_argument("--stocks-dir")
    ap.add_argument("--heldout", default="2016,2018,2024")
    ap.add_argument("--cash-rate", type=float, default=0.0, help="lai tien mat/nam khi dung ngoai, vd 0.04")
    a = ap.parse_args()
    w = to_weekly(load_daily(a.index))
    print(f"VN-Index tuan: {w.index[0].date()} -> {w.index[-1].date()} ({len(w)} tuan)\n")
    main, cr, sub, tr, rules = index_report(w, a.cash_rate)
    print("== Toan giai doan ==\n" + fmt(main))
    print("\n== Muc sut lon nhat trong tung dot giam ==\n" + fmt(cr))
    print("\n== Sharpe theo tung giai doan (xem co on dinh khong) ==\n" + sub.round(2).to_string())
    print("\n== Thong ke lenh cua trendline ==\n" + fmt(tr))
    held = [int(x) for x in a.heldout.split(",")]
    ret = w["close"].pct_change().fillna(0)
    yearly, split = {}, {}
    for name, gg in rules.items():
        r = ret if name == "Nam giu" else run(ret, gg, a.cash_rate)[0]
        yearly[name] = (1 + r).groupby(r.index.year).prod() - 1
        isheld = r.index.year.isin(held)
        split[name] = {"Lai/nam - nam phat trien": stats(r[~isheld])["Lai/nam"],
                       "Sut max - nam phat trien": stats(r[~isheld])["Sut max"],
                       "Lai/nam - nam khoa": stats(r[isheld])["Lai/nam"],
                       "Sut max - nam khoa": stats(r[isheld])["Sut max"]}
    print("\n== Lai/lo tung nam ==\n" + (pd.DataFrame(yearly) * 100).round(1).to_string())
    print(f"\n== Tach nam phat trien / nam khoa {held} ==\n" + fmt(pd.DataFrame(split).T))
    g = rules["Trendline k=3"]
    print(f"\nTrang thai cong hien tai (k=3, chot {w.index[-1].date()}): {'MO' if g.iloc[-1] == 1 else 'DONG'}")
    if a.stocks_dir:
        s, sc, n = stock_report(w, a.stocks_dir, cash_rate=a.cash_rate)
        print(f"\n== Co phieu ({n} ma, chia deu, k=3) ==\n" + fmt(s))
        print("\n== Co phieu: muc sut trong tung dot giam ==\n" + fmt(sc))
