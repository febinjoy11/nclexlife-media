"""NCLEX.life "Never mix up again" engine (v9).
Formats: 'vs' (two cards) and 'list' (rows of label/value). Centered layout, big hook on frame 0,
af_heart voice, word captions, save-this end card.
Usage: python mixengine.py build <config.json> <outdir>
       python mixengine.py stills <config.json> <outdir> t1 t2 ...
"""
import sys, os, json, math, re, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, SR = 1080, 1920, 30, 24000
FD = '/usr/share/fonts/opentype/inter/'
_fc = {}
def F(size, w='Black'):
    k = (int(size), w)
    if k not in _fc: _fc[k] = ImageFont.truetype(FD + f'Inter-{w}.otf', int(size))
    return _fc[k]

PAL = {
    'purple': ((22, 10, 58), (68, 34, 150), (12, 6, 34)),
    'teal':   ((4, 30, 40), (10, 92, 104), (2, 16, 22)),
    'navy':   ((10, 16, 52), (40, 50, 140), (6, 8, 28)),
    'plum':   ((40, 8, 46), (120, 30, 110), (20, 4, 24)),
}
WHITE = (255, 255, 255); YEL = (255, 216, 64); RED = (255, 72, 86); ORG = (255, 150, 40)
BLUE = (80, 160, 255); GRN = (40, 220, 140); PINK = (255, 100, 190); CYAN = (90, 225, 255)
COLS = {'red': RED, 'orange': ORG, 'blue': BLUE, 'green': GRN, 'pink': PINK, 'cyan': CYAN, 'yellow': YEL, 'white': WHITE}
def col(c): return COLS.get(c, c) if isinstance(c, str) else tuple(c)

# ---------------- background ----------------
def make_bg(pal):
    top, mid, bot = PAL[pal]
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xs - W * .5) / W) ** 2 + ((ys - H * .38) / H) ** 2)
    g = np.clip(1 - d * 2.1, 0, 1)[..., None]
    v = (ys / H)[..., None]
    base = np.array(top, np.float32) * (1 - v) + np.array(bot, np.float32) * v
    img = base * (1 - g * .9) + np.array(mid, np.float32) * g * .9
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

R = np.random.RandomState(4)
STARS = [(R.rand() * W, R.rand() * H, R.rand() * 6.28, 1 + R.rand() * 2.2) for _ in range(70)]
ECG = [(0, 0), (.30, 0), (.33, -.10), (.36, 0), (.40, 0), (.42, .12), (.45, -1), (.48, .35), (.51, 0), (.60, -.12), (.66, 0), (1, 0)]
def ecg_y(u):
    for i in range(len(ECG) - 1):
        (a1, b1), (a2, b2) = ECG[i], ECG[i + 1]
        if a1 <= u <= a2: return b1 + (b2 - b1) * (u - a1) / (a2 - a1 + 1e-9)
    return 0

def deco(d, t, accent):
    for x, y, ph, s in STARS:
        a = .35 + .65 * (.5 + .5 * math.sin(t * 2.2 + ph))
        c = tuple(int(255 * a * .8) for _ in range(3))
        d.ellipse((x - s, y - s, x + s, y + s), fill=c)
    per = 360; off = (t * 120) % per; y0 = 1640
    pts = [(x, y0 + ecg_y(((x + off) % per) / per) * 70) for x in range(0, W + 1, 4)]
    d.line(pts, fill=tuple(int(c * .45) for c in accent), width=4)

# ---------------- text helpers ----------------
from fontTools.ttLib import TTFont
_CMAP = set(TTFont(FD + 'Inter-Black.otf').getBestCmap().keys())
def renderable(t): return all(ord(ch) in _CMAP or ch == ' ' for ch in t)

def wrap(text, f, maxw):
    out = []
    for para in text.split('\n'):
        cur = ''
        for w in para.split(' '):
            if cur and f.getlength(cur + ' ' + w) > maxw: out.append(cur); cur = w
            else: cur = (cur + ' ' + w).strip()
        out.append(cur)
    return out

def fit(text, maxw, start, wt='Black', minsize=40):
    s = start
    while s > minsize and F(s, wt).getlength(text) > maxw: s -= 4
    return s

