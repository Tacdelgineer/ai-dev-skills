---
name: tacdel-motion
description: Make a finished tacdel animated Short (50–60 s, 1080x1920) end to end from just an idea. You write a story script with soul starring Tac, the one-eyed robot, then generate Alireza's ElevenLabs voice and use its word timings. The animation is drawn in code in one of three looks (Riso 2.0, Living Simulation, Tiny AI Factory), with matched sound effects, an original code-composed score and burned-in captions. Delivers the MP4 plus titles, description and thumbnail. Use whenever Alireza gives a topic or idea for an animated explainer or story Short, or asks for "another one like the three episodes". Use tacdel-shorts instead for quick first-person trend/test Shorts.
---

# tacdel motion

Alireza gives an idea, and you deliver a finished, publishable Short. Do every step yourself, in order, and don't stop for approval between steps. In your first message, say the idea in one line and show the script, then keep going.

The files live in `github.com/Tacdelgineer/ai-dev-skills` under `skills/tacdel-motion/`. If that folder is not on main yet, it is on the branch `add-tacdel-motion-skill`. The skill reuses `skills/tacdel-shorts/tools/` for `timing.py` and `render.cjs`. If the folder is not on disk, attach and clone the repo.

| Path | What it is |
|---|---|
| `looks/riso2.html` | Finished Ep 1 "100 AI agents". Cream riso paper, cyan + orange halftone, morphing shapes, a crowd of 100 Tacs, ink wipes. Good for crowds, chaos and systems. |
| `looks/living.html` | Finished Ep 2 "Agent vs chatbot". Navy glow, bokeh, soft cards, a split screen that focuses then merges, Chat the speech-bubble creature. Good for comparisons and UI-like demos. |
| `looks/factory.html` | Finished Ep 3 "Why AI forgets". Pastel isometric factory outside and a workbench inside, with a dive through the door. Good for processes, pipelines and memory. |
| `looks/*.script.txt`, `*.chunks.txt` | The script and caption chunks each example was built from. |
| `tools/sound.py` | Mixer. It plays sound effects at the page's `CUES`, writes an original score from the page's `MUSIC` sections (one palette per look), ducks the music under the voice and outputs a loudness-normalised AAC. |
| `tools/sfx/*.mp3` | Sound-effect library made with ElevenLabs Sound Effects v2: stamp, stampede, paint, printer, whistle, pages, scratch, tada, drone, press, sizzle, conveyor, register, typing, drawer, buzzer. |
| `tools/voice.py` | Voice without the connector: 2 takes from the ElevenLabs API with word timings, then `pick_take.py`. Reads `ELEVENLABS_API_KEY` and `ELEVENLABS_VOICE_ID` from the environment, or from `~/.tacdel.env` when they're not set. |
| `tools/pick_take.py` | Picks the best of 4 voice takes without listening: transcript match, pace and longest pause. |
| `tools/grab.cjs` | Contact sheet with timestamps at any size (`node grab.cjs page out.png 300 6 t1 t2 …`). |
| `tools/still.cjs` | One clean 1080x1920 frame without captions, used for thumbnails. |
| `tools/est_words.py` | Estimated word timings, a fallback only when no voice can be made yet. |
| `tools/retime.sh` | Re-times a finished page to a different take, then remixes and renders. |
| `references/script-soul.md` | How the script must sound, with a before/after example. **Read it before writing.** |

Needs Node with `playwright` (`npm install` at the repo root, then `npx playwright install chromium`), Python 3 with numpy and scipy, and `ffmpeg`.

In Claude Code on a local machine:

- **Credentials:** keep `ELEVENLABS_API_KEY=` and `ELEVENLABS_VOICE_ID=` lines in `~/.tacdel.env` (chmod 600, outside every repo). The shell profile loads it (`set -a; . ~/.tacdel.env; set +a`), and `voice.py` reads it directly when the variables are missing, for example in non-interactive shells.
- **Ollama for experiments:** set `OLLAMA_HOST` to `<address>:11434` in the shell profile when Ollama listens only on a Tailscale address rather than localhost. Experiment scripts call `http://$OLLAMA_HOST/api/...` with an MoE model such as `qwen3.6:35b-a3b`. Run a tiny pilot first, then the full run as a plain script that writes a small results file.

## One-time setup: the voice settings

