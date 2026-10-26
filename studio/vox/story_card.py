"""Instagram Story image for a reel: the hook thumbnail + 'NEW REEL' banner + 'tap @moneyincloud' pointer.

Usage: python3 story_card.py <thumbnail.jpg> <out_story.jpg> [label]
Instagram's API cannot add clickable link stickers, so the Story points viewers to the profile instead.
Thumbnail art sits in y 420–1500; the banner uses the top band and the pointer uses the bottom band.
"""
import sys, os
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *


def build(thumb, label='NEW REEL · OUT NOW'):
    c = Image.open(thumb).convert('RGBA').resize((W, H)); d = ImageDraw.Draw(c)
    # top banner
    b = text_img(label, 'anton', 76, INK); bw, bh = b.size[0] + 90, b.size[1] + 40
    bx, by = (W - bw) // 2, 170
    d.rounded_rectangle((bx + 10, by + 10, bx + bw + 10, by + bh + 10), 30, fill=INK)
    d.rounded_rectangle((bx, by, bx + bw, by + bh), 30, fill=YEL, outline=INK, width=7)
    c.alpha_composite(b, (bx + 45, by + 20))
    # bottom pointer
    t1 = text_img('TAP', 'anton', 64, CREAM); t2 = text_img('@moneyincloud', 'anton', 64, YEL); t3 = text_img('TO WATCH', 'anton', 64, CREAM)
    gap = 22; tw = t1.size[0] + t2.size[0] + t3.size[0] + 2 * gap; th = max(t1.size[1], t2.size[1]) + 44
    px, py = (W - tw - 80) // 2, 1610
    d.rounded_rectangle((px, py, px + tw + 80, py + th), 40, fill=(20, 20, 22, 235), outline=CREAM, width=5)
    x = px + 40
    for t in (t1, t2, t3): c.alpha_composite(t, (x, py + 22)); x += t.size[0] + gap
    ax = W // 2; ay = py - 30
    d.polygon([(ax - 40, ay - 50), (ax + 40, ay - 50), (ax, ay)], fill=YEL, outline=INK)
    return c


if __name__ == '__main__':
    lab = sys.argv[3] if len(sys.argv) > 3 else 'NEW REEL · OUT NOW'
    build(sys.argv[1], lab).convert('RGB').save(sys.argv[2], quality=92); print('story ok', sys.argv[2])
