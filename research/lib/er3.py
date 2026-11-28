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
    expo = [0.0]
    trades_log, entry, reason = [], {}, {}
    lim_of = lambda s: limits.get(s, 0.07)
    for i in range(1, len(day_list)):
        d, prev = day_list[i], day_list[i - 1]
        if d in exec_plan:
            tg = exec_plan[d]
            stopped = set()
            pend_sell = held - tg
            for x in pend_sell: reason.setdefault(x, 'rot')
            pend_buy = tg - held
        for s in list(held):
            if last_day[s] is not None and d > last_day[s]:
                held.discard(s); pend_sell.discard(s)
                if s in entry:
                    e = entry.pop(s); ld = last_day[s]
                    trades_log.append((s, e[0], e[1], ld, Cf.at[ld, s], 'delist')); reason.pop(s, None)
        r, trades, sold, bought = 0.0, 0, {}, {}
        for s in list(pend_sell):
            if s not in held:
                pend_sell.discard(s); continue
            px, ref = O.at[d, s], Cf.at[prev, s]
            if pd.isna(px) or px <= ref * (1 - lim_of(s)) * 1.003:
                continue
            sold[s] = px; held.discard(s); pend_sell.discard(s); trades += 1
            if s in entry:
                e = entry.pop(s); trades_log.append((s, e[0], e[1], d, px, reason.pop(s, 'rot')))
        for s in list(pend_buy):
            if s in stopped:
                pend_buy.discard(s); continue
            px, ref = O.at[d, s], Cf.at[prev, s]
            if pd.isna(px) or pd.isna(ref) or px >= ref * (1 + lim_of(s)) * 0.997:
                continue
            bought[s] = px; pend_buy.discard(s); trades += 1; entry[s] = (d, px); reason.pop(s, None)
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
        expo.append(len(held) / N)
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
                pend_sell.add(s); stopped.add(s); pend_buy.discard(s); reason[s] = 'floor'
    for s_, e in entry.items():
        ld = Cf[s_].last_valid_index(); trades_log.append((s_, e[0], e[1], ld, Cf.at[ld, s_], 'open'))
    tl = pd.DataFrame(trades_log, columns=['sym','d_in','px_in','d_out','px_out','why'])
    return pd.Series(rets, index=days), pd.Series(expo, index=days), tl


