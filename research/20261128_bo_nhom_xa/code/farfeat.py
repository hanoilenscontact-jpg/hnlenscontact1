import numpy as np, pandas as pd, factor_lab as fl, daily_exec as de
from scipy import stats
M = pd.read_csv("margin_trades.csv", parse_dates=["d_in"])
u = pd.read_csv("/home/claude/repo/data/universe_history.csv")
lim = {r.symbol: de.LIMIT.get(str(r.exchange).strip(), 0.07) for r in u.itertuples()}
rows = []
for y in range(2013, 2027):
    tr = M[(M.yr >= y-3) & (M.yr <= y-1)]
    th = tr.margin.quantile(2/3) if y >= 2016 else M[M.yr <= 2015].margin.quantile(2/3)   # 2013-15 chi dung lam train
    rows.append(M[(M.yr == y) & (M.margin > th)])
F = pd.concat(rows).reset_index(drop=True)
cache = {}
out = []
for x in F.itertuples():
    if x.sym not in cache: cache[x.sym] = fl.load(f"/home/claude/repo/data/stocks_long/{x.sym}.csv")
    d = cache[x.sym]; h = d[d.index < x.d_in]
    if len(h) < 61: continue
    c, v = h.close, h.value; r = c.pct_change()
    L = lim.get(x.sym, 0.07)
    out.append(dict(sym=x.sym, d_in=x.d_in, yr=x.yr, ret=x.ret, win=x.win, why=x.why,
        r10=c.iloc[-1]/c.iloc[-11]-1, r20=c.iloc[-1]/c.iloc[-21]-1, vol20=r.iloc[-20:].std(),
        maxup20=r.iloc[-20:].max(), ntran20=int((r.iloc[-20:] >= 0.9*L).sum()),
        vratio=v.iloc[-10:].mean()/v.iloc[-60:].mean(), up20=(r.iloc[-20:] > 0).mean(), ext10=c.iloc[-1]/c.iloc[-10:].mean()))
D = pd.DataFrame(out); D.to_csv("far_trades_feat.csv", index=False)
feats = ["r10","r20","vol20","maxup20","ntran20","vratio","up20","ext10"]
T = D[D.yr >= 2016]
print(f"Lenh nhom xa 2016-2026: {len(T)} | thang {T.win.mean()*100:.1f}% | lai TB {T.ret.mean()*100:.2f}%")
print("\nMo ta 2016-2026 (trung vi thang | thua | Mann-Whitney p):")
for f in feats:
    a, b = T[T.win][f], T[~T.win][f]
    print(f"{f:8s} {a.median():8.3f} | {b.median():8.3f} | p={stats.mannwhitneyu(a,b).pvalue:.3f}")
print("\nWalk-forward (train 3 nam lenh nhom xa -> test 1 nam):")
R = []
for f in feats:
    ok, n, bad, rest = 0, 0, [], []
    for y in range(2016, 2027):
        tr = D[(D.yr >= y-3) & (D.yr <= y-1)]; te = D[D.yr == y]
        if len(tr) < 60 or len(te) < 10: continue
        q = tr[f].quantile([1/3, 2/3]).values
        if q[0] == q[1]: q = [q[0] - 1e-9, q[1]]
        g = lambda z: np.where(z[f] <= q[0], 0, np.where(z[f] <= q[1], 1, 2))
        bg = tr.groupby(g(tr)).ret.mean().idxmin(); ib = g(te) == bg
        if ib.sum() < 3 or (~ib).sum() < 3: continue
        n += 1; ok += te.ret[ib].mean() < te.ret[~ib].mean(); bad += list(te.ret[ib]); rest += list(te.ret[~ib])
    t = stats.ttest_ind(bad, rest, equal_var=False).statistic
    R.append(dict(dac_diem=f, nhom_xau=np.mean(bad)*100, con_lai=np.mean(rest)*100, n_xau=len(bad), dung_dau=f"{ok}/{n}", t=t))
print(pd.DataFrame(R).round(2).to_string(index=False))
