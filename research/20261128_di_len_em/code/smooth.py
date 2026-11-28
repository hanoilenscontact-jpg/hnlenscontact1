from ctx_funcs import *
Cf = Cl.ffill(); lp = np.log(Cf)
ER = (Cf - Cf.shift(60)).abs() / Cf.diff().abs().rolling(60).sum()
tt = pd.Series(np.arange(len(days)), index=days, dtype=float)
R2 = lp.rolling(60).corr(tt) ** 2
VOL = Cf.pct_change(fill_method=None).rolling(60).std()
for D in (ER, R2, VOL): D[Cl.isna()] = np.nan
dl = list(days); pos = {d: i for i, d in enumerate(dl)}
M = pd.read_csv("margin_trades.csv", parse_dates=["d_in"])
for nm, D in (("er60", ER), ("r2_60", R2), ("vol60", VOL)):
    M[nm] = [D.at[dl[pos[d]-1], s] for s, d in zip(M.sym, M.d_in)]
M.to_csv("smooth_trades.csv", index=False)
# Phan B
ERw = ER.reindex(weeks, method="ffill")
nd = {t: dl[days.searchsorted(t, side="right")] for t in weeks if days.searchsorted(t, side="right") < len(dl) - 20}
fw = {}
rows = []
for t in weeks:
    if t < pd.Timestamp("2013-03-01") or t not in nd: continue
    d0 = nd[t]; d1 = dl[pos[d0] + 20]
    m = elig.loc[t] & (sc.loc[t] >= 0.9)
    syms = m[m].index
    if len(syms) < 15: continue
    e = ERw.loc[t, syms].dropna()
    if len(e) < 15: continue
    po = O.loc[d0, e.index].fillna(Cf.loc[d0, e.index]); f = Cf.loc[d1, e.index] / po - 1
    q = e.rank(pct=True)
    for lab, mk in (("lac", q <= 1/3), ("giua", (q > 1/3) & (q <= 2/3)), ("em", q > 2/3)):
        rows.append(dict(t=t, nhom=lab, f=f[mk].mean(), n=mk.sum()))
B = pd.DataFrame(rows); B["yr"] = B.t.dt.year; B.to_csv("smooth_market.csv", index=False)
thr = {y: M[(M.yr >= y-3) & (M.yr <= y-1)].er60.quantile(1/3) for y in range(2016, 2027)}
print("nguong ER60:", {k: round(v, 3) for k, v in thr.items()}, flush=True)
def tg(use):
    cur, out, prev = set(), {}, set()
    for t in C.index:
        s = sc.loc[t][elig.loc[t]].dropna()
        okc = lambda x: (not use) or (t.year not in thr) or not (ERw.at[t, x] < thr[t.year])
        if len(s) < 40: cur = set()
        else:
            cur = {x for x in cur if x in s.index}
            if ok40.loc[t]:
                if cur: cur -= set(s[list(cur)].nsmallest(2).index)
                for x in s.sort_values(ascending=False).index:
                    if len(cur) >= 20: break
                    if x not in cur and okc(x): cur.add(x)
            elif cur: cur -= set(s[list(cur)].nsmallest(2).index)
        tl = TL.loc[t]; o = {x for x in cur if tl.get(x, 0) == 1}
        if not ok40.loc[t]: o &= prev
        out[t] = o; prev = o
    return out
er3.N = 20; res, ex = {}, {}
for nm, u in (("nen", False), ("bo ma lac", True)):
    res[nm], ex[nm], _ = er3.simulate(days, O, Cl, tg(u), lim, SUP, rule_floor=True); print("xong", nm, flush=True)
pd.DataFrame(res).to_csv("smooth_returns.csv"); pd.DataFrame(ex).to_csv("smooth_expo.csv"); print("done")
