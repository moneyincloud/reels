// devops on <canvas>: "Your app broke at 9 PM and was fixed by 10" — DevOps in 5 steps, one real-time bug-fix story.
const RED = [225, 80, 70], LIGHTT = [240, 240, 240], CARD = [32, 34, 36], CARDLN = [80, 84, 88], TERM = [24, 26, 30], AMBER = [240, 170, 50];
const ACCENTS = [["nine PM,", "fixed by ten."], ["Plan and code."], ["pay button freezes.", "three line fix,", "GitHub."], ["Build."],
  ["GitHub Actions,", "Docker container,", "runs the same"], ["Test.", "saves your weekend."], ["automatic tests", "pipeline stops,", "never reaches"],
  ["Deploy."], ["Kubernetes", "Ten percent", "Zero downtime."], ["Monitor."], ["Prometheus and Grafana", "alert fires,", "rolls back", "Fixed."],
  ["on loop.", "DevOps.", "Save this,"]];
const DARK = new Set([3, 4, 7, 8]), NI = 5;
const NAMES = ['Plan & code', 'Build', 'Test', 'Deploy', 'Monitor'];
const PILLS = ['GIT · GITHUB', 'CI · GITHUB ACTIONS · DOCKER', 'AUTOMATED TESTS', 'CD · KUBERNETES ROLLOUT', 'PROMETHEUS · GRAFANA'];
const SLUGS = ['plan & code', 'build', 'test', 'deploy', 'monitor'];
const SRC = ['Example story · tools: Git (version control), GitHub (code hosting)',
  'Tools: GitHub Actions (continuous integration), Docker (containers)',
  'Tools: unit + integration tests run by the CI pipeline (e.g. Jest, pytest)',
  'Tools: Kubernetes rolling update / canary release',
  'Tools: Prometheus (metrics), Grafana (dashboards), kubectl rollout undo'];

