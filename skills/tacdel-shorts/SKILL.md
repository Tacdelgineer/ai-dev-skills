---
name: tacdel-shorts
description: Make a finished vertical tacdel Short or Reel (about 45 s) from a trend item. Check the facts, write a ~100-word voiceover, voice it in Alireza's ElevenLabs voice, animate code-drawn scenes in one of four styles (riso, paper-cut, kinetic type, CRT terminal) timed to the words, and render a 1080x1920 MP4 with voice and captions. Use for any new Short or Reel, for re-timing a Short to a new voice take, or for adding a new style.
---

# tacdel Shorts

One idea becomes one finished 9:16 video. The visuals are drawn in code, so they are original work
and every number on screen can be checked. A run takes one idea through eight steps. The files live in
`github.com/Tacdelgineer/ai-dev-skills` under `skills/tacdel-shorts/`. If that folder is not on disk,
attach and clone the repo first.

| Folder | What is in it |
|---|---|
| `styles/` | One finished Short per style (`riso`, `papercut`, `kinetic`, `crt`). Each is a single HTML file with a matching `.chunks.txt`. Copy the closest one to start. |
| `tools/timing.py` | Turns ElevenLabs word timings into captions, or re-times a finished Short to a new take. |
| `tools/sheet.cjs` | Makes one contact sheet of chosen moments, for checking layout. |
| `tools/render.cjs` | Renders a frame-exact 30 fps MP4, with the voice muxed in. |
| `references/muse-brief.md` | The brief that makes Muse's trend packs ready for this skill. |

The tools need Node with `playwright`, Python 3 and `ffmpeg`.

## Steps

1. **Pick and check.** Use primary sources only: the repo, the model card, the paper, the official post.
   Open each page. Build a fact table with these columns: value · what it compares (same model? which
   baseline?) · link · tag (third-party measured / vendor-reported / unverified). If a source gives no
   latency or cost number, write "not given" and never infer one. Check that the test can run on the
   DGX Spark (ARM64, 128 GB unified memory).
2. **Script.** Write 95–110 words in the first person, in short sentences. The result or surprise comes
   first, and the last line is Alireza's own test as a cliffhanger. Never claim a result he doesn't have.
   Write numbers as words ("sixty-one point eight") and write no audio tags. Use
   `<break time="0.5s" />` at most twice. Then write `chunks.txt`: one caption chunk per line in the
   spoken words, with ` || shown text` added where the screen should show digits.
3. **Voice.** Voice "Alireza" (look up its id with `creative_list_voices`). Model: Multilingual v2.
   Settings: speed 1.0, stability 69%, similarity 78%, style exaggeration 24%.
   - The Claude ElevenLabs connector can set only the model and the voice, not those sliders. So
     Alireza makes the take on the ElevenLabs Text to Speech page with these settings and attaches the
     MP3.
   - Otherwise use the connector with the voice's saved defaults: `creative_create_flow`, then
     `creative_generate_speech`. Poll ONCE after about 20 s; the replies are long. Pin the take with
     `creative_add_flow_asset_node` and label it "Chosen take (synced to video)".
4. **Word timings.** Get the take onto a flow: an attached file goes through `creative_create_asset_upload`,
   a PUT of the bytes, then `creative_finalize_asset_upload`. Run `creative_transcribe_audio` on it
   (free). Download `words_download_url` with curl, plus the take's `content_url` as `voice.mp3`. Read
   neither into chat. Then run `python3 tools/timing.py caps words.json chunks.txt`, which prints `CAPS`.
   Each scene starts at the start of its chunk.
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
8. **Deliver.** Send the MP4 and the HTML. Notes: the title, the voiceover as recorded, the fact table with
   links, a post caption of 70 words or fewer with the same rounding as the voiceover, and 3 hashtags.
   Name the payoff post ("Part 2: I ran it") that the cliffhanger promises.

**Re-time a finished Short to a new take** (no scene edits): run
`python3 tools/timing.py warp words.json chunks.txt page.html --write`, then render again.

## Rules

- Numbers on screen come only from the fact table. Illustrations (receipts, tickets, meters, logs) carry no
  invented numbers, bars start at zero, and vendor numbers say "vendor-reported" on screen.
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
