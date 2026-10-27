"""2D paper-cutout scene backgrounds for the Tamil story reel (moneyincloud paper Vox style).
scene(i, ts, T) -> RGBA 1080x1920 canvas, ts = seconds into scene i, T = scene length."""
import math, functools
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from scenes import bgs
import paperchars as P
from storyta_txt import text_ta

ROADY = 1330


@functools.lru_cache(maxsize=1)
def paper():
    pbg, _ = bgs(); return pbg.resize((W, H)).convert('RGBA')


def tint(c, col, a):
    c.alpha_composite(Image.new('RGBA', c.size, col + (int(a),)))


def hills(c, off=0.0, col=(196, 214, 170), y=1180):
    d = ImageDraw.Draw(c)
    pts = [(x, y - 70 * math.sin((x + off) / 230) - 40 * math.sin((x + off) / 90)) for x in range(-20, W + 40, 20)]
    d.polygon(pts + [(W + 40, H), (-20, H)], fill=col, outline=INK); d.line(pts, fill=INK, width=6)


def road(c, scroll=0.0, y=ROADY):
    d = ImageDraw.Draw(c)
    d.rectangle((0, y, W, y + 240), fill=(92, 90, 88)); d.line((0, y, W, y), fill=INK, width=7); d.line((0, y + 240, W, y + 240), fill=INK, width=7)
    off = -(scroll % 260)
    for x in range(int(off) - 260, W + 260, 260): d.rounded_rectangle((x, y + 110, x + 140, y + 130), 8, fill=(250, 240, 200))
    d.rectangle((0, y + 244, W, H), fill=(214, 196, 150))


def sun(c, x, y, r=110, col=(255, 196, 64)):
    d = ImageDraw.Draw(c); d.ellipse((x - r, y - r, x + r, y + r), fill=col, outline=INK, width=6)


def trees(c, scroll, y=ROADY + 10, gap=420, s=0.8):
    off = -(scroll % gap)
    for k, x in enumerate(range(int(off) - gap, W + gap, gap)):
        t = P.tree(k % 2, s); place(c, t, x + 150, y - t.size[1] / 2 + 20)


