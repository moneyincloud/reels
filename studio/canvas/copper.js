// copper on <canvas>: Tamil reel — why Hindustan Copper rose (Q2 FY27 profit +182%, copper prices). Same pro look as giants.js.
const BG = [9, 11, 16], WHITE = [244, 245, 247], DIM = [130, 138, 152], RED = [255, 77, 77], GREEN = [32, 214, 138], GOLD = [255, 196, 64], PANEL = [20, 24, 32], LINE = [44, 50, 62];

let SCRIPT, DURS, STARTS, VO, DUR, CL, KICKS, SHAKES;
const at = (i, ph, off = 0) => { const k = SCRIPT[i].indexOf(ph); if (k < 0) throw new Error(ph); return VO[i] + DURS[i] * k / SCRIPT[i].length + off; };
const segAt = t => { let i = 0; STARTS.forEach((s, k) => { if (t >= s) i = k; }); return i; };
const val = k => 100000 * CL[k][CL[k].length - 1] / CL[k][0];
const pct = k => (CL[k][CL[k].length - 1] / CL[k][0] - 1) * 100;
const inr = v => '₹' + Math.round(v).toLocaleString('en-IN');

// ---------------- look: grain + vignette + background ----------------
let GRAIN = [], VIG;
function makeLook() {
  for (let g = 0; g < 4; g++) {
    const cv = document.createElement('canvas'); cv.width = 540; cv.height = 960; const x = cv.getContext('2d'), im = x.createImageData(540, 960);
    for (let p = 0; p < im.data.length; p += 4) { const v = Math.random() * 255; im.data[p] = im.data[p + 1] = im.data[p + 2] = v; im.data[p + 3] = 255; }
    x.putImageData(im, 0, 0); GRAIN.push(cv);
  }
  VIG = document.createElement('canvas'); VIG.width = W; VIG.height = H; const v = VIG.getContext('2d');
  const gr = v.createRadialGradient(W / 2, H * 0.45, H * 0.25, W / 2, H * 0.45, H * 0.75);
  gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(1, 'rgba(0,0,0,0.72)'); v.fillStyle = gr; v.fillRect(0, 0, W, H);
}
function background(c, t, tint) {
  c.fillStyle = rgb(BG); c.fillRect(0, 0, W, H);
  const g = c.createRadialGradient(W * (0.3 + 0.1 * Math.sin(t * 0.3)), H * 0.35, 0, W * 0.3, H * 0.35, 900);
  g.addColorStop(0, rgb(tint, 0.16)); g.addColorStop(1, rgb(tint, 0)); c.fillStyle = g; c.fillRect(0, 0, W, H);
  c.strokeStyle = rgb(LINE, 0.35); c.lineWidth = 1;
  for (let y = 160; y < H; y += 120) { c.beginPath(); c.moveTo(0, y); c.lineTo(W, y); c.stroke(); }
}
function finish(c, t) {
  c.drawImage(VIG, 0, 0);
  c.save(); c.globalAlpha = 0.07; c.globalCompositeOperation = 'overlay'; c.drawImage(GRAIN[Math.floor(t * 24) % 4], 0, 0, W, H); c.restore();
}

