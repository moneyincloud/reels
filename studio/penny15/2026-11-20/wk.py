import json
# (name, symbol, ind_key, prev_close_13Nov, close_20Nov) from get_indian_stocks_ohlc 1week 14d, retrieved 2026-11-21 09:55 IST
R=[("Vodafone Idea","IDEA","INDS03017",12.57,12.15),("JP Power","JPPOWER","INDS02953",14.07,13.37),
("Yes Bank","YESBANK","INDS02937",17.42,17.91),("Reliance Power","RPOWER","INDS01338",18.55,17.66),
("IRB Infra","IRB","INDS03137",18.78,18.05),("Trident","TRIDENT","INDS00196",23.54,23.39),
("UCO Bank","UCOBANK","INDS02381",24.84,25.42),("Vedanta Iron & Steel","VISL","INDS43035",26.34,23.88),
("Vedanta Oil & Gas","VOGL","INDS43040",30.87,29.19),("Bharat Coking Coal","BHARATCOAL","INDS40658",31.54,30.46),
("Indian Overseas Bank","IOB","INDS00229",31.63,31.99),("Central Bank","CENTRALBK","INDS01862",32.22,34.37),
("Ola Electric","OLAELEC","INDS32068",34.65,32.59),("Vedanta Power","VEDPOWER","INDS43055",34.92,34.70),
("Tata Teleservices","TTML","INDS01930",37.90,36.02),("Suzlon","SUZLON","INDS02952",38.25,36.96),
("NMDC Steel","NSLNISP","INDS24432",40.54,38.85),("Motherson Wiring","MSUMI","INDS04083",39.02,42.71),
("Sagility","SAGILITY","INDS33697",43.87,45.25),("MMTC","MMTC","INDS00035",55.83,51.34),("SJVN","SJVN","INDS02595",57.41,55.78)]
pen=sorted([r for r in R if r[4]<50],key=lambda r:r[4])
print(len(pen),'under 50')
top=pen[:15]
out=[dict(name=n,symbol=s,ind_key=k,prev=p,close=c,week_pct=round((c/p-1)*100,2)) for n,s,k,p,c in top]
out.sort(key=lambda d:-d['week_pct'])
for d in out: print(d)
json.dump(out,open('week.json','w'),indent=1)
