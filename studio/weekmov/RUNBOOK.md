# Movers reels runbook (weekly + monthly)

Two reels per run: **Top Gainers** (male voice am_michael) and **Top Losers** (female voice af_heart),
top 10 in each of Nifty 100 / Nifty Midcap 150 / Nifty Smallcap 250. Posted through the GitHub
auto-post queue (YouTube Short + Instagram reel + trial reel + story).

Standing order from the owner (chat, 16 Nov 2026 09:46 IST): "every week top gain top loss reels,
create it on Friday and post it on Saturday morning; and create monthly reels for monthly top gained
and lose reels". So these runs queue the posts as approved. The owner can stop a post by deleting its
entry from autopost/queue.yaml before the publish time.

| run | when it is built | `KIND END` | gainers | losers |
|---|---|---|---|---|
| weekly | Friday after 16:00 IST | `week <Friday date>` | Sat 07:00 | Sat 09:00 |
| monthly | 1st of the month | `month <last day of previous month>` | 2nd 08:00 | 2nd 12:00 |

All paths below are relative to `/home/claude/reels`.

## 0. Setup
- Repo at /home/claude/reels (`add_repo moneyincloud/reels`, access push, if missing), `git pull`.
- `bash studio/setup.sh`; `cd motion/weekmov && npm install` if `node_modules` is missing.
- `export HYPERFRAMES_BROWSER_PATH=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell | tail -1)`
- Never use INDmoney portfolio / holdings / networth tools. Never place trades.

## 1. Constituents (members/*.csv)
`members/{large,mid,small}.csv` = name,symbol,ind_key. `members/ASOF.txt` says when they were last checked.
NSE rebalances these indices at the end of March and September (announced in Feb/Aug) and swaps single
names for mergers and demergers. Run one WebSearch for NSE index changes ("niftyindices press release
Nifty Midcap 150 Smallcap 250 replacement") since the ASOF date. If anything changed, edit the rows
(resolve new ind_keys with `lookup_ind_keys`) and update ASOF.txt. Skip a name that has no price yet.

## 2. Fetch candles (INDmoney, about 505 calls)
INDmoney allows ~500 calls per hour shared across everything, so the fetch takes 1–2 hours. Use 3
background helper agents, one per cap (large 100, mid 150, small 250), each told:
- For every row of `studio/weekmov/members/<cap>.csv` call
  `get_indian_stocks_ohlc(ind_key, interval=<1week|1month>, lookback=<14d for week | 1y for month>)`.
- Append one JSON line per stock to `studio/weekmov/raw/<cap>.jsonl`:
  `{"ind_key": "...", "candles": [<the last 3 candles exactly as returned>]}`
  (write in batches of ~20 with a small python snippet; do not rewrite earlier lines).
- On a rate-limit error, write what you have, stop, and report how many are done. The main session
  resumes the same agent with SendMessage after waiting (wait ~20 minutes with a Monitor until-loop first).
- Skip keys already present in the jsonl (resumable).
Main session also writes `studio/weekmov/raw/index.json` with the same interval/lookback for the index
keys in `members/index_keys.json` (Nifty 50, Nifty 100, Nifty Midcap 150) plus `"nifty50_daily"` = Nifty 50 `1day` candles, lookback 14d
(week) or 1y (month).

## 3. Compute + sanity check
`python3 studio/weekmov/compute.py <KIND> <END>` → CSVs, indices.json, period.json. It exits 1 under
98% coverage per cap: fetch the missing keys it prints and rerun.
Then check the 3 biggest gainers and 3 biggest losers overall against `1day` candles (prev close and
last close must match). A move above 40% needs a reason (results, demerger, split/bonus, circuit): if
it is a corporate action (split/bonus/demerger) the % is fake → drop that stock from members for this
run only and rerun compute. Note any stock in "Trade for Trade"/ASM in the report.

## 4. Build both reels
```
cd motion/weekmov/build && python3 prep.py           # prints both scripts; read them
```
Add pronunciation fixes to `build/say.json` for acronyms/odd names (e.g. "PB Fintech": "P B Fintech"),
long names to `NAMES` in prep.py, rerun prep.py. Then for mode in gain, loss:
```
cd studio && python3 kokoro/vo_cast.py weekmov_<mode>
python3 myvoice/asr.py weekmov_<mode>/vo/*.wav         # every company name recognisable?
cd vox && python3 weekmov_audio.py weekmov_<mode>
cp ../weekmov_<mode>/mix.wav ../../motion/weekmov/assets/vo_mix.wav
cd ../../motion/weekmov && python3 build/gen.py <mode> && npm run check   # must say "Check passed"
npx hyperframes snapshot --at 1.5,4,10,19,28,34      # read the contact sheet: nothing clipped/overlapping
npm run render && mv "$(ls -t renders/weekmov_*.mp4 | head -1)" renders/<mode>.mp4
```
If check fails with clipped names: shorten via NAMES; the row font already shrinks for long names.

## 5. Covers, queue, push
```
python3 studio/weekmov/cover/build.py && (cd studio/weekmov/cover && node shot.js)   # read the 4 jpgs
python3 studio/weekmov/make_queue.py "<gain time>" "<loss time>" "standing order: owner chat 16 Nov 2026 09:46 IST"
python3 -c "import yaml; yaml.safe_load(open('autopost/queue.yaml'))"           # must parse
```
Read the two new queue entries (numbers must match the CSVs). Archive the data:
`mkdir -p studio/weekmov/history/<KIND>_<END> && cp studio/weekmov/{large,mid,small}.csv studio/weekmov/{indices,period}.json studio/weekmov/history/<KIND>_<END>/`
Update `studio/state.json` history (tag "movers-weekly"/"movers-monthly"; last_voice stays as is: this
series always uses male for gainers, female for losers). Commit (message ends with the Co-Authored-By
line) → `git pull --rebase` → push. Pushing queue.yaml starts the auto-post workflow; it posts at the
publish times.

## Final message to the owner (under 180 words)
"Movers reels ready · <period>": top gainer and top loser with %, the 3 per cap in one line each,
post times, any data notes (T2T/ASM stocks, dropped corporate actions), and
"To stop a post, delete its entry in autopost/queue.yaml (github.com/moneyincloud/reels) before the time,
or tell me in chat." If anything failed, say exactly what, and do not queue a half-finished reel.
