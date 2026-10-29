#!/usr/bin/env python3
"""Print one logged model answer, as it was saved by the run: the command filmed for a Short's proof beat.

  answer.py 'claude|split|r2' [--from WORD] [--lines 8] [--width 42] [--log logs/calls.jsonl]

The log is the experiment's JSONL, one record per model call: {"key", "model", "run", "t", "answer", "error"}.
The last record with that key and no error is the one printed.

Prints the model id, run and time from the log record, then the answer wrapped to --width columns. --from starts
the excerpt at the first line that contains WORD (marked with "..."). Markdown bold/headers are stripped for
reading; no words are changed.
"""
import argparse, json, re, textwrap

ap = argparse.ArgumentParser()
ap.add_argument('key'); ap.add_argument('--from', dest='frm'); ap.add_argument('--lines', type=int, default=8)
ap.add_argument('--width', type=int, default=42); ap.add_argument('--log', default='logs/calls.jsonl')
a = ap.parse_args()
rec = None
for line in open(a.log):
    r = json.loads(line)
    if r.get('key') == a.key and not r.get('error'): rec = r
if rec is None: raise SystemExit(f'no answer logged for {a.key}')
text = re.sub(r'\*\*|__|^#+\s*|`', '', rec['answer'], flags=re.M)
paras = [p.strip() for p in text.split('\n') if p.strip() and not re.fullmatch(r'[|\-: ]+', p.strip())]
start = next((i for i, p in enumerate(paras) if a.frm and a.frm.lower() in p.lower()), 0)
out, used = [], start
for p in paras[start:]:
    out += textwrap.wrap(p, a.width) or ['']; used += 1
    if len(out) >= a.lines: break
when = rec.get('t', '').replace('T', ' ')[:16]
print(f"\033[36m{rec['model']}\033[0m  run {rec.get('run', '?')}  {when}")
if start: print('...')
for l in out[:a.lines]: print(l)
if len(out) > a.lines or used < len(paras): print('...')
