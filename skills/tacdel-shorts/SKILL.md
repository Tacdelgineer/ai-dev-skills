---
name: tacdel-shorts
description: Make a finished vertical tacdel Short or Reel (about 45 s) from a trend item. Check the facts, write a ~110-word voiceover, voice it in one take of Alireza's ElevenLabs voice (eleven_v4), animate code-drawn scenes in one of four styles (riso, paper-cut, kinetic type, CRT terminal) timed to the words, and render a 1080x1920 MP4 with voice and captions, plus its post text (titles, thumbnails and extras only when asked). Shorts that report a real test get a real-terminal proof beat. Use for any new Short or Reel, for re-timing a Short to a new voice take, or for adding a new style.
---

# tacdel Shorts

One idea becomes one finished 9:16 video. The visuals are drawn in code, so they are original work
and every number on screen can be checked. A run takes one idea through eight steps. The files live in
`github.com/Tacdelgineer/ai-dev-skills` under `skills/tacdel-shorts/`. If that folder is not on disk,
attach and clone the repo first.

| Folder | What is in it |
|---|---|
| `styles/` | One finished Short per style (`riso`, `papercut`, `kinetic`, `crt`). Each is a single HTML file with a matching `.chunks.txt`. Copy the closest one to start. |
| `../tacdel-motion/tools/voice.py` | The voice: one `eleven_v4` take with the final settings and word timings, checked by `pick_take.py`. |
| `tools/timing.py` | Turns ElevenLabs word timings into captions, or re-times a finished Short to a new take. |
| `tools/sheet.cjs` | Makes one contact sheet of chosen moments, for checking layout. |
| `tools/render.cjs` | Renders a frame-exact 30 fps MP4, with the voice muxed in. |
| `references/muse-brief.md` | The brief that makes Muse's trend packs ready for this skill. |

The tools need Node with `playwright`, Python 3 and `ffmpeg`.

## Experiment Shorts: proof beat on by default

When the Short reports a test that was actually run (not a trend item read from a source), it gets the proof beat
from `tacdel-motion` ("Proof beat" in its SKILL.md): one 2–3 s real terminal shot of a real logged model answer,
filmed with VHS by `../tacdel-motion/tools/proof.sh`, placed where the result is revealed, plus the model names and
the run count on screen whenever results are shown. Paste `../tacdel-motion/tools/proof.js` into the page, then run
`proof.sh record` before the render and `proof.sh overlay` after it. Trend and story Shorts leave it off.

## Steps

1. **Pick and check.** Use primary sources only: the repo, the model card, the paper, the official post.
   Open each page. Build a fact table with these columns: value · what it compares (same model? which
   baseline?) · link · tag (third-party measured / vendor-reported / unverified). If a source gives no
   latency or cost number, write "not given" and never infer one. Check that the test can run on the
   DGX Spark (ARM64, 128 GB unified memory).
2. **Script.** Write about 110 words (100–120, ≈45 s at the v4 pace) in the first person, in short sentences. The result or surprise comes
   first. The last line is the payoff, the takeaway, or a short question to the viewer about this Short;
   never a tease of another post ("follow for part 2", "results next"). Never claim a result he doesn't have.
   Write numbers as words ("sixty-one point eight") and write no audio tags. Use
   `<break time="0.5s" />` at most twice. Then write `chunks.txt`: one caption chunk per line in the
   spoken words, with ` || shown text` added where the screen should show digits.
