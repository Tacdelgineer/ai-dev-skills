#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy>=1.26", "scipy>=1.11"]
# ///
"""tacdel episode audio: original code-composed music + SFX (synth + ElevenLabs files) + optional voice, mixed.

  uv run sound.py <page.html> <out.m4a> [voice.mp3]

Reads CUES / MUSIC / DUR / WARP / CAPS from the page (page time) and maps them to video time through the
page's WARP (so a re-timed page keeps its sounds on the action). Music ducks under the voice; with no voice
file it ducks under the caption timing so the review mix already sits where the final will.
All music here is composed in code for these videos (no samples, no third-party tracks).
"""
import json, os, subprocess, sys
import numpy as np
from scipy.signal import butter, lfilter, fftconvolve

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
SFXDIR = os.path.join(HERE, 'sfx')
rng = np.random.default_rng(7)

def tt(d): return np.arange(int(d * SR)) / SR
def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def bp(x, lo, hi, o=2): b, a = butter(o, [lo / (SR / 2), min(hi / (SR / 2), .99)], 'band'); return lfilter(b, a, x)
def hp(x, f, o=2): b, a = butter(o, f / (SR / 2), 'high'); return lfilter(b, a, x)
def lp(x, f, o=2): b, a = butter(o, min(f / (SR / 2), .99), 'low'); return lfilter(b, a, x)
def norm(x, peak=.89): m = np.max(np.abs(x)) or 1; return x / m * peak
def att(x, a=.002): n = max(1, int(a * SR)); x = x.copy(); x[:n] *= np.linspace(0, 1, n); return x
def fade_tail(x, r=.01): n = min(len(x), max(1, int(r * SR))); x = x.copy(); x[-n:] *= np.linspace(1, 0, n); return x

# ---------------------------------------------------------------- synth SFX
def s_pop(r=1):
    t = tt(.11); f = 260 * r + 700 * r * np.exp(-t * 45); ph = 2 * np.pi * np.cumsum(f) / SR
    return att(np.sin(ph) * np.exp(-t * 30) + .2 * hp(rng.standard_normal(len(t)), 2000) * np.exp(-t * 200))
def s_tick(r=1):
    t = tt(.05); return att(.6 * np.sin(2 * np.pi * 2600 * r * t) * np.exp(-t * 120) + .5 * hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 260), .0005)
def s_click(r=1):
    t = tt(.04); return att(np.sin(2 * np.pi * 1500 * r * t) * np.exp(-t * 160) + .6 * bp(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t * 300), .0003)
def s_key(r=1): return s_click(.8 * r) * .9
def s_whoosh(r=1, d=.5):
    d = d / r; t = tt(d); n = rng.standard_normal(len(t)); u = t / d
    lo = bp(n, 300, 1400); hi = bp(n, 1400, 5000); mixu = np.clip(u * 1.4, 0, 1)
    return (lo * (1 - mixu) + hi * mixu) * np.sin(np.pi * u) ** 1.5 * 1.6
def s_swish(r=1): return s_whoosh(r * 1.6, .32)
def s_wipe(r=1): return s_whoosh(r * .9, .55)
def s_thunk(r=1):
    t = tt(.35); f = 48 * r + 90 * r * np.exp(-t * 25); ph = 2 * np.pi * np.cumsum(f) / SR
    return att(np.sin(ph) * np.exp(-t * 11) + .35 * lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 40))
def bell(f, d=1.4, amp=1.):
    t = tt(d); x = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * dk) for k, a, dk in ((1, 1, 2.6), (2.756, .45, 6), (5.404, .22, 12), (8.933, .1, 20)))
    return att(x * amp, .001)
def s_ding(r=1): return bell(1320 * r, 1.6)
def s_coin(r=1): x = bell(1760 * r, .35) * .8; y = bell(2350 * r, .5); out = np.zeros(int(.6 * SR)); out[:len(x)] += x; o = int(.06 * SR); out[o:o + len(y)] += y; return out
def s_sparkle(r=1):
    out = np.zeros(int(.8 * SR))
    for k in range(7): f = 2200 * r * 2 ** (rng.integers(0, 8) / 12); o = int((k * .055 + rng.random() * .02) * SR); b = bell(f, .45, .5 - k * .04); out[o:o + len(b)] += b[:len(out) - o]
    return out
def s_chime(r=1):
    out = np.zeros(int(1.8 * SR))
    for k, m in enumerate((84, 88, 91, 96)): b = bell(mtof(m) * r, 1.4, .6); o = int(k * .09 * SR); out[o:o + len(b)] += b[:len(out) - o]
    return out
def s_blip(r=1):
    t = tt(.09); x = np.sign(np.sin(2 * np.pi * 880 * r * t)) * .35 + np.sin(2 * np.pi * 880 * r * t) * .5; return att(lp(x, 4000) * np.exp(-t * 30))
def s_wink(r=1):
    a = s_blip(1.0 * r); b = s_blip(1.5 * r); out = np.zeros(len(a) + int(.07 * SR) + len(b)); out[:len(a)] += a; o = int(.07 * SR); out[o:o + len(b)] += b; return out
