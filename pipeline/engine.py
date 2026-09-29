"""NCLEX.life high-retention quiz Short template (v2).

  python nclex_short_v2.py prep   config.json work          # voice (fit to windows) + sound mix
  python nclex_short_v2.py render config.json work START END
  python nclex_short_v2.py final  config.json work out.mp4
  python nclex_short_v2.py still  config.json work 1.0 5.5 ...

Fixed retention timeline (~23 s): hook > question > options > PICK ONE + 3-2-1 > reveal > visual
explanation > mnemonic > engage + next-question tease > loop.
"""
import sys, os, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, SR = 1080, 1920, 30, 48000
FB = os.environ.get('NCLEX_FONT_BOLD', '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf')
BG = (11, 48, 56); DARK = (7, 34, 40); TEAL = (20, 125, 131); AQUA = (127, 224, 207); LIGHT = (216, 241, 236)
WHITE = (255, 255, 255); GREEN = (30, 175, 100); CARD = (21, 76, 86); DIM = (18, 56, 63); DIMTXT = (95, 135, 140)
CORAL = (240, 110, 80); YELLOW = (255, 204, 77); SKIN = (236, 214, 196)

# ---------- fixed retention timeline (seconds) ----------
T = dict(Q=0.00, OPT=-0.25, GAP=0.20, PICK=3.60, CD=4.00, REV=6.40, EXP=8.60, MN=12.60, EN=15.40, END=18.60)
CDD = (T['REV'] - T['CD']) / 3

_fc = {}
def font(size):
    k = max(6, int(size))
    if k not in _fc: _fc[k] = ImageFont.truetype(FB, k)
    return _fc[k]
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, t0, dur): return clamp((t - t0) / dur) if dur > 0 else float(t >= t0)
def eo(p): return 1 - (1 - p) ** 3
def eio(p): return 3 * p * p - 2 * p ** 3
def back(p, s=1.4): p -= 1; return p * p * ((s + 1) * p + s) + 1
def lerp(a, b, p): return a + (b - a) * p
def mix(c1, c2, p): p = clamp(p); return tuple(int(a + (b - a) * p) for a, b in zip(c1, c2))
def punch(t, t0, dur=0.22, frm=1.45):  # returns (scale, alpha)
    p = prog(t, t0, dur); return lerp(frm, 1.0, eo(p)), clamp(p * 1.6)

