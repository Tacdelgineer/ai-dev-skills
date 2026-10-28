# [Video title] — script v1

Automated mode: this file is the source for the voice (tools/voice_ch.py reads each **Voice** block), the shots
(each chapters/NN_scenes.js cues its shots to words in it) and the fact check (every **Check** line names a file).
Main cast: [at most 3 + a yardstick]. Spoken words: [N] (eleven_v4 at speed .93 reads ~170 wpm).

---

## 00. Cold open

**Voice**

This page looks like a real data sheet. Every number on it is made up.

The agent read it, and believed it. Here is what it wrote.

**Shots**
- 0.0 s, before the first word (voice/edits.json "leads") → the payoff: the real call on the fake page, fake label on
- "This page looks like" → the fake sheet, fake label on
- "Here is what it wrote" → split: the sheet left, the agent's real log right

**Check**
- "made up": data/fakes/[file] (written by me for the test).
- "it wrote": runs/[run id]/decisions.jsonl line [n], word for word.

---

## 01. [Chapter name]

**Voice**

[One idea, introduced right before it's needed. Numbers spelled out; most of them stay on screen.]

**Shots**
- "[first words]" → [shot] · [look]

**Check**
- [claim]: [file and field]
