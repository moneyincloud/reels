"""Toon thumbnail: python3 thumb.py <land> <out.jpg> '<line1>' '<line2>' '<line3>' [tag]  (keywords in *stars* go yellow)"""
import sys, re, toon, subprocess, html as H
land, out, l1, l2, l3 = sys.argv[1:6]; tag = sys.argv[6] if len(sys.argv) > 6 else ''
F = '/home/claude/reels/motion/goldbill/assets/fonts/'
fmt = lambda s: re.sub(r'\*(.+?)\*', r'<span class="k">\1</span>', H.escape(s))
bg, lab = toon.backdrop(land)
rot = lambda svg, cid, side, d: svg.replace(f'id="{cid}-arm{side}" style="transform-origin:', f'id="{cid}-arm{side}" style="transform:rotate({d}deg);transform-origin:')
k = rot(rot(toon.kavya('kt'), 'kt', 'R', -150), 'kt', 'L', 150).replace('id="kt-mo" opacity="0"', 'id="kt-mo" opacity="1"').replace('id="kt-mc" ', 'opacity="0" id="kt-mc" ')
a = rot(toon.arjun('at'), 'at', 'R', -100)
page = f'''<html><head><meta charset='utf-8'><style>@font-face{{font-family:P;src:url({F}Poppins-Bold.ttf)}}@font-face{{font-family:O;src:url({F}oswald-latin-500-normal.woff)}}
body{{margin:0;width:1080px;height:1920px;position:relative;overflow:hidden;font-family:P}} .bgsvg{{position:absolute;inset:0;width:100%;height:100%}}
#sh{{position:absolute;left:0;right:0;top:220px;height:820px;background:linear-gradient(rgba(10,6,30,.55),rgba(10,6,30,.35) 80%,transparent)}} .c{{position:absolute;top:1010px;height:1000px;width:444px}} .c svg{{width:100%;height:100%;overflow:visible}}
.t{{position:absolute;left:30px;right:30px;text-align:center;color:#fff;-webkit-text-stroke:18px #140c06;paint-order:stroke fill;line-height:1.02;text-shadow:0 10px 0 rgba(0,0,0,.35)}}
.k{{color:#ffd23f}} .tag{{position:absolute;left:50%;transform:translateX(-50%) rotate(-3deg);top:930px;background:#e63946;color:#fff;font-size:60px;padding:8px 34px;border:6px solid #140c06;border-radius:18px;white-space:nowrap}}
.loc{{position:absolute;left:60px;top:1600px;font:34px O;letter-spacing:3px;color:#fff;background:rgba(20,14,40,.85);padding:8px 20px;border-radius:12px;border:3px solid #fff}}</style></head>
<body>{bg}<div id='sh'></div><div class="c" style="left:60px">{a}</div><div class="c" style="left:576px;transform:scaleX(-1)">{k}</div>
<div class="t" style="top:300px;font-size:104px">{fmt(l1)}</div><div class="t" style="top:520px;font-size:128px">{fmt(l2)}</div><div class="t" style="top:740px;font-size:84px">{fmt(l3)}</div>
{f'<div class="tag">{H.escape(tag)}</div>' if tag else ''}<div class="loc">{H.escape(lab)}</div></body></html>'''
open('/tmp/thumb.html', 'w').write(page)
B = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell'
subprocess.run([B, '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--window-size=1080,1920', '--screenshot=/tmp/thumb.png', 'file:///tmp/thumb.html'], capture_output=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '/tmp/thumb.png', '-q:v', '2', out]); print(out)
