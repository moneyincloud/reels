// Render a canvas reel with headless Chromium.
//   node render.mjs <slug> stills 1.5,6,12 out.png      -> contact sheet (270x480 per frame)
//   node render.mjs <slug> frame -1 cover.jpg            -> one full-size frame (t < 0 = the reel's cover)
//   node render.mjs <slug> video out.mp4 [audio.wav]    -> 1080x1920 30 fps mp4
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const [slug, mode, ...rest] = process.argv.slice(2);
const still = mode === 'stills' || mode === 'frame';
const [arg, out] = still ? rest : [null, ...rest];
const audio = still ? null : rest[1];
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.ttf': 'font/ttf', '.woff': 'font/woff', '.woff2': 'font/woff2' };

const server = http.createServer((req, res) => {
  const f = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(ROOT) || !fs.existsSync(f)) { res.writeHead(404).end(); return; }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' }).end(fs.readFileSync(f));
}).listen(0);
const port = server.address().port;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
page.on('pageerror', e => { console.error('page error:', e.message); process.exit(1); });
await page.goto(`http://localhost:${port}/canvas/index.html?reel=${slug}`);
const dur = await page.evaluate(() => window.READY);

const grab = (t, q) => page.evaluate(([t, q]) => { seek(t); return document.getElementById('c').toDataURL(q ? 'image/jpeg' : 'image/png', q || undefined); }, [t, q]);

if (mode === 'frame') {
  const url = await grab(Number(arg), out.endsWith('.jpg') ? 0.92 : 0);
  fs.writeFileSync(out, Buffer.from(url.split(',')[1], 'base64')); console.log('frame', out);
} else if (mode === 'stills') {
  const ts = arg.split(',').map(Number), cols = Math.min(8, ts.length);
  const urls = []; for (const t of ts) urls.push(await grab(t));
  const sheet = await page.evaluate(async ([urls, cols]) => {
    const s = document.createElement('canvas'); s.width = 270 * cols; s.height = 480 * Math.ceil(urls.length / cols);
    const g = s.getContext('2d');
    for (let k = 0; k < urls.length; k++) { const im = new Image(); im.src = urls[k]; await im.decode(); g.drawImage(im, (k % cols) * 270, Math.floor(k / cols) * 480, 270, 480); }
    return s.toDataURL('image/png');
  }, [urls, cols]);
  fs.writeFileSync(out, Buffer.from(sheet.split(',')[1], 'base64'));
  console.log('sheet', out);
} else {
  const n = Math.round(dur * 30), a0 = Date.now();
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-',
    ...(audio ? ['-i', audio, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '192k', '-shortest'] : []),
    '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = 0; f < n; f++) {
    const url = await grab(f / 30, 0.95);
    if (!ff.stdin.write(Buffer.from(url.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 300 === 0) console.log(`frame ${f}/${n}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  console.log(`RENDERED ${out} · ${n} frames in ${((Date.now() - a0) / 1000).toFixed(0)} s`);
}
await browser.close(); server.close();
