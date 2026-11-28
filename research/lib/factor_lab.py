"""
Phong thi nghiem chien luoc chon co phieu VN - danh sach khai bao truoc, bao cao het.

Moi cuoi thang: ro = ma co GTGD TB 20 phien >= 5 ty TAI THOI DIEM DO. Xep hang, mua N ma dau, chia deu von,
giu 1 thang. Phi 0.15% moi chieu tren phan doi ma.

Chien luoc (deu la hien tuong da duoc nghien cuu nhieu):
  MOM    momentum 12-1: lai 12 thang bo thang gan nhat (Jegadeesh-Titman 1993)
  HIGH52 gan dinh 52 tuan: gia / dinh cao nhat 52 tuan (George-Hwang 2004)
  REV    dao chieu ngan han: mua ma giam manh nhat 1 thang qua (Jegadeesh 1990, Lehmann 1990)
  LOWVOL bien dong thap: do lech chuan lai tuan 26 tuan thap nhat (Ang et al. 2006, Blitz-van Vliet 2007)
  HIGH52+TL / MOM+TL: nhu tren nhung chi cam ma con tren trendline tuan cua chinh no (k=2), con lai de tien mat
Doi chung: ro chia deu moi ma thanh khoan (EW), VN-Index.
"""
import glob, os, sys
import numpy as np
import pandas as pd
from vn_gate import swing_gate, stats, period_loss

COST = 0.0015
MIN_VALUE = float(os.environ.get("MIN_VALUE", "5e9"))
HELD = (2016, 2018, 2024)
END = "2026-11-26"
HAIRCUT = float(os.environ.get("HAIRCUT", "0"))   # mat them khi ma ngung giao dich (vd 0.5)
TOPN_LIQ = int(os.environ.get("TOPN_LIQ", "0"))   # >0: ro = N ma thanh khoan nhat thay vi nguong 5 ty


def load(path):
    d = pd.read_csv(path, parse_dates=["date"]).sort_values("date").drop_duplicates("date").set_index("date")
    d = d[:END]
    d = d[(d[["open", "high", "low", "close"]] > 0).all(axis=1)]          # bo phien khong giao dich (gia 0)
    r = d["close"].pct_change(); rn = r.shift(-1)
    spike = (r.abs() > 0.4) & (rn * r < 0) & (rn.abs() > 0.28)          # gai 1 ngay roi quay lai = loi du lieu
    d = d[~spike]
    unit = 1000 if d["close"].max() < 1000 else 1
    d["value"] = d["close"] * unit * d["volume"]
    return d


def panel(dirs, idx_weeks):
    C, HI, LIQ, TL = {}, {}, {}, {}
    for f in sum([glob.glob(os.path.join(x, "*.csv")) for x in dirs], []):
        d = load(f)
        if len(d) < 60:
            continue
        s = os.path.basename(f)[:-4]
        w = d.resample("W-FRI").agg({"high": "max", "low": "min", "close": "last"}).dropna()
        C[s], HI[s] = w["close"], w["high"]
        if HAIRCUT and d.index[-1] < pd.Timestamp(END) - pd.Timedelta(days=30) and len(w) > 1:
            C[s] = w["close"].copy(); C[s].iloc[-1] *= (1 - HAIRCUT)
        LIQ[s] = d["value"].rolling(20).mean().resample("W-FRI").last()
        TL[s] = swing_gate(w, k=2)
    f = lambda D: pd.DataFrame(D).reindex(idx_weeks)
    return f(C), f(HI), f(LIQ), f(TL)


