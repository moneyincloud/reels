"""Add an audience-gain FOLLOW card to a finished reel.
usage: python3 follow_overlay.py in.mp4 out.mp4 [line] [handle|-]
Card slides in at 3.0s (after the hook lands) for 3s, and again for the last 4s."""
import sys, subprocess, json, os
sys.path.insert(0, os.path.dirname(__file__))
import hook as HK
src, dst = sys.argv[1], sys.argv[2]
line = sys.argv[3] if len(sys.argv) > 3 else 'for daily money truths'
handle = sys.argv[4] if len(sys.argv) > 4 else '@moneyincloud'
if handle == '-': handle = None
png = os.path.splitext(dst)[0] + '_follow.png'
HK.follow_pill(line, handle).save(png)
dur = float(json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', src]))['format']['duration'])
a0, a1 = 3.0, 6.0; b0, b1 = dur - 4.0, dur
# x: slide in from the right over 0.35s, centred; sits over the top header strip so lesson content stays visible
x = (f"if(between(t,{a0},{a1}),(W-w)/2+max(0,({a0}+0.35-t))/0.35*(w+60),"
     f"(W-w)/2+max(0,({b0}+0.35-t))/0.35*(W))")
fc = (f"[1:v]format=rgba[s];[0:v][s]overlay=x='{x}':y=40:"
      f"enable='between(t,{a0},{a1})+between(t,{b0},{b1})'[v]")
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-loop', '1', '-i', png, '-filter_complex', fc,
                '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-b:v', '7000k', '-pix_fmt', 'yuv420p',
                '-c:a', 'copy', '-t', f'{dur:.3f}', '-movflags', '+faststart', dst], check=True)
os.remove(png)
print('ok', dst, round(dur, 2))
