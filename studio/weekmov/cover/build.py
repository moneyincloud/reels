import json
F='/home/claude/reels/motion/weekmov/assets/fonts/'
for m in ('gain','loss'):
    D=json.load(open(f'/home/claude/reels/motion/weekmov/build/{m}.json'))
    g=m=='gain'; col='#1E8E4E' if g else '#D93A2B'; word='GAINERS' if g else 'LOSERS'
    tops=[(gr['label'].capitalize().replace('Midcap','Mid cap').replace('Smallcap','Small cap'), gr['rows'][0]) for gr in D['groups']]
    def fmt(p): return ('+' if p>0 else '−')+f"{abs(p):.1f}%"
    rows=''.join(f'<div class="r"><span class="l">{l}</span><span class="n">{r["name"]}</span><span class="p">{fmt(r["pct"])}</span></div>' for l,r in tops)
    for kind in ('cover','story'):
        extra = '<div class="tag">NEW REEL 👆 tap to watch</div>' if kind=='story' else ''
        html=f'''<html><head><style>
@font-face{{font-family:A;src:url({F}anton-latin-400-normal.woff)}}
@font-face{{font-family:C;src:url({F}Caveat-700-latin.woff2)}}
@font-face{{font-family:P;src:url({F}Poppins-Bold.ttf)}}
body{{margin:0;width:1080px;height:1920px;background:#FBF8F0;background-image:linear-gradient(#e9e4d6 1px,transparent 1px),linear-gradient(90deg,#e9e4d6 1px,transparent 1px);background-size:40px 40px;font-family:P;color:#1a1a1a;position:relative;overflow:hidden}}
.safe{{position:absolute;left:90px;right:90px;top:300px;height:1320px;display:flex;flex-direction:column;align-items:center}}
.pill{{background:#1a1a1a;color:#fff;font-family:A;font-size:44px;letter-spacing:2px;padding:10px 34px;border-radius:40px}}
.t1{{font-family:A;font-size:190px;line-height:1;margin-top:40px;color:{col}}}
.t2{{font-family:A;font-size:96px;line-height:1.05;text-align:center}}
.t3{{font-family:C;font-size:72px;margin-top:10px}}
.box{{margin-top:50px;width:100%;border:6px solid #1a1a1a;border-radius:24px;background:#fff;box-shadow:12px 12px 0 #1a1a1a;padding:16px 30px;box-sizing:border-box}}
.r{{display:flex;align-items:center;padding:20px 0;border-bottom:3px dashed #ccc}} .r:last-child{{border:0}}
.l{{width:200px;font-size:30px;color:#777}} .n{{flex:1;font-size:42px}} .p{{font-family:A;font-size:66px;color:{col}}}
.foot{{position:absolute;bottom:0;font-size:26px;color:#666}}
.h{{position:absolute;left:40px;top:150px;font-size:34px;color:#555}}
.tag{{position:absolute;bottom:170px;left:0;right:0;text-align:center;font-family:A;font-size:70px;color:{col}}}
</style></head><body><div class="h">@moneyincloud</div><div class="safe">
<div class="pill">9–13 NOV 2026</div><div class="t1">TOP 10</div><div class="t2">{word} THIS WEEK</div>
<div class="t3">large · mid · small caps</div><div class="box">{rows}</div>
<div class="foot">Data: INDmoney · Not a buy/sell call · Education only</div></div>{extra}</body></html>'''
        open(f'{m}_{kind}.html','w').write(html)