Alireza's settings are speed 1.0, stability 69%, similarity 78% and style 24%, on Eleven Multilingual v2. The Claude ElevenLabs connector can't pass sliders. ElevenLabs uses a voice's *stored* settings whenever a request passes none, so store them on the voice once with the API (`POST /v1/voices/{voice_id}/settings/edit`, body `{"stability":0.69,"similarity_boost":0.78,"style":0.24,"speed":1.0,"use_speaker_boost":true}`).

To check they took effect, read them back with `GET /v1/voices/{voice_id}/settings` (read-only, no credits). Pace is only a rough check, and only on a full 130–150-word script with sentence breaks. At speed 1.0 expect about 150–170 wpm. That range is measured, not estimated: three full Shorts made at speed 1.0 on Oct 21, 2026 ran 154–168 wpm. A one-sentence test has no pauses and runs around 200 wpm, which is expected, not a failure. If a full script runs far above the range, read the stored settings back before shipping and say what you found in the delivery. Never pretend the settings were applied, and never swap to another voice.

## Steps

1. **Facts.** Use primary sources only, and open each page. Build a fact table with these columns: value · what it compares · link · tag (measured / vendor-reported / example). Put at most 1–2 real numbers on screen. A vendor number is said and shown as theirs, for their system. Label demo data on screen as EXAMPLE or DEMO.
2. **Script.** Follow `references/script-soul.md`: 130–150 words, Tac (or "you") wants something, one specific detail per beat, no template phrases, one gut-punch, varied rhythm, an ending that's a feeling or a callback, never a tease of another episode or video ("next time...", "follow for part 2", "subscribe to see..."). Write numbers as words. Use `<break time="0.6s" />` at most twice and no other tags. Then write `chunks.txt`: one caption chunk of 2–6 spoken words per line, adding ` || shown text` where the screen should show digits.
3. **Storyboard.** 12–16 shots, with the picture changing every 2–4 s. Each shot has a beginning, an escalating problem, a turn and a payoff. Map every shot to the caption chunk that starts it. Pick the look whose example is closest.
4. **Voice first.** Make the voice before you animate, so the animation is timed to the real words.
   - `creative_create_flow`, then `creative_generate_speech`: voice "Alireza" (id from `creative_list_voices`), model `eleven_multilingual_v2`, the script as the prompt, default 4 takes.
   - Poll `creative_get_flow_run_status` once after about 20 s with all session ids. The reply is long; read only the URLs.
   - curl every take's `content_url` to `take1..4.mp3`.
   - For each take, run `creative_add_flow_asset_node` (its generation_id), then `creative_transcribe_audio` (`eleven_scribe_v1`, connect_from that node). Poll once, then curl each `words_download_url` to `take1..4.words.json`.
   - Run `python3 tools/pick_take.py script.txt take*.words.json`. Keep the winner as `voice.mp3` + `words.json`. Pin it on the flow with `creative_add_flow_asset_node`, labelled "Chosen take (synced to video)", so Alireza can hear it.
   - If `pick_take.py`'s pace warning fires on a full script, read the stored settings back and say what you found. Ignore it on a one-sentence test.
   - **With an API key instead of the connector** (Claude Code): `python3 tools/voice.py script.txt <episode dir>` replaces the bullets above. It makes 2 takes on the stored settings, takes word timings from the TTS alignment instead of Scribe, runs `pick_take.py` and leaves `voice.mp3` + `words.json`. Keep keys and voice ids in the environment or `~/.tacdel.env`, never in the repo.
5. **Timing.** Run `python3 ../tacdel-shorts/tools/timing.py caps words.json chunks.txt` to get `CAPS`. Set `DUR` = last end + about 1.6 s, and `PAGE_END` = the same number.
6. **Animate.** Copy the closest `looks/*.html` and keep its helpers, Tac, captions function, player block, `WARP`/`warp`, `PAGE_END`, `LOOK`, the `?pending` tag and `Object.assign(window, …)`. Replace `CAPS`, `DUR`, the scene functions, `CUES` and `MUSIC`. Key every move to `S(k)` (start of chunk k), `E(k)` or `M(k, f)`.
   - Frame 0 is the hook: the title and Tac are fully visible, with no fade-in.
   - Every physical action gets a cue (`cue(t, name, gain, rate, offset, length)`).
   - `MUSIC` is `[[t, section], …, [PAGE_END, 'end']]`, using the section names of that look in `tools/sound.py` (add sections there if needed). Cut the music on the gut-punch.
