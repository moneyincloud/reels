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

### 4b. Hook + caption tools (from Jakeschincariol/instagram-agent-skill, MIT, offline)
- Write 3 hook options for line 0, save one per line to a file, run
  `python3 -I $ST/ig-skills/ig-reel/hookscore.py hooks.txt` and use the top one (must score 50+, rewrite if not).
- Time the script: `python3 -I $ST/ig-skills/ig-reel/beats.py script.txt --target 75` (one line per beat).
- Lint the caption: `python3 -I $ST/ig-skills/ig-caption/caption.py caption.txt --keywords "<primary keyword>"`;
  the first 125 characters must carry the hook + keyword.
- Caption/script de-slop: `python3 -I $ST/ig-skills/ig-human/humanize.py <file>` is fine for wording, but ALWAYS
  keep the AI-content labels (isAiGenerated) and the compliance lines; never use it to hide that content is AI-made.
- Other playbooks in `ig-skills/*/SKILL.md` (ig-story, ig-carousel, ig-reply, ig-plan, ig-audit) can be read when useful.

## 5. Animation module (paper Vox template v2 — light paper, NOT dark, NOT 3D)
Copy the reference template `vox/lows2.py` to `vox/<slug>.py`. It already contains every standard upgrade —
keep them in every reel:
- **Word-by-word captions** (bottom, y≈1665, current word yellow) — automatic from the script (`captions()`).
- **Progress bar** in the header rule — automatic.
- **Loop ending** — last 0.6 s cross-fades back to the hook frame; end the script with a line that echoes the hook.
- **Real charts** — fetch weekly closes with `get_indian_stocks_ohlc(interval=1week, lookback=1y)` (or 1day/14d for
  very recent moves), save to `$ST/<slug>/closes.json`, draw with `chart_pts()` + `spark()`. Never draw fake data
  shaped like a chart; if a chart is illustrative, label it "illustration".
- **Number counters** — values tick along the chart tip / count down to the final number (see `low_card`, `s2`).
- **Part markers** ("1/5") when the reel is a list.
- **Icons** — simple drawn icons per company/topic (`icon()`); never real company logos.
Change in your copy: `SH` default dir (`os.environ.get('LDIR', '<slug>')`), `CLOSES` path, header label text,
`STK`/`ORDER`/`TA`, and the scene functions `s1..s9`, `SCENES`, `SLAMS()`. Keep `dark = (i == 8)`.
Layout: content between y≈170 and y≈1500 (captions own 1600–1720). Keep reasons/labels above y≈1500.
Helpers: `place_text(c, text, font, size, colour, x, y, t, key, t0, mode='pop'|'slide'|'fade', rot=)`,
`words_line`, `slam(t,t0)->(scale,alpha)`, `stamp_c(text, colour, size, rot, seed)`, `card_box(w,h,SOFT)`,
`label(text, colour)`, `text_img(text, font, size, colour)`, `place(c, img, x, y, scale, rot, alpha)`,
`spark(c, pts, progress, colour, width)`, `follow_btn()`, easing `eback/eo/eio/prog/clamp`,
`at(i, 'phrase', offset)` = time the phrase is spoken in line i (phrase must exist in the script).
Fonts: anton, osw, osw5, mark, type, pf, pfi, ta (Tamil, use `text_ta()` for mixed text).
Colours: INK RED GRN CREAM YEL NAVY BLUE GREY GOLD PINK TEAL ORG SOFT.
Check stills: `cd $ST/vox && MOD=<slug> python3 still.py <t1> <t2> ...` → `$ST/frames/still.jpg`; Read it; fix overlaps
(especially labels vs captions).

## 6. Audio
Copy `vox/lows2_audio.py` → `vox/<slug>_audio.py` and run `python3 <slug>_audio.py <slug>` (writes `$ST/<slug>/mix.wav`).
Replace the custom SFX block (between `put(drum(3)` and `mix=vo+mus`) with SFX timed to your scenes:
whoosh, pop, tick, hit, ding, rumble, drum, horn, clink, clunk, riser (before a big reveal), beep (counters),
kaching (money moments). Music bed ducks under the voice automatically. Run it → "mix ok".
In the render command (section 8) use `../SLUG/mix.wav` as the audio path.

## 6b. Optional extras (do them when there is time)
- **Hook B trial reel**: a second script folder with a different line 0, module `<slug>b.py` =
  `import os; os.environ['LDIR']='<slug>b'; from <slug> import *`, render it, schedule as Instagram
  `TRIAL_REEL` (instagram only) 30 min after the main reel.
- **Tamil-subtitle version**: fill `TA` (one Tamil line per script line), module `<slug>ta.py` =
  `import os; os.environ['CAP']='ta'; os.environ['LDIR']='<slug>'; from <slug> import *`; render; post to YouTube
  only (or keep for the owner's Tamil channel).
- **Carousel**: adapt `vox/carousel_lows.py` (7 slides, 1080x1350) and schedule as an Instagram POST with all slide
  URLs in `media`, the next day at 13:00.

## 7. Hook thumbnail (centred sunburst)
Copy `vox/thumb_lows.py`. Themes: maroon night chai blue navy teal purple green.
Everything inside y 420–1500: title ~510 (`fit_text` 150), band ~665, art ~910 (`art_glow` scale 0.6–0.75),
tag ~1225, pill ~1430. Output `../out/<slug>_thumbnail.jpg`; check `$ST/frames/th.jpg` (3 crops: full, 3:4, square).

## 8. Render (≈25–35 min; run in background with a 2 h timeout and wait for it)
```
cd $ST/vox; (for k in 0 1; do python3 render_mod.py $k 2 SLUG & done; wait) && cd ../src && printf "file 'SLUG_part0.mp4'\nfile 'SLUG_part1.mp4'\n" > SLUG_list.txt && ffmpeg -y -loglevel error -loop 1 -t 0.5 -i ../out/SLUG_thumbnail.jpg -f lavfi -t 0.5 -i anullsrc=r=48000:cl=mono -vf "scale=1080:1920,fps=30,format=yuv420p" -c:v libx264 -crf 18 -preset veryfast -c:a pcm_s16le -ar 48000 -ac 1 SLUG_cover.mkv && ffmpeg -y -loglevel error -f concat -safe 0 -i SLUG_list.txt -c copy SLUG_vid.mp4 && ffmpeg -y -loglevel error -i SLUG_cover.mkv -i SLUG_vid.mp4 -i ../SLUG/mix.wav -filter_complex "[1:v]fps=30,format=yuv420p[mv];[2:a]aresample=48000,aformat=channel_layouts=mono[ma];[0:v][0:a][mv][ma]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 22 -maxrate 7M -bufsize 14M -preset veryfast -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart ../out/SLUG_reel.mp4 && echo RENDERED
```
(The thumbnail is the first 0.5 s so it becomes the cover.) GitHub rejects files over 100 MB: if the mp4 is larger, re-encode with -crf 26.

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