3. **Voice.** One take of "Alireza" on `eleven_v4` with the settings in `FINAL_VOICE.md` at the repo root
   (also inside this skill's zip): `{"stability": 0.69, "similarity_boost": 0.78, "speed": 0.93}`, sent with
   every request as written, no style, no speaker boost. Never Multilingual v2 or another v2 model.
   - With an API key (Claude Code): `python3 ../tacdel-motion/tools/voice.py script.txt <short dir>` makes the
     take, writes `voice.mp3` + `words.json` from the TTS alignment and checks it with `pick_take.py`. Re-voice
     only for a wrong, swallowed or garbled word, never for taste.
   - Without one: Alireza makes the one take on the ElevenLabs Text to Speech page with Eleven v4 and these
     settings and attaches the MP3. Don't voice through the connector's `creative_generate_speech`: it can't
     pass sliders and would use the voice's stored settings, which are left over from v2.
4. **Word timings.** `voice.py` already wrote `words.json`. For an attached take: get it onto a flow
   (`creative_create_asset_upload`, a PUT of the bytes, then `creative_finalize_asset_upload`), run
   `creative_transcribe_audio` on it (free), and download `words_download_url` with curl, plus the take's
   `content_url` as `voice.mp3`. Read neither into chat. Then run
   `python3 tools/timing.py caps words.json chunks.txt`, which prints `CAPS`. Each scene starts at the start
   of its chunk.
5. **Animate.** Copy the style file, then replace `CAPS`, `SCENES`, `DUR` and the scene functions. Keep
   the palette and helpers, the captions function and the player block. Key each animation to the
   start time of its cue word. Layout:
   - visuals between y 220 and 1380
   - the caption pill centered at y 1520
   - nothing that matters below y 1600 (app buttons)
   - a 90 px right margin
6. **Check.** Run `node tools/sheet.cjs page.html sheet.png <8–14 times>`, look at the one sheet and fix
   overlaps. At most one more sheet.
7. **Render.** Run `node tools/render.cjs page.html out.mp4 <DUR> voice.mp3`. To leave the voice out, put
   `-` where the MP3 goes. For a version without captions, add `nocaps` as a fifth argument. A 45 s Short
   takes about 10 minutes on 2 CPUs. Run at most 2 renders at once, and render only after the sheet is right.
8. **Deliver.** `NN_name.mp4` plus `NN_name.txt`: a post caption of 70 words or fewer with the same
   rounding as the voiceover, how it was tested, and 3 hashtags. Put the voiceover as recorded in your
   message. Nothing else unless asked: title options, thumbnails, a long description with links and new
   sound effects are extras. Keep the fact table in the Short's folder as a working file.

**Re-time a finished Short to a new take** (no scene edits): run
`python3 tools/timing.py warp words.json chunks.txt page.html --write`, then render again.

## Rules

- Numbers on screen come only from the fact table. Illustrations (receipts, tickets, meters, logs) carry no
  invented numbers, bars start at zero, and vendor numbers say "vendor-reported" on screen.
- Never tease, promote or advertise another Short or video, in the voice, on screen or in the caption
  ("next time...", "follow for the numbers", "subscribe to see..."). End on this Short's payoff.
- Compared things get equal visual weight: same size, same color. A label says who wins.
- Captions are white text on a dark pill, with no word-by-word animation.
- Example rules or data shown on screen are labelled as examples.
- Credits for the riso look: IshaanKalra2103's riso-rooms (MIT) and Kevin Ngo's "a small light, room by room".
- This repo is public. Put no voice ids, flow links, keys, hostnames or home paths in it.

## Styles

| File | Look | Good for |
|---|---|---|
| `riso.html` | black paper, white, orange and brick halftone, iso machines | hardware, chips, machines |
| `papercut.html` | cut paper, tape, yarn, ransom letters, 12 fps | a concept, costs, "receipts" |
| `kinetic.html` | the words are the visuals; black, paper and electric blue | model releases, number stories |
| `crt.html` | green phosphor terminal, scanlines, curved glass | tools, logs, CLI and dev stories |

Styles are still being tested. Compare "viewed vs. swiped away" per style in YouTube Studio after 48 hours,
then settle on one house look. To add a style, copy any example, swap its palette and helper section, and
keep the player and captions as they are.

## Long-form

Not covered yet. For 10-minute videos use the `tacdel-video` skill. Once a Shorts style wins, its scenes can
be laid out at 16:9 for long-form chapters.

## Wrap

Only when Alireza says "wrap <project>", never automatically: follow `WRAP.md` at the repo root (it ships
inside this skill's zip too) to archive the Short to the PC, verify the hashes, then wipe the scratch.