// ---------------- icons ----------------
function icoCode(c, cx, cy, s) {
  rr(c, cx - 80 * s, cy - 65 * s, cx + 80 * s, cy + 65 * s, 16 * s, PAPERW, INKL, lw(s));
  line(c, [cx - 25 * s, cy - 30 * s, cx - 55 * s, cy, cx - 25 * s, cy + 30 * s], INKL, lw(s));
  line(c, [cx + 25 * s, cy - 30 * s, cx + 55 * s, cy, cx + 25 * s, cy + 30 * s], INKL, lw(s));
  line(c, [cx + 12 * s, cy - 38 * s, cx - 12 * s, cy + 38 * s], ACC, lw(s));
}
function gearPath(c, cx, cy, r, teeth, rot) {
  c.beginPath();
  for (let k = 0; k < teeth * 4; k++) {
    const a = rot + k * Math.PI / (teeth * 2), rr2 = (k % 4 < 2) ? r : r * 0.78;
    k ? c.lineTo(cx + rr2 * Math.cos(a), cy + rr2 * Math.sin(a)) : c.moveTo(cx + rr2 * Math.cos(a), cy + rr2 * Math.sin(a));
  }
  c.closePath();
}
function icoGear(c, cx, cy, s, rot = 0) {
  gearPath(c, cx, cy, 80 * s, 8, rot); c.fillStyle = rgb(PAPERW); c.fill(); c.strokeStyle = rgb(INKL); c.lineWidth = lw(s); c.lineJoin = 'round'; c.stroke();
  ell(c, cx - 28 * s, cy - 28 * s, cx + 28 * s, cy + 28 * s, ACC, INKL, lw(s));
}
function icoTest(c, cx, cy, s) {
  rr(c, cx - 70 * s, cy - 85 * s, cx + 70 * s, cy + 85 * s, 14 * s, PAPERW, INKL, lw(s));
  for (let k = 0; k < 3; k++) {
    const y = cy - 45 * s + k * 45 * s;
    rr(c, cx - 50 * s, y - 14 * s, cx - 22 * s, y + 14 * s, 5 * s, k < 2 ? ACC : PAPERW, INKL, Math.max(2, 3 * s));
    line(c, [cx - 8 * s, y, cx + 50 * s, y], [170, 170, 170], Math.max(2, 5 * s));
  }
}
function icoRocket(c, cx, cy, s) {
  c.beginPath(); c.moveTo(cx, cy - 95 * s); c.bezierCurveTo(cx + 45 * s, cy - 55 * s, cx + 40 * s, cy + 20 * s, cx + 28 * s, cy + 50 * s);
  c.lineTo(cx - 28 * s, cy + 50 * s); c.bezierCurveTo(cx - 40 * s, cy + 20 * s, cx - 45 * s, cy - 55 * s, cx, cy - 95 * s); c.closePath();
  c.fillStyle = rgb(PAPERW); c.fill(); c.strokeStyle = rgb(INKL); c.lineWidth = lw(s); c.stroke();
  ell(c, cx - 15 * s, cy - 35 * s, cx + 15 * s, cy - 5 * s, ACC, INKL, Math.max(2, 4 * s));
  poly(c, [cx - 28 * s, cy + 15 * s, cx - 55 * s, cy + 60 * s, cx - 25 * s, cy + 50 * s], INKL);
  poly(c, [cx + 28 * s, cy + 15 * s, cx + 55 * s, cy + 60 * s, cx + 25 * s, cy + 50 * s], INKL);
  poly(c, [cx - 16 * s, cy + 52 * s, cx, cy + 95 * s, cx + 16 * s, cy + 52 * s], AMBER);
}
function icoMonitor(c, cx, cy, s) {
  rr(c, cx - 90 * s, cy - 65 * s, cx + 90 * s, cy + 50 * s, 12 * s, PAPERW, INKL, lw(s));
  line(c, [cx - 70 * s, cy + 20 * s, cx - 35 * s, cy + 5 * s, cx - 5 * s, cy + 15 * s, cx + 25 * s, cy - 40 * s, cx + 70 * s, cy - 20 * s], ACC, lw(s));
  line(c, [cx, cy + 50 * s, cx, cy + 75 * s], INKL, lw(s)); line(c, [cx - 40 * s, cy + 78 * s, cx + 40 * s, cy + 78 * s], INKL, lw(s));
}
const ICONS = [icoCode, icoGear, icoTest, icoRocket, icoMonitor];

let SCRIPT, DURS, STARTS, VO, DUR, WORDS, ALLW, ACC_IDX, PAGES, SWITCH, FILL;

function accIdx(i) {
  const ws = WORDS[i].map(w => w[0]), out = new Set();
  for (const ph of ACCENTS[i]) {
    const p = ph.split(' ');
    for (let k = 0; k <= ws.length - p.length; k++) if (p.every((x, j) => ws[k + j] === x)) { for (let j = 0; j < p.length; j++) out.add(k + j); break; }
  }
  return out;
}
function pages(i) {
  const ws = WORDS[i], out = []; let st = 0;
  ws.forEach(([w], k) => { if (/[.?!]$/.test(w) && k < ws.length - 1 && k - st >= 3) { out.push([st, k + 1]); st = k + 1; } });
  out.push([st, ws.length]);
  const m = [];
  for (const [a, b] of out) { if (m.length && m[m.length - 1][1] - m[m.length - 1][0] <= 2) m[m.length - 1][1] = b; else m.push([a, b]); }
  return m;
}
const segAt = t => { let i = 0; STARTS.forEach((s, k) => { if (t >= s) i = k; }); return i; };
function at(i, phrase, off = 0) {
  const k = SCRIPT[i].indexOf(phrase); if (k < 0) throw new Error(phrase);
  return VO[i] + DURS[i] * (k / SCRIPT[i].length) + off;
}
function head(c, t, i, dark) {
  let pg = PAGES[i][0];
  for (const [a, b] of PAGES[i]) if (t >= WORDS[i][a][1] - 0.05) pg = [a, b];
  const [a, b] = pg, ws = WORDS[i].slice(a, b), n = ws.map(w => w[0]).join(' ').length;
  const acc = new Set([...ACC_IDX[i]].filter(k => k >= a && k < b).map(k => k - a));
  headline(c, t, ws, acc, { size: n < 40 ? 70 : n < 75 ? 62 : 56, col: dark ? LIGHTT : INKL, hl: dark ? [30, 80, 58] : ACC_SOFT });
}

