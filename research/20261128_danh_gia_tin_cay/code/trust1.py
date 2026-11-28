import numpy as np, pandas as pd, pickle, glob, os
from scipy import stats
S = pd.read_csv("shrink_returns.csv", parse_dates=[0], index_col=0)["G2 MA40 bo dan 2 ma"]
idx = pd.read_csv("/home/claude/repo/data/VNINDEX.csv", parse_dates=["date"]).set_index("date")["close"]
V = idx.pct_change().reindex(S.index).fillna(0)
x, v = S["2016":"2026"], V["2016":"2026"]
cagr = lambda r: (1 + r).prod() ** (365.25 / (r.index[-1] - r.index[0]).days) - 1
print(f"CHIEN LUOC 2016-2026: lai/nam {cagr(x)*100:.1f}% | VN-Index {cagr(v)*100:.1f}%")
# ---------- 1. Deflated Sharpe ----------
sr = {}
for f in ["regime_returns.csv","shrink_returns.csv","nvar_returns.csv","nofar_returns.csv","hot_returns.csv","smooth_returns.csv","exit_rules_returns.csv","g_test_returns.csv"]+glob.glob("g_days_W-*.csv"):
    if not os.path.exists(f): continue
    D = pd.read_csv(f, parse_dates=[0], index_col=0)
    for c in D.columns:
        if "VN" in c.upper() or "VNI" in c: continue
        r = D[c]["2016":"2026"].dropna()
        if len(r) > 1000 and r.std() > 0: sr[f"{f}:{c}"] = r.mean() / r.std()
sr = pd.Series(sr); print(f"\nSo chuoi bien the con luu: {len(sr)}; Sharpe nam hoa trung vi {sr.median()*np.sqrt(250):.2f}, cao nhat {sr.max()*np.sqrt(250):.2f}")
Nn = 49; g = 0.5772
sr0 = sr.std() * ((1 - g) * stats.norm.ppf(1 - 1/Nn) + g * stats.norm.ppf(1 - 1/(Nn*np.e)))
srh = x.mean() / x.std(); T = len(x)
dsr = stats.norm.cdf((srh - sr0) * np.sqrt(T - 1) / np.sqrt(1 - stats.skew(x) * srh + (stats.kurtosis(x, fisher=False) - 1) / 4 * srh**2))
print(f"Sharpe chien luoc {srh*np.sqrt(250):.2f}/nam; nguong 'may man' khi thu {Nn} bien the: {sr0*np.sqrt(250):.2f}; DSR = {dsr*100:.1f}%")
# ---------- 2. Bootstrap khoi ----------
rng = np.random.default_rng(1); B, L = 2000, 20
a, b = x.values, v.values; n = len(a); res = []
for _ in range(B):
    st = rng.integers(0, n, size=n // L + 1)
    ii = ((st[:, None] + np.arange(L)[None, :]) % n).ravel()[:n]
    ra, rb = a[ii], b[ii]; ea = np.cumprod(1 + ra); yrs = n / 250
    res.append((ea[-1] ** (1/yrs) - 1, ra.mean() / ra.std() * np.sqrt(250), (ea / np.maximum.accumulate(ea) - 1).min(), np.prod(1 + rb) ** (1/yrs) - 1))
R = pd.DataFrame(res, columns=["cagr","sharpe","mdd","vni"])
print("\nBootstrap khoi 20 phien, 2000 lan (khoang 90%):")
for c in ("cagr","sharpe","mdd"): print(f"  {c}: {R[c].quantile(.05):.3f} .. {R[c].median():.3f} .. {R[c].quantile(.95):.3f}")
print(f"  P(lai/nam > VN-Index cung mau) = {(R.cagr > R.vni).mean()*100:.1f}% ; P(sut max sau hon -40%) = {(R.mdd < -.4).mean()*100:.1f}%")
# ---------- 3. Du lieu: tap trung lai, huy niem yet ----------
P = pickle.load(open("swaps.pkl","rb")); T_ = P["trades"]; T_["ret"] = T_.px_out / T_.px_in - 1 - 0.003
T_ = T_[T_.d_in >= "2016-01-01"].sort_values("ret", ascending=False)
tot = T_.ret.sum(); k = len(T_)
print(f"\nLENH 2016-2026: {k} lenh, tong lai cong don (don vi % von vi the) {tot:.1f}; lai TB {T_.ret.mean()*100:.2f}%, trung vi {T_.ret.median()*100:.2f}%")
for q in (10, int(k*0.01), int(k*0.05)):
    print(f"  {q} lenh tot nhat = {T_.ret.head(q).sum()/tot*100:.0f}% tong lai; bo di thi lai TB/lenh con {T_.ret.iloc[q:].mean()*100:.2f}%")
print("10 lenh tot nhat:"); print(T_.head(10)[["sym","d_in","d_out","px_in","px_out","ret"]].assign(ret=lambda d: (d.ret*100).round(0)).to_string(index=False))
dl = T_[T_.why == "delist"]; print(f"\nLenh ket thuc do ngung giao dich/huy: {len(dl)} (lai TB {dl.ret.mean()*100:.1f}%). Phat them 50% von moi lenh nay ~ mat {len(dl)*0.5/20/12*100:.2f}%/nam von (uoc luong, ~12 nam)")
