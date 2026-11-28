from ctx_funcs import *
tg = tgG_N(20, 2, True); er3.N = 20; out = {}
for c in (0.0015, 0.0030, 0.0050, 0.0080):
    er3.COST = c
    r, ex, tl = er3.simulate(days, O, Cl, tg, lim, SUP, rule_floor=True); out[f"{c*100:.2f}%"] = r; print("xong", c, len(tl), flush=True)
pd.DataFrame(out).to_csv("cost_returns.csv"); print("done")
