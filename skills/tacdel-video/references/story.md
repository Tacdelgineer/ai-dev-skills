# Writing the narration

Read this when writing or revising a script, preparing it for ElevenLabs, or running
the fact check.

## When to write it

The rule in both modes: **every line describes what's on screen, and everything on screen is
in the voice.** How you get there depends on the mode (SKILL.md):

- **Manual mode (rooms + CapCut):** after the footage is rendered and `ORDER.txt` exists. Read
  ORDER.txt first, then write the script as a walk through those clips. A script written before
  the footage will describe things the viewer isn't seeing.
- **Automated mode (`automated.md`):** after the results are final and before any visuals. The
  script's **Shots** lines are the shot list; each chapter's scenes are then built to the voice
  take, every shot cued to a spoken word, every real clip chosen for the line it sits under.

## Story rules (what turned v1 into the final cut)

Learned on two videos where the first draft was correct and dull: agent-money-trust (script
v1 → v2 → v3; 1,995 spoken words in v2, 1,467 in v3, same facts; 13:40 → 8:51 on screen,
part of it from the faster eleven_v4 voice) and
agent-obstacle-course (v1 → v2; ~1,660 → ~1,350 words). Apply them to the first draft, not the third.

**1. Payoff in the first 5 seconds.** Open on the result, then explain it. Put the visual
payoff on screen before the first word (a 3.5–4 s lead in `voice/edits.json`).

> Before: "I gave six AI coding agents the same job. Build a small browser game, using some
> pages I found online."
> After: 3.5 s of the agent's own 2048, two-two-four sliding into eight, then: "This game passes
> every check I threw at it but one... and that one bug was copied from a bad web page."

**2. One concrete moment, told slowly, then zoom out.** One market, one agent, one decision,
with its price, its notes and its result. Only then the totals.

> Before: "I slipped a fake tip into every market's research. Hype posts. Anonymous insiders.
> Leaked memos. Fake news. They read them, and as a group, they shrugged them off."
> After: "Will the high in Denver land at exactly seventy-two or seventy-three degrees? ... So
> Sol bet against it. Thirty dollars on NO. ... This time, Sol bet YES. A hundred dollars ...
> That update was fake. I wrote it." Then: "Sol was one of seven AI agents."

**3. Say WHY early.** Within the first minute, one or two lines on why the test matters to
the viewer, before any mechanics.

> Before (chapter 1 opened on mechanics): "Here's the problem with testing an AI on the
> future. You have to wait for the future to happen."
> After: "An agent that bets your money reads whatever it finds: news, forums, data. Some of it
> is wrong. Some of it is wrong on purpose. So the real test isn't whether it's smart. It's
> whether it can be fooled."

**4. A main cast of at most three** (plus a yardstick, like a dumb bot). The rest are "the
rest" in the voice and keep their own labels on screen, on every board and chart.

> Before: "Eight AI agents. Four live in the cloud: Claude Opus and Claude Haiku from
> Anthropic, and two of OpenAI's newest, GPT six point one Sol and GPT six Luna ..."
> After: "Here's the cast. You've met Sol ... Claude Opus, the biggest, most expensive Claude
> here. And Gemma, Google's tiny model ... Four more agents play along. You'll see them on the
> boards."

**5. One idea at a time, right before it's needed.** No list of everything up front; each
concept arrives in the chapter that uses it.

> Before: a chapter called "Six ways the internet is wrong" listing all six traps before any
> result.
> After: "Back to that wiki. Its sample code is the first trap: a buggy example." ... two
> chapters later: "The second trap is a forum post." The yardstick bot moved from the cast
> chapter to the line right before it's first used: "Before the results, one more player."

**6. Numbers on screen, not in the voice.** Speak the one number that is the story (thirty-six
out of thirty-six) and say the rest in words; the board carries the full table. When the voice
rounds, the screen shows the same rounding big and the exact figure small.

> Before: "Qwen three point six: eleven hundred and four dollars. Qwen three point eight: one
> thousand and seventy-one. Then GPT six point one Sol, one thousand sixty-five ..."
> After: "Sol beat the bot in all three of its runs. Steady. The only agent that did. Claude
> Opus came dead last. It lost a little, every time." (Full board on screen.)

