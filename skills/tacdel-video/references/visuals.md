# Visuals: rooms, footage, stat cards, charts, live page

Read this in Claude Code when building rooms, rendering footage, stat cards or charts, or
publishing the live page. Chat Claude reads it when planning which rooms a video needs.

> The contract sections are decided; don't change them. The implementation below was written
> from hedgefly's working code (the neon-riso-fly skill, its room code, renderer, stat cards,
> charts and live page) and generalised: the code in this skill's `scripts/` and `assets/`
> knows nothing about flies except its default character.

## Contract: the look

- **Neon risograph, isometric rooms:** a dark navy "paper" background, halftone grain, and
  hand-drawn canvas animation.
- **Colors:** two groups being compared get two equal-weight colors (hedgefly: cyan for
  real, magenta for fake), with gold reserved for the hero or champion.
- **Equal brightness and size** for anything being compared, so nothing looks like it's
  winning before it wins.
- **One room = one idea.** The camera moves slowly.
- **Numbers on screen come only from results files.** Title cards carry no numbers.
- **Credit** the riso-rooms and hand-drawn-canvas-animation skills (IshaanKalra2103, MIT)
  and Kevin Ngo's inspiration.

## Contract: output

- **Footage:** `results/final_footage/{wide,vertical}/NN_chapter_shot.mp4` at 1920x1080 and
  1080x1920, 30 fps, H.264, usually 6–18 s per shot, plus `ORDER.txt`.
  See the naming contract in SKILL.md.
- **Stat cards:** `results/film-stats/S#_name_{wide,vertical}.mp4`, about 6 s: the number
  counts up, then holds. Same palette. Numbers are read from files at render time.
- **Charts:** `results/filmpack/*.png` in the same palette, readable at phone size.
- **Live page:** one self-contained HTML file with all data baked in. It works from a
  double-click and from GitHub Pages, and is published to gh-pages only with explicit
  permission.
- **Director mode:** F fullscreen, H hides the UI, number keys jump rooms, WASD pans,
  +/- zooms, Shift for slow motion.

## Room menu (what worked in hedgefly, and what it's for in general)

| Room | Shows | Works for any experiment that has... |
|---|---|---|
| Street / establishing | the building from outside | an opening tour |
| Lab | the real machine on the desk | "it all ran locally" |
| Server room timelapse | hours of compute | long runs |
| Core-object room (Brain) | the thing being studied, pulsing | a model or structure to explain |
| Eye / input room | how data enters the system | an input encoding |
| Switchboard | what's allowed to change | trainable parameters |
| Blueprint / dollhouse | the whole system at once | an architecture overview |
| Barcode wall | every agent × every round | populations over time |
| Nursery | new agents born | mutation or reproduction |
| Selection / the Pile | who got eliminated | selection or pruning |
| Tree of life | family lines, hero in gold | lineages or checkpoints |
| Archive | one poster per round | per-round summaries |
| Trading floor | the population at work | many agents acting at once |
| Ticker tape | real events scrolling | logs worth showing verbatim |
| Replay room | one decision at a time, with internals | explainability |
| Toll booth | costs | fees, latency, compute cost |
| Hero desk / cam | following one agent | a character to root for |
| Overfit room | training line vs surprise exam | train/validation splits |
| Corridor | the locked-away period | a held-out test set |
| Vault + scoreboard | the final reveal | a final evaluation |
| Model's office | an LLM challenger thinking | an AI baseline |
| Boardroom | the verdict | conclusions |
| Night to day | the outro | endings |

## Implementation

### Palette, type and texture

| Token | Hex | Means |
|---|---|---|
| paper | `#07070b` | near-black stock with a faint violet cast; never pure black |
| cyan | `#27f2d2` | subject A of the comparison, and nothing else |
| magenta | `#ff3d9a` | subject B, equally bright, and nothing else |
| gold | `#ffc93c` | the one hero or champion the story follows |
| amber | `#ff7a1a` | what is held back: the locked test, the vault, the reveal |
| slate | `#5b6cff` | architecture: walls, floors, furniture (always at low tone) |
| ghost | `#d8dcff` | linework, small type, and anyone outside the comparison |

