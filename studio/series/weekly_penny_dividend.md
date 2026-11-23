# Weekly data series: 15 Penny Stocks (Sat 12:00) + Dividend Week Ahead (Sun 18:00)

Owner's order (chat, 19 Nov 2026 21:24 IST): "create 15 penny stock for each week and create dividend
stock for each week". These are DATA reels, never a buy list (PIPELINE §3 still applies: no penny-stock
promotion, no buy/sell calls, risks next to any upside).

## 15 Penny Stocks of the Week (Saturday 12:00, built Saturday ~09:50)
- Universe: the Nifty 500 set the Friday movers run already computed: studio/weekmov/{large,mid,small}.csv
  (columns name,symbol,ind_key,prev_week_close,close,week_pct,mcap_cr), with period.json for the week.
  Use these only if period.json's end date is this Friday. Penny = Friday close under ₹50 (if fewer
  than 15, raise to ₹60 and say so on screen). Take the 15 cheapest and sort them by week_pct.
- Show for each: name, close ₹, week %, market cap. Add the 52-week high and % below it from
  get_indian_stocks_details for those 15 only.
- Template: motion/penny15 (build/gen.py + t.json) and studio/penny15 (lines/voices). Previous run: 13 Nov.
- A repeated message on screen and in the caption: "Low price ≠ cheap. Check market cap, debt and NSE
  ASM/GSM surveillance lists. Penny stocks are volatile and can hit lower circuits."
- History tag "penny-weekly".

## Dividend Week Ahead (Sunday 18:00, built Sunday ~14:30)
- Stocks whose EX-DIVIDEND date falls Mon–Fri of the coming week (mainboard NSE, market cap above
  ₹1,000 Cr, max 8, biggest dividend yield first). Sources: NSE corporate actions, plus one of
  Moneycontrol/Trendlyne/BSE corporate actions to cross-check ex-date, record date and ₹ per share.
- Yield shown = this dividend ÷ Friday close (INDmoney get_indian_stocks_details), and label it as
  "this payout" (not annual). Explain the ex-date rule once: buy before the ex-date to get it, and the
  price usually drops by about the dividend on the ex-date.
- If fewer than 3 qualify, make "Dividend payers to know" with trailing-12-month yields from INDmoney
  for 6 Nifty 500 stocks not featured in the last 4 weeks.
- Template: motion/divi6ta (build/gen.py) and studio/divi6 / divi6ta. History tag "dividend-weekly".

> Style (23 Nov 2026): owner's house style is the PCJ paper collage (studio/vox/pcj2.py look and sounds), no subtitles.
