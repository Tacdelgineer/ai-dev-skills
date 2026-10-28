# Chapter kit: script → voice → finished master and Shorts, no editor

The render pipeline behind the automated videos (`references/automated.md`). Each chapter is one HTML canvas page
whose shots are cued to words of the real voice take; headless Chromium renders it frame by frame, ffmpeg lays the
real footage into its holes, mixes voice and code-made sound effects, and joins the chapters into a master at
-14 LUFS with captions, a chapter list and vertical Shorts.

Built from the tools of two finished videos (an AI-agents-with-money test and an AI-agent obstacle course) and the
riso / papercut / CRT looks of the tacdel-shorts skill. Tested end to end on the template (2026-10-27).

## Copy into a project

```bash
KIT=~/.claude/skills/tacdel-video/scripts/chapters
mkdir -p video && cp -r "$KIT"/{styles,tools} video/ && cp -r "$KIT"/template/* video/
printf 'video/results/\nvideo/work/\nvideo/logs/\nvideo/voice/raw/\n*.mp4\n*.wav\n' >> .gitignore
```

Needs: ffmpeg, node with Playwright (`NODE_PATH`, default `~/ai-dev-skills/node_modules`), `uv` (the tools that
need numpy/scipy/Pillow/faster-whisper run in throwaway `uv run --no-project --with …` environments), and the sibling
skills tacdel-shorts (`render.cjs`, `timing.py`) and tacdel-motion (`voice.py`, `sound.py`) under `TACDEL_SKILLS`
(default `~/ai-dev-skills/skills`). ElevenLabs keys come from the environment or `~/.tacdel.env`, never the repo.

## Files

| Path | What it is |
|---|---|
| `styles/core.js` | the player: word cues (`cue('phrase')`), `shot()`, `sfx()`, `clip()`, real-footage windows `win()`, `fakeLabel()`, `example()` tag, counter, recording slates, captions |
| `styles/riso.js` · `papercut.js` · `crt.js` | the three looks (`R`, `PC`, `CR`); scenes use their colour names only |
| `styles/fonts/` | Inter + JetBrains Mono latin subsets (SIL OFL 1.1, `LICENSES.txt`) |
| `template/` | a one-chapter sample: `SCRIPT.md`, `chapters/{chapters,video,shorts}.json`, `data.js`, `common.js`, `00_scenes.js`, `voice/edits.json` |
| `tools/kit.py` | shared paths and config (read by every Python tool) |
| `tools/voice_ch.py` | one ElevenLabs generation per chapter with the final settings, plus word timings; `--text-only` costs nothing |
| `tools/align.py` | word timings for any take (faster-whisper, local, no credits); its matched count doubles as a take check |
| `tools/mute.py` | applies `voice/edits.json` to the takes: payoff lead, silent beats, muted lines |
| `tools/mkpage.py` | builds `chapters/NN_name.html` from the take and `NN_scenes.js` |
| `tools/check.cjs` · `tools/sheet.cjs` | page errors and shot list · a contact sheet of frames at given seconds |
| `tools/sfx.py` | chapter mix: voice + synthesised effects, ducked |
| `tools/compose.py` | lays real clips into their holes (crop, burned label, last frame held), two-pass loudnorm |
| `tools/build.sh` · `tools/build_all.sh` | one chapter · every stale chapter 2 at a time, then master, Shorts and the cut check (resumable) |
| `tools/master.py` | `results/final/<slug>_master.mp4`, `voice_full.wav`, `captions.srt`, `chapters.txt`, `work/timeline.json` |
| `tools/shorts.py` | 1080x1920 Shorts cut from the chapter MP4s by spoken phrases, hook on top, captions, end card |
| `tools/stills.py` | lists every stretch with no cut longer than 6.2 s (real moving footage is allowed) |
| `tools/voice_watch.sh` · `tools/take.sh` | drop `NN_anything.wav` into `voice/drop/`: aligned, edited, page rebuilt, chapter rendered |
| `tools/el_check.py` | voice name and credits left; prints no keys or ids |

## Order of work

```bash
cd video
python3 tools/voice_ch.py --text-only          # voice/text/NN.txt from the script: check word counts first
python3 tools/voice_ch.py 00                   # one chapter, listen, then the rest (spends credits)
python3 tools/align.py voice/raw/00.mp3 voice/text/00.txt work/check00.json   # take check: N/N matched
python3 tools/mute.py && for n in 00 01; do python3 tools/mkpage.py $n; done
NODE_PATH=~/ai-dev-skills/node_modules node tools/check.cjs chapters/00_cold_open.html
NODE_PATH=~/ai-dev-skills/node_modules node tools/sheet.cjs chapters/00_cold_open.html work/s00.png 1 5 9 13
systemd-run --user --unit=<prefix>-render --working-directory=$PWD -p Environment=PATH=$PATH tools/build_all.sh
```

## Writing a chapter's scenes

- Every shot starts on a spoken word: `const K = { fake: cue('This page looks like') }; shot(K.fake, 'paper', 'name', (lt, t) => …)`.
  A cue that isn't in the take is a page error, so a changed script line fails loudly instead of drifting.
- Numbers and texts only from `chapters/data.js`, which the project's export step writes from `results/`. Never type one.
- Real footage: `win(t0, t1, 'split' | 'full' | 'pip', [{src, title, from, crop}], {title})` puts the run's own
  recording beside, over or instead of the shot; `'punch'` pushes in on the frame. Sources are 1280x720; narrow
  windows crop the centre 4:3. Sounds: `sfx(t, 'thunk' | 'whoosh' | 'swish' | 'tick' | 'paper' | 'tear' | …, gain)`.
- Fakes: call `fakeLabel(x, y)` in every shot that shows made-up content, outside the fake itself. Set the wording once
  in `common.js` (`FAKE_LABEL = 'FAKE NUMBERS · MADE UP FOR THIS TEST'`).
- The payoff goes before the first word: `"leads": {"00": 3.5}` in `voice/edits.json`, and a shot at 0.
- Re-cut without new credits: edit `voice/edits.json` (pauses, leads, mutes) or the scenes, then `build_all.sh`.
