# Records every clip in six natural neural voices (Microsoft Edge voices via edge-tts), then embeds them in the page.
# Run with the Bible Shorts venv, which has edge_tts:  ~/bible-shorts-studio/.venv/bin/python build.py
import asyncio, base64, json, os, re, subprocess, tempfile
import edge_tts
from content import *
FF = ["ffmpeg", "-loglevel", "error", "-y"]
RATE = {"w": "-22%", "l": "-12%", "p": "-8%"}

def finish(src, dst, pre=""):
    # trim silences, gentle compression, peak-normalise to -1 dBFS: loud and clear
    chain = (pre + "silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
             "silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
             "acompressor=threshold=-22dB:ratio=2.5:attack=5:release=60:makeup=2,adelay=40")
    tmp = dst + ".wav"
    subprocess.run(FF + ["-i", src, "-ac", "1", "-ar", "24000", "-af", chain, tmp], check=True)
    vd = subprocess.run(["ffmpeg", "-i", tmp, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    peak = float(re.search(r"max_volume: (-?[\d.]+) dB", vd).group(1))
    subprocess.run(FF + ["-i", tmp, "-af", f"volume={-1.0 - peak}dB", "-b:a", "40k", dst], check=True)
    os.remove(tmp)

async def tts(text, voice, rate, path):
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, voice, rate=rate).save(path); return
        except Exception as e:
            if attempt == 3: raise
            await asyncio.sleep(1.5 * (attempt + 1))

async def clip(sem, voice, dst, text, rate):
    if os.path.exists(dst): return
    async with sem:
        with tempfile.TemporaryDirectory() as d:
            await tts(text, voice, rate, f"{d}/r.mp3")
            await asyncio.to_thread(finish, f"{d}/r.mp3", dst)

async def vowel_sound(sem, voice, dst, word):
    # Real short-vowel sound: cut the vowel off the front of a word, before its stop-consonant closure, and slow it.
    if os.path.exists(dst): return
    async with sem:
        with tempfile.TemporaryDirectory() as d:
            await tts(word, voice, "-25%", f"{d}/r.mp3")
            subprocess.run(FF + ["-i", f"{d}/r.mp3", "-ac", "1", "-ar", "24000", "-af",
                                 "silenceremove=start_periods=1:start_threshold=-45dB", f"{d}/a.wav"], check=True)
            cut = None
            for db in (-32, -28, -24, -20):  # find the stop-consonant closure; some voices close it less fully
                sd = subprocess.run(["ffmpeg", "-i", f"{d}/a.wav", "-af", f"silencedetect=n={db}dB:d=0.02", "-f", "null", "-"],
                                    capture_output=True, text=True).stderr
                m = re.search(r"silence_start: ([\d.]+)", sd)
                if m and 0.06 < float(m.group(1)) < 0.45: cut = float(m.group(1)) - 0.005; break
            print(f"vowel {dst}: closure {cut} at {db} dB")
            cut = min(cut or 0.16, 0.3)
            slow = 0.55; L = cut / slow
            pre = f"atrim=0:{cut:.3f},atempo={slow},afade=t=in:d=0.02,afade=t=out:st={max(L - 0.09, 0):.3f}:d=0.09"
            subprocess.run(FF + ["-i", f"{d}/a.wav", "-af", pre, f"{d}/v.wav"], check=True)
            finish(f"{d}/v.wav", dst)

def clip_list():
    """Every clip the page needs: id -> (text, rate). Vowel sounds are handled separately."""
    words = set(w for w, _ in FIRST_VOWEL) | {d["word"] for d in VOWELS.values()} | {w for _, w, _ in ALPHABET}
    for st in STAGES:
        words |= {w.replace("|", "") for w, _ in st.get("words", [])} | {st["animal"]}
    for s, _ in SENTENCES:
        words |= set(s.lower().rstrip(".").split())
    words |= {v[2] for v in LETTER_SOUNDS.values()}
    c = {f"w_{w}": (WORD_TEXT.get(w, w + "."), RATE["w"]) for w in words}
    c.update({f"l_{x}": (x.upper() + ".", RATE["l"]) for x in "abcdefghijklmnopqrstuvwxyz"})
    c.update({f"p_{k}": (t, RATE["p"]) for k, t in PHRASES.items()})
    c.update({f"a_{l}": (f"{l.upper()} is for {WORD_TEXT.get(w, w + '.').rstrip('.')}.", RATE["l"]) for l, w, _ in ALPHABET})
    c.update({f"t_{i}": (s, "-18%") for i, (s, _) in enumerate(SENTENCES)})
    return c

CLIPS = clip_list()
TALK_WORDS = sorted({w for pool in TALK.values() for w, _ in pool})
TALK_NEW = {f"w_{w}": (WORD_TEXT.get(w, w + "."), RATE["w"]) for w in TALK_WORDS if f"w_{w}" not in CLIPS}

def slow_copy(src, dst):
    # a slower model of the word (pitch kept) so a child can hear every sound
    if not os.path.exists(dst):
        subprocess.run(FF + ["-i", src, "-af", "atempo=0.72,apad=pad_dur=0.05", "-b:a", "40k", dst], check=True)

async def main():
    sem = asyncio.Semaphore(12)
    jobs = []
    for key, voice, name, *_ in VOICES:
        out = f"audio/{key}"; os.makedirs(out, exist_ok=True)
        for cid, (text, rate) in {**CLIPS, **TALK_NEW}.items(): jobs.append(clip(sem, voice, f"{out}/{cid}.mp3", text, rate))
        jobs.append(clip(sem, voice, f"{out}/p_hello.mp3", f"Hi! I'm {name}. Let's read together!", RATE["p"]))
        for v, d in VOWELS.items(): jobs.append(vowel_sound(sem, voice, f"{out}/s_{v}.mp3", d["src"]))
    await asyncio.gather(*jobs)

asyncio.run(main())
# ---- Sound Garden: cut real letter sounds and blends from each voice's own words ----
import shutil, sys
sys.path.insert(0, "phonics"); import slice as ph
PH_SRC = sorted({v[0] for v in LETTER_SOUNDS.values() if v[0]} | set(BLEND_SRC.values()))
async def raw_sources():
    sem = asyncio.Semaphore(12)
    async def one(voice, key, w):
        dst = f"audio/{key}/raw/{w}.mp3"
        if os.path.exists(dst): return
        async with sem: await tts(w + ".", voice, "-15%", dst)
    jobs = []
    for key, voice, *_ in VOICES:
        os.makedirs(f"audio/{key}/raw", exist_ok=True)
        jobs += [one(voice, key, w) for w in PH_SRC]
    await asyncio.gather(*jobs)
asyncio.run(raw_sources())
report = {}
for key, *_ in VOICES:
    for L, (src, how, *_r) in LETTER_SOUNDS.items():
        dst = f"audio/{key}/snd_{L}.mp3"
        if how == "vowel":
            if not os.path.exists(dst): shutil.copy(f"audio/{key}/s_{L}.mp3", dst)
        elif not os.path.exists(dst):
            method = "clip" if how == "clip2" else how
            if how == "clip2":   # qu: keep more of the "kw" glide
                full = ph.pcm(f"audio/{key}/raw/{src}.mp3"); ef = ph.frames(full); s0 = ph.start_of_sound(ef)
                _, ms = None, ph.render(f"audio/{key}/raw/{src}.mp3", s0 / 100, s0 / 100 + .23, dst, fade_out=.06)
            else:
                _, ms = ph.sound(f"audio/{key}/raw/{src}.mp3", method, dst)
            report.setdefault(L, []).append(ms)
    for b, src in BLEND_SRC.items():
        dst = f"audio/{key}/bl_{b}.mp3"
        if not os.path.exists(dst):
            _, ms = ph.blend(f"audio/{key}/raw/{src.lower()}.mp3" if os.path.exists(f"audio/{key}/raw/{src.lower()}.mp3") else f"audio/{key}/raw/{src}.mp3", dst)
            report.setdefault("bl_" + b, []).append(ms)
for k, v in report.items(): print("cut", k, v)
for key, *_ in VOICES:
    for w in TALK_WORDS: slow_copy(f"audio/{key}/w_{w}.mp3", f"audio/{key}/v_{w}.mp3")
TALK_IDS = sorted(TALK_NEW) + [f"v_{w}" for w in TALK_WORDS]
need = set(CLIPS) | {"p_hello"} | {f"s_{v}" for v in VOWELS} | {f"snd_{L}" for L in LETTER_SOUNDS} | {f"bl_{b}" for b in BLEND_SRC}
def pack(key):
    return {i: base64.b64encode(open(f"audio/{key}/{i}.mp3", "rb").read()).decode() for i in sorted(need)}
# Talk Time clips live in their own per-voice pack (voices/<key>.talk.js), loaded when Talk Time opens.
os.makedirs("voices", exist_ok=True)
for key, *_ in VOICES:
    tp = {i: base64.b64encode(open(f"audio/{key}/{i}.mp3", "rb").read()).decode() for i in TALK_IDS}
    open(f"voices/{key}.talk.js", "w").write(f"(window.__TP=window.__TP||{{}})[{json.dumps(key)}]={json.dumps(tp)};")
# The default voice ships inside the page; the others are loaded only when chosen (voices/<key>.js).
os.makedirs("voices", exist_ok=True)
default = VOICES[0][0]
for key, *_ in VOICES[1:]:
    open(f"voices/{key}.js", "w").write(f"(window.__VP=window.__VP||{{}})[{json.dumps(key)}]={json.dumps(pack(key))};")
data = {"blendIds": sorted(BLEND_SRC), "phonics": PHONICS, "letterSounds": {k: [v[2], v[3]] for k, v in LETTER_SOUNDS.items()}, "talk": {str(k): v for k, v in TALK.items()}, "pairLevels": PAIR_LEVELS, "vowels": VOWELS, "firstVowel": FIRST_VOWEL, "alphabet": ALPHABET, "sentences": SENTENCES, "stages": STAGES,
        "phrases": PHRASES, "voices": [{"key": k, "name": n, "accent": a, "g": g} for k, _, n, a, g in VOICES]}
html = open("template.html", encoding="utf-8").read()
credits = json.load(open("animals/credits.json"))
anim = {a: {"b64": base64.b64encode(open(f"animals/clips/{a}.mp3", "rb").read()).decode(), **c} for a, c in credits.items()}
html = html.replace("/*__ANIM__*/{}", json.dumps(anim, ensure_ascii=False))
html = html.replace("/*__AUDIO__*/{}", json.dumps({default: pack(default)})).replace("/*__DATA__*/{}", json.dumps(data, ensure_ascii=False))
open("reading-adventure.html", "w", encoding="utf-8").write(html)
print(len(need), "clips per voice;", round(len(html) / 1e6, 2), "MB html;",
      {k: round(os.path.getsize(f"voices/{k}.js") / 1e6, 2) for k, *_ in VOICES[1:]}, "MB packs")
