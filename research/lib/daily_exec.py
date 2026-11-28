"""
Chay lai chien luoc "Gan dinh 52 tuan + trendline" bang GIA NGAY, khop lenh sat thuc te.

Tin hieu (khong doi): cuoi thang chon 20 ma gan dinh 52 tuan nhat (thanh khoan >= nguong),
cuoi tuan bo ma thung trendline tuan cua chinh no (k=2), quay lai tren trendline thi mua lai.
Phien chot tin hieu = phien giao dich cuoi cung cua tuan.

Cach khop lenh:
  V0  ATC chinh phien chot      (ly tuong - gia dinh cua backtest cu)
  V1  ATO phien hom sau         (gia mo cua)
  V2  ATC phien hom sau         (gia dong cua)
Rang buoc that:
  - Mua khong khop neu gia khop >= gia tran - 0.3%; ban khong khop neu <= gia san + 0.3%
    -> lenh treo, thu lai phien sau cung kieu khop.
  - Bien do theo san hien tai: HOSE 7%, HNX 10%, UPCoM 15% (khong ro -> 7%, chat hon).
  - Ma ngung giao dich khi dang cam: tinh ban o gia dong cua cuoi cung.
  - Phi 0.15% moi chieu. Moi vi the = 1/20 von, phan con lai la tien mat (lai 0).
"""
import os, sys
import numpy as np
import pandas as pd
import factor_lab as fl

N = 20
COST = 0.0015
LIMIT = {"HOSE": 0.07, "HNX": 0.10, "UPCOM": 0.15, "UPCoM": 0.15}


def daily_panels(dirs, days):
    O, Cl = {}, {}
    for d0 in dirs:
        for f in os.listdir(d0):
            d = fl.load(os.path.join(d0, f))
            if len(d) < 60:
                continue
            s = f[:-4]
            O[s], Cl[s] = d["open"], d["close"]
    O = pd.DataFrame(O).reindex(days)
    Cl = pd.DataFrame(Cl).reindex(days)
    return O, Cl


def targets(C, HI, LIQ, TL):
    """Tap ma muc tieu tai moi tuan (nhan W-FRI)."""
    sc = C / HI.rolling(52, min_periods=52).max()
    elig = (LIQ >= fl.MIN_VALUE) & C.notna()
    month_end = set(C.index.to_series().groupby(C.index.to_period("M")).max().values)
    cur, out = set(), {}
    for t in C.index:
        if t in month_end:
            s = sc.loc[t][elig.loc[t]].dropna()
            cur = set(s.nlargest(N).index) if len(s) >= 2 * N else set()
        tl = TL.loc[t]
        out[t] = {x for x in cur if tl.get(x, 0) == 1}
    return out


def simulate(days, O, Cl, tgt_by_week, mode, limits):
    Cf = Cl.ffill()
    last_day = Cl.apply(lambda s: s.last_valid_index())
    # phien chot = phien GD cuoi cung <= nhan thu 6 cua tuan
    dser = pd.Series(days, index=days)
    sig_day = {}
    for wk, tg in tgt_by_week.items():
        x = dser[(dser <= wk) & (dser > wk - pd.Timedelta(days=7))]
        if len(x):
            sig_day[x.iloc[-1]] = tg
    day_list = list(days)
    pos = {d: i for i, d in enumerate(day_list)}
    exec_plan = {}
    for sd, tg in sig_day.items():
        i = pos[sd] + (0 if mode == "V0" else 1)
        if i < len(day_list):
            exec_plan[day_list[i]] = tg
    price_kind = "open" if mode == "V1" else "close"
    held, pend_buy, pend_sell = set(), set(), set()
    rets, unfilled = [], 0
    for i, d in enumerate(day_list):
        if i == 0:
            rets.append(0.0); continue
        prev = day_list[i - 1]
        if d in exec_plan:
            tg = exec_plan[d]
            pend_sell = (held - tg)
            pend_buy = (tg - held)
        # ma da ngung GD -> ban o gia cuoi
        for s in list(held):
            if last_day[s] is not None and d > last_day[s]:
                held.discard(s); pend_sell.discard(s)
        r = 0.0; trades = 0
        sold_today, bought_today = {}, {}
        lim_of = lambda s: limits.get(s, 0.07)
        for s in list(pend_sell):
            if s not in held:
                pend_sell.discard(s); continue
            px = O.at[d, s] if price_kind == "open" else Cl.at[d, s]
            ref = Cf.at[prev, s]
            if pd.isna(px) or px <= ref * (1 - lim_of(s)) * 1.003:
                unfilled += 1; continue
            sold_today[s] = px; held.discard(s); pend_sell.discard(s); trades += 1
        for s in list(pend_buy):
            px = O.at[d, s] if price_kind == "open" else Cl.at[d, s]
            ref = Cf.at[prev, s]
            if pd.isna(px) or pd.isna(ref) or px >= ref * (1 + lim_of(s)) * 0.997:
                unfilled += 1; continue
            bought_today[s] = px; pend_buy.discard(s); trades += 1
        for s in held:
            c, cp = Cl.at[d, s], Cf.at[prev, s]
            if not pd.isna(c) and not pd.isna(cp):
                r += (c / cp - 1) / N
        for s, px in sold_today.items():
            r += (px / Cf.at[prev, s] - 1) / N
        for s, px in bought_today.items():
            r += (Cl.at[d, s] / px - 1) / N
            held.add(s)
        r -= trades * COST / N
        rets.append(r)
    return pd.Series(rets, index=days), unfilled


