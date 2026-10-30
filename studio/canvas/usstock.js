// usstock on <canvas>: port of vox/usstock.py ("Don't buy a US stock before you know these 5 things").
const RED = [225, 80, 70], LIGHTT = [240, 240, 240], CARD = [32, 34, 36], CARDLN = [80, 84, 88];
const ACCENTS = [["five things."], ["How to buy."], ["W-8BEN,", "fraction"], ["real cost."],
  ["half to one point two percent", "point two five percent", "twenty percent TCS", "claim it back"],
  ["Tax.", "surprises"], ["slab rate.", "twelve point five percent.", "twenty five percent", "Schedule FA."],
  ["Pros and cons."], ["Pros.", "Cons.", "biggest companies,", "dollar rises.", "both ways,", "late at night,", "stronger rupee"],
  ["already use."], [], ["Not a buy call,", "Save this,"]];
const DARK = new Set([3, 4, 7, 8]), NI = 5;
const ICONS = [icoPhone, icoSwap, icoTaxdoc, icoScale, icoGrid10];
const NAMES = ['How to buy', 'The real cost', 'Tax', 'Pros & cons', '10 companies'];
const PILLS = ['4 STEPS · FRACTIONS OK', 'FX + BROKERAGE + TCS', 'THE 2-YEAR LINE', 'KNOW BOTH SIDES', 'YOU USE THEM DAILY'];
const SLUGS = ['how to buy', 'real cost', 'tax', 'pros & cons', 'the 10'];
const SRC = ['Steps as in the INDmoney app (Oct 2026) · app I use',
  'FX 0.5-1.2% & brokerage 0.25% (max $25) + GST: INDmoney · TCS: Business Today, Oct 2026',
  'Tax rules: Tickertape (Sep 2026) · ask a CA for your case',
  'NYSE 9:30 AM-4 PM New York = 8 PM-2:30 AM IST (from 2 Nov 2026)',
  'Prices: INDmoney live, 30 Oct 2026, 11:09 PM IST · not a buy/sell call'];
const CO = [['Google', 'GOOGL', 278.94, 'Search, YouTube'], ['Apple', 'AAPL', 346.27, 'iPhone, Mac'],
  ['Microsoft', 'MSFT', 519.98, 'Windows, Office'], ['Amazon', 'AMZN', 239.11, 'Shopping, Prime'],
  ['Meta', 'META', 618.21, 'Instagram, WhatsApp'], ['Netflix', 'NFLX', 62.11, 'Streaming'],
  ['Nvidia', 'NVDA', 203.15, 'AI & gaming chips'], ['Visa', 'V', 416.28, 'Card payments'],
  ['Coca-Cola', 'KO', 94.60, 'Coke, Thums Up'], ["McDonald's", 'MCD', 259.49, 'Burgers']];

let SCRIPT, DURS, STARTS, VO, DUR, WORDS, ALLW, ACC_IDX, PAGES, SWITCH, FILL;

function merge(i, a, b, nw) {
  const ws = WORDS[i];
  for (let k = 0; k < ws.length - 1; k++) if (ws[k][0] === a && ws[k + 1][0] === b) { ws[k] = [nw, ws[k][1]]; ws.splice(k + 1, 1); return; }
}
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

