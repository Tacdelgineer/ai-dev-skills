#!/usr/bin/env python3
"""Check a voice take without listening to it (or pick the best of several, if you were asked for more).

  python3 pick_take.py script.txt take1.words.json [take2.words.json ...]

Each words.json holds the word timings of one take: voice.py's TTS alignment, or an ElevenLabs Scribe
transcript (creative_transcribe_audio -> words_download_url). Scores every take on: how closely the transcript matches the script (a skipped,
doubled or garbled word costs points), the speaking pace, and the longest pause (a long dead gap usually
means a glitch). Prints a table and the winner. Pace is a rough check on the voice settings: on full Short scripts the
final eleven_v4 settings (FINAL_VOICE.md) measured 148-168 words per minute. A one-sentence test has no pauses
and runs about 200 wpm, so the warning means nothing there. On a full script, a take far faster than that
means the request didn't carry FINAL_VOICE.md's settings.
"""
import difflib, json, re, sys

def words(path):
    d = json.load(open(path))
    if isinstance(d, dict):
        d = d.get('words') or (d.get('transcripts') or [{}])[0].get('words', [])
    return [w for w in d if w.get('type', 'word') == 'word']

NUM = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine', '10': 'ten',
       '12': 'twelve', '15': 'fifteen', '30': 'thirty', '100': 'hundred'}
def norm(s):
    s = re.sub(r"[^a-z0-9]", '', s.lower()); return NUM.get(s, s)

def main():
    script = [norm(w) for w in re.sub(r'<[^>]+>', ' ', open(sys.argv[1], encoding='utf-8').read()).split()]
    script = [w for w in script if w]
    rows = []
    for p in sys.argv[2:]:
        w = words(p); said = [norm(x['text']) for x in w]; said = [s for s in said if s]
        sm = difflib.SequenceMatcher(None, script, said, autojunk=False); ratio = sm.ratio()
        bad = [(tag, ' '.join(script[i1:i2]), ' '.join(said[j1:j2])) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
        dur = w[-1]['end'] - w[0]['start']; wpm = len(said) / dur * 60
        gaps = [b['start'] - a['end'] for a, b in zip(w, w[1:])]; mx = max(gaps) if gaps else 0
        score = ratio * 100 - max(0, abs(wpm - 150) - 12) * .6 - max(0, mx - 1.3) * 12
        rows.append((score, p, ratio, wpm, mx, dur, bad))
    rows.sort(reverse=True)
    print(f"{'score':>6} {'match':>6} {'wpm':>5} {'max gap':>8} {'length':>7}  take")
    for sc, p, r, wpm, mx, dur, bad in rows:
        print(f"{sc:6.1f} {r * 100:5.1f}% {wpm:5.0f} {mx:7.2f}s {dur:6.1f}s  {p}")
        for tag, a, b in bad[:6]: print(f"{'':>36}{tag}: script '{a}' -> heard '{b}'")
    best = rows[0]
    print(f"\nbest: {best[1]}")
    if best[3] > 175: print('WARNING: pace is above the final v4 settings — on a full script, check the request sent FINAL_VOICE.md\'s settings. One-sentence tests run fast; ignore it there.')
    if best[2] < .9: print('WARNING: the take drifts from the script; check the flagged words before using it.')

if __name__ == '__main__':
    main()
