"""Topic background themes for NCLEX.life engine v8.
Each theme draws onto a transparent RGBA overlay that is composited over the gradient background.
theme(o, t, k, C): o = ImageDraw on RGBA overlay, t = time, k = visibility (0..1), C = config.
"""
import math
import numpy as np
from PIL import ImageFont

W, H = 1080, 1920
FB = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
_fc = {}
def font(s):
    s = int(s)
    if s not in _fc: _fc[s] = ImageFont.truetype(FB, s)
    return _fc[s]

WH = (255, 255, 255); YE = (255, 225, 90); RED = (255, 80, 110); GRN = (80, 240, 160); CY = (120, 235, 255)
def A(c, a): return c + (int(max(0, min(255, a))),)
def rot(pts, cx, cy, ang):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]

_R = np.random.RandomState(11)
FLOAT = [(_R.rand() * W, _R.rand() * H, .6 + _R.rand() * .8, _R.rand() * 6.28, 20 + _R.rand() * 40) for _ in range(14)]
def floaters(o, t, k, draw_one):
    for i, (x, y, s, ph, sp) in enumerate(FLOAT):
        px = (x + 30 * math.sin(t * .7 + ph)) % W; py = (y - t * sp) % (H + 200) - 100
        draw_one(o, px, py, s, t * (.6 + .3 * (i % 3)) + ph, k * (.55 + .25 * math.sin(t * 2 + ph)))

# ---------- shapes ----------
def heart_pts(cx, cy, s):
    out = []
    for n in range(60):
        a = 2 * math.pi * n / 60
        out.append((cx + 16 * math.sin(a) ** 3 * s, cy - (13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)) * s))
    return out

def capsule(o, cx, cy, L, r, ang, c1, c2, a):
    # two halves of a capsule, rotated
    for half, col in ((-1, c1), (1, c2)):
        pts = []
        for n in range(16):  # rounded end
            th = math.pi / 2 + half * 0 + n * math.pi / 15
            ex = cx + half * (L / 2) ; pts.append((ex + half * r * math.sin(th - math.pi / 2) * -1, cy + r * math.cos(th - math.pi / 2)))
        pts = [(cx, cy - r)] + [(cx + half * L / 2 + half * r * math.cos(th), cy - r * math.sin(th)) for th in np.linspace(math.pi / 2, -math.pi / 2, 14)] + [(cx, cy + r)]
        o.polygon(rot(pts, cx, cy, ang), fill=A(col, a))

def germ(o, cx, cy, r, ang, col, a):
    pts = []
    for n in range(48):
        th = 2 * math.pi * n / 48 + ang
        rr = r * (1 + .08 * math.sin(th * 5 + ang * 2))
        pts.append((cx + rr * math.cos(th), cy + rr * math.sin(th)))
    o.polygon(pts, fill=A(col, a * .55), outline=A(col, a))
    for n in range(10):
        th = 2 * math.pi * n / 10 + ang
        x1, y1 = cx + r * math.cos(th), cy + r * math.sin(th); x2, y2 = cx + r * 1.38 * math.cos(th), cy + r * 1.38 * math.sin(th)
        o.line((x1, y1, x2, y2), fill=A(col, a), width=max(2, int(r * .09)))
        o.ellipse((x2 - r * .11, y2 - r * .11, x2 + r * .11, y2 + r * .11), fill=A(col, a))
    for n in range(4):
        th = n * 1.7 + ang * .5
        x, y = cx + r * .45 * math.cos(th), cy + r * .45 * math.sin(th)
        o.ellipse((x - r * .12, y - r * .12, x + r * .12, y + r * .12), fill=A(WH, a * .6))

def rbc(o, cx, cy, r, ang, a):
    rx, ry = r, r * (.55 + .45 * abs(math.cos(ang)))
    o.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=A(RED, a))
    o.ellipse((cx - rx * .5, cy - ry * .5, cx + rx * .5, cy + ry * .5), fill=A((200, 40, 70), a))

def drop(o, cx, cy, s, col, a):
    o.ellipse((cx - 30 * s, cy - 10 * s, cx + 30 * s, cy + 50 * s), fill=A(col, a))
    o.polygon([(cx - 28 * s, cy + 10 * s), (cx + 28 * s, cy + 10 * s), (cx, cy - 55 * s)], fill=A(col, a))

# ---------- themes ----------
ECG = [(0, 0), (.18, 0), (.22, -.12), (.26, 0), (.30, 0), (.33, .18), (.36, -1.0), (.39, .30), (.42, 0), (1, 0)]
def ecg_y(u):
    for i in range(len(ECG) - 1):
        (a1, b1), (a2, b2) = ECG[i], ECG[i + 1]
        if a1 <= u <= a2: return b1 + (b2 - b1) * (u - a1) / (a2 - a1 + 1e-9)
    return 0