# ---------- background: gradient, glow, airborne particles ----------
_ys, _xs = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
_base = np.stack([np.full_like(_xs, c) for c in BG], -1) + (_ys / (H // 4))[..., None] * np.array([-5, -12, -13], np.float32)
_R = np.random.RandomState(7)
BGP = [(_R.rand() * W, _R.rand() * H, 2 + _R.rand() * 5, _R.rand() * 6.28, 8 + _R.rand() * 16) for _ in range(46)]

def background(t, dark=0.0):
    img = _base.copy()
    for cx, cy, r, amp in [(W / 8 + 50 * math.sin(t * .6), H / 7 + 40 * math.cos(t * .5), 160, .5),
                           (W / 5 + 40 * math.cos(t * .4), H / 5 + 50 * math.sin(t * .35), 140, .28)]:
        g = np.exp(-((_xs - cx) ** 2 + (_ys - cy) ** 2) / (2 * r * r))[..., None]
        img += g * amp * (np.array(TEAL, np.float32) - img)
    img *= (1 - 0.35 * dark)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    d = ImageDraw.Draw(im)
    for x, y, r, ph, sp in BGP:  # slow floating airborne particles
        px = (x + 22 * math.sin(t * .7 + ph)) % W; py = (y - t * sp) % H
        d.ellipse((px - r, py - r, px + r, py + r), fill=mix(BG, AQUA, (0.16 + 0.08 * math.sin(t + ph)) * (1 - .4 * dark)))
    return im, d

# ---------- text ----------
def parse(text):
    out, on = [], False
    for w in text.split(' '):
        s = w.startswith('**'); w = w[2:] if s else w
        if s: on = True
        e = '**' in w; w = w.replace('**', '')
        out.append((w, on)); on = on and not e
    return out

def lay(words, f, x0, y0, maxw, lh, center=False):
    lines, cur, cw = [], [], 0; sp = f.getlength(' ')
    for w, k in words:
        wl = f.getlength(w)
        if cur and cw + sp + wl > maxw: lines.append((cur, cw)); cur, cw = [], 0
        cw = cw + (sp if cur else 0) + wl; cur.append((w, k, wl))
    if cur: lines.append((cur, cw))
    out = []
    for li, (ws, lw) in enumerate(lines):
        x = x0 + ((maxw - lw) / 2 if center else 0)
        for w, k, wl in ws: out.append((w, k, x, y0 + li * lh, wl)); x += wl + sp
    return out

def kinetic(d, placed, f, t, t0, stag=0.05, a=1.0, dy=0.0, col=WHITE, hl=AQUA, hltxt=DARK, glow=True):
    for i, (w, k, x, y, wl) in enumerate(placed):
        ts = t0 + i * stag; p = eo(prog(t, ts, 0.18))
        if p <= 0: continue
        yy = y + (1 - p) * 22 + dy
        c = col
        if k:
            hp = eo(prog(t, ts + .1, .25)); ww = f.getlength(w.rstrip('.,?!:;'))
            if hp > 0:
                if glow:
                    gl = 0.5 + 0.5 * math.sin(t * 6)
                    d.rounded_rectangle((x - 14, yy - 8, x - 14 + (ww + 28) * hp, yy + f.size * 1.2), radius=14, fill=mix(BG, hl, .35 * a * p * gl))
                d.rounded_rectangle((x - 8, yy - 3, x - 8 + (ww + 16) * hp, yy + f.size * 1.1), radius=10, fill=mix(BG, hl, a * p))
            c = mix(col, hltxt, hp)
        d.text((x, yy), w, font=f, fill=mix(BG, c, p * a))

def ctext(d, s, cx, cy, size, col, a=1.0, sc=1.0):
    if a <= 0.02: return
    d.text((cx, cy), s, font=font(size * sc), fill=mix(BG, col, a), anchor='mm')

def check(d, cx, cy, s, p, col=WHITE, w=10):
    if p <= 0: return
    A, B, C = (cx - s * .45, cy), (cx - s * .12, cy + s * .32), (cx + s * .5, cy - s * .36)
    if p < .4: q = p / .4; d.line([A, (lerp(A[0], B[0], q), lerp(A[1], B[1], q))], fill=col, width=w)
    else: q = (p - .4) / .6; d.line([A, B, (lerp(B[0], C[0], q), lerp(B[1], C[1], q))], fill=col, width=w, joint='curve')

def wrap(text, f, maxw):
    lines, cur = [], ''
    for w in text.split(' '):
        if cur and f.getlength(cur + ' ' + w) > maxw: lines.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    return lines + [cur]

# ---------- option cards ----------
CX, CW, CH, CY0, CGAP = 510, 900, 150, 700, 172
def option_card(d, i, text, cx, cy, sc, fill, txt, circ, a=1.0):
    w, h = CW * sc, CH * sc
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=int(30 * sc), fill=mix(BG, fill, a))
    r = 44 * sc; ccx = x0 + 70 * sc
    d.ellipse((ccx - r, cy - r, ccx + r, cy + r), fill=mix(BG, circ, a))
    d.text((ccx, cy), 'ABCD'[i], font=font(46 * sc), fill=mix(BG, WHITE, a), anchor='mm')
    maxw = w - 250 * sc
    for fs in (52, 46, 42):
        f = font(fs * sc); lines = wrap(text, f, maxw)
        if len(lines) == 1 or (len(lines) == 2 and fs <= 46): break
    lh = f.size * 1.12
    for j, l in enumerate(lines):
        d.text((x0 + 132 * sc, cy + (j - (len(lines) - 1) / 2) * lh), l, font=f, fill=mix(BG, txt, a), anchor='lm')
    return x0, y0, x0 + w, y0 + h

# ---------- explanation scene: airborne ----------
_P = np.random.RandomState(3)
CPART = [(_P.uniform(.25, 1.0) * 230, _P.uniform(-.55, .55) * 260, _P.uniform(0, .9), _P.uniform(4, 9), _P.rand() * 6.28) for _ in range(70)]
def person(d, x, y, s, col, a):
    d.ellipse((x - 58 * s, y - 175 * s, x + 58 * s, y - 59 * s), fill=mix(BG, col, a))
    d.rounded_rectangle((x - 95 * s, y - 45 * s, x + 95 * s, y + 175 * s), radius=int(70 * s), fill=mix(BG, col, a))

def scene_airborne(d, t, C):
    u = t - T['EXP']; out = eio(prog(t, T['MN'] - .3, .3)); A = 1 - out
    # headline statements (swap at 2.4 s)
    f = font(58)
    if u < 2.6:
        a1 = A * (1 - prog(u, 2.25, .25))
        kinetic(d, lay(parse(C['explain_1']), f, 70, 290, 920, 72), f, t, T['EXP'] + .08, stag=.045, a=a1, dy=-prog(u, 2.25, .25) * 60)
    if u > 2.3:
        kinetic(d, lay(parse(C['explain_2']), f, 70, 290, 920, 72), f, t, T['EXP'] + 2.45, stag=.05, a=A)
    px, py = 330, 1000
    sp, sa = punch(t, T['EXP'] + .1, .3, 0.6)
    person(d, px, py, sp, LIGHT, sa * A)
    ctext(d, 'CLIENT WITH TB', px, py + 230, 34, AQUA, sa * A)
    mx, my = px + 45, py - 110
    # negative-pressure room + vent (draws in at 3.3)
    rp = eo(prog(u, 3.3, .6)); vent = (px, 555)
    if rp > 0:
        x0, y0, x1, y1 = 120, 575, 600, 1290
        per = [(x0, y0), (x1, y0), (x1, 840), None, (x1, 1010), (x1, y1), (x0, y1), (x0, y0)]
        segs = [((x0, y0), (x1, y0)), ((x1, y0), (x1, 840)), ((x1, 1010), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]
        L = sum(math.dist(a, b) for a, b in segs); need = L * rp
        for a_, b_ in segs:
            l = math.dist(a_, b_)
            if need <= 0: break
            q = min(1, need / l); d.line([a_, (lerp(a_[0], b_[0], q), lerp(a_[1], b_[1], q))], fill=mix(BG, AQUA, A), width=8); need -= l
        d.rounded_rectangle((px - 70, 540, px + 70, 585), radius=10, fill=mix(BG, TEAL, rp * A))
        for k in range(3):
            d.line((px - 40 + k * 40, 548, px - 40 + k * 40, 578), fill=mix(BG, AQUA, rp * A), width=5)
        # inward airflow arrows at door
        for k, ay in enumerate((880, 925, 970)):
            ph = ((u * 1.6 + k * .33) % 1)
            ax = 700 - ph * 150
            if u > 3.5: d.polygon([(ax - 24, ay), (ax + 6, ay - 14), (ax + 6, ay + 14)], fill=mix(BG, AQUA, A * (1 - ph) * rp))
        ctext(d, 'NEGATIVE-PRESSURE ROOM', 360, 1335, 34, AQUA, rp * A)
        ctext(d, 'air flows in, exhausts out', 360, 1380, 28, LIGHT, rp * A * .8)
    # particles: coughed out, suspended, then pulled to the vent
    for i, (dx, dy, delay, r, ph) in enumerate(CPART):
        te = .35 + delay; pu = u - te
        if pu <= 0: continue
        k = 1 - math.exp(-pu * 2.2)
        x = mx + dx * k + 10 * math.sin(u * 1.3 + ph); y = my + dy * k + 12 * math.cos(u * 1.1 + ph)
        suck = eio(prog(u, 3.7 + (i % 10) * .06, .9))
        x = lerp(x, vent[0], suck); y = lerp(y, vent[1] + 20, suck)
        al = A * min(1, pu * 4) * (1 - prog(suck, .85, .15))
        if al > 0: d.ellipse((x - r, y - r, x + r, y + r), fill=mix(BG, CORAL, .85 * al))
    if 1.3 < u < 3.3:
        a = eo(prog(u, 1.3, .25)) * (1 - prog(u, 3.0, .3)) * A
        ctext(d, 'suspended in the air', 560, 690, 40, CORAL, a)
    # nurse with N95 outside the door
    nx, ny = 850, 1000
    npg = eo(prog(u, 2.4, .45))
    if npg > 0:
        xx = lerp(1200, nx, npg)
        person(d, xx, ny, 0.9, (150, 215, 225), A)
        mp = back(prog(u, 2.8, .3)) if u < 3.1 else 1
        if u > 2.8:
            mw = 70 * mp
            d.rounded_rectangle((xx - mw, ny - 130, xx + mw, ny - 70), radius=20, fill=mix(BG, WHITE, A))
            d.line((xx - mw, ny - 115, xx - 52, ny - 150), fill=mix(BG, WHITE, A), width=4)
            d.line((xx + mw, ny - 115, xx + 52, ny - 150), fill=mix(BG, WHITE, A), width=4)
            ctext(d, 'N95', xx, ny - 100, 30, DARK, A * clamp(mp))
        ctext(d, 'NURSE', xx, ny + 215, 34, AQUA, A)

def scene_flow(d, t, C):  # generic fallback: two statements + icon row from config['flow']
    u = t - T['EXP']; A = 1 - eio(prog(t, T['MN'] - .3, .3)); f = font(58)
    if u < 2.6: kinetic(d, lay(parse(C['explain_1']), f, 70, 290, 920, 72), f, t, T['EXP'] + .08, a=A * (1 - prog(u, 2.25, .25)))
    if u > 2.3: kinetic(d, lay(parse(C['explain_2']), f, 70, 290, 920, 72), f, t, T['EXP'] + 2.45, a=A)
    items = C.get('flow', [])
    for i, s in enumerate(items):
        p = eo(prog(u, .4 + i * 1.0, .35)); y = 640 + i * 230
        if p <= 0: continue
        d.rounded_rectangle((70 + (1 - p) * 200, y, 1010, y + 170), radius=28, fill=mix(BG, CARD, p * A))
        d.ellipse((110, y + 45, 190, y + 125), fill=mix(BG, AQUA, p * A)); check(d, 150, y + 86, 40, p * A, col=DARK, w=7)
        d.text((230, y + 85), s, font=font(48), fill=mix(BG, WHITE, p * A), anchor='lm')
        if i < len(items) - 1 and u > 1.1 + i:
            ap = eo(prog(u, 1.1 + i, .3)) * A
            d.line((540, y + 175, 540, y + 175 + 40 * ap), fill=mix(BG, AQUA, ap), width=8)


def scene_priority(d, t, C):
    u = t - T['EXP']; A = 1 - eio(prog(t, T['MN'] - .3, .3)); f = font(58)
    if u < 2.6: kinetic(d, lay(parse(C['explain_1']), f, 70, 290, 920, 72), f, t, T['EXP'] + .08, stag=.05, a=A * (1 - prog(u, 2.25, .25)), dy=-prog(u, 2.25, .25) * 60)
    if u > 2.3: kinetic(d, lay(parse(C['explain_2']), f, 70, 290, 920, 72), f, t, T['EXP'] + 2.45, stag=.05, a=A)
    ok = C['correct']; order = [i for i in range(4) if i != ok]
    for i, chip in enumerate(C['chips']):
        p = eo(prog(u, .1 + i * .12, .3))
        if p <= 0: continue
        col, row = i % 2, i // 2
        x, y, w, h = 70 + col * 480, 470 + row * 240, 460, 210
        a = p * A
        if i == ok:
            mv = eio(prog(u, 2.3, .5)); x = lerp(x, 540 - w * 1.15 / 2, mv); y = lerp(y, 520, mv); sc = lerp(1, 1.15, mv)
            w2, h2 = w * sc, h * sc
            pulse = .5 + .5 * math.sin(t * 7)
            d.rounded_rectangle((x - 6, y - 6, x + w2 + 6, y + h2 + 6), radius=34, outline=mix(BG, CORAL, a * (.5 + .5 * pulse * prog(u, 1.8, .3))), width=6)
            d.rounded_rectangle((x, y, x + w2, y + h2), radius=30, fill=mix(BG, CARD, a))
            d.ellipse((x + 22, y + 22, x + 86, y + 86), fill=mix(BG, CORAL if u > 1.8 else TEAL, a)); d.text((x + 54, y + 54), 'ABCD'[i], font=font(38), fill=mix(BG, WHITE, a), anchor='mm')
            for j, l in enumerate(chip.split('\n')): d.text((x + 30, y + 110 * sc + j * 50 * sc), l, font=font(42 * sc), fill=mix(BG, WHITE, a))
        else:
            k = order.index(i); sp = eo(prog(u, .9 + k * .3, .3)); fade = 1 - prog(u, 2.3, .3)
            a2 = a * fade
            if a2 <= 0.02: continue
            fill = mix(CARD, DIM, sp); txt = mix(WHITE, DIMTXT, sp)
            d.rounded_rectangle((x, y, x + w, y + h), radius=30, fill=mix(BG, fill, a2))
            d.ellipse((x + 22, y + 22, x + 86, y + 86), fill=mix(BG, mix(TEAL, DIM, sp), a2)); d.text((x + 54, y + 54), 'ABCD'[i], font=font(38), fill=mix(BG, txt, a2), anchor='mm')
            for j, l in enumerate(chip.split('\n')): d.text((x + 30, y + 110 + j * 50), l, font=font(42), fill=mix(BG, txt, a2))
            if sp > 0:
                d.line((x + 20, y + h / 2, x + 20 + (w - 40) * sp, y + h / 2), fill=mix(BG, CORAL, a2), width=8)
                lp = eo(prog(u, 1.05 + k * .3, .2))
                if lp > 0:
                    lf = font(30); lw = lf.getlength('EXPECTED') + 36
                    d.rounded_rectangle((x + w - lw - 16, y + 20, x + w - 16, y + 66), radius=23, fill=mix(BG, YELLOW, a2 * lp))
                    d.text((x + w - 16 - lw / 2, y + 43), 'EXPECTED', font=lf, fill=mix(BG, DARK, a2 * lp), anchor='mm')
    # airway visual
    ap = eo(prog(u, 2.8, .4))
    if ap > 0:
        a = ap * A
        d.line((540, 800, 540, 800 + 70 * ap), fill=mix(BG, AQUA, a), width=8)
        d.polygon([(518, 800 + 70 * ap - 6), (562, 800 + 70 * ap - 6), (540, 800 + 70 * ap + 18)], fill=mix(BG, AQUA, a))
        sw = eio(prog(u, 3.2, 1.0))
        top, bot = 920, 1230
        for side in (-1, 1):
            pts = []
            for k in range(21):
                yy = top + (bot - top) * k / 20
                bulge = math.exp(-((k - 10) / 3.2) ** 2) * 55 * sw
                pts.append((540 + side * (90 - bulge), yy))
            d.line(pts, fill=mix(BG, LIGHT, a), width=12, joint='curve')
        for k in range(4):
            yy = top + 40 + k * 75
            if abs(k - 1.5) > 1.2 or sw < .3:
                d.line((540 - 70, yy, 540 + 70, yy), fill=mix(BG, AQUA, a * .5), width=6)
        tp = eo(prog(u, 3.6, .3)) * A
        if tp > 0:
            ctext(d, C['scene_label'], 540, 1300, 44, CORAL, tp)
            f2 = font(56); tw = f2.getlength(C['scene_tag'])
            d.rounded_rectangle((540 - tw / 2 - 40, 1360, 540 + tw / 2 + 40, 1450), radius=45, fill=mix(BG, YELLOW, tp))
            d.text((540, 1405), C['scene_tag'], font=f2, fill=mix(BG, DARK, tp), anchor='mm')


def scene_sort(d, t, C):
    u = t - T['EXP']; A = 1 - eio(prog(t, T['MN'] - .3, .3)); f = font(58)
    if u < 2.6: kinetic(d, lay(parse(C['explain_1']), f, 70, 280, 920, 72), f, t, T['EXP'] + .08, stag=.05, a=A * (1 - prog(u, 2.25, .25)), dy=-prog(u, 2.25, .25) * 60)
    if u > 2.3: kinetic(d, lay(parse(C['explain_2']), f, 70, 280, 920, 72), f, t, T['EXP'] + 2.45, stag=.05, a=A)
    cols = C['sort_cols']
    hp = eo(prog(u, .05, .3)) * A
    scol = [tuple(c) for c in C.get('sort_colors', [AQUA, GREEN])]; hl = C.get('sort_hl', 1)
    for j, (name, colr) in enumerate([(cols[0], scol[0]), (cols[1], scol[1])]):
        x = 70 + j * 500
        d.rounded_rectangle((x, 440, x + 440, 520), radius=40, fill=mix(BG, colr, hp))
        d.text((x + 220, 480), name, font=font(48), fill=mix(BG, DARK if sum(colr) > 500 else WHITE, hp), anchor='mm')
    slots = {0: 0, 1: 0}
    for i, (lab, dest, why) in enumerate(zip(C['chips'], C['sort_dest'], C['sort_why'])):
        k = slots[dest]; slots[dest] += 1
        ts = .2 + i * .7; ap = eo(prog(u, ts, .22)); mv = eio(prog(u, ts + .3, .4))
        if ap <= 0: continue
        w, h = 440, 180
        sx, sy = 540 - w / 2, 1180
        tx, ty = 70 + dest * 500, 560 + k * 205
        x, y = lerp(sx, tx, mv), lerp(sy, ty, mv)
        a = ap * A
        good = dest == hl
        done = prog(u, ts + .8, .2)
        fill = mix(CARD, tuple(int(c * .55) for c in scol[hl]) if good else CARD, done * (.9 if good else 0))
        d.rounded_rectangle((x, y, x + w, y + h), radius=28, fill=mix(BG, fill, a))
        d.ellipse((x + 18, y + 18, x + 74, y + 74), fill=mix(BG, scol[hl] if good else TEAL, a)); d.text((x + 46, y + 46), 'ABCD'[i], font=font(32), fill=mix(BG, WHITE, a), anchor='mm')
        for jj, l in enumerate(lab.split('\n')): d.text((x + 90, y + 28 + jj * 44), l, font=font(38), fill=mix(BG, WHITE, a))
        if done > 0:
            tf = font(26); tw = tf.getlength(why) + 28
            d.rounded_rectangle((x + w - tw - 14, y + h - 52, x + w - 14, y + h - 12), radius=20, fill=mix(BG, YELLOW, a * done))
            d.text((x + w - 14 - tw / 2, y + h - 32), why, font=tf, fill=mix(BG, DARK, a * done), anchor='mm')
        if good and u > ts + 1.0:
            cp = eo(prog(u, ts + 1.0, .35)) * A
            d.ellipse((x + w - 70, y + 14, x + w - 14, y + 70), fill=mix(BG, WHITE, cp)); check(d, x + w - 42, y + 43, 34, cp, col=scol[hl], w=6)

# ---------- mnemonic ----------
def mnemonic(d, t, C):
    m = C.get('mnemonic'); u = t - T['MN']; A = 1 - eio(prog(t, T['EN'] - .25, .25))
    if not m:
        f = font(92); pl = lay(parse(C.get('principle', '')), f, 70, 620, 940, 112, center=True)
        kinetic(d, pl, f, t, T['MN'] + .1, stag=.09, a=A, hl=CORAL, hltxt=WHITE)
        p = eo(prog(u, 1.6, .35))
        if p > 0: ctext(d, C.get('principle_sub', ''), 540, 1160 + (1 - p) * 30, 50, AQUA, p * A)
        return
    n = len(m['letters']); move = eio(prog(u, .95, .45))
    for i, L in enumerate(m['letters']):
        sc, a = punch(t, T['MN'] + .05 + i * .2, .22, 1.8)
        x = lerp(540 + (i - (n - 1) / 2) * 260, 170, move); y = lerp(820, 560 + i * 200, move)
        size = lerp(250, 140, move) * sc
        ctext(d, L, x, y, size, AQUA, a * A)
        wp = eo(prog(u, 1.3 + i * .18, .3))
        if wp > 0:
            d.text((270 + (1 - wp) * 80, y), m['words'][i], font=font(88), fill=mix(BG, WHITE, wp * A), anchor='lm')
    sc, a = punch(t, T['MN'] + 2.0, .22, 1.7)
    if a > 0:
        f = font(96 * sc); tw = f.getlength(m['tag'])
        shake = 6 * math.sin(u * 90) * (1 - prog(u, 2.0, .25))
        ty = max(1230, 560 + n * 200 + 60)
        d.rounded_rectangle((540 - tw / 2 - 40 + shake, ty - 70 * sc, 540 + tw / 2 + 40 + shake, ty + 70 * sc), radius=int(30 * sc), fill=mix(BG, AQUA, a * A))
        d.text((540 + shake, ty), m['tag'], font=f, fill=mix(BG, DARK, a * A), anchor='mm')

# ---------- engage + next tease ----------
def engage(d, t, C):
    u = t - T['EN']; A = 1 - eio(prog(t, T['END'] - .45, .45))
    L = 'ABCD'[C['correct']]
    f = font(112); words = [('Did', False), ('you', False), ('pick', False), (f'{L}?', True)]
    kinetic(d, lay(words, f, 60, 480, 960, 130, center=True), f, t, T['EN'] + .05, stag=.08, a=A, hl=GREEN, hltxt=WHITE, glow=False)
    p = eo(prog(u, .9, .3))
    if p > 0:
        y0 = 720 + (1 - p) * 30; pulse = 1 + .03 * math.sin(u * 7)
        w = 760 * pulse; h = 130 * pulse
        d.rounded_rectangle((540 - w / 2, y0, 540 + w / 2, y0 + h), radius=int(65 * pulse), fill=mix(BG, AQUA, p * A))
        px, py = 540 - w / 2 + 80, y0 + h / 2
        d.polygon([(px - 34, py - 4), (px + 34, py - 30), (px + 10, py + 32), (px, py + 8)], fill=mix(BG, DARK, p * A))
        d.text((px + 70, py), 'SEND to a study buddy', font=font(52), fill=mix(BG, DARK, p * A), anchor='lm')
    p = eo(prog(u, 1.65, .3))
    if p > 0:
        x = 70 - (1 - p) * 300
        d.rounded_rectangle((x, 1000, x + 190, 1070), radius=35, fill=mix(BG, CORAL, p * A))
        d.text((x + 95, 1035), 'NEXT', font=font(40), fill=mix(BG, WHITE, p * A), anchor='mm')
        f2 = font(70)
        kinetic(d, lay(parse(C['next_tease']), f2, 70, 1110, 920, 86), f2, t, T['EN'] + 1.8, stag=.06, a=A, hl=CORAL, hltxt=WHITE)


def captions(d, t, C, work):
    try: lens = json.load(open(os.path.join(work, 'voice_lens.json')))
    except Exception: return
    for key, (at, win, text) in C['voice'].items():
        L = lens.get(key, win)
        if not (at <= t < at + L + .25): continue
        words = text.split(); n = len(words)
        i = min(n - 1, int((t - at) / max(L, .1) * n))
        chunks, cur = [], []
        for k, w in enumerate(words):
            cur.append(k)
            if len(cur) == 4 or w[-1] in '.?!,:': chunks.append(cur); cur = []
        if cur: chunks.append(cur)
        idx = next(c for c in chunks if i in c); start = idx[0]; chunk = [words[k] for k in idx]
        f = font(54); sp = f.getlength(' ')
        tw = sum(f.getlength(w) for w in chunk) + sp * (len(chunk) - 1)
        x = 540 - tw / 2; y = 1605
        d.rounded_rectangle((x - 26, y - 44, x + tw + 26, y + 44), radius=22, fill=DARK)
        for j, w in enumerate(chunk):
            cur = start + j == i
            d.text((x, y), w, font=f, fill=YELLOW if cur else WHITE, anchor='lm'); x += f.getlength(w) + sp

# ---------- frame ----------
def frame(t, C, work=None):
    OY = C.get('options_y', CY0); PY = OY + 3 * CGAP + 180
    dark = eo(prog(t, T['CD'] - .3, .4)) * (1 - eo(prog(t, T['REV'], .3)))
    im, d = background(t, dark)
    d.rectangle((0, 0, W, 9), fill=mix(BG, AQUA, .2)); d.rectangle((0, 0, W * min(1, t / T['END']), 9), fill=AQUA)
    chip = f"NCLEX  ·  {C['topic'].upper()}"; f = font(30); cw = f.getlength(chip) + 56
    d.rounded_rectangle((60, 60, 60 + cw, 112), radius=26, fill=TEAL); d.text((88, 71), chip, font=f, fill=WHITE)
    d.text((1020, 86), 'nclex.life', font=font(32), fill=mix(BG, AQUA, .85), anchor='rm')
    loop = eio(prog(t, T['END'] - .45, .45))

    # HOOK
    if False:
        out = 0
        for i, line in enumerate(C['hook_lines']):
            hs = min(150 if i == 0 else 120, 130 * 930 / font(130).getlength(line))
            sc, a = punch(t, -.3 + i * .45, .22, 1.25)  # line 1 fully visible on frame 0 (scroll-stopping first frame)
            y = 800 + i * 150 - out * 300
            ctext(d, line, 540, y, hs * (1 - .3 * out), WHITE if i == 0 else AQUA, a * (1 - out), sc)
            if i == len(C['hook_lines']) - 1:
                up = eo(prog(t, .8, .3)); tw = font(hs).getlength(line)
                if up > 0: d.rounded_rectangle((540 - tw / 2, y + 78, 540 - tw / 2 + tw * up, y + 92), radius=7, fill=mix(BG, YELLOW, (1 - out)))
    # QUESTION
    if T['Q'] <= t < T['EXP'] + .1:
        out = eio(prog(t, T['EXP'] - .35, .35))
        fq = font(66)
        kinetic(d, lay(parse(C['question']), fq, 70, 250, 930, 80), fq, t, T['Q'] - 1.0, stag=.0, a=1 - out, dy=-out * 150)
    # OPTIONS
    if T['OPT'] <= t < T['EXP'] + .1:
        out = eio(prog(t, T['EXP'] - .35, .35))
        zoom = 1 + .035 * eo(prog(t, T['CD'], .6)) * (1 - eo(prog(t, T['REV'], .2)))
        rev = prog(t, T['REV'], .3); win = eo(prog(t, T['REV'] + .2, .35))
        for i, opt in enumerate(C['options']):
            ts = T['OPT'] + i * T['GAP']
            if t < ts: continue
            p = back(prog(t, ts, .35), 1.2) if t < ts + .35 else 1
            cx = CX + (1 - p) * 350 + out * (-900 if i % 2 else 900)
            cy = OY + i * CGAP + 2.5 * math.sin(t * 2.2 + i * 1.7) * prog(t, T['OPT'] + 2, .5)
            cy = (OY + 1.5 * CGAP) + (cy - (OY + 1.5 * CGAP)) * zoom
            ok = i == C['correct']
            sc, fill, txt, circ = zoom, CARD, WHITE, TEAL
            if T['PICK'] <= t < T['REV']: fill = mix(CARD, TEAL, .12 + .12 * math.sin(t * 5 + i))
            if rev > 0:
                if ok:
                    sc = lerp(zoom, 1.07, win); fill = mix(CARD, GREEN, win); circ = mix(TEAL, (18, 120, 70), win); cx += 14 * win
                else:
                    sc = lerp(zoom, .93, eo(rev)); fill = mix(CARD, DIM, eo(rev)); txt = mix(WHITE, DIMTXT, eo(rev)); circ = mix(TEAL, (35, 75, 82), eo(rev)); cx -= 22 * eo(rev)
            if rev > 0 and ok and win > 0:
                gw = 10 + 6 * math.sin(t * 8)
                d.rounded_rectangle((cx - CW * sc / 2 - gw, cy - CH * sc / 2 - gw, cx + CW * sc / 2 + gw, cy + CH * sc / 2 + gw), radius=40, fill=mix(BG, GREEN, .35 * win * (1 - out)))
            x0, y0, x1, y1 = option_card(d, i, opt, cx, cy, sc, fill, txt, circ, a=1 - out)
            if ok and t >= T['REV'] + .35:
                cp = eo(prog(t, T['REV'] + .35, .35))
                bx = x1 - 20; by = cy
                br = 60 + 90 * eo(prog(t, T['REV'] + .35, .5)); ba = (1 - prog(t, T['REV'] + .35, .5)) * (1 - out)
                if ba > 0: d.ellipse((bx - br, by - br, bx + br, by + br), outline=mix(BG, WHITE, ba), width=6)
                d.ellipse((bx - 56, by - 56, bx + 56, by + 56), fill=mix(BG, WHITE, cp * (1 - out)))
                check(d, bx, by + 2, 62, cp * (1 - out), col=GREEN, w=12)
    # PICK ONE + COUNTDOWN
    if T['PICK'] <= t < T['REV'] + .3:
        a = eo(prog(t, T['PICK'], .2)) * (1 - prog(t, T['REV'], .25))
        sc = punch(t, T['PICK'], .22, 1.6)[0] * (1 + .05 * math.sin(t * 9))
        f = font(56 * sc); tw = f.getlength('PICK ONE')
        d.rounded_rectangle((540 - tw / 2 - 44, PY - 45 * sc, 540 + tw / 2 + 44, PY + 45 * sc), radius=45, fill=mix(BG, AQUA, a))
        d.text((540, PY), 'PICK ONE', font=f, fill=mix(BG, DARK, a), anchor='mm')
    if T['CD'] <= t < T['REV'] + .3:
        a = eo(prog(t, T['CD'], .2)) * (1 - prog(t, T['REV'], .25))
        el = (t - T['CD']) / CDD; n = 3 - min(2, int(el)); fr = el % 1
        pulse = 1 + .12 * (1 - eo(clamp(fr * 4)))
        r = 92 * pulse; cx, cy = 540, PY + 165
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=mix(BG, AQUA, .25 * a), width=14)
        d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * (1 - fr), fill=mix(BG, YELLOW if n > 1 else CORAL, a), width=14)
        ctext(d, str(n), cx, cy, 96, WHITE, a, 1 + .45 * (1 - eo(clamp(fr * 3.5))))
    # REVEAL banner
    if T['REV'] + .45 <= t < T['EXP'] + .1:
        out = eio(prog(t, T['EXP'] - .35, .35))
        sc, a = punch(t, T['REV'] + .45, .22, 1.5); a *= (1 - out)
        lab = f"CORRECT: {'ABCD'[C['correct']]}"; f = font(52 * sc); tw = f.getlength(lab)
        d.rounded_rectangle((540 - tw / 2 - 110, PY + 10 - 50 * sc, 540 + tw / 2 + 40, PY + 10 + 50 * sc), radius=50, fill=mix(BG, GREEN, a))
        check(d, 540 - tw / 2 - 62, PY + 12, 40 * sc, a, w=8)
        d.text((540 + 35, PY + 10), lab, font=f, fill=mix(BG, WHITE, a), anchor='mm')
        p = eo(prog(t, T['REV'] + 1.25, .3)) * (1 - out)
        if p > 0: ctext(d, C['answer_sub'], 540, PY + 125 + (1 - p) * 30, 46, AQUA, p)
    # EXPLANATION
    if T['EXP'] <= t < T['MN'] + .05:
        {'airborne': scene_airborne, 'priority': scene_priority, 'sort': scene_sort}.get(C.get('scene'), scene_flow)(d, t, C)
    if T['MN'] <= t < T['EN'] + .05: mnemonic(d, t, C)
    if t >= T['EN']: engage(d, t, C)
    # 2) series badge
    if C.get('series_no'):
        lab = f"DAILY #{C['series_no']}"; f = font(30); w = f.getlength(lab) + 40
        chipw = font(30).getlength(f"NCLEX  ·  {C['topic'].upper()}") + 56
        d.rounded_rectangle((70 + chipw, 60, 70 + chipw + w, 112), radius=26, fill=YELLOW); d.text((70 + chipw + w / 2, 86), lab, font=f, fill=DARK, anchor='mm')
    # 3) comment-before-reveal prompt during countdown
    if T['CD'] <= t < T['REV']:
        a = eo(prog(t, T['CD'] + .2, .3)) * (1 - prog(t, T['REV'] - .2, .2))
        ctext(d, 'Comment your answer before the reveal', 540, 1610, 42, LIGHT, a)
    if work: captions(d, t, C, work)
    return im

