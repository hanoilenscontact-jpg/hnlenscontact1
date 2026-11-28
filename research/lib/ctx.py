"""Bo loc VNI duoi MA L tuan -> dung ngoai. L in {0,30,40,50}. Xem LUAT_CHOT_TRUOC_regime.md"""
import sys, os
import numpy as np, pandas as pd
import factor_lab as fl, daily_exec as de, exit_rules as er, er3
from vn_gate import swing_gate

N = 20
data = '/home/claude/repo/data'
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

