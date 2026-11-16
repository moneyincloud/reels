# How to schedule a post (no Metricool)

Every @moneyincloud post goes out through this folder: `post.py` on GitHub Actions posts approved
entries of `queue.yaml` to YouTube (Data API) and Instagram (Graph API). Owner's instruction,
16 Nov 2026: "all running through api youtube and instagram, not metricool".

## Steps
1. Copy the files into `autopost/media/` (public repo, so the raw GitHub URL is what Instagram fetches).
   Use descriptive, SEO-friendly file names. Video ≤ 100 MB (GitHub limit), H.264/AAC mp4.
2. Append one entry to the end of `autopost/queue.yaml` (format below). Strings containing ": " must be
   quoted; easiest is to write them as JSON strings. Check it parses:
   `python3 -c "import yaml; yaml.safe_load(open('autopost/queue.yaml'))"`.
3. Commit, `git pull --rebase`, push. Pushing queue.yaml starts the workflow; it also runs every 15 min.
   YouTube uploads at once (private + publishAt when the time is in the future); Instagram publishes on
   the first run at or after `publish_at` (never more than 6 h late).
4. Results land in `autopost/posted.json` under the entry id (permalinks, video ids). Read it after the
   run (`gh run watch <id> -R moneyincloud/reels`, then `git pull`) and report the links.

## Entry
```yaml
- id: <slug>-<YYYY-MM-DD>                # unique
  approved: true   # <who approved / which standing order, with date>
  publish_at: 2026-11-18 10:00           # IST, "YYYY-MM-DD HH:MM"
  platforms: [youtube, instagram, instagram_trial, instagram_story]
  video: <file>.mp4                      # in autopost/media
  cover: <file>-cover.jpg                # YouTube thumbnail + Instagram cover (3:4-safe 1080x1920)
  story: <file>-story.jpg                # needed for instagram_story (1080x1920)
  story_delay_min: 60                    # story goes up this long after publish_at
  ig_caption: |
    <caption, multi-line>
  first_comment: "<posted as the first comment on the Instagram reel>"
  yt_title: "<max 100 chars, ends with #shorts for a Short>"
  yt_description: |
    <description>
  yt_tags: ["tag one", "tag two"]
```
- Reels: use all four platforms (reel + trial reel + story + YouTube Short) unless told otherwise.
- **Carousel** (Instagram only): `platforms: [instagram]`, `images: [slide1.jpg, ...]` (2–10 files in
  media/, 1080x1350), plus `ig_caption` and optional `first_comment`; no `video`.
- **Long YouTube video** (16:9, not a Short): `platforms: [youtube]`, `yt_long: true`, title without #shorts.
- To cancel before it posts: delete the entry (or set `approved: false`) and push.
- No monthly post limit applies (the old Metricool free-plan 20/month cap is gone).
