#!/bin/sh
# External animation toolkits (owner request 28 Oct 2026). Run once per fresh session.
set -e
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
export PLAYWRIGHT_CHROME=$HYPERFRAMES_BROWSER_PATH
mkdir -p /home/claude/ext && cd /home/claude/ext
for r in heygen-com/hyperframes lemomo-ai/lemo-opuscar JohnHeibel/ClaudeAnimationBase; do
  d=${r#*/}; [ -d "$d" ] || GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 https://github.com/$r $d
done
(cd lemo-opuscar && npm i -s --ignore-scripts >/dev/null 2>&1 || true)
(cd ClaudeAnimationBase && npm i -s >/dev/null 2>&1 && npm i -s @fontsource/permanent-marker >/dev/null 2>&1 \
  && cp node_modules/@fontsource/permanent-marker/files/*latin-400-normal.woff2 fonts_pm.woff2 \
  && sed -i 's#<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Permanent+Marker&display=block">#<style>@font-face{font-family:"Permanent Marker";src:url(fonts_pm.woff2) format("woff2");font-display:block}</style>#' studio.html \
  && sed -i "s/{ waitUntil: 'networkidle0' }/{ waitUntil: 'load' }/" render.mjs) || true
npx -y hyperframes@latest --version >/dev/null 2>&1 || true
# Hypit (video cloning / SVML workflows): skill + executable
npx -y skills add hypit-ai/hypit -g -y >/dev/null 2>&1 || true
npm install --global @hypit/hypit >/dev/null 2>&1 || true
# Skill finder (skills.sh CLI + find-skills). Search needs skills.sh, which is blocked here; installing from GitHub works
npx -y skills add vercel-labs/skills --skill find-skills -g -y >/dev/null 2>&1 || true
# Dalal Street Skills (NSE/BSE analysis, paper trading only). Data needs query1/query2.finance.yahoo.com, nsearchives.nseindia.com, niftyindices.com, news.google.com allowed
npx -y skills add Adityaraj0421/dalal-street-skills -g -y >/dev/null 2>&1 || true
echo "ext ok · export HYPERFRAMES_BROWSER_PATH=$HYPERFRAMES_BROWSER_PATH PLAYWRIGHT_CHROME=$PLAYWRIGHT_CHROME"
