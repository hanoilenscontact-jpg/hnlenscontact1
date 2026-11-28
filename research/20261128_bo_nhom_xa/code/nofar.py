from ctx_funcs import *
M = pd.read_csv("margin_trades.csv", parse_dates=["d_in"])
thr = {y: M[(M.yr >= y-3) & (M.yr <= y-1)].margin.quantile(2/3) for y in range(2016, 2027)}
print({k: round(float(np.exp(v)-1), 3) for k, v in thr.items()}, flush=True)
SUPw = SUP.copy(); SUPw.index = weeks; SUPw = SUPw.shift(1)
MW = np.log(C) - SUPw
def tg(use):
    cur, out, prev = set(), {}, set()
    for t in C.index:
        s = sc.loc[t][elig.loc[t]].dropna()
        th = thr.get(t.year) if use else None
        okc = lambda x: th is None or not (MW.at[t, x] > th)
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
for nm, u in (("nen", False), ("bo nhom xa", True)):
    res[nm], ex[nm], _ = er3.simulate(days, O, Cl, tg(u), lim, SUP, rule_floor=True); print("xong", nm, flush=True)
res["VNI"] = idx.pct_change().reindex(days).fillna(0); ex["VNI"] = pd.Series(1.0, index=days)
pd.DataFrame(res).to_csv("nofar_returns.csv"); pd.DataFrame(ex).to_csv("nofar_expo.csv"); print("done")