// ---------------- type helpers ----------------
function slamText(c, t, t0, s, fn, size, col, cx, cy, { rot = 0, glow = 0, rgbsplit = 0 } = {}) {
  if (t < t0) return;
  const p = prog(t, t0, 0.18), sc = 1.6 - 0.6 * eo(p), a = clamp(p * 4);
  const b = box(s, fn, size);
  place(c, b.w, b.h, cx, cy, sc, rot, a, c => {
    if (rgbsplit > 0) {
      c.save(); c.globalCompositeOperation = 'lighter';
      text(c, s, fn, size, [255, 40, 60], -rgbsplit, 0, 0, a * 0.8); text(c, s, fn, size, [40, 220, 255], rgbsplit, 0, 0, a * 0.8); c.restore();
    }
    if (glow) { c.save(); c.shadowColor = rgb(col, 0.8); c.shadowBlur = glow; text(c, s, fn, size, col, 0, 0, 0, a); c.restore(); }
    text(c, s, fn, size, col, 0, 0, 0, a);
  });
}
function chip(c, t, t0, s, x, y, fg, bg, size = 30) {
  if (t < t0) return;
  const fn = /[\u0B80-\u0BFF]/.test(s) ? 'ta' : 'mono', tr = fn === 'mono' ? 2 : 0;
  const b = box(s, fn, size, tr), w = b.w + 36, h = b.h + 12;
  place(c, w, h, x, y, popIn(t, t0, 0.25), 0, 1, c => { rr(c, 0, 0, w, h, h / 2, bg); text(c, s, fn, size, fg, 18, 6, tr, c.globalAlpha); });
}
function counter(c, t, t0, v0, v1, d, fn, size, col, cx, cy, fmt = inr, glow = 0) {
  if (t < t0) return;
  const v = v0 + (v1 - v0) * eio(prog(t, t0, d));
  if (glow) { c.save(); c.shadowColor = rgb(col, 0.7); c.shadowBlur = glow; placeText(c, fmt(v), fn, size, col, cx, cy); c.restore(); }
  else placeText(c, fmt(v), fn, size, col, cx, cy);
}

// real weekly closes, drawn up to fraction p; returns the tip
function chart(c, data, x0, y0, w, h, p, col, { fill = true, glow = 18, dot = true, lo, hi } = {}) {
  lo = lo ?? Math.min(...data); hi = hi ?? Math.max(...data);
  const X = k => x0 + w * k / (data.length - 1), Y = v => y0 + h - h * (v - lo) / (hi - lo);
  const n = (data.length - 1) * clamp(p), m = Math.floor(n), f = n - m;
  if (n <= 0) return [X(0), Y(data[0])];
  const pts = []; for (let k = 0; k <= m; k++) pts.push([X(k), Y(data[k])]);
  if (m < data.length - 1) pts.push([X(m + f), Y(data[m] + (data[m + 1] - data[m]) * f)]);
  if (fill) {
    const g = c.createLinearGradient(0, y0, 0, y0 + h); g.addColorStop(0, rgb(col, 0.28)); g.addColorStop(1, rgb(col, 0));
    c.beginPath(); c.moveTo(pts[0][0], y0 + h); pts.forEach(([x, y]) => c.lineTo(x, y)); c.lineTo(pts[pts.length - 1][0], y0 + h); c.closePath(); c.fillStyle = g; c.fill();
  }
  c.save(); c.shadowColor = rgb(col, 0.9); c.shadowBlur = glow;
  c.beginPath(); pts.forEach(([x, y], k) => k ? c.lineTo(x, y) : c.moveTo(x, y)); c.strokeStyle = rgb(col); c.lineWidth = 7; c.lineJoin = 'round'; c.lineCap = 'round'; c.stroke(); c.restore();
  const tip = pts[pts.length - 1];
  if (dot) { ell(c, tip[0] - 13, tip[1] - 13, tip[0] + 13, tip[1] + 13, WHITE); ell(c, tip[0] - 26, tip[1] - 26, tip[0] + 26, tip[1] + 26, null, col, 3); }
  return tip;
}

