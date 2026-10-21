#!/usr/bin/env python3
"""Voice takes straight from the ElevenLabs API, with word timings, then pick the best one.

  ELEVENLABS_API_KEY=... ELEVENLABS_VOICE_ID=... python3 voice.py script.txt [out_dir]

Calls text-to-speech "with-timestamps" on eleven_multilingual_v2 twice. It sends no voice_settings, so
the voice's stored settings apply (see "One-time setup" in SKILL.md). Writes take1.mp3/take2.mp3 and
take1.words.json/take2.words.json in the shape timing.py and pick_take.py read, runs pick_take.py
(full report in pick.txt) and copies the winner to voice.mp3 + words.json. Prints a short summary
only: no audio, base64, keys, voice ids or URLs. Costs about 1 credit per character per take.
"""
import base64, json, os, re, shutil, subprocess, sys, urllib.error, urllib.request

TAKES = 2
MODEL = 'eleven_multilingual_v2'
HERE = os.path.dirname(os.path.abspath(__file__))

def speak(text, key, voice):
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps',
                                 data=json.dumps({'text': text, 'model_id': MODEL}).encode(),
                                 headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=300) as r: return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'replace')
        try: msg = json.loads(body).get('detail', body)
        except ValueError: msg = body
        if isinstance(msg, dict): msg = msg.get('message') or msg.get('status') or json.dumps(msg)
        sys.exit(f'ElevenLabs HTTP {e.code}: {str(msg)[:160]}')
    except urllib.error.URLError as e:
        sys.exit(f'ElevenLabs request failed: {str(e.reason)[:160]}')

def words_from_alignment(al):
    """Character timings -> [{"text","type","start","end"}]. Whitespace splits words; <break .../> tags are skipped."""
    out, cur, tag = [], None, False
    for ch, s, e in zip(al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']):
        if ch == '<': tag = True
        if tag or ch.isspace():
            if cur: out.append(cur); cur = None
            if ch == '>': tag = False
            continue
        if cur is None: cur = {'text': ch, 'type': 'word', 'start': round(s, 3), 'end': round(e, 3)}
        else: cur['text'] += ch; cur['end'] = round(e, 3)
    if cur: out.append(cur)
    return out

def main():
    if len(sys.argv) < 2: sys.exit(__doc__.strip().splitlines()[2].strip())
    key, voice = os.environ.get('ELEVENLABS_API_KEY'), os.environ.get('ELEVENLABS_VOICE_ID')
    if not key or not voice: sys.exit('set ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID in the environment')
    script = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else '.'
    os.makedirs(out, exist_ok=True)
    text = open(script, encoding='utf-8').read().strip()
    spoken = re.sub(r'<[^>]+>', ' ', text)
    print(f'{len(spoken.split())} words, {len(text)} chars x {TAKES} takes (~{len(text) * TAKES} credits)')
    wjs = []
    for n in range(1, TAKES + 1):
        d = speak(text, key, voice)
        mp3, wj = os.path.join(out, f'take{n}.mp3'), os.path.join(out, f'take{n}.words.json')
        open(mp3, 'wb').write(base64.b64decode(d['audio_base64']))
        w = words_from_alignment(d.get('alignment') or d['normalized_alignment'])
        json.dump({'words': w}, open(wj, 'w'))
        print(f'take{n}: {len(w)} words, {w[-1]["end"] if w else 0:.1f} s, {os.path.getsize(mp3) // 1024} KB')
        wjs.append(wj)
    r = subprocess.run([sys.executable, os.path.join(HERE, 'pick_take.py'), script, *wjs], capture_output=True, text=True)
    report = r.stdout + r.stderr
    open(os.path.join(out, 'pick.txt'), 'w').write(report)
    # table rows, winner and warnings only; the per-word diffs stay in pick.txt
    for line in report.splitlines():
        if line.strip() and not line.startswith(' ' * 20): print(line)
    best = re.search(r'^best: (.+)$', report, re.M)
    if r.returncode or not best: sys.exit('pick_take.py failed; see pick.txt')
    wj = best.group(1).strip()
    shutil.copy(wj, os.path.join(out, 'words.json'))
    shutil.copy(wj.replace('.words.json', '.mp3'), os.path.join(out, 'voice.mp3'))
    print(f'-> voice.mp3 + words.json = {os.path.basename(wj).split(".")[0]}  (details: pick.txt)')

if __name__ == '__main__':
    main()
