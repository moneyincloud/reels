/* @moneyincloud camera kit: seek-safe GSAP camera moves for HyperFrames reels.
   Usage (after gsap + your paused root timeline `tl`):
     const cam = CAM(tl);
     cam.pushIn("#cam2", 3.0, {to:1.3});
   Wrap each scene's content in a full-frame div (the "camera", e.g. .cam) and move that div.
   For 3D moves (orbit, tilt, dutch3d) give the scene section `perspective:1600px`.
   Every move is fromTo or absolute, so seeking/scrubbing renders identical frames. */
window.CAM = function (tl) {
  const O = (o, d) => Object.assign({}, d, o || {});
  return {
    /* slow zoom in on a point (ox/oy = focus point) */
    pushIn(el, at, o) { o = O(o, {from:1, to:1.25, dur:1.4, ox:"50%", oy:"50%", ease:"power2.inOut"});
      return tl.fromTo(el, {scale:o.from, transformOrigin:o.ox+" "+o.oy}, {scale:o.to, duration:o.dur, ease:o.ease}, at); },
    /* zoom out to reveal the whole frame */
    pullOut(el, at, o) { o = O(o, {from:1.35, to:1, dur:1.4, ox:"50%", oy:"50%", ease:"power3.out"});
      return tl.fromTo(el, {scale:o.from, transformOrigin:o.ox+" "+o.oy}, {scale:o.to, duration:o.dur, ease:o.ease}, at); },
    /* very fast punch-in with motion blur, for a number reveal */
    crashZoom(el, at, o) { o = O(o, {to:1.7, dur:0.22, hold:0.6, ox:"50%", oy:"50%"});
      tl.fromTo(el, {scale:1, filter:"blur(0px)", transformOrigin:o.ox+" "+o.oy}, {scale:o.to, filter:"blur(6px)", duration:o.dur*0.6, ease:"power4.in"}, at);
      tl.to(el, {filter:"blur(0px)", duration:o.dur*0.4, ease:"none"}, at + o.dur*0.6);
      return tl.to(el, {scale:1, duration:0.45, ease:"power3.inOut"}, at + o.dur + o.hold); },
    /* pan across a wide set; x/y are where the camera ends (negative = move right/down in the world) */
    track(el, at, o) { o = O(o, {x0:0, y0:0, x:-400, y:0, dur:2, ease:"power1.inOut"});
      return tl.fromTo(el, {x:o.x0, y:o.y0}, {x:o.x, y:o.y, duration:o.dur, ease:o.ease}, at); },
    /* whip pan between two scenes (out goes one way, in comes from the other) with blur */
    whip(outEl, inEl, at, o) { o = O(o, {dir:1, dist:1150, dur:0.42});
      if (outEl) tl.fromTo(outEl, {x:0, filter:"blur(0px)"}, {x:-o.dir*o.dist, filter:"blur(14px)", duration:o.dur, ease:"power3.in"}, at - o.dur);
      return tl.fromTo(inEl, {x:o.dir*o.dist, filter:"blur(14px)"}, {x:0, filter:"blur(0px)", duration:o.dur+0.08, ease:"power3.out"}, at - 0.05); },
    /* dutch angle: roll the camera for tension */
    dutch(el, at, o) { o = O(o, {deg:-7, dur:0.6, hold:1.2});
      tl.fromTo(el, {rotation:0}, {rotation:o.deg, duration:o.dur, ease:"back.out(1.7)"}, at);
      return tl.to(el, {rotation:0, duration:o.dur, ease:"power2.inOut"}, at + o.dur + o.hold); },
    /* 3D orbit around the subject (needs perspective on the parent) */
    orbit(el, at, o) { o = O(o, {from:-28, to:22, dur:2.2, ease:"sine.inOut"});
      return tl.fromTo(el, {rotationY:o.from, transformPerspective:1600}, {rotationY:o.to, duration:o.dur, ease:o.ease}, at); },
    /* 3D tilt (look up / look down at a chart) */
    tilt(el, at, o) { o = O(o, {from:24, to:0, dur:1.4, ease:"power3.out"});
      return tl.fromTo(el, {rotationX:o.from, transformPerspective:1600, transformOrigin:"50% 100%"}, {rotationX:o.to, duration:o.dur, ease:o.ease}, at); },
    /* focus pull: blurred to sharp (or reverse with o.out=true) */
    rack(el, at, o) { o = O(o, {blur:10, dur:0.7, out:false});
      return o.out ? tl.fromTo(el, {filter:"blur(0px)"}, {filter:`blur(${o.blur}px)`, duration:o.dur}, at)
                   : tl.fromTo(el, {filter:`blur(${o.blur}px)`}, {filter:"blur(0px)", duration:o.dur, ease:"power2.out"}, at); },
    /* impact shake (uses y so it never fights x pans) */
    shake(el, at, o) { o = O(o, {amp:14, n:8, step:0.04});
      const kf = []; for (let k = 0; k < o.n; k++) kf.push({y:(k%2?-1:1)*o.amp*(1-k/o.n), duration:o.step, ease:"none"});
      kf.push({y:0, duration:o.step}); return tl.to(el, {keyframes:kf}, at); },
    /* Ken Burns: slow drift + zoom for stills */
    kenBurns(el, at, o) { o = O(o, {dur:4, from:1.05, to:1.18, x:-40, y:-30});
      return tl.fromTo(el, {scale:o.from, x:0, y:0}, {scale:o.to, x:o.x, y:o.y, duration:o.dur, ease:"none"}, at); },
    /* dolly zoom (vertigo): background grows while the subject shrinks back, so the subject stays put */
    dollyZoom(bg, subject, at, o) { o = O(o, {amt:0.35, dur:1.6, ease:"power2.inOut"});
      tl.fromTo(bg, {scale:1}, {scale:1 + o.amt, duration:o.dur, ease:o.ease}, at);
      return tl.fromTo(subject, {scale:1 + o.amt*0.5}, {scale:1, duration:o.dur, ease:o.ease}, at); },
    /* parallax: layers move at different speeds (pass [back, mid, front]) */
    parallax(layers, at, o) { o = O(o, {dur:2.4, dist:-260, ease:"power1.inOut"});
      layers.forEach((l, i) => tl.fromTo(l, {x:0}, {x:o.dist*(0.35 + i*0.45), duration:o.dur, ease:o.ease}, at)); return tl; },
    /* handheld float for the whole video (deterministic sine) */
    handheld(el, dur, o) { o = O(o, {rot:0.35, x:5, y:-4, period:3});
      return tl.to(el, {rotation:o.rot, x:o.x, y:o.y, duration:o.period, ease:"sine.inOut", repeat:Math.max(0, Math.floor(dur/o.period)-1), yoyo:true}, 0); },
  };
};