// a sticker in a warning colour (red fill, white text)
function alarm(c, t, t0, txt, x, y, rot = -5, size = 40, fill = RED) {
  if (t < t0) return;
  const b = box(txt, 'pop', size), w = b.w + 44, h = b.h + 22;
  place(c, w + 10, h + 10, x, y, 1.35 - 0.35 * eo(prog(t, t0, 0.22)), rot, clamp((t - t0) / 0.08), c => {
    const a = c.globalAlpha; rr(c, 8, 8, w + 8, h + 8, 16, INKL); rr(c, 0, 0, w, h, 16, fill, INKL, 5);
    text(c, txt, 'pop', size, PAPERW, 22, 6, 0, a);
  });
}
function clock(c, t, cx, cy, s, label, col, scale = 1) {
  place(c, 520, 300, cx, cy, scale, 0, 1, c => {
    rr(c, 10, 10, 520, 300, 30, INKL); rr(c, 0, 0, 510, 290, 30, PAPERW, INKL, 6);
    placeText(c, label, 'pop', label.length > 7 ? 96 : 112, col, 265, 140);
    if (Math.floor(t * 2) % 2 === 0) { ell(c, 30, 30, 54, 54, col); }
  });
}

// ---------------- visuals ----------------
function vIntro(c, t) {
  const t0 = VO[0] + 0.1, tf = at(0, 'fixed');
  const p = popIn(t, t0, 0.4);
  if (t < tf) { if (p) clock(c, t, 640, 900, 1, '9:00 PM', RED, p); alarm(c, t, at(0, 'broke'), 'APP DOWN', 760, 1120, -6, 44); }
  else {
    const q = popIn(t, tf, 0.35); clock(c, t, 640, 900, 1, '10:00 PM', ACC, 0.85 + 0.15 * q);
    sticker(c, t, tf, 'FIXED IN 1 HOUR', 720, 1110, 5, 44);
  }
  sticker(c, t, at(0, 'five'), '5 DEVOPS STEPS', 740, 1290, -4, 38);
}
function phone(c, t, cx, cy, frozen) {
  place(c, 260, 440, cx, cy, 1, frozen ? Math.sin(t * 40) * 1.5 : 0, 1, c => {
    rr(c, 0, 0, 260, 440, 34, INKL); rr(c, 14, 40, 246, 400, 10, [232, 240, 235]);
    text(c, 'Checkout', 'pop', 30, INKL, 30, 60); text(c, 'Masala dosa x2', 'type', 20, MUTE, 32, 115); text(c, '₹249', 'pop', 44, INKL, 30, 150);
    rr(c, 30, 280, 230, 350, 18, frozen ? [170, 170, 170] : ACC);
    placeText(c, frozen ? 'PAY  …' : 'PAY ₹249', 'pop', 30, PAPERW, 130, 313);
  });
  if (frozen) alarm(c, t, -1, 'FROZEN', cx + 60, cy - 170, 8, 30);
}
function terminal(c, t, x, y, w, rows, title) {
  const h = 70 + rows.length * 58;
  rr(c, x + 8, y + 8, x + w + 8, y + h + 8, 18, INKL); rr(c, x, y, x + w, y + h, 18, TERM, INKL, 4);
  [[RED, 0], [AMBER, 1], [ACC, 2]].forEach(([col, k]) => ell(c, x + 22 + k * 30, y + 18, x + 42 + k * 30, y + 38, col));
  text(c, title, 'mono', 20, [150, 150, 150], x + 120, y + 12);
  rows.forEach(([t0, s, col], k) => {
    if (t < t0) return;
    const n = Math.floor(clamp((t - t0) / 0.6) * s.length), cur = n < s.length || Math.floor(t * 3) % 2 === 0;
    text(c, s.slice(0, n) + (cur && k === rows.filter(r => t >= r[0]).length - 1 ? '▌' : ''), 'mono', 25, col, x + 24, y + 58 + k * 58);
  });
}
function vCode(c, t) {
  const tb = at(2, 'Users');
  if (t > tb) phone(c, t, 230, 950, t < at(2, 'pushes', 1.2));
  terminal(c, t, 420, 770, 600, [
    [at(2, 'finds'), '$ git checkout -b fix-pay', LIGHTT],
    [at(2, 'three'), '+3 lines  src/checkout.js', ACC],
    [at(2, 'pushes'), '$ git push origin fix-pay', LIGHTT],
    [at(2, 'Git tracks'), '✓ commit a1f3c9e · 9:12 PM', ACC]], 'terminal · 9:05 PM');
  sticker(c, t, at(2, 'GitHub.'), 'PUSHED TO GITHUB', 760, 1150, -5, 36);
}
function node(c, cx, cy, label, sub, draw, a) {
  place(c, 230, 250, cx, cy, a, 0, 1, c => { rr(c, 0, 0, 230, 250, 22, CARD, CARDLN, 3); draw(c); placeText(c, label, 'pop', 28, LIGHTT, 115, 190); placeText(c, sub, 'type', 18, [170, 170, 170], 115, 225); });
}
function container(c, cx, cy, s) {
  rr(c, cx - 70 * s, cy - 45 * s, cx + 70 * s, cy + 45 * s, 8 * s, [40, 120, 200], INKL, lw(s));
  for (let k = -2; k <= 2; k++) line(c, [cx + k * 24 * s, cy - 35 * s, cx + k * 24 * s, cy + 35 * s], [20, 70, 130], Math.max(2, 4 * s));
}
function vBuild(c, t) {
  const tA = at(4, 'GitHub Actions'), tB = at(4, 'builds'), tD = at(4, 'Docker'), tL = at(4, 'laptop'), y = 900;
  node(c, 180, y, 'GitHub', 'push · fix-pay', c => { icoCode(c, 115, 85, 0.6); }, popIn(t, VO[4], 0.3));
  if (t > tA) node(c, 540, y, 'Actions', 'CI pipeline', c => icoGear(c, 115, 85, 0.75, t * 2.5), popIn(t, tA, 0.3));
  if (t > tD) node(c, 900, y, 'Docker', 'image v2.4.1', c => container(c, 115, 85, 0.8), popIn(t, tD, 0.3));
  for (const [x0, x1, ts] of [[300, 420, tA], [660, 780, tD]]) if (t > ts) {
    line(c, [x0, y, x1, y], [150, 150, 150], 5); poly(c, [x1, y - 12, x1 + 18, y, x1, y + 12], [150, 150, 150]);
    const u = ((t - ts) * 0.9) % 1; ell(c, x0 + (x1 - x0) * u - 9, y - 9, x0 + (x1 - x0) * u + 9, y + 9, ACC);
  }
  if (t > tB) {
    const q = eio(prog(t, tB, Math.max(0.5, tD - tB + 0.6)));
    text(c, 'BUILD', 'mono', 24, [170, 170, 170], 70, 1060); text(c, Math.round(q * 100) + '%', 'mono', 24, ACC, 940, 1060);
    rr(c, 70, 1105, 1010, 1135, 15, CARD, CARDLN, 3); if (q > 0.02) rr(c, 74, 1109, 74 + 932 * q, 1131, 11, ACC);
  }
  if (t > tL) {
    const p = popIn(t, tL, 0.3), p2 = popIn(t, at(4, 'server'), 0.3);
    if (p) place(c, 300, 200, 470, 1250, p, 0, 1, c => { rr(c, 40, 20, 260, 150, 12, PAPERW, INKL, 5); rr(c, 10, 150, 290, 172, 8, INKL); container(c, 150, 85, 0.6); placeText(c, 'LAPTOP', 'type', 20, LIGHTT, 150, 195); });
    if (p2) place(c, 300, 200, 830, 1250, p2, 0, 1, c => { for (let k = 0; k < 3; k++) rr(c, 60, 15 + k * 52, 240, 60 + k * 52, 8, PAPERW, INKL, 4); container(c, 150, 85, 0.6); placeText(c, 'SERVER', 'type', 20, LIGHTT, 150, 195); });
    sticker(c, t, at(4, 'server', 0.4), 'SAME BOX, SAME RESULT', 650, 1410, -4, 30);
  }
}
function vTest(c, t) {
  const COLS = 20, ROWS = 7, n = COLS * ROWS, t0 = VO[6] + 0.3, tf = at(6, 'If one'), bad = 97;
  const done = Math.floor(clamp((t - t0) / Math.max(0.5, tf - t0 - 0.3)) * (n - 1));
  for (let k = 0; k < n; k++) {
    const x = 100 + (k % COLS) * 46, y = 830 + Math.floor(k / COLS) * 46;
    const failed = k === bad && t > tf;
    const col = failed ? RED : k < done || (k !== bad && t > tf) ? ACC : [205, 205, 200];
    const r = failed ? 17 + 3 * Math.sin(t * 12) : 15;
    ell(c, x - r, y - r, x + r, y + r, col);
  }
  const passed = t > tf ? n - 1 : done;
  text(c, `TESTS  ${passed} / ${n} passed${t > tf ? '  ·  1 FAILED' : ''}`, 'mono', 24, t > tf ? RED : MUTE, 80, 760);
  sticker(c, t, at(6, 'fake'), 'FAKE CARD 4242 ✓', 780, 1200, 4, 32);
  alarm(c, t, at(6, 'pipeline stops'), 'PIPELINE STOPPED', 720, 1310, -5, 38);
  sticker(c, t, at(6, 'never reaches'), 'BUG NEVER SHIPS', 800, 1430, 4, 34);
}
function vDeploy(c, t) {
  const tT = at(8, 'Ten percent'), tE = at(8, 'then everyone'), tO = at(8, 'Old servers'), y = 870;
  text(c, 'KUBERNETES · 10 PODS', 'mono', 24, [170, 170, 170], 70, 760);
  for (let k = 0; k < 10; k++) {
    const sw = k === 0 ? tT : tE + 0.25 * k, on = t > sw, x = 110 + k * 96;
    const q = on ? popIn(t, sw, 0.3) : 1;
    place(c, 80, 110, x, y, q, 0, 1, c => {
      rr(c, 0, 0, 80, 110, 14, on ? ACC : CARD, on ? INKL : CARDLN, 4);
      placeText(c, on ? 'v2' : 'v1', 'pop', 30, on ? PAPERW : [170, 170, 170], 40, 55);
    });
  }
  if (t > tT) {
    const pct = t < tE ? 10 * eo(prog(t, tT, 0.5)) : 10 + 90 * eio(prog(t, tE, 2.6));
    text(c, 'USERS ON NEW VERSION', 'mono', 24, [170, 170, 170], 70, 975);
    rr(c, 70, 1020, 1010, 1060, 20, CARD, CARDLN, 3); rr(c, 74, 1024, 74 + 932 * pct / 100, 1056, 16, ACC);
    placeText(c, Math.round(pct) + '%', 'pop', 72, LIGHTT, 540, 1140);
  }
  if (t > tO) {
    text(c, 'v1 keeps serving until v2 is healthy', 'type', 24, [200, 200, 200], 230, 1215);
    const u = ((t - tO) * 0.6) % 1;
    line(c, [120, 1275, 960, 1275], [80, 84, 88], 6); ell(c, 120 + 840 * u - 12, 1263, 120 + 840 * u + 12, 1287, ACC);
    text(c, 'UPTIME 100%', 'mono', 24, ACC, 760, 1295);
  }
  sticker(c, t, at(8, 'Zero'), 'ZERO DOWNTIME', 700, 1400, -5, 42);
}
function vMonitor(c, t) {
  const x0 = 80, x1 = 1000, y0 = 760, y1 = 1120, tJ = at(10, 'errors jump'), tR = at(10, 'rolls back', 0.4);
  rr(c, x0, y0, x1, y1, 22, CARD, CARDLN, 3);
  text(c, 'GRAFANA · ERRORS / MIN · LIVE', 'mono', 22, [170, 170, 170], x0 + 24, y0 + 12);
  if (Math.floor(t * 2) % 2 === 0) ell(c, x1 - 50, y0 + 26, x1 - 30, y0 + 46, RED);
  const base = y1 - 60, thr = y0 + 150;
  c.save(); c.setLineDash([12, 10]); line(c, [x0 + 20, thr, x1 - 20, thr], RED, 3, 'butt'); c.restore();
  text(c, 'alert line', 'type', 20, RED, x1 - 150, thr - 40);
  const pts = [];
  for (let k = 0; k <= 60; k++) {
    const ts = t - (60 - k) * 0.08;
    let e = 18 + 6 * Math.sin(ts * 7.3) + 4 * Math.sin(ts * 13.1);
    if (ts > tJ) e += 220 * eo(prog(ts, tJ, 0.6));
    if (ts > tR) e -= 220 * eo(prog(ts, tR, 0.8));
    pts.push(x0 + 30 + k * 14.5, base - Math.max(4, e));
  }
  if (t > VO[10]) line(c, pts, t > tJ && t < tR + 1.5 ? RED : ACC, 6);
  alarm(c, t, at(10, 'alert fires'), 'ALERT · ON-CALL PAGED', 720, 1210, -4, 32);
  sticker(c, t, at(10, 'one command'), '$ kubectl rollout undo', 700, 1320, 4, 30);
  sticker(c, t, at(10, 'Ten PM'), '10:00 PM · FIXED', 780, 1440, -6, 40);
}
function vOutro(c, t) {
  const cx = 660, cy = 975, r = 215, names = ['Plan', 'code', 'build', 'test', 'deploy', 'monitor'];
  const tl = names.map(n => at(11, n));
  c.save(); c.translate(cx, cy); c.rotate(t * 0.5);
  c.setLineDash([18, 14]); c.beginPath(); c.arc(0, 0, r, 0, 2 * Math.PI); c.strokeStyle = rgb([170, 170, 170]); c.lineWidth = 5; c.stroke(); c.restore();
  names.forEach((n, k) => {
    const a = -Math.PI / 2 + k * Math.PI / 3, x = cx + r * Math.cos(a), y = cy + r * Math.sin(a), on = t > tl[k];
    const label = n[0].toUpperCase() + n.slice(1), b = box(label, 'pop', 30), w = b.w + 30;
    place(c, w, 60, x, y, on ? popIn(t, tl[k], 0.3) : 1, 0, 1, c => { rr(c, 0, 0, w, 60, 30, on ? ACC : PAPERW, INKL, 4); placeText(c, label, 'pop', 30, on ? PAPERW : MUTE, w / 2, 30); });
  });
  const p = popIn(t, at(11, 'DevOps'), 0.4);
  placeText(c, p ? 'DevOps' : '∞', 'pop', p ? 64 : 110, p ? INKL : [190, 190, 190], cx, cy, p || 1);
  sticker(c, t, at(11, 'Save'), 'SAVE', 930, 1260, 7, 52);
  sticker(c, t, at(11, 'send'), 'SEND TO A FRIEND', 800, 1400, -5, 36);
}
const VIS = { 0: vIntro, 2: vCode, 4: vBuild, 6: vTest, 8: vDeploy, 10: vMonitor, 11: vOutro };

