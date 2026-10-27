from PIL import Image
from lib import *
FONTS['ta'] = FD + 'noto-sans-tamil-tamil-800-normal.woff'


def text_ta(word, size, col):
    runs, cur, isT = [], '', None
    for ch in word:
        t_ = 0x0B80 <= ord(ch) <= 0x0BFF or ch in '‌‍'
        if isT is None or t_ == isT: cur += ch
        else: runs.append((cur, isT)); cur = ch
        isT = t_
    if cur: runs.append((cur, isT))
    ims = [text_img(r, 'ta' if tt else 'anton', size if tt else int(size * 1.05), col) for r, tt in runs]
    h = max(m.size[1] for m in ims); w = sum(m.size[0] for m in ims)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); x = 0
    for m in ims: im.alpha_composite(m, (x, h - m.size[1])); x += m.size[0]
    return im
