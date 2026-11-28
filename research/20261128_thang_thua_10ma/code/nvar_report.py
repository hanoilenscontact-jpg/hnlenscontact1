import numpy as np, pandas as pd
R = pd.read_csv("nvar_returns.csv", parse_dates=[0], index_col=0)["2013-03-01":]
E = pd.read_csv("nvar_expo.csv", parse_dates=[0], index_col=0).reindex(R.index); E = np.maximum(E, E.shift(1).fillna(0))
D = pd.read_csv("nvar_distinct.csv", index_col=0).iloc[:, 0]
gap = R.index.to_series().diff().dt.days.fillna(1); d = 1.05 ** (1 / 365.25) - 1
S = R + (1 - E).mul((1 + d) ** gap - 1, axis=0)
def m(r):
    eq = (1 + r).cumprod(); y = (r.index[-1] - r.index[0]).days / 365.25
    return eq.iloc[-1] ** (1 / y) - 1, r.mean() * 250 / (r.std() * np.sqrt(250)), (eq / eq.cummax() - 1).min()
for per in (("2016", "2026"), ("2013-03", "2026-11")):
    print(f"\n--- {per[0]}..{per[1]}: lai/nam / Sharpe / sut max | gui 5%: lai/nam / Sharpe / sut max | von dung | so ma khac nhau ---")
    for c in R:
        a, b, e = m(R.loc[per[0]:per[1], c]); a2, b2, e2 = m(S.loc[per[0]:per[1], c])
        print(f"{c:14s} {a*100:5.1f}% / {b:.2f} / {e*100:6.1f}% | {a2*100:5.1f}% / {b2:.2f} / {e2*100:6.1f}% | {E.loc[per[0]:per[1], c].mean()*100:3.0f}% | {D[c]}")
print("\nTung nam, tien mat lai 0 (%):")
print((((1 + R).groupby(R.index.year).prod() - 1) * 100).round(1).to_string())