function frame(c, t) {
  const i = segAt(t), dark = DARK.has(i), item = i >= 1 && i <= 2 * NI ? Math.floor((i - 1) / 2) : null;
  bg(c, dark);
  hud(c, item !== null ? item + 2 : (i === 0 ? 1 : NI + 2), item !== null ? `#${item + 1} · ${SLUGS[item]}` : (i === 0 ? '9:00 PM · bug' : 'the loop'),
    FILL.filter(ft => t > ft).length, NI, dark, 'STEPS');
  head(c, t, i, dark);
  if (item !== null) {
    itemTitle(c, t, VO[1 + 2 * item], item + 1, NAMES[item], PILLS[item], ICONS[item], 640, dark);
    if (i % 2 === 1) {
      const q = popIn(t, VO[i] + 0.15, 0.45);
      if (q > 0.02) place(c, 600, 600, 720, 1050, q, Math.sin(t * 2) * 3, 1, c => item === 1 ? icoGear(c, 300, 300, 2.0, t) : ICONS[item](c, 300, 300, 2.0));
    }
  }
  if (VIS[i]) VIS[i](c, t);
  if (item !== null && t > VO[1 + 2 * item]) text(c, SRC[item], 'type', 21, dark ? [150, 150, 150] : MUTE, 60, 1870);
  if (i === 0 || i === 11) text(c, 'Illustrative example of a typical CI/CD pipeline. Education only.', 'type', 22, MUTE, 60, 1870);
  shelf(c, t, 560, 1690, NI, FILL, ICONS, { w: 470, dark, label: 'PIPELINE' });
  drawHost(c, t, ALLW, !dark);
  flash(c, t, SWITCH);
}

