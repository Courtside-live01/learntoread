"""Cut real letter sounds and consonant+vowel blends out of a teacher voice's own recorded words.

sound(word, method): the consonant at the start of `word` (or the end, for x), found from the energy
contour: fricatives end where voicing (energy under 900 Hz) starts; nasals and voiced fricatives end
where the vowel gets loud; stops/glides keep their burst plus a short "uh" so a child can hear them.
blend(word): the consonant+vowel before the final stop's closure silence ("cat" -> "ca").
"""
import array, os, re, subprocess
SR = 16000
FF = ["ffmpeg", "-loglevel", "error", "-y"]

def pcm(src, af=None):
    cmd = ["ffmpeg", "-loglevel", "error", "-i", src]
    if af: cmd += ["-af", af]
    return array.array("h", subprocess.run(cmd + ["-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout)

def frames(x, ms=10):
    n = SR * ms // 1000
    return [(sum(v * v for v in x[i:i + n]) / n) ** .5 for i in range(0, len(x) - n, n)]

def start_of_sound(e, frac=.04):
    m = max(e) or 1
    return next((i for i, v in enumerate(e) if v > m * frac), 0)

def render(src, t0, t1, dst, target=None, fade_in=.015, fade_out=.04, clean=None):
    L = t1 - t0
    chain = [f"atrim={t0:.3f}:{t1:.3f}", "asetpts=PTS-STARTPTS"] + ([clean] if clean else [])
    if target and L < target:                      # hold a continuant sound (sss, mmm) long enough to hear
        f = L / target
        while f < .5: chain.append("atempo=0.5"); f /= .5
        chain.append(f"atempo={f:.3f}"); L = target
    chain += [f"afade=t=in:d={fade_in}", f"afade=t=out:st={max(L - fade_out, 0):.3f}:d={fade_out}"]
    tmp = dst + ".wav"
    subprocess.run(FF + ["-i", src, "-ac", "1", "-ar", "24000", "-af", ",".join(chain), tmp], check=True)
    vd = subprocess.run(["ffmpeg", "-i", tmp, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    peak = float(re.search(r"max_volume: (-?[\d.]+) dB", vd).group(1))
    subprocess.run(FF + ["-i", tmp, "-af", f"adelay=30,volume={-1.5 - peak}dB", "-b:a", "40k", dst], check=True)
    os.remove(tmp)
    return L

def sound(src, method, dst):
    full, low, mid = pcm(src), pcm(src, "lowpass=f=900"), pcm(src, "highpass=f=1000,highpass=f=1000,lowpass=f=3000,lowpass=f=3000")
    ef, el, em = frames(full), frames(low), frames(mid)
    s = start_of_sound(ef, .004)                      # soft sounds like fff and th start very quietly
    ml, mm = max(el[s:]) or 1, max(em[s:]) or 1
    def seg(b, lo=6, fallback=11):                   # guard against a cut that is implausibly short
        return b if b - s >= lo else s + fallback
    if method == "fric":       # voiceless sss, fff, shh, th: ends where voicing (energy under 900 Hz) begins
        b = next((i for i in range(s + 2, len(el)) if el[i] > ml * .2 and el[min(i + 2, len(el) - 1)] > ml * .2), s + 12)
        b = seg(b) - 1                                # stop just before the vowel
        return render(src, s / 100, b / 100, dst, target=.5, clean="highpass=f=1100,highpass=f=1100"), (b - s) * 10
    if method in ("nasal", "vfric"):   # mmm, nnn, zzz, vvv: little energy at 1-3 kHz until the vowel arrives
        b = next((i for i in range(s + 2, len(em)) if em[i] > mm * .3 and em[min(i + 2, len(em) - 1)] > mm * .3), s + 9)
        b = seg(b, 5, 9) - 1
        clean = "lowpass=f=1100,lowpass=f=1100" if method == "nasal" else None   # a pure hum for mmm / nnn
        return render(src, s / 100, b / 100, dst, target=.5, clean=clean), (b - s) * 10
    if method == "clip":       # buh, duh, kuh...: burst + a short neutral vowel
        v = next((i for i in range(s + 1, len(el)) if el[i] > ml * .35), s + 5)
        return render(src, s / 100, v / 100 + .085, dst, fade_out=.045), (v - s) * 10
    if method == "tail":       # x at the end of box: release burst + hiss after the closure
        mf = max(ef) or 1
        e = len(ef) - 1
        while e > 0 and ef[e] < mf * .01: e -= 1
        c = e
        while c > s and ef[c] > mf * .02: c -= 1
        if e - c < 8 or e - c > 40: c = e - 18      # no clear closure: keep the last 180 ms (the "ks")
        return render(src, c / 100, (e + 2) / 100, dst, target=.35, clean="highpass=f=900"), (e - c) * 10
    raise ValueError(method)

def blend(src, dst):
    full = pcm(src); ef = frames(full)
    s = start_of_sound(ef); m = max(ef) or 1
    peak = max(range(s, len(ef)), key=lambda i: ef[i])
    c = next((i for i in range(peak, len(ef)) if ef[i] < m * .06), None)   # the closure before the final stop
    if c is None: c = peak + 12
    end = max(s / 100 + .12, c / 100 - .06)          # stop before the tongue moves toward the final sound
    return render(src, s / 100, end, dst, fade_out=.09), (c - s) * 10
