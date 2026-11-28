import sys
from ctx_funcs import *
lo, hi = int(sys.argv[1]), int(sys.argv[2])
rows = []
yrs = lambda r: (1 + r).groupby(r.index.year).prod() - 1
for seed in range(lo, hi):
    rng = np.random.default_rng(seed)
    RS = pd.DataFrame(rng.random(C.shape), index=C.index, columns=C.columns)
    cur, out, prev = set(), {}, set()
    for t in C.index:
        m = elig.loc[t]; s = RS.loc[t][m]
        if len(s) < 40: cur = set()
        else:
            cur = {x for x in cur if x in s.index}
            if ok40.loc[t]:
                if cur: cur -= set(s[list(cur)].nsmallest(2).index)
                for x in s.sort_values(ascending=False).index:
                    if len(cur) >= 20: break
                    cur.add(x)
            elif cur: cur -= set(s[list(cur)].nsmallest(2).index)
        tl = TL.loc[t]; o = {x for x in cur if tl.get(x, 0) == 1}
        if not ok40.loc[t]: o &= prev
        out[t] = o; prev = o
    er3.N = 20
    r, ex, _ = er3.simulate(days, O, Cl, out, lim, SUP, rule_floor=True)
    x = r["2016":"2026"]; eq = (1 + x).cumprod(); y = (x.index[-1] - x.index[0]).days / 365.25
    y_ = yrs(r["2016":"2026"])
    rows.append(dict(seed=seed, cagr=eq.iloc[-1] ** (1 / y) - 1, sharpe=x.mean() * 250 / (x.std() * np.sqrt(250)), mdd=(eq / eq.cummax() - 1).min(),
                     expo=ex["2016":"2026"].mean(), **{f"y{k}": v for k, v in y_.items()}))
    pd.DataFrame(rows).to_csv(f"placebo_{lo}.csv", index=False); print(seed, round(rows[-1]["cagr"], 3), flush=True)
