# Writing the narration

Read this when writing or revising a script, preparing it for ElevenLabs, or running
the fact check.

## When to write it

Only after the footage is rendered and `ORDER.txt` exists. Read ORDER.txt (or the
creator's clip list) first, then write the script as a walk through those clips. A script
written before the footage will describe things the viewer isn't seeing.

## Chapter structure (about 11 chapters, 9–11 minutes)

1. **Cold open** (under 60 s): the trend, the internet's reaction, what I did, and the twist
   nobody else did. Built from 1–3 s pieces of later clips. The title card lands right after
   the last line, with a music hit.
2. **Welcome / tour:** where we are, "every number on these walls is real", the machine it
   ran on, and how it was built (Claude Code and Codex).
3. **The core object, explained simply** (hedgefly: the brain).
4. **What changes and what stays fixed.** Plus the rules everyone plays by.
5. **The fair test / control** (hedgefly: the fake twins).
6. **The process** (evolution, training rounds, eliminations).
7. **The first finding** — ideally a surprise.
8. **The honest problem** (memorizing instead of learning — the surprise exam).
9. **The real test** on locked-away data (the vault).
10. **Challengers:** an AI model and simple baselines.
11. **The twist, the verdict and the call to action.**

## Voice

- **Tour guide, first person:** "This is the brain room." "Watch these two lines." "The ones
  that didn't make it end up here."
- Use contractions. Keep most sentences under 15 words.
- **Set up and pay off:** "Remember that." early, then the payoff later.
- **Light jokes only when they're true** (the headline AI "really only had one idea").
- **End the verdict as simple Q&A:** "Can a fly brain trade? No. Is real wiring better than
  random? Yes. Because it knows how to sit still."
- **Close** with the live link and "tell me what to run it on next."

## Plain-word swaps

| Jargon | Say instead |
|---|---|
| basis points, fee per side | a small fee every time it buys or sells |
| median | the typical one |
| control group | fake twins, the shuffled copies |
| overfitting | memorizing instead of learning |
| validation, out-of-sample | a surprise exam |
| held-out test set | locked away in the vault |
| genome, parameters | dials, its DNA |
| buy-and-hold | just holding Bitcoin (or whatever the asset is) |
| momentum strategy | a robot that chases the trend |
| random baseline | a robot that picks at random |
| connectome | wiring map (say "connectome" once, then explain it) |

## Timing

- ElevenLabs reads about 150 words a minute.
- Target words ≈ (footage seconds + stat cards + planned recordings) × 2.5.
- Each clip carries 1–3 sentences; a 12-second clip holds about 25–30 words.
- If the script runs more than 20% longer than the footage, cut words first. Then add
  director-mode recordings. Never add new rooms at this stage.

## Numbers

- Take every number from the results files. Ask Claude Code for a numbers sheet if needed.
- **Spell numbers the way they're spoken:** "nine hundred fifty-two dollars", "two point
  seven percent", "seventeen hundred eighty-eight".
- Keep the rounding identical to the stat cards.
- Speak fewer numbers; let the stat cards carry the rest.
- **Avoid phrases that go stale:** "three weeks ago" → "a few weeks ago", "this month" → "just".
- **Word partial effects precisely:** if a gap remains even without fees, say "most of that
  gap is fees", not "fees ate the difference".

## ElevenLabs formatting

- One chapter = one generation, with the same voice and settings every time.
- Use "..." for pauses and blank lines between paragraphs.
- **No square brackets or stage directions** — some models treat [tags] as instructions or
  read them aloud.
- Keep stability around the middle. Lower is more emotional but less consistent.
- Do 2–3 takes per chapter, and regenerate single lines instead of whole chapters.
- A paid plan is needed for monetized videos (the free plan is non-commercial and needs
  attribution).
- Name the files by chapter: `01_cold_open.mp3`, `02_welcome.mp3`, and so on.

## Fact check (before any voice is generated)

Send the full script to Claude Code: check every number and claim against the logs and
results files, list each mismatch with the correct value and its source file, and don't
edit the script. Apply the fixes, then record the voice. A block for this is in
`templates/claude-code-prompts.md`.

## Output

Use `templates/script-template.md`. Each chapter has a paste-ready **Voice** block and a
**Shots** list: `"first words of the line" → NN shot`, `S#` stat card, chart, or `Rec:`
screen recording. End the file with a Shorts list and the credits.
