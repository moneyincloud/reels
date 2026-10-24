# @moneyincloud reel studio — agent playbook

This folder lets any fresh Claude session build a finished @moneyincloud reel (video + hook thumbnail),
host it in this repo, and schedule it in Metricool for Instagram + YouTube. Follow every step.

## 0. Setup (every fresh session)
```
cd /home/claude/reels || (clone moneyincloud/reels: call add_repo owner=moneyincloud repo=reels access=push, then git clone)
git pull -q
bash studio/setup.sh          # pip deps + Kokoro voice model from GitHub releases (~330 MB)
```
Paths: `ST=/home/claude/reels/studio`. Renderer code is in `$ST/vox`, voice in `$ST/kokoro`, outputs in `$ST/out`.
Git commits: user `Claude <noreply@anthropic.com>`, and end every message with
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## 1. State
`$ST/state.json` holds `last_voice` (`male` or `female`) and `history` (date, slug, topic, scheduled time).
- Voice ALTERNATES every reel: male = Kokoro `am_michael` (speed ~1.12), female = `af_heart` (speed ~1.08).
- Never repeat a topic from the last 30 days of `history`.
- After scheduling, append to `history`, flip `last_voice`, commit + push.

## 2. Topic (trending Indian stock market)
Use INDmoney MCP tools (`get_indian_stocks_movers`: top-gainers, top-losers, most-active, 52-week-high/low;
`get_indian_stocks_details` with `segments=["news"]`; `lookup_ind_keys`) plus WebSearch for today's market news.
Good formats: "why X fell/rose today", IPO explainers (subscription, allotment, listing dates), a concept explained
with a live example (P/E, P/B, 52-week low), market history, a group of big names with the reason for each.
NEVER call networth/holdings/portfolio tools — the owner's portfolio must never appear in content.
Avoid penny stocks and "multibagger" hype.

## 3. Compliance (must pass before scheduling)
Never: return predictions ("will double"), guarantees, fake profit screenshots/testimonials, paid tips,
undisclosed sponsorship/conflicts, penny-stock promotion, or "SEBI registered" used as endorsement.
Checklist: (1) no return predictions; (2) source + date on every number (on screen and caption);
(3) risks shown next to any upside; (4) "Education only, not investment advice" on the end card AND caption;
(5) general disclosure "I may hold some of these stocks" when naming stocks (never name actual holdings);
(6) no buy/sell calls.

## 4. Script
Create `$ST/<slug>/script.json`: a JSON list of 9 lines (scene 0 = hook, scene 8 = CTA end card, dark).
~70-85 s total. Write numbers in words for the voice ("thirty two percent"). Hook: a question or shock number in
line 0. End line: "Save this … and follow moneyincloud. Education only, not investment advice."
Voice: `mkdir -p $ST/<slug>/vo && cd $ST/kokoro && python3 vo.py ../<slug> <voice> <speed>` → prints durations.

## 5. Animation module (paper Vox template — light paper, NOT dark, NOT 3D)
Copy the working example `vox/lows.py` to `vox/<slug>.py` and change:
- `SH = ROOT + '<slug>/'`
- header label text (`'52-WEEK LOW CHECK'`) → your topic (short, caps)
- the scenes block between `STK = {` and the end of `def SLAMS()` → your 9 scene functions `s1..s9`,
  `SCENES = [...]`, `SLAMS()` (times for screen shake). Keep `dark = (i == 8)`.
Helpers: `place_text(c, text, font, size, colour, x, y, t, key, t0, mode='pop'|'slide'|'fade', rot=)`,
`words_line`, `slam(t,t0)->(scale,alpha)`, `stamp_c(text, colour, size, rot, seed)`, `card_box(w,h,SOFT)`,
`label(text, colour)`, `text_img(text, font, size, colour)`, `place(c, img, x, y, scale, rot, alpha)`,
`spark(c, pts, progress, colour, width)`, `follow_btn()`, easing `eback/eo/eio/prog/clamp`,
`at(i, 'phrase', offset)` = time the phrase is spoken in line i (phrase must exist in the script).
Fonts: anton, osw, osw5, mark, type, pf, pfi. Colours: INK RED GRN CREAM YEL NAVY BLUE GREY GOLD PINK TEAL ORG SOFT.
Canvas 1080x1920; keep content between y≈250 and y≈1750.
Check stills: `cd $ST/vox && MOD=<slug> python3 still.py <t1> <t2> ...` → `$ST/frames/still.jpg`; Read it; fix overlaps.

