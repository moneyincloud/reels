// giants on <canvas>: "India's biggest names fell 20-30% in one year. This quiet stock made 145%."
// Pro edit, no host: dark cinematic grade, kinetic type, real weekly-close charts, punch-ins, shake, whips, grain.
const BG = [9, 11, 16], WHITE = [244, 245, 247], DIM = [130, 138, 152], RED = [255, 77, 77], GREEN = [32, 214, 138], GOLD = [255, 196, 64], PANEL = [20, 24, 32], LINE = [44, 50, 62];
const STOCKS = [['RELIANCE', 'Reliance', 'RELIANCE'], ['HDFC BANK', 'HDFC Bank', 'HDFCBANK'], ['INFOSYS', 'Infosys', 'INFY']];
const SRC = 'INDmoney weekly closes · 3 Nov 2025 → 30 Oct 2026';

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
  const b = box(s, 'mono', size, 2), w = b.w + 36, h = b.h + 12;
  place(c, w, h, x, y, popIn(t, t0, 0.25), 0, 1, c => { rr(c, 0, 0, w, h, h / 2, bg); text(c, s, 'mono', size, fg, 18, 6, 2, c.globalAlpha); });
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

// ---------------- scenes ----------------
function s0(c, t) {    // hook: three giants slam red, then the mystery +145%
  const tq = at(0, 'This quiet'), rows = [at(0, 'biggest'), at(0, 'fell'), at(0, 'twenty')];
  const up = eio(prog(t, tq - 0.1, 0.4));
  STOCKS.forEach(([nm, , key], k) => {
    const t0 = rows[k]; if (t < t0) return;
    const y = 560 + k * 230 - up * (330 + k * 40), sc = 1 - up * 0.42, a = 1 - up * 0.45;
    c.save(); c.globalAlpha = a; c.translate(540, y); c.scale(sc, sc); c.translate(-540, -y);
    rr(c, 60, y - 95, 1020, y + 95, 26, PANEL, LINE, 2);
    chart(c, CL[key], 500, y - 60, 220, 120, prog(t, t0, 0.5), RED, { glow: 8, dot: false });
    slamText(c, t, t0, nm, 'anton', 92, WHITE, 300, y);
    slamText(c, t, t0 + 0.1, Math.round(pct(key)) + '%', 'anton', 110, RED, 900, y);
    c.restore();
  });
  if (t > tq) {
    const tr = at(0, 'one hundred');
    if (t < tr) {
      const b = 'WHO?'; placeText(c, b, 'anton', 260, [70, 76, 90], 540, 1330, 1 + 0.03 * Math.sin(t * 20));
    } else {
      const jit = t - tr < 0.35 ? 22 * (1 - (t - tr) / 0.35) : 3;
      slamText(c, t, tr, '+145%', 'anton', 330, GREEN, 540, 1310, { glow: 50, rgbsplit: jit });
      chip(c, t, tr + 0.3, 'SAME 1 YEAR', 540, 1530, BG, GREEN);
    }
  }
}
function s1(c, t) {    // ₹1 lakh in each, 3 Nov
  const t0 = VO[1];
  counter(c, t, t0, 0, 100000, 0.9, 'anton', 210, WHITE, 540, 560);
  chip(c, t, at(1, 'each'), 'IN EACH OF 4 STOCKS', 540, 760, WHITE, [40, 46, 58]);
  for (let k = 0; k < 4; k++) {
    const tk = at(1, 'each', 0.15 + 0.12 * k); if (t < tk) continue;
    const x = 150 + k * 260, q = popIn(t, tk, 0.3);
    place(c, 230, 300, x, 1080, q, 0, 1, c => {
      rr(c, 0, 0, 230, 300, 22, PANEL, LINE, 3);
      placeText(c, k < 3 ? STOCKS[k][1] : '???', 'pop', 30, k < 3 ? WHITE : GREEN, 115, 60);
      placeText(c, '₹1L', 'anton', 90, WHITE, 115, 170); placeText(c, 'invested', 'mono', 22, DIM, 115, 250);
    });
  }
  chip(c, t, at(1, 'third'), '3 NOV 2025', 540, 1340, BG, GOLD, 34);
}
function s2(c, t) {    // three cards: chart down, value down
  const ph = ['Reliance', 'HDFC', 'Infosys'];
  STOCKS.forEach(([nm, , key], k) => {
    const t0 = at(2, ph[k], -0.15); if (t < t0) return;
    const y = 420 + k * 400, xo = (1 - eo(prog(t, t0, 0.25))) * 300;
    c.save(); c.translate(xo, 0);
    rr(c, 50, y, 1030, y + 360, 30, PANEL, LINE, 2);
    text(c, nm, 'anton', 64, WHITE, 90, y + 20);
    chart(c, CL[key], 90, y + 130, 520, 190, prog(t, t0, 1.1), RED, { glow: 12 });
    counter(c, t, t0, 100000, val(key), 1.1, 'anton', 104, WHITE, 830, y + 170);
    if (t > t0 + 1.0) { const b = box(Math.round(pct(key)) + '%', 'anton', 64); rr(c, 830 - b.w / 2 - 24, y + 250, 830 + b.w / 2 + 24, y + 330, 20, RED); placeText(c, Math.round(pct(key)) + '%', 'anton', 64, WHITE, 830, y + 290, popIn(t, t0 + 1.0, 0.25)); }
    c.restore();
  });
}
function s3(c, t) {    // rehook: the fourth one, full-screen green chart
  const t0 = VO[3], tt = at(3, 'turned');
  if (t < tt) {
    slamText(c, t, t0, 'THE 4TH ONE', 'anton', 170, WHITE, 540, 860);
    placeText(c, '...', 'anton', 160, GREEN, 540 + 30 * Math.sin(t * 6), 1060);
    return;
  }
  const p = prog(t, tt, 2.6);
  const tip = chart(c, CL.LAURUS, 70, 620, 940, 900, p, GREEN, { glow: 30 });
  counter(c, t, tt, 100000, val('LAURUS'), 2.6, 'anton', 190, GREEN, 540, 420, inr, 40);
  if (p > 0.98) { slamText(c, t, tt + 2.65, '+145%', 'anton', 120, WHITE, Math.min(tip[0] - 120, 860), tip[1] - 110); }
  text(c, 'NOV 25', 'mono', 26, DIM, 70, 1550); text(c, 'OCT 26', 'mono', 26, DIM, 900, 1550);
}
function s4(c, t) {    // name reveal
  const t0 = at(4, 'Laurus', -0.1), name = 'LAURUS LABS';
  for (let k = 0; k < name.length; k++) {
    const tk = t0 + k * 0.045; if (t < tk) continue;
    const xw = textW(name.slice(0, k), 'anton', 190) - textW(name, 'anton', 190) / 2;
    const q = eo(prog(t, tk, 0.2));
    text(c, name[k], 'anton', 190, GREEN, 540 + xw - box(name, 'anton', 190).pad, 520 + (1 - q) * 120, 0, q);
  }
  chip(c, t, at(4, 'medicine'), 'MEDICINE MAKER', 330, 920, BG, WHITE, 34);
  chip(c, t, at(4, 'Hyderabad'), 'HYDERABAD', 790, 920, BG, WHITE, 34);
  slamText(c, t, at(4, 'No ads'), 'NO ADS', 'anton', 150, WHITE, 540, 1150, { rot: -3 });
  if (t > at(4, 'No famous')) {
    slamText(c, t, at(4, 'No famous'), 'FAMOUS BRAND', 'anton', 130, DIM, 540, 1380, { rot: 2 });
    const q = eo(prog(t, at(4, 'brand'), 0.3)); if (q > 0) line(c, [140, 1395, 140 + 800 * q, 1365], RED, 14);
  }
}
function bar(c, t, t0, label, v, maxv, col, y, note) {
  if (t < t0) return;
  const q = eio(prog(t, t0, 1.0)), w = 900 * Math.min(1, v / maxv) * q;
  text(c, label, 'mono', 34, DIM, 90, y - 70, 3);
  rr(c, 90, y, 990, y + 130, 24, PANEL, LINE, 2); if (w > 4) { c.save(); c.shadowColor = rgb(col, 0.8); c.shadowBlur = 30; rr(c, 90, y, 90 + w, y + 130, 24, col); c.restore(); }
  counter(c, t, t0, 0, v, 1.0, 'anton', 100, WHITE, 300, y + 65, x => '+' + x.toFixed(x < 100 ? 1 : 0) + '%');
  if (note && t > t0 + 1.0) chip(c, t, t0 + 1.0, note, 780, y + 65, BG, GOLD, 28);
}
function s5(c, t) {
  slamText(c, t, VO[5], 'WHAT DID IT HAVE?', 'anton', 110, WHITE, 540, 470);
  bar(c, t, at(5, 'revenue'), 'REVENUE · LAST QUARTER', 33.5, 130, GREEN, 760);
  bar(c, t, at(5, 'profit'), 'PROFIT · LAST QUARTER', 126, 130, GREEN, 1120, 'MORE THAN 2×');
}
function s6(c, t) {    // meanwhile: the giants' problems
  const ti = at(6, 'Infosys'), th = at(6, 'HDFC');
  slamText(c, t, VO[6], 'MEANWHILE', 'anton', 110, DIM, 540, 400);
  if (t > ti) {
    const q = eo(prog(t, ti, 0.25)); c.save(); c.translate((1 - q) * -400, 0);
    rr(c, 50, 520, 1030, 960, 30, PANEL, LINE, 2); text(c, 'INFOSYS', 'anton', 70, WHITE, 90, 540);
    text(c, 'FY27 GROWTH TARGET', 'mono', 30, DIM, 90, 680, 2);
    counter(c, t, at(6, 'cut'), 5, 1.5, 0.8, 'anton', 150, RED, 760, 800, () => '1–2%');
    poly(c, [400, 760, 460, 860, 520, 760], RED); c.restore();
  }
  if (t > th) {
    const q = eo(prog(t, th, 0.25)); c.save(); c.translate((1 - q) * 400, 0);
    rr(c, 50, 1010, 1030, 1450, 30, PANEL, LINE, 2); text(c, 'HDFC BANK', 'anton', 70, WHITE, 90, 1030);
    chip(c, t, at(6, 'margins'), 'MARGINS ↓', 300, 1250, WHITE, RED, 40);
    chip(c, t, at(6, 'CEO'), 'NEW CEO', 760, 1250, BG, GOLD, 40);
    text(c, 'Q2 FY27 · profit +4.7%', 'mono', 28, DIM, 90, 1370); c.restore();
  }
}
function s7(c, t) {    // the answer
  const ta = at(7, 'The market'), tb = at(7, 'big names'), tg = at(7, 'growth'), tw = at(7, 'But after');
  if (t < tw) {
    slamText(c, t, ta, "THE MARKET DOESN'T PAY FOR", 'anton', 70, WHITE, 540, 560);
    if (t > tb) { slamText(c, t, tb, 'BIG NAMES', 'anton', 170, DIM, 540, 740); const q = eo(prog(t, tb + 0.5, 0.25)); if (q > 0) line(c, [130, 760, 130 + 820 * q, 720], RED, 16); }
    slamText(c, t, at(7, 'It pays'), 'IT PAYS FOR', 'anton', 70, WHITE, 540, 980);
    slamText(c, t, tg, 'GROWTH', 'anton', 260, GREEN, 540, 1190, { glow: 60, rgbsplit: t - tg < 0.3 ? 14 : 0 });
  } else {
    slamText(c, t, VO[7] + 0.2, 'GROWTH', 'anton', 150, GREEN, 540, 440, { glow: 40 });
    const q = popIn(t, tw, 0.3);
    place(c, 940, 640, 540, 980, q, 0, 1, c => {
      rr(c, 0, 0, 940, 640, 34, [40, 30, 10], GOLD, 5);
      poly(c, [470, 50, 540, 170, 400, 170], GOLD); placeText(c, '!', 'anton', 80, BG, 470, 125);
      placeText(c, 'BUT AFTER +145%', 'anton', 90, WHITE, 470, 260);
      placeText(c, 'experts disagree', 'pop', 44, GOLD, 470, 360);
      if (t > at(7, 'Kotak')) { rr(c, 170, 440, 770, 560, 24, RED); placeText(c, 'KOTAK: SELL', 'anton', 80, WHITE, 470, 500); }
    });
  }
}
function s8(c, t) {    // cheat sheet + CTA
  const t0 = VO[8] - 0.1, q = eo(prog(t, t0, 0.4));
  c.save(); c.globalAlpha = q;
  rr(c, 50, 360, 1030, 1340, 34, PANEL, LINE, 2);
  text(c, '₹1 LAKH · 1 YEAR', 'anton', 72, WHITE, 90, 390);
  text(c, '3 Nov 2025 → 30 Oct 2026', 'mono', 26, DIM, 92, 500);
  [...STOCKS.map(s => [s[1], s[2]]), ['Laurus Labs', 'LAURUS']].forEach(([nm, key], k) => {
    const y = 600 + k * 170, up = pct(key) > 0, col = up ? GREEN : RED;
    line(c, [90, y - 20, 990, y - 20], LINE, 2);
    text(c, nm, 'pop', 48, WHITE, 90, y + 10);
    text(c, inr(val(key)), 'anton', 70, col, 500, y + 4);
    const ps = (up ? '+' : '') + Math.round(pct(key)) + '%'; text(c, ps, 'anton', 56, col, 990 - box(ps, 'anton', 56).w, y + 14);
  });
  c.restore();
  const ts = at(8, 'Save');
  if (t > ts) { const b = Math.abs(Math.sin((t - ts) * 5)) * 18 * Math.exp(-(t - ts) * 1.5); chip(c, t, ts, 'SAVE THIS', 300, 1460 - b, BG, GREEN, 40); }
  const tf = at(8, 'Send');
  if (t > tf) chip(c, t, tf, 'SEND TO A FRIEND →', 640, 1580, WHITE, [60, 66, 80], 34);
  slamText(c, t, at(8, 'Big names'), 'BIG NAMES FELL. THE QUIET ONE GREW.', 'anton', 52, GOLD, 540, 1700);
}
const SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8];
const TINT = [RED, GOLD, RED, GREEN, GREEN, GREEN, RED, GREEN, GOLD];