def s_riser(r=1, d=2.0):
    t = tt(d); f = 180 * r * 2 ** (t / d * 2.2); ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + .35 * np.sin(2 * ph)) * (t / d) ** 1.6 + .5 * bp(rng.standard_normal(len(t)), 2000, 8000) * (t / d) ** 2.5
    return fade_tail(x, .04)
def s_freeze(r=1):
    t = tt(.6); f = 2600 * r * np.exp(-t * 2.5) + 600; ph = 2 * np.pi * np.cumsum(f) / SR
    return att(np.sin(ph) * np.exp(-t * 5) * .6 + bell(3300 * r, .6, .3)[:len(t)])
def s_roll(r=1):
    t = tt(.4 / r); n = lp(rng.standard_normal(len(t)), 700) * (1 + .6 * np.sin(2 * np.pi * 22 * t)); return n * np.sin(np.pi * t / t[-1]) * 2.2
def s_splat(r=1):
    t = tt(.22); x = lp(rng.standard_normal(len(t)), 1800 * r) * np.exp(-t * 26) * 1.8 + np.sin(2 * np.pi * (120 * r) * t) * np.exp(-t * 30) * .7; return att(x, .001)
def s_boing(r=1):
    t = tt(.6); f = 260 * r * (1 + .35 * np.sin(2 * np.pi * 11 * t) * np.exp(-t * 5)) * (1 + .5 * np.exp(-t * 10)); ph = 2 * np.pi * np.cumsum(f) / SR
    return att(np.sin(ph) * np.exp(-t * 4.5))
def s_whirr(r=1, d=1.):
    t = tt(d); x = np.sin(2 * np.pi * 180 * r * t + 3 * np.sin(2 * np.pi * 9 * t)) * .5 + .3 * bp(rng.standard_normal(len(t)), 800, 3000); return x * np.minimum(1, np.minimum(t / .1, (t[-1] - t) / .2))
def s_beep(r=1):
    t = tt(.14); return att(lp(np.sign(np.sin(2 * np.pi * 1040 * r * t)), 5000) * .5 * np.minimum(1, (t[-1] - t) / .01))
def s_ping(r=1):  # phone notification: two soft tones
    a = bell(1568 * r, .5, .7); b = bell(2093 * r, .8, .8); out = np.zeros(int(.9 * SR)); out[:len(a)] += a; o = int(.09 * SR); out[o:o + len(b)] += b[:len(out) - o]; return out
def s_radar(r=1):
    t = tt(.3); return att(np.sin(2 * np.pi * 1200 * r * t) * np.exp(-t * 14) * .8 + np.sin(2 * np.pi * 2400 * r * t) * np.exp(-t * 30) * .2)
def s_alarm(r=1):
    out = np.zeros(int(.75 * SR))
    for k in range(3): b = s_beep(r * (1 if k % 2 == 0 else .84)); o = int(k * .24 * SR); out[o:o + len(b)] += b
    return out
def s_steam(r=1):
    t = tt(1.4); return hp(rng.standard_normal(len(t)), 3500) * np.sin(np.pi * t / t[-1]) ** 2 * .6
def s_hum(r=1, d=2.5):
    t = tt(d); x = sum(np.sin(2 * np.pi * 110 * r * k * t) / k for k in (1, 2, 3)) * .4; return x * np.minimum(1, np.minimum(t / .4, (t[-1] - t) / .5))
def s_lock(r=1):
    a = s_click(.7 * r); b = s_click(1.1 * r); out = np.zeros(int(.2 * SR)); out[:len(a)] += a; o = int(.08 * SR); out[o:o + len(b)] += b * 1.2; return out
def s_spin(r=1):
    t = tt(.8); f = 400 * r * (1 + 1.5 * np.sin(np.pi * t / .8)); ph = 2 * np.pi * np.cumsum(f) / SR; return np.sin(ph) * np.sin(np.pi * t / .8) * .5 + s_whoosh(1, .8)[:len(t)] * .5

SYN = dict(pop=s_pop, tick=s_tick, click=s_click, key=s_key, whoosh=s_whoosh, swish=s_swish, wipe=s_wipe, thunk=s_thunk, ding=s_ding, coin=s_coin,
           sparkle=s_sparkle, chime=s_chime, blip=s_blip, wink=s_wink, riser=s_riser, freeze=s_freeze, roll=s_roll, splat=s_splat, boing=s_boing,
           whirr=s_whirr, beep=s_beep, ping=s_ping, radar=s_radar, alarm=s_alarm, steam=s_steam, hum=s_hum, lock=s_lock, spin=s_spin)

def load_audio(path, stereo=False):
    ch = 2 if stereo else 1
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', str(ch), '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    return x.reshape(-1, 2) if stereo else x
_FILE = {}
def file_sfx(name):
    if name not in _FILE:
        x = load_audio(os.path.join(SFXDIR, name + '.mp3')); pk = np.max(np.abs(x)) or 1
        on = np.argmax(np.abs(x) > pk * .12); on = max(0, on - int(.004 * SR))
        x = x[on:]; x = norm(x, .89); _FILE[name] = x
    return _FILE[name]