# ---------- audio ----------
def env(n, a=.004, r=.1): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / r)
def S(kind):
    if kind == 'tick': n = int(SR * .045); t = np.arange(n) / SR; return .32 * np.sin(2 * np.pi * 2100 * t) * env(n, .001, .01)
    if kind == 'pop': n = int(SR * .08); t = np.arange(n) / SR; return .3 * np.sin(2 * np.pi * np.cumsum(820 - 4200 * t) / SR) * env(n, .002, .025)
    if kind == 'whoosh':
        n = int(SR * .3); x = np.convolve(np.random.RandomState(2).randn(n), np.ones(20) / 20, 'same'); return .45 * x * np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    if kind == 'chime':
        n = int(SR * 1.0); t = np.arange(n) / SR; out = np.zeros(n)
        for k, f0 in enumerate((784, 1046.5, 1318.5)):
            s0 = int(SR * .07 * k); out[s0:] += np.sin(2 * np.pi * f0 * t[:n - s0]) * env(n - s0, .002, .3)
        return .22 * out
    if kind == 'impact':
        n = int(SR * .35); t = np.arange(n) / SR; return .7 * np.sin(2 * np.pi * np.cumsum(120 - 180 * t) / SR) * env(n, .002, .08)
    if kind == 'beat': n = int(SR * .16); t = np.arange(n) / SR; return .4 * np.sin(2 * np.pi * 72 * t) * env(n, .003, .05)

