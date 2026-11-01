"""Render an HTML/CSS/canvas reel (window.seek(t)) frame by frame with Playwright into an mp4 part.
usage: python3 web_render.py <html> <out.mp4> <dur> <k> <K> [fps]"""
import sys, subprocess
from playwright.sync_api import sync_playwright
html, out, dur, k, K = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
fps = int(sys.argv[6]) if len(sys.argv) > 6 else 30
N = int(dur * fps); a = N * k // K; b = N * (k + 1) // K
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-',
                       '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', str(fps), out], stdin=subprocess.PIPE)
with sync_playwright() as p:
    br = p.chromium.launch(args=['--disable-gpu-vsync', '--force-color-profile=srgb'])
    pg = br.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
    pg.goto('file://' + html); pg.evaluate('window.ready')
    for f in range(a, b):
        pg.evaluate(f'Promise.resolve(window.seek({f / fps:.4f}))')
        ff.stdin.write(pg.screenshot(type='jpeg', quality=93))
    br.close()
ff.stdin.close(); ff.wait(); print('done', k)
