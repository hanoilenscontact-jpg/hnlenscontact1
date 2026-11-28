from ctx_funcs import *
Cf = Cl.ffill()
dr = Cf.pct_change(fill_method=None).where(Cl.notna())
L = pd.Series({c: lim.get(c, 0.07) for c in Cl.columns})
ntr = (dr.ge(0.9 * L, axis=1)).astype(float).where(Cl.notna()).rolling(20, min_periods=10).sum()
r20 = Cf / Cf.shift(20) - 1
NTR = ntr.reindex(weeks, method="ffill"); R20 = r20.reindex(weeks, method="ffill")
M = pd.read_csv("margin_trades.csv", parse_dates=["d_in"])
dl = list(days); pos = {d: i for i, d in enumerate(dl)}
M["r20"] = [r20.at[dl[pos[d] - 1], s] for s, d in zip(M.sym, M.d_in)]
thr = {y: M[(M.yr >= y-3) & (M.yr <= y-1)].r20.quantile(2/3) for y in range(2016, 2027)}
print("nguong r20:", {k: round(v, 3) for k, v in thr.items()}, flush=True)
print("ty le lenh nen co >=2 phien tran:", round(float(np.mean([ntr.at[dl[pos[d]-1], s] >= 2 for s, d in zip(M.sym, M.d_in)])), 3), flush=True)
def tg(rule):
    cur, out, prev = set(), {}, set()
    for t in C.index:
        s = sc.loc[t][elig.loc[t]].dropna()
        def okc(x):
            if rule == "B1": return not (NTR.at[t, x] >= 2)
            if rule == "B2" and t.year in thr: return not (R20.at[t, x] > thr[t.year])
            return True
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
for nm in ("nen", "B1", "B2"):
    res[nm], ex[nm], _ = er3.simulate(days, O, Cl, tg(nm), lim, SUP, rule_floor=True); print("xong", nm, flush=True)
pd.DataFrame(res).to_csv("hot_returns.csv"); pd.DataFrame(ex).to_csv("hot_expo.csv"); print("done")