// ---------------- camera + compositing ----------------
let STAGE;
function camera(t, i) {
  let z = 1 + 0.035 * prog(t, STARTS[i], (STARTS[i + 1] ?? DUR) - STARTS[i]), sx = 0, sy = 0;
  for (const k of KICKS) if (t >= k && t - k < 0.6) z += 0.07 * Math.exp(-(t - k) * 9);
  for (const k of SHAKES) if (t >= k && t - k < 0.4) { const a = 16 * Math.exp(-(t - k) * 12); sx += a * Math.sin(t * 91); sy += a * Math.cos(t * 77); }
  return { z, sx, sy };
}
function hud(c, t, i) {
  c.fillStyle = rgb(WHITE, 0.15); c.fillRect(0, 0, W, 8); c.fillStyle = rgb(GREEN); c.fillRect(0, 0, W * t / DUR, 8);
  text(c, '@MONEYINCLOUD', 'mono', 26, DIM, 60, 120, 3);
  const r = '1Y · NSE'; text(c, r, 'mono', 26, DIM, W - 60 - box(r, 'mono', 26, 3).w, 120, 3);
  const foot = i === 8 ? 'Education only · not investment advice · I may hold some of these stocks' :
    i === 5 ? 'Laurus Labs Q2 FY27 results · via INDmoney news, 29 Oct 2026' :
    i === 6 ? 'Infosys guidance 23 Oct · HDFC Bank Q2 17 Oct 2026 · via INDmoney news' :
    i === 7 ? 'Kotak rating: INDmoney news, 28 Oct 2026 · not a buy/sell call' : SRC;
  text(c, foot, 'mono', 22, DIM, 60, 1840);
}
function frame(c, t) {
  const i = segAt(t), g = STAGE.getContext('2d');
  background(g, t, TINT[i]);
  const cam = camera(t, i);
  g.save(); g.translate(540 + cam.sx, 960 + cam.sy); g.scale(cam.z, cam.z); g.translate(-540, -960);
  SCENES[i](g, t); g.restore();
  // whip transition into each new scene: slide + motion blur for 0.2 s
  const ws = STARTS[i], wp = i > 0 ? (t - ws) / 0.2 : 1;
  c.fillStyle = rgb(BG); c.fillRect(0, 0, W, H);
  if (wp < 1) { c.save(); c.filter = `blur(${Math.round(24 * (1 - wp))}px)`; c.drawImage(STAGE, (1 - eo(wp)) * 520, 0); c.restore(); }
  else c.drawImage(STAGE, 0, 0);
  for (const k of KICKS) if (t >= k && t - k < 0.08) { c.fillStyle = `rgba(255,255,255,${0.25 * (1 - (t - k) / 0.08)})`; c.fillRect(0, 0, W, H); }
  finish(c, t); hud(c, t, i);
}

