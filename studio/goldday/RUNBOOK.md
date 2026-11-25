# Gold Today carousel — daily runbook (Mon–Fri, owner's standing order 25 Nov 2026: "post daily morning gold price comex prediction in carousel image")
Goal: a 5–6 slide carousel queued for 08:00 IST, before MCX opens at 9:00. It is a FORMULA ESTIMATE from overnight Comex + rupee, never a forecast or a buy/sell call.

1. Data (real numbers only; note the source and time of each):
   - Comex gold $/oz: the latest Comex gold futures (front month) price at build time, from WebSearch/WebFetch (Kitco, CME, GoldSeek/Dow Jones, Trading Economics). Also the previous settlement for the % change.
   - USD/INR: the latest close (PTI report, or Trading Economics) — previous trading day.
   - MCX gold previous close: INDmoney `lookup_ind_keys(["gold"], filter_type="IN_COMMODITY")` → `get_indian_stocks_details` → `prev_close` of the front GOLD future.
   - Yesterday's check: from history.json, the previous estimate; its MCX open = `get_indian_stocks_ohlc(<gold fut key>, 1day, 7d)` open of that date. Add it as `check`.
2. Write studio/goldday/<YYYY-MM-DD>.json (fields in carousel_goldday.py docstring), then `cd studio/vox && python3 carousel_goldday.py ../goldday/<date>.json`. READ every slide image before queueing.
3. Append {date, est} to history.json (fill mcx_open the next day).
4. Skip NSE/MCX holidays (if MCX is closed today, stop and report).
5. Queue a carousel entry (platforms [instagram], images: the slide files) at publish_at "<date> 08:00", approved: true with comment "standing order: owner chat 25 Nov 2026 – daily gold carousel".
   Caption: hook line with the estimate, the 3 inputs with sources, the formula, "Estimate, not a forecast. Not a buy/sell call. Education only.", 3–5 hashtags (#goldrate #goldpricetoday #mcx #comex #moneyincloud).
