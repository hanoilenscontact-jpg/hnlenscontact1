from ctx_funcs import *
import pickle
er3.N = 20
r, ex, tl = er3.simulate(days, O, Cl, tgG_N(20, 2), lim, SUP, rule_floor=True)
print("trades", len(tl), flush=True)
Cf = Cl.ffill(); Of = O
dl = list(days); pos = {d: i for i, d in enumerate(dl)}
SUPd = SUP.reindex(days, method="ffill")
scr = sc.where(elig).rank(axis=1, ascending=False)
Rw = C.pct_change(fill_method=None)
F = {"dist": sc, "rank": scr, "ret4": C / C.shift(4) - 1, "ret13": C / C.shift(13) - 1, "ret26": C / C.shift(26) - 1,
     "vol26": Rw.rolling(26, min_periods=26).std(), "liq": np.log(LIQ.where(LIQ > 0))}
vni_dist = wk_full / wk_full.rolling(40).mean() - 1; vni_r4 = wk_full.pct_change(4)
rows = []
for x in tl.itertuples():
    i = pos[x.d_in]
    if i == 0: continue
    prev = dl[i - 1]
    k = C.index.searchsorted(prev, side="right") - 1
    if k < 0: continue
    t = C.index[k]
    row = {"sym": x.sym, "d_in": x.d_in, "d_out": x.d_out, "why": x.why, "ret": x.px_out / x.px_in - 1}
    for nm, D in F.items(): row[nm] = D.at[t, x.sym]
    row["gap"] = x.px_in / Cf.at[prev, x.sym] - 1
    sp = SUPd.at[prev, x.sym]; row["margin"] = np.log(Cf.at[prev, x.sym]) - sp if pd.notna(sp) else np.nan
    row["vni_ma40"] = vni_dist.get(t, np.nan); row["vni_ret4"] = vni_r4.get(t, np.nan)
    row["san"] = lim.get(x.sym, 0.07)
    c = Cl[x.sym].loc[x.d_in:x.d_out].dropna()
    row["hold"] = pos[x.d_out] - i
    if len(c) > 5:
        row["ret5"] = c.iloc[5] / x.px_in - 1; row["after5"] = x.px_out / c.iloc[5] - 1
    else: row["ret5"] = row["after5"] = np.nan
    row["dd10"] = c.iloc[:11].min() / x.px_in - 1 if len(c) else np.nan
    rows.append(row)
T = pd.DataFrame(rows); T.to_pickle("trades.pkl"); T.to_csv("trades.csv", index=False)
print(T.shape, T.ret.mean(), (T.ret > 0).mean(), flush=True)