// ---------------- scenes (Tamil) ----------------
const CU = [226, 128, 64];
const fit = (s, fn, size, maxw = 960) => { while (box(s, fn, size).w > maxw && size > 24) size -= 2; return size; };
function taText(c, t, t0, s, size, col, cx, cy, o = {}) { slamText(c, t, t0, s, 'ta', fit(s, 'ta', size), col, cx, cy, o); }
function mine(c, cx, cy, s) {            // a simple open-pit copper mine: terraces + ore + truck
  for (let k = 0; k < 4; k++) { const w = (420 - k * 90) * s, y = cy - 40 * s + k * 50 * s; rr(c, cx - w / 2, y, cx + w / 2, y + 40 * s, 10 * s, [70 + k * 18, 52 + k * 10, 40], LINE, 2); }
  for (let k = 0; k < 6; k++) ell(c, cx - 120 * s + k * 48 * s - 14 * s, cy + 160 * s, cx - 120 * s + k * 48 * s + 14 * s, cy + 188 * s, CU);
  rr(c, cx + 140 * s, cy - 110 * s, cx + 260 * s, cy - 50 * s, 8 * s, GOLD); ell(c, cx + 150 * s, cy - 60 * s, cx + 180 * s, cy - 30 * s, WHITE); ell(c, cx + 220 * s, cy - 60 * s, cx + 250 * s, cy - 30 * s, WHITE);
}
function coil(c, cx, cy, s, t) {          // copper wire coil
  for (let k = 0; k < 9; k++) { c.beginPath(); c.ellipse(cx - 160 * s + k * 40 * s, cy, 40 * s, 120 * s, 0, 0, Math.PI * 2); c.strokeStyle = rgb(CU, 0.9); c.lineWidth = 14 * s; c.stroke(); }
  c.save(); c.shadowColor = rgb(CU, 0.9); c.shadowBlur = 40; line(c, [cx + 180 * s, cy, cx + 360 * s, cy - 40 * s + 20 * Math.sin(t * 3)], CU, 14 * s); c.restore();
}
function s0(c, t) {
  slamText(c, t, VO[0] + 0.1, 'HINDUSTAN COPPER', 'anton', 120, WHITE, 540, 420);
  chip(c, t, at(0, 'ஏறிருக்கு'), 'இன்று +3.8% · 12 NOV', 540, 560, BG, GREEN, 36);
  const tp = at(0, 'profit');
  if (t > tp) {
    text(c, 'PROFIT', 'anton', 90, DIM, 540 - box('PROFIT', 'anton', 90).w / 2, 680);
    const jit = t - tp < 0.35 ? 18 * (1 - (t - tp) / 0.35) : 0;
    slamText(c, t, tp + 0.2, '+182%', 'anton', 300, GREEN, 540, 980, { glow: 50, rgbsplit: jit });
    taText(c, t, at(0, 'மூணு'), 'கிட்டத்தட்ட 3 மடங்கு!', 70, GOLD, 540, 1200);
  }
  taText(c, t, at(0, 'ஏன்'), 'ஏன் தெரியுமா?', 110, WHITE, 540, 1400, { rot: -2 });
}
function s1(c, t) {
  slamText(c, t, VO[1], 'HINDUSTAN', 'anton', 150, CU, 540, 430);
  slamText(c, t, VO[1] + 0.15, 'COPPER LTD', 'anton', 150, WHITE, 540, 590);
  if (t > at(1, 'சுரங்கம்', -0.3)) place(c, 600, 460, 540, 1000, popIn(t, at(1, 'சுரங்கம்', -0.3), 0.35), 0, 1, c => mine(c, 300, 230, 1));
  chip(c, t, at(1, 'சுரங்கம்'), 'COPPER சுரங்கம்', 330, 1360, BG, CU, 36);
  chip(c, t, at(1, 'அரசு'), 'அரசு நிறுவனம்', 760, 1360, BG, WHITE, 36);
}
function s2(c, t) {
  chip(c, t, VO[2], 'Q2 FY27 RESULT · 11 NOV 2026', 540, 400, BG, GOLD, 32);
  bar(c, t, at(2, 'Revenue'), 'REVENUE', 64, 190, GREEN, 640, '₹1,175 கோடி');
  bar(c, t, at(2, 'Profit'), 'PROFIT', 182, 190, GREEN, 1020, '₹518 கோடி');
}
function s3(c, t) {
  taText(c, t, VO[3], 'company magic மட்டும் இல்ல...', 64, DIM, 540, 760);
  taText(c, t, at(3, 'உண்மையான'), 'உண்மையான காரணம்?', 110, CU, 540, 1000, { glow: 40 });
  placeText(c, '?', 'anton', 200, WHITE, 540 + 20 * Math.sin(t * 5), 1250);
}
function s4(c, t) {
  slamText(c, t, VO[4], 'COPPER விலை', 'tanton', 140, CU, 540, 420, { glow: 40 });
  if (t > VO[4] + 0.3) coil(c, 470, 820, 1, t);
  chip(c, t, at(4, 'record'), 'RECORD HIGH · SEP 2026', 540, 1120, BG, GOLD, 40);
  taText(c, t, at(4, 'உலகத்துல'), 'உலக சந்தையில்', 60, WHITE, 540, 1260);
}
function reason(c, t, t0, n, title, sub, y, col) {
  if (t < t0) return;
  const q = eo(prog(t, t0, 0.3)); c.save(); c.translate((1 - q) * 300, 0); c.globalAlpha = q;
  rr(c, 60, y, 1020, y + 300, 30, PANEL, LINE, 2);
  ell(c, 100, y + 40, 200, y + 140, col); placeText(c, String(n), 'anton', 70, BG, 150, y + 90);
  text(c, title, 'ta', fit(title, 'ta', 58, 760), WHITE, 230, y + 40); text(c, sub, 'tanton', 48, col, 230, y + 160);
  c.restore();
}
function s5(c, t) {
  taText(c, t, VO[5], 'ஏன்?', 140, WHITE, 540, 400);
  reason(c, t, at(5, 'ஒண்ணு'), 1, 'சுரங்கங்களில் பிரச்சனை', 'SUPPLY ↓', 560, RED);
  reason(c, t, at(5, 'ரெண்டு'), 2, 'AI · EV · SOLAR', 'DEMAND ↑', 940, GREEN);
  if (t > at(5, 'wire')) chip(c, t, at(5, 'wire'), 'எல்லாத்துக்கும் COPPER WIRE', 540, 1340, BG, CU, 34);
}
function s6(c, t) {
  slamText(c, t, VO[6], 'COPPER ↑', 'anton', 170, CU, 540, 600, { glow: 30 });
  if (t > at(6, 'சுரங்கம்')) { const q = eo(prog(t, at(6, 'சுரங்கம்'), 0.4)); poly(c, [490, 760, 590, 760, 540, 760 + 120 * q], WHITE); }
  taText(c, t, at(6, 'லாபம்'), 'சுரங்க லாபம் ↑', 110, GREEN, 540, 1020, { glow: 40 });
  chip(c, t, at(6, 'result'), 'PROFIT +182% இங்கிருந்து தான்', 540, 1240, BG, GOLD, 34);
}
function s7(c, t) {
  const t0 = VO[7];
  taText(c, t, t0, 'ஆனா கவனம்!', 100, GOLD, 540, 400);
  const tip = chart(c, CL, 80, 560, 920, 560, prog(t, at(7, 'ஜனவரில', -0.2), 2.2), CU, { glow: 20 });
  if (t > at(7, 'எழுநூத்து')) chip(c, t, at(7, 'எழுநூத்து'), '52W HIGH ₹760 · JAN', 300, 600, BG, WHITE, 30);
  if (t > at(7, 'இப்போ')) chip(c, t, at(7, 'இப்போ'), 'இப்போ ₹453', Math.min(tip[0], 860), tip[1] - 90, BG, GOLD, 32);
  if (t > at(7, 'நாப்பது')) slamText(c, t, at(7, 'நாப்பது'), '−40%', 'anton', 200, RED, 540, 1260, { glow: 30 });
  if (t > at(7, 'இறங்குனா')) chip(c, t, at(7, 'இறங்குனா'), 'COPPER ↓ = லாபம் ↓', 540, 1450, WHITE, RED, 40);
}
function s8(c, t) {
  const t0 = VO[8] - 0.1, q = eo(prog(t, t0, 0.4));
  c.save(); c.globalAlpha = q;
  rr(c, 50, 340, 1030, 1360, 34, PANEL, LINE, 2);
  text(c, 'HINDUSTAN COPPER', 'anton', 70, CU, 90, 370);
  text(c, 'சுருக்கமா · 12 Nov 2026', 'ta', 34, DIM, 92, 480);
  [['இன்று', '+3.8%', GREEN], ['Revenue (Q2)', '+64%', GREEN], ['Profit (Q2)', '+182%', GREEN], ['காரணம்', 'COPPER விலை', CU], ['52W high-ல இருந்து', '−40%', RED]].forEach(([a, b, col], k) => {
    const y = 580 + k * 150; line(c, [90, y - 16, 990, y - 16], LINE, 2);
    text(c, a, 'ta', 46, WHITE, 90, y + 10); const w = box(b, 'tanton', 66).w; text(c, b, 'tanton', 66, col, 990 - w, y);
  });
  c.restore();
  const tf = at(8, 'அனுப்புங்க'); if (t > tf) chip(c, t, tf, 'FRIEND-க்கு அனுப்புங்க →', 560, 1470, WHITE, [60, 66, 80], 36);
  const ts = at(8, 'Save'); if (t > ts) { const b = Math.abs(Math.sin((t - ts) * 5)) * 18 * Math.exp(-(t - ts) * 1.5); chip(c, t, ts, 'SAVE பண்ணுங்க', 540, 1590 - b, BG, GREEN, 40); }
}
// bars use Tamil-safe font for the note chip
function bar(c, t, t0, label, v, maxv, col, y, note) {
  if (t < t0) return;
  const q = eio(prog(t, t0, 1.0)), w = 900 * Math.min(1, v / maxv) * q;
  text(c, label, 'mono', 34, DIM, 90, y - 70, 3);
  rr(c, 90, y, 990, y + 130, 24, PANEL, LINE, 2); if (w > 4) { c.save(); c.shadowColor = rgb(col, 0.8); c.shadowBlur = 30; rr(c, 90, y, 90 + w, y + 130, 24, col); c.restore(); }
  counter(c, t, t0, 0, v, 1.0, 'anton', 100, WHITE, 300, y + 65, x => '+' + Math.round(x) + '%');
  if (note && t > t0 + 1.0) chip(c, t, t0 + 1.0, note, 780, y + 65, BG, GOLD, 28);
}
const SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8];
const TINT = [GREEN, CU, GREEN, CU, CU, CU, GREEN, RED, GOLD];
// ---------------- camera + compositing ----------------
let STAGE;
function camera(t, i) {
  let z = 1 + 0.035 * prog(t, STARTS[i], (STARTS[i + 1] ?? DUR) - STARTS[i]), sx = 0, sy = 0;
  for (const k of KICKS) if (t >= k && t - k < 0.6) z += 0.07 * Math.exp(-(t - k) * 9);
  for (const k of SHAKES) if (t >= k && t - k < 0.4) { const a = 16 * Math.exp(-(t - k) * 12); sx += a * Math.sin(t * 91); sy += a * Math.cos(t * 77); }
  return { z, sx, sy };
}
function hud(c, t, i) {
  c.fillStyle = rgb(WHITE, 0.15); c.fillRect(0, 0, W, 8); c.fillStyle = rgb(CU); c.fillRect(0, 0, W * t / DUR, 8);
  text(c, '@MONEYINCLOUD', 'mono', 26, DIM, 60, 120, 3);
  const r = 'NSE · HINDCOPPER'; text(c, r, 'mono', 26, DIM, W - 60 - box(r, 'mono', 26, 3).w, 120, 3);
  const foot = i === 8 ? 'Education only · not investment advice · not a buy/sell call' :
    i === 2 || i === 6 ? 'Hindustan Copper Q2 FY27 results · via INDmoney news, 11-12 Nov 2026' :
    i === 4 || i === 5 ? 'Copper record Sep 2026, −6% in a month: Trading Economics, Goldman Sachs' :
    i === 7 ? 'INDmoney weekly closes · 52-week high ₹760.05 · 12 Nov 2026, 10 AM' : 'INDmoney · price at 10:00 AM IST, 12 Nov 2026';
  text(c, foot, 'mono', 22, DIM, 60, 1840);
}
function frame(c, t) {
  const i = segAt(t), g = STAGE.getContext('2d');
  background(g, t, TINT[i]);
  const cam = camera(t, i);
  g.save(); g.translate(540 + cam.sx, 960 + cam.sy); g.scale(cam.z, cam.z); g.translate(-540, -960);
  SCENES[i](g, t); g.restore();
  const ws = STARTS[i], wp = i > 0 ? (t - ws) / 0.2 : 1;
  c.fillStyle = rgb(BG); c.fillRect(0, 0, W, H);
  if (wp < 1) { c.save(); c.filter = `blur(${Math.round(24 * (1 - wp))}px)`; c.drawImage(STAGE, (1 - eo(wp)) * 520, 0); c.restore(); }
  else c.drawImage(STAGE, 0, 0);
  for (const k of KICKS) if (t >= k && t - k < 0.08) { c.fillStyle = `rgba(255,255,255,${0.25 * (1 - (t - k) / 0.08)})`; c.fillRect(0, 0, W, H); }
  finish(c, t); hud(c, t, i);
}
function cover(c) {
  background(c, 0, CU);
  placeText(c, 'HINDUSTAN COPPER', 'anton', 120, WHITE, 540, 330);
  c.save(); c.shadowColor = rgb(GREEN, 0.8); c.shadowBlur = 60; placeText(c, 'PROFIT +182%', 'anton', 170, GREEN, 540, 620); c.restore();
  coil(c, 470, 950, 0.8, 0);
  placeText(c, 'ஏன் இவ்ளோ ஏறுச்சு?', 'ta', fit('ஏன் இவ்ளோ ஏறுச்சு?', 'ta', 100, 940), GOLD, 540, 1260, 1, -2);
  chip(c, 1, 0, 'Q2 RESULT · 11 NOV 2026', 540, 1430, BG, CU, 36);
  finish(c, 0); text(c, '@MONEYINCLOUD', 'mono', 30, DIM, 60, 1800, 3);
}
let LOOPBUF;
function drawFrame(c, t) {
  if (t < 0) return cover(c);
  frame(c, t);
  if (t > DUR - 0.5) { const g = LOOPBUF.getContext('2d'); frame(g, 1.5); c.globalAlpha = eio((t - (DUR - 0.5)) / 0.5); c.drawImage(LOOPBUF, 0, 0); c.globalAlpha = 1; }
}
async function init(root) {
  SCRIPT = await getJSON(root + 'copper/script.json'); DURS = await getJSON(root + 'copper/vo/durs.json');
  ({ starts: STARTS, vo: VO, dur: DUR } = await getJSON(root + 'copper/timing.json'));
  CL = (await getJSON(root + 'copper/closes.json')).closes;
  KICKS = [at(0, 'profit', 0.2), at(0, 'ஏன்'), at(2, 'Revenue'), at(2, 'Profit'), at(3, 'உண்மையான'), at(5, 'ஒண்ணு'), at(5, 'ரெண்டு'), at(6, 'லாபம்'), at(7, 'நாப்பது'), at(8, 'Save'), ...STARTS.slice(1)];
  SHAKES = [at(0, 'profit', 0.2), at(3, 'உண்மையான'), at(7, 'நாப்பது'), at(7, 'இறங்குனா')];
  makeLook();
  STAGE = document.createElement('canvas'); STAGE.width = W; STAGE.height = H;
  LOOPBUF = document.createElement('canvas'); LOOPBUF.width = W; LOOPBUF.height = H;
  return DUR;
}
window.REEL = { init, drawFrame };
