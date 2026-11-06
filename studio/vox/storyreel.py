"""Money Story Ep1: The Raise That Disappeared (lifestyle creep). Storybook layers + emotion FX.
Layers: inpainted background + cut-out foreground (Karthi + props) with parallax, breathing, hops, emotion FX."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, re
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from scenes import stamp_c

SH = ROOT + 'storyreel/'
LAY = ROOT + 'storyreel/layers/'
SCRIPT = [l['text'] for l in json.load(open(SH + 'lines.json'))]
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.15 if i == 0 else 0.14)); _t = VO[-1] + d + 0.24
DUR = _t + 1.2
B = STARTS[1:]
MUST = (232, 160, 30); TERRA = (196, 92, 48); CREAM = (255, 246, 228); BROWN = (92, 52, 24); RED = (214, 52, 40); GRN = (40, 150, 80)


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase); assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def line_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s: i = k
    return i


@functools.lru_cache(None)
def layer(kind, n):
    im = Image.open(f'{LAY}{kind}{n}.png').convert('RGBA')
    s = max(W * 1.12 / im.size[0], H * 1.12 / im.size[1])     # cover + margin for motion
    return im.resize((int(im.size[0] * s), int(im.size[1] * s)), Image.LANCZOS)


@functools.lru_cache(None)
def head_xy(n):
    a = np.asarray(layer('fg', n))[..., 3] > 100
    ys, xs = np.where(a)
    # topmost 6% of the figure ~ head
    top = ys.min(); sel = ys < top + (ys.max() - top) * 0.12
    return float(xs[sel].mean()), float(top)


@functools.lru_cache(None)
def frame_border():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, (w, col) in enumerate([(26, (150, 70, 20)), (16, (226, 150, 40)), (6, (120, 50, 15))]):
        o = [0, 26, 42][k]
        d.rectangle((o, o, W - 1 - o, H - 1 - o), outline=col, width=w)
    for cx, cy in [(48, 48), (W - 48, 48), (48, H - 48), (W - 48, H - 48)]:
        for r, col in [(46, (226, 150, 40)), (32, (150, 70, 20)), (16, (255, 214, 120))]:
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
        for a in range(8):
            ang = a * math.pi / 4
            d.ellipse((cx + 58 * math.cos(ang) - 9, cy + 58 * math.sin(ang) - 9, cx + 58 * math.cos(ang) + 9, cy + 58 * math.sin(ang) + 9), fill=(226, 150, 40))
    for x in range(140, W - 140, 70):
        for y in (21, H - 21):
            d.polygon([(x, y - 9), (x + 9, y), (x, y + 9), (x - 9, y)], fill=(255, 214, 120))
    for y in range(140, H - 140, 70):
        for x in (21, W - 21):
            d.polygon([(x, y - 9), (x + 9, y), (x, y + 9), (x - 9, y)], fill=(255, 214, 120))
    return im


def scene(c, t, n, st, en, mood):
    q = clamp((t - st) / (en - st))
    bg, fg = layer('bg', n), layer('fg', n)
    # camera: slow push + drift; fg moves 1.6x more (parallax)
    z = 1.0 + 0.06 * q
    dx = -18 + 36 * q
    def put(im, k, extra_y=0.0, sx=1.0, sy=1.0, rot=0.0):
        w, h = int(im.size[0] * z * sx), int(im.size[1] * z * sy)
        r = im.resize((w, h), Image.BILINEAR)
        if rot: r = r.rotate(rot, Image.BILINEAR, expand=False, center=(w / 2, h))
        c.alpha_composite(r, (int(W / 2 - w / 2 + dx * k), int(H / 2 - h / 2 + extra_y + (h - h / sy * 1) * 0)))
    put(bg, 1.0)
    breathe = 1 + 0.010 * math.sin(t * 2.6)
    hop = 0.0; rot = 0.4 * math.sin(t * 1.3)
    if mood == 'happy':
        k = (t - st - 0.7) if t > st + 0.7 else -1
        if 0 <= k < 0.6: hop = -40 * math.sin(k / 0.6 * math.pi)
        rot += 1.2 * math.sin(t * 5)
    if mood == 'sad':
        hop = 12 * eo(prog(t, st, 0.8)); rot = 0.2 * math.sin(t * 1.0)
    fgh = fg.size[1] * z
    put(fg, 1.6, hop + fgh * (1 - breathe) * 0.5, 1.0, breathe, rot)
    return z, dx


def head_screen(n, z, dx):
    hx, hy = head_xy(n); fg = layer('fg', n)
    return W / 2 + (hx - fg.size[0] / 2) * z + dx * 1.6, H / 2 + (hy - fg.size[1] / 2) * z


def sparkle(c, x, y, t, k):
    d = ImageDraw.Draw(c); a = 0.5 + 0.5 * math.sin(t * 7 + k * 2.1); r = 10 + 18 * a
    d.polygon([(x, y - r), (x + r * 0.25, y - r * 0.25), (x + r, y), (x + r * 0.25, y + r * 0.25), (x, y + r), (x - r * 0.25, y + r * 0.25),
               (x - r, y), (x - r * 0.25, y - r * 0.25)], fill=(255, 236, 140), outline=BROWN)


def coin(c, x, y, s=1.0):
    d = ImageDraw.Draw(c); r = 30 * s
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 200, 50), outline=BROWN, width=4)
    d.text((x, y + 2), '₹', font=font('pop', int(34 * s)), fill=BROWN, anchor='mm')


def rain_cloud(c, x, y, t, a):
    d = ImageDraw.Draw(c, 'RGBA')
    for (ox, oy, r) in [(-60, 10, 48), (0, -14, 62), (64, 8, 50), (-20, 30, 44), (34, 32, 44)]:
        d.ellipse((x + ox - r, y + oy - r, x + ox + r, y + oy + r), fill=(110, 116, 130, int(235 * a)), outline=(60, 60, 70, int(255 * a)), width=4)
    for k in range(9):
        ph = (t * 1.8 + k * 0.37) % 1
        rx = x - 80 + k * 20; ry = y + 60 + ph * 220
        d.line((rx, ry, rx - 6, ry + 26), fill=(90, 150, 230, int(220 * a * (1 - ph))), width=5)


def sweat(c, x, y, t):
    ph = (t * 0.9) % 1
    d = ImageDraw.Draw(c, 'RGBA'); yy = y + ph * 60
    d.polygon([(x, yy - 26), (x + 16, yy + 6), (x - 16, yy + 6)], fill=(140, 200, 255, int(255 * (1 - ph))))
    d.ellipse((x - 16, yy - 6, x + 16, yy + 22), fill=(140, 200, 255, int(255 * (1 - ph))), outline=(40, 90, 160, int(255 * (1 - ph))), width=3)


def tag(s, bg, fg=(255, 255, 255), size=64):
    tt = text_img(s, 'anton', size, fg)
    w, h = tt.size[0] + 64, tt.size[1] + 30
    im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, w + 11, h + 11), 26, fill=BROWN)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=bg, outline=BROWN, width=6)
    im.alpha_composite(tt, (32, 15))
    return im


tag = functools.lru_cache(None)(tag)


def segs(i):
    return [(m.start(), m.end()) for m in re.finditer(r'[^.!?]+[.!?]*\s*', SCRIPT[i])]


def caption(c, t, i, cy=1660, size=48):
    if t < VO[i] - 0.05: return
    sp = clamp((t - VO[i]) / DURS[i]) * len(SCRIPT[i])
    sg = [g for g in segs(i) if g[0] <= sp][-1] if sp > 0 else segs(i)[0]
    words = SCRIPT[i][sg[0]:sg[1]].split()
    lines, cur = [], []
    for wd in words:
        if cur and text_w(' '.join(cur + [wd]), 'pop', size) > 860: lines.append(cur); cur = [wd]
        else: cur.append(wd)
    if cur: lines.append(cur)
    lh = int(size * 1.3)
    w = max(text_w(' '.join(l), 'pop', size) for l in lines) + 80; h = lh * len(lines) + 40
    im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w + 9, h + 9), 30, fill=BROWN)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=CREAM, outline=BROWN, width=5)
    pos = sg[0]; y = 20 + lh // 2
    for ln in lines:
        x = w / 2 - text_w(' '.join(ln), 'pop', size) / 2
        for wd in ln:
            col = BROWN if pos <= sp else (190, 160, 130)
            if pos <= sp and (wd.lower().startswith(('fifteen', 'zero', 'one', 'six', 'five', 'two', 'thirty', 'eighteen', 'twelve', 'ten')) or any(ch.isdigit() for ch in wd)): col = TERRA
            ti = text_img(wd, 'pop', size, col); im.alpha_composite(ti, (int(x - size * 0.12), int(y - ti.size[1] / 2)))
            x += text_w(wd + ' ', 'pop', size); pos += len(wd) + 1
        y += lh
    place(c, im, 540, cy - (h - 90) / 2)


# ---------------- reel ----------------
from fridge import follow_btn
SCN = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '11', '12', 'creep', 'lessons', '13', '14']
SINGLE = {'07', '11'}
MOOD = {0: 'calm', 1: 'happy', 2: 'happy', 3: 'happy', 4: 'happy', 5: 'happy', 7: 'sad', 8: 'calm', 9: 'calm', 12: 'happy', 15: 'calm', 16: 'happy'}


@functools.lru_cache(None)
def full_img(n, blur=0):
    im = Image.open(f'{LAY}bg{n}_full.png').convert('RGBA')
    s = max(W * 1.12 / im.size[0], H * 1.12 / im.size[1])
    im = im.resize((int(im.size[0] * s), int(im.size[1] * s)), Image.LANCZOS)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    return im


def single(c, t, n, st, en, blur=0, zoom=0.07):
    q = clamp((t - st) / (en - st)); im = full_img(n, blur); z = 1 + zoom * q
    w, h = int(im.size[0] * z), int(im.size[1] * z)
    c.alpha_composite(im.resize((w, h), Image.BILINEAR), (int(W / 2 - w / 2 - 10 + 20 * q), int(H / 2 - h / 2)))


def meter(c, t, spent):
    w, h = 820, 56; x0, y0 = 130, 1460
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((x0 + 8, y0 + 8, x0 + w + 8, y0 + h + 8), 28, fill=BROWN)
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 28, fill=CREAM, outline=BROWN, width=5)
    f = spent / 15000
    if f > 0: d.rounded_rectangle((x0 + 6, y0 + 6, x0 + 6 + (w - 12) * f, y0 + h - 6), 22, fill=RED if f >= 1 else TERRA)
    place(c, tag(f'RAISE USED: ₹{spent:,} / ₹15,000', BROWN, CREAM, 40), 540, y0 - 46)


SPEND = {2: ('+₹6,000 RENT', 6000, 'Six'), 3: ('+₹5,000 EMI', 11000, 'Five'), 4: ('+₹2,500 FOOD', 13500, 'Two'),
         5: ('+₹1,500 GADGETS', 15000, 'Another')}


def bulb(c, x, y, t, a):
    d = ImageDraw.Draw(c, 'RGBA'); g = 0.6 + 0.4 * math.sin(t * 6)
    for k in range(10):
        ang = k * math.pi / 5
        d.line((x + 70 * math.cos(ang), y + 70 * math.sin(ang), x + (90 + 12 * g) * math.cos(ang), y + (90 + 12 * g) * math.sin(ang)),
               fill=(255, 210, 60, int(255 * a)), width=6)
    d.ellipse((x - 48, y - 52, x + 48, y + 40), fill=(255, 236, 120, int(255 * a)), outline=(*BROWN, int(255 * a)), width=5)
    d.rectangle((x - 22, y + 38, x + 22, y + 66), fill=(160, 160, 170, int(255 * a)), outline=(*BROWN, int(255 * a)), width=4)


def creep_chart(c, t, st):
    d = ImageDraw.Draw(c)
    x0, y0, x1, y1 = 140, 1340, 960, 820
    d.line((x0, y0, x1, y0), fill=BROWN, width=6); d.line((x0, y0, x0, y1), fill=BROWN, width=6)
    p = eo(prog(t, st + 0.4, 2.2))
    for col, off, lab in [(GRN, 0, 'SALARY'), (RED, 22, 'SPENDING')]:
        pts = []
        for k in range(6):
            q = k / 5
            if q > p: break
            x = x0 + 40 + q * (x1 - x0 - 80); y = y0 - 60 - q * 420 - (k % 2) * 40 + off
            pts += [(x, y - 70), (x + (x1 - x0 - 80) / 5 * 0.0, y - 70)]
            pts.append((x, y))
        if len(pts) > 1: stroke(c, pts, 12, col)
        if p > 0.95:
            place(c, text_img(lab, 'anton', 44, col), x1 - 90, y0 - 60 - 420 + off - (110 if col == GRN else -40))
    place(c, text_img('SAVINGS STAY ₹0', 'anton', 56, RED), 540, y0 + 70, 1, 0, clamp((t - st - 2.6) * 3))


def card_txt(s, bg, fg=(255, 255, 255), size=74):
    return tag(s, bg, fg, size)


def _render(t):
    i = line_at(t)
    c = Image.new('RGBA', (W, H), CREAM)
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    n = SCN[i]; mood = MOOD.get(i, 'calm')
    if i in (10, 11):
        st = STARTS[10]; en = STARTS[12]
    hx = hy = None
    if n == 'creep':
        single(c, t, '05', st, en, blur=14)
        c.alpha_composite(Image.new('RGBA', (W, H), (255, 246, 228, 170)))
        place(c, card_txt('LIFESTYLE CREEP', RED, size=96), 540, 330, 0.6 + 0.4 * eback(prog(t, at(13, 'Lifestyle', -0.2), 0.4)), -3,
              clamp((t - at(13, 'Lifestyle', -0.2)) * 4))
        creep_chart(c, t, st)
    elif n == 'lessons':
        single(c, t, '13', st, en, blur=14)
        c.alpha_composite(Image.new('RGBA', (W, H), (255, 246, 228, 150)))
        for k, (ph, s, col) in enumerate([('Raise is not', 'RAISE IS NOT RICH', TERRA), ('Upgrade', 'UPGRADE IS NOT WEALTH', BROWN),
                                          ('Save the raise', 'SAVE THE RAISE FIRST', GRN)]):
            tk = at(14, ph, -0.15)
            if t < tk: continue
            p = prog(t, tk, 0.4)
            place(c, card_txt(s, col, size=70), 540 + (1 - eo(p)) * (700 if k % 2 else -700), 520 + k * 260, 1, [-3, 2, -2][k])
    elif n in SINGLE:
        single(c, t, n, st, en)
    else:
        z, dx = scene(c, t, n, st, en, mood)
        hx, hy = head_screen(n, z, dx)
    # ---- overlays per line ----
    if i == 0:
        place(c, tag('NEVER SPEND', TERRA, size=100), 540, 240, 0.5 + 0.5 * eback(prog(t, 0.05, 0.35)), -3)
        if t > at(0, 'next', -0.2): place(c, tag('YOUR NEXT RAISE', BROWN, (255, 214, 120), 90), 540, 400, 0.5 + 0.5 * eback(prog(t, at(0, 'next', -0.2), 0.35)), 2)
        if t > at(0, 'thirty', -0.15):
            pz = prog(t, at(0, 'thirty', -0.15), 0.22)
            place(c, stamp_c('₹34 LAKH MISSED', RED, 96, -8, 2), 540, 1330, 1 + 1.2 * (1 - eo(pz)), 0, clamp(pz * 4))
    elif i == 1:
        t1 = at(1, 'fifteen', -0.1)
        if t > t1:
            p = prog(t, t1, 0.35)
            place(c, tag('+₹15,000 HIKE', GRN, size=80), 540, 330, 0.5 + 0.5 * eback(p), -3)
            for k in range(8):
                kk = (t - t1 - k * 0.05)
                if 0 < kk < 1.4:
                    ang = -math.pi / 2 + (k - 3.5) * 0.32
                    coin(c, hx + math.cos(ang) * 420 * kk, hy + 60 + math.sin(ang) * 420 * kk + 380 * kk * kk, 0.9)
        for k, (ox, oy) in enumerate([(-170, 20), (160, -10), (-120, -90), (140, 110)]):
            if t > st + 0.4: sparkle(c, hx + ox, hy + oy, t, k)
    elif i in SPEND:
        s, total, ph = SPEND[i]
        tk = at(i, ph, -0.15)
        prev = SPEND[i - 1][1] if i - 1 in SPEND else 0
        if t > tk:
            p = prog(t, tk, 0.4)
            place(c, tag(s, RED, size=70), 540 + (1 - eo(p)) * (700 if i % 2 else -700), 330, 1, [-4, 3][i % 2])
        cur = prev + (total - prev) * eo(prog(t, tk, 0.6)) if t > tk else prev
        meter(c, t, int(cur))
        if i == 5 and t > tk + 0.8:
            place(c, stamp_c('RAISE: ₹0 LEFT', RED, 80, -6, 5), 540, 1280, 1, 0, clamp((t - tk - 0.8) * 4))
    elif i == 6:
        p = prog(t, st, 0.3)
        place(c, tag('1 YEAR LATER', TERRA, size=100), 540, 330, 1.6 - 0.6 * eback(p), -3, clamp(p * 3))
    elif i == 7:
        c.alpha_composite(Image.new('RGBA', (W, H), (120, 20, 10, int(60 * clamp((t - st) * 3)))))
        pz = prog(t, at(7, 'Zero', -0.1), 0.22)
        place(c, stamp_c('₹0 SAVED', RED, 130, -8, 3), 540, 1260, 1 + 1.2 * (1 - eo(pz)), 0, clamp(pz * 4))
        rain_cloud(c, hx, hy - 120, t, clamp((t - st - 0.2) * 3)); sweat(c, hx + 110, hy + 60, t)
    elif i == 8:
        p = prog(t, at(8, 'Raghavan', -0.2), 0.35)
        if p > 0: place(c, tag('RAGHAVAN SIR', (96, 110, 50), size=64), 540, 330, 0.5 + 0.5 * eback(p), -2)
        for k, (ox, oy) in enumerate([(-260, 300), (-120, 200), (60, 330)]):
            if t > st + 0.5: sparkle(c, 330 + ox + 200, 700 + oy, t, k)
    elif i == 9:
        bulb(c, 170, 470, t, clamp((t - at(9, 'Same', -0.2)) * 3))
        p = prog(t, at(9, 'Save the raise', -0.2), 0.4)
        if p > 0: place(c, tag('SAVE THE RAISE FIRST', GRN, size=72), 540, 330, 0.5 + 0.5 * eback(p), -2)
    elif i in (10, 11):
        for k in range(10):
            ts = STARTS[10] + 0.6 + k * 0.45
            q = (t - ts) / 0.7
            if 0 <= q <= 1: coin(c, 540 + (k % 3 - 1) * 60, 300 + q * 720, 1.2)
        if i == 11:
            p = prog(t, at(11, 'eighteen', -0.2), 0.35)
            place(c, tag('₹15,000 x 120 MONTHS', BROWN, CREAM, 60), 540, 300, 1, -2, clamp((t - st) * 3))
            if p > 0: place(c, tag('= ₹18 LAKH SAVED', GRN, size=86), 540, 450, 0.5 + 0.5 * eback(p), 2)
    elif i == 12:
        tk = at(12, 'could grow', -0.3)
        v = 18 + (34.4 - 18) * eo(prog(t, tk, 2.2)) if t > tk else 18
        place(c, tag(f'₹{v:.1f} LAKH', GRN, size=110), 540, 330, 1, -2)
        place(c, tag('Nifty 50 TRI 20-yr avg 12.44%/yr', BROWN, CREAM, 40), 540, 490, 1, 0, clamp((t - at(12, 'Nifty', -0.2)) * 3))
        if t > tk: 
            for k in range(6): sparkle(c, 260 + k * 110, 760 + (k % 2) * 120, t, k)
        place(c, text_img('Source: NSE Indices Nifty 50 whitepaper (data to 27 Feb 2026). My calculation. Past returns, not a promise.',
                          'osw5', 24, BROWN), 540, 1820)
    elif i == 15:
        p = prog(t, at(15, 'automatic', -0.2), 0.4)
        if p > 0: place(c, tag('AUTO SIP: ON', GRN, size=86), 540, 330, 0.5 + 0.5 * eback(p), -2)
        for k, (ox, oy) in enumerate([(-200, -60), (180, -20)]):
            sparkle(c, hx + ox, hy + oy, t, k)
    elif i == 16:
        tf = at(16, 'Follow', -0.1)
        if t > tf: place(c, follow_btn(), 540, 1250, 0.6 + 0.4 * eback(prog(t, tf, 0.35)), 2)
        if t > at(16, 'never', -0.2):
            place(c, tag('NEVER SPEND YOUR NEXT RAISE', TERRA, size=60), 540, 300, 1, -2, clamp((t - at(16, 'never', -0.2)) * 3))
    if i in (12,):
        pass
    if i not in (13, 14):
        caption(c, t, i)
    else:
        caption(c, t, i, cy=1620)
    place(c, text_img('Characters are fictional · Not a buy/sell call · Education only', 'osw5', 22, BROWN), 540, 1868)
    c.alpha_composite(frame_border())
    if i == 7 and 0 <= t - at(7, 'Zero', -0.1) < 0.4:
        k = math.exp(-(t - at(7, 'Zero', -0.1)) * 10) * 14; ox = k * math.sin(t * 90); oy = k * math.cos(t * 70)
        c = c.transform((W, H), Image.AFFINE, (1, 0, ox, 0, 1, oy), Image.BICUBIC)
    return c


def render(t):
    LOOP = 0.5
    if t > DUR - LOOP:
        a = np.asarray(_render(t).convert('RGB')).astype(float); bb = np.asarray(_render(1.5).convert('RGB')).astype(float)
        q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + bb * q).astype(np.uint8)
    for b in B:
        if b - 0.18 <= t < b and not (b in (STARTS[11],)):
            a = np.asarray(_render(t).convert('RGB')).astype(float); bb = np.asarray(_render(b + 0.01).convert('RGB')).astype(float)
            q = (t - (b - 0.18)) / 0.18
            return (a * (1 - q) + bb * q).astype(np.uint8)
    return np.asarray(_render(t).convert('RGB'))