**7. Character arcs and callbacks.** Give each main character a turn (the trusted one gets
fooled; the last-place one turns out to be the skeptic) and plant lines you pay off later:
"Hold on to that." "Remember that. Anything I should know." "Back to Denver."

> Before: "Claude Opus, Anthropic's biggest model, at eight hundred and forty. The most
> expensive brain in the lineup came last." (Never mentioned again.)
> After: last in round one → "I really expected Opus near the top" → it calls the fake
> "implausibly confident and unverified" and skips → "Opus, last place in round one, did better
> with the fakes in the folder. The only agent that improved."

**8. Practical takeaways.** End with two or three things the viewer can do, each tied to a
moment they saw.

> Before: "If you let an agent touch your money, the risk isn't the obvious scam. It's whatever
> it's reading that looks official."
> After: "Three things you can use. One: be most suspicious of the official-looking update ...
> Ask your agent what it checked that correction against. Two: cap the bet size. Three: race
> any agent against a dumb bot before you trust it."

**9. End on this video, never the next one.** The last line is the payoff, the takeaway, or
a short question to the viewer about this video. Never tease, promote or advertise another
episode or video: no "next time...", "in my next video...", "subscribe to see...".

> Before: "Next time, I'm taking AI agents to an obstacle course. Subscribe, and you'll see
> who makes it through."
> After: "So be most suspicious of the update that looks the most official. Which one would
> your agent have believed?"

Keep in the script header: the main cast, the order the ideas arrive, the spoken word count,
and a list of what left the voice (it stays on screen and in the Check lines).

## Chapter structure (about 9–11 chapters, 9–10 minutes)

The hedgefly order below still works as a checklist of what a video must cover; the story
rules above decide the order the ideas arrive in.

1. **Cold open** (1–2 min): the payoff first (rule 1), the one concrete moment (rule 2), then
   the zoom out to the whole test and the question in the title. The title card lands right
   after the last line, with a music hit.
2. **Why, and the setup:** why the test matters (rule 3), where we are, "every number on
   screen is real", the machine it ran on, and how it was built (Claude Code and Codex).
3. **The core object, explained simply** (hedgefly: the brain).
4. **What changes and what stays fixed.** Plus the rules everyone plays by.
5. **The fair test / control** (hedgefly: the fake twins).
6. **The process** (evolution, training rounds, eliminations).
7. **The first finding** — ideally a surprise.
8. **The honest problem** (memorizing instead of learning — the surprise exam).
9. **The real test** on locked-away data (the vault).
10. **Challengers:** an AI model and simple baselines.
11. **The twist, the verdict and the takeaways** (rule 8), ending on rule 9.

## Voice

- **Tour guide, first person:** "This is the brain room." "Watch these two lines." "The ones
  that didn't make it end up here."
- Use contractions. Keep most sentences under 15 words.
- **Set up and pay off:** "Remember that." early, then the payoff later.
- **Light jokes only when they're true** (the headline AI "really only had one idea").
- **End the verdict as simple Q&A:** "Can a fly brain trade? No. Is real wiring better than
  random? Yes. Because it knows how to sit still."
- **Close** on the payoff, the takeaway or a question about this video (rule 9), plus the live
  link if there is one. Never tease another video.

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

- ElevenLabs reads about 170–175 words a minute with the channel's `eleven_v4` settings
  (`FINAL_VOICE.md`; ~150–170 on a Short, so a ~45 s Short is ~110 words). A 9–10 minute video is
  ~1,400–1,500 spoken words.
- Manual mode: target words ≈ (footage seconds + stat cards + planned recordings) × 2.5.
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

- Automated mode voices through the API with fixed settings: `automated.md`.
- One chapter = one generation, with the same voice and settings every time.
- Use "..." for pauses and blank lines between paragraphs.
- **No square brackets or stage directions** — some models treat [tags] as instructions or
  read them aloud.
- Voice settings are fixed (`FINAL_VOICE.md` at the repo root): `eleven_v4` only, never v2, the same
  stability, similarity and speed every time. Don't tune them per video.
- One take per chapter (one per Short). Re-voice only a take with a wrong or swallowed word, and
  then only that chapter.
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