function cover(c) {
  background(c, 0, RED);
  STOCKS.forEach(([nm, , key], k) => {
    const y = 330 + k * 170; rr(c, 80, y - 70, 1000, y + 70, 24, PANEL, LINE, 2);
    placeText(c, nm, 'anton', 80, WHITE, 340, y); placeText(c, Math.round(pct(key)) + '%', 'anton', 96, RED, 830, y);
  });
  c.save(); c.shadowColor = rgb(GREEN, 0.8); c.shadowBlur = 60; placeText(c, '+145%', 'anton', 340, GREEN, 540, 1050); c.restore();
  placeText(c, 'WHO MADE THIS?', 'anton', 120, WHITE, 540, 1300, 1, -2);
  chip(c, 1, 0, 'SAME 1 YEAR · REAL DATA', 540, 1470, BG, GOLD, 36);
  finish(c, 0); text(c, '@MONEYINCLOUD', 'mono', 30, DIM, 60, 1800, 3);
}

let LOOPBUF;
function drawFrame(c, t) {
  if (t < 0) return cover(c);
  frame(c, t);
  if (t > DUR - 0.5) { const g = LOOPBUF.getContext('2d'); frame(g, 0.9); c.globalAlpha = eio((t - (DUR - 0.5)) / 0.5); c.drawImage(LOOPBUF, 0, 0); c.globalAlpha = 1; }
}