// ---------------- visuals ----------------
function vIntro(c, t) {
  const p = popIn(t, VO[0] + 0.2, 0.4);
  if (p) placeText(c, '0/5', 'pop', 300, INKL, 640, 980, p);
  sticker(c, t, at(0, "Don't"), "DON'T BUY YET", 660, 790, -7, 44);
  sticker(c, t, at(0, 'five'), '5 THINGS FIRST', 690, 1170, 5, 40);
}
function stepCard(c, t, t0, n, title, sub, x, y, w = 500) {
  if (t < t0) return;
  const q = eo(prog(t, t0, 0.3)), h = 104;
  place(c, w + 10, h + 10, x + w / 2 + (1 - q) * 80, y, 1, 0, q, c => {
    const a = c.globalAlpha;
    rr(c, 8, 8, w + 8, h + 8, 18, INKL); rr(c, 0, 0, w, h, 18, PAPERW, INKL, 4); ell(c, 18, 26, 70, 78, ACC);
    const nb = box(String(n), 'pop', 32); text(c, String(n), 'pop', 32, PAPERW, 44 - Math.floor(nb.w / 2), 28, 0, a);
    text(c, title, 'pop', 34, INKL, 88, 12, 0, a); text(c, sub, 'type', 22, MUTE, 90, 64, 0, a);
  });
}
function vBuy(c, t) {
  const rows = [['open US stocks', 'Open US stocks', 'inside the INDmoney app'], ['KYC', 'Finish KYC', 'PAN, address, bank'],
    ['W-8', 'Sign form W-8BEN', 'US dividend tax 30% -> 25%'], ['add money', 'Add money', 'rupees go out under LRS'],
    ['and buy', 'Buy', 'even a fraction of 1 share']];
  rows.forEach(([ph, ti, sb], k) => stepCard(c, t, at(2, ph, -0.15), k + 1, ti, sb, 500, 800 + k * 112));
  if (t > at(2, 'fraction')) {
    const q = eo(prog(t, at(2, 'fraction'), 0.8)), cx = 250, cy = 880, r = 110;
    ell(c, cx - r, cy - r, cx + r, cy + r, PAPERW, INKL, 6);
    if (q > 0) { c.beginPath(); c.moveTo(cx, cy); c.arc(cx, cy, r - 8, -Math.PI / 2, -Math.PI / 2 + 36 * q * Math.PI / 180); c.closePath(); c.fillStyle = rgb(ACC); c.fill(); }
    placeText(c, '0.1 SHARE', 'type', 26, INKL, cx, cy + r + 30, 1, 0, 1, 2);
  }
}
function costRow(c, label, big, sub, cx, cy, alpha, w = 520) {
  const h = 150;
  place(c, w, h, cx, cy, 1, 0, alpha, c => {
    const a = c.globalAlpha; rr(c, 0, 0, w - 1, h - 1, 20, CARD, CARDLN, 3);
    text(c, label, 'type', 22, [170, 170, 170], 24, 14, 2, a); text(c, big, 'pop', 48, ACC, 24, 40, 0, a); text(c, sub, 'type', 22, [220, 220, 220], 24, 108, 0, a);
  });
}
function vCost(c, t) {
  const p = popIn(t, VO[4] + 0.1, 0.45);
  if (p) place(c, 420, 300, 270, 900, p, 0, 1, c => icoSwap(c, 210, 170, 1.7));
  const rows = [['half to one', 'FX CONVERSION', '0.5% - 1.2%', 'charged by your bank'], ['Brokerage', 'BROKERAGE', '0.25% a trade', '+ GST, max $25 per trade'],
    ['Above ten lakh', 'TCS (ABOVE ₹10 LAKH/YR)', '20%', 'only on the extra · claim back in ITR']];
  rows.forEach(([ph, a, b, s], k) => {
    const t0 = at(4, ph, -0.2);
    if (t > t0) { const q = eo(prog(t, t0, 0.3)); costRow(c, a, b, s, 780 + (1 - q) * 60, 830 + k * 170, q); }
  });
  const t1 = at(4, 'GST', 0.6);
  if (t > t1) {
    const v = Math.floor(100000 - 1292 * eo(prog(t, t1, 1.2)));
    placeText(c, 'ON ₹1 LAKH (AT 1% FX):', 'type', 24, [190, 190, 190], 270, 1080, 1, 0, 1, 2);
    placeText(c, '₹' + v.toLocaleString('en-US'), 'pop', 64, LIGHTT, 270, 1140);
    placeText(c, 'reaches the stock', 'type', 22, [190, 190, 190], 270, 1195);
  }
  sticker(c, t, at(4, 'claim it back'), 'TCS IS NOT LOST', 300, 1330, -6, 32);
}
function vTax(c, t) {
  const x0 = 110, x1 = 990, y = 930, mid = x0 + (x1 - x0) * 0.5, t0 = at(6, 'Sell'), t2 = at(6, 'Hold');
  if (t > t0) {
    const q = eo(prog(t, t0, 0.5));
    rr(c, x0, y - 22, x0 + (mid - x0) * q, y + 22, 12, RED, INKL, 4);
    placeText(c, 'SELL WITHIN 2 YEARS', 'type', 24, MUTE, (x0 + mid) / 2, y - 90, 1, 0, 1, 2);
    if (t > at(6, 'slab')) placeText(c, 'YOUR SLAB RATE', 'pop', 40, RED, (x0 + mid) / 2, y + 70, popIn(t, at(6, 'slab')));
  }
  if (t > t2) {
    const q = eo(prog(t, t2, 0.5));
    rr(c, mid, y - 22, mid + (x1 - mid) * q, y + 22, 12, ACC, INKL, 4);
    placeText(c, 'HOLD 2+ YEARS', 'type', 24, MUTE, (mid + x1) / 2, y - 90, 1, 0, 1, 2);
    if (t > at(6, 'twelve')) {
      const v = 12.5 * eo(prog(t, at(6, 'twelve'), 0.8));
      placeText(c, v.toFixed(1) + '%', 'pop', 64, ACC, (mid + x1) / 2, y + 80);
      placeText(c, '+ surcharge & cess', 'type', 22, MUTE, (mid + x1) / 2, y + 135);
    }
  }
  if (t > t0) {
    placeText(c, '24 MONTHS', 'type', 22, INKL, mid, y - 46, 1, 0, 1, 2);
    line(c, [mid, y - 30, mid, y + 30], INKL, 5, 'butt');
    const u = clamp((t - t0) / Math.max(0.1, at(6, 'Dividends') - t0)), mx = x0 + (x1 - x0) * u;
    ell(c, mx - 16, y - 16, mx + 16, y + 16, PAPERW, INKL, 5);
  }
  const td = at(6, 'Dividends');
  if (t > td) {
    const v = 100 - 25 * eo(prog(t, td + 0.5, 0.8));
    placeText(c, '$100 DIVIDEND', 'type', 26, MUTE, 300, 1060, 1, 0, 1, 2);
    placeText(c, '$' + Math.round(v), 'pop', 84, INKL, 300, 1125);
    if (t > at(6, 'claim')) sticker(c, t, at(6, 'claim'), 'CLAIM CREDIT IN INDIA', 760, 1110, 4, 32);
  }
  sticker(c, t, at(6, 'Schedule'), 'REPORT IN SCHEDULE FA', 770, 1290, -5, 34);
}
function pcRow(c, txt, good, cx, cy, scale, w = 440) {
  const h = 92;
  place(c, w, h, cx, cy, scale, 0, 1, c => {
    rr(c, 0, 0, w - 1, h - 1, 18, CARD, CARDLN, 3); ell(c, 16, 22, 64, 70, good ? ACC : RED);
    if (good) line(c, [28, 46, 38, 57, 54, 36], PAPERW, 6);
    else { line(c, [30, 36, 50, 56], PAPERW, 6); line(c, [50, 36, 30, 56], PAPERW, 6); }
    let f = 30; while (textW(txt, 'pop', f) > w - 100 && f > 18) f -= 2;
    const b = box(txt, 'pop', f); text(c, txt, 'pop', f, LIGHTT, 80, Math.floor((h - b.h) / 2) - 4);
  });
}
function vPc(c, t) {
  placeText(c, 'PROS', 'pop', 46, ACC, 290, 800); placeText(c, 'CONS', 'pop', 46, RED, 790, 800);
  [['biggest', "World's biggest companies"], ['dollar rises', 'Gain if the dollar rises']].forEach(([ph, tx], k) => {
    const t0 = at(8, ph, -0.3); if (t > t0) pcRow(c, tx, true, 290, 900 + k * 110, popIn(t, t0, 0.25));
  });
  [['both ways', 'FX cost in and out'], ['late at night', 'Opens 8 PM IST (winter)'], ['stronger rupee', 'Strong rupee cuts returns']].forEach(([ph, tx], k) => {
    const t0 = at(8, ph, -0.3); if (t > t0) pcRow(c, tx, false, 790, 900 + k * 110, popIn(t, t0, 0.25));
  });
}
function coCard(c, k, cx, cy, scale) {
  const [name, tk, px, use] = CO[k], w = 460, h = 96;
  place(c, w + 8, h + 8, cx, cy, scale, 0, 1, c => {
    rr(c, 7, 7, w + 7, h + 7, 16, INKL); rr(c, 0, 0, w, h, 16, PAPERW, INKL, 4);
    ell(c, 12, 12, 46, 46, ACC); const nb = box(String(k + 1), 'pop', 24); text(c, String(k + 1), 'pop', 24, PAPERW, 29 - Math.floor(nb.w / 2), 13);
    text(c, name, 'pop', 32, INKL, 56, 6); text(c, use, 'type', 20, MUTE, 58, 58);
    const ps = '$' + px.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    text(c, ps, 'pop', 30, ACC, w - 18 - box(ps, 'pop', 30).w, 8); text(c, tk, 'type', 20, INKL, w - 18 - box(tk, 'type', 20, 2).w, 58, 2);
  });
}
function vTen(c, t) {
  const ws = WORDS[10];
  for (let k = 0; k < 10; k++) {
    const r = k % 5, q = Math.floor(k / 5), x = 300 + q * 490, y = 800 + r * 112, tk = k < ws.length ? ws[k][1] : 1e9;
    if (t < tk - 0.1) {
      dashed(c, x - 230, y - 48, x + 230, y - 48, [170, 170, 170], 2, 8, 8); dashed(c, x - 230, y + 48, x + 230, y + 48, [170, 170, 170], 2, 8, 8);
      placeText(c, '?', 'pop', 40, [170, 170, 170], x, y);
    } else coCard(c, k, x, y, popIn(t, tk - 0.1, 0.25));
  }
}
function vOutro(c, t) {
  const p = popIn(t, VO[11], 0.4);
  if (p) placeText(c, '5/5', 'pop', 260, ACC, 680, 900, p);
  sticker(c, t, at(11, 'Not a buy'), 'NOT A BUY CALL', 690, 1100, -5, 40);
  sticker(c, t, at(11, 'Save'), 'SAVE', 900, 1270, 7, 52);
  sticker(c, t, at(11, 'send'), 'SEND TO THAT FRIEND', 710, 1420, -6, 36);
}
const VIS = { 0: vIntro, 2: vBuy, 4: vCost, 6: vTax, 8: vPc, 9: vTen, 10: vTen, 11: vOutro };