def fit_voice(src, dst, window):
    import soundfile as sf
    v, sr = sf.read(src); dur = len(v) / sr
    tempo = clamp(dur / window, 1.0, 1.08)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-filter:a', f'atempo={tempo:.3f}', '-ar', str(SR), dst], check=True)
    return dur / tempo

def prep(C, work):
    import soundfile as sf
    from kokoro_onnx import Kokoro
    os.makedirs(work, exist_ok=True)
    k = Kokoro(os.environ.get('KOKORO_MODEL', 'kokoro16.onnx'), os.environ.get('KOKORO_VOICES', 'voices.bin'))
    lens = {}
    out = np.zeros(int(SR * (T['END'] + .3)))
    def put(x, at, g=1.0):
        i = int(at * SR); j = min(len(out), i + len(x)); out[i:j] += g * x[:j - i]
    for key, (at, win, text) in C['voice'].items():
        a, sr = k.create(text, voice=C.get('voice_name', 'am_michael'), speed=C.get('voice_speed', 1.18), lang='en-us')
        raw = os.path.join(work, f'raw_{key}.wav'); fit = os.path.join(work, f'v_{key}.wav')
        sf.write(raw, a, sr); L = fit_voice(raw, fit, win)
        v, _ = sf.read(fit); put(v, at, 1.0); lens[key] = L
        print(key, 'len', round(L, 2), 'window', win, 'OVER' if L > win + .15 else '')
    tt = np.arange(len(out)) / SR
    pad = .03 * (np.sin(2 * np.pi * 110 * tt) + .5 * np.sin(2 * np.pi * 165 * tt)) * (.7 + .3 * np.sin(2 * np.pi * .5 * tt))
    out += pad * np.minimum(1, tt / .3) * np.clip((T['END'] - tt) / .5, 0, 1)
    put(S('impact'), .03, .8); put(S('whoosh'), .4, .6); put(S('whoosh'), T['Q'], .5)
    for i in range(4): put(S('pop'), T['OPT'] + i * T['GAP'], .8)
    put(S('pop'), T['PICK'], .9)
    for s in range(3): put(S('beat'), T['CD'] + s * CDD); put(S('tick'), T['CD'] + s * CDD + CDD / 2, .7)
    put(S('whoosh'), T['REV'], .5); put(S('impact'), T['REV'] + .3, .7); put(S('chime'), T['REV'] + .35)
    put(S('whoosh'), T['EXP'] - .3, .6); put(S('pop'), T['EXP'] + 2.4, .6); put(S('pop'), T['EXP'] + 2.8, .6); put(S('whoosh'), T['EXP'] + 3.3, .5)
    for i in range(3): put(S('pop'), T['MN'] + .05 + i * .2, .9)
    put(S('impact'), T['MN'] + 2.0, .8)
    put(S('whoosh'), T['EN'], .5); put(S('pop'), T['EN'] + 1.65, .7)
    # 5) subtle beat (110 bpm) under hook..countdown, drops out at reveal, softer return in explanation
    bp = 60 / 110
    kick = .5 * np.sin(2 * np.pi * np.cumsum(90 - 60 * np.arange(int(SR * .12)) / SR) / SR) * env(int(SR * .12), .002, .05)
    hat = np.convolve(np.random.RandomState(9).randn(int(SR * .03)), [1, -1], 'same') * env(int(SR * .03), .001, .008) * .25
    b = 0.0
    while b < T['END'] - .6:
        g = .55 if b < T['REV'] else (0 if b < T['EXP'] else .3)
        if g: put(kick, b, g); put(hat, b + bp / 2, g)
        b += bp
    json.dump(lens, open(os.path.join(work, 'voice_lens.json'), 'w'))
    out = out / max(1e-6, np.abs(out).max()) * .9
    sf.write(os.path.join(work, 'audio.wav'), out.astype(np.float32), SR)

def render(C, work, a, b):
    b = min(b, int(T['END'] * FPS)); outp = os.path.join(work, f'chunk_{a:05d}.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', outp], stdin=subprocess.PIPE)
    for fi in range(a, b): p.stdin.write(frame(fi / FPS, C, work).tobytes())
    p.stdin.close(); p.wait(); print('chunk', a, b)

def final(C, work, outpath):
    chunks = sorted(f for f in os.listdir(work) if f.startswith('chunk_'))
    open(os.path.join(work, 'chunks.txt'), 'w').write(''.join(f"file '{c}'\n" for c in chunks))
    tmp = os.path.join(work, 'joined.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', os.path.join(work, 'chunks.txt'), '-i', os.path.join(work, 'audio.wav'),
                    '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', outpath], check=True)
    print('done', outpath)

if __name__ == '__main__':
    mode, C, work = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3]
    if mode == 'prep': prep(C, work)
    elif mode == 'render': render(C, work, int(sys.argv[4]), int(sys.argv[5]))
    elif mode == 'final': final(C, work, sys.argv[4])
    elif mode == 'still':
        os.makedirs(work, exist_ok=True)
        for ts in sys.argv[4:]: frame(float(ts), C, work).save(os.path.join(work, f'still_{ts}.png'))
