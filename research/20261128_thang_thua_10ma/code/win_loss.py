import numpy as np, pandas as pd
from scipy import stats
T = pd.read_pickle("trades.pkl"); T["ret"] = T["ret"] - 0.003          # tru phi 2 chieu
T = T[T.d_in >= "2013-03-01"].copy(); T["yr"] = T.d_in.dt.year; T["win"] = T.ret > 0
print(f"Tong {len(T)} lenh | thang {T.win.mean()*100:.1f}% | lai TB/lenh {T.ret.mean()*100:.2f}% | trung vi {T.ret.median()*100:.2f}%")
print(f"Lai TB lenh thang {T[T.win].ret.mean()*100:.1f}% | lenh thua {T[~T.win].ret.mean()*100:.1f}% | giu TB thang {T[T.win].hold.mean():.0f} phien, thua {T[~T.win].hold.mean():.0f} phien")
print("\nTheo ly do ban:"); print(T.groupby("why").agg(n=("ret","size"), win=("win","mean"), ret=("ret","mean"), hold=("hold","mean")).round(3).to_string())
print("\nTheo nam (so lenh, ty le thang, lai TB/lenh):")
print(T.groupby("yr").agg(n=("ret","size"), win=("win","mean"), ret=("ret","mean")).round(3).to_string())
feats = ["dist","rank","ret4","ret13","ret26","vol26","liq","gap","margin","vni_ma40","vni_ret4","san"]
print("\nDAC DIEM LUC MUA - TB lenh thang vs thua (trung vi) va Mann-Whitney p (trong mau, mo ta):")
for f in feats:
    a, b = T[T.win][f].dropna(), T[~T.win][f].dropna()
    p = stats.mannwhitneyu(a, b).pvalue
    print(f"{f:9s} thang {a.median():9.3f} | thua {b.median():9.3f} | p={p:.3f}")
print("\nSAU KHI MUA (mo ta):")
for f in ["ret5","dd10","after5","hold"]:
    a, b = T[T.win][f].dropna(), T[~T.win][f].dropna()
    print(f"{f:7s} thang {a.median():8.3f} | thua {b.median():8.3f}")
# walk-forward cap lenh
print("\n=== WALK-FORWARD CAP LENH (train 3 nam -> test 1 nam, 2016-2026) ===")
res = []
for f in feats:
    ys, bad_all, rest_all, ok = [], [], [], 0
    for y in range(2016, 2027):
        tr = T[(T.yr >= y-3) & (T.yr <= y-1)][[f, "ret"]].dropna(); te = T[T.yr == y][[f, "ret"]].dropna()
        if len(tr) < 100 or len(te) < 20: continue
        q1, q2 = tr[f].quantile([1/3, 2/3])
        g = lambda d: np.where(d[f] <= q1, 0, np.where(d[f] <= q2, 1, 2))
        m = tr.groupby(g(tr)).ret.mean(); badg = m.idxmin()
        isb = g(te) == badg
        if isb.sum() < 5 or (~isb).sum() < 5: continue
        d = te.ret[isb].mean() - te.ret[~isb].mean(); ok += d < 0
        bad_all += list(te.ret[isb]); rest_all += list(te.ret[~isb]); ys.append((y, d))
    t, p = stats.ttest_ind(bad_all, rest_all, equal_var=False)
    res.append({"dac diem": f, "nhom xau (OOS) lai TB": np.mean(bad_all), "phan con lai": np.mean(rest_all),
                "chenh": np.mean(bad_all) - np.mean(rest_all), "so lenh nhom xau": len(bad_all), "so nam dung dau": f"{ok}/{len(ys)}", "t": t})
R = pd.DataFrame(res); 
fm = {c: (lambda v: f"{v*100:.2f}%") for c in ["nhom xau (OOS) lai TB","phan con lai","chenh"]}
print(R.to_string(index=False, formatters=fm | {"t": lambda v: f"{v:.2f}"}))
R.to_csv("win_loss_wf.csv", index=False)
# sau khi mua: lai tu ngay 5 theo muc sut ngay 5
print("\nSAU MUA: lai TB tu ngay 5 den luc ban, theo lai ngay 5 (mo ta, khong dung de chon ma):")
S = T.dropna(subset=["ret5","after5"]).copy()
S["b5"] = pd.cut(S.ret5, [-1, -0.08, -0.04, 0, 0.04, 0.08, 10], labels=["<-8%","-8..-4","-4..0","0..4","4..8",">8%"])
print(S.groupby("b5", observed=True).agg(n=("after5","size"), after5=("after5","mean"), win=("win","mean")).round(3).to_string())
print("\nTheo tercile dist/rank/vni_ma40 (toan ky, trong mau): lai TB/lenh va ty le thang")
for f in ["dist","vol26","gap","ret26","vni_ma40","margin"]:
    q = pd.qcut(T[f], 3, labels=["thap","giua","cao"], duplicates="drop")
    print(f, T.groupby(q, observed=True).agg(n=("ret","size"), win=("win","mean"), ret=("ret","mean")).round(3).to_dict("index"))