- Write this table out with the project's own nouns before drawing a room. A colour with no
  noun is a bug. Check the two compared inks in greyscale: they must read as the same grey.
- **Texture:** every fill is a halftone dot screen, and inks are added like light (canvas
  `screen` mode), so overlaps brighten instead of muddying. Each ink has its own screen angle
  and sits about a pixel off register. Lines are resampled and wobbled with noise. The drawing
  updates at 12 fps and the wobble re-rolls every 4 frames (the "boil"). Paper grain goes on
  last, over everything. No gradients except glows, no blur, no drop shadows.
- **Type:** no web fonts on the canvas. The stencil alphabet in `riso-core.js` draws
  A–Z, 0–9 and `$ % - + . , : / ( ) * · ' ! ?` with the same wobbly pen (`text`,
  `textCentred`; `{wall:'i'}` or `{wall:'j'}` shears it onto a wall). Lettering hangs *down*
  from its anchor by its own size, and a room is 32 px per unit of height: space wall lines
  by at least the text size plus a few pixels. At stat-card size the core's 8 reads as a 0;
  the stat card swaps in a two-loop 8. Page chrome (buttons, key legend) uses a system
  monospace stack and is hidden in every take.

### Canvas, pen and the room template

- **Projection:** `iso(i, j, z)`: tiles 64×32 px, 32 px per unit of height. Rooms sit on a
  `(col, row)` grid with a gap between, so the world reads as one building.
- **The pen** (`makePen(ctx, {ox, oy, boil})`), one per room per frame: fills (`knock`,
  `tint`, `fill`, `shade`), `line(points, ink, width, {tone, amp, dash, closed})`, `shape`,
  `dot`, `floorQuad`, `wallQuad(wall, u, z, w, h)`, `ellipse`, `circle`, `box`,
  `shell(room)` (the cutaway: floor plus two back walls), furniture (`table`, `chair`, `rug`,
  `bookcase`, `books`, `window`, `lamp`, `plant`), light (`glow`, `halo`, `light`, `steam`,
  `sparkle`) and characters (`fly`, `minifly` for crowds, `deadfly` for a pile).
- **Characters:** hedgefly's are flies. For another project, swap `pen.fly` for one other
  non-human shape and keep it the only kind of character in the world.
- **A room:**

  ```js
  room({id: 'vault', name: 'the vault', col: 3, row: 0, w: 7, d: 7, h: 3.2,
    style: {floor: ['slate', .34], wall: ['slate', .14], wall2: ['slate', .18], planks: false},
    draw(pen, t, R) {        // t = seconds, R = this room's seeded random (never re-rolls)
      // 1. furniture and a character, so it is a place and not a slide
      // 2. signs: words only
      // 3. numbers: read from RUN and the current stage, never computed or typed
    }});
  ```

- `draw()` never re-derives a figure the data could have carried. Each room's draw is wrapped
  in a try/catch so one broken room can't stop the world, which also means a broken room
  simply comes out empty: run the smoke check (below) after every change.
- Keep each room under about a thousand marks per frame. hedgefly's Pile caps its heap at 900
  bodies however many were eliminated, and the wall says the true count.
- Start from `assets/world/index.html`: section 1 is the clock, 2 the rooms, 3 the runtime
  (layout, camera, drift, drag and wheel, boil, draw loop), 4 the control surface. Replace
  section 2; keep the rest.

### How rooms read data (the runs file)

