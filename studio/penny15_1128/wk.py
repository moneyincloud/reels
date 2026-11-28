import json
# (name, symbol, ind_key, prev_close_20Nov, close_27Nov) from studio/weekmov/*.csv (INDmoney 1week candles, movers run 27 Nov);
# 52w high + mcap from get_indian_stocks_details, price_updated 27 Nov 2026 ~16:00 IST, retrieved 28 Nov 09:57 IST.
# Spot-check 1day candles: BHARATCOAL 30.46->31.12, TTML 36.02->33.81 (match).
R=[("Vodafone Idea","IDEA","INDS03017",12.15,11.55,15.79,125136.21),
("JP Power","JPPOWER","INDS02953",13.37,13.14,24.5,9005.44),
("Reliance Power","RPOWER","INDS01338",17.66,17.11,40.8,7076.3),
("IRB Infra","IRB","INDS03137",18.05,17.3,23.95,20894.94),
("Yes Bank","YESBANK","INDS02937",17.91,17.8,25.78,55876.97),
("Trident","TRIDENT","INDS00196",23.39,23.68,30.94,12067.22),
("UCO Bank","UCOBANK","INDS02381",25.42,24.26,31.75,30420.97),
("Vedanta Iron & Steel","VISL","INDS43035",23.88,24.29,44.78,9498.33),
("Vedanta Oil & Gas","VOGL","INDS43040",29.19,29.43,47.6,11508.27),
("Indian Overseas Bank","IOB","INDS00229",31.99,30.79,40.3,59291.04),
("Bharat Coking Coal","BHARATCOAL","INDS40658",30.46,31.12,45.09,14492.58),
("Ola Electric","OLAELEC","INDS32068",32.59,32.04,49.05,16015.77),
("Central Bank","CENTRALBK","INDS01862",34.37,32.99,40.92,29860.57),
("Tata Teleservices","TTML","INDS01930",36.02,33.81,54.78,6609.61),
("Vedanta Power","VEDPOWER","INDS43055",34.7,34.05,49.88,13314.87)]
out=[dict(name=n,symbol=s,ind_key=k,prev=p,close=c,week_pct=round((c/p-1)*100,2),hi52=h,mcap_cr=m,below_hi=round((c/h-1)*100,1)) for n,s,k,p,c,h,m in R]
out.sort(key=lambda d:-d['week_pct'])
for d in out: print(d['name'],d['close'],d['week_pct'],d['below_hi'],d['mcap_cr'])
json.dump(out,open('week.json','w'),indent=1)
