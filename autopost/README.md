# moneyincloud auto-post agent (Instagram + YouTube, no Metricool)

A free scheduler that runs on **GitHub Actions** in this repo. Every 15 minutes it reads
`queue.yaml`, and for each entry marked `approved: true`:

- **YouTube:** uploads it right away as *private*, with `publishAt` set to the slot, so YouTube releases it on time.
- **Instagram:** publishes the reel on the first run at or after its slot. Instagram's API can't schedule ahead.
- **Record:** writes what went out to `posted.json`, so nothing is ever posted twice.

Nothing is posted unless `approved: true`. Cost: ₹0 (GitHub Actions minutes for public repos are free).

## One-time setup (about 45 minutes, done by you, never share tokens in chat)

### 1. Instagram (Instagram API with Instagram Login)
1. The @moneyincloud account must be **Professional** (Creator or Business). It already is if Metricool posts to it.
2. Go to developers.facebook.com → **My Apps → Create app**. Choose the use case **"Manage messaging & content on Instagram"**.
3. In the app: **Instagram → API setup with Instagram login → Generate access tokens**. Add the @moneyincloud account and allow:
   - `instagram_business_basic`
   - `instagram_business_content_publish`
   - `instagram_business_manage_comments` (for the pinned first comment)
4. Copy the **long-lived access token** and the **Instagram user ID** shown there. The app can stay in Development mode, since it only posts to your own account.

### 2. YouTube (Data API v3)
1. Go to console.cloud.google.com → new project → **Enable "YouTube Data API v3"**.
2. Set up the **OAuth consent screen**: External, add your Gmail as a test user. Then go to **Credentials → Create OAuth client ID → Desktop app** and download `client_secret.json`.
3. On your laptop, run `pip install google-auth-oauthlib`, then `python autopost/get_youtube_token.py client_secret.json`. Sign in with the channel's Google account. It prints three values.
4. ⚠️ **Google's rule:** uploads from an API project that hasn't been audited stay **private** until the project passes the free YouTube API compliance audit (form: "YouTube API Services – Audit and Quota Extension"). Until then, YouTube uploads arrive as private and you switch them to public in YouTube Studio. You could also keep YouTube on Metricool's 20 free posts and use this agent for Instagram.
5. Custom thumbnails need a phone-verified channel (youtube.com/verify).
6. While the consent screen is in "Testing" status, the refresh token expires after 7 days. To stop that, set the consent screen's publishing status to **In production** (no review is needed for your own use).

### 3. GitHub secrets
Repo **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | From |
|---|---|
| `IG_USER_ID` | step 1.4 |
| `IG_ACCESS_TOKEN` | step 1.4 |
| `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` | step 2.3 |
| `GH_PAT` (optional) | github.com/settings/personal-access-tokens: a fine-grained token for this repo with **Secrets: read and write**. It lets `ig-token-refresh` renew the 60-day Instagram token by itself. |

Then go to **Actions → autopost → Run workflow**, tick **dry run**, and check the log.

## Adding a reel
1. Put `name.mp4` and `name-cover.jpg` in `autopost/media/`.
2. Add an entry to `queue.yaml` (copy an existing one), with `publish_at: "YYYY-MM-DD HH:MM"` in IST.
3. Set `approved: true` and push. Claude prepares the entries; **you** flip `approved` (or tell Claude "approve <id>").

## Notes
- **Repo must be public.** The video is fetched by Instagram from its public GitHub URL.
- **Late runs:** GitHub can start scheduled runs 5–20 minutes late. Instagram posts may land at 7:05–7:20 PM; YouTube stays exact.
- **Missed slots:** a reel more than 6 hours late is skipped, not posted at a strange hour. Re-date it.
- **Media clean-up:** after posting, delete old media from `autopost/media/` to keep the repo small.