def text_img(lines, size, color, wt='Black', glow=False, align='center', lh=1.12, stroke=0, maxw=None):
    f = F(size, wt)
    ws = [f.getlength(l) for l in lines]
    w = int(max(ws + [1])) + 40; h = int(size * lh * len(lines)) + 30
    pad = 40 if glow else 6
    im = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        x = pad + (w - ws[i]) / 2 if align == 'center' else pad
        y = pad + i * size * lh
        if glow: d.text((x, y), l, font=f, fill=color + (255,))
        else:
            d.text((x + 4, y + 5), l, font=f, fill=(0, 0, 0, 150), stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
            d.text((x, y), l, font=f, fill=color + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    if glow:
        g = im.filter(ImageFilter.GaussianBlur(16))
        ga = np.array(g).astype(np.float32); ga[..., 3] *= 1.6; g = Image.fromarray(np.clip(ga, 0, 255).astype(np.uint8))
        out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.alpha_composite(g); out.alpha_composite(im)
        d2 = ImageDraw.Draw(out)
        for i, l in enumerate(lines):
            x = pad + (w - ws[i]) / 2; y = pad + i * size * lh
            d2.text((x, y), l, font=f, fill=color + (255,))
        im = out
    return im

def card_img(w, h, color, fill_a=60, r=34):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=(10, 8, 30, 120), outline=color + (255,), width=5)
    d.rounded_rectangle((5, 5, w - 6, h - 6), radius=r - 4, fill=color + (fill_a // 3,))
    return im

# ---------------- voice ----------------
SPEAK = [('mEq/L', ''), ('mg/dL', ''), ('ng/mL', ''), ('mcg/mL', ''), ('g/dL', ''), ('mm Hg', ''), ('/mm³', ''),
         ('–', ' to '), ('≥', 'at least '), ('≤', 'at most '), ('>', 'over '), ('<', 'under '), ('%', ' percent'),
         ('°C', ' degrees'), ('°F', ' degrees'), ('aPTT', 'A P T T'), ('PT/INR', 'P T, I N R'), ('INR', 'I N R'),
         ('ABG', 'A B G'), ('ICP', 'I C P'), ('MAP', 'map'), ('IV', 'I V'), ('IM', 'I M'), ('PaCO2', 'C O 2'),
         ('PaO2', 'P O 2'), ('HCO3', 'bicarb'), ('NS', 'normal saline'), ('LR', 'lactated Ringer\'s'), ('ANC', 'A N C'),
         ('WBC', 'white count'), ('Hgb', 'hemoglobin'), ('SSRIs', 'S S R Is'), ('SSRI', 'S S R I'), ('DTs', 'D Ts'),
         ('RLQ', 'right lower quadrant'), ('RUQ', 'right upper quadrant'), ('UC', 'U C'), ('TB', 'T B'), ('RN', 'R N'),
         ('RNs', 'R Ns'), ('NG', 'N G'), (' kg', ' kilogram'), (' lb', ' pounds'), ('mo', 'months'), ('hr', 'hours')]
def speakable(s):
    s = ' ' + s + ' '
    for a, b in SPEAK:
        if a in ('mo', 'hr'): s = re.sub(r'(?<=\d)\s?' + a + r'\b', ' ' + b, s); continue
        if a.isalpha() or a in ('PaCO2', 'PaO2', 'HCO3', 'SSRIs', 'SSRI', 'RNs'):
            s = re.sub(r'\b' + re.escape(a) + r'\b', b, s)
        else: s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip()

_K = None
def tts(text, speed=1.13):
    global _K
    from kokoro_onnx import Kokoro
    if _K is None: _K = Kokoro('/home/claude/kokoro16.onnx', '/home/claude/voices.bin')
    a, sr = _K.create(speakable(text), voice='af_heart', speed=speed, lang='en-us')
    a = np.asarray(a, np.float32)
    nz = np.where(np.abs(a) > 0.01)[0]
    if len(nz): a = a[max(0, nz[0] - 600): nz[-1] + 1200]
    return a

def tone(f0, dur, g=.18, decay=14):
    t = np.arange(int(SR * dur)) / SR
    return (g * np.sin(2 * np.pi * f0 * t) * np.exp(-t * decay)).astype(np.float32)
def pop(): return tone(880, .12, .10, 30) + tone(1320, .12, .06, 34)
def whoosh():
    n = int(SR * .35); t = np.arange(n) / SR
    noise = np.random.RandomState(1).randn(n).astype(np.float32)
    env = np.sin(np.pi * t / .35) ** 2
    return (noise * env * .05).astype(np.float32)
def chime():
    out = np.zeros(int(SR * 1.0), np.float32)
    for k, f0 in enumerate((784, 1046.5, 1318.5)):
        s = int(SR * .07 * k); t = np.arange(len(out) - s) / SR
        out[s:] += .08 * np.sin(2 * np.pi * f0 * t) * np.exp(-t * 4)
    return out

# ---------------- plan ----------------
def plan(C, out):
    """Build the segment timeline. Returns list of segments with start/dur/text and audio."""
    segs = []  # dict(kind, idx, text, audio)
    segs.append(dict(kind='hook', text=C['vo_hook']))
    for i, it in enumerate(C['items']):
        segs.append(dict(kind='item', idx=i, text=it.get('vo') or it['text'].replace('\n', ' ')))
    if C.get('punch'): segs.append(dict(kind='punch', text=C['vo_punch']))
    segs.append(dict(kind='end', text=C.get('vo_end', 'Save this for exam day.')))
    t = 0.0; gap = .07
    for s in segs:
        s['audio'] = tts(s['text']); s['start'] = t; s['dur'] = len(s['audio']) / SR
        t += s['dur'] + gap
        if s['kind'] == 'hook': t += .05
    total = t + .5
    C['_total'] = total
    return segs, total

def build_audio(segs, total, path):
    a = np.zeros(int(SR * (total + .2)), np.float32)
    def put(x, at):
        i = int(at * SR); j = min(len(a), i + len(x)); a[i:j] += x[:j - i]
    for s in segs:
        put(s['audio'], s['start'])
        if s['kind'] == 'item': put(pop(), max(0, s['start'] - .04))
        if s['kind'] == 'punch': put(whoosh(), max(0, s['start'] - .2))
        if s['kind'] == 'end': put(chime(), s['start'])
    a = a / max(1e-6, np.abs(a).max()) * .9
    sf.write(path, a, SR)

# ---------------- elements ----------------
class El:
    def __init__(s, img, cx, cy, t_in, t_out, anim='pop'):
        s.img, s.cx, s.cy, s.t_in, s.t_out, s.anim = img, cx, cy, t_in, t_out, anim

def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3

def draw_el(base, e, t):
    if t < e.t_in - .001 or t > e.t_out: return
    u = (t - e.t_in) / .22; ua = (e.t_out - t) / .15
    a = min(1, max(0, ease(u) if e.anim != 'none' else 1), max(0, min(1, ua)))
    if e.t_in <= 0.0: a = min(1, max(0, ua))  # frame 0 elements fully visible
    if a <= .01: return
    img = e.img; sc = 1.0; dx = dy = 0
    if e.anim == 'pop' and e.t_in > 0: sc = 1.18 - .18 * ease(u)
    if e.anim == 'hookpop': sc = 1.08 - .08 * ease(t / .3)
    if e.anim == 'slideL': dx = -80 * (1 - ease(u))
    if e.anim == 'slideR': dx = 80 * (1 - ease(u))
    if e.anim == 'slideU': dy = 50 * (1 - ease(u))
    if abs(sc - 1) > .005:
        img = img.resize((max(1, int(img.width * sc)), max(1, int(img.height * sc))), Image.BILINEAR)
    if a < .99:
        img = img.copy(); al = np.array(img.getchannel('A')).astype(np.float32) * a
        img.putalpha(Image.fromarray(al.astype(np.uint8)))
    base.alpha_composite(img, (int(e.cx - img.width / 2 + dx), int(e.cy - img.height / 2 + dy)))

def build_elements(C, segs, total):
    acc = col(C.get('accent', 'yellow'))
    els = []
    hook_end = next(s['start'] for s in segs if s['kind'] == 'item') - .05
    first_item = hook_end
    punch = next((s for s in segs if s['kind'] == 'punch'), None)
    end = next(s for s in segs if s['kind'] == 'end')
    body_end = (punch['start'] if punch else end['start']) - .05
    # header
    hdr = Image.new('RGBA', (W, 120), (0, 0, 0, 0)); hd = ImageDraw.Draw(hdr)
    hd.text((70, 60), 'nclex.life', font=F(46, 'ExtraBold'), fill=CYAN + (255,), anchor='lm')
    badge = C.get('badge', 'NEVER MIX UP AGAIN'); bf = F(34, 'Black'); bw = bf.getlength(badge) + 50
    hd.rounded_rectangle((W - 70 - bw, 30, W - 70, 90), radius=30, fill=YEL + (255,))
    hd.text((W - 70 - bw / 2, 60), badge, font=bf, fill=(20, 12, 40, 255), anchor='mm')
    els.append(El(hdr, W / 2, 170, 0, total + 1, 'none'))
    # hook
    h = C['hook']
    b1s = fit(h['big1'], 960, 190); b2s = fit(h['big2'], 960, 190)
    bs = min(b1s, b2s)
    els.append(El(text_img([h['big1']], bs, col(h.get('c1', 'red')), glow=True), W / 2, 470, 0, hook_end, 'hookpop'))
    if h.get('join'): els.append(El(text_img([h['join']], 56, (200, 200, 220), wt='Bold'), W / 2, 470 + bs * .62 + 20, 0, hook_end, 'none'))
    els.append(El(text_img([h['big2']], bs, col(h.get('c2', 'orange')), glow=True), W / 2, 470 + bs * 1.25 + 40, 0, hook_end, 'hookpop'))
    ty = 470 + bs * 1.25 + 40 + bs * .55 + 90
    els.append(El(text_img([h['title']], fit(h['title'], 960, 84), WHITE), W / 2, ty, 0, hook_end, 'none'))
    tw = wrap(h['twist'], F(70), 960)
    els.append(El(text_img(tw, fit(max(tw, key=len), 960, 70), YEL), W / 2, ty + 70 + 40 * len(tw), 0, hook_end, 'none'))
    items = C['items']; isegs = [s for s in segs if s['kind'] == 'item']
    if C['kind'] == 'vs':
        L, Rr = C['left'], C['right']
        cw = 465; y0 = 300
        built = []
        both_icons = all(i.get('icon') and renderable(i['icon']) for i in (L, Rr))
        for side, info, cx, anim in (('L', L, 55 + cw / 2, 'slideL'), ('R', Rr, W - 55 - cw / 2, 'slideR')):
            c = col(info['color'])
            first = next((s for s in isegs if items[s['idx']]['side'] == side), None)
            tin = first['start'] - .05 if first else first_item
            parts = []; yy = 40
            if both_icons:
                ic = text_img([info['icon']], fit(info['icon'], cw - 60, 150), c); parts.append((ic, yy + 70, tin)); yy += 165
            nm = wrap(info['name'], F(80), cw - 50)
            ns = min(fit(l, cw - 50, 80) for l in nm)
            ni = text_img(nm, ns, c); parts.append((ni, yy + ni.height / 2 - 10, tin)); yy += ni.height + 20
            for s in isegs:
                it = items[s['idx']]
                if it['side'] != side: continue
                fs = 62
                lines = wrap(it['text'], F(fs, 'ExtraBold'), cw - 60)
                while len(lines) > 2 and fs > 46: fs -= 4; lines = wrap(it['text'], F(fs, 'ExtraBold'), cw - 60)
                ti = text_img(lines, fs, WHITE, wt='ExtraBold', lh=1.08)
                parts.append((ti, yy + ti.height / 2, s['start'] - .05)); yy += ti.height + 22
            built.append((c, cx, anim, tin, parts, yy))
        chh = max(max(b[5] for b in built) + 40, 700)
        for c, cx, anim, tin, parts, yy in built:
            els.append(El(card_img(cw, int(chh), c), cx, y0 + chh / 2, tin, body_end, anim))
            for im, py, t0 in parts:
                els.append(El(im, cx, y0 + py, t0, body_end, anim if t0 == tin else 'slideU'))
    else:  # list
        title = C.get('list_title', '')
        if title: els.append(El(text_img([title], fit(title, 960, 80), YEL), W / 2, 340, first_item, body_end, 'pop'))
        n = len(items); rh = min(200, int(960 / max(n, 1))); y0 = 430
        for k, s in enumerate(isegs):
            it = items[s['idx']]; c = col(it.get('color', C.get('row_color', 'cyan')))
            rw = 960; im = card_img(rw, rh - 22, c, fill_a=50, r=26); d = ImageDraw.Draw(im)
            lab = it['label']; val = it['value']
            vs = fit(val, 520, 66 if rh >= 170 else 56, 'Black', 30); ls = fit(lab, rw - 80 - F(vs).getlength(val) - 40, 62 if rh >= 170 else 52, 'ExtraBold', 28)
            d.text((36, (rh - 22) / 2), lab, font=F(ls, 'ExtraBold'), fill=WHITE + (255,), anchor='lm')
            d.text((rw - 36, (rh - 22) / 2), val, font=F(vs), fill=c + (255,), anchor='rm')
            els.append(El(im, W / 2, y0 + k * rh + rh / 2, s['start'] - .05, body_end, 'slideL'))
    if punch:
        pl = C['punch']; ys = []
        sizes = [fit(p['t'], 960, p.get('size', 110)) for p in pl]
        tot = sum(s * 1.15 for s in sizes); y = 720 - tot / 2
        for p, s in zip(pl, sizes):
            im = text_img([p['t']], s, col(p.get('c', 'yellow')), glow=p.get('glow', True))
            els.append(El(im, W / 2, y + s * .55, punch['start'] - .02, end['start'] - .05, 'pop')); y += s * 1.15
    # end card
    bm = Image.new('RGBA', (260, 330), (0, 0, 0, 0)); bd = ImageDraw.Draw(bm)
    bd.polygon([(20, 0), (240, 0), (240, 320), (130, 230), (20, 320)], fill=YEL + (255,))
    els.append(El(bm, W / 2, 560, end['start'] - .02, total + 1, 'pop'))
    els.append(El(text_img(['SAVE THIS'], 120, WHITE), W / 2, 830, end['start'] + .1, total + 1, 'pop'))
    els.append(El(text_img(['one NCLEX trick a day'], 50, (200, 200, 225), wt='Bold'), W / 2, 935, end['start'] + .2, total + 1, 'none'))
    return els

# ---------------- captions ----------------
def chunks_for(segs, keys):
    out = []
    for s in segs:
        words = s['text'].replace('\n', ' ').split()
        if not words: continue
        groups = []; cur = []
        for w in words:
            cur.append(w)
            if len(cur) >= 3 or w.endswith(('.', ',', ':', '?')): groups.append(cur); cur = []
        if cur: groups.append(cur)
        n = sum(len(g) for g in groups); t = s['start']
        for g in groups:
            d = s['dur'] * len(g) / n; out.append((t, t + d, g)); t += d
    return out

def cap_img(words, keys):
    f = F(64, 'Black'); sp = f.getlength(' ')
    ws = [f.getlength(w) for w in words]; tw = sum(ws) + sp * (len(words) - 1)
    if tw > 980:
        f = F(int(64 * 980 / tw), 'Black'); sp = f.getlength(' '); ws = [f.getlength(w) for w in words]; tw = sum(ws) + sp * (len(words) - 1)
    im = Image.new('RGBA', (int(tw) + 40, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 20
    for w, wl in zip(words, ws):
        clean = re.sub(r'[^\w%.–-]', '', w).lower().strip('.')
        c = YEL if (any(ch.isdigit() for ch in w) or clean in keys) else WHITE
        d.text((x, 55), w, font=f, fill=c + (255,), anchor='lm', stroke_width=8, stroke_fill=(0, 0, 0, 255)); x += wl + sp
    return im

# ---------------- render ----------------
def render(C, outdir, stills=None):
    os.makedirs(outdir, exist_ok=True)
    segs, total = plan(C, outdir)
    if stills is None: build_audio(segs, total, f'{outdir}/audio.wav')
    els = build_elements(C, segs, total)
    bg = make_bg(C.get('palette', 'purple')).convert('RGBA')
    keys = set(k.lower() for k in C.get('keys', []))
    caps = [(a, b, cap_img(g, keys)) for a, b, g in chunks_for(segs, keys)]
    acc = col(C.get('accent', 'yellow'))
    def frame(t):
        im = bg.copy(); d = ImageDraw.Draw(im)
        deco(d, t, (120, 130, 255) if C.get('palette', 'purple') in ('purple', 'navy') else (60, 220, 220))
        d.rectangle((0, 0, int(W * min(1, t / total)), 10), fill=YEL + (255,))
        for e in els: draw_el(im, e, t)
        for a, b, ci in caps:
            if a <= t < b: im.alpha_composite(ci, (int(W / 2 - ci.width / 2), 1380)); break
        return im.convert('RGB')
    if stills is not None:
        for t in stills: frame(float(t)).save(f'{outdir}/still_{t}.png')
        return
    nf = int(total * FPS)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', f'{outdir}/audio.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p',
                          '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-shortest',
                          '-movflags', '+faststart', f'{outdir}/{C["id"]}.mp4'], stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    frame(0.25).save(f'{outdir}/{C["id"]}_cover.jpg', quality=92)
    json.dump({'total': total}, open(f'{outdir}/{C["id"]}.json', 'w'))
    print(C['id'], round(total, 1))

if __name__ == '__main__':
    cmd, cfgp, out = sys.argv[1], sys.argv[2], sys.argv[3]
    C = json.load(open(cfgp))
    if cmd == 'build': render(C, out)
    else: render(C, out, stills=sys.argv[4:])
