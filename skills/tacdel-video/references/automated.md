# Automated mode: Claude Code makes the whole video

Read this when Claude Code runs a video end to end: experiment, script, voice, render, Shorts and
packaging, with no CapCut and no chat-Claude relay. Proven on two ~9-minute videos (an AI-agents-
with-money test and an AI-agent obstacle course, October 2026). The kickoff prompt is in
`templates/claude-code-prompts.md` ("New experiment video").

## Who does what

| Who | Does |
|---|---|
| Claude Code (the build machine) | research, PLAN.md, the experiment, scoring, script, fact check, voice through the ElevenLabs API, chapter pages, render, master, Shorts, captions, packaging text, thumbnail prompts, STATUS.md |
| Owner | writes BRIEF.md (or approves it), approves the script, picks the voice once, watches the MP4, makes the thumbnail in ChatGPT from the prompts, picks the title, uploads; music in CapCut only if wanted |

Stop and ask only before spending money beyond the plan, or anything irreversible. Everything
else: decide, write it down in STATUS.md, keep going.

## The project files

- **BRIEF.md** — the owner's standing rules for this video. Wins over everything, including CLAUDE.md.
  Title, style, money rules, the machine-sharing rules (prefix, ports), honesty rules.
- **STATUS.md** — starts with a block **"In plain English (updated <date time>)"**: phase X of 6,
  what's running (with the command to check it), what's next, what's needed from the owner.
  Updated after every step. "continue" from the owner means: read BRIEF, then STATUS, resume.
- **PLAN.md** — the experiment design and a simplification pass (what was cut and why).
- **CLAUDE.md** — the same rules in project form, so a fresh session loads them.
- **video/SCRIPT_vN.md** — every version kept; the header says what changed and why.
- **video/FACTCHECK.md** — every number and claim, its file, and the fixes.

## Phases

0. Research + PLAN.md + a fairness/leak report (can the subject cheat, did it see the answers).
1. **Pilot**: one agent, a handful of items, end to end including scoring. Fix what breaks.
2. Full runs, detached and resumable → `results/*.json`. Only complete runs are scored.
3. Findings + numbers sheet → script (story rules in `story.md`) → fact check → **owner approves**.
4. Voice + render → master MP4 (this file, "Voice" and "Render").
5. Packaging: titles, description with chapters, captions, Shorts, `SHORTS.md`, thumbnail prompts.
6. Owner uploads.

## Voice (the channel's final settings, picked 2026-10-26)

