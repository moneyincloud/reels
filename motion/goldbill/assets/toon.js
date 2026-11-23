/* @moneyincloud Chennai Toon kit: seek-safe character + caption animation helpers (GSAP).
   const T = TOON(tl);  T.idle('arjun', 0, 8); T.talk('arjun', [0.4, 0.7, ...]); T.pose('arjun', 2.0, {R:[-150, -30]}); */
window.TOON = function (tl) {
  const OR = {armR:'281 352', armL:'119 352', foreR:'281 470', foreL:'119 470', head:'200 330', body:'200 880', eyes:'200 222'};
  const q = (cid, part) => document.getElementById(cid + '-' + part);
  const T = {
    /* breathing + gentle head sway between t0 and t1 */
    idle(cid, t0, t1, o) {
      o = Object.assign({period:1.6, amp:0.014, sway:2.5}, o || {});
      const n = Math.max(1, Math.floor((t1 - t0) / o.period));
      tl.fromTo(q(cid, 'body'), {scaleY:1, svgOrigin:OR.body}, {scaleY:1 + o.amp, duration:o.period / 2, ease:'sine.inOut', yoyo:true, repeat:n * 2 - 1}, t0);
      tl.fromTo(q(cid, 'head'), {rotation:-o.sway, svgOrigin:OR.head}, {rotation:o.sway, duration:o.period * 1.3, ease:'sine.inOut', yoyo:true, repeat:Math.max(1, Math.floor((t1 - t0) / (o.period * 1.3)) - 1)}, t0);
    },
    /* mouth flaps on each word time (absolute seconds) */
    talk(cid, words, close) {
      const mo = q(cid, 'mo'), mc = q(cid, 'mc');
      tl.set(mo, {opacity:0}, 0); tl.set(mc, {opacity:1}, 0);
      words.forEach((t, i) => {
        const nxt = i + 1 < words.length ? words[i + 1] : t + 0.3;
        tl.set(mo, {opacity:1}, t); tl.set(mc, {opacity:0}, t);
        const c = Math.min(t + 0.16, nxt - 0.03);
        if (c > t + 0.05) { tl.set(mo, {opacity:0}, c); tl.set(mc, {opacity:1}, c); }
      });
      if (close != null) { tl.set(mo, {opacity:0}, close); tl.set(mc, {opacity:1}, close); }
    },
    blink(cid, t0, t1, every) {
      every = every || 2.9;
      for (let t = t0 + 0.8; t < t1 - 0.2; t += every) {
        tl.fromTo(q(cid, 'eyes'), {scaleY:1, svgOrigin:OR.eyes}, {scaleY:0.1, duration:0.06, ease:'none', yoyo:true, repeat:1, immediateRender:false}, t);
      }
    },
    /* arm pose: {R:[upper, fore], L:[upper, fore]} degrees. R raises with negative, L with positive. */
    pose(cid, at, p, dur) {
      dur = dur || 0.35;
      const set = (side, v) => {
        if (!v) return;
        tl.to(q(cid, 'arm' + side), {rotation:v[0], svgOrigin:OR['arm' + side], duration:dur, ease:'back.out(1.8)'}, at);
        tl.to(q(cid, 'fore' + side), {rotation:v[1] || 0, svgOrigin:OR['fore' + side], duration:dur, ease:'back.out(1.8)'}, at);
      };
      set('R', p.R); set('L', p.L);
    },
    rest(cid, at) { T.pose(cid, at, {R:[-6, 0], L:[6, 0]}, 0.4); },
    wave(cid, at, n, side) {
      side = side || 'R'; n = n || 3; const s = side === 'R' ? -1 : 1;
      T.pose(cid, at, side === 'R' ? {R:[-150, 0]} : {L:[150, 0]}, 0.3);
      tl.fromTo(q(cid, 'fore' + side), {rotation:-25 * s, svgOrigin:OR['fore' + side]}, {rotation:25 * s, duration:0.2, ease:'sine.inOut', yoyo:true, repeat:n * 2 - 1, immediateRender:false}, at + 0.3);
      tl.to(q(cid, 'fore' + side), {rotation:0, duration:0.15, svgOrigin:OR['fore' + side]}, at + 0.3 + n * 0.4);
    },
    point(cid, at, side) { side = side || 'R'; T.pose(cid, at, side === 'R' ? {R:[-95, -10]} : {L:[95, 10]}); },
    pointUp(cid, at, side) { side = side || 'R'; T.pose(cid, at, side === 'R' ? {R:[-140, -40]} : {L:[140, 40]}); },
    cheer(cid, at) { T.pose(cid, at, {R:[-155, -20], L:[155, 20]}); T.hop(cid, at); },
    shrug(cid, at) { T.pose(cid, at, {R:[-50, -90], L:[50, 90]}); },
    think(cid, at) { T.pose(cid, at, {R:[-20, -150]}); },
    hop(cid, at, h) {
      h = h || 40;
      tl.fromTo(q(cid, 'body'), {y:0}, {y:-h, duration:0.18, ease:'power2.out', yoyo:true, repeat:1, immediateRender:false}, at);
    },
    nod(cid, at) { tl.fromTo(q(cid, 'head'), {rotation:0, svgOrigin:OR.head}, {rotation:6, duration:0.14, yoyo:true, repeat:3, immediateRender:false}, at); },
    /* slide a character wrapper in from off-screen */
    enter(cid, at, from) {
      const w = document.getElementById(cid + 'w'); const dx = from === 'right' ? 700 : -700;
      tl.fromTo(w, {x:dx}, {x:0, duration:0.55, ease:'back.out(1.3)'}, at);
    },
    /* caption chunk: words pop in at their times */
    caption(chunkId, t0, t1, wordTimes) {
      const el = document.getElementById(chunkId);
      tl.set(el, {opacity:1}, t0); tl.set(el, {opacity:0}, t1);
      el.querySelectorAll('.w').forEach((w, i) => {
        tl.fromTo(w, {opacity:0, scale:1.35, y:14}, {opacity:1, scale:1, y:0, duration:0.16, ease:'back.out(3)', immediateRender:false}, wordTimes[i]);
      });
    },
  };
  return T;
};
