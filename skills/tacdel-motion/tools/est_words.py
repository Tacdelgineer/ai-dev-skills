#!/usr/bin/env python3
"""Estimated word timings for a script (fallback when no voice can be made yet): model fitted on Alireza's real takes,
calibrated on today's connector sample, then slowed for speed 0.93. Output = words.json shape."""
import json, re, sys
SPEED = 0.93
def raw(text):
    text = re.sub(r'<break time="([\d.]+)s" />', r' <BRK\1> ', text)
    out, t = [], 0.12
    toks = text.split()
    for i, tok in enumerate(toks):
        m = re.match(r'<BRK([\d.]+)>', tok)
        if m: t += float(m.group(1)); continue
        n = len(re.sub('[^A-Za-z0-9]', '', tok))
        d = 0.035 + 0.055 * n
        out.append({'text': tok, 'type': 'word', 'start': t, 'end': t + d}); t += d
        end = tok[-1]
        t += 0.50 if end in '.!?' else 0.20 if end in ',:;' else 0.055
    return out
def est(text, cal):
    w = raw(text)
    for x in w: x['start'] = round(x['start'] * cal / SPEED, 3); x['end'] = round(x['end'] * cal / SPEED, 3)
    return w
if __name__ == '__main__':
    sample = "Imagine you hire a hundred AI agents. They never sleep, and they have one job: build me a website. Here's what happens."
    r = raw(sample); cal = 0.90   # between past takes (1.0) and today's faster sample (0.815)
    if sys.argv[1] == 'cal': print('cal', round(cal, 3)); sys.exit()
    w = est(open(sys.argv[1]).read(), cal)
    json.dump({'words': w}, open(sys.argv[2], 'w'))
    print(sys.argv[1], 'est. voice ends at', w[-1]['end'], 's')