| Setting | Value |
|---|---|
| Endpoint | `POST /v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_192` (audio + character timings) |
| Voice | the owner's professional clone; id = `ELEVENLABS_VOICE_ID` in `~/.tacdel.env` (never commit it) |
| Model | `eleven_v4` |
| `voice_settings` | `{"stability": 0.69, "similarity_boost": 0.78, "speed": 0.93}` |
| Not sent | `style`, `use_speaker_boost` (eleven_v4 takes neither; clone strength can't be set through the API) |
| Takes | one generation per chapter, plain text: no SSML, no [tags], ⟦markers⟧ stripped |

- Reads ~170–175 words a minute (eleven_multilingual_v2 read the same text at ~149). Cost ~0.44
  credits per character: a ~1,450-word video is ~3,000 credits, plus a few hundred per re-take.
- Before the first full voicing of a new project, render a voice test of the cold open (the
  money-trust project compared two models as two MP4s with the same visuals) only if the owner
  wants to change the voice; otherwise use these settings unchanged so every video sounds the same.
- Check every take locally with Whisper (`tools/align.py`: "N/N words matched"). Re-voice only a
  chapter that fails (a swallowed word, a misread number, a line the fact check changed). Never
  re-generate to "try again" for taste: it spends credits.
- Takes come in quiet; the mix brings the voice to a 0.9 peak and the master is two-pass
  loudnorm to -14 LUFS integrated, true peak under -1 dBTP.
- Silent beats, the payoff lead before the hook, and muted lines are edits on the same take
  (`voice/edits.json`), never new generations.

## Render (no CapCut needed)

The chapter kit in `scripts/chapters/` (its README has the commands). In short:

1. An export step writes `video/chapters/data.js` from `results/`: every number and text on screen.
2. `voice_ch.py` → takes; `mute.py` → edits; `mkpage.py NN` → one HTML page per chapter.
3. `NN_scenes.js` per chapter: shots cued to spoken words (`cue('phrase')`), real footage in
   `win()` windows whenever the voice mentions it, `fakeLabel()` on every fake, sound effects
   made in code. Check each page (`check.cjs`) and look at a contact sheet (`sheet.cjs`) before
   rendering; check cut gaps with `stills.py`.
4. `build_all.sh` as a detached user unit → chapter MP4s (2 at a time, resumable) → master,
   `captions.srt`, `chapters.txt` → Shorts → cut check.
5. Look at frames of the finished master (`ffmpeg -ss T -frames:v 1`), not just the pages.

Music: none in the master. The owner adds a track in CapCut if they want one; the voice and
effects are already mixed and normalised.

## Shorts

Cut from the finished chapters by spoken phrases (`chapters/shorts.json`), 1080x1920, the wide
frame in the middle, a two-line hook on top that says only what the clip shows (shrunk to fit),
captions below, a "full video" end card. One Short should be the cold open's payoff from frame
0. Write `SHORTS.md` at the repo root: file, length, hook, the line it starts and ends on.

## Packaging

- `packaging/TITLES.md` (5–10 options, the question in the title), `description.txt` (hook, chapters
  from `chapters.txt`, what was tested, limits, credits), `captions.srt`.
- **Thumbnails: ChatGPT prompts only.** Write 2–3 prompts in `packaging/THUMBNAILS.md`
  from the template in `packaging.md` (one subject, one idea, three words or fewer, a tension
  not a label, the brand lettering and pill badge), each a different idea for Test & Compare.
  Claude Code never renders thumbnails itself. The owner makes them in ChatGPT; Claude Code
  checks any number or claim on them against the results when they're dropped into `thumbnails/`.

## Operating lessons

- **Fresh sessions.** Start each big step in a fresh session that reads BRIEF.md, then the plain-
  English block of STATUS.md. Keep command output short (`tail -3`, `head`); write long output to
  files and read summaries. One video per session family; never start a second.
- **Detached jobs.** Anything longer than a few minutes runs as a systemd user unit
  (`systemd-run --user --unit=<prefix>-name ...` or a unit file kept in the repo and linked into
  `~/.config/systemd/user`), with its PID in a file, resumable (skips finished work), so it
  survives the chat ending and the machine rebooting. An earlier batch started from a chat died
  when the chat closed; the machine also rebooted once mid-project.
- **PATH in services.** systemd's PATH has no `~/.local/bin`, so a bare `uv` fails: pass
  `-p Environment=PATH=$PATH` to systemd-run, or put `Environment=PATH=%h/.local/bin:/usr/local/bin:/usr/bin:/bin`
  in the unit. One queue crash-looped 78 times overnight on exactly this.
- **Waiting out usage limits.** A usage limit, a rate limit or a crashed model server is not the
  subject failing. The run exits with code 75 and writes `run.cut_off.json`, never a results row;
  the queue waits (30 min for a limit; 1 / 5 / 15 min retries for backend errors) and runs it
  again. When Claude Code itself hits a limit, the detached jobs keep going; the next session
  resumes from STATUS.md.
- **Sharing the machine.** Other sessions use the same machine and GPU. Only touch the project
  folder. Every container, unit, network and volume starts with the project's prefix (e.g. `amt-`,
  `aoc-`); each project gets its own 100-port block (7100-7199, 7200-7299, ... check `ss -ltn`
  first) written into BRIEF.md. Check GPU and memory before a heavy local run (`free -g`,
  `nvidia-smi`, Ollama `/api/ps`) and queue if someone else is busy. Never stop or kill what you
  didn't start; kill exact PIDs only, never `pkill -f`. No `docker prune` or system-wide cleanup.
- **No paid APIs except ElevenLabs.** Subjects run through the owner's existing logins (the
  `claude` and `codex` CLIs, in throwaway containers or with tools locked down) or local models
  (Ollama, llama.cpp). Never the OpenAI API, no new API keys. ElevenLabs is the only paid API.
- **Private repos.** The project repo is private before the first push; the push script checks
  visibility and refuses otherwise. Never change a repo's visibility, never publish. (This skill's
  own repo is public: no IPs, hostnames, user names, voice ids or home paths in anything copied here.)
- **Honesty.** Numbers only from results files, through the export step; the fact check runs on
  every script version before voicing. Cut-off runs are re-run, never scored. Pilot first.
