// LISTX on <canvas>: port of vox/lib.py + vox/listx.py helpers to the 2D canvas API.
// Every helper takes the target context `c`, so a frame can be drawn into any canvas (main or loop buffer).
const W = 1080, H = 1920, FPS = 30;
const rgb = (a, al = 1) => `rgba(${a[0]},${a[1]},${a[2]},${al})`;
const INKL = [20, 20, 22], ACC = [34, 170, 110], ACC_SOFT = [200, 236, 214], MUTE = [140, 140, 140];
const LIGHT = [240, 240, 238], DARK_BG = [16, 17, 18], PAPERW = [252, 252, 250], OFFW = [250, 250, 248];
const FONT = { pop: '"pop"', type: '"type", "pop"', mono: '"mono", "pop"', anton: '"anton", "pop"' };

// ---------------- easing (same maths as lib.py) ----------------
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const eo = p => { p = clamp(p); return 1 - (1 - p) ** 3; };
const eio = p => { p = clamp(p); return 3 * p * p - 2 * p * p * p; };
const eback = (p, s = 1.9) => { p = clamp(p) - 1; return p * p * ((s + 1) * p + s) + 1; };
const prog = (t, t0, d) => clamp((t - t0) / d);
const popIn = (t, t0, d = 0.3) => t >= t0 ? eback(prog(t, t0, d), 1.7) : 0;

// ---------------- text: same box model as text_img (pad = 12% of size, asc + desc tall) ----------------
const MCTX = document.createElement('canvas').getContext('2d');
const _met = {};
function setFont(c, fn, size, track = 0) {
  c.font = `${size}px ${FONT[fn]}`; c.letterSpacing = `${track}px`; c.textBaseline = 'alphabetic'; c.textAlign = 'left';
}
function box(s, fn, size, track = 0) {
  const k = fn + size + '|' + track + '|' + s;
  if (_met[k]) return _met[k];
  setFont(MCTX, fn, size, track);
  const m = MCTX.measureText(s), pad = Math.floor(size * 0.12);
  const asc = Math.ceil(m.fontBoundingBoxAscent), desc = Math.ceil(m.fontBoundingBoxDescent);
  return (_met[k] = { w: m.width + 2 * pad, h: asc + desc + 2 * pad, tw: m.width, pad, asc });
}
const textW = (s, fn, size, track = 0) => box(s, fn, size, track).tw;
// top-left of the text box at (x, y), like c.alpha_composite(text_img(...), (x, y))
function text(c, s, fn, size, col, x, y, track = 0, alpha = 1) {
  const b = box(s, fn, size, track);
  setFont(c, fn, size, track); c.globalAlpha = alpha; c.fillStyle = rgb(col);
  c.fillText(s, x + b.pad, y + b.pad + b.asc); c.globalAlpha = 1;
  return b;
}

// place(): centre a w x h sprite at (cx, cy), scaled, rotated (degrees, counter-clockwise like PIL), faded
function place(c, w, h, cx, cy, scale, rot, alpha, draw) {
  if (alpha <= 0.003 || scale <= 0.01) return;
  c.save(); c.translate(cx, cy); if (rot) c.rotate(-rot * Math.PI / 180); c.scale(scale, scale);
  c.translate(-w / 2, -h / 2); c.globalAlpha = clamp(alpha); draw(c); c.restore();
}
function placeText(c, s, fn, size, col, cx, cy, scale = 1, rot = 0, alpha = 1, track = 0) {
  const b = box(s, fn, size, track);
  place(c, b.w, b.h, cx, cy, scale, rot, alpha, c => text(c, s, fn, size, col, 0, 0, track, c.globalAlpha));
}

