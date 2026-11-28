from ctx_funcs import *
res, ex, nm_ = {}, {}, {}
for N, k in ((10, 1), (10, 2), (20, 2)):
    for sh in (False, True):
        nm = f"N{N}k{k}{'_MA40' if sh else ''}"
        er3.N = N
        tg = tgG_N(N, k, sh)
        res[nm], ex[nm], tl = er3.simulate(days, O, Cl, tg, lim, SUP, rule_floor=True)
        nm_[nm] = tl.sym.nunique()
        print("xong", nm, nm_[nm], flush=True)
pd.DataFrame(res).to_csv("nvar_returns.csv"); pd.DataFrame(ex).to_csv("nvar_expo.csv")
pd.Series(nm_).to_csv("nvar_distinct.csv"); print("done")
