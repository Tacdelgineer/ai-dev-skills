# Screen recordings, CapCut edit, audio and export

Read this when the creator is recording, editing, fixing audio or exporting. The creator
edits in CapCut on Windows and records with OBS.

## Folder on the Windows desktop

`final_footage/wide`, `final_footage/vertical`, `film-stats`, `filmpack`, `voice`,
`recordings`. Claude Code's copy commands should create exactly these folders.

## Screen recordings (OBS)

- **OBS settings:** 1920x1080, 30 fps (matches the renders), MP4. Use Window Capture and
  untick "Capture Cursor".
- **Terminal B-roll** (VS Code over SSH):
  - Press Ctrl+= a few times so the text reads on a phone, and Ctrl+B to hide the sidebar.
  - Split the terminal: the B-roll command on one side, `watch -n 1 nvidia-smi` on the other.
  - Record 2–3 takes.
- **Director mode** on the live page:
  - Keys: F fullscreen, H hides the UI, number keys jump rooms, WASD pans, +/- zooms,
    hold Shift for slow motion.
  - Slow moves look best. Record 20–40 s per take.
  - Record after the voice exists, playing that chapter's audio in headphones.
- **Real-world B-roll without filming:** free stock clips (Pexels, Pixabay, CapCut's
  library), scrolling the source paper, a price chart of the test period.

## Timeline

1. New project: 1920x1080, 30 fps.
2. Put the voice files on audio track 1 in chapter order, about 0.5 s apart.
3. Follow each chapter's Shots list: start a clip where the voice says those words. Ctrl+B
   splits a clip; trim from there.
4. **Cold open:** use 1–3 s pieces, then the title card for 3–4 s right after the hook, on a
   music hit.
5. **Stat cards** are full-screen cut-ins.
6. **Charts:** show for 5–8 s, with Scale keyframed from 100% to 110% for a slow zoom.
7. To swap in a re-rendered clip: right-click the clip → Replace.
8. **Music** goes on audio track 2. The creator's own tracks (FLOWR8) avoid copyright claims.
   Start around −18 dB, louder for the hook, the big reveal and the outro.
9. **Captions:** Auto captions from the voice track, then fix names and jargon.
10. Put the credits line in the last seconds.

## Audio loudness

CapCut's "Loudness normalization" levels audio to about −23 LUFS, which is quieter than
YouTube's −14. YouTube turns loud videos down but not quiet ones up, so fix loudness after
export with ffmpeg on Windows:

```powershell
winget install Gyan.FFmpeg        # once; reopen PowerShell afterwards
ffmpeg -i video.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 320k video_youtube.mp4
```

The video stream is copied untouched; only the audio changes. To open PowerShell in a
folder: click File Explorer's address bar, type `powershell`, press Enter.

## Export

1080p, 30 fps, H.264, MP4, bitrate "Higher".

## Shorts

- Build a new 9:16 project from the vertical renders.
- One moment per Short, 20–45 s, with a text hook in the first second.
- Voice lines from the long video can be reused.
- Good picks are the most visual beats: things filling up, a reveal, a character refusing
  to act, two lines splitting.