// PIL-style rounded rectangle: outline drawn inside the box
function rr(c, x0, y0, x1, y1, r, fill, stroke, lw = 0) {
  const i = stroke ? lw / 2 : 0;
  c.beginPath(); c.roundRect(x0 + i, y0 + i, x1 - x0 - 2 * i, y1 - y0 - 2 * i, Math.max(0, r - i));
  if (fill) { c.fillStyle = rgb(fill); c.fill(); }
  if (stroke) { c.strokeStyle = rgb(stroke); c.lineWidth = lw; c.stroke(); }
}
function ell(c, x0, y0, x1, y1, fill, stroke, lw = 0) {
  const i = stroke ? lw / 2 : 0;
  c.beginPath(); c.ellipse((x0 + x1) / 2, (y0 + y1) / 2, Math.max(0.5, (x1 - x0) / 2 - i), Math.max(0.5, (y1 - y0) / 2 - i), 0, 0, 2 * Math.PI);
  if (fill) { c.fillStyle = rgb(fill); c.fill(); }
  if (stroke) { c.strokeStyle = rgb(stroke); c.lineWidth = lw; c.stroke(); }
}
function line(c, pts, col, lw, cap = 'round') {
  c.beginPath(); c.moveTo(pts[0], pts[1]);
  for (let k = 2; k < pts.length; k += 2) c.lineTo(pts[k], pts[k + 1]);
  c.strokeStyle = rgb(col); c.lineWidth = lw; c.lineCap = cap; c.lineJoin = 'round'; c.stroke();
}
function poly(c, pts, fill) {
  c.beginPath(); c.moveTo(pts[0], pts[1]);
  for (let k = 2; k < pts.length; k += 2) c.lineTo(pts[k], pts[k + 1]);
  c.closePath(); c.fillStyle = rgb(fill); c.fill();
}
function dashed(c, x0, y0, x1, y1, col, lw = 2, on = 7, gap = 7) {
  c.save(); c.setLineDash([on, gap]); line(c, [x0, y0, x1, y1], col, lw, 'butt'); c.restore();
}

// ---------------- timing (LX.timing / LX.word_times) ----------------
function timing(durs, lead = 0.15, tail = 0.25) {
  const starts = [], vo = []; let t = 0;
  durs.forEach((d, i) => { starts.push(t); vo.push(t + (i === 0 ? 0.1 : lead)); t = vo[i] + d + tail; });
  return { starts, vo, dur: t + 1.6 };
}
function wordTimes(script, durs, vo) {
  return script.map((s, i) => {
    let pos = 0;
    return s.split(' ').map(w => { const k = s.indexOf(w, pos); pos = k + w.length; return [w, vo[i] + durs[i] * (k / Math.max(1, s.length))]; });
  });
}

// ---------------- background + flash ----------------
let _darkBg = null;
function bg(c, dark) {
  if (!dark) { c.fillStyle = rgb(LIGHT); c.fillRect(0, 0, W, H); return; }
  if (!_darkBg) {
    _darkBg = document.createElement('canvas'); _darkBg.width = W; _darkBg.height = H;
    const g = _darkBg.getContext('2d'); g.fillStyle = rgb(DARK_BG); g.fillRect(0, 0, W, H);
    g.filter = 'blur(160px)'; ell(g, 80, 900, 1000, 1700, null); g.fillStyle = 'rgba(40,180,120,0.42)'; g.fill(); g.filter = 'none';
  }
  c.drawImage(_darkBg, 0, 0);
}
function flash(c, t, times, d = 0.12) {
  for (const tb of times) if (t - tb >= 0 && t - tb < d) { c.fillStyle = `rgba(255,255,255,${1 - (t - tb) / d})`; c.fillRect(0, 0, W, H); }
}

// ---------------- host avatar ----------------
const HOST = new Image();
function drawHost(c, t, words, big = true) {
  let kick = 0;
  for (const [, tw] of words) if (t - tw >= 0 && t - tw < 0.18) kick = Math.max(kick, Math.exp(-(t - tw) * 18));
  const bob = Math.sin(t * 2.2) * 6;
  if (big) {
    const h = 760, w = Math.floor(HOST.width * h / HOST.height), pad = 24;
    place(c, w + 2 * pad, h + 2 * pad, 300, 1560 + bob, 1 + 0.012 * kick, Math.sin(t * 1.3) * 1.2, 1, c => {
      c.save(); c.shadowColor = 'rgba(0,0,0,0.235)'; c.shadowBlur = 12; c.shadowOffsetX = 8; c.shadowOffsetY = 10;
      c.drawImage(HOST, pad, pad, w, h); c.restore();
    });
  } else {
    const w = 300, h = 330, s = w - 24;
    place(c, w, h, 230, 1560 + bob * 0.5, 1 + 0.015 * kick, -1.5, 1, c => {
      rr(c, 0, 0, w, h, 26, OFFW, [60, 60, 64], 4);
      c.save(); c.beginPath(); c.roundRect(12, 12, s, s, 18); c.clip();
      c.fillStyle = 'rgb(232,236,233)'; c.fillRect(12, 12, s, s);
      c.drawImage(HOST, 0, 0, HOST.width, HOST.width, 12, 12, s, s); c.restore();
      const b = box('● @MONEYINCLOUD', 'type', 20, 1);
      rr(c, w / 2 - b.w / 2 - 12, h - 44, w / 2 + b.w / 2 + 12, h - 12, 14, OFFW, INKL, 2);
      text(c, '● @MONEYINCLOUD', 'type', 20, INKL, w / 2 - b.w / 2, h - 42, 1);
    });
  }
}

