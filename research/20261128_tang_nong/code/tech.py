import numpy as np, pandas as pd, factor_lab as fl
from scipy import stats
D = pd.read_csv("far_trades_feat.csv", parse_dates=["d_in"])
cache, out = {}, []
for x in D.itertuples():
    if x.sym not in cache: cache[x.sym] = fl.load(f"/home/claude/repo/data/stocks_long/{x.sym}.csv")
    d = cache[x.sym]; h = d[d.index < x.d_in]
    if len(h) < 60: continue
    c, hi, lo, v = h.close, h.high, h.low, h.volume
    dlt = c.diff(); up = dlt.clip(lower=0).ewm(alpha=1/14, adjust=False).mean(); dn = (-dlt.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
    rsi = 100 - 100 / (1 + up.iloc[-1] / dn.iloc[-1]) if dn.iloc[-1] > 0 else 100
    macd = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean(); hist = macd - macd.ewm(span=9, adjust=False).mean()
    m20, s20 = c.iloc[-20:].mean(), c.iloc[-20:].std()
    tr = pd.concat([hi - lo, (hi - c.shift()).abs(), (lo - c.shift()).abs()], axis=1).max(axis=1)
    lo14, hi14 = lo.iloc[-14:].min(), hi.iloc[-14:].max()
    out.append(dict(yr=x.yr, ret=x.ret, win=x.win, rsi14=rsi, macdh=hist.iloc[-1] / c.iloc[-1],
        pctb=(c.iloc[-1] - (m20 - 2*s20)) / (4*s20) if s20 > 0 else np.nan, atr=tr.ewm(alpha=1/14, adjust=False).mean().iloc[-1] / c.iloc[-1],
        d_ma20=c.iloc[-1] / m20 - 1, d_ma50=c.iloc[-1] / c.iloc[-50:].mean() - 1,
        vr5=v.iloc[-5:].mean() / v.iloc[-20:].mean() if v.iloc[-20:].mean() > 0 else np.nan,
        stoch=(c.iloc[-1] - lo14) / (hi14 - lo14) * 100 if hi14 > lo14 else np.nan))
T = pd.DataFrame(out); T.to_csv("far_tech.csv", index=False)
feats = ["rsi14","macdh","pctb","atr","d_ma20","d_ma50","vr5","stoch"]
X = T[T.yr >= 2016]
print(f"Lenh nhom xa 2016-2026: {len(X)}, thang {X.win.mean()*100:.1f}%")
print("Mo ta (trung vi thang | thua | p):")
for f in feats:
    a, b = X[X.win][f].dropna(), X[~X.win][f].dropna()
    print(f"{f:7s} {a.median():8.3f} | {b.median():8.3f} | p={stats.mannwhitneyu(a,b).pvalue:.3f}")
print("Walk-forward:")
R = []
for f in feats:
    ok, n, bad, rest = 0, 0, [], []
    for y in range(2016, 2027):
        tr = T[(T.yr >= y-3) & (T.yr <= y-1)].dropna(subset=[f]); te = T[T.yr == y].dropna(subset=[f])
        if len(tr) < 60 or len(te) < 10: continue
        q = tr[f].quantile([1/3, 2/3]).values
        g = lambda z: np.where(z[f] <= q[0], 0, np.where(z[f] <= q[1], 1, 2))
        bg = tr.groupby(g(tr)).ret.mean().idxmin(); ib = g(te) == bg
        if ib.sum() < 3 or (~ib).sum() < 3: continue
        n += 1; ok += te.ret[ib].mean() < te.ret[~ib].mean(); bad += list(te.ret[ib]); rest += list(te.ret[~ib])
    R.append(dict(chi_bao=f, nhom_xau=np.mean(bad)*100, con_lai=np.mean(rest)*100, n_xau=len(bad), dung_dau=f"{ok}/{n}",
                  t=stats.ttest_ind(bad, rest, equal_var=False).statistic))
print(pd.DataFrame(R).round(2).to_string(index=False))