// cover / thumbnail (drawn when t < 0)
function cover(c) {
  bg(c, false);
  placeText(c, 'APP BROKE AT', 'pop', 64, MUTE, 540, 300);
  clock(c, 0.3, 540, 500, 1, '9:00 PM', RED);
  placeText(c, 'FIXED BY 10', 'pop', 120, INKL, 540, 760, 1, -2);
  rr(c, 170, 860, 910, 960, 50, ACC);
  placeText(c, 'DEVOPS IN 5 STEPS', 'pop', 54, PAPERW, 540, 908);
  ICONS.forEach((ic, k) => { const x = 180 + k * 180; rr(c, x - 75, 1010, x + 75, 1160, 20, PAPERW, INKL, 4); k === 1 ? icoGear(c, x, 1085, 0.7, 0.3) : ic(c, x, 1085, 0.6); });
  placeText(c, 'Git · Actions · Docker', 'type', 30, INKL, 790, 1250, 1, 0, 1, 1);
  placeText(c, 'Kubernetes · Grafana', 'type', 30, INKL, 790, 1300, 1, 0, 1, 1);
  drawHost(c, 0, [], true);
  sticker(c, 1, 0, 'REAL EXAMPLE', 780, 1450, -6, 50);
}

let LOOPBUF;
function drawFrame(c, t) {
  if (t < 0) return cover(c);
  frame(c, t);
  const LOOP = 0.6;
  if (t > DUR - LOOP) {
    const g = LOOPBUF.getContext('2d'); frame(g, 0.35);
    c.globalAlpha = eio((t - (DUR - LOOP)) / LOOP); c.drawImage(LOOPBUF, 0, 0); c.globalAlpha = 1;
  }
}

async function init(root) {
  SCRIPT = await getJSON(root + 'devops/script.json'); DURS = await getJSON(root + 'devops/vo/durs.json');
  ({ starts: STARTS, vo: VO, dur: DUR } = timing(DURS));
  WORDS = wordTimes(SCRIPT, DURS, VO);
  ALLW = WORDS.flat(); ACC_IDX = SCRIPT.map((_, i) => accIdx(i)); PAGES = SCRIPT.map((_, i) => pages(i));
  SWITCH = [3, 5, 7, 9, 11].map(k => STARTS[k]); FILL = [...Array(NI)].map((_, k) => VO[1 + 2 * k] + 0.5);
  LOOPBUF = document.createElement('canvas'); LOOPBUF.width = W; LOOPBUF.height = H;
  return DUR;
}
window.REEL = { init, drawFrame };
