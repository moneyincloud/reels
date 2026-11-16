"""Turn raw INDmoney candles into the movers CSVs + period.json.

usage: python3 compute.py week  2026-11-20
       python3 compute.py month 2026-11-30

Inputs (written by the fetch step, see RUNBOOK.md):
  members/{large,mid,small}.csv        name,symbol,ind_key   (index constituents)
  raw/{large,mid,small}.jsonl          one line per stock: {"ind_key": "...", "candles": [...]}
                                       candles = get_indian_stocks_ohlc(interval=1week|1month) as returned
  raw/index.json                       {"nifty50": [...], "nifty100": [...], "midcap150": [...],   (same interval)
                                        "nifty50_daily": [...]}                                    (1day candles)
Outputs: {large,mid,small}.csv, indices.json, period.json.  Exits 1 if coverage is below 98%.
"""
import csv, datetime as dt, json, os, sys

W = os.path.dirname(os.path.abspath(__file__)) + '/'
kind, end = sys.argv[1], dt.date.fromisoformat(sys.argv[2])
assert kind in ('week', 'month')


def day(c): return dt.date.fromisoformat(c['datetime_ist'][:10])


def in_period(d):
    if kind == 'week':
        return end - dt.timedelta(days=end.weekday()) - dt.timedelta(days=1) <= d <= end   # Sun..end (a Sunday Muhurat candle may be labelled Sun)
    return d.year == end.year and d.month == end.month


def pick(candles):
    """(prev_close, close) for the period that contains `end`, or None."""
    cs = sorted([c for c in candles if day(c) <= end], key=day)
    if len(cs) < 2 or not in_period(day(cs[-1])):
        return None
    return float(cs[-2]['close']), float(cs[-1]['close'])


IDX = json.load(open(W + 'raw/index.json'))
daily = sorted([c for c in IDX['nifty50_daily'] if day(c) <= end], key=day)
sess = [day(c) for c in daily if in_period(day(c)) and (kind == 'month' or day(c) >= end - dt.timedelta(days=end.weekday()))]
before = [day(c) for c in daily if day(c) < sess[0]]
prevd, last = before[-1], sess[-1]
if last != end:
    print(f'NOTE: last session {last} is before {end} (holiday?)')

bad = 0
for cap in ('large', 'mid', 'small'):
    mem = list(csv.DictReader(open(W + f'members/{cap}.csv')))
    raw = {}
    for line in open(W + f'raw/{cap}.jsonl'):
        line = line.strip()
        if line:
            r = json.loads(line); raw[r['ind_key']] = r['candles']
    out, miss = [], []
    for m in mem:
        p = pick(raw.get(m['ind_key'], []))
        if not p:
            miss.append(m['ind_key'] + ' ' + m['name']); continue
        out.append(dict(name=m['name'], symbol=m.get('symbol', ''), ind_key=m['ind_key'], prev_week_close=p[0], close=p[1],
                        week_pct=round((p[1] / p[0] - 1) * 100, 2), mcap_cr=''))
    with open(W + f'{cap}.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    cov = len(out) / len(mem)
    print(f'{cap}: {len(out)}/{len(mem)} ({cov:.0%})' + (f'  missing: {miss[:12]}' if miss else ''))
    if cov < 0.98: bad += 1

ind = {}
for k in ('nifty50', 'nifty100', 'midcap150'):
    p = pick(IDX.get(k, []))
    if p: ind[k] = dict(prev=p[0], close=p[1], pct=round((p[1] / p[0] - 1) * 100, 2))
json.dump(ind, open(W + 'indices.json', 'w'), indent=1)
if 'nifty50' not in ind or 'midcap150' not in ind:
    print('index candles missing'); bad += 1

D = lambda d: f'{d.day} {d.strftime("%b")}'
muhurat = prevd.weekday() >= 5
P = dict(kind=kind, end=str(last), start=str(sess[0]), prev_close=str(prevd), sessions=len(sess),
         prev_label=D(prevd) + (' (Muhurat)' if muhurat else ''), end_label=D(last),
         month_name=last.strftime('%B %Y'),
         range_label=(f'{sess[0].day}–{last.day} {last.strftime("%b").upper()} {last.year}' if sess[0].month == last.month
                      else f'{D(sess[0]).upper()} – {D(last).upper()} {last.year}') if kind == 'week' else last.strftime('%B %Y').upper())
json.dump(P, open(W + 'period.json', 'w'), indent=1)
print(json.dumps(P))
sys.exit(1 if bad else 0)
