# SFX library index

Pass the name (file name without `.mp3`) to `cue(...)`; `sound.py` loads `tools/sfx/<name>.mp3`.
Search this table by tag to find an effect. Made with ElevenLabs Sound Effects v2 (`eleven_text_to_sound_v2`).

| Name | Tags | What it is | Length | Notes |
|---|---|---|---|---|
| `earthquake_rumble` | earthquake, rumble, shake, wood, creak, bed, loop | Low earthquake rumble: a wooden workbench shaking side to side, wood creaking and rattling | 6.0 s | Made as a seamless loop: tile it under any shaking. Scale the gain to the shake strength; resample to ~0.6x for slow motion. |
| `wood_clack` | impact, wood, clack, block, place, tap, small | One small wooden toy block set down on a stack: short dry clack | 0.6 s | Hits hard at the start: vary the gain (0.3–0.5) and rate (0.9–1.15) when a run of blocks is placed. |
| `wood_collapse` | impact, wood, collapse, crash, fall, scatter, blocks | A tower of small wooden blocks toppling onto a wooden table, blocks clattering and scattering | 3.0 s | Start it on the collapse frame. Use rate 0.85 for slow-motion replays. |

First used in the Earthquake Towers pilot Short (2026-11-24). The other effects (stamp, stampede, paint, printer,
whistle, pages, scratch, tada, drone, press, sizzle, conveyor, register, typing, drawer, buzzer) are listed in SKILL.md.
