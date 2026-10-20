#!/usr/bin/env python3
"""Word timings -> captions, or re-time a finished Short to a new voice take.

  python3 timing.py caps words.json chunks.txt                  print a CAPS array for a new Short
  python3 timing.py warp words.json chunks.txt page.html [--write]   print (or write) WARP + DUR so a
                                                                   finished Short follows a new take

words.json  ElevenLabs transcript words (creative_transcribe_audio -> words_download_url), a list of
            {"text","type","start","end"} or a dict holding that list under "words".
chunks.txt  one caption chunk per line, in the words the voice SAYS ("sixty-two"); add " || shown text"
            to show it differently on screen ("62.5"). Same order and count as the page's CAPS.
"""
import json, re, sys

def load_words(path):
    d = json.load(open(path))
    if isinstance(d, dict):
        d = d.get('words') or (d.get('transcripts') or [{}])[0].get('words', [])
    return [w for w in d if w.get('type', 'word') == 'word']

def load_chunks(path):
    out = []
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip():
            continue
        say, _, show = line.partition(' || ')
        out.append((say.strip(), (show or say).strip()))
    return out

norm = lambda s: re.sub(r"[^a-z0-9]", '', s.lower())

def chunk_times(words, chunks):
    """Walk the transcript once; each spoken token eats one word (with a 3-word look-ahead to resync)."""
    out, i = [], 0
    for say, show in chunks:
        toks = [norm(x) for x in say.split() if norm(x)]
        start = end = None
        for tok in toks:
            j = i
            while j < min(len(words), i + 3) and norm(words[j]['text']) != tok:
                j += 1
            if j < len(words) and norm(words[j]['text']) == tok:
                i = j
            w = words[min(i, len(words) - 1)]
            start = w['start'] if start is None else start
            end = w['end']
            i += 1
        out.append((show, round(start, 2), round(end, 2)))
    return out

def js_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"

def old_caps(html):
    block = re.search(r'const CAPS = \[(.*?)\n\];', html, re.S).group(1)
    return [(float(a), float(b)) for a, b in re.findall(r"'(?:[^'\\]|\\.)*'\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*\]", block)]

def main():
    mode, words, chunks = sys.argv[1], load_words(sys.argv[2]), load_chunks(sys.argv[3])
    caps = chunk_times(words, chunks)
    if mode == 'caps':
        print('const CAPS = [\n' + ''.join(f'  [{js_str(s)}, {a}, {b}],\n' for s, a, b in caps) + '];')
        print(f'// voice ends at {caps[-1][2]} s; set DUR about 1.2 s later')
        return
    page = sys.argv[4]; html = open(page, encoding='utf-8').read(); old = old_caps(html)
    if len(old) != len(caps):
        sys.exit(f'chunk count {len(caps)} != CAPS count {len(old)} in {page}')
    dur_old = float(re.search(r'DUR = ([\d.]+)', html).group(1))
    anchors = [(0.0, 0.0)]
    for (s, e), (_, ns, ne) in zip(old, caps):
        for new_t, old_t in ((ns, s), (ne, e)):
            if new_t > anchors[-1][0] and old_t > anchors[-1][1]:
                anchors.append((new_t, old_t))
    tail = dur_old - old[-1][1]
    dur_new = round(caps[-1][2] + tail, 1)
    anchors.append((dur_new, dur_old))
    warp = 'const WARP = [' + ', '.join(f'[{a:g}, {b:g}]' for a, b in anchors) + '];'
    print(warp); print(f'DUR = {dur_new}  (was {dur_old})')
    if '--write' in sys.argv:
        html = re.sub(r'const WARP = \[.*?\];', warp, html, count=1)
        html = re.sub(r'DUR = [\d.]+', f'DUR = {dur_new}', html, count=1)
        open(page, 'w', encoding='utf-8').write(html); print('written', page)

if __name__ == '__main__':
    main()
