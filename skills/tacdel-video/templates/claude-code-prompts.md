# Claude Code prompt blocks

Chat Claude assembles prompts from these blocks. Always start with the header and end
with a REPORT step. Fill in the [brackets]. Keep each step to one job.

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
