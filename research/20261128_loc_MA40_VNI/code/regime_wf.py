import numpy as np, pandas as pd
S = pd.read_csv("regime_returns.csv", parse_dates=[0], index_col=0)["2013-03-01":]
Ls = (0, 30, 40, 50)
sh = lambda x: x.mean() * 250 / (x.std() * np.sqrt(250)) if x.std() > 0 else np.nan
def st(x):
    eq = (1 + x).cumprod(); yrs = (x.index[-1] - x.index[0]).days / 365.25
    return eq.iloc[-1] ** (1 / yrs) - 1, sh(x), (eq / eq.cummax() - 1).min()
yr = lambda x: (1 + x).groupby(x.index.year).prod() - 1
for base in ("G2", "AD"):
    print(f"\n===== {base} =====")
    wf, pick = [], {}
    for y in range(2016, 2027):
        tr = S[str(y - 3):str(y - 1)]
        best = max(Ls, key=lambda L: sh(tr[f"{base}_L{L}"]))
        pick[y] = best; wf.append(S.loc[str(y)][f"{base}_L{best}"])
    wf = pd.concat(wf)
    T = pd.DataFrame({"khong loc": yr(S[f"{base}_L0"]), "MA30": yr(S[f"{base}_L30"]),
                      "MA40": yr(S[f"{base}_L40"]), "MA50": yr(S[f"{base}_L50"]),
                      "WF": yr(wf), "VNI": yr(S["VNI_L0"]), "VNI+MA40": yr(S["VNI_L40"])})
    T["WF chon"] = pd.Series(pick)
    print((T.drop(columns="WF chon") * 100).round(1).join(T["WF chon"]).to_string())
    print("Gop 2016-2026 (11 nam test):")
    for nm, x in {"khong loc": S[f"{base}_L0"], "MA30": S[f"{base}_L30"], "MA40": S[f"{base}_L40"],
                  "MA50": S[f"{base}_L50"], "WF": wf, "VNI": S["VNI_L0"], "VNI+MA40": S["VNI_L40"],
                  "VNI+MA50": S["VNI_L50"]}.items():
        a, b, c = st(x["2016":"2026"]); print(f"  {nm:10s} lai/nam {a*100:5.1f}%  Sharpe {b:.2f}  sut max {c*100:5.1f}%")
    print("Toan ky 2013-03..2026-11 (trong mau):")
    for L in Ls:
        a, b, c = st(S[f"{base}_L{L}"]); print(f"  L{L:2d} lai/nam {a*100:5.1f}%  Sharpe {b:.2f}  sut max {c*100:5.1f}%")
# ty le thoi gian dung ngoai va so lan chuyen
idx = pd.read_csv("/home/claude/repo/data/VNINDEX.csv", parse_dates=["date"]).set_index("date")["close"]
w = idx.resample("W-FRI").last().dropna()
for L in (30, 40, 50):
    ok = (w >= w.rolling(L).mean())["2013-03":"2026-11"]
    print(f"MA{L}: dung ngoai {(~ok).mean()*100:.0f}% so tuan, chuyen trang thai {int(ok.astype(int).diff().abs().sum())} lan")
