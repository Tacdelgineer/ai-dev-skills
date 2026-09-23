---
name: tacdel-video
description: The tacdel channel's end-to-end workflow for turning a coding or AI experiment into a faceless YouTube explainer — code-drawn neon risograph "rooms" rendered to footage, a narration script written to that footage, an ElevenLabs voiceover, a CapCut edit, and YouTube packaging (title, thumbnail prompt, description, chapters, Shorts). Use this whenever the user plans, builds visuals for, scripts, narrates, edits or publishes a YouTube video or Short — including "new video", "next video", "turn this project into a video", voiceover or narration scripts, stat cards, B-roll, footage renders, thumbnails, titles, descriptions, chapters, click-through rate, or how to do something in CapCut. In Claude Code, also use it whenever building rooms, rendering footage, stat cards or charts for a video, or publishing the live page.
---

# tacdel video pipeline

Turn an experiment into a ~10-minute faceless explainer video. The work is split
between two agents and the creator, who carries messages between them:

| Who | Where | Does |
|---|---|---|
| Chat Claude | claude.ai, one Project per video | plans the story, writes prompts for Claude Code, writes the script to the footage, packaging, reads Claude Code's reports |
| Claude Code | the build machine (e.g. a DGX Spark) | builds and runs the experiment, builds the rooms, renders footage, stat cards and charts, makes B-roll commands, fact-checks the script against the files, publishes the live page |
| Creator | Windows PC | ElevenLabs voice, screen recordings, CapCut edit, thumbnail in ChatGPT, upload |

The loop: chat writes a prompt → the creator pastes it into Claude Code → Claude Code
reports back → the creator pastes the report into chat.

## Which file to read

- Building rooms, rendering footage, stat cards, charts, the live page → `references/visuals.md`
- Writing the narration, fact check, ElevenLabs → `references/story.md`
- Screen recordings, CapCut edit, audio loudness, export, Shorts → `references/edit.md`
- Title, thumbnail, description, chapters, click-through rate, README → `references/packaging.md`
- Ready-made Claude Code prompt blocks → `templates/claude-code-prompts.md`
- The script file format → `templates/script-template.md`
- Reusable build code (renderer, starter room, stat-card template, director mode) → `scripts/`
  and `assets/`, listed at the end of `references/visuals.md`

Chat Claude mostly needs story, edit and packaging. Claude Code mostly needs visuals
and the naming contract below.

## The pipeline, in order

1. **Idea and angle.** Ride a trend fast. Add the test everyone else skips — in
   hedgefly it was fake flies with shuffled wiring. The fair test is often the story.
2. **Chapter outline** (8–12 chapters): what each chapter must show and prove. Not the script.
3. **Build and run the experiment.** The logs and results files are the only source of
   truth for numbers.
4. **Build the rooms** — one room per idea, driven by the data. Publish the live page.
5. **Render footage** in chapter order, using the naming contract. Then lock it: no new rooms.
6. **Stat cards, charts and B-roll commands.**
7. **Write the script to the footage** as a tour of the building. Never before step 5.
8. **Fact check.** Claude Code checks every number and claim in the script against the files.
9. **Voice** in ElevenLabs, one chapter per generation.
10. **Screen recordings:** terminal B-roll any time; director-mode fly-throughs after the
    voice exists, while listening to that chapter.
11. **CapCut edit**, following each chapter's Shots list.
12. **Loudness pass** with ffmpeg, then upload.
13. **Packaging:** title, two or three thumbnails for Test & Compare, description with
    chapters and credits, Shorts from the vertical renders.
14. **Repo:** README with a GIF, screenshots, the live link and the video link.

## The naming contract (both agents rely on this)

```
results/final_footage/wide/NN_chapter_shot.mp4        1920x1080, 30 fps, H.264
results/final_footage/vertical/NN_chapter_shot.mp4    1080x1920, same names
results/final_footage/ORDER.txt                        NN | chapter | shot | one-line description | seconds
results/film-stats/S#_name_wide.mp4 / _vertical.mp4    stat cards, ~6 s, number counts up then holds
results/filmpack/*.png                                 charts in the video's palette
```

- `NN` is the order clips appear in the video, and `chapter` matches the script's chapter
  names. That is what lets a Shots list say "→ 14 nursery" and the creator find the clip
  instantly in CapCut.
- Wide and vertical share names, so Shorts come almost free.
- Footage and mp4s stay out of git.

## Hard rules

1. **Numbers only come from logs and results files.** No model — chat Claude included —
   types a number onto the screen, and every script is fact-checked before recording.
2. **Every claim needs a file behind it.** Say "I ran the statistics" only if a saved test
   exists. Prefer claims viewers can picture ("the worst real one still beat the best fake one").
3. **Rounding matches** between the narration, the stat cards and the description.
4. **Compared groups get equal visual treatment** (same brightness, same size), so nothing
   looks like it's winning before it wins.
5. **Script after footage.** Every line describes what's on screen.
6. **Hook before the title card.** The title lands after the cold open.
7. **Plain words, short sentences.** Explain each term once, simply. The creator prefers
   plain English in every message, not only the script.
8. **Claude Code reports:** under 300 words, plain English, ending with exact copy commands.
9. **Public repos:** no IP addresses, hostnames, usernames, keys or home paths. Use placeholders.
10. **Credit** borrowed styles, skills, data and libraries in the description and README.
11. **The live page (gh-pages) is only published** when the prompt explicitly allows it.

## Output formats

- **Script:** `templates/script-template.md` — chapters, each with a paste-ready Voice
  block and a Shots list.
- **Claude Code prompts:** "Fresh session." header with scope limits, numbered steps with
  one job each, and a final REPORT step saying exactly what to report.
- **Replies to the creator:** short and plain, ending with the one next step.

## Lessons from hedgefly

- The first script was written before the rooms existed, so the narration fought the
  footage. Rewriting it as a tour of the building fixed that and cut 13 minutes to 9.5.
- Opening on the title card wasted the first seconds. Title after the hook.
- The fact check caught four wrong or unsupported claims. Always run it.
- A local model writing per-generation headlines was bland ("Real flies lead"). Fine as
  background texture, not worth featuring.
- Once footage is locked, extra runtime comes from director-mode recordings, not new rooms.

## Credits

The visual style builds on the riso-rooms and hand-drawn-canvas-animation skills by
IshaanKalra2103 (MIT) and is inspired by Kevin Ngo's "a small light, room by room" and
"life of a fruit fly" (@kevin_t_ngo). Keep these credits in every video that uses the style.
