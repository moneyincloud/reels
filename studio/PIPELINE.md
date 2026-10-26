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

## 0b. Posting plan — Metricool FREE plan (max 20 scheduled posts per calendar month)
A post to Instagram + YouTube together counts as ONE post. Stories and single-image posts are NOT scheduled
(they would use up the 20) — the owner shares each reel to his Story from the Instagram app (✈️ → "Add reel to your
story", which is clickable). Weekly plan (IST):
| Day | Time | Item | Agent |
|---|---|---|---|
| Mon | 10:00 | Reel → IG REEL + YouTube Short | Morning agent (runs 06:41 Mon & Wed) |
| Wed | 10:00 | Reel → IG REEL + YouTube Short | Morning agent |
| Fri | 16:00 | YouTube long video — weekly recap (YouTube only) | Weekly recap agent (11:23 Fri) |
| Fri | 18:00 | "Animal Friday" reel → IG REEL + YouTube Short | Animal Friday agent (13:37 Fri) |
| 1st Mon/Wed run of the month | 16:00 | ONE carousel (Instagram) | Morning agent |
≈ 13 reels + 4–5 weekly videos + 1 carousel ≈ 18–20 per month.
BUDGET CHECK (every agent, before scheduling anything): call getScheduledPosts for the whole current calendar month
(1st 00:00 → last day 23:59, all statuses: published, pending, error) and count the posts. Limit = 20.
If count + items you plan ≥ 20, drop items in this order until it fits: carousel first, then the reel.
Never schedule past the limit; report "Monthly Metricool limit reached (<n>/20)" in the final message.
Reel topics: Mon = today's market news (results, IPO, big movers) with real data; Wed = evergreen viral format
(myth vs fact, quiz, checklist, past maths, two-character story). Friday evening = Animal Friday: money lessons with
original paper-style animal characters (bull vs bear, tortoise vs hare = compounding, ant vs grasshopper = saving,
squirrel's emergency fund, sheep following the herd = FOMO, owl doing research, monkey overtrading, elephant staying
invested). Educational, real numbers only, no return promises.
Carousel: adapt `vox/carousel_lows.py` (7–8 slides, 1080x1350, cheat-sheet last slide with SAVE THIS), schedule as an
Instagram POST with all slide URLs in `media`. `vox/post_card.py` and `vox/story_card.py` stay available: put their
images in the final message so the owner can post them manually if he wants.

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
- **NO subtitles/captions** — the owner does not want on-screen subtitles. Captions are OFF by default (`CAPS_ON`);
  never turn them on unless the owner asks.
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
Layout: content between y≈170 and y≈1700.
Helpers: `place_text(c, text, font, size, colour, x, y, t, key, t0, mode='pop'|'slide'|'fade', rot=)`,
`words_line`, `slam(t,t0)->(scale,alpha)`, `stamp_c(text, colour, size, rot, seed)`, `card_box(w,h,SOFT)`,
`label(text, colour)`, `text_img(text, font, size, colour)`, `place(c, img, x, y, scale, rot, alpha)`,
`spark(c, pts, progress, colour, width)`, `follow_btn()`, easing `eback/eo/eio/prog/clamp`,
`at(i, 'phrase', offset)` = time the phrase is spoken in line i (phrase must exist in the script).
Fonts: anton, osw, osw5, mark, type, pf, pfi, ta (Tamil, use `text_ta()` for mixed text).
Colours: INK RED GRN CREAM YEL NAVY BLUE GREY GOLD PINK TEAL ORG SOFT.
Check stills: `cd $ST/vox && MOD=<slug> python3 still.py <t1> <t2> ...` → `$ST/frames/still.jpg`; Read it; fix overlaps
(especially labels vs captions).

## 5b. Save + share standards (MANDATORY in every reel — owner's standing request)
Helpers live in `vox/saveshare.py` (`import saveshare as SS`). Every reel must include:
1. **Cheat-sheet ending** — `SS.cheat_sheet()` freeze-frame summary in the last content scene (all key numbers on one
   screenshot-able card) with the bouncing bookmark "SAVE THIS".
2. **"Send this to…" frame** — `SS.send_frame(c, t, t0, who)` naming a specific person ("the friend who buys every dip",
   "your dad who only trusts FDs") with the flying paper plane; the voice says the same line.
3. **Myth vs Fact** — `SS.myth_fact()` paper-tear split screen whenever the topic has a common misconception.
4. Save/share icons pulse when the voice says "save" or "send" (`SS.save_pulse`, `SS.plane_icon`).
5. Spoken CTA names who to send it to, then "save this", then follow — not just "follow".
Recurring formats (use 2–3 times a week): **self-ticking checklist** (`SS.checklist`), **calculator / rolling number**
(`SS.roll_number` + `SS.coin_stack`, past or clearly illustrative maths only, never a return promise),
**quiz with countdown** (`SS.countdown_ring`, 3-second pause before the answer), **step ladder** (IPO in 4 steps),
**tear reveal** of a shock number (`SS.tear_reveal`), **two-character mini story** (panic seller vs patient investor).
SFX: pop on save, whoosh on the plane, ding per checklist tick, rip (whoosh + hit) on tears, beep per countdown second.
No subtitles. Keep everything compliant (section 3).

## 5c. Growth automation
- **First comment** on every reel: set `firstCommentText` in createScheduledPost to an engaging question
  (e.g. "Which stock should I break down next? 👇").
- **Results-day reels**: check the results calendar (INDmoney news "board meeting … results") — when a big company
  reports, prefer a "results explained in 60 seconds" reel that evening (facts from the filing/news, no buy/sell call).
- **Learn from the weekly report**: read `state.json` → `next_ideas` and `winning_patterns` (written by the weekly
  report) and prefer those topics/hook styles.

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
3. Story ("master" story for the reel): make the Story image with
   `python3 vox/story_card.py out/<slug>_thumbnail.jpg out/<slug>_story.jpg` (adds "NEW REEL · OUT NOW" and
   "TAP @moneyincloud TO WATCH"; Instagram's API cannot add clickable link stickers, so the Story points to the profile).
   Host it, then a second `createScheduledPost` 15 min after the reel, provider instagram only,
   `instagramData {type: STORY, isAiGenerated: true}`, media = the raw story jpg URL, no text, autoPublish true.
4. Always schedule at least 30 min ahead so the owner can review in the Metricool app.

## 10. Friday YouTube long video (weekly recap, YouTube only)
Every Friday the week's reels (Sat→Fri, 6–8 of them, ~8–10 min total) are compiled into ONE 16:9 YouTube video:
`python3 vox/weekly_compile.py plan.json` (see its docstring). It adds an intro card with a voice-over, a side panel per
part ("PART n/N", title, SAVE THIS / SUBSCRIBE, disclaimer), an outro, chapter timestamps (`<out>.chapters.txt`) and a
16:9 thumbnail (`<out>_thumbnail.jpg`). The mp4 is kept under ~95 MB so it can be hosted in this repo.
Pick the reels from the dated folders of the last 7 days (prefer *_v2_reel.mp4 over older versions; skip trial reels);
if fewer than 5 exist, include the strongest older reels. Order: best hook first.
Schedule with Metricool: provider youtube only, `youtubeData {type: "video", title: "This Week in the Indian Market
(<dates>): <top story> & more", category: EDUCATION, madeForKids: false, privacy: public, tags: [...]}`, media = raw mp4
URL, videoThumbnailUrl = raw thumbnail URL, text = description (2-line summary, the chapter list, sources, "Education
only, not investment advice."). Publish Friday 16:00 IST (YouTube peak).
