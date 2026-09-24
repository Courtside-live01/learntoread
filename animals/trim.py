# Trim each raw field recording to its liveliest stretch; no effects beyond a short fade and a peak-level match.
import array, glob, os, re, subprocess
LEN = {"horse": 0, "dog": 0, "cow": 0, "duck": 0, "eagle": 0, "lion": 5.0, "rooster": 4.8, "whale": 5.0, "monkey": 4.0, "frog": 4.0, "dolphin": 4.0}
SR = 16000
os.makedirs("animals/clips", exist_ok=True)
for src in sorted(glob.glob("animals/src/*")):
    a = os.path.splitext(os.path.basename(src))[0]
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = array.array("h", pcm); dur = len(x) / SR
    L = LEN[a] if LEN[a] and LEN[a] < dur else dur
    start = 0.0
    if L < dur:  # slide a window and keep the one with the most energy
        hop, win = SR // 10, int(L * SR)
        e = [v * v for v in x]
        best, s = -1, 0
        cur = sum(e[:win])
        for i in range(0, len(x) - win, hop):
            if i: cur += sum(e[i - hop + win:i + win]) - sum(e[i - hop:i])
            if cur > best: best, s = cur, i
        start = s / SR
    fade = min(.35, L / 5)
    af = f"atrim={start:.2f}:{start + L:.2f},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={L - fade:.2f}:d={fade:.2f}"
    tmp = f"animals/clips/{a}.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-ac", "1", "-ar", "32000", "-af", af, tmp], check=True)
    vd = subprocess.run(["ffmpeg", "-i", tmp, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    peak = float(re.search(r"max_volume: (-?[\d.]+) dB", vd).group(1))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af", f"volume={-1 - peak}dB", "-b:a", "64k", f"animals/clips/{a}.mp3"], check=True)
    os.remove(tmp)
    print(f"{a:8} {dur:6.1f}s -> {start:5.1f}-{start + L:5.1f}s  {os.path.getsize(f'animals/clips/{a}.mp3') // 1024} KB")