def stamp_sfx(r=1):  # the generated stamp is quiet and thin: layer it on a synth thunk for weight
    f = file_sfx('stamp'); th = s_thunk(1.25 * r) * .7; out = np.zeros(max(len(f), len(th))); out[:len(f)] += f * .9; out[:len(th)] += th; return out
def get_sfx(name, r=1.):
    if name == 'stamp': x = stamp_sfx(r)
    elif name in SYN: x = SYN[name](r)
    elif os.path.exists(os.path.join(SFXDIR, name + '.mp3')):
        x = file_sfx(name)
        if abs(r - 1) > 1e-3: n = int(len(x) / r); x = np.interp(np.arange(n) * r, np.arange(len(x)), x)
    else: raise SystemExit(f'unknown sfx {name}')
    return x

# ---------------------------------------------------------------- instruments
def inst_marimba(f, d, v=1.):
    t = tt(min(d + .6, 1.6)); x = np.sin(2 * np.pi * f * t) * np.exp(-t * 5.5) + .32 * np.sin(2 * np.pi * 3.93 * f * t) * np.exp(-t * 16) + .08 * np.sin(2 * np.pi * 9.2 * f * t) * np.exp(-t * 40)
    return att(x * v, .0015)
def inst_epiano(f, d, v=1.):
    t = tt(d + .9); I = 1.6 * np.exp(-t * 3) + .22; x = np.sin(2 * np.pi * f * t + I * np.sin(2 * np.pi * f * t)) * np.exp(-t * 1.3) + .12 * np.sin(2 * np.pi * 7 * f * t) * np.exp(-t * 14)
    rel = np.clip(1 - (t - d) / .5, 0, 1); return att(x * rel * v, .003)
def inst_glock(f, d, v=1.): return bell(f, min(2.2, d + 1.2), v)
def inst_pluck(f, d, v=1.):  # soft pizzicato
    t = tt(min(d + .3, .9)); x = (np.sin(2 * np.pi * f * t) + .4 * np.sin(4 * np.pi * f * t) + .15 * np.sin(6 * np.pi * f * t)) * np.exp(-t * 9); return att(x * v, .002)
def inst_bass(f, d, v=1.):
    t = tt(d + .25); x = np.sin(2 * np.pi * f * t) + .28 * np.sin(4 * np.pi * f * t) + .08 * np.sin(6 * np.pi * f * t)
    e = np.exp(-t * 2.2) * np.clip(1 - (t - d) / .2, 0, 1); return att(x * e * v, .006)
def inst_pad(f, d, v=1.):
    t = tt(d + 1.0); vib = 1 + .003 * np.sin(2 * np.pi * 4.8 * t)
    x = sum(np.sin(2 * np.pi * f * k * vib * t * (1 + det)) / k / (1 + (k * f / 1400) ** 2) for k in range(1, 7) for det in (-.003, .003)) * .5
    e = np.minimum(1, t / .5) * np.clip(1 - (t - d) / 1.0, 0, 1); return x * e * v
def inst_musicbox(f, d, v=1.):
    t = tt(1.4); x = np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2) + .35 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 9) + .12 * np.sin(2 * np.pi * 5.1 * f * t) * np.exp(-t * 18)
    return att(x * v, .0008)
def drum_kick(v=1.):
    t = tt(.4); f = 46 + 110 * np.exp(-t * 30); ph = 2 * np.pi * np.cumsum(f) / SR; return att(np.sin(ph) * np.exp(-t * 8) * v + .15 * v * hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 300), .001)
def drum_clap(v=1.):
    t = tt(.25); n = bp(rng.standard_normal(len(t)), 900, 5000); e = np.exp(-t * 18) + .6 * np.exp(-((t - .012) ** 2) / .00002) + .5 * np.exp(-((t - .024) ** 2) / .00002)
    return n * e * v * .8 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25) * v * .25
def drum_hat(v=1.):
    t = tt(.06); return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * 70) * v * .7
def drum_shaker(v=1.):
    t = tt(.08); return hp(rng.standard_normal(len(t)), 5000) * np.sin(np.pi * t / t[-1]) ** 2 * v * .45
def drum_wood(v=1.):
    t = tt(.08); return att(np.sin(2 * np.pi * 1250 * t) * np.exp(-t * 60) * v * .7 + np.sin(2 * np.pi * 2500 * t) * np.exp(-t * 90) * v * .2, .0005)
def drum_snare(v=1.):
    t = tt(.22); return (bp(rng.standard_normal(len(t)), 1500, 7000) * np.exp(-t * 20) * .7 + np.sin(2 * np.pi * 200 * t) * np.exp(-t * 30) * .4) * v
