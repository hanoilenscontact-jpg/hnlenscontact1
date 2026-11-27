"""Bo loc VNI duoi MA L tuan -> dung ngoai. L in {0,30,40,50}. Xem LUAT_CHOT_TRUOC_regime.md"""
import sys, os
import numpy as np, pandas as pd
import factor_lab as fl, daily_exec as de, exit_rules as er, er2
from vn_gate import swing_gate

N = 20
data = sys.argv[1]
rule = "W-FRI"
idx = pd.read_csv(f"{data}/VNINDEX.csv", parse_dates=["date"]).set_index("date")["close"][:fl.END]
days = idx["2012-01-01":].index
wk_full = idx.resample(rule).last().dropna()
weeks = wk_full["2012-01-01":].index
C, HI, LIQ, TL, sup = {}, {}, {}, {}, {}
for f in os.listdir(f"{data}/stocks_long"):
    d = fl.load(f"{data}/stocks_long/{f}")
    if len(d) < 60: continue
    s = f[:-4]
    w = d.resample(rule).agg({"high": "max", "low": "min", "close": "last"}).dropna()
    C[s], HI[s] = w["close"], w["high"]
    LIQ[s] = d["value"].rolling(20).mean().resample(rule).last()
    TL[s] = swing_gate(w, k=2)
    sup[s] = er.weekly_support(w)
R = lambda D: pd.DataFrame(D).reindex(weeks)
C, HI, LIQ, TL = R(C), R(HI), R(LIQ), R(TL)
SUP = R(sup); SUP.index = SUP.index + pd.Timedelta(days=1)
O, Cl = de.daily_panels([f"{data}/stocks_long"], days)
u = pd.read_csv(f"{data}/universe_history.csv")
lim = {r.symbol: de.LIMIT.get(str(r.exchange).strip(), 0.07) for r in u.itertuples()}
sc = C / HI.rolling(52, min_periods=52).max(); elig = (LIQ >= 1e9) & C.notna()
print("loaded", flush=True)

def tg4(off):
    cur, out = set(), {}
    for i, t in enumerate(C.index):
        if i % 4 == off:
            s = sc.loc[t][elig.loc[t]].dropna()
            cur = set(s.nlargest(N).index) if len(s) >= 2 * N else set()
        tl = TL.loc[t]; out[t] = {x for x in cur if tl.get(x, 0) == 1}
    return out

def tgG(k):
    cur, out = set(), {}
    for t in C.index:
        s = sc.loc[t][elig.loc[t]].dropna()
        if len(s) < 2 * N: cur = set()
        else:
            cur = {x for x in cur if x in s.index}
            if not cur: cur = set(s.nlargest(N).index)
            else:
                cur -= set(s[list(cur)].nsmallest(k).index)
                for x in s.sort_values(ascending=False).index:
                    if len(cur) >= N: break
                    cur.add(x)
        tl = TL.loc[t]; out[t] = {x for x in cur if tl.get(x, 0) == 1}
    return out

def gate(tg, L):
    if L == 0: return tg
    ok = (wk_full >= wk_full.rolling(L).mean()).reindex(weeks).fillna(True)
    return {t: (s if ok.loc[t] else set()) for t, s in tg.items()}


ok40 = (wk_full >= wk_full.rolling(40).mean()).reindex(weeks).fillna(True)

def tgG_shrink(k=2):
    """Duoi MA40: khong them ma moi, moi tuan bo k ma diem thap nhat; tren MA40: G binh thuong (lap day 20)."""
    cur, out, prev = set(), {}, set()
    for t in C.index:
        s = sc.loc[t][elig.loc[t]].dropna()
        if len(s) < 2 * N: cur = set()
        else:
            cur = {x for x in cur if x in s.index}
            if ok40.loc[t]:
                if not cur: cur = set(s.nlargest(N).index)
                else:
                    cur -= set(s[list(cur)].nsmallest(k).index)
                    for x in s.sort_values(ascending=False).index:
                        if len(cur) >= N: break
                        cur.add(x)
            else:
                if cur: cur -= set(s[list(cur)].nsmallest(k).index)
        tl = TL.loc[t]; o = {x for x in cur if tl.get(x, 0) == 1}
        if not ok40.loc[t]: o &= prev          # khong mua moi (ke ca ma quay lai tren trendline)
        out[t] = o; prev = o
    return out

G2 = tgG(2)
res, ex = {}, {}
for nm, tg in {"G2 khong loc": G2, "G2 MA40 ban het": gate(G2, 40), "G2 MA40 bo dan 2 ma": tgG_shrink(2)}.items():
    res[nm], ex[nm] = er2.simulate(days, O, Cl, tg, lim, SUP, rule_floor=True)
    print("xong", nm, flush=True)
pd.DataFrame(res).to_csv("shrink_returns.csv"); pd.DataFrame(ex).to_csv("shrink_expo.csv")
print("done")
