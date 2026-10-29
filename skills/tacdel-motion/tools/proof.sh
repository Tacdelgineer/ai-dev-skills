#!/bin/bash
# Proof beat for experiment Shorts: a real terminal shot of one real logged model answer, at the reveal.
#
#   proof.sh record  <short dir> '<log key>' [answer.py options, e.g. --from WORD --lines 6]
#       Films answer.py printing that record from <short dir>/logs/calls.jsonl with VHS -> <short dir>/proof.mp4
#       (960x560, ~2.5-3.5 s: the command types in, the answer appears, it holds). Nothing is typed by hand.
#   proof.sh overlay <page.html> <render.mp4> <out.mp4>
#       Reads window.PROOF {t0, t1, x, y} from the page and lays proof.mp4 (next to the page) over the render,
#       frame-exact, from t0 to t1. Audio is copied. A page without PROOF is copied through unchanged.
#
# Needs vhs + ttyd on PATH (github.com/charmbracelet/vhs, github.com/tsl0922/ttyd), ffmpeg, node + playwright.
# VHS drives a headless Chromium. Where it can't find or download one (ARM64 Linux), this script puts a
# temporary `chromium` wrapper on PATH that runs Playwright's Chromium with --no-sandbox.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
case "${1:-}" in
record)
  D=$(cd "$2" && pwd); KEY=$3; shift 3
  OPTS=""; for o in "$@"; do case "$o" in *" "*) OPTS+=" '$o'";; *) OPTS+=" $o";; esac; done   # quote multi-word options
  cd "$D"; mkdir -p work logs
  if ! command -v chromium >/dev/null && ! command -v google-chrome >/dev/null; then
    C=$(ls -d "$HOME"/.cache/ms-playwright/chromium-*/chrome-linux*/chrome 2>/dev/null | tail -1 || true)
    if [ -n "$C" ]; then W=$(mktemp -d); printf '#!/bin/sh\nexec "%s" --no-sandbox "$@"\n' "$C" > "$W/chromium"; chmod +x "$W/chromium"; PATH="$W:$PATH"; fi
  fi
  cat > work/proof.tape <<TAPE
Output proof.mp4
Set Shell bash
Set FontSize 30
Set Width 960
Set Height 560
Set Padding 28
Set TypingSpeed 8ms
Set Theme { "name": "tacdel", "background": "#0b1026", "foreground": "#eef2ff", "cursor": "#5ef2c9", "selection": "#26356a", "black": "#0b1026", "red": "#ff5d6c", "green": "#5ef2c9", "yellow": "#ffcf4d", "blue": "#4f7dff", "magenta": "#a48cff", "cyan": "#5ec8e5", "white": "#eef2ff", "brightBlack": "#59617d", "brightRed": "#ff5d6c", "brightGreen": "#5ef2c9", "brightYellow": "#ffcf4d", "brightBlue": "#4f7dff", "brightMagenta": "#a48cff", "brightCyan": "#5ec8e5", "brightWhite": "#ffffff" }
Hide
Type "export PS1='\$ '; alias answer='python3 $HERE/answer.py'; clear"
Enter
Sleep 300ms
Show
Type "answer '$KEY'$OPTS"
Enter
Sleep 2.2s
TAPE
  vhs work/proof.tape > logs/proof.txt 2>&1 || { tail -3 logs/proof.txt; exit 1; }
  echo "proof.mp4: $(ffprobe -v error -show_entries format=duration -of csv=p=0 proof.mp4) s, $KEY$OPTS" ;;
overlay)
  PAGE=$2; IN=$3; OUT=$4; CLIP="$(dirname "$PAGE")/proof.mp4"
  P=$(node "$HERE/pageinfo.cjs" "$PAGE")
  if [ "$P" = "null" ] || [ ! -f "$CLIP" ]; then cp "$IN" "$OUT"; echo "no proof beat"; exit 0; fi
  read T0 T1 X Y < <(echo "$P" | python3 -c "import json,sys; p=json.load(sys.stdin); print(p['t0'], p['t1'], p['x'], p['y'])")
  ffmpeg -v error -y -i "$IN" -i "$CLIP" -filter_complex "[1:v]tpad=stop_mode=clone:stop_duration=10,setpts=PTS-STARTPTS+$T0/TB[p];[0:v][p]overlay=$X:$Y:enable='between(t,$T0,$T1)':eof_action=pass[v]" \
    -map "[v]" -map 0:a? -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"
  echo "proof beat $T0-$T1 s -> $OUT" ;;
*) sed -n 2,14p "$0"; exit 1 ;;
esac
