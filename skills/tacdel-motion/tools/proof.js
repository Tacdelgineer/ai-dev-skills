/* ---------- proof beat + cast line (tacdel-motion tools/proof.js) ----------
   For experiment Shorts. Paste this block into the page after CAPS / S() / the CUES array and before draw().
   1. Set PROOF = { t0, t1, key } in page time: 2-3 s at the reveal, key = the log record proof.sh filmed.
      Leave PROOF = null for story Shorts.
   2. Call proofWin(t) in draw() after the scenes and before the captions. It dims the frame and draws the terminal
      window; `proof.sh overlay` lays the real VHS clip into PROOF_BOX after the render, frame-exact.
   3. Call castLine(a, runs) whenever results are on screen: the model names and the run count.
   Uses only ctx, W and H. Recolour PROOF_STYLE to match the look. */
const PROOF = null;                      // e.g. { t0: S(24) - .1, t1: S(26) + .4, key: 'qwen|excited|r1' }
const CAST = ['Claude', 'Qwen 3.6', 'Nemotron 3 Nano', 'Devstral', 'GLM-4'];   // the models actually run, in this order
const PROOF_BOX = { x: 60, y: 520, w: 960, h: 560 };   // where the 960x560 clip lands; keep it inside y 220-1380
const PROOF_STYLE = { shade: 'rgba(6,9,20,.75)', frame: '#1a2244', screen: '#0b1026', title: '#ffcf4d', text: '#eef2ff',
  dim: 'rgba(238,242,255,.6)', dots: ['#ff5d6c', '#ffcf4d', '#5ef2c9'], font: '"Inter","Helvetica Neue",Arial,sans-serif', mono: '"DejaVu Sans Mono",monospace' };
if (PROOF) { Object.assign(PROOF, PROOF_BOX); if (typeof cue === 'function') cue(PROOF.t0 - .05, 'typing', .35, 1, 0, 1.0); }
window.PROOF = PROOF;                    // proof.sh overlay reads this

function proofWin(t) {
  if (!PROOF) return; const a = Math.min(1, Math.max(0, (t - PROOF.t0 + .2) / .2)) * (1 - Math.min(1, Math.max(0, (t - PROOF.t1 + .2) / .2)));
  if (a <= 0) return; const { x, y, w, h } = PROOF_BOX, S_ = PROOF_STYLE;
  ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = S_.shade; ctx.fillRect(0, 0, W, H);
  ctx.shadowColor = 'rgba(0,0,0,.45)'; ctx.shadowBlur = 24; ctx.shadowOffsetY = 10; ctx.fillStyle = S_.frame;
  ctx.beginPath(); ctx.roundRect(x - 14, y - 110, w + 28, h + 124, 26); ctx.fill(); ctx.shadowColor = 'transparent';
  S_.dots.forEach((c, i) => { ctx.fillStyle = c; ctx.beginPath(); ctx.arc(x + 22 + i * 34, y - 66, 10, 0, 7); ctx.fill(); });
  ctx.textAlign = 'left'; ctx.fillStyle = S_.title; ctx.font = `900 30px ${S_.font}`; ctx.fillText('REAL RUN LOG', x + 130, y - 56);
  ctx.textAlign = 'right'; ctx.fillStyle = S_.dim; ctx.font = `800 26px ${S_.mono}`; ctx.fillText('logs/calls.jsonl', x + w - 10, y - 56);
  ctx.fillStyle = S_.screen; ctx.beginPath(); ctx.roundRect(x, y, w, h, 6); ctx.fill();
  ctx.textAlign = 'center'; ctx.fillStyle = S_.text; ctx.font = `800 32px ${S_.font}`; ctx.fillText("the model's answer as saved, unedited", W / 2, y + h + 70);
  ctx.restore(); }

function castLine(a, runs, y = 1398) {
  if (a <= 0) return; ctx.save(); ctx.globalAlpha *= Math.min(1, a); ctx.textAlign = 'center'; ctx.fillStyle = PROOF_STYLE.dim;
  ctx.font = `800 27px ${PROOF_STYLE.font}`; ctx.fillText(CAST.join(' · '), W / 2, y); ctx.fillText(runs, W / 2, y + 38); ctx.restore(); }
