"""Friday YouTube long-form: compile the week's reels into one 16:9 video (~10 min) with chapters.

Usage: python3 weekly_compile.py plan.json
plan = {
  "title": "THIS WEEK IN THE INDIAN MARKET",
  "dates": "23 – 30 OCT 2026",
  "voice": "am_michael",                       # intro/outro voice (Kokoro)
  "out": "../out/weekly_2026-10-30.mp4",
  "chapters": [ {"file": "/path/reel.mp4", "title": "Jio IPO: did you get shares?"}, ... ]
}
Writes the mp4 (kept under ~95 MB for GitHub hosting) and <out>.chapters.txt (YouTube chapter timestamps).
"""
import sys, os, json, subprocess, textwrap
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lib import *
from scenes import bgs
import saveshare as SS

FW, FH = 1920, 1080
VW = 608  # reel width inside the frame (1080x1920 scaled to height 1080)
TMP = os.path.join(HERE, '..', 'src', 'weekly'); os.makedirs(TMP, exist_ok=True)


def run(cmd): subprocess.run(cmd, check=True)


def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)


def paper():
    pbg, _ = bgs(); return pbg.resize((FW, int(FW * pbg.size[1] / pbg.size[0]))).crop((0, 0, FW, FH)).convert('RGBA')


def wrap_lines(s, width): return textwrap.wrap(s, width)


