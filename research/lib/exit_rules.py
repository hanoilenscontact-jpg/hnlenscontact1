"""
So sanh tan suat review va cac quy tac ban ngay (muc thanh khoan 1 ty, khop ATO, co rang buoc tran/san).

A  Goc: chia 4 phan von, moi phan review 4 tuan/lan (so le), ban khi dong cua TUAN thung trendline
B  Review MOI TUAN ca danh muc (xep hang lai, ban ma roi top 20, mua ma moi vao)
C  A + ban khi gia dong cua NGAY thung trendline
D  A + ban khi giam san
E  A + ban khi giam >= 5% trong 1 phien
F  A + C + D + E
Quy tac ban ngay: tin hieu chot cuoi phien -> ban ATO phien hom sau (neu mo cua nam san thi treo, thu lai).
Ma da bi ban theo quy tac ngay: cho lan review ke tiep moi duoc mua lai (neu van dat dieu kien).
"""
import sys
import numpy as np
import pandas as pd
import factor_lab as fl
import daily_exec as de
from vn_gate import line

N, COST = 20, 0.0015


def weekly_support(w, k=2):
    """Gia tri duong ho tro (log) dung cho TUAN SAU, chi tu pivot da xac nhan."""
    H, L = np.log(w["high"].values), np.log(w["low"].values)
    lows, out = [], np.full(len(w), np.nan)
    for i in range(len(w)):
        t = i - k
        if t - k >= 0 and L[t] <= L[t - k:t + k + 1].min():
            lows.append((t, L[t]))
        if lows:
            out[i] = line(lows, i + 1, "up")
    return pd.Series(out, index=w.index)


def simulate(days, O, Cl, tgt_by_week, limits, SUP=None, rule_tl=False, rule_floor=False, rule_drop5=False):
    Cf = Cl.ffill()
    last_day = Cl.apply(lambda s: s.last_valid_index())
    dser = pd.Series(days, index=days)
    day_list = list(days); pos = {d: i for i, d in enumerate(day_list)}
    exec_plan = {}
    for wk, tg in tgt_by_week.items():
        x = dser[(dser <= wk) & (dser > wk - pd.Timedelta(days=7))]
        if len(x) and pos[x.iloc[-1]] + 1 < len(day_list):
            exec_plan[day_list[pos[x.iloc[-1]] + 1]] = tg
    sup_daily = SUP.reindex(days, method="ffill") if SUP is not None else None
    held, pend_buy, pend_sell, stopped = set(), set(), set(), set()
    rets, n_trades = [0.0], 0
    lim_of = lambda s: limits.get(s, 0.07)
    for i in range(1, len(day_list)):
        d, prev = day_list[i], day_list[i - 1]
        if d in exec_plan:
            tg = exec_plan[d]
            stopped = set()
            pend_sell = held - tg
            pend_buy = tg - held
        for s in list(held):
            if last_day[s] is not None and d > last_day[s]:
                held.discard(s); pend_sell.discard(s)
        r, trades, sold, bought = 0.0, 0, {}, {}
        for s in list(pend_sell):
            if s not in held:
                pend_sell.discard(s); continue
            px, ref = O.at[d, s], Cf.at[prev, s]
            if pd.isna(px) or px <= ref * (1 - lim_of(s)) * 1.003:
                continue
            sold[s] = px; held.discard(s); pend_sell.discard(s); trades += 1
        for s in list(pend_buy):
            if s in stopped:
                pend_buy.discard(s); continue
            px, ref = O.at[d, s], Cf.at[prev, s]
            if pd.isna(px) or pd.isna(ref) or px >= ref * (1 + lim_of(s)) * 0.997:
                continue
            bought[s] = px; pend_buy.discard(s); trades += 1
        for s in held:
            c, cp = Cl.at[d, s], Cf.at[prev, s]
            if not pd.isna(c) and not pd.isna(cp):
                r += (c / cp - 1) / N
        for s, px in sold.items():
            r += (px / Cf.at[prev, s] - 1) / N
        for s, px in bought.items():
            r += (Cl.at[d, s] / px - 1) / N; held.add(s)
        r -= trades * COST / N
        n_trades += trades
        rets.append(r)
        # quy tac ban ngay: xet gia dong cua hom nay -> ban ATO phien sau
        for s in list(held):
            c, cp = Cl.at[d, s], Cf.at[prev, s]
            if pd.isna(c) or pd.isna(cp):
                continue
            hit = False
            if rule_tl and sup_daily is not None and not pd.isna(sup_daily.at[d, s]) and np.log(c) < sup_daily.at[d, s]:
                hit = True
            if rule_floor and c <= cp * (1 - lim_of(s)) * 1.003:
                hit = True
            if rule_drop5 and c / cp - 1 <= -0.05:
                hit = True
            if hit:
                pend_sell.add(s); stopped.add(s); pend_buy.discard(s)
    return pd.Series(rets, index=days), n_trades