async function init(root) {
  SCRIPT = await getJSON(root + 'giants/script.json'); DURS = await getJSON(root + 'giants/vo/durs.json');
  const tm = await getJSON(root + 'giants/timing.json'); ({ starts: STARTS, vo: VO, dur: DUR } = tm);
  CL = (await getJSON(root + 'giants/closes.json')).closes;
  KICKS = [at(0, 'biggest'), at(0, 'fell'), at(0, 'twenty'), at(0, 'one hundred'), at(2, 'Reliance'), at(2, 'HDFC'), at(2, 'Infosys'), at(3, 'turned'),
    at(4, 'Laurus'), at(4, 'No ads'), at(5, 'profit'), at(6, 'cut'), at(7, 'growth'), at(7, 'Kotak'), at(8, 'Save'), ...STARTS.slice(1)];
  SHAKES = [at(0, 'biggest'), at(0, 'fell'), at(0, 'twenty'), at(0, 'one hundred'), at(3, 'turned', 2.65), at(4, 'No ads'), at(6, 'cut'), at(7, 'growth'), at(7, 'Kotak')];
  makeLook();
  STAGE = document.createElement('canvas'); STAGE.width = W; STAGE.height = H;
  LOOPBUF = document.createElement('canvas'); LOOPBUF.width = W; LOOPBUF.height = H;
  return DUR;
}
window.REEL = { init, drawFrame };
