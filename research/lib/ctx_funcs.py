from ctx import *
ok40 = (wk_full >= wk_full.rolling(40).mean()).reindex(weeks).fillna(True)

def tgG_N(N, k, shrink=False):
    cur, out, prev = set(), {}, set()
    for t in C.index:
        s = sc.loc[t][elig.loc[t]].dropna()
        if len(s) < 2 * N: cur = set()
        else:
            cur = {x for x in cur if x in s.index}
            if (not shrink) or ok40.loc[t]:
                if not cur: cur = set(s.nlargest(N).index)
                else:
                    cur -= set(s[list(cur)].nsmallest(k).index)
                    for x in s.sort_values(ascending=False).index:
                        if len(cur) >= N: break
                        cur.add(x)
            elif cur:
                cur -= set(s[list(cur)].nsmallest(k).index)
        tl = TL.loc[t]; o = {x for x in cur if tl.get(x, 0) == 1}
        if shrink and not ok40.loc[t]: o &= prev
        out[t] = o; prev = o
    return out