if __name__ == "__main__":
    data = sys.argv[1]
    idx = pd.read_csv(f"{data}/VNINDEX.csv", parse_dates=["date"]).set_index("date")["close"][:fl.END]
    days = idx["2012-01-01":].index
    weeks = idx.resample("W-FRI").last().dropna()["2012-01-01":].index
    C, HI, LIQ, TL = fl.panel([f"{data}/stocks_long"], weeks)
    O, Cl = de.daily_panels([f"{data}/stocks_long"], days)
    u = pd.read_csv(f"{data}/universe_history.csv")
    lim = {r.symbol: de.LIMIT.get(str(r.exchange).strip(), 0.07) for r in u.itertuples()}
    # duong ho tro tuan cho tung ma
    import os
    sup = {}
    for f in os.listdir(f"{data}/stocks_long"):
        d = fl.load(f"{data}/stocks_long/{f}")
        if len(d) < 60:
            continue
        w = d.resample("W-FRI").agg({"high": "max", "low": "min", "close": "last"}).dropna()
        sup[f[:-4]] = weekly_support(w)
    SUP = pd.DataFrame(sup).reindex(weeks)
    SUP.index = SUP.index + pd.Timedelta(days=1)   # dung tu thu 7 -> ap cho tuan sau
    sc = C / HI.rolling(52, min_periods=52).max(); elig = (LIQ >= 1e9) & C.notna()

    def tg(off, step):
        cur, out = set(), {}
        for i, t in enumerate(C.index):
            if i % step == off:
                s = sc.loc[t][elig.loc[t]].dropna()
                cur = set(s.nlargest(N).index) if len(s) >= 2 * N else set()
            tl = TL.loc[t]; out[t] = {x for x in cur if tl.get(x, 0) == 1}
        return out
    T4 = [tg(o, 4) for o in range(4)]
    T1 = tg(0, 1)
    variants = {
        "A Goc (4 phan, review 4 tuan)": dict(),
        "C A + vo trendline gia ngay": dict(rule_tl=True),
        "D A + giam san": dict(rule_floor=True),
        "E A + giam >=5%/phien": dict(rule_drop5=True),
        "F A + C + D + E": dict(rule_tl=True, rule_floor=True, rule_drop5=True),
    }
    res = {}
    for nm, kw in variants.items():
        out = [simulate(days, O, Cl, T4[o], lim, SUP, **kw) for o in range(4)]
        res[nm] = (pd.concat([x[0] for x in out], axis=1).mean(axis=1), np.sum([x[1] for x in out]))
        print("xong", nm, flush=True)
    rB, nB = simulate(days, O, Cl, T1, lim, SUP)
    res["B Review moi tuan (ca von)"] = (rB, nB)
    vni = idx.pct_change().fillna(0)
    S = pd.DataFrame({k: v[0] for k, v in res.items()} | {"VN-Index": vni})["2013-03-01":]
    S.to_csv("exit_rules_returns.csv")
    yrs = (S.index[-1] - S.index[0]).days / 365.25
    rows = {}
    for c in S:
        x = S[c]; eq = (1 + x).cumprod()
        y = (1 + x).groupby(x.index.year).prod() - 1
        rows[c] = {"Lai/nam": eq.iloc[-1] ** (1 / yrs) - 1, "Sharpe": x.mean() * 250 / (x.std() * np.sqrt(250)),
                   "Sut max": (eq / eq.cummax() - 1).min(), "Nam te nhat": y.min(),
                   "2022": y.get(2022), "2023": y.get(2023),
                   "Lenh/nam": (res[c][1] / yrs) if c in res else np.nan}
    t = pd.DataFrame(rows).T
    pct = ["Lai/nam", "Sut max", "Nam te nhat", "2022", "2023"]
    print(t.to_string(formatters={c: (lambda x: f"{x*100:.1f}%") for c in pct}
                      | {"Sharpe": lambda x: f"{x:.2f}", "Lenh/nam": lambda x: "" if pd.isna(x) else f"{x:.0f}"}))