7. **Check.** Run `node tools/grab.cjs page.html sheet.png 300 6 <12–18 times>` and look at it. Fix overlaps, clipped text and empty stretches. Check the transitions too. Do at most two more rounds.
8. **Sound.** Run `python3 tools/sound.py page.html mix.m4a voice.mp3` (it ends at -14 LUFS).
   - You only need a new ElevenLabs effect when the library and the synth names can't cover an action. Use `creative_generate_in_flow`, `node_type: sfx`, `eleven_text_to_sound_v2` (about 17 credits per take). Poll with one session id per effect, save it as `tools/sfx/<name>.mp3`, and add it to the repo.
   - Synth names: pop, tick, click, key, whoosh, swish, wipe, thunk, ding, coin, sparkle, chime, blip, wink, riser, freeze, roll, splat, boing, whirr, beep, ping, radar, alarm, steam, hum, lock, spin.
9. **Render.** Run `node ../tacdel-shorts/tools/render.cjs page.html out.mp4 <DUR> mix.m4a`. Then:
   - check `ffprobe` duration and loudness (`ffmpeg -af ebur128`);
   - pull 3 frames from the MP4.

   Renders take 3–10 min (crowd scenes are the slowest). Run at most 2 at once and start them in the background.
10. **Deliver.** Send the MP4, a thumbnail frame (`tools/still.cjs`), 3 title options, a description with source links and the demo disclaimer, a thumbnail concept and the voiceover text. Save the production notes to the Claude Motion project. If anything is temporary (estimated timing, missing voice), name the file `_REVIEW` and add `?pending` to the render so the tag shows on screen.

To swap in a different take later, run `tools/retime.sh page.html voice.mp3 words.json chunks.txt out.mp4`.

## Tac: the same robot in every look

- **Proportions:** unit = body width.
  - Body: superellipse `superE(.5, .44, 3.4)`.
  - Legs: rounded rects at x -.29 and .12, y .34, .17 × .24.
  - Antenna: from y -.42 to -.6, topped by an **orange ball** r .08.
  - **One eye:** at y -.04, r .25, with an **orange ring** of width .07. Pupil r .105 follows `lx`/`ly`, with a small highlight.
- **Colour:** the body is always cyan; only the rendering changes. In Riso it's flat multiply ink with a halftone shadow. In Living it's a gradient with glow. In the Factory it's a soft pastel gradient.
- **Moods:**
  - `happy`/`wink`: a ^ arc instead of the eye
  - `squint`
  - `blink`
  - `palm`: facepalm
  - `thumbs`
  - `cap`: manager
  - `belt`: tools
  - plus props (magnifier, roller, book)
- **Sidekick:** Chat, a lilac speech-bubble creature with two eyes, plays any "plain chatbot".

## Rules

- **Layout:**
  - Visuals stay between y 220 and 1380.
  - The caption pill is centred at y 1520, white text on a dark pill, with no word-by-word animation.
  - Nothing that matters goes below y 1600.
  - Keep a 90 px right margin.
  - Iso scenes must fit 1080 wide, so compute the corner extents.
- **Honesty:**
  - Numbers on screen come only from the fact table. Bars start at zero, and compared things get equal visual weight.
  - Illustrations carry no invented numbers. Use $$ vs $$$$, not prices.
  - Fictional demos are labelled as such.
- **Credits:** the riso look credits IshaanKalra2103's riso-rooms (MIT) and Kevin Ngo's "a small light, room by room". The music is original, composed in code; no third-party tracks.
- **This repo is public.** Put no voice ids, flow links, keys or home paths in it.

## Pitfalls already hit

- In riso, anything drawn with `multiply` can't be lighter than what's under it. Draw paper-coloured text, eyes and highlights with `source-over`.
- Small figures on a painted or coloured area need a paper halo.
- `DUR` is rewritten when a page is re-timed. Use `PAGE_END` for every page-time decision: the end fade, end cues and the last `MUSIC` mark.
- Rows of labels collide easily (tools, permission switches, time slots, phones). Give each row its own y band.
- Don't `pkill -f` a pattern that also appears in the same shell command; it kills the shell.
- Poll ElevenLabs with as few session ids as you need. Each generation repeats its long signed URL three times.
- Credits:
  - A 4-take voiceover costs about 1 credit per character per take, so about 3,200 credits for a 150-word script.
  - Transcription is free.
  - A sound effect costs about 17 credits per take.
