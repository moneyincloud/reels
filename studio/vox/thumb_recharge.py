"""Thumbnail in the Data Storytelling look (cream sheet, dot grid, pencil notes) for the recharge reel."""
import math
from PIL import Image, ImageDraw, ImageFont
FD = '../fonts/'
W, H = 1080, 1920
PAPER = (243, 236, 220); INK = (43, 38, 34); RED = (200, 55, 45); BLUE = (47, 93, 158)
c = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(c)
for y in range(0, H, 36):
    for x in range(0, W, 36): d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(222, 213, 196))
F = lambda f, s: ImageFont.truetype(FD + f, s)
serif = lambda s: F('playfair-display-latin-800-normal.woff', s)
hand = lambda s: F('permanent-marker-latin-400-normal.woff', s)
mono = lambda s: F('special-elite-latin-400-normal.woff', s)
rup = lambda s: F('Poppins-Bold.ttf', s)
def ctext(t, f, y, col, x=W // 2):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=col)
d.text((52, 60), '@moneyincloud', font=mono(32), fill=INK); d.line((60, 118, W - 60, 118), fill=INK, width=2)
ctext('Your recharge', serif(118), 300, INK); ctext('may cost more.', serif(118), 440, INK)
# phone
d.rounded_rectangle((300, 650, 780, 1250), 46, outline=INK, width=10, fill=(251, 247, 238)); d.line((490, 690, 590, 690), fill=INK, width=8)
ctext('RECHARGE · 28 DAYS', mono(34), 740, INK)
ctext('₹189', rup(150), 820, (150, 140, 130)); d.line((360, 920, 720, 880), fill=RED, width=12)
ctext('₹217?', rup(170), 990, RED)
pts = [(540 + 300 * (1 + 0.04 * math.sin(i * 1.7)) * math.cos(-0.6 + i / 40 * 2 * math.pi * 0.93), 1090 + 120 * (1 + 0.04 * math.sin(i * 1.7)) * math.sin(-0.6 + i / 40 * 2 * math.pi * 0.93)) for i in range(41)]
d.line(pts, fill=RED, width=8)
ctext('you pay 13 times a year', hand(78), 1330, BLUE)
for i, (t, bg, fg) in enumerate((('JIO', (15, 60, 201), (255, 255, 255)), ('AIRTEL', (228, 0, 0), (255, 255, 255)), ('Vi', (242, 194, 0), INK))):
    f = F('anton-latin-400-normal.woff', 64); w = d.textlength(t, font=f) + 50; x = [230, 540, 850][i] - w / 2
    d.rounded_rectangle((x, 1490, x + w, 1590), 16, fill=bg, outline=INK, width=5); d.text((x + 25, 1497), t, font=f, fill=fg)
ctext('DO THIS BEFORE THE HIKE', serif(60), 1660, RED)
c.save('../out/recharge_thumbnail.jpg', quality=92)
c.resize((540, 960)).save('../frames/th.jpg')
