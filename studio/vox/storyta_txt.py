from PIL import Image
from lib import *
import os as _o
LANG = _o.environ.get('STORY_LANG', 'ta')
FONTS['ta'] = FD + 'noto-sans-tamil-tamil-800-normal.woff'


def text_ta(word, size, col):
    word = L(word)
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


EN = {
 'நாள் 92': 'DAY 92', 'கையில் ₹0': 'IN MY POCKET: ₹0', 'ஒரு லாரி டிரைவரின்\nகதை…': "A TRUCK DRIVER'S\nSTORY…",
 'லிஃப்ட் கேட்டேன்': 'I ASKED FOR A LIFT', 'எங்க போறீங்க?': 'Where are you going?', '"நீங்க போற இடத்துக்கே"': '"WHEREVER YOU\'RE GOING"',
 '15 வருஷமா\nவீட்டுக்கே போகல…': "Haven't been home\nin 15 years…", 'ஏன்?': 'WHY?', 'நம்ம வீட்டுலயும்\nநடந்தது தான்…': 'IT HAPPENS IN\nOUR HOMES TOO…',
 'அப்பாவின் சேமிப்பு': "DAD'S LIFE SAVINGS", '"இரட்டிப்பு!"': '"DOUBLE IT!"', 'போலி திட்டம்': 'FAKE SCHEME',
 '"உன்னால தான்!"': '"This is YOUR fault!"', '15 வயசுல வீட்ட விட்டு…': 'RAN AWAY AT 15…',
 'பணம் திரும்ப வரும்…\nஅம்மா காத்திருப்பாங்களா?': 'Money comes back…\nWill your mother wait?', 'லாரி வழி மாறுச்சு': 'THE TRUCK TURNED AROUND',
 '15 வருஷம்\nகழிச்சு': '15 YEARS\nLATER', 'போன பணம் திரும்ப வரும்.': 'LOST MONEY COMES BACK.', 'போன குடும்பம் வராது.': "A LOST FAMILY DOESN'T.",
 '"இரட்டிப்பு"\nதிட்டங்களை': '"DOUBLE YOUR MONEY"\nSCHEMES?', 'நம்பாதீங்க!': "DON'T TRUST THEM!",
 'இதை உங்க அப்பா அம்மாவுக்கு': 'SEND THIS TO', 'அனுப்புங்க': 'YOUR PARENTS', '@moneyincloud\nஃபாலோ பண்ணுங்க': 'FOLLOW\n@moneyincloud',
 'கற்பனை கதை · கல்வி நோக்கம் மட்டும்': 'Fictional story · Education only · Not investment advice', 'கற்பனை கதை': 'FICTIONAL STORY',
 'இரட்டிப்பு!': 'DOUBLE IT!', 'சொந்த ஊர்': 'HOME',
}


def L(s): return EN.get(s, s) if LANG == 'en' else s