def signpost(c, x, y, txt, p=1.0):
    im = Image.new('RGBA', (560, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((250, 150, 290, 510), fill=(120, 80, 50), outline=INK, width=6)
    d.polygon([(20, 40), (470, 40), (540, 120), (470, 200), (20, 200)], fill=GRN, outline=INK); d.line([(20, 40), (470, 40), (540, 120), (470, 200), (20, 200), (20, 40)], fill=INK, width=7)
    tx = text_ta(txt, 70, CREAM); im.alpha_composite(tx, (int(250 - tx.size[0] / 2 + 20), int(120 - tx.size[1] / 2)))
    place(c, P.shadowed(im), x, y, p)


def bob(ts, f=2.2, a=10): return a * math.sin(ts * f * math.pi)


def s0_hook(c, ts, T):
    sun(c, 820, 700, 120); hills(c, ts * 40); road(c, ts * 120)
    place(c, P.person(mask=True, bag=True, shirt=(40, 90, 150), pants=(50, 50, 60), pose='down'), 540, 1050 + abs(bob(ts, 1.6, 16)), 1.05, bob(ts, 1.6, 2))
    # empty pocket: flying moth puff
    if ts > 0.8:
        q = ((ts - 0.8) % 2.2) / 2.2; d = ImageDraw.Draw(c)
        for k in range(3):
            x = 720 + 60 * k + 30 * math.sin(q * 6 + k); y = 1060 - 260 * q - 20 * k
            d.ellipse((x - 12, y - 12, x + 12, y + 12), outline=(150, 140, 120), width=5)


def s1_lift(c, ts, T):
    sun(c, 860, 620, 100); hills(c, 0); road(c, 0); trees(c, 0)
    place(c, P.person(mask=True, bag=True, shirt=(40, 90, 150), pants=(50, 50, 60), pose='up'), 170, 1060, 0.9)
    k = eo(clamp(ts / 2.2)); x = 1700 - 920 * k
    place(c, P.lorry(), x, 1280 + (0 if k >= 1 else bob(ts, 6, 4)), 0.8)


def s2_cab(c, ts, T):
    d = ImageDraw.Draw(c)
    # windshield view
    d.rectangle((0, 0, W, H), fill=(246, 241, 230))
    win = Image.new('RGBA', (W, 900), (0, 0, 0, 0)); sub = paper().crop((0, 0, W, 900)).copy()
    sun(sub, 760, 300, 90); hills(sub, ts * 260, y=640); road(sub, ts * 600, y=760); trees(sub, ts * 600, y=770, s=0.55)
    c.alpha_composite(sub, (0, 380))
    d.rectangle((0, 1240, W, H), fill=(120, 70, 45)); d.line((0, 1240, W, 1240), fill=INK, width=8)
    d.rectangle((0, 360, W, 400), fill=INK); d.rectangle((0, 1200, W, 1250), fill=INK)
    d.line((540, 380, 540, 1240), fill=INK, width=24)
    place(c, P.person(mask=True, bag=False, shirt=(40, 90, 150), pants=(50, 50, 60), mood='calm'), 280, 1300 + bob(ts, 3, 4), 1.0)
    mood = 'sad' if ts > T * 0.45 else 'happy'
    place(c, P.person(skin='c', mustache=True, shirt=(250, 250, 245), pants=(80, 70, 60), pose='wheel', mood=mood), 800, 1300 + bob(ts, 3.2, 4), 1.0)
    d = ImageDraw.Draw(c); a = ts * 0.6
    d.ellipse((690, 1290, 910, 1510), outline=INK, width=22); d.line((800, 1400, 800 + 100 * math.cos(a), 1400 + 100 * math.sin(a)), fill=INK, width=14)


def s3_why(c, ts, T):
    tint(c, (40, 50, 70), 60 + 30 * clamp(ts / T))
    beat = 1 + 0.035 * max(0, math.sin(ts * 2 * math.pi * 1.1)) ** 8
    place(c, P.person(skin='c', mustache=True, shirt=(250, 250, 245), mood='sad', pose='down'), 540, 1250, 1.75 * beat)
    if ts > T * 0.5:  # memory polaroid
        q = eback(prog(ts, T * 0.5, 0.5)); pol = Image.new('RGBA', (360, 400), (255, 255, 255, 255)); dd = ImageDraw.Draw(pol)
        dd.rectangle((0, 0, 359, 399), outline=INK, width=6); dd.rectangle((24, 24, 336, 300), fill=(240, 220, 180)); h = P.house().resize((300, 233))
        pol.alpha_composite(h, (30, 50)); place(c, P.shadowed(pol), 820, 760, q * 0.9, 8)


def s4_scam(c, ts, T):
    d = ImageDraw.Draw(c); d.rectangle((0, 1280, W, H), fill=(214, 196, 150)); d.line((0, 1280, W, 1280), fill=INK, width=7)
    gone = clamp((ts - T * 0.72) / 0.35)
    if gone < 1:
        b = P.booth(); bb = b.copy(); dd = ImageDraw.Draw(bb)
        tx = text_ta('இரட்டிப்பு!', 58, RED); bb.alpha_composite(tx, (int(bb.size[0] / 2 - tx.size[0] / 2), int(125 - tx.size[1] / 2)))
        tx2 = text_ta('2×', 90, YEL); bb.alpha_composite(tx2, (int(bb.size[0] / 2 - tx2.size[0] / 2), 290))
        place(c, bb, 760, 1020, 1 - gone * 0.9, gone * 30, 1 - gone)
    else:
        q = clamp((ts - T * 0.72 - 0.35) / 0.6); dd = ImageDraw.Draw(c)
        for k in range(10):
            a = k * 0.63; r = 80 + 260 * q
            x = 760 + r * math.cos(a); y = 1020 + r * math.sin(a); s = 46 * (1 - q)
            if s > 2: dd.ellipse((x - s, y - s, x + s, y + s), fill=(235, 230, 220), outline=INK, width=4)
    mood = 'happy' if ts < T * 0.72 else 'wow'
    place(c, P.person(skin='b', mustache=True, shirt=(255, 255, 255), pants=(240, 235, 225), mood=mood, pose='up' if ts < T * 0.7 else 'head'), 290, 1080, 0.95)
    # coins flying into booth
    if gone < 1:
        for k in range(6):
            q = ((ts * 0.9 + k / 6) % 1.0)
            if ts < 0.3: break
            x = 380 + 380 * q; y = 900 - 220 * math.sin(math.pi * q)
            place(c, P.coin_img(28), x, y, 1, q * 360)


def s5_fight(c, ts, T):
    tint(c, (226, 58, 44), 25)
    shake = 8 * math.sin(ts * 40) * clamp(1 - ts / 1.2)
    place(c, P.person(skin='b', mustache=True, shirt=(255, 255, 255), pants=(240, 235, 225), mood='angry', pose='up'), 260 + shake, 1050, 0.95)
    place(c, P.person(skin='b', saree=True, shirt=(0, 137, 123), mood='cry', pose='head'), 560, 1060, 0.92)
    k = clamp((ts - T * 0.5) / (T * 0.45)); x = 820 + 500 * eio(k)
    place(c, P.person(skin='a', kid=True, bag=True, shirt=(255, 160, 0), pants=(60, 60, 120), mood='sad', pose='down'), x, 1130 - abs(bob(ts, 3, 18)), 1.0, -6 * k)
    if ts < 1.0: place(c, text_img('!!', 'anton', 140, RED), 260, 560, pop(ts, 0.0) if False else eback(clamp(ts / 0.3)))


def s6_turn(c, ts, T):
    tint(c, (250, 140, 60), 40)
    sun(c, 540, 1080, 170, (255, 140, 60)); hills(c, ts * 30, (180, 170, 140)); road(c, ts * 260); trees(c, ts * 260)
    k = clamp((ts - T * 0.7) / 0.9)
    if k > 0: signpost(c, 840, 1060, 'சொந்த ஊர்', eback(k))
    flip = ts > T * 0.78
    lr = P.lorry(); lr = lr.transpose(Image.FLIP_LEFT_RIGHT) if flip else lr
    place(c, lr, 460, 1290 + bob(ts, 6, 3), 0.82, (-4 * math.sin(math.pi * clamp((ts - T * 0.78) / 0.6))))


def s7_home(c, ts, T):
    sun(c, 900, 520, 90); hills(c, 0, (190, 210, 160), 1150)
    d = ImageDraw.Draw(c); d.rectangle((0, 1330, W, H), fill=(214, 196, 150)); d.line((0, 1330, W, 1330), fill=INK, width=7)
    place(c, P.house(), 540, 900, 0.95)
    k = clamp((ts - 0.6) / 2.2)
    mx = 820 - 220 * eio(k)
    hugging = k >= 1
    place(c, P.person(skin='c', mustache=True, shirt=(250, 250, 245), pants=(80, 70, 60), mood='cry' if hugging else 'sad', pose='hug' if hugging else 'down'), 380, 1150, 0.9)
    place(c, P.person(skin='b', saree=True, shirt=(0, 137, 123), old=True, mood='cry', pose='hug' if hugging else 'both_up'), mx, 1160 - (0 if hugging else abs(bob(ts, 3, 14))), 0.88)
    if ts > T * 0.4: place(c, P.person(skin='b', mustache=True, old=True, shirt=(255, 255, 255), pants=(240, 235, 225), mood='cry'), 900, 1170, 0.8)
    if hugging:  # hearts
        for j in range(4):
            q = ((ts * 0.5 + j / 4) % 1)
            place(c, text_img('♥', 'anton', 70, RED) if False else heart(), 470 + 60 * math.sin(j * 2 + q * 5), 820 - 300 * q, 0.8, 0, 1 - q)


@functools.lru_cache(maxsize=1)
def heart():
    im = Image.new('RGBA', (90, 84), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((4, 4, 48, 48), fill=RED, outline=INK, width=4); d.ellipse((42, 4, 86, 48), fill=RED, outline=INK, width=4)
    d.polygon([(8, 34), (82, 34), (45, 80)], fill=RED); d.line([(8, 34), (45, 80), (82, 34)], fill=INK, width=4)
    return im


def s8_end(c, ts, T):
    tint(c, (250, 120, 50), 70); sun(c, 540, 1180, 220, (255, 120, 50)); hills(c, 0, (150, 120, 110)); road(c, ts * 60)
    place(c, P.person(mask=True, bag=True, shirt=(40, 90, 150), pants=(50, 50, 60)), 540 + ts * 20, 1150, 0.7)


SC = [s0_hook, s1_lift, s2_cab, s3_why, s4_scam, s5_fight, s6_turn, s7_home, s8_end]


def scene(i, ts, T):
    c = paper().copy(); SC[i](c, ts, T); return c
