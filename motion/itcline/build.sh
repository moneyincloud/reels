#!/bin/sh
# one-command build: voice must exist in ../../studio/itcline/vo (python3 studio/kokoro/vo_words.py studio/itcline)
set -e; cd "$(dirname "$0")"
python3 build/make.py ../../studio/itcline && python3 build/audio.py ../../studio/itcline
HYPERFRAMES_BROWSER_PATH=${HYPERFRAMES_BROWSER_PATH:-/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell} npx --yes hyperframes@0.9.41 render -o ../../studio/out/itcline_raw.mp4 -q delivery -w 2
