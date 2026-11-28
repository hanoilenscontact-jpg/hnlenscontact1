import numpy as np, pandas as pd, os, factor_lab as fl
fl.END = "2100-01-01"
D = "/home/claude/repo/data"
u = pd.read_csv(f"{D}/universe_history.csv"); sanof = {r.symbol: str(r.exchange).strip().upper() for r in u.itertuples()}
lim = lambda s: {"HOSE": .07, "HNX": .10, "UPCOM": .15}.get(sanof.get(s, "HOSE"), .07)
# ---- A. thien lech song sot: so ma co du lieu cuoi cung theo nam ----
last, first, nrow = {}, {}, {}
for f in os.listdir(f"{D}/stocks_long"):
    d = pd.read_csv(f"{D}/stocks_long/{f}", parse_dates=["date"], usecols=["date","close"]); s = f[:-4]
    if len(d): last[s], first[s] = d.date.max(), d.date.min()
L = pd.Series(last); F = pd.Series(first)
print("A. Ma trong stocks_long theo nam ket thuc du lieu (chi tinh ma ket thuc truoc 11/2026):")
e = L[L < "2026-10-01"]; print(e.dt.year.value_counts().sort_index().to_string())
print("So ma co du lieu dang giao dich moi nam (co gia trong nam):", {y: int(((F <= f"{y}-12-31") & (L >= f"{y}-01-01")).sum()) for y in (2013, 2016, 2019, 2022, 2025)})
st = u.set_index("symbol").status.value_counts().to_dict(); print("universe_history:", st)
# ---- B. Top lenh: co vuot bien do gia/ngay khong ----
print("\nB. Kiem tra bien do gia ngay cua cac ma trong 10 lenh tot nhat:")
for s, a, b in [("TCM","2020-11-09","2021-02-03"),("CTP","2024-07-15","2024-08-30"),("TGG","2021-08-16","2021-10-04"),("SBS","2020-12-14","2020-12-28"),
                ("ANV","2018-01-15","2018-05-21"),("THD","2026-05-25","2026-06-09"),("AAA","2016-04-19","2016-08-22"),("BII","2021-08-30","2021-09-17"),
                ("TDC","2020-11-02","2021-01-20"),("QCG","2017-05-05","2017-05-30")]:
    d = fl.load(f"{D}/stocks_long/{s}.csv"); r = d.close.pct_change(); w = r[a:b]
    print(f"{s} ({sanof.get(s,'?')}, bien {lim(s)*100:.0f}%): {len(w)} phien, tang max 1 phien {w.max()*100:.1f}%, so phien > bien do+0,5%: {(w.abs() > lim(s)+0.005).sum()}, KL TB {d.volume[a:b].mean():,.0f}, GTGD TB {d.value[a:b].mean()/1e9:.1f} ty")
# ---- C. Toan bo du lieu: phien vuot bien do ----
tot = bad = 0; badsym = {}
for f in os.listdir(f"{D}/stocks_long"):
    s = f[:-4]; d = fl.load(f"{D}/stocks_long/{f}")
    if len(d) < 60: continue
    r = d.close.pct_change()["2016":]; n = int((r.abs() > lim(s) + 0.02).sum()); tot += len(r); bad += n
    if n: badsym[s] = n
print(f"\nC. Phien 2016+ co |lai ngay| vuot bien do + 2 diem %: {bad:,}/{tot:,} ({bad/tot*1e4:.1f} tren 10.000 phien), {len(badsym)} ma; nhieu nhat: {sorted(badsym.items(), key=lambda kv:-kv[1])[:8]}")
# ---- D. Doi chieu VCI (stocks_long) vs KBS (stocks) ----
rat = []
for f in os.listdir(f"{D}/stocks"):
    s = f[:-4]
    if not os.path.exists(f"{D}/stocks_long/{f}"): continue
    a = pd.read_csv(f"{D}/stocks/{f}", parse_dates=["date"]).set_index("date").close; b = pd.read_csv(f"{D}/stocks_long/{f}", parse_dates=["date"]).set_index("date").close
    j = pd.concat([a, b], axis=1, keys=["kbs","vci"]).dropna()["2022":]
    if len(j) > 50: q = (j.vci / j.kbs); rat.append(dict(sym=s, n=len(j), med=q.median(), pct_lech=(abs(q - 1) > 0.01).mean(), gia_1000=abs(q.median() - 1000) < 100))
Rt = pd.DataFrame(rat)
print(f"\nD. Doi chieu gia dong cua VCI vs KBS, 2022+, {len(Rt)} ma: ty le ngay lech >1% TB {Rt.pct_lech.mean()*100:.1f}%; so ma lech >1% o hon 20% so ngay: {(Rt.pct_lech>0.2).sum()}; ma lech 1000 lan (don vi): {Rt.gia_1000.sum()}")
print(Rt.sort_values("pct_lech", ascending=False).head(5).round(3).to_string(index=False))
