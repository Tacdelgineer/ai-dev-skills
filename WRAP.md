# Wrap a finished project (tacdel channel)

The one end-of-video step for `tacdel-video`, `tacdel-shorts` and `tacdel-motion`: archive the keepers to the
owner's PC, verify them, then wipe the scratch. Approved by the owner on 2026-10-28 after a hand-run cleanup of
seven finished projects. `scripts/build.sh` copies this file into each tacdel skill zip.

**Runs only when the owner says "wrap <project>".** Never at the end of a render, never on a guess that a
project is finished, never on a project the owner didn't name.

## The rules

- **The PC pulls.** Never push to it, ask for logins, or set up a network service. Stage files on the box
  and hand the owner one pull command and one hash check.
- **Nothing is deleted before the owner says the hashes match.** Staging only copies.
- **Git:** delete only ignored or untracked media; tracked files stay. No history rewrites. A whole folder goes
  only when the owner says so.
- **Anything that fits neither list below gets listed, archived, and left in place until the owner decides.**
- Touch only the named project. No `docker prune` or system-wide cleanup. Don't stop processes you didn't start.

## Steps

1. **Check.** Read the project's STATUS/notes. Look for anything still running in the folder (`pgrep -af
   <folder>`, stale `*.pid` files). Record `df -B1 --output=used,avail /`.
2. **Freeze the source.**
   - Commit uncommitted source (never media). First grep for keys; credentials stay in `~/.tacdel.env`.
   - Add output rules to `.gitignore` where they're missing (`*.mp4`, `*.wav`, `*.mp3`, `*.m4a`, `work/`,
     `tmp/`, `.venv/`, `node_modules/`, frame folders).
   - No remote? Write `git bundle create <outbox>/<slug>.bundle --all` and check it with `git bundle verify`.
3. **Sort.** Start from the defaults and show the owner the list with sizes:

   | Archive (to the PC) | Wipe (no copy) |
   |---|---|
   | master, Shorts, `final_footage/` with `ORDER.txt` | PNG frame folders and raw takes |
   | stat cards, charts, posters, thumbnails | `work/`, `tmp/`, `scratch/`, intermediate render MP4s |
   | captions, description, chapters, POST.md | contact sheets (`sheet*.png`, `contact.png`) |
   | voice takes and word timings, `chunks.txt`, script | `.venv`, `node_modules`, `.pw`, `.npm-cache`, `_repo` copies, `__pycache__` |
   | scene/chapter code, `page.html`, `events.json`, sfx, data and results | per-chapter renders and unused takes |

   Before wiping any takes or renders, `cmp` every used one against its copy in the final folder (via
   `ORDER.txt`). Wipe only if all are byte-identical.
4. **Stage.** Copy the archive set to `~/archive-outbox/<YYYY-MM-DD>_<slug>/` with paths mirrored. Then:
   - Write `manifest.txt` in `sha256sum` format with paths relative to the folder:
     `find . -type f ! -name manifest.txt -print0 | sort -z | xargs -0 sha256sum | sed 's#  \./#  #'`
   - `cmp` every staged file against its source.
5. **Hand over and stop.** Give the owner these two commands. `<user>@<host>` is the box as the PC reaches it:
   the SSH host alias, or `whoami` and the box's Tailscale address. Several projects staged on the same day go
   in one pull with `<date>_*`.

   ```powershell
   mkdir -Force D:\1MDrive\Tacdel\Archive | Out-Null; scp -r '<user>@<host>:archive-outbox/<date>_<slug>' D:\1MDrive\Tacdel\Archive\
   ```
   ```powershell
   Get-ChildItem D:\1MDrive\Tacdel\Archive\<date>_<slug> -Directory | % { $n=$_.Name; $d=$_.FullName; $m=Get-Content "$d\manifest.txt"; $bad=0; foreach($l in $m){ $h,$p=$l -split '  ',2; $f=Join-Path $d $p; if(!(Test-Path -LiteralPath $f) -or (Get-FileHash -LiteralPath $f -Algorithm SHA256).Hash -ne $h){ "BAD $n/$p"; $bad++ } }; "${n}: $bad bad of $($m.Count)" }
   ```
   Every folder must print `0 bad`. Then stop and wait.
6. **Wipe, after the owner says the hashes match.**
   - First check that nothing in the project is newer than the manifest
     (`find <folder> -newer <outbox>/manifest.txt -not -path '*/.git/*'`). If anything is, stop and ask.
   - Then delete the wipe set and the archived ignored media, and delete the outbox folder.
   - Run `git gc` only if the owner OKs it.
   - Files owned by root (Docker output) can't be removed without sudo. List them for the owner instead.
7. **Report.** Give `df` used/free before and after, GB freed, what was archived, and what was skipped and why.
   Add one line to `~/archive-log.md` on the box: date, project, archive folder, file count, size, freed.