// ---------------- type ----------------
function headline(c, t, words, accent, { x0 = 70, y0 = 215, size = 66, maxw = 940, col = INKL, hl = ACC_SOFT } = {}) {
  const lh = Math.floor(size * 1.12); let x = x0, y = y0; const lay = [];
  setFont(MCTX, 'pop', size);
  words.forEach(([w, tw], k) => {
    const ww = MCTX.measureText(w + ' ').width;
    if (x + ww - x0 > maxw) { x = x0; y += lh; }
    lay.push([k, w, tw, x, y]); x += ww;
  });
  for (const [k, w, tw, xx, yy] of lay) {
    if (t < tw - 0.05) continue;
    const a = clamp((t - tw + 0.05) / 0.12), dy = (1 - eo(a)) * 18;
    if (accent.has(k)) {
      const hp = eo(clamp((t - tw) / 0.25)), bw = Math.floor((textW(w, 'pop', size) + 8) * hp);
      if (bw > 1) { c.fillStyle = rgb(hl, 0.745); c.fillRect(xx - 4, yy + size * 0.6, bw, Math.floor(size * 0.5)); }
    }
    text(c, w, 'pop', size, accent.has(k) ? ACC : col, xx, yy + dy, 0, a);
  }
}

function hud(c, idx, slug, done, total, dark, word = 'SET UP') {
  const col = dark ? [150, 150, 150] : MUTE;
  text(c, `// ${String(idx).padStart(2, '0')} · ${slug}`, 'type', 30, col, 70, 150, 2);
  const n = box(`${done}/${total}`, 'type', 30, 2), r = box(word, 'type', 30, 2);
  text(c, word, 'type', 30, col, W - 70 - n.w - 20 - r.w, 150, 2);
  text(c, `${done}/${total}`, 'type', 30, ACC, W - 70 - n.w, 150, 2);
}

function itemTitle(c, t, t0, n, name, pill, icon, y = 600, dark = false) {
  if (t < t0) return;
  const p = eback(prog(t, t0, 0.35), 1.6), fg = dark ? [245, 245, 245] : INKL, cx = 110, r = 38 * p;
  ell(c, cx - r, y - r, cx + r, y + r, dark ? [245, 245, 245] : INKL);
  if (p > 0.6) placeText(c, String(n), 'pop', 46, dark ? INKL : [245, 245, 245], cx, y - 4);
  const ix = 190; rr(c, ix - 36, y - 36, ix + 36, y + 36, 14, OFFW, dark ? [80, 80, 84] : INKL, 3);
  if (icon) icon(c, ix, y + 2, 0.3);
  const nb = box(name, 'pop', 66);
  text(c, name, 'pop', 66, fg, 250 + (1 - eo(clamp(p))) * 30, y - nb.h / 2 - 10, 0, clamp(p));
  if (pill && t > t0 + 0.25) {
    const pb = box(pill, 'type', 24, 1), pw = pb.w + 36, px = 260, py = y + 58;
    rr(c, px, py, px + pw, py + 40, 20, dark ? [240, 240, 240] : INKL);
    text(c, pill, 'type', 24, dark ? INKL : [245, 245, 245], px + 18, py + 6, 1);
  }
}

