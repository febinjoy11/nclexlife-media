"""Long-form 16:9 NCLEX quiz video builder (colorful v8 style).
python build.py KEY  -> out/KEY.mp4 + out/KEY_thumb.jpg
"""
import sys, os, re, math, json, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/claude/anim3')
import themes8
from content import VIDEOS

W, H, SR = 1920, 1080, 24000
FB = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
_fc = {}
def font(s):
    s = int(s)
    if s not in _fc: _fc[s] = ImageFont.truetype(FB, s)
    return _fc[s]
WHITE = (255, 255, 255); DARK = (28, 16, 72); YEL = (255, 210, 60); GREEN = (0, 200, 120); DIM = (95, 85, 140)
OPTC = [(255, 85, 99), (50, 130, 255), (255, 170, 20), (160, 90, 235)]

def wrap(text, f, maxw):
    lines, cur = [], ''
    for w in text.split(' '):
        if cur and f.getlength(cur + ' ' + w) > maxw: lines.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    return lines + [cur]

def background(theme, t=8.0):
    ys, xs = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
    g = (ys / (H // 4) * .6 + xs / (W // 4) * .4)[..., None]
    top = np.array([110, 50, 220], np.float32); bot = np.array([255, 80, 150], np.float32)
    img = Image.fromarray(np.clip(top * (1 - g) + bot * g, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR).convert('RGBA')
    if theme in themes8.THEMES:  # reuse vertical theme art, scaled into the right side
        ov = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        themes8.THEMES[theme](ImageDraw.Draw(ov), t, .55, {})
        ov = ov.crop((0, 900, 1080, 1800)).resize((960, 800))
        img.alpha_composite(ov, (W - 980, H - 820))
    return img.convert('RGB')

def shadow_text(d, xy, s, f, fill, anchor='la'):
    d.text((xy[0] + 4, xy[1] + 4), s, font=f, fill=DARK, anchor=anchor)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)

def header(d, V, label):
    f = font(34); chip = f"NCLEX  ·  {V['topic']}"; cw = f.getlength(chip) + 60
    d.rounded_rectangle((60, 40, 60 + cw, 100), radius=30, fill=(255, 70, 140)); d.text((90, 52), chip, font=f, fill=WHITE)
    if label:
        lw = f.getlength(label) + 50
        d.rounded_rectangle((80 + cw, 40, 80 + cw + lw, 100), radius=30, fill=YEL); d.text((80 + cw + lw / 2, 70), label, font=f, fill=DARK, anchor='mm')
    d.text((W - 60, 70), 'nclex.life', font=font(38), fill=(90, 230, 255), anchor='rm')

def option_cards(d, opts, state, correct):
    # 2x2 grid; state: 'show' | 'reveal'
    cw, ch = 860, 150
    for i, o in enumerate(opts):
        x = 70 + (i % 2) * 920; y = 470 + (i // 2) * 180
        col = OPTC[i]; txt = WHITE
        if state == 'reveal':
            if i == correct: col = GREEN
            else: col = DIM; txt = (200, 195, 225)
        if state == 'reveal' and i == correct:
            d.rounded_rectangle((x - 10, y - 10, x + cw + 10, y + ch + 10), radius=40, outline=WHITE, width=6)
        d.rounded_rectangle((x, y, x + cw, y + ch), radius=32, fill=col)
        d.ellipse((x + 25, y + ch / 2 - 45, x + 115, y + ch / 2 + 45), fill=WHITE)
        d.text((x + 70, y + ch / 2), 'ABCD'[i], font=font(52), fill=col, anchor='mm')
        for fs in (46, 40, 36):
            lines = wrap(o, font(fs), cw - 170)
            if len(lines) <= 2: break
        for j, l in enumerate(lines):
            d.text((x + 145, y + ch / 2 + (j - (len(lines) - 1) / 2) * fs * 1.15), l, font=font(fs), fill=txt, anchor='lm')
        if state == 'reveal' and i == correct:
            cx, cy = x + cw - 60, y + ch / 2
            d.ellipse((cx - 40, cy - 40, cx + 40, cy + 40), fill=WHITE)
            d.line([(cx - 20, cy), (cx - 5, cy + 16), (cx + 22, cy - 16)], fill=GREEN, width=9, joint='curve')

def q_frame(V, bg, n, N, q, state, count=None):
    stem, opts, cor, rat = q
    im = bg.copy(); d = ImageDraw.Draw(im)
    header(d, V, f'QUESTION {n} / {N}')
    f = font(56); lines = wrap(stem, f, 1780)
    if len(lines) > 3: f = font(48); lines = wrap(stem, f, 1780)
    for j, l in enumerate(lines): shadow_text(d, (70, 150 + j * f.size * 1.2), l, f, WHITE)
    option_cards(d, opts, state, cor)
    if count is not None:
        cx, cy, r = W / 2, 935, 80
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=DARK, outline=YEL, width=10)
        d.text((cx, cy), str(count), font=font(90), fill=WHITE, anchor='mm')
        d.text((cx - 130, cy), 'PAUSE & PICK', font=font(46), fill=WHITE, anchor='rm')
        d.text((cx + 130, cy), 'comment A, B, C or D', font=font(40), fill=WHITE, anchor='lm')
    if state == 'reveal':
        f2 = font(42); lines = wrap(rat, f2, 1700)
        bh = 40 + len(lines) * 54
        d.rounded_rectangle((70, 850, W - 70, 850 + bh), radius=28, fill=WHITE)
        for j, l in enumerate(lines): d.text((110, 870 + j * 54), l, font=f2, fill=DARK)
    return im

def title_frame(V, bg, lines, sub):
    im = bg.copy(); d = ImageDraw.Draw(im); header(d, V, '')
    for j, l in enumerate(lines):
        f = font(150); shadow_text(d, (W / 2, 380 + j * 180), l, f, YEL if j == 0 else WHITE, anchor='mm')
    d.rounded_rectangle((W / 2 - 520, 760, W / 2 + 520, 860), radius=50, fill=(90, 230, 255))
    d.text((W / 2, 810), sub, font=font(48), fill=DARK, anchor='mm')
    return im

SPEAK = [('mEq/L', ''), ('mg/dL', ''), ('ng/mL', ''), ('g/dL', ''), ('/mm³', ''), ('INR', 'I N R'), ('PPE', 'P P E'), ('C. diff', 'C diff'),
         ('N95', 'N 95'), (' IM ', ' I M '), ('MRSA', 'mersa'), ('BUN', 'B U N'), ('CT ', 'C T '), ('IV ', 'I V '), ('TB', 'T B'), ('A1C', 'A 1 C')]
def speakable(s):
    for a, b in SPEAK: s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s)

_K = None
def tts(text):
    global _K
    from kokoro_onnx import Kokoro
    if _K is None: _K = Kokoro('/home/claude/kokoro16.onnx', '/home/claude/voices.bin')
    a, sr = _K.create(speakable(text), voice='af_heart', speed=1.05, lang='en-us')
    if sr != SR:
        import scipy.signal as ss
        a = ss.resample_poly(a, SR, sr)
    return a.astype(np.float32)

def tone(f0, dur, g=.25):
    t = np.arange(int(SR * dur)) / SR
    return (g * np.sin(2 * np.pi * f0 * t) * np.exp(-t * 18)).astype(np.float32)
def chime():
    out = np.zeros(int(SR * .9), np.float32)
    for k, f0 in enumerate((784, 1046.5, 1318.5)):
        s = int(SR * .08 * k); t = np.arange(len(out) - s) / SR
        out[s:] += .18 * np.sin(2 * np.pi * f0 * t) * np.exp(-t * 4)
    return out

def build(key):
    V = VIDEOS[key]; out = f'/home/claude/long8/out/{key}'; os.makedirs(out, exist_ok=True)
    bg = background(V['theme'])
    segs = []  # (image path, duration, audio array)
    def add(img, dur, audio=None, name=None):
        p = f'{out}/f{len(segs):03d}.png'; img.save(p)
        a = np.zeros(int(SR * dur), np.float32)
        if audio is not None: a[:min(len(a), len(audio))] += audio[:len(a)]
        segs.append((p, dur, a))
    # intro
    v = tts(V['intro']); add(title_frame(V, bg, V['thumb'], 'Pause on every question and keep score'), len(v) / SR + .6, v)
    N = len(V['qs'])
    for n, q in enumerate(V['qs'], 1):
        stem, opts, cor, rat = q
        read = f"Question {n}. {stem} " + ' '.join(f"{'ABCD'[i]}. {o}." for i, o in enumerate(opts))
        v = tts(read); add(q_frame(V, bg, n, N, q, 'show'), len(v) / SR + .4, v)
        for c in (5, 4, 3, 2, 1):
            add(q_frame(V, bg, n, N, q, 'show', c), 1.0, tone(1800 if c > 1 else 1300, .06))
        v = tts(f"The answer is {'ABCD'[cor]}. {rat}")
        a = np.concatenate([chime()[:int(SR * .5)], v]); add(q_frame(V, bg, n, N, q, 'reveal'), len(a) / SR + .9, a)
    v = tts(f"How many did you get out of {N}? Comment your score below, and follow for a new NCLEX question every day.")
    add(title_frame(V, bg, [f'SCORE / {N}?', 'COMMENT IT'], 'Follow nclex.life for daily questions'), len(v) / SR + 1.0, v)
    # video: concat stills
    with open(f'{out}/list.txt', 'w') as fh:
        for p, dur, _ in segs: fh.write(f"file '{p}'\nduration {dur:.3f}\n")
        fh.write(f"file '{segs[-1][0]}'\n")
    audio = np.concatenate([a for _, _, a in segs]); audio = audio / max(1e-6, np.abs(audio).max()) * .9
    sf.write(f'{out}/audio.wav', audio, SR)
    final = f'/home/claude/long8/out/{key}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{out}/list.txt', '-i', f'{out}/audio.wav',
                    '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-tune', 'stillimage',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-shortest', final], check=True)
    # thumbnail
    th = title_frame(V, bg, V['thumb'], f"Can you get all {N}?").resize((1280, 720))
    th.save(f'/home/claude/long8/out/{key}_thumb.jpg', quality=92)
    print(key, 'duration', round(sum(s[1] for s in segs), 1))

if __name__ == '__main__':
    for k in sys.argv[1:]: build(k)
