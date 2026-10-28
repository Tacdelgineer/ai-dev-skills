# Final voice settings (tacdel channel)

The one voice setup for every tacdel video and Short: `tacdel-video`, `tacdel-shorts` and `tacdel-motion` all
use it. Picked by the owner on 2026-10-26 after a v2-vs-v4 cold-open test in the money-trust video; made the
standing default for Shorts on 2026-10-28. `scripts/build.sh` copies this file into each tacdel skill zip.

| Setting | Value |
|---|---|
| Provider | ElevenLabs text-to-speech API |
| Voice | the owner's professional clone "Alireza" (id = `ELEVENLABS_VOICE_ID` in `~/.tacdel.env`; never commit it) |
| Model | `eleven_v4` only. Never `eleven_multilingual_v2` or any other v2 model. |
| `voice_settings` | `{"stability": 0.69, "similarity_boost": 0.78, "speed": 0.93}`, sent with every request, unchanged |
| Not sent | `style`, `use_speaker_boost` (eleven_v4 takes neither: models API `can_use_style` / `can_use_speaker_boost` = false). Clone strength can't be set through the API. |
| Endpoint | `POST /v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_192` (audio + character timings) |
| Takes | **one** generation per Short (per chapter in a long video), plain text: no SSML, no [tags] |

Request body:

```json
{"text": "<one Short or chapter>", "model_id": "eleven_v4",
 "voice_settings": {"stability": 0.69, "similarity_boost": 0.78, "speed": 0.93}}
```

**Always send `voice_settings`.** The settings stored on the voice in ElevenLabs are left over from v2
(read back 2026-10-28: stability 0.42, similarity 0.78, style 0.24, speed 1.0, speaker boost on) and apply to
any request that sends none, including the ElevenLabs connector's `creative_generate_speech`. Don't edit them
and don't rely on them.

**Pace:** ~150–170 words a minute on a Short (seven v4 Shorts on 2026-10-27: 100–119 words in 40–43 s of
voice), ~170–175 on long-form chapters. A ~45 s Short is ~110 spoken words.

**One take:** check it instead of re-rolling it. The word timings from the alignment go through
`tacdel-motion/tools/pick_take.py` (transcript match, pace, longest pause) or `tacdel-video`'s `align.py`
(Whisper, "N/N words matched"). Re-voice only a take with a wrong, swallowed or garbled word, never for taste.

**Loudness:** takes come in quiet; normalise in the mix (two-pass ffmpeg loudnorm, -14 LUFS integrated,
-1 dBTP).

**Cost** on the owner's plan (measured from the ElevenLabs history): ~0.44 credits per character, so ~300
credits for a ~110-word Short and 630 for a 1,432-character chapter.

**Code that sends these settings:** `skills/tacdel-motion/tools/voice.py` (Shorts),
`skills/tacdel-video/scripts/chapters/tools/voice_ch.py` (long-form chapters). Both carry `MODEL` and
`SETTINGS` constants that must match this file.

**Retired (don't use):** `eleven_multilingual_v2`, stability 0.69, similarity_boost 0.78, style 0.24, speed
0.93 or 1.0, use_speaker_boost true, 2–4 takes per script (until 2026-10-26 for long-form, 2026-10-28 for Shorts).