function shelf(c, t, x0, y0, slots, filled, icons, { w = 520, dark = false, label = 'THE CHECKLIST' } = {}) {
  const ln = dark ? [210, 210, 210] : INKL, sw = (w - 40) / slots;
  for (let k = 0; k < slots; k++) {
    const bx0 = x0 + 20 + k * sw + 6, bx1 = bx0 + sw - 12, by0 = y0 - sw + 12, by1 = y0 - 4, ft = filled[k];
    if (ft != null && t > ft) {
      const q = eback(prog(t, ft, 0.3), 2), cx = (bx0 + bx1) / 2, cy = (by0 + by1) / 2, hw = (bx1 - bx0) / 2 * q, hh = (by1 - by0) / 2 * q;
      rr(c, cx - hw, cy - hh, cx + hw, cy + hh, 10, OFFW, ln, 3);
      c.fillStyle = rgb(ACC); c.fillRect(cx - hw, cy - hh, 2 * hw, 10 * q);
      if (q > 0.7 && icons[k]) icons[k](c, cx, cy + 4, 0.42 * Math.min(1, 4 / slots));
    } else {
      dashed(c, bx0, by0, bx1, by0, ln); dashed(c, bx0, by1, bx1, by1, ln);
      dashed(c, bx0, by0, bx0, by1, ln); dashed(c, bx1, by0, bx1, by1, ln);
      const pb = box('+', 'pop', 30); text(c, '+', 'pop', 30, ln, (bx0 + bx1) / 2 - pb.w / 2, (by0 + by1) / 2 - 22);
    }
    ell(c, bx0 - 8, by0 - 14, bx0 + 20, by0 + 14, dark ? [90, 90, 96] : INKL);
    const nb = box(String(k + 1), 'pop', 20); text(c, String(k + 1), 'pop', 20, OFFW, bx0 + 6 - nb.w / 2, by0 - 14);
  }
  rr(c, x0, y0, x0 + w, y0 + 16, 6, OFFW, ln, 3);
  c.fillStyle = rgb(ln); for (const lx of [x0 + 30, x0 + w - 30]) c.fillRect(lx - 5, y0 + 16, 10, 24);
  const lb = box(label, 'type', 20, 2), lw = lb.w + 40;
  c.fillStyle = rgb(INKL); c.fillRect(x0 + w / 2 - lw / 2, y0 + 26, lw, 30);
  text(c, label, 'type', 20, OFFW, x0 + w / 2 - lb.w / 2, y0 + 28, 2);
}

function sticker(c, t, t0, txt, x, y, rot = -6, size = 46) {
  if (t < t0) return;
  const b = box(txt, 'pop', size), w = b.w + 44, h = b.h + 22;
  place(c, w + 10, h + 10, x, y, 1.35 - 0.35 * eo(prog(t, t0, 0.22)), rot, clamp((t - t0) / 0.08), c => {
    const a = c.globalAlpha;
    rr(c, 8, 8, w + 8, h + 8, 16, INKL); rr(c, 0, 0, w, h, 16, PAPERW, INKL, 5);
    text(c, txt, 'pop', size, INKL, 22, 6, 0, a);
  });
}