def inst_chip(f, d, v=1.):  # soft square lead (odd harmonics), for the terminal look
    t = tt(min(d + .15, 1.2)); x = sum(np.sin(2 * np.pi * f * h * t) / h for h in (1, 3, 5, 7)) * np.exp(-t * 4) * np.clip(1 - (t - d) / .1, 0, 1); return att(lp(x * v * .8, 3200), .004)
INST = dict(chip=inst_chip, marimba=inst_marimba, epiano=inst_epiano, glock=inst_glock, pluck=inst_pluck, bass=inst_bass, pad=inst_pad, musicbox=inst_musicbox)
DRUM = dict(kick=drum_kick, clap=drum_clap, hat=drum_hat, shaker=drum_shaker, wood=drum_wood, snare=drum_snare)

# chord name -> midi notes (root position, mid register)
NOTE = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}
def chord(name):
    q = 'maj'; root = name
    for suf in ('maj7', 'm7', 'sus', '7', 'm'):
        if name.endswith(suf) and name[:-len(suf)] in NOTE: root, q = name[:-len(suf)], suf; break
    r = 48 + NOTE[root]; iv = {'maj': (0, 4, 7), 'm': (0, 3, 7), '7': (0, 4, 7, 10), 'maj7': (0, 4, 7, 11), 'm7': (0, 3, 7, 10), 'sus': (0, 5, 7)}[q]
    return r, [r + i for i in iv]

