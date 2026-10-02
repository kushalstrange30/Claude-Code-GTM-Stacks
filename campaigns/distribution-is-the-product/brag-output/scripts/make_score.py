"""Synthesize the 60s 'THE CURRENT' score: history tick clock -> product pulse with chords,
UI cues, Shepard rise, the hit, silence. Deterministic. Writes composition/assets/audio/score.wav
and composition/assets/ticks.json (the same map drives the picture)."""
import json, os, wave
import numpy as np

SR, DUR = 48000, 60.0
N = int(SR * DUR)
rng = np.random.default_rng(1882)
OUT = os.path.join(os.path.dirname(__file__), "..", "composition", "assets")

PRODUCT_START, PRODUCT_END, HIT = 15.6, 51.6, 54.6

# ---- tick map ----
hist, t = [], 0.25
while t < 15.3:
    hist.append(round(t, 3))
    t += 60 / (60 * (115 / 60) ** (t / 15.6))
hist = [x for x in hist if not (11.0 < x < 11.6)]          # the stumble at the AC twist
product = [round(PRODUCT_START + 0.5 * k, 3) for k in range(int((PRODUCT_END - PRODUCT_START) / 0.5))]
calm = [52.1, 53.1, 54.1]
ticks = hist + product + calm

# UI cue times (picture uses the same numbers)
CUES = {
    "intent": 17.6, "submit": 22.6,
    "enrich": [25.1, 25.6, 26.1, 26.6, 27.1, 27.6],
    "score": 31.1, "assign": 36.6, "booked": 40.6,
    "slack": 43.6, "crm": 44.6, "dot": 45.6, "system": 47.6,
}

