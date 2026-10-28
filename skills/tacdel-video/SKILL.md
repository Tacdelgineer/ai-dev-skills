---
name: tacdel-video
description: The tacdel channel's workflow for turning a coding or AI experiment into a faceless YouTube explainer and its Shorts. Manual mode films code-drawn neon risograph rooms for a CapCut edit; automated mode has Claude Code run the experiment, write and fact-check the script, voice it through the ElevenLabs API and render the master and Shorts. Covers YouTube packaging too. Use whenever the user plans, builds visuals for, scripts, narrates, edits or publishes a YouTube video or Short, including "new video", "next video", "new experiment video", "turn this project into a video", story or script rewrites, voiceover or narration scripts, stat cards, B-roll, footage or chapter renders, gameplay overlays, thumbnails, titles, descriptions, chapters, click-through rate, or how to do something in CapCut. In Claude Code, also use it when building rooms or chapter pages, rendering footage, a master or Shorts, stat cards or charts for a video, or publishing the live page. Also use for "wrap PROJECT".
---

# tacdel video pipeline

Turn an experiment into a ~9–10 minute faceless explainer and its Shorts. Two modes:

| Mode | Who does what | Read |
|---|---|---|
| **Automated** (default for new experiment videos) | Claude Code does everything: experiment, script, fact check, voice through the ElevenLabs API, render, master, Shorts, packaging text. The owner approves the script, makes the thumbnail in ChatGPT from Claude Code's prompts, and uploads. No CapCut. | `references/automated.md`, kit in `scripts/chapters/` |
| **Manual** | Chat Claude (one claude.ai Project per video) plans and writes; Claude Code builds and renders rooms; the creator carries messages, voices in ElevenLabs, edits in CapCut, uploads. | the pipeline below |

## Which file to read

- Story rules, narration, fact check, ElevenLabs formatting → `references/story.md`
- What must be on screen while the voice talks; rooms, footage, stat cards, charts, live page → `references/visuals.md`
- Automated mode: roles, voice settings, render, Shorts, operating lessons → `references/automated.md`
- The chapter kit (word-cued pages, real-footage windows, fake label, voice tools, master, Shorts) → `scripts/chapters/README.md`
- Screen recordings, CapCut edit, loudness, export → `references/edit.md`
- Title, thumbnail prompts, description, chapters, CTR, README → `references/packaging.md`
- Ready-made Claude Code prompts, including the automated kickoff → `templates/claude-code-prompts.md`
- Manual-mode script format → `templates/script-template.md` (automated: `scripts/chapters/template/SCRIPT.md`)
- Archiving a finished project (only when the owner says "wrap <project>", never automatically) → `WRAP.md`
  at the repo root (it ships inside this skill's zip too)

## Manual pipeline, in order

1. **Idea and angle:** ride a trend; add the fair test everyone else skips.
2. **Chapter outline** (8–12 chapters): what each must show and prove.
3. **Build and run the experiment.** Logs and results files are the only source of numbers.
4. **Build the rooms** (one per idea, data-driven), publish the live page.
5. **Render footage** in chapter order with the naming contract, then lock it.
6. **Stat cards, charts, B-roll commands.**
7. **Write the script to the footage**, then **fact check** it against the files.
8. **Voice** (one chapter per generation), **screen recordings**, **CapCut edit**, loudness pass.
9. **Packaging and repo README**, then upload.

Naming contract (both agents rely on it): `results/final_footage/{wide,vertical}/NN_chapter_shot.mp4`
(1920x1080 / 1080x1920, 30 fps, H.264, same names), `results/final_footage/ORDER.txt`
(`NN | chapter | shot | one line | seconds`), stat cards `results/film-stats/S#_name_{wide,vertical}.mp4`,
charts `results/filmpack/*.png`. Footage and mp4s stay out of git.

## Hard rules (both modes)

1. **Numbers only come from logs and results files**, through one export step. No model types
   a number onto the screen, and every script version is fact-checked before any voice.
2. **Every claim needs a file behind it.** Prefer claims viewers can picture.
3. **Rounding matches** between the voice, the screen and the description.
4. **Compared groups get equal visual treatment**; each character keeps one colour all video.
5. **Script and picture match line by line.** Every line describes what's on screen, and the
   real thing (gameplay, logs, pages) is on screen whenever the voice mentions it. Manual mode
   writes the script after the footage is locked. Automated mode writes the script first, from
   the results, and builds every shot to the voice take, cued to a spoken word; a line with no
   picture gets a shot, a shot with no line gets cut.
6. **Payoff first:** the result is on screen in the first 5 seconds; the title lands after the
   cold open. The story rules in `story.md` apply to every first draft.
7. **Plain words, short sentences**, in the script and in every message to the owner.
8. **Fake content is labelled** in every shot it appears in; nothing real is ever bet or sent.
9. **Claude Code reports:** under 300 words, plain English, ending with what's needed next
   (manual mode: the exact copy commands).
10. **Repos:** automated projects stay private (the push script checks). Any public repo (this
    skill's, a manual project with a live page) has no IP addresses, hostnames, user names,
    keys, voice ids or home paths; use placeholders.
11. **Credit** borrowed styles, skills, data and libraries in the description and README.
12. **The live page (gh-pages) is published** only when the prompt explicitly allows it.

## Lessons

- hedgefly (manual): a script written before the rooms fought the footage; rewriting it as a
  tour cut 13 minutes to 9.5. The fact check caught four wrong claims. Once footage is locked,
  extra runtime comes from director-mode recordings, not new rooms.
- agent-money-trust and agent-obstacle-course (automated): the first drafts were correct and
  dull; the story rules cut 1,995 spoken words to 1,467 with the same facts (13:40 → 8:51, part
  of it a faster voice). The owner asked for the real games on screen and no still over ~6 s
  (24 clips → 150). Payoff-first opens and re-cuts came from editing the same takes, with no
  new voice credits.

## Output formats

- **Script:** chapters, each with a paste-ready **Voice** block, a **Shots** list and (automated)
  a **Check** line naming the file behind every number.
- **Claude Code prompts:** "Fresh session." header with scope limits, numbered steps with one
  job each, and a final REPORT step saying exactly what to report.
- **Replies to the owner:** short and plain, ending with the one next step.

## Credits

The visual style builds on the riso-rooms and hand-drawn-canvas-animation skills by
IshaanKalra2103 (MIT) and is inspired by Kevin Ngo's "a small light, room by room" and
"life of a fruit fly" (@kevin_t_ngo). Keep these credits in every video that uses the style.
