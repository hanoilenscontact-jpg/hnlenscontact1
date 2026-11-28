from ctx_funcs import *
er3.N = 20
cur_log, out, prev, cur, adds, rems = {}, {}, set(), set(), {}, {}
for t in C.index:
    s = sc.loc[t][elig.loc[t]].dropna(); before = set(cur)
    if len(s) < 40: cur = set()
    else:
        cur = {x for x in cur if x in s.index}
        if ok40.loc[t]:
            if not cur: cur = set(s.nlargest(20).index)
            else:
                cur -= set(s[list(cur)].nsmallest(2).index)
                for x in s.sort_values(ascending=False).index:
                    if len(cur) >= 20: break
                    cur.add(x)
        elif cur: cur -= set(s[list(cur)].nsmallest(2).index)
    adds[t], rems[t] = cur - before, before - cur
    tl = TL.loc[t]; o = {x for x in cur if tl.get(x, 0) == 1}
    if not ok40.loc[t]: o &= prev
    out[t] = o; prev = o; cur_log[t] = set(cur)
r, ex, trl = er3.simulate(days, O, Cl, out, lim, SUP, rule_floor=True)
import pickle; pickle.dump(dict(adds=adds, rems=rems, cur=cur_log, trades=trl, ok40=ok40), open("swaps.pkl","wb"))
print("done", len(trl))