def env(n, tau): return np.exp(-np.arange(n) / (tau * SR))
def sine(f, n): return np.sin(2 * np.pi * f * np.arange(n) / SR)
def lowpass(x, k): return np.convolve(x, np.ones(int(k)) / int(k), mode="same")
def place(buf, sig, at, g=1.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if 0 <= i < N: buf[i:j] += sig[: j - i] * g

mix = np.zeros(N)
tt = np.arange(N) / SR

def tick_sig(s):
    n = int(0.12 * SR)
    click = np.diff(rng.normal(0, 1, n), prepend=0) * env(n, 0.0025)
    return (click * 0.35 + sine(2350, n) * env(n, 0.018) * 0.55 + sine(880, n) * env(n, 0.012) * 0.35
            + sine(110, n) * env(n, 0.05) * 0.5 * s) * s

for tk in hist:
    place(mix, tick_sig(0.55 + 0.35 * tk / 15.6), tk, 0.9)
for tk in product:
    place(mix, tick_sig(0.55), tk, 0.55)
for tk in calm:
    place(mix, tick_sig(0.8), tk, 0.85)

# ---- history: filament hum, drone, dynamo, projector, stumble ----
n = int(2.8 * SR)
hum = (sine(120, n) + 0.5 * sine(240, n) + 0.25 * sine(360, n)) * 0.06
hum *= np.minimum(1, np.arange(n) / (0.8 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.4 * SR))
place(mix, hum, 0.25)

drone = sum(a * np.sin(2 * np.pi * f * tt + 0.3 * np.sin(2 * np.pi * 0.11 * tt))
            for f, a in [(55, 1.0), (82.41, 0.6), (110, 0.45), (164.8, 0.25)])
hist_env = np.clip(tt / 15.6, 0, 1) ** 1.5 * 0.13 + 0.03
hist_env = np.where(tt > PRODUCT_START + 0.4, 0, hist_env)
mix += drone * hist_env

a, b = 5.645, 8.659
n = int((b - a) * SR); x = np.arange(n) / SR
ph = 2 * np.pi * np.cumsum(70 + 170 * (x / (b - a)) ** 1.4) / SR
place(mix, (np.sin(ph) + 0.4 * np.sin(2 * ph)) * 0.07 * np.minimum(1, x / 0.6) * np.minimum(1, (b - a - x) / 0.25), a)

k = 8.659
while k < 10.691:
    m = int(0.03 * SR); place(mix, rng.normal(0, 1, m) * env(m, 0.004) * 0.12, k); k += 1 / 18

n = int(1.2 * SR); x = np.arange(n) / SR
place(mix, np.sin(2 * np.pi * np.cumsum(60 - 25 * x / 1.2) / SR) * env(n, 0.5) * 0.35, 11.05)
place(mix, tick_sig(1.0) * 1.1, 13.732)  # relay

# ---- whoosh into color + arrival ----
n = int(0.6 * SR)
place(mix, lowpass(rng.normal(0, 1, n), 6) * (np.arange(n) / n) ** 3 * 0.35, 15.0)
m = int(0.9 * SR); place(mix, sine(55, m) * env(m, 0.3) * 0.5, PRODUCT_START)

# ---- product act: chord pad + pulse bass (Am F C G, 4s each) ----
chords = [(55.0, [220.0, 261.6, 329.6]), (43.65, [174.6, 220.0, 261.6]),
          (65.41, [196.0, 261.6, 329.6]), (49.0, [196.0, 246.9, 293.7])]
seg = 4.0
c = PRODUCT_START
idx = 0
while c < PRODUCT_END - 0.01:
    root, triad = chords[idx % 4]
    n = int(seg * SR); x = np.arange(n) / SR
    pad = sum(np.sin(2 * np.pi * f * x) + 0.3 * np.sin(2 * np.pi * 2 * f * x) for f in triad) / 3
    pad += 0.6 * np.sin(2 * np.pi * root * 2 * x)
    pad *= np.minimum(1, x / 0.25) * np.minimum(1, (seg - x) / 0.25)
    level = 0.05 + 0.06 * (c - PRODUCT_START) / (PRODUCT_END - PRODUCT_START)
    place(mix, pad * level, c)
    # pulse bass on every beat of this chord
    for bt in np.arange(0, seg - 0.01, 0.5):
        m = int(0.4 * SR)
        place(mix, sine(root, m) * env(m, 0.12) * 0.28, c + bt)
    c += seg; idx += 1

# ---- UI cues ----
def ping(f, g=0.12, tau=0.08):
    m = int(0.4 * SR); return (sine(f, m) + 0.3 * sine(2 * f, m)) * env(m, tau) * g
place(mix, ping(1568), CUES["intent"])
place(mix, tick_sig(1.2) * 0.9, CUES["submit"]); place(mix, ping(1976, 0.14), CUES["submit"])
for i, et in enumerate(CUES["enrich"]):
    place(mix, ping([1318, 1480, 1568, 1760, 1976, 2093][i], 0.09, 0.05), et)
place(mix, ping(2093, 0.14, 0.12), CUES["score"])
place(mix, ping(1760, 0.14, 0.12), CUES["assign"])
for f in (1568, 1976, 2349):
    place(mix, ping(f, 0.12, 0.25), CUES["booked"])
for key, f in (("slack", 1760), ("crm", 1976), ("dot", 2349)):
    place(mix, ping(f, 0.1), CUES[key])

# ---- Shepard rise (38.1 -> 51.6), then calm ----
a, b = 38.1, PRODUCT_END
n = int((b - a) * SR); x = np.arange(n) / SR
shep = np.zeros(n)
for o in range(8):
    logf = np.log2(55) + ((o + x * 0.22) % 8)
    w = np.exp(-0.5 * ((logf - np.log2(440)) / 1.3) ** 2)
    shep += w * np.sin(2 * np.pi * np.cumsum(2 ** logf) / SR)
shep *= (x / (b - a)) ** 1.6 * 0.09
shep[-int(0.3 * SR):] *= np.linspace(1, 0, int(0.3 * SR))
place(mix, shep, a)

# tower: low warm bed
n = int((HIT - PRODUCT_END) * SR); x = np.arange(n) / SR
bed = (np.sin(2 * np.pi * 55 * x) + 0.5 * np.sin(2 * np.pi * 82.41 * x)) * 0.06
bed *= np.minimum(1, x / 0.4); bed[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
place(mix, bed, PRODUCT_END)

# ---- the hit, silence, filament hum ----
n = int(2.4 * SR); x = np.arange(n) / SR
boom = np.sin(2 * np.pi * np.cumsum(52 - 18 * np.minimum(1, x / 1.5)) / SR) * env(n, 0.6) * 0.95
boom += lowpass(rng.normal(0, 1, n), 4) * env(n, 0.08) * 0.5
boom[: int(0.12 * SR)] += tick_sig(1.4)
place(mix, boom, HIT)
n = int(3.0 * SR)
place(mix, (sine(120, n) + 0.5 * sine(240, n)) * 0.05 * np.minimum(1, np.arange(n) / (0.8 * SR)), 57.0)

mix[-int(0.3 * SR):] *= np.linspace(1, 0, int(0.3 * SR))
mix = mix / np.max(np.abs(mix)) * 0.89
pcm = (np.stack([mix, mix], 1) * 32767).astype("<i2")
os.makedirs(os.path.join(OUT, "audio"), exist_ok=True)
with wave.open(os.path.join(OUT, "audio", "score_raw.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
json.dump({"ticks": ticks, "hit": HIT, "cues": CUES}, open(os.path.join(OUT, "ticks.json"), "w"))
print("ticks", len(ticks))
