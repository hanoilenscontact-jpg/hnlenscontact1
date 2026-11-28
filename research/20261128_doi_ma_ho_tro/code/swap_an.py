from ctx_funcs import *
import pickle
P = pickle.load(open("swaps.pkl","rb")); adds, rems, curl, T = P["adds"], P["rems"], P["cur"], P["trades"]
Cf = Cl.ffill(); dl = list(days); pos = {d:i for i,d in enumerate(dl)}
def nextday(t):
    i = days.searchsorted(t, side="right")
    return dl[i] if i < len(dl) else None
def fwd(sym, d0, h):
    i = pos[d0]; j = min(i + h, len(dl) - 1)
    if dl[j] > pd.Timestamp(fl.END) or i + h >= len(dl): return np.nan
    po = O.at[d0, sym] if pd.notna(O.at[d0, sym]) else Cf.at[d0, sym]
    pc = Cf.at[dl[j], sym]
    return pc / po - 1 if pd.notna(po) and pd.notna(pc) and po > 0 else np.nan
rows = []
for t in C.index:
    if t < pd.Timestamp("2013-03-01") or not ok40.loc[t]: continue
    a, rm = adds[t], rems[t]
    if not a or not rm: continue
    d0 = nextday(t)
    if d0 is None: continue
    el = list(elig.loc[t][elig.loc[t]].index)
    kept = curl[t] - a
    for h in (20, 60):
        fa = np.nanmean([fwd(x, d0, h) for x in a]); fr = np.nanmean([fwd(x, d0, h) for x in rm])
        fk = np.nanmean([fwd(x, d0, h) for x in kept]); fe = np.nanmean([fwd(x, d0, h) for x in el])
        rows.append(dict(t=t, h=h, add=fa, rem=fr, kept=fk, all=fe))
S = pd.DataFrame(rows).dropna(); S["yr"] = S.t.dt.year
for h in (20, 60):
    X = S[S.h == h]
    print(f"\n=== {h} phien sau (~{h//20} thang) ===")
    for lab, Y in (("3/2013-11/2026", X), ("2016-2026", X[X.yr >= 2016])):
        print(f"{lab}: {len(Y)} tuan doi ma | them {Y['add'].mean()*100:.2f}% | bo {Y.rem.mean()*100:.2f}% | giu lai {Y.kept.mean()*100:.2f}% | TB ca thi truong {Y['all'].mean()*100:.2f}% | tuan them>bo {(Y['add']>Y.rem).mean()*100:.0f}%")
    g = X.groupby("yr").agg(n=("add","size"), them=("add","mean"), bo=("rem","mean"), giu=("kept","mean"), tt=("all","mean"))
    g["them>bo %"] = X.groupby("yr").apply(lambda d: (d["add"] > d.rem).mean())
    print((g[["them","bo","giu","tt"]]*100).round(2).join(g[["n"]]).join((g[["them>bo %"]]*100).round(0)).to_string())
S.to_csv("swaps_fwd.csv", index=False)

# ---------- Phan 2: margin ----------
SUPd = SUP.reindex(days, method="ffill")
wk_of = lambda d: C.index[C.index.searchsorted(d, side="left") - 1]   # tuan tin hieu truoc ngay thuc hien
R2 = []
for x in T.itertuples():
    i = pos[x.d_in]
    if i == 0 or x.d_in < pd.Timestamp("2013-03-01"): continue
    prev = dl[i-1]; sp = SUPd.at[prev, x.sym]
    m = np.log(Cf.at[prev, x.sym]) - sp if pd.notna(sp) else np.nan
    why = x.why
    if why == "rot":
        w = wk_of(x.d_out)
        why = "trendline" if x.sym in curl.get(w, set()) else ("MA40 bo dan" if not ok40.get(w, True) else "rot hang")
    R2.append(dict(sym=x.sym, d_in=x.d_in, ret=x.px_out/x.px_in - 1 - 0.003, margin=m, why=why, hold=pos[x.d_out]-i))
M = pd.DataFrame(R2).dropna(subset=["margin"]); M["yr"] = M.d_in.dt.year; M["win"] = M.ret > 0
print(f"\n=== PHAN 2: {len(M)} lenh, ly do ban: {M.why.value_counts().to_dict()}")
def tab(D, q):
    D = D.assign(nhom=pd.cut(D.margin, [-np.inf, q[0], q[1], np.inf], labels=["gan","giua","xa"]))
    g = D.groupby("nhom", observed=True)
    out = g.agg(n=("ret","size"), thang=("win","mean"), lai=("ret","mean"), giu=("hold","mean"), margin_tv=("margin","median"))
    for w in ["trendline","floor","rot hang","MA40 bo dan"]:
        out[f"ban vi {w}"] = g.why.apply(lambda s: (s == w).mean())
    return out
qa = M.margin.quantile([1/3, 2/3]).values
print(f"\nToan ky 3/2013-11/2026 (trong mau, nguong {np.exp(qa[0])-1:.1%} / {np.exp(qa[1])-1:.1%} tren duong ho tro):")
print(tab(M, qa).round(3).to_string())
W = []
for y in range(2016, 2027):
    tr = M[(M.yr >= y-3) & (M.yr <= y-1)]; te = M[M.yr == y]
    if len(tr) < 100 or not len(te): continue
    W.append(tab(te, tr.margin.quantile([1/3, 2/3]).values).assign(yr=y))
W = pd.concat(W)
print("\nWalk-forward 2016-2026 (nguong tu 3 nam truoc) - gop:")
Wt = []
for y in range(2016, 2027):
    tr = M[(M.yr >= y-3) & (M.yr <= y-1)]; te = M[M.yr == y]
    q = tr.margin.quantile([1/3, 2/3]).values
    Wt.append(te.assign(nhom=pd.cut(te.margin, [-np.inf, q[0], q[1], np.inf], labels=["gan","giua","xa"])))
Wt = pd.concat(Wt)
g = Wt.groupby("nhom", observed=True)
o = g.agg(n=("ret","size"), thang=("win","mean"), lai=("ret","mean"), giu=("hold","mean"))
for w in ["trendline","floor","rot hang","MA40 bo dan"]: o[f"ban vi {w}"] = g.why.apply(lambda s: (s == w).mean())
print(o.round(3).to_string())
print("\nTung nam (walk-forward): lai TB/lenh xa - gan, va ty le thang xa vs gan")
yy = Wt.groupby(["yr","nhom"], observed=True).agg(lai=("ret","mean"), thang=("win","mean")).unstack()
d = pd.DataFrame({"lai gan": yy[("lai","gan")], "lai xa": yy[("lai","xa")], "xa-gan": yy[("lai","xa")]-yy[("lai","gan")],
                  "thang gan": yy[("thang","gan")], "thang xa": yy[("thang","xa")]})
print((d*100).round(1).to_string()); print("nam xa kem hon gan:", int((d["xa-gan"]<0).sum()), "/", len(d))
M.to_csv("margin_trades.csv", index=False)
