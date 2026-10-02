"""Synthesize the 'THE CURRENT' score: tick clock, drone, era SFX, Shepard rise, hit.
Deterministic (seeded). Writes composition/assets/audio/score.wav and ticks.json."""
import json, math, os, wave
import numpy as np

SR = 48000
DUR = 25.0
N = int(SR * DUR)
rng = np.random.default_rng(1882)
OUT = os.path.join(os.path.dirname(__file__), "..", "composition", "assets")

# ---- tick map (shared with the picture) ----
ticks, t = [], 0.25
while t < 20.6:
    ticks.append(round(t, 3))
    bpm = 60 * (170 / 60) ** (min(t, 20.4) / 20.4)
    t += 60 / bpm
ticks = [x for x in ticks if not (11.75 < x < 12.45)]  # the stumble at the AC twist
ticks += [20.9, 21.7]                                   # calm, controlled
HIT = 22.4

def env_exp(n, tau):  # exponential decay envelope, tau in seconds
    return np.exp(-np.arange(n) / (tau * SR))

def place(buf, sig, at, gain=1.0):
    i = int(at * SR)
    j = min(N, i + len(sig))
    if i < N:
        buf[i:j] += sig[: j - i] * gain

def lowpass(x, k):
    k = max(1, int(k))
    return np.convolve(x, np.ones(k) / k, mode="same")

def sine(f, n, phase=0.0):
    return np.sin(2 * np.pi * f * np.arange(n) / SR + phase)

mix = np.zeros(N)

# ---- the tick: escapement click with body ----
def tick_sig(strength):
    n = int(0.12 * SR)
    noise = rng.normal(0, 1, n)
    click = np.diff(noise, prepend=0) * env_exp(n, 0.0025)
    ring = sine(2350, n) * env_exp(n, 0.018) * 0.55
    body = sine(880, n) * env_exp(n, 0.012) * 0.35
    thump = sine(110, n) * env_exp(n, 0.05) * 0.5 * strength
    return (click * 0.35 + ring + body + thump) * strength

for i, tk in enumerate(ticks):
    s = 0.55 + 0.45 * min(1.0, tk / 20.0)
    if tk >= 20.8:
        s = 0.8
    place(mix, tick_sig(s), tk, 0.9)

# ---- filament hum (hook) ----
n = int(2.9 * SR)
hum = (sine(120, n) + 0.5 * sine(240, n) + 0.25 * sine(360, n)) * 0.06
hum *= np.minimum(1, np.arange(n) / (0.8 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.4 * SR))
place(mix, hum, 0.25)

# ---- drone bed (0 -> 22.4) ----
tt = np.arange(N) / SR
drone = np.zeros(N)
for f, a in [(55, 1.0), (82.41, 0.6), (110, 0.45), (164.8, 0.25), (220, 0.12)]:
    drone += a * np.sin(2 * np.pi * f * tt + 0.3 * np.sin(2 * np.pi * 0.11 * tt))
swell = np.clip(tt / 20.0, 0, 1) ** 1.6 * 0.16 + 0.03
swell = np.where(tt > 20.35, 0.05, swell)
swell = np.where(tt >= HIT, 0, swell)
mix += drone * swell

# ---- dynamo spin-up (Pearl Street) ----
a, b = 5.53, 9.04
n = int((b - a) * SR)
x = np.arange(n) / SR
freq = 70 + 170 * (x / (b - a)) ** 1.4
phase = 2 * np.pi * np.cumsum(freq) / SR
dyn = (np.sin(phase) + 0.4 * np.sin(2 * phase) + 0.2 * np.sin(3 * phase)) * 0.07
dyn *= np.minimum(1, x / 0.6) * np.minimum(1, (b - a - x) / 0.25)
place(mix, dyn, a)

# ---- projector clatter (The Trust) ----
a, b = 9.04, 11.44
k = a
while k < b:
    m = int(0.03 * SR)
    place(mix, rng.normal(0, 1, m) * env_exp(m, 0.004) * 0.12, k)
    k += 1 / 18
place(mix, lowpass(rng.normal(0, 1, int((b - a) * SR)), 30) * 0.05, a)

# ---- the stumble: a sub drop where the beat goes missing ----
n = int(1.2 * SR)
x = np.arange(n) / SR
place(mix, np.sin(2 * np.pi * np.cumsum(60 - 25 * x / 1.2) / SR) * env_exp(n, 0.5) * 0.35, 11.80)

# ---- relay click at the switchboard ----
place(mix, tick_sig(1.0) * 1.1, 14.08)

# ---- Shepard rise (14.08 -> 22.4) ----
a, b = 14.08, HIT
n = int((b - a) * SR)
x = np.arange(n) / SR
shep = np.zeros(n)
octaves_per_sec = 0.28
for o in range(8):
    logf = np.log2(55) + ((o + x * octaves_per_sec) % 8)
    f = 2 ** logf
    w = np.exp(-0.5 * ((logf - np.log2(440)) / 1.3) ** 2)
    shep += w * np.sin(2 * np.pi * np.cumsum(f) / SR)
shep *= (x / (b - a)) ** 1.5 * 0.09
shep *= np.where(x > (20.35 - a), 0.45, 1.0)
shep[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
place(mix, shep, a)

# ---- whoosh into color (15.2 -> 15.96) + soft hit ----
n = int(0.76 * SR)
wh = lowpass(rng.normal(0, 1, n), 6) * (np.arange(n) / n) ** 3 * 0.35
place(mix, wh, 15.2)
m = int(0.8 * SR)
place(mix, sine(65, m) * env_exp(m, 0.25) * 0.45, 15.96)

# ---- UI pings on the five nodes ----
NODE_TIMES = [16.404, 16.837, 17.26, 17.674, 18.08]
for f, nt in zip([1568, 1760, 1976, 2093, 2637], NODE_TIMES):
    m = int(0.35 * SR)
    place(mix, (sine(f, m) + 0.3 * sine(f * 2, m)) * env_exp(m, 0.08) * 0.12, nt)

# ---- the hit, then silence ----
n = int(2.2 * SR)
x = np.arange(n) / SR
boom = np.sin(2 * np.pi * np.cumsum(52 - 18 * np.minimum(1, x / 1.5)) / SR) * env_exp(n, 0.55) * 0.95
boom += lowpass(rng.normal(0, 1, n), 4) * env_exp(n, 0.08) * 0.5
boom += np.concatenate([tick_sig(1.4), np.zeros(n - int(0.12 * SR))])
place(mix, boom, HIT)

# ---- final filament hum (23.9 -> 25) ----
n = int(1.1 * SR)
hum2 = (sine(120, n) + 0.5 * sine(240, n)) * 0.05 * np.minimum(1, np.arange(n) / (0.6 * SR))
place(mix, hum2, 23.9)

# ---- master ----
mix[-int(0.15 * SR):] *= np.linspace(1, 0, int(0.15 * SR))
mix = mix / np.max(np.abs(mix)) * 0.89
st = np.stack([mix, mix], axis=1)
pcm = (st * 32767).astype("<i2")
os.makedirs(os.path.join(OUT, "audio"), exist_ok=True)
with wave.open(os.path.join(OUT, "audio", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
with open(os.path.join(OUT, "ticks.json"), "w") as f:
    json.dump({"ticks": ticks, "hit": HIT, "nodes": NODE_TIMES}, f)
print("ticks", len(ticks), "written")
