"""One-time: run on YOUR computer to get the YouTube refresh token for the auto-post agent.

  pip install google-auth-oauthlib
  python get_youtube_token.py client_secret.json

A browser opens; sign in with the Google account that owns the @moneyincloud YouTube channel and allow
"upload videos". The script prints YT_CLIENT_ID, YT_CLIENT_SECRET and YT_REFRESH_TOKEN: paste each into
GitHub -> repo Settings -> Secrets and variables -> Actions. Never paste them into a chat or commit them.
"""
import json, sys
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(sys.argv[1], ["https://www.googleapis.com/auth/youtube.upload"])
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
cs = json.load(open(sys.argv[1]))["installed"]
print("YT_CLIENT_ID     =", cs["client_id"])
print("YT_CLIENT_SECRET =", cs["client_secret"])
print("YT_REFRESH_TOKEN =", creds.refresh_token)