function frame(c, t) {
  const i = segAt(t), dark = DARK.has(i), item = i >= 1 && i <= 2 * NI ? Math.floor((i - 1) / 2) : null;
  bg(c, dark);
  hud(c, item !== null ? item + 2 : (i === 0 ? 1 : NI + 2), item !== null ? `#${item + 1} · ${SLUGS[item]}` : (i === 0 ? 'before you buy' : 'ready'),
    FILL.filter(ft => t > ft).length, NI, dark, 'LEARNED');
  head(c, t, i, dark);
  if (item !== null) {
    itemTitle(c, t, VO[1 + 2 * item], item + 1, NAMES[item], PILLS[item], ICONS[item], 640, dark);
    if (i % 2 === 1 && i !== 9) {
      const q = popIn(t, VO[i] + 0.15, 0.45);
      if (q > 0.02) place(c, 600, 600, 720, 1050, q, Math.sin(t * 2) * 3, 1, c => ICONS[item](c, 300, 300, 2.0));
    }
  }
  if (VIS[i]) VIS[i](c, t);
  if (item !== null && t > VO[1 + 2 * item]) text(c, SRC[item], 'type', 21, dark ? [150, 150, 150] : MUTE, 60, 1870);
  if (i === 0 || i === 11) text(c, 'Not a buy/sell call. Education only.', 'type', 22, MUTE, 60, 1870);
  shelf(c, t, 560, 1690, NI, FILL, ICONS, { w: 470, dark, label: 'WHAT YOU KNOW' });
  drawHost(c, t, ALLW, !dark && i !== 9 && i !== 10);
  flash(c, t, SWITCH);
}