def run(C, HI, LIQ, TL, idx, N=20):
    R = C.pct_change(fill_method=None)
    month_end = C.index.to_series().groupby(C.index.to_period("M")).max().values
    scores = {
        "MOM": C.shift(4) / C.shift(52) - 1,
        "HIGH52": C / HI.rolling(52, min_periods=52).max(),
        "REV": -(C / C.shift(4) - 1),
        "LOWVOL": -R.rolling(26, min_periods=26).std(),
    }
    if TOPN_LIQ:
        rk = LIQ.where(C.notna()).rank(axis=1, ascending=False)
        elig = rk <= TOPN_LIQ
    else:
        elig = (LIQ >= MIN_VALUE) & C.notna()
    out = {}
    def simulate(pick_fn, trend=False):
        wts = pd.DataFrame(0.0, index=C.index, columns=C.columns)
        cur = pd.Series(0.0, index=C.columns)
        for t in C.index:
            if t in month_end:
                sel = pick_fn(t)
                cur = pd.Series(0.0, index=C.columns)
                if len(sel):
                    cur[sel] = 1.0 / N if pick_fn is not ew_pick else 1.0 / len(sel)
            w = cur.copy()
            if trend:
                w = w * (TL.loc[t].fillna(0) == 1)
            wts.loc[t] = w
        held = wts.shift(1).fillna(0)
        r = (held * R.fillna(0)).sum(axis=1) - held.diff().abs().sum(axis=1).fillna(0) * COST
        return r
    def top(name):
        def f(t):
            s = scores[name].loc[t][elig.loc[t]].dropna()
            return list(s.nlargest(N).index) if len(s) >= N * 2 else []
        return f
    def ew_pick(t):
        return list(elig.loc[t][elig.loc[t]].index)
    out["EW (doi chung)"] = simulate(ew_pick)
    for nm in scores:
        out[nm] = simulate(top(nm))
    out["HIGH52+TL"] = simulate(top("HIGH52"), trend=True)
    out["MOM+TL"] = simulate(top("MOM"), trend=True)
    out["VN-Index"] = idx.reindex(C.index).pct_change().fillna(0)
    return out


def report(out, years):
    rows = {}
    vni = out["VN-Index"]
    first = out["MOM"].ne(0).idxmax()          # bat dau khi momentum co du 12 thang lich su
    for nm, r in out.items():
        r = r[first:]
        r = r[r.index.year.isin(years)]
        v = vni.reindex(r.index)
        st = stats(r)
        yr = (1 + r).groupby(r.index.year).prod() - 1
        yv = (1 + v).groupby(v.index.year).prod() - 1
        rows[nm] = {"Lai/nam": st["Lai/nam"], "Hon VNI/nam": st["Lai/nam"] - stats(v)["Lai/nam"],
                    "Sharpe": st["Sharpe"], "Sut max": st["Sut max"],
                    "So nam thang VNI": f"{int((yr > yv).sum())}/{len(yr)}"}
    return pd.DataFrame(rows).T, first


if __name__ == "__main__":
    dirs = sys.argv[1:-1]
    idx = pd.read_csv(sys.argv[-1], parse_dates=["date"]).set_index("date")["close"]
    weeks = idx.resample("W-FRI").last().dropna()[os.environ.get("START", "2012-01-01"):].index
    C, HI, LIQ, TL = panel(dirs, weeks)
    open_held = os.environ.get("OPEN_HELD") == "1"
    for N in (10, 20):
        out = run(C, HI, LIQ, TL, idx.resample("W-FRI").last(), N=N)
        dev_years = [y for y in range(2012, 2027) if y not in HELD]
        t, first = report(out, dev_years)
        print(f"\n=== N={N} ma | NAM PHAT TRIEN {dev_years} (bat dau tu {first.date()}) ===")
        print(t.to_string(formatters={c: (lambda x: f'{x*100:.1f}%') for c in ['Lai/nam', 'Hon VNI/nam', 'Sut max']} | {'Sharpe': lambda x: f'{x:.2f}'}))
        if open_held:
            t, _ = report(out, list(HELD))
            print(f"\n=== N={N} | NAM KHOA {HELD} ===")
            print(t.to_string(formatters={c: (lambda x: f'{x*100:.1f}%') for c in ['Lai/nam', 'Hon VNI/nam', 'Sut max']} | {'Sharpe': lambda x: f'{x:.2f}'}))
