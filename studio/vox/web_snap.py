"""Snapshot frames of a web reel at given times and tile them. usage: web_snap.py <html> <out.jpg> t1 t2 ..."""
import sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
html, out, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]]
ims = []
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
    msgs = []; pg.on('console', lambda m: msgs.append(m.text)); pg.on('pageerror', lambda e: msgs.append('ERR ' + str(e)))
    pg.goto('file://' + html); pg.evaluate('window.ready')
    for t in ts:
        pg.evaluate(f'Promise.resolve(window.seek({t}))'); pg.wait_for_timeout(30)
        ims.append(Image.open(io.BytesIO(pg.screenshot(type='jpeg', quality=85))).resize((432, 768)))
    br.close(); print('\n'.join(msgs[:10]))
cols = min(5, len(ims)); rows = (len(ims) + cols - 1) // cols
S = Image.new('RGB', (cols * 432, rows * 768), 'white')
for i, im in enumerate(ims): S.paste(im, ((i % cols) * 432, (i // cols) * 768))
S.save(out, quality=85)