# ---------------------------------------------------------------- arranger
def render_section(spec, dur, bpm, seed, tail=2.0):
    """spec: {'chords': [...], 'layers': {name: level}, 'inst': {...}}; returns mono-ish stereo pair (L,R)."""
    r = np.random.default_rng(seed); n = int((dur + tail) * SR); L = np.zeros(n); R = np.zeros(n)
    beat = 60 / bpm; bar = 4 * beat; chords = spec.get('chords', ['C']); lay = spec.get('layers', {}); swing = spec.get('swing', 0.)
    def put(x, t0, g=1., pan=0.):
        i = int(t0 * SR)
        if i >= n or i < 0: return
        x = x[:n - i]; L[i:i + len(x)] += x * g * (1 - max(0, pan)); R[i:i + len(x)] += x * g * (1 + min(0, pan))
    def sw(pos):  # swing 8ths
        return pos + (swing * beat / 2 if (round(pos / (beat / 2)) % 2 == 1) else 0)
    nb = int(np.ceil(dur / bar)) + 1
    for b in range(nb):
        t0 = b * bar
        if t0 >= dur: break
        root, notes = chord(chords[b % len(chords)])
        for name, lv in lay.items():
            kind, _, inst = name.partition(':'); fn = INST.get(inst or spec.get('lead', 'marimba'), inst_marimba)
            if kind == 'arp8' or kind == 'arp16' or kind == 'wonky':
                step = beat / 2 if kind != 'arp16' else beat / 4; seq = [notes[0] + 12, notes[1] + 12, notes[2] + 12, notes[0] + 24, notes[2] + 12, notes[1] + 12]
                for k in range(int(round(bar / step))):
                    m = seq[k % len(seq)] + spec.get('oct', 0) * 12; f = mtof(m) * (2 ** (r.normal(0, .012)) if kind == 'wonky' else 1)
                    put(fn(f, step, .55 + .25 * (k % 4 == 0) + r.random() * .1), t0 + sw(k * step) + r.normal(0, .004), lv, (k % 2 - .5) * .5)
            elif kind == 'stab':
                for pos in (0, 1.5 * beat, 3 * beat):
                    for m in notes: put(fn(mtof(m + 12 + spec.get('oct', 0) * 12), beat * .4, .45), t0 + pos, lv / len(notes) * 1.6)
            elif kind == 'offbeat':
                for k in range(4): m = notes[(k + b) % len(notes)] + 24 + spec.get('oct', 0) * 12; put(fn(mtof(m), beat * .3, .6), t0 + k * beat + beat / 2 + r.normal(0, .005), lv, .3 if k % 2 else -.3)
            elif kind == 'clock':
                for k in range(4): m = notes[2] + 24 + (12 if k == 0 else 0) + spec.get('oct', 0) * 12; put(fn(mtof(m), beat * .5, .5 + .3 * (k == 0)), t0 + k * beat, lv, -.2)
            elif kind == 'chords':
                for m in notes: put(fn(mtof(m + 12), bar * .95, .5), t0 + r.normal(0, .006), lv / len(notes) * 1.5)
            elif kind == 'chords2':
                for pos in (0, 2 * beat):
                    for m in notes: put(fn(mtof(m + 12), beat * 1.8, .5), t0 + pos + r.normal(0, .006), lv / len(notes) * 1.5)
            elif kind == 'pad':
                for m in notes: put(inst_pad(mtof(m + 12), bar), t0, lv / len(notes) * 1.2, (m % 3 - 1) * .3)
            elif kind == 'mel':
                mel = spec.get('mel', [[0, 2, 1]]); ph = mel[b % len(mel)]
                for (pos, deg, ln) in ph:
                    m = notes[deg % len(notes)] + 24 + 12 * (deg // len(notes)) + spec.get('moct', 0) * 12; put(fn(mtof(m), ln * beat, .7), t0 + pos * beat, lv, .15)
            elif kind == 'bass':
                for pos in (0, 2 * beat): put(inst_bass(mtof(root - 12), beat * 1.6, .9), t0 + pos, lv)
            elif kind == 'bass8':
                for k in range(8): put(inst_bass(mtof(root - 12 + (12 if k % 4 == 3 else 0)), beat * .45, .8), t0 + sw(k * beat / 2), lv)
            elif kind == 'bass1':
                put(inst_bass(mtof(root - 12), bar * .9, .9), t0, lv)
            elif kind == 'pulse':
                for k in range(4): put(inst_bass(mtof(root - 12), beat * .35, .8), t0 + k * beat, lv)
            elif kind == 'kick4':
                for k in range(4): put(drum_kick(1), t0 + k * beat, lv)
            elif kind == 'kick13':
                for k in (0, 2): put(drum_kick(1), t0 + k * beat, lv)
            elif kind == 'kicklofi':
                for pos in (0, 1.75 * beat, 2.5 * beat): put(drum_kick(1), t0 + pos, lv)
            elif kind == 'clap24':
                for k in (1, 3): put(drum_clap(1), t0 + k * beat, lv)
            elif kind == 'snare24':
                for k in (1, 3): put(drum_snare(1), t0 + k * beat + r.normal(0, .004), lv)
            elif kind == 'hat8':
                for k in range(8): put(drum_hat(.7 + .3 * (k % 2 == 0)), t0 + sw(k * beat / 2), lv, .35)
            elif kind == 'hat16':
                for k in range(16): put(drum_hat(.5 + .5 * (k % 4 == 0)), t0 + k * beat / 4, lv, .35)
            elif kind == 'shaker16':
                for k in range(16): put(drum_shaker(.5 + .5 * (k % 2)), t0 + k * beat / 4 + r.normal(0, .003), lv, -.3)
            elif kind == 'tick4':
                for k in range(4): put(drum_wood(1 if k % 2 == 0 else .7), t0 + k * beat, lv, .4)
            elif kind == 'tick8':
                for k in range(8): put(drum_wood(.8 if k % 2 == 0 else .55), t0 + k * beat / 2, lv, .4)
    return L, R

def reverb(L, R, wet=.2, decay=.5):
    n = int(1.8 * SR); t = np.arange(n) / SR
    irL = lp(rng.standard_normal(n), 5000) * np.exp(-t / decay); irR = lp(rng.standard_normal(n), 5000) * np.exp(-t / decay)
    irL /= np.sqrt(np.sum(irL ** 2)); irR /= np.sqrt(np.sum(irR ** 2))
    return L + wet * fftconvolve(L, irL)[:len(L)], R + wet * fftconvolve(R, irR)[:len(R)]

def render_music(style, sections, total):
    """sections: [(t0, name)], last entry is the end; style: {'bpm', 'secs': {name: spec}}"""
    n = int(total * SR) + SR; L = np.zeros(n); R = np.zeros(n); bpm = style['bpm']
    for k in range(len(sections) - 1):
        t0, name = sections[k]; t1 = sections[k + 1][0]; spec = style['secs'].get(name)
        if not spec or t1 - t0 < .05: continue
        nxt = sections[k + 1][1]; cut = (style['secs'].get(nxt) or {}).get('hard', False) or nxt == 'stop'
        l, r = render_section(spec, t1 - t0, spec.get('bpm', bpm), seed=k * 31 + 5)
        g = np.ones(len(l)); e = int((t1 - t0) * SR)
        fo = int((.06 if cut else spec.get('release', .9)) * SR)
        if e < len(g): g[e:e + fo] = np.linspace(1, 0, min(fo, len(g) - e)); g[e + fo:] = 0
        fi = int(spec.get('fadein', .02) * SR); g[:fi] *= np.linspace(0, 1, fi)
        lvl = spec.get('gain', 1.); i = int(t0 * SR); m = min(len(l), n - i)
        L[i:i + m] += l[:m] * g[:m] * lvl; R[i:i + m] += r[:m] * g[:m] * lvl
    L, R = reverb(L, R, style.get('wet', .22), style.get('decay', .5))
    return L[:int(total * SR)], R[:int(total * SR)]

# ---------------------------------------------------------------- episode styles (all original)
STYLES = {
 'riso2': {'bpm': 116, 'wet': .2, 'secs': {
   'intro':  {'chords': ['C', 'Am', 'F', 'G'], 'layers': {'arp8:marimba': .32, 'bass1': .24, 'shaker16': .12}, 'gain': .9},
   'chaos':  {'chords': ['C', 'G', 'Am', 'F'], 'layers': {'arp16:marimba': .3, 'wonky:marimba': .14, 'bass8': .34, 'kick4': .36, 'clap24': .2, 'hat8': .14}, 'gain': 1.0},
   'quirk':  {'chords': ['F', 'G', 'Em', 'Am'], 'layers': {'offbeat:pluck': .36, 'bass': .3, 'tick4': .22}, 'gain': .95},
   'bill':   {'chords': ['Am', 'F', 'Dm', 'E'], 'layers': {'pulse': .34, 'tick8': .22, 'arp8:marimba': .16, 'pad': .14}, 'oct': -1, 'gain': .95},
   'stop':   None,
   'build':  {'chords': ['C', 'F', 'G', 'C'], 'layers': {'clock:marimba': .3, 'bass': .3, 'kick13': .3, 'hat8': .12, 'arp8:marimba': .12}, 'gain': 1.0, 'release': .25},
   'quiet':  {'chords': ['Cmaj7'], 'layers': {'pad': .2}, 'gain': .7, 'fadein': .4, 'hard': True},
   'resolve':{'chords': ['F', 'G', 'Am', 'F', 'C'], 'layers': {'chords2:epiano': .3, 'mel:glock': .2, 'bass': .3, 'kick13': .22, 'shaker16': .1},
              'mel': [[[0, 2, 1], [1.5, 1, .5], [2, 0, 1]], [[0, 1, 1], [2, 2, 1.5]], [[0, 0, 1], [1, 1, .5], [2, 2, 2]], [[0, 2, 2], [2, 3, 2]], [[0, 0, 4]]], 'gain': 1.0, 'release': 2.0},
 }},
 'living': {'bpm': 84, 'wet': .26, 'decay': .6, 'secs': {
   'intro':  {'chords': ['Dm7', 'G7', 'Cmaj7', 'Am7'], 'layers': {'chords2:epiano': .3, 'bass1': .3, 'kicklofi': .26, 'snare24': .14, 'hat8': .1}, 'swing': .3, 'gain': .95},
   'chat':   {'chords': ['Fmaj7', 'G7', 'Em7', 'Am7'], 'layers': {'chords2:epiano': .3, 'arp8:glock': .1, 'bass': .3, 'kicklofi': .28, 'snare24': .16, 'hat8': .12}, 'swing': .3, 'gain': 1.0},
   'except': {'chords': ['Am'], 'layers': {'pad': .12}, 'gain': .6, 'hard': True, 'fadein': .3},
   'agent':  {'chords': ['Am7', 'Fmaj7', 'Dm7', 'E7'], 'layers': {'pulse': .3, 'tick8': .18, 'arp8:pluck': .18, 'kick13': .22, 'pad': .1}, 'oct': -1, 'gain': .95},
   'full':   {'chords': ['E7'], 'layers': {'pad': .12}, 'gain': .6, 'hard': True},
   'retry':  {'chords': ['Dm7', 'E7', 'Am7', 'G7'], 'layers': {'pulse': .3, 'tick8': .2, 'arp8:pluck': .2, 'kick13': .26, 'snare24': .1}, 'oct': -1, 'gain': 1.0},
   'success':{'chords': ['Cmaj7', 'Fmaj7', 'G7', 'Cmaj7'], 'layers': {'chords2:epiano': .32, 'arp8:glock': .14, 'bass': .32, 'kicklofi': .3, 'snare24': .16, 'hat8': .12}, 'swing': .3, 'gain': 1.05},
   'explain':{'chords': ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7'], 'layers': {'chords2:epiano': .3, 'bass1': .28, 'kicklofi': .22, 'hat8': .08}, 'swing': .3, 'gain': .95},
   'outro':  {'chords': ['Fmaj7', 'G7', 'Cmaj7'], 'layers': {'chords:epiano': .3, 'mel:glock': .16, 'bass1': .28}, 'mel': [[[0, 2, 2], [2, 1, 2]], [[0, 3, 2], [2, 2, 2]], [[0, 0, 4]]], 'gain': .95, 'release': 2.0},
 }},
 'terminal': {'bpm': 92, 'wet': .3, 'decay': .7, 'secs': {
   'boot':   {'chords': ['Am', 'F', 'C', 'G'], 'layers': {'arp16:chip': .16, 'bass1': .26, 'hat16': .06}, 'gain': .9},
   'inbox':  {'chords': ['Am', 'F', 'C', 'G'], 'layers': {'arp8:chip': .2, 'bass8': .3, 'kick13': .26, 'hat8': .1}, 'gain': 1.0},
   'hidden': {'chords': ['Am'], 'layers': {'pad': .14, 'tick4': .08}, 'gain': .6, 'hard': True, 'fadein': .3},
   'obey':   {'chords': ['Dm', 'Am', 'E7', 'Am'], 'layers': {'pulse': .32, 'tick8': .2, 'stab:chip': .16, 'kick4': .28}, 'oct': -1, 'gain': 1.0, 'release': .2},
   'stop':   None,
   'defend': {'chords': ['F', 'G', 'Am', 'Em'], 'layers': {'arp8:chip': .18, 'bass': .3, 'kick13': .24, 'snare24': .12, 'hat8': .08}, 'gain': 1.0},
   'verdict':{'chords': ['Fmaj7', 'Em7', 'Dm7', 'Am7'], 'layers': {'chords2:epiano': .28, 'arp8:glock': .08, 'bass1': .26, 'kicklofi': .2, 'hat8': .08}, 'swing': .2, 'gain': .95},
   'outro':  {'chords': ['Fmaj7', 'G', 'Am'], 'layers': {'chords:epiano': .28, 'mel:chip': .14, 'bass1': .26}, 'mel': [[[0, 2, 2], [2, 1, 2]], [[0, 3, 2], [2, 2, 2]], [[0, 0, 4]]], 'gain': .95, 'release': 2.0},
 }},
 'papercut': {'bpm': 104, 'wet': .2, 'decay': .45, 'secs': {
   'intro':  {'chords': ['C', 'Am', 'F', 'G'], 'layers': {'offbeat:pluck': .3, 'arp8:marimba': .16, 'bass1': .26, 'shaker16': .1}, 'gain': .9},
   'work':   {'chords': ['C', 'G', 'Am', 'F'], 'layers': {'arp8:marimba': .26, 'bass8': .3, 'kick13': .26, 'tick8': .14, 'shaker16': .08}, 'gain': 1.0},
   'sneak':  {'chords': ['Am', 'E', 'Am', 'E7'], 'layers': {'offbeat:pluck': .34, 'bass': .28, 'tick4': .2}, 'oct': -1, 'gain': .95},
   'snip':   {'chords': ['Am'], 'layers': {'pad': .12}, 'gain': .6, 'hard': True, 'fadein': .3},
   'caught': {'chords': ['Dm', 'Am', 'E7', 'Am'], 'layers': {'pulse': .3, 'tick8': .2, 'stab:pluck': .18, 'kick4': .26}, 'oct': -1, 'gain': 1.0, 'release': .2},
   'stop':   None,
   'lock':   {'chords': ['F', 'G', 'Am', 'Em'], 'layers': {'arp8:marimba': .2, 'bass': .3, 'kick13': .22, 'shaker16': .1}, 'gain': 1.0},
   'honest': {'chords': ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7'], 'layers': {'chords2:epiano': .28, 'arp8:glock': .08, 'bass1': .26, 'kicklofi': .18, 'shaker16': .06}, 'swing': .2, 'gain': .95},
   'outro':  {'chords': ['F', 'G', 'C'], 'layers': {'chords:marimba': .28, 'mel:glock': .16, 'bass1': .26}, 'mel': [[[0, 2, 2], [2, 1, 2]], [[0, 3, 2], [2, 2, 2]], [[0, 0, 4]]], 'gain': .95, 'release': 2.0},
 }},
 'factory': {'bpm': 100, 'wet': .24, 'secs': {
   'intro':  {'chords': ['C', 'Em', 'F', 'G'], 'layers': {'arp8:musicbox': .26, 'bass1': .26, 'tick4': .1}, 'gain': .9},
   'steak':  {'chords': ['Ab'], 'layers': {'pad': .12}, 'gain': .6, 'hard': True, 'fadein': .3},
   'inside': {'chords': ['C', 'G', 'Am', 'F'], 'layers': {'arp8:musicbox': .24, 'bass': .3, 'kick13': .26, 'tick8': .14, 'shaker16': .08}, 'gain': 1.0},
   'middle': {'chords': ['Am', 'F', 'Am', 'E'], 'layers': {'pad': .16, 'arp8:musicbox': .14, 'pulse': .22, 'tick4': .1}, 'oct': -1, 'gain': .9},
   'full':   {'chords': ['Dm', 'E', 'Dm', 'E'], 'layers': {'pulse': .32, 'tick8': .2, 'stab:pluck': .2, 'kick4': .26}, 'gain': 1.0},
   'back':   {'chords': ['F', 'G', 'C'], 'layers': {'chords2:musicbox': .3, 'bass': .3, 'kick13': .2, 'shaker16': .1}, 'gain': 1.0},
   'resolve':{'chords': ['F', 'G', 'Em', 'Am', 'F', 'C'], 'layers': {'chords2:epiano': .26, 'mel:musicbox': .22, 'bass': .28, 'kick13': .18, 'shaker16': .08},
              'mel': [[[0, 2, 1], [1, 1, 1], [2, 0, 2]], [[0, 1, 2], [2, 2, 2]], [[0, 0, 1], [1, 1, 1], [2, 2, 2]], [[0, 2, 4]], [[0, 1, 2], [2, 0, 2]], [[0, 0, 4]]], 'gain': 1.0, 'release': 2.0},
 }},
}

# ---------------------------------------------------------------- page reading + mix
def node_env():  # every node_modules from this file up to / (the repo root's has playwright), ahead of any NODE_PATH already set
    mods, d = [], HERE
    while True:
        if os.path.isdir(os.path.join(d, 'node_modules')): mods.append(os.path.join(d, 'node_modules'))
        up = os.path.dirname(d)
        if up == d: break
        d = up
    return dict(os.environ, NODE_PATH=os.pathsep.join(mods + [p for p in os.environ.get('NODE_PATH', '').split(os.pathsep) if p]))

def page_data(page):
    js = r"""
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + path.resolve(process.argv[1]) + '?clean&nocaps');
  await p.waitForTimeout(600); const d = await p.evaluate(() => JSON.stringify({ CUES, MUSIC, DUR, WARP, CAPS, LOOK: window.LOOK || '' })); console.log(d); await b.close(); })();
"""
    out = subprocess.run(['node', '-e', js, os.path.abspath(page)], capture_output=True, text=True, check=True, env=node_env()).stdout
    return json.loads(out.strip().splitlines()[-1])

def inv_warp(WARP):
    if len(WARP) < 2: return lambda x: x
    a = np.array([w[0] for w in WARP]); b = np.array([w[1] for w in WARP])
    return lambda x: float(np.interp(x, b, a))

def env_follow(x, att=.03, rel=.35, win=.03):
    w = int(win * SR); e = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, mode='same'))
    out = np.zeros_like(e); a1 = np.exp(-1 / (att * SR)); r1 = np.exp(-1 / (rel * SR)); v = 0.
    # vectorised-ish smoothing in blocks for speed
    for i in range(0, len(e), 64):
        target = e[i]; c = a1 if target > v else r1; v = target + (v - target) * c ** 64; out[i:i + 64] = v
    return out

def main():
    page, outp = sys.argv[1], sys.argv[2]; voice = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != '-' else None
    d = page_data(page); iw = inv_warp(d['WARP']); total = d['DUR']  # video length (DUR is rewritten when a page is re-timed)
    ep = d.get('LOOK') or {'ep1': 'riso2', 'ep2': 'living', 'ep3': 'factory'}.get(os.path.basename(page)[:3], 'riso2'); style = STYLES[ep]
    secs = [(iw(t), n) for t, n in d['MUSIC']]
    print(f'{ep}: {total:.2f} s, {len(d["CUES"])} cues, {len(secs) - 1} music sections, voice={"yes" if voice else "no (caption-timed ducking)"}')
    mL, mR = render_music(style, secs, total)
    n = int(total * SR); sfx = np.zeros(n)
    for t, name, g, r, off, ln in d['CUES']:
        x = get_sfx(name, r); x = x[int(off * SR):]
        if ln and ln * SR > len(x):  # loop with short crossfades
            xf = int(.05 * SR); seg = x.copy(); seg[:xf] *= np.linspace(0, 1, xf); seg[-xf:] *= np.linspace(1, 0, xf); hop = len(seg) - xf
            y = np.zeros(int(ln * SR) + len(seg))
            for j in range(0, int(ln * SR), hop): y[j:j + len(seg)] += seg
            x = y
        if ln: x = x[:int(ln * SR)]; x = fade_tail(x, min(.25, ln * .3))
        i = int(iw(t) * SR)
        if i >= n: continue
        x = x[:n - i]; sfx[i:i + len(x)] += x * g
    if voice:
        v = load_audio(voice); v = np.pad(v, (0, max(0, n - len(v))))[:n]; env = env_follow(v); env = np.clip(env / (np.percentile(env[env > 1e-4], 90) + 1e-9), 0, 1)
    else:
        v = np.zeros(n); env = np.zeros(n)
        for c in d['CAPS']: a, b = int(iw(c[1]) * SR), int(iw(c[2]) * SR); env[a:b] = 1
        k = int(.25 * SR); env = np.convolve(env, np.ones(k) / k, mode='same')
    # stem levels: voice speech RMS -20 dBFS, music bed RMS about -29 dBFS (ducked ~6 dB under the voice), SFX peaks <= -9 dBFS
    if voice:
        act = env > .25; vr = np.sqrt(np.mean(v[act] ** 2)) if act.any() else np.sqrt(np.mean(v ** 2)); v = v * (.1 / (vr + 1e-9))
    mm = np.sqrt(np.mean((mL ** 2 + mR ** 2) / 2)); mg = .036 / (mm + 1e-9)
    duck = 1 - .5 * env
    L = mL * duck * mg + sfx * .34 + v
    R = mR * duck * mg + sfx * .34 + v
    L = hp(L, 35); R = hp(R, 35)
    print(f'levels: music rms {20*np.log10(.036):.1f} dBFS (pre-duck), sfx peak {20*np.log10(np.max(np.abs(sfx*.34))+1e-9):.1f} dBFS, voice {"rms -20 dBFS" if voice else "none"}')
    st = np.stack([L, R], 1); st = np.tanh(st * 1.1) / 1.1
    tmp = outp + '.tmp.wav'
    import wave
    with wave.open(tmp, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes())
    target = -14 if voice else -16
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', f'loudnorm=I={target}:TP=-1.5:LRA=11', '-ar', str(SR), '-c:a', 'aac', '-b:a', '192k', outp], check=True)
    os.remove(tmp); print('wrote', outp)

if __name__ == '__main__':
    main()
