import json
D = json.load(open('data.json'))
F = '/home/claude/reels/motion/nhit/assets/fonts/'
N = 9
def cr(v): return f"₹{v/100000:.2f} lakh cr" if v >= 100000 else f"₹{v:,.0f} cr"
def rows(lst, start, col):
    return ''.join(f'<div class="row"><span class="rk" style="background:{col}">{start+i}</span><span class="nm">{n}</span><span class="pr">₹{p:.2f}</span><span class="mc">{cr(m)}</span></div>' for i, (n, p, m) in enumerate(lst))
CSS = f'''@font-face{{font-family:A;src:url({F}anton-latin-400-normal.woff)}}
@font-face{{font-family:C;src:url({F}Caveat-700-latin.woff2)}}
@font-face{{font-family:P;src:url({F}Poppins-Bold.ttf)}}
@font-face{{font-family:O;src:url({F}oswald-latin-500-normal.woff)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:P;color:#1B1B1F;background:var(--bg)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(70,120,220,.10) 2px,transparent 2px),linear-gradient(90deg,rgba(70,120,220,.10) 2px,transparent 2px);background-size:54px 54px}}
.h{{position:absolute;left:60px;bottom:44px;font-family:O;font-size:30px;color:#555}}
.pg{{position:absolute;right:60px;bottom:44px;font-family:A;font-size:34px;color:#555}}
.src{{position:absolute;left:60px;right:200px;bottom:90px;font-family:O;font-size:24px;color:#555}}
.ttl{{position:absolute;left:60px;right:60px;top:110px;font-family:A;font-size:84px;line-height:1.02}}
.sub{{position:absolute;left:60px;right:60px;font-family:C;font-size:60px}}
.tag{{display:inline-block;padding:6px 26px;border:5px solid #1B1B1F;border-radius:14px;box-shadow:6px 6px 0 #1B1B1F;font-family:A;font-size:44px;color:#fff}}
.card{{position:absolute;left:60px;right:60px;background:#fff;border:6px solid #1B1B1F;border-radius:26px;box-shadow:12px 12px 0 #1B1B1F;padding:10px 30px}}
.row{{display:flex;align-items:center;gap:20px;padding:16px 0;border-bottom:3px dashed #ddd}} .row:last-child{{border:0}}
.rk{{width:62px;height:62px;border-radius:50%;border:4px solid #1B1B1F;color:#fff;font-family:A;font-size:34px;display:flex;align-items:center;justify-content:center;flex:none}}
.nm{{flex:1;font-size:38px}} .pr{{font-family:A;font-size:46px;width:180px;text-align:right}} .mc{{font-family:O;font-size:30px;color:#555;width:220px;text-align:right}}
.hd{{display:flex;gap:20px;padding:14px 0 6px;font-family:O;font-size:26px;color:#777}} .hd span:nth-child(1){{flex:1;padding-left:82px}} .hd span:nth-child(2){{width:180px;text-align:right}} .hd span:nth-child(3){{width:220px;text-align:right}}
.step{{display:flex;gap:26px;padding:24px 0;border-bottom:3px dashed #ddd}} .step:last-child{{border:0}}
.sn{{font-family:A;font-size:64px;width:70px;color:var(--ac)}} .st b{{display:block;font-family:A;font-weight:400;font-size:48px;line-height:1.1}} .st span{{font-size:32px;color:#444;line-height:1.3}}
'''
HD = '<div class="hd"><span>stock</span><span>price</span><span>market cap</span></div>'
SRC = f'<div class="src">Prices &amp; market cap: INDmoney (NSE), {D["asof"]} · Index: Nifty 100 / Midcap 150 / Smallcap 250 · Not a buy/sell call · Education only · I may hold some stocks named</div>'
S = []
S.append(('#FFF1B8', f'''<div class="ttl" style="top:150px;font-size:150px;color:#D93A2B">STOCKS<br>UNDER ₹50</div>
<div class="sub" style="top:500px;font-size:70px">in Nifty large, mid &amp; small caps</div>
<div style="position:absolute;left:60px;top:640px;display:flex;flex-direction:column;gap:26px">
<span class="tag" style="background:#2F6FE4">1 LARGE CAP</span><span class="tag" style="background:#C25E00">3 MID CAPS</span><span class="tag" style="background:#1E8E4E">11 SMALL CAPS</span></div>
<div style="position:absolute;right:70px;top:640px;width:420px;font-family:A;font-size:66px;line-height:1.05;text-align:right">+ the 7-step<br>filter to check<br>any of them 👉</div>''', False))
S.append(('#FFD6DE', f'''<div class="ttl">A ₹12 share is NOT<br>a cheap company</div>
<div class="card" style="top:400px;padding:40px">
<div style="font-family:O;font-size:34px;color:#555">Vodafone Idea · {D["asof"]}</div>
<div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:16px"><span style="font-size:44px">share price</span><span style="font-family:A;font-size:100px">₹12.26</span></div>
<div style="display:flex;justify-content:space-between;align-items:baseline;border-top:5px solid #1B1B1F;margin-top:10px;padding-top:10px"><span style="font-size:44px">company value</span><span style="font-family:A;font-size:84px;color:#D93A2B">₹1.36 lakh cr</span></div></div>
<div class="sub" style="top:900px;font-size:66px;line-height:1.1">Price alone tells you nothing.<br>Market cap, profit &amp; debt do.</div>''', True))
S.append(('#DDF0FF', f'''<div class="ttl">Large &amp; mid caps<br>under ₹50</div>
<div class="card" style="top:330px">{HD}<div style="font-family:A;font-size:34px;color:#2F6FE4;padding-top:10px">LARGE CAP · NIFTY 100</div>{rows(D["large"],1,"#2F6FE4")}
<div style="font-family:A;font-size:34px;color:#C25E00;padding-top:16px">MID CAP · NIFTY MIDCAP 150</div>{rows(D["mid"],2,"#C25E00")}</div>''', True))
S.append(('#D7F5E9', f'''<div class="ttl">Small caps under ₹50<br><span style="font-size:52px;color:#1E8E4E">Nifty Smallcap 250 · by market cap (1–6)</span></div>
<div class="card" style="top:330px">{HD}{rows(D["small"][:6],5,"#1E8E4E")}</div>''', True))
S.append(('#D7F5E9', f'''<div class="ttl">Small caps under ₹50<br><span style="font-size:52px;color:#1E8E4E">by market cap (7–11)</span></div>
<div class="card" style="top:330px">{HD}{rows(D["small"][6:],11,"#1E8E4E")}
<div style="font-family:O;font-size:30px;color:#1E8E4E;padding:14px 0 6px">✓ All 15 in normal (rolling) settlement today. Still check ASM/GSM before you buy.</div></div>''', True))
steps1 = [("Ignore the price, read market cap", "₹20 can be a ₹50,000 cr company; ₹200 can be ₹500 cr."), ("Profit for 3+ years?", "Rising net profit, not one-time gains. Losses = higher risk."), ("Debt under control", "Debt-to-equity below 1 (banks: check gross NPA instead)."), ("Promoter holding & pledge", "Stable or rising holding; pledge near 0%.")]
steps2 = [("Watch dilution", "Share count growing every year? Each raise shrinks your slice."), ("Liquidity & circuit band", "Lakhs of shares traded daily. A 5% band = extra caution."), ("Surveillance check", "NSE ASM/GSM lists & T2T settlement: avoid if listed.")]
def steplist(lst, start): return ''.join(f'<div class="step"><span class="sn">{start+i}</span><div class="st"><b>{t}</b><span>{d}</span></div></div>' for i, (t, d) in enumerate(lst))
S.append(('#E6E0FF', f'''<div class="ttl" style="--ac:#6C4BD8">The 7-step filter<br><span style="font-size:52px;color:#6C4BD8">steps 1–4</span></div>
<div class="card" style="top:330px;--ac:#6C4BD8">{steplist(steps1,1)}</div>''', True))
S.append(('#E6E0FF', f'''<div class="ttl">The 7-step filter<br><span style="font-size:52px;color:#6C4BD8">steps 5–7</span></div>
<div class="card" style="top:330px;--ac:#6C4BD8">{steplist(steps2,5)}</div>''', True))
S.append(('#FFE2D1', f'''<div class="ttl">Screenshot this 📸<br><span style="font-size:52px;color:#C25E00">a free-screener query (e.g. Screener.in)</span></div>
<div class="card" style="top:340px;background:#1B1B1F;color:#FFE45C;font-family:O;font-size:44px;line-height:1.6;padding:34px 40px">
Current price &lt; 50 AND<br>Market Capitalization &gt; 5000 AND<br>Net profit 3Years &gt; 0 AND<br>Debt to equity &lt; 1 AND<br>Pledged percentage &lt; 5 AND<br>Promoter holding &gt; 40</div>
<div class="sub" style="top:930px;font-size:52px;line-height:1.15">Then read the last 4 quarterly results<br>before you put in a single rupee.</div>''', True))
S.append(('#FFF1B8', f'''<div class="ttl" style="font-size:96px">Which one are you<br>researching? 👇</div>
<img src="/home/claude/reels/motion/nhit/assets/img/s0_008.png" style="position:absolute;left:40px;top:420px;width:400px"/>
<div style="position:absolute;left:470px;top:470px;display:flex;flex-direction:column;gap:30px">
<span class="tag" style="background:#1E8E4E;font-size:60px">COMMENT 50</span><span class="tag" style="background:#FFE45C;color:#1B1B1F;font-size:52px">💾 SAVE THIS</span><span class="tag" style="background:#2F6FE4;font-size:46px">SHARE with a friend</span></div>
<div class="sub" style="top:930px;font-size:46px;line-height:1.2">Low price ≠ low risk. Not a buy/sell call.<br>Education only, not investment advice.</div>''', True))
for i, (bg, body, src) in enumerate(S):
    open(f's{i+1}.html', 'w').write(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="--bg:{bg}"><div class="grid"></div>{body}{SRC if src else ""}<div class="h">@moneyincloud</div><div class="pg">{i+1}/{N}</div></body></html>')
print(len(S))
