#!/usr/bin/env bash
# One-time setup for a fresh session. Run from anywhere: bash studio/setup.sh
set -e
D="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$D/out" "$D/src" "$D/frames"
pip install -q --break-system-packages kokoro-onnx soundfile numpy pillow >/dev/null 2>&1 || pip install -q kokoro-onnx soundfile numpy pillow
cd "$D/kokoro"
[ -f kokoro-v1.0.onnx ] || curl -sSL -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f voices-v1.0.bin ] || curl -sSL -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
which ffmpeg >/dev/null || (apt-get install -y -qq ffmpeg >/dev/null 2>&1 || true)
echo "studio ready: $D"