def side_panel(n, total, title, plan):
    c = paper(); d = ImageDraw.Draw(c)
    x0 = (FW - VW) // 2
    d.rectangle((x0 - 8, 0, x0 + VW + 8, FH), fill=INK)
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, INK, 1), (50, 50))
    place(c, text_img(f'PART {n}/{total}', 'anton', 110, RED), x0 // 2, 330)
    for k, ln in enumerate(wrap_lines(title.upper(), 16)[:4]):
        place(c, text_img(ln, 'anton', 64, INK), x0 // 2, 470 + k * 80)
    place(c, text_img(plan['title'], 'osw5', 30, (120, 116, 108)), x0 // 2, 900)
    rx = x0 + VW + (FW - x0 - VW) // 2
    place(c, SS.bookmark_icon(90), rx, 360, 1, -6)
    place(c, text_img('SAVE THIS', 'anton', 64, INK), rx, 470)
    pill = SS._card(420, 110, YEL); place(c, pill, rx, 640); place(c, text_img('SUBSCRIBE', 'anton', 62, INK), rx, 635)
    place(c, text_img('Education only.', 'type', 26, (120, 116, 108)), rx, 880)
    place(c, text_img('Not investment advice.', 'type', 26, (120, 116, 108)), rx, 915)
    return c


def title_card(plan, kind):
    c = paper(); d = ImageDraw.Draw(c)
    c.alpha_composite(text_img('@moneyincloud', 'type', 34, INK, 1), (60, 50))
    if kind == 'intro':
        place(c, text_img(plan['title'], 'anton', 120, INK), FW // 2, 220)
        place(c, text_img(plan['dates'], 'mark', 64, (30, 60, 120)), FW // 2, 340, 1, -2)
        for k, ch in enumerate(plan['chapters'][:8]):
            place(c, text_img(f"{k + 1}.  {ch['title']}", 'osw', 46, INK), FW // 2, 460 + k * 66)
    else:
        place(c, text_img('THAT WAS THE WEEK', 'anton', 130, INK), FW // 2, 330)
        place(c, SS._card(620, 140, YEL), FW // 2, 560); place(c, text_img('SUBSCRIBE FOR MORE', 'anton', 70, INK), FW // 2, 555)
        place(c, text_img('New Shorts daily · weekly recap every Friday', 'osw', 48, INK), FW // 2, 720)
        place(c, text_img('Sources on screen in each part. Education only. Not investment advice.', 'type', 30, (120, 116, 108)), FW // 2, 900)
    return c


def voice(text, name, v):
    d = os.path.join(TMP, name); os.makedirs(d + '/vo', exist_ok=True)
    json.dump([text], open(d + '/script.json', 'w'))
    run(['python3', os.path.join(HERE, '..', 'kokoro', 'vo.py'), d, v, '1.08'])
    return d + '/vo/0.wav'


def still_segment(img, wav, out, pad=1.5):
    p = out + '.png'; img.convert('RGB').save(p)
    D = dur(wav) + pad
    run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', f'{D:.2f}', '-i', p, '-i', wav, '-filter_complex',
         f'[1:a]aresample=48000,aformat=channel_layouts=mono,apad=whole_dur={D:.2f}[a]', '-map', '0:v', '-map', '[a]',
         '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-c:a', 'pcm_s16le', '-t', f'{D:.2f}', out])
    return D


def reel_segment(n, total, ch, plan, out):
    p = out + '.png'; side_panel(n, total, ch['title'], plan).convert('RGB').save(p)
    x0 = (FW - VW) // 2
    run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', p, '-ss', '0.5', '-i', ch['file'], '-filter_complex',
         f'[1:v]scale={VW}:{FH},fps=30[r];[0:v][r]overlay={x0}:0:shortest=1,format=yuv420p[v];[1:a]aresample=48000,aformat=channel_layouts=mono[a]',
         '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-c:a', 'pcm_s16le', out])
    return dur(out)


def thumb16x9(plan, out):
    import hook as HK
    c = HK.rays_bg('navy').resize((FW, int(FW * H / W))).crop((0, (int(FW * H / W) - FH) // 2, FW, (int(FW * H / W) - FH) // 2 + FH))
    place(c, HK.fit_text(plan['title'], 130, CREAM, maxw=1700), FW // 2, 260)
    place(c, HK.band(f"{len(plan['chapters'])} STORIES · {plan['dates']}", 100, maxw=1500), FW // 2, 470)
    place(c, HK.tag('WEEKLY RECAP', RED, CREAM, 110, -5), FW // 2, 740)
    c.convert('RGB').save(out, quality=92)


def main(plan):
    segs, t, chapters = [], 0.0, []
    n = len(plan['chapters'])
    intro_txt = f"This week in the Indian market. {n} stories, in about ten minutes. " + ' '.join(f"Part {k + 1}: {c['title']}." for k, c in enumerate(plan['chapters']))
    s = os.path.join(TMP, 'seg_intro.mkv'); D = still_segment(title_card(plan, 'intro'), voice(intro_txt, 'intro', plan.get('voice', 'am_michael')), s)
    segs.append(s); chapters.append((0, 'Intro')); t += D
    for k, ch in enumerate(plan['chapters']):
        s = os.path.join(TMP, f'seg_{k}.mkv'); D = reel_segment(k + 1, n, ch, plan, s)
        segs.append(s); chapters.append((t, ch['title'])); t += D
    s = os.path.join(TMP, 'seg_outro.mkv')
    D = still_segment(title_card(plan, 'outro'), voice("That was the week. Subscribe for daily Shorts and a full recap every Friday. Education only, not investment advice.", 'outro', plan.get('voice', 'am_michael')), s)
    segs.append(s); chapters.append((t, 'Wrap-up')); t += D
    lst = os.path.join(TMP, 'list.txt'); open(lst, 'w').write(''.join(f"file '{x}'\n" for x in segs))
    cat = os.path.join(TMP, 'cat.mkv'); run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', cat])
    vbit = int((93 * 8 * 1024) / t - 128)  # kbit/s so the file stays under ~95 MB
    vbit = max(600, min(vbit, 4000))
    out = plan['out']
    run(['ffmpeg', '-v', 'error', '-y', '-i', cat, '-c:v', 'libx264', '-preset', 'medium', '-b:v', f'{vbit}k', '-maxrate', f'{int(vbit * 1.4)}k',
         '-bufsize', f'{vbit * 2}k', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out])
    with open(out + '.chapters.txt', 'w') as f:
        for ts, title in chapters:
            m, s_ = divmod(int(ts), 60); f.write(f'{m}:{s_:02d} {title}\n')
    thumb16x9(plan, out.replace('.mp4', '_thumbnail.jpg'))
    print('weekly ok', out, round(t, 1), 's', round(os.path.getsize(out) / 1e6, 1), 'MB', vbit, 'kbps')


if __name__ == '__main__':
    main(json.load(open(sys.argv[1])))
