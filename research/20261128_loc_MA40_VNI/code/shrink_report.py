import numpy as np, pandas as pd
R = pd.read_csv("shrink_returns.csv", parse_dates=[0], index_col=0)["2013-03-01":]
E = pd.read_csv("shrink_expo.csv", parse_dates=[0], index_col=0).reindex(R.index)
E = np.maximum(E, E.shift(1).fillna(0))           # von dang dung trong phien
def m(r, e):
    eq = (1 + r).cumprod(); yrs = (r.index[-1] - r.index[0]).days / 365.25
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    sh = r.mean() * 250 / (r.std() * np.sqrt(250))
    mdd = (eq / eq.cummax() - 1).min()
    inm = e > 0
    ri = (r[inm] / e[inm])
    ann_inv = (1 + ri).prod() ** (250 / max(inm.sum(), 1)) - 1
    return cagr, sh, mdd, e.mean(), ann_inv
for per in [("2013-03", "2026-11"), ("2016", "2026")]:
    print(f"\n--- {per[0]} .. {per[1]} ---")
    print(f"{'':22s} lai/nam(tong von)  Sharpe  sut max  von dung TB  lai/nam tren von dung")
    for c in R:
        a, b, d, e, f = m(R.loc[per[0]:per[1], c], E.loc[per[0]:per[1], c])
        print(f"{c:22s} {a*100:8.1f}%        {b:5.2f}  {d*100:6.1f}%   {e*100:5.0f}%      {f*100:6.1f}%")
print("\nTung nam: lai tren tong von % | von dung TB %")
yr = (1 + R).groupby(R.index.year).prod() - 1
ye = E.groupby(E.index.year).mean()
T = (yr * 100).round(1).astype(str) + " | " + (ye * 100).round(0).astype(int).astype(str)
print(T.to_string())
