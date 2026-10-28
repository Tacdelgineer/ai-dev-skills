# Claude Code prompt blocks

Chat Claude assembles prompts from these blocks. Always start with the header and end
with a REPORT step. Fill in the [brackets]. Keep each step to one job.

## New experiment video (automated mode kickoff)

One prompt that starts a whole video in automated mode (`references/automated.md`). Paste it
into a fresh Claude Code session on the build machine; after that, "continue" resumes it.

```
Fresh session. New tacdel video, fully automated: you run the experiment, write the script,
voice it, render the master and the Shorts, and package it. Use the tacdel-video skill: read
SKILL.md, references/automated.md, references/story.md and references/visuals.md first.

THE VIDEO: "[title as a question]". [2-3 sentences: what's tested, on which subjects, and the
twist nobody else tests.] Style: riso / papercut / terminal, 9-10 minutes.

1. SET UP: create ~/[project] (git init; private GitHub repo Tacdelgineer/[project] over the
   github-tacdel SSH alias; push only through a tools/push.sh that refuses if the repo isn't
   private). Write BRIEF.md with these standing rules (they win over everything), CLAUDE.md
   with the same rules, and STATUS.md with a plain-English block at the top (phase X of 6,
   what's running and how to check it, what's next, what you need from me), updated after
   every step. "continue" means: read BRIEF.md, then STATUS.md, and resume.
2. RULES for BRIEF.md:
   - Money: no paid APIs, never the OpenAI API. Subjects run only through my existing logins
     (claude and codex CLIs) or local models. ElevenLabs is the only paid API.
   - Sharing the machine: only touch ~/[project]. Every container, unit, network and volume
     starts with "[pfx]-"; ports [7N00-7N99] only (check they're free). Check GPU and memory
     before local runs; queue if someone else is busy. Never stop or kill anything you didn't
     start; exact PIDs only, never pkill -f; no docker prune.
   - Jobs: anything longer than a few minutes runs detached as a systemd user unit with
     PATH set (Environment=PATH=%h/.local/bin:/usr/local/bin:/usr/bin:/bin), its PID in a
     file, resumable, so it survives this chat ending and a reboot. A usage limit, rate limit
     or crashed model server is not the subject failing: exit 75, write a cut-off file, wait
     it out and re-run; never write a result row for it.
   - Honesty: numbers only from results files, through one export step; never typed by you
     or a model. Fact-check every script version against the files before any voice.
   - Working style: keep command output short (tail/head), long output to files. Python with
     uv only.
3. PLAN (phase 0): research, PLAN.md with a simplification pass, and a fairness report (can a
   subject see the answers or cheat?). Then a PILOT (phase 1): one subject, a few items, end
   to end including scoring. Then the FULL RUNS (phase 2), detached.
4. SCRIPT (phase 3): from results only, in video/SCRIPT_v1.md (Voice / Shots / Check per
   chapter), applying every story rule in references/story.md: payoff in the first 5 seconds
   (and on screen before the first word); one concrete moment told slowly, then zoom out; say
   why it matters in the first minute; main cast of at most 3 plus a yardstick, the rest are
   "the rest"; one idea at a time, right before it's needed; numbers on screen, not in the
   voice; character arcs and callbacks; 2-3 practical takeaways tied to moments in the video;
   end on the payoff, the takeaway or a short question about this video, never a tease of
   another video. ~1,400-1,500 spoken words. Fact check into
   video/FACTCHECK.md. Then STOP and ask me to approve the script.
5. VOICE + RENDER (phase 4, after my approval): copy scripts/chapters/ from the skill into
   video/. Voice each chapter once through the ElevenLabs API with the settings in
   references/automated.md (eleven_v4, stability .69, similarity .78, speed .93; creds from
   ~/.tacdel.env, never committed); check each take with tools/align.py and re-voice only a
   chapter that fails. Build one page per chapter following the visuals contract: the real
   thing (gameplay, logs, pages) on screen whenever the voice mentions it; no still over ~6 s
   (tools/stills.py clean); a visual change every 20-30 s; one consistent colour per
   character; a visible label on any fake content. Render the master and the Shorts with
   tools/build_all.sh as a detached [pfx]-render unit. Look at real frames of the master.
6. PACKAGING (phase 5): titles, description with chapters, captions, SHORTS.md (file, length,
   hook, first and last line), and 2-3 thumbnail PROMPTS for ChatGPT (I make the images).
7. PUSH through tools/push.sh. Keep results/, voice audio and every mp4 out of git.
8. REPORT at each stop: phase, what's done, what's running, what you need from me, under 300
   words, plain English, file paths for anything I should watch.
```

## Header

```
Fresh session. [Scope limits, e.g. "No new rooms, no new runs."] Every number on
screen comes from the logs or results files, never typed by you or a model. Commit
and push as you go. Report under 300 words, plain English.
```

## Push

```
PUSH: commit and push every branch and worktree to origin over SSH. Keep results/
and all mp4s out of git.
```

## Live page

```
LIVE PAGE: rebuild the single-file page from the latest room code and publish it to
gh-pages. You have my permission to push to gh-pages for this. If Pages hasn't
rebuilt within 10 minutes, push an empty rebuild commit. Then fetch [live URL] and
confirm every room loads with no errors.
```

## Render footage

```
FOOTAGE: render every shot in [list or ORDER draft] into results/final_footage/wide
(1920x1080) and /vertical (1080x1920), 30 fps H.264, named NN_chapter_shot.mp4 in
video order, and write ORDER.txt (NN | chapter | shot | one line | seconds). Check each
file plays and has the right size and fps.
```

## Stat cards

```
STAT CARDS into results/film-stats/: [style], wide and vertical, 30 fps H.264, about
6 s each (the number counts up, then holds), every number read from the results files:
S1 [what]
S2 [what]
...
S# end card: "[call to action]" plus [live URL], no numbers
```

## Charts

```
CHARTS into results/filmpack/: [list], same palette, readable at phone size, numbers
from the results files.
```

## B-roll commands

```
B-ROLL: give me [N] tested commands I can run and screen-record in my VS Code
terminal. None may write or change any results.
a. [e.g. replay one agent's decisions at a readable speed, about 60 s, in color]
b. [e.g. ask the local model one real question live]
```

## Fact check

```
FACT CHECK: my narration script is pasted at the bottom. Check every number and
claim against the logs and results files. List each one that doesn't match or has no
file behind it, with the correct value and the file it comes from. Don't edit the
script.
```

## Copy to Windows

```
Include PowerShell commands that create [folder] on the Desktop Windows actually
shows ([Environment]::GetFolderPath('Desktop')) and copy [folders] into it over
Tailscale from the build machine.
```

## README screenshots

```
README: take [N] screenshots of the live page with headless Chrome, 1600 wide, UI
hidden, compressed JPG under 400 KB each, into docs/screenshots/. Add one GIF under
5 MB of [moment]. Update the README: pitch, GIF, live link, video link, screenshot
grid (2 per row, captions), results from files, how to run, credits.
```

## Report

```
REPORT: [exactly what to list — what's live, fact-check results, file counts and
lengths, commands to copy files, anything I need to decide].
```