- **One JSON file is everything the world knows** (`data.json`; hedgefly's `runs.json`).
  Only the project's exporter writes it, from the logs and results files. The page replays
  it; it never reads raw logs, re-runs anything, or computes a number it could be handed.
- **Shape:** `contract_version` (an integer the page checks, refusing versions it doesn't
  know), `run_id`, `generated`, `fake`, `subjects` (the compared groups, in ink order),
  `start_value`, and `frames`: one per stage (generation, epoch, round), dense and
  ascending, so `frames[k]` is stage `k`. Big optional blocks (a finale, lineages, replays)
  may be missing; the room that needs one checks and says "not yet" instead of throwing.
- **A curve that draws itself** walks `frames.slice(0, stage + 1)`. Two compared lines
  always share one scale.
- **Inks are handed out by a subject's position** in `subjects`, never by its name.
- **The exporter** rounds on the way out (money to cents, ratios to 4 places), thins long
  curves to a few hundred points, checks counts and cross-references, and fails loudly
  rather than writing a file that draws wrong. hedgefly's grew from v1 to v4 as rooms were
  added (about 770 KB for 12 generations of two 100-fly tribes).
- **A fake generator** writes the same shape with invented numbers and `"fake": true`, so
  rooms can be built before the real run ends. The page stamps FAKE DATA on every frame, so a
  fake frame can't slip into a cut.
- Bump `contract_version` whenever a room would break without a re-export; old worlds kept
  for B-roll stay pinned to the version they were built for.

### The renderer

- **The control surface.** A filmable page exposes `window.__world` (hedgefly's was
  `window.__hedgefly`; the scripts accept both): `ready`, `step(ms)`, `shot('room', id, ms)` or
  `shot('building', null, ms)`, `rooms()`, `stages()`, `play(on)`, `stage(n)`,
  `cam(x, y, zoom)`, `frame(id)`, `spot(id, i, j, z)`, plus a setter for any state a shot
  needs (hedgefly added `gen`, `sel` for the selection event, `open` for the vault door,
  `reply`).
- **The virtual clock.** `?record` makes the page read time from `window.__VCLOCK__`, stop
  its animation loop, and hide the UI. The renderer calls `step(1000 / fps)`, screenshots,
  and repeats, so a take is identical every run and never drops a frame however slow Chrome
  is. Drawing code must read time from `NOW()`, never `performance.now()`.
- **Commands** (run from the project root):

  ```bash
  R="node scripts/video/render.mjs --page visuals/world/index.html --data visuals/world/data.json --shots visuals/world/shots.mjs"
  $R                                   # every shot, wide and vertical, plus ORDER.txt
  $R --only 07 --shapes wide           # one shot, one shape (matches NN or any part of the name)
  $R --only pile,vault                 # several
  ```

- **Settings:** 1920x1080 and 1080x1920 at device scale 1, 30 fps, H.264 `yuv420p`, CRF 18,
  `+faststart`. The drawing boils at 12 fps inside 30 fps video, so each drawing holds for
  2–3 frames: that is the hand-drawn look, not a bug. Frames travel to ffmpeg as JPEG at
  quality 95 (`--png` for lossless).
- **The shot list** (`assets/world/shots.mjs`) is the film in order. Each shot is
  `{chapter, shot, desc, seconds, setup, at}`; its place in the list is its `NN`. Four kinds
  cover most videos: a room as it stands; a room while its data advances (`at` steps the
  stage, so a wall fills on camera); a camera move (`at` sets `api.cam(...)` along an eased
  path built from `frame()` and `spot()`); the whole building. ORDER.txt is always written
  for the whole list, so re-rendering one shot never renumbers the others.
- **Vertical** uses the same list; the page's `?vertical` class adjusts anything
  screen-anchored. Check wall text still reads at 1080 wide.

### Stat cards

- `assets/statcard/index.html` draws whatever `stats.json` says. The project's exporter
  writes that file from the results: each card's numbers (value, format, ink, label), a
  kicker, a note, the curves or bars behind it, and one source line shown small on every card.
  The page holds no project logic and types no number.
- Each number counts up from zero over 2.4 s, then holds; the note fades in after the count.
  Both numbers on a card are set at the same size. Formats fix the rounding (`dollars`,
  `dollars2`, `whole`, `pct`, `pct1`, `dec1`, `dec2`, `times`); the narration and the
  description copy the card's rounding exactly.
- The last card is the end card: a call to action and the live URL, no numbers.
- Render: `node scripts/video/render.mjs --cards --page visuals/statcard/index.html --data
  results/stats.json` → `results/film-stats/S#_name_{wide,vertical}.mp4`, 6 s each
  (`--seconds`), plus a PNG of each card's final frame for the thumbnail and the README.

### Charts

- One page, one chart per `?chart=<name>`, drawn with the same core from the same data file
  (hedgefly: `visuals/filmpack/`, five charts). Each is a function of the data: title words
  (no numbers in titles), plotted values, and a source line at the bottom, all read from the
  file. A chart whose data hasn't landed draws a "pending" card instead.
- Compared lines share one scale and one line weight. Rendered at 3840x2160 (hedgefly's titles
  were 92 px there). Shrink each chart to phone size and re-check every label before using it.
- Render: give the chart page the same `ready`/`step` surface and use
  `node scripts/video/stills.mjs --page visuals/charts/index.html --data visuals/world/data.json
  --stills visuals/charts/stills.mjs --size 3840x2160 --format png --out results/filmpack`
  (one still per chart, `setup` picking it). A page with no control surface can be shot with
  plain Chrome: `chrome --headless --screenshot=out.png --window-size=3840,2160
  --virtual-time-budget=15000 file://…/index.html?chart=fitness` (hedgefly's `filmpack.mjs`).

### Single-file build and gh-pages publish

- **Build:** `node scripts/video/build_single.mjs --page visuals/world/index.html --data
  visuals/world/data.json --out visuals/dist/index.html --title "Project name"`. It inlines
  every local `<script src>` and the data (as `window.__RUN__`, with every `<` escaped so
  nothing can close the script early), and refuses a script containing `</script`. The result
  opens by double-click and runs unchanged on GitHub Pages. hedgefly's was about 830 KB.
- **Check before publishing:** `render.mjs --smoke --page visuals/dist/index.html`, press
  through director mode once, and grep the file for hostnames, usernames and home paths.
- **Publish, only when the prompt allows it.** The `gh-pages` branch holds one file,
  `index.html`, kept in its own worktree:

  ```bash
  git worktree add --orphan -b gh-pages ../REPO-pages      # first time only (git 2.42+)
  cp visuals/dist/index.html ../REPO-pages/index.html
  git -C ../REPO-pages add index.html
  git -C ../REPO-pages commit -m "Republish: <what changed>, built from $(git rev-parse --short HEAD)"
  git -C ../REPO-pages push origin gh-pages
  ```

  First time only, switch Pages on: repo Settings → Pages → deploy from branch `gh-pages`,
  folder `/` (or `gh api -X POST repos/OWNER/REPO/pages -f "source[branch]=gh-pages" -f
  "source[path]=/"`). If the live page hasn't changed within 10 minutes, push an empty
  commit (`git -C ../REPO-pages commit --allow-empty -m "Rebuild" && git -C ../REPO-pages push`).
- **Confirm it's live:** `node scripts/video/render.mjs --smoke --page
  https://OWNER.github.io/REPO/` draws every room from the published file and fails on any
  error.

### Director mode wiring

- `assets/lib/director.js` → `installDirector({rooms, current, goRoom, pan, zoom, rate,
  extra, legend})`. It owns the keys (1–9 and 0 jump to the first ten rooms, `,` `.` step
  through all, arrows or WASD pan, `+` `-` zoom, hold Shift for slow motion and a finer pan,
  H hide, F fullscreen, P save a PNG) and fills the key legend. `extra` adds project keys
  (hedgefly: `[` `]` generations, B building, Y hero cam, T terminal, K blueprint, O
  dollhouse, N night-to-day, I about).
- The page provides the four moves. **Pan and zoom must move the camera's resting point
  (`camBase`), not the camera itself**: the idle drift rebuilds the camera from the base every
  frame, so a key that moves only the camera is undone before anyone sees it. `touch()` folds
  the current drift into the base first, so taking over the camera never jumps.
- **Slow motion** needs a clock that accumulates time at `RATE` (`advance()` in the starter);
  Shift sets `RATE` to 0.25 while held.
- Everything with class `ui` hides under `body.clean` (H, `?clean`, `?record`). Keys never
  change a number, so a hand-recorded take shows exactly what a render would.
- Mouse: drag pans, the wheel zooms toward the pointer, double-click flies into a room.

### Performance notes and gotchas on the build machine

- **ARM64 Linux (DGX Spark):** Google ships no Chrome for it. Use Playwright's headless shell
  (`npx playwright install chromium-headless-shell`, found automatically) or set `$CHROME`.
  Node 22 or newer (the scripts use Node's built-in WebSocket; no npm packages).
- **H.264:** Playwright's bundled ffmpeg is VP8-only. `apt install ffmpeg` has libx264; `$FFMPEG`
  overrides. Without one, the renderer writes PNG frames and prints the command to encode them
  on Windows (`winget install Gyan.FFmpeg`).
- **Speed:** headless Chrome draws the canvas on the CPU (`--disable-gpu`), so renders never
  compete with GPU jobs. Measured on the Spark with the starter world: 0.12–0.21 s per frame
  (drawing about 40 ms, the screenshot most of the rest; PNG screenshots were 3x slower than
  JPEG). Busier rooms draw slower. Budget
  4–6 minutes of machine time per minute of footage per shape; the renderer prints s/frame.
- **Size:** halftone grain is noisy to compress: about 4 MB per second of 1080p at CRF 18.
  hedgefly's 40 wide shots came to 1.6 GB. Keep `results/` and `*.mp4` in `.gitignore`.
- **Silent failures:** a room that throws draws nothing (see the smoke check), and a page
  opened from `file://` can't fetch its JSON, so always film the inlined page, never the
  source file directly.
- **Screen size:** the renderer sets device scale 1, so CSS pixels are video pixels; the page
  caps its own `devicePixelRatio` at 2 for people's screens.
- **GIFs:** one palette per clip with an ordered (bayer) dither keeps the halftone crisp;
  800 px wide at 12 fps fits a 5–6 s loop under 5 MB.
- **Public repos:** helper scripts that print copy commands or run unattended tend to pick up
  the machine's user, host name, address or home path. Keep those out of committed scripts and
  pages; take them from arguments or the environment.

### Reusable code in this skill

| File | What it is | Use |
|---|---|---|
| `scripts/render.mjs` | the renderer: footage, stat cards, smoke check | `--shots list.mjs`, `--cards`, `--smoke` (usage at the top of the file) |
| `scripts/stills.mjs` | README screenshots, GIFs, chart PNGs | `--stills list.mjs --size 1600x900` |
| `scripts/build_single.mjs` | the one-file live page | `--page … --data … --out visuals/dist/index.html` |
| `scripts/pagekit.mjs` | Chrome, ffmpeg, inlining, DevTools client | imported by the three above |
| `assets/lib/riso-core.js` | the drawing core: inks, halftone, pen, furniture, characters, type | loaded by every page |
| `assets/lib/director.js` | director-mode keys and legend | `installDirector({...})` (usage at the top) |
| `assets/world/` | starter world: two data-driven rooms, runtime, control surface; sample `data.json`, `shots.mjs`, `stills.mjs` | copy, then replace the rooms |
| `assets/statcard/` | stat-card template and a sample `stats.json` | the exporter writes the real `stats.json` |
| `assets/NOTICE.txt` | MIT notice and credits | keep it next to `riso-core.js` |

**Starting a new project:**

```bash
SKILL=~/.claude/skills/tacdel-video                  # or the unzipped skill folder
mkdir -p visuals scripts/video
cp -r "$SKILL"/assets/* visuals/                     # lib/ world/ statcard/ NOTICE.txt
cp "$SKILL"/scripts/*.mjs scripts/video/
printf 'results/\n*.mp4\n' >> .gitignore
python3 -m http.server 8000                          # then open localhost:8000/visuals/world/
```

Then, in order: bind the palette to the project's nouns; write the exporter (and a fake one)
that produces `visuals/world/data.json`; replace the starter rooms one at a time, running
`render.mjs --smoke` after each; write `shots.mjs` in chapter order and render; have the
exporter write `results/stats.json` and render the cards; build the single file; publish only
with permission.
