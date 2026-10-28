#!/bin/bash
# Re-time a finished page to another voice take, remix, render.
#   tools/retime.sh page.html voice.mp3 words.json chunks.txt out.mp4
# words.json = Scribe transcript of that exact take. Writes page_final.html next to the page.
set -euo pipefail
PAGE=$1; V=$2; WJ=$3; CH=$4; OUT=$5
HERE="$(cd "$(dirname "$0")" && pwd)"; SK="$HERE/../../tacdel-shorts/tools"
FIN="${PAGE%.html}_final.html"; cp "$PAGE" "$FIN"
python3 "$SK/timing.py" warp "$WJ" "$CH" "$FIN" --write
DUR=$(grep -oP '^const DUR = \K[\d.]+' "$FIN")
uv run "$HERE/sound.py" "$FIN" "${OUT%.mp4}.m4a" "$V"
node "$SK/render.cjs" "$FIN" "$OUT" "$DUR" "${OUT%.mp4}.m4a"
echo "done: $OUT ($DUR s)"
