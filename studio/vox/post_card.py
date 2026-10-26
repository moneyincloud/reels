"""Single-image Instagram feed post (1080x1350) in the paper style.

Usage: python3 post_card.py spec.json out.jpg
spec = {
  "kind": "fact" | "mythfact" | "quiz" | "stat",
  "kicker": "DID YOU KNOW?",              # small top line
  "title": "MRF SHARE ₹1,17,915",          # big line (fact/stat/quiz)
  "body": ["one line", "another line"],    # 1-4 short lines
  "myth": ["Low price =", "cheap stock"], "fact": ["Check profits,", "debt, valuation"],   # mythfact
  "options": ["A  ...", "B  ...", "C  ..."],   # quiz (answer goes in the caption/first comment)
  "big": "-59%", "big_colour": "red",      # stat
  "source": "NSE via INDmoney, 23 Oct 2026",
  "cta": "SAVE THIS · SEND TO A FRIEND"
}
Always keep "Education only. Not investment advice." (added automatically at the bottom).
"""
import sys, json
from PIL import Image, ImageDraw
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from lib import *
from scenes import stamp_c, bgs
import saveshare as SS

W2, H2 = 1080, 1350
COL = {'red': RED, 'green': GRN, 'ink': INK, 'navy': (30, 60, 120), 'yellow': YEL}


def build(spec):
    pbg, _ = bgs(); c = pbg.crop((0, 0, W2, H2)).copy(); d = ImageDraw.Draw(c)
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, INK, 1), (52, 50))
    d.line((60, 100, W2 - 60, 100), fill=INK, width=2)
    k = spec.get('kind', 'fact')
    if spec.get('kicker'): place(c, text_img(spec['kicker'], 'mark', 56, (30, 60, 120)), 540, 175, 1, -2)
    if k == 'mythfact':
        SS.myth_fact(c, 5, 0, spec.get('myth', []), spec.get('fact', []), y0=240, y1=1080)
    else:
        if spec.get('title'):
            t = spec['title']; size = 110 if len(t) < 16 else 84 if len(t) < 24 else 64
            place(c, text_img(t, 'anton', size, INK), 540, 300)
        if k == 'stat' and spec.get('big'):
            place(c, stamp_c(spec['big'], COL.get(spec.get('big_colour', 'red'), RED), 220, -6, 31), 540, 560)
        y = 830 if k == 'stat' else 470
        if k == 'quiz':
            for j, o in enumerate(spec.get('options', [])[:4]):
                place(c, SS._card(880, 130), 540, y + j * 160, 1, (-1, 1, -0.5, 0.8)[j]); place(c, text_img(o, 'anton', 58, INK), 540, y + j * 160)
            y += 160 * len(spec.get('options', [])[:4]) + 20
            place(c, text_img('answer in the first comment 👇'.replace(' 👇', ''), 'mark', 50, RED), 540, y, 1, -2); y += 80
        else:
            for j, ln in enumerate(spec.get('body', [])[:4]):
                place(c, text_img(ln, 'osw', 56, INK), 540, y + j * 80)
    if spec.get('cta'):
        place(c, SS.bookmark_icon(80), 170, 1150, 1, -8); place(c, text_img(spec['cta'], 'anton', 56, INK), 580, 1150)
    if spec.get('source'): place(c, text_img('Source: ' + spec['source'], 'type', 24, (120, 116, 108)), 540, 1245)
    place(c, text_img('Education only. Not investment advice.', 'type', 24, (120, 116, 108)), 540, 1285)
    return c


if __name__ == '__main__':
    spec = json.load(open(sys.argv[1])); build(spec).convert('RGB').save(sys.argv[2], quality=92); print('post ok', sys.argv[2])
