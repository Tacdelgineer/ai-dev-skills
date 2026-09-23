# Packaging: title, thumbnail, description, CTR, README

Read this when naming the video, making a thumbnail, writing the description, reading
click-through stats, or updating the project's README.

## Title

- Keep it to 60 characters or fewer, in plain words, with the searchable trend words early.
- **Pattern:** "I [did something surprising] [with clear stakes]".
  Example: "I Gave 100 Fruit Fly Brains $1,000 Each to Trade Bitcoin".
- Offer one pick and two backups.
- Don't repeat the thumbnail's words. The title gives context; the thumbnail gives the
  picture and the emotion.

## Thumbnail

**Brand (keep on every video):** hand-brushed title lettering in bright yellow and white
with a thick black outline, plus a glowing neon pill badge holding a short tag.

**Rules:**
- **One subject, one idea, three words or fewer.** It must read at phone size: shrink it to
  about 160 px wide, and if you can't tell what it is, simplify.
- **Show a tension or question, not a label.** "REAL vs FAKE" beats "3D FACTORY".
- **Show an emotion:** a character with an obvious expression, or clear stakes (money, a
  winner and a loser).
- **Match the video's look,** so the click delivers what the thumbnail promised.
- **No small handwritten notes,** panels or extra text. They turn to noise at phone size.
- **Make 2–3 versions** that differ in the idea, not the font, and run YouTube's Test & Compare.

**Prompt template (ChatGPT image):**

```
YouTube thumbnail, 16:9, 1280x720.
[Background and texture matching the video's style]. Colors: [2–3 colors only].

Center: [one subject or scene showing the tension, with a clear emotion].

Bottom: huge hand-brushed title text "[2–3 WORDS]". First word in bright yellow,
the rest in white, thick black outline, rough street-poster brush strokes.
Under it, a glowing neon pill badge with the text "[SHORT TAG]".

One clear focal point, bold shapes, lots of empty space, readable at phone size.
No other text anywhere.
```

**Version B:** attach an older thumbnail and add "Match the style of the attached
thumbnail, but keep it this simple."

## Click-through rate playbook

- **Baseline:** most videos land between about 2% and 10%. The channel's first measured
  video got 5.7% on 1.6K impressions, and impressions flattened by day 4. The bottleneck was
  reach, not CTR.
- CTR naturally drops as YouTube shows a video to colder audiences. The goal is a steady
  CTR while impressions keep growing, not a high CTR on a few hundred impressions.
- **The idea is half the CTR.** Curious, trending topics beat product names; a "DGX Spark"
  label only pulls people who already care about the box.
- Check CTR by traffic source (browse, search, suggested) in YouTube Studio before changing
  anything.
- Change one big thing per test.

## Description template

```
[2 lines: the hook — what I did, and the twist]

[2–3 lines: how it works in plain words; what it ran on; built with Claude Code and Codex]

Walk through the whole experiment yourself: [live page URL]
Code: [repo URL]

Chapters
0:00 [Cold open]
m:ss [Chapter 2 name]
...

Credits
[style inspirations, skills and their licenses, data sources, libraries]

[For trading or finance videos: "Not financial advice. It's an experiment."]

#tag1 #tag2 #tag3
```

- **Chapters:** the first must be at 0:00, with at least 3 chapters, each 10 s or longer.
  Use the script's chapter names and take the times from CapCut.
- Don't include links to things that don't exist yet (no community link until there is one).

## Project README (after upload)

Include: a one-line pitch, a GIF, the live page link, the video link, a screenshot grid, the
results (numbers from files), how to run it, and credits.

## Publish checklist

- [ ] ffmpeg loudness pass done
- [ ] Title picked; 2–3 thumbnails loaded into Test & Compare
- [ ] Description chapter times filled in
- [ ] Repo public, if the video says the code is
- [ ] Live page up to date
- [ ] Comment pinned with the live link
- [ ] 3–5 Shorts scheduled over the following days, each linked to the full video