def th_cardiac(o, t, k, C):
    ph = (t % .7) / .7
    beat = 1 + .09 * math.exp(-ph * 9) + .05 * math.exp(-max(0, ph - .2) * 12) * (ph > .2)
    hp = heart_pts(540, 1290, 15 * beat)
    o.polygon(hp, fill=A(RED, 95 * k)); o.line(hp + [hp[0]], fill=A(WH, 120 * k), width=8, joint='curve')
    # sweeping ECG trace
    y0, amp, per = 1520, 85, 360
    head = (t * 600) % (W + 300) - 100
    pts = [(x, y0 + ecg_y(((x + 40) % per) / per) * amp) for x in range(-20, int(head) + 1, 6)]
    if len(pts) > 2:
        n = len(pts); seg = max(2, n // 8)
        for j in range(0, n - 1, seg):
            o.line(pts[j:j + seg + 1], fill=A(GRN, (50 + 180 * (j + seg) / n) * k), width=7, joint='curve')
        hx, hy = pts[-1]; o.ellipse((hx - 12, hy - 12, hx + 12, hy + 12), fill=A(WH, 230 * k))
    o.text((1020, 1430), C.get('theme_value', 'HR 118'), font=font(40), fill=A(GRN, 170 * k), anchor='rm')
    floaters(o, t, k, lambda o, x, y, s, a, kk: o.polygon(heart_pts(x, y, 2.2 * s), fill=A(WH, 70 * kk)))

def th_glucose(o, t, k, C):
    cx, cy = 540, 1300; bob = 10 * math.sin(t * 1.5)
    o.rounded_rectangle((cx - 150, cy - 230 + bob, cx + 150, cy + 200 + bob), radius=60, fill=A(WH, 60 * k), outline=A(WH, 140 * k), width=7)
    o.rounded_rectangle((cx - 110, cy - 180 + bob, cx + 110, cy - 20 + bob), radius=22, fill=A((20, 20, 60), 120 * k))
    val = C.get('theme_value', '250')
    shown = val if (t % 4) > .9 else str(int(abs(math.sin(t * 9)) * 400 + 40))
    o.text((cx, cy - 115 + bob), shown, font=font(96), fill=A(YE, 230 * k), anchor='mm')
    o.text((cx, cy - 48 + bob), 'mg/dL', font=font(32), fill=A(WH, 180 * k), anchor='mm')
    for j in range(2): o.ellipse((cx - 70 + j * 100, cy + 50 + bob, cx - 30 + j * 100, cy + 90 + bob), fill=A(WH, 110 * k))
    o.rectangle((cx - 22, cy + 200 + bob, cx + 22, cy + 300 + bob), fill=A(YE, 110 * k))  # test strip
    drop(o, cx, cy + 345 + bob + 6 * math.sin(t * 3), .7, RED, 170 * k)
    def cube(o, x, y, s, ang, kk):
        sq = [(x - 22 * s, y - 22 * s), (x + 22 * s, y - 22 * s), (x + 22 * s, y + 22 * s), (x - 22 * s, y + 22 * s)]
        o.polygon(rot(sq, x, y, ang), fill=A(WH, 90 * kk), outline=A(WH, 150 * kk))
    floaters(o, t, k, cube)

def th_lungs(o, t, k, C):
    br = .5 + .5 * math.sin(t * 1.8); s = 1 + .07 * br; cx, cy = 540, 1300
    o.line((cx, cy - 330, cx, cy - 130), fill=A(WH, 150 * k), width=26)
    for side in (-1, 1):
        o.line((cx, cy - 140, cx + side * 110, cy - 60), fill=A(WH, 150 * k), width=18)
        pts = []
        for n in range(40):
            th = 2 * math.pi * n / 40
            x = math.cos(th) * 150 * s; y = math.sin(th) * 230 * s
            if side * x < 0: x *= .55
            pts.append((cx + side * 205 + x, cy + 40 + y))
        o.polygon(pts, fill=A((255, 140, 170), (60 + 50 * br) * k), outline=A(WH, 150 * k))
        for b in range(3):
            o.line((cx + side * 110, cy - 60, cx + side * (170 + b * 30), cy + 20 + b * 80), fill=A(WH, 90 * k), width=8)
    o.text((900, 1000), 'SpO₂ ' + C.get('theme_value', '91%'), font=font(44), fill=A(CY, 200 * k), anchor='mm')
    def bubble(o, x, y, s, ang, kk):
        r = 26 * s; o.ellipse((x - r, y - r, x + r, y + r), outline=A(CY, 160 * kk), width=4)
        o.text((x, y), 'O₂', font=font(int(22 * s)), fill=A(WH, 170 * kk), anchor='mm')
    floaters(o, t, k, bubble)

def th_germs(o, t, k, C):
    germ(o, 540 + 20 * math.sin(t * .8), 1290 + 15 * math.cos(t), 150, t * .5, GRN, 160 * k)
    germ(o, 330, 1520, 60, -t * .8, YE, 140 * k); germ(o, 790, 1480, 75, t * .7, (255, 150, 90), 140 * k)
    floaters(o, t, k, lambda o, x, y, s, ang, kk: germ(o, x, y, 22 * s, ang, (GRN, YE, CY)[int(x) % 3], 120 * kk))

def th_pills(o, t, k, C):
    capsule(o, 540, 1290, 300, 95, t * .6, (255, 90, 120), WH, 170 * k)
    # syringe
    x0, y0 = 250, 1560; ang = -.35 + .05 * math.sin(t * 1.4)
    body = rot([(x0, y0 - 28), (x0 + 330, y0 - 28), (x0 + 330, y0 + 28), (x0, y0 + 28)], x0, y0, ang)
    o.polygon(body, fill=A(WH, 70 * k), outline=A(WH, 170 * k))
    fill = .4 + .4 * (.5 + .5 * math.sin(t * 1.2))
    o.polygon(rot([(x0 + 330 * (1 - fill), y0 - 22), (x0 + 330, y0 - 22), (x0 + 330, y0 + 22), (x0 + 330 * (1 - fill), y0 + 22)], x0, y0, ang), fill=A(CY, 140 * k))
    o.line(rot([(x0 + 330, y0), (x0 + 450, y0)], x0, y0, ang), fill=A(WH, 200 * k), width=6)
    o.line(rot([(x0 - 80, y0), (x0, y0)], x0, y0, ang), fill=A(WH, 170 * k), width=16)
    def pill(o, x, y, s, ang, kk):
        if int(x) % 2: capsule(o, x, y, 60 * s, 20 * s, ang, (255, 200, 60), WH, 140 * kk)
        else:
            r = 24 * s; o.ellipse((x - r, y - r, x + r, y + r), fill=A(WH, 120 * kk)); o.line(rot([(x - r * .7, y), (x + r * .7, y)], x, y, ang), fill=A((120, 100, 200), 160 * kk), width=4)
    floaters(o, t, k, pill)

_NR = np.random.RandomState(5)
NEUR = [(540 + _NR.uniform(-230, 230), 1290 + _NR.uniform(-160, 160)) for _ in range(14)]
def th_brain(o, t, k, C):
    cx, cy = 540, 1290
    for dx, dy, rx, ry in [(-120, -40, 160, 130), (110, -50, 170, 135), (-60, 80, 170, 110), (90, 70, 160, 110), (0, -90, 150, 100)]:
        o.ellipse((cx + dx - rx, cy + dy - ry, cx + dx + rx, cy + dy + ry), fill=A((255, 160, 200), 45 * k), outline=A(WH, 120 * k), width=6)
    o.line((cx, cy - 190, cx, cy + 170), fill=A(WH, 90 * k), width=5)
    for i in range(len(NEUR) - 1):
        a, b = NEUR[i], NEUR[(i * 5 + 3) % len(NEUR)]
        o.line((a, b), fill=A(CY, 70 * k), width=3)
        p = (t * .9 + i * .23) % 1
        x, y = a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p
        o.ellipse((x - 9, y - 9, x + 9, y + 9), fill=A(YE, 230 * k * math.sin(math.pi * p)))
    floaters(o, t, k, lambda o, x, y, s, ang, kk: o.ellipse((x - 8 * s, y - 8 * s, x + 8 * s, y + 8 * s), fill=A(YE, 140 * kk)))

def th_blood(o, t, k, C):
    s = 3.2 * (1 + .05 * math.sin(t * 4))
    drop(o, 540, 1300, s, RED, 210 * k)
    o.text((540, 1400), C.get('theme_value', ''), font=font(70), fill=A(WH, 220 * k), anchor='mm')
    floaters(o, t, k, lambda o, x, y, sc, ang, kk: rbc(o, x, y, 30 * sc, ang, 150 * kk))

THEMES = {'cardiac': th_cardiac, 'glucose': th_glucose, 'lungs': th_lungs, 'germs': th_germs,
          'pills': th_pills, 'brain': th_brain, 'blood': th_blood}
