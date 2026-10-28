#!/usr/bin/env bash
# Check every skill's frontmatter (description present, at most 1,024 characters, no < or >), then zip
# skills into dist/ for upload to claude.ai.
# The tacdel-* zips also get the repo's FINAL_VOICE.md (the one voice setup) and WRAP.md (the end-of-video
# archive step) inside the skill folder.
#   scripts/build.sh               zip every skill
#   scripts/build.sh tacdel-video  zip only the named skills
set -euo pipefail
cd "$(dirname "$0")/.."

python3 scripts/check_skills.py

mkdir -p dist
skills=("$@")
[ ${#skills[@]} -eq 0 ] && skills=($(ls skills))
cd skills
for s in "${skills[@]}"; do
  [ -f "$s/SKILL.md" ] || { echo "no skill named $s" >&2; exit 1; }
  rm -f "../dist/$s.zip"
  zip -qr -X "../dist/$s.zip" "$s" -x '*/__pycache__/*' '*/node_modules/*'
  if [[ $s == tacdel-* ]]; then
    tmp=$(mktemp -d); mkdir "$tmp/$s"; cp ../FINAL_VOICE.md ../WRAP.md "$tmp/$s/"
    (cd "$tmp" && zip -q -X "$OLDPWD/../dist/$s.zip" "$s/FINAL_VOICE.md" "$s/WRAP.md"); rm -r "$tmp"
  fi
  echo "built dist/$s.zip ($(stat -c %s "../dist/$s.zip") bytes)"
done