## 6. Audio
Copy `vox/lows_audio.py` → `vox/<slug>_audio.py`, change `import lows as F` → `import <slug> as F`,
`lows_mix.wav` → `<slug>_mix.wav`, and replace the custom SFX block (between `put(drum(3)` and `mix=vo+mus`)
with SFX timed to your scenes (whoosh, pop, tick, hit, ding, rumble, drum, horn, clink, clunk). Run it → "mix ok".

## 7. Hook thumbnail (centred sunburst)
Copy `vox/thumb_lows.py`. Themes: maroon night chai blue navy teal purple green.
Everything inside y 420–1500: title ~510 (`fit_text` 150), band ~665, art ~910 (`art_glow` scale 0.6–0.75),
tag ~1225, pill ~1430. Output `../out/<slug>_thumbnail.jpg`; check `$ST/frames/th.jpg` (3 crops: full, 3:4, square).

## 8. Render (≈25–35 min; run in background with a 2 h timeout and wait for it)
```
cd $ST/vox; (for k in 0 1; do python3 render_mod.py $k 2 SLUG & done; wait) && cd ../src && printf "file 'SLUG_part0.mp4'\nfile 'SLUG_part1.mp4'\n" > SLUG_list.txt && ffmpeg -y -loglevel error -loop 1 -t 0.5 -i ../out/SLUG_thumbnail.jpg -f lavfi -t 0.5 -i anullsrc=r=48000:cl=mono -vf "scale=1080:1920,fps=30,format=yuv420p" -c:v libx264 -crf 18 -preset veryfast -c:a pcm_s16le -ar 48000 -ac 1 SLUG_cover.mkv && ffmpeg -y -loglevel error -f concat -safe 0 -i SLUG_list.txt -c copy SLUG_vid.mp4 && ffmpeg -y -loglevel error -i SLUG_cover.mkv -i SLUG_vid.mp4 -i ../SLUG/SLUG_mix.wav -filter_complex "[1:v]fps=30,format=yuv420p[mv];[2:a]aresample=48000,aformat=channel_layouts=mono[ma];[0:v][0:a][mv][ma]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 22 -maxrate 7M -bufsize 14M -preset veryfast -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart ../out/SLUG_reel.mp4 && echo RENDERED
```
(The thumbnail is the first 0.5 s so it becomes the cover.)

## 9. Host + schedule
1. Copy `out/<slug>_reel.mp4` and `out/<slug>_thumbnail.jpg` to `/home/claude/reels/YYYY-MM-DD/` (post date),
   also commit the module/script files under `studio/`, push, then check
   `https://raw.githubusercontent.com/moneyincloud/reels/main/YYYY-MM-DD/<file>` returns 200.
2. Metricool `createScheduledPost`, blogId `7366187`, timezone `Asia/Calcutta`, providers instagram + youtube,
   media = raw mp4 URL, videoThumbnailUrl = raw jpg URL,
   `instagramData {type: REEL, showReelOnFeed: true, isAiGenerated: true}`,
   `youtubeData {title: "<hook title> #shorts", type: short, privacy: public, category: EDUCATION, madeForKids: false, isAiGeneratedContent: false, tags: [...]}`.
   Caption: primary keyword in the first line, short facts with sources + dates, "Education only, not investment advice.",
   3–5 hashtags incl. #moneyincloud.
3. Story ("master" story for the reel): a second `createScheduledPost` 15 min after the reel, provider instagram only,
   `instagramData {type: STORY, isAiGenerated: true}`, media = the raw thumbnail jpg URL, no text.
4. Always schedule at least 30 min ahead so the owner can review in the Metricool app.
