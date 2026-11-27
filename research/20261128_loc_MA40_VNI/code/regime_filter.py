"""Bo loc VNI duoi MA L tuan -> dung ngoai. L in {0,30,40,50}. Xem LUAT_CHOT_TRUOC_regime.md"""
import sys, os
import numpy as np, pandas as pd
import factor_lab as fl, daily_exec as de, exit_rules as er
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

res = {}
G2 = tgG(2); A4 = [tg4(o) for o in range(4)]
for L in (0, 30, 40, 50):
    res[f"G2_L{L}"] = er.simulate(days, O, Cl, gate(G2, L), lim, SUP, rule_floor=True)[0]
    A = [er.simulate(days, O, Cl, gate(A4[o], L), lim, SUP, rule_floor=True)[0] for o in range(4)]
    res[f"AD_L{L}"] = pd.concat(A, axis=1).mean(axis=1)
    # VNI co cung bo loc: tin hieu thu 6 -> ap tu phien sau (xap xi: lai ngay cua VNI x trang thai tuan truoc)
    vr = idx.pct_change().fillna(0).reindex(days)
    if L == 0:
        res["VNI_L0"] = vr
    else:
        ok = (wk_full >= wk_full.rolling(L).mean()).astype(float)
        okd = ok.reindex(days, method="ffill").shift(1).fillna(1)   # trang thai tu dong cua thu 6, ap tu phien ke
        sw = okd.diff().abs().fillna(0)
        res[f"VNI_L{L}"] = vr * okd - sw * 0.0015
    print("xong L", L, flush=True)
pd.DataFrame(res).to_csv("regime_returns.csv")
print("done")