// loop ending: last 0.6 s cross-fades back to the hook frame
let LOOPBUF;
function drawFrame(c, t) {
  frame(c, t);
  const LOOP = 0.6;
  if (t > DUR - LOOP) {
    const g = LOOPBUF.getContext('2d'); frame(g, 0.35);
    c.globalAlpha = eio((t - (DUR - LOOP)) / LOOP); c.drawImage(LOOPBUF, 0, 0); c.globalAlpha = 1;
  }
}

async function init(root) {
  SCRIPT = await getJSON(root + 'usstock/script.json'); DURS = await getJSON(root + 'usstock/vo/durs.json');
  ({ starts: STARTS, vo: VO, dur: DUR } = timing(DURS));
  WORDS = wordTimes(SCRIPT, DURS, VO);
  merge(2, 'IND', 'money', 'INDmoney'); merge(2, 'W-8', 'BEN,', 'W-8BEN,'); merge(6, 'F', 'A.', 'FA.');
  ALLW = WORDS.flat(); ACC_IDX = SCRIPT.map((_, i) => accIdx(i)); PAGES = SCRIPT.map((_, i) => pages(i));
  SWITCH = [3, 5, 7, 9, 11].map(k => STARTS[k]); FILL = [...Array(NI)].map((_, k) => VO[1 + 2 * k] + 0.5);
  LOOPBUF = document.createElement('canvas'); LOOPBUF.width = W; LOOPBUF.height = H;
  return DUR;
}
window.REEL = { init, drawFrame };