def st(r):
    r = r.dropna()
    eq = (1 + r).cumprod(); yrs = len(r) / 250
    vol = r.std() * np.sqrt(250)
    return {"Lai/nam": eq.iloc[-1] ** (1 / yrs) - 1, "Sharpe": r.mean() * 250 / vol,
            "Sut max": (eq / eq.cummax() - 1).min()}


if __name__ == "__main__":
    data = sys.argv[1]
    fl.MIN_VALUE = float(os.environ.get("MIN_VALUE", "2e9"))
    idx = pd.read_csv(f"{data}/VNINDEX.csv", parse_dates=["date"]).set_index("date")["close"][:fl.END]
    days = idx["2012-01-01":].index
    weeks = idx.resample("W-FRI").last().dropna()["2012-01-01":].index
    C, HI, LIQ, TL = fl.panel([f"{data}/stocks_long"], weeks)
    tg = targets(C, HI, LIQ, TL)
    O, Cl = daily_panels([f"{data}/stocks_long"], days)
    u = pd.read_csv(f"{data}/universe_history.csv")
    limits = {r.symbol: LIMIT.get(str(r.exchange).strip(), 0.07) for r in u.itertuples()}
    vni = idx.pct_change().fillna(0)
    first = min(w for w, s in tg.items() if s)
    res, yearly = {}, {}
    for mode, lab in (("V0", "ATC phien chot (ly tuong)"), ("V1", "ATO phien hom sau"), ("V2", "ATC phien hom sau")):
        r, unf = simulate(days, O, Cl, tg, mode, limits)
        r = r[first:]
        dev = r[~r.index.year.isin(fl.HELD)]; hel = r[r.index.year.isin(fl.HELD)]
        a, b = st(dev), st(hel)
        res[lab] = {"Lai/nam PT": a["Lai/nam"], "Sharpe PT": a["Sharpe"], "Sut PT": a["Sut max"],
                    "Lai/nam khoa": b["Lai/nam"], "Sharpe khoa": b["Sharpe"], "Sut khoa": b["Sut max"],
                    "Lenh treo (luot)": unf}
        yearly[lab] = (1 + r).groupby(r.index.year).prod() - 1
    v = vni[first:]
    a, b = st(v[~v.index.year.isin(fl.HELD)]), st(v[v.index.year.isin(fl.HELD)])
    res["VN-Index"] = {"Lai/nam PT": a["Lai/nam"], "Sharpe PT": a["Sharpe"], "Sut PT": a["Sut max"],
                       "Lai/nam khoa": b["Lai/nam"], "Sharpe khoa": b["Sharpe"], "Sut khoa": b["Sut max"]}
    yearly["VN-Index"] = (1 + v).groupby(v.index.year).prod() - 1
    t = pd.DataFrame(res).T
    print(f"Nguong thanh khoan {fl.MIN_VALUE/1e9:.0f} ty | bat dau {first.date()} | PT = nam phat trien, khoa = {fl.HELD}")
    print(t.to_string(formatters={c: (lambda x: "" if pd.isna(x) else f"{x*100:.1f}%") for c in t.columns if "Lai" in c or "Sut" in c}
          | {c: (lambda x: "" if pd.isna(x) else f"{x:.2f}") for c in t.columns if "Sharpe" in c}
          | {"Lenh treo (luot)": lambda x: "" if pd.isna(x) else f"{int(x)}"}))
    print("\nLai/lo tung nam (%):")
    print((pd.DataFrame(yearly) * 100).round(1).to_string())