// ---------------- line-art icons ----------------
const lw = s => Math.max(2, Math.floor(6 * s));
function icoPhone(c, cx, cy, s) {
  const w = 110 * s, h = 190 * s;
  rr(c, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, 18 * s, PAPERW, INKL, lw(s));
  rr(c, cx - w / 2 + 12 * s, cy - h / 2 + 22 * s, cx + w / 2 - 12 * s, cy + h / 2 - 30 * s, 6 * s, [232, 240, 235]);
  line(c, [cx - 20 * s, cy - h / 2 + 11 * s, cx + 20 * s, cy - h / 2 + 11 * s], INKL, Math.max(2, Math.floor(4 * s)));
  line(c, [cx - 32 * s, cy + 30 * s, cx - 10 * s, cy + 5 * s, cx + 8 * s, cy + 15 * s, cx + 32 * s, cy - 30 * s], ACC, lw(s));
  ell(c, cx - 10 * s, cy + h / 2 - 22 * s, cx + 10 * s, cy + h / 2 - 8 * s, null, INKL, Math.max(1, Math.floor(3 * s)));
}
function icoSwap(c, cx, cy, s) {
  const r = 46 * s;
  for (const [dx, sym, col] of [[-50, '₹', PAPERW], [50, '$', ACC]]) {
    const x = cx + dx * s; ell(c, x - r, cy - r, x + r, cy + r, col, INKL, lw(s));
    c.font = `${Math.floor(60 * s)}px "pop"`; c.letterSpacing = '0px'; c.textAlign = 'center'; c.textBaseline = 'middle';
    c.fillStyle = rgb(INKL); c.fillText(sym, x, cy + 2 * s); c.textAlign = 'left'; c.textBaseline = 'alphabetic';
  }
  line(c, [cx - 20 * s, cy - r - 14 * s, cx + 20 * s, cy - r - 14 * s], INKL, lw(s));
  poly(c, [cx + 22 * s, cy - r - 24 * s, cx + 36 * s, cy - r - 14 * s, cx + 22 * s, cy - r - 4 * s], INKL);
}
function icoTaxdoc(c, cx, cy, s) {
  const w = 130 * s, h = 170 * s;
  const p = [cx - w / 2, cy - h / 2, cx + w / 2 - 30 * s, cy - h / 2, cx + w / 2, cy - h / 2 + 30 * s, cx + w / 2, cy + h / 2, cx - w / 2, cy + h / 2];
  poly(c, p, PAPERW); line(c, [...p, p[0], p[1]], INKL, lw(s));
  for (let k = 0; k < 3; k++) line(c, [cx - w / 2 + 18 * s, cy - 30 * s + k * 26 * s, cx + w / 2 - 22 * s, cy - 30 * s + k * 26 * s], [170, 170, 170], Math.max(2, Math.floor(5 * s)));
  c.font = `${Math.floor(44 * s)}px "pop"`; c.letterSpacing = '0px'; c.textAlign = 'center'; c.textBaseline = 'middle';
  c.fillStyle = rgb(ACC); c.fillText('%', cx, cy + 58 * s); c.textAlign = 'left'; c.textBaseline = 'alphabetic';
}
function icoScale(c, cx, cy, s) {
  const W2 = 90 * s, t3 = Math.max(2, Math.floor(3 * s));
  line(c, [cx, cy - 70 * s, cx, cy + 70 * s], INKL, lw(s)); line(c, [cx - 40 * s, cy + 70 * s, cx + 40 * s, cy + 70 * s], INKL, lw(s));
  line(c, [cx - W2, cy - 50 * s, cx + W2, cy - 50 * s], INKL, lw(s));
  for (const [dx, col] of [[-W2, ACC], [W2, [230, 90, 80]]]) {
    const x = cx + dx; line(c, [x, cy - 50 * s, x - 30 * s, cy + 10 * s], INKL, t3); line(c, [x, cy - 50 * s, x + 30 * s, cy + 10 * s], INKL, t3);
    c.beginPath(); c.ellipse(x, cy + 12 * s, 36 * s - lw(s) / 2, 22 * s - lw(s) / 2, 0, 0, Math.PI); c.closePath();
    c.fillStyle = rgb(col); c.fill(); c.strokeStyle = rgb(INKL); c.lineWidth = lw(s); c.stroke();
  }
}
function icoGrid10(c, cx, cy, s) {
  const cs = 34 * s;
  for (let k = 0; k < 10; k++) {
    const r = Math.floor(k / 5), q = k % 5, x = cx - 2.5 * cs + q * cs, y = cy - cs + r * cs;
    rr(c, x + 3 * s, y + 3 * s, x + cs - 3 * s, y + cs - 3 * s, 6 * s, k % 3 === 0 ? ACC : PAPERW, INKL, Math.max(2, Math.floor(4 * s)));
  }
}

// ---------------- boot: fonts + host image, then the reel module sets window.drawFrame ----------------
async function loadAssets(root) {
  const faces = [new FontFace('pop', `url(${root}fonts/Poppins-Bold.ttf)`), new FontFace('type', `url(${root}fonts/special-elite-latin-400-normal.woff)`),
    new FontFace('anton', `url(${root}fonts/anton-latin-400-normal.woff)`),
    new FontFace('mono', `url(${root}fonts/ibm-plex-mono-latin-500-normal.woff2)`)];
  for (const f of faces) document.fonts.add(await f.load());
  HOST.src = root + 'host/host.png'; await HOST.decode();
}
const getJSON = u => fetch(u).then(r => r.json());
