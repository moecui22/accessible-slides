#!/usr/bin/env python3
"""Accessible-slides audit: contrast, CVD separability, text size. Stdlib only.

  python3 audit.py --colors "#d62728,#2ca02c,#0072b2"
  python3 audit.py --contrast "#8a8a8a" "#ffffff"
  python3 audit.py --room --distance 15 --screen-height 2.0
"""
import argparse, math, sys

# ---------- colour basics ----------

def hex_rgb(h):
    h = h.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError('bad hex: ' + h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

def rgb_hex(c):
    return '#' + ''.join('%02x' % max(0, min(255, round(v * 255))) for v in c)

def to_linear(v):
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

def to_srgb(v):
    v = max(0.0, min(1.0, v))
    return v * 12.92 if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055

def luminance(c):
    r, g, b = (to_linear(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(c1, c2):
    a, b = luminance(c1), luminance(c2)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)

# ---------- dichromat simulation (Vienot 1999 / Brettel 1997) ----------

_RGB2LMS = ((17.8824, 43.5161, 4.11935),
            (3.45565, 27.1554, 3.86714),
            (0.0299566, 0.184309, 1.46709))
_LMS2RGB = ((0.0809444479, -0.130504409, 0.116721066),
            (-0.0102485335, 0.0540193266, -0.113614708),
            (-0.000365296938, -0.00412161469, 0.693511405))

def _mul(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(3)) for i in range(3))

def simulate(c, kind):
    """kind: 'protan' | 'deutan' | 'tritan'"""
    lin = tuple(to_linear(v) for v in c)
    L, M, S = _mul(_RGB2LMS, lin)
    if kind == 'protan':
        L = 2.02344 * M - 2.52581 * S
    elif kind == 'deutan':
        M = 0.494207 * L + 1.24827 * S
    elif kind == 'tritan':
        S = -0.395913 * L + 0.801109 * M
    else:
        raise ValueError(kind)
    out = _mul(_LMS2RGB, (L, M, S))
    return tuple(to_srgb(v) for v in out)

# ---------- CIELAB + CIEDE2000 ----------

_WP = (0.95047, 1.0, 1.08883)

def rgb_lab(c):
    r, g, b = (to_linear(v) for v in c)
    X = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    Y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    Z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b
    def f(t):
        return t ** (1 / 3) if t > (6 / 29) ** 3 else t / (3 * (6 / 29) ** 2) + 4 / 29
    fx, fy, fz = f(X / _WP[0]), f(Y / _WP[1]), f(Z / _WP[2])
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))

def ciede2000(lab1, lab2):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7))) if Cb > 0 else 0.5
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    else:
        dhp = h2p - h1p
        dhp -= 360 if dhp > 180 else (-360 if dhp < -180 else 0)
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp / 2))
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) > 180:
        hbp = (h1p + h2p + 360) / 2 if (h1p + h2p) < 360 else (h1p + h2p - 360) / 2
    else:
        hbp = (h1p + h2p) / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30))
         + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6))
         - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dT = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7)) if Cbp > 0 else 0.0
    Sl = 1 + (0.015 * (Lbp - 50) ** 2) / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dT)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2
                     + Rt * (dCp / Sc) * (dHp / Sh))

# ---------- text size ----------

def min_font(distance_m, screen_h_m, arcmin=18.0, xratio=0.52, slide_units=540.0):
    """Minimum font size, in the same units as slide_units (default: points on
    a 7.5in-tall 16:9 slide)."""
    theta = math.radians(arcmin / 60.0)
    x_h = 2 * distance_m * math.tan(theta / 2)
    font_m = x_h / xratio
    return font_m / screen_h_m * slide_units

def arcmin_of(font_units, distance_m, screen_h_m, xratio=0.52, slide_units=540.0):
    font_m = font_units / slide_units * screen_h_m
    x_h = font_m * xratio
    return math.degrees(2 * math.atan(x_h / (2 * distance_m))) * 60

# ---------- reports ----------

def report_colors(hexes):
    cols = [(h, hex_rgb(h)) for h in hexes]
    print('\nColour separability (dE2000 after dichromat simulation)')
    print('  pass >= 15   marginal 5-15   fail < 5\n')
    worst = None
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            (h1, c1), (h2, c2) = cols[i], cols[j]
            row = []
            for kind in ('normal', 'protan', 'deutan', 'tritan'):
                s1 = c1 if kind == 'normal' else simulate(c1, kind)
                s2 = c2 if kind == 'normal' else simulate(c2, kind)
                row.append(ciede2000(rgb_lab(s1), rgb_lab(s2)))
            lo = min(row[1:])
            flag = 'PASS' if lo >= 15 else ('WARN' if lo >= 5 else 'FAIL')
            if worst is None or lo < worst[0]:
                worst = (lo, h1, h2)
            print('  %s  %s vs %s   normal %5.1f | protan %5.1f | deutan %5.1f | tritan %5.1f'
                  % (flag.ljust(4), h1, h2, row[0], row[1], row[2], row[3]))
    if worst and worst[0] < 15:
        print('\n  Worst pair: %s vs %s (dE2000 %.1f). Add a redundant channel '
              '(dash, marker, direct label) or recolour.' % (worst[1], worst[2], worst[0]))

def report_contrast(fg, bg):
    c = contrast(hex_rgb(fg), hex_rgb(bg))
    print('\nContrast %s on %s = %.2f:1' % (fg, bg, c))
    for label, need in (('projected, lit room (body)', 7.0),
                        ('projected, dark room (body)', 4.5),
                        ('screen share, WCAG AA (body)', 4.5),
                        ('large text', 3.0)):
        print('  %-32s need %4.1f:1  %s' % (label, need, 'PASS' if c >= need else 'FAIL'))
    bgl = luminance(hex_rgb(bg))
    dark_bg = bgl < 0.5
    for need in (7.0, 4.5):
        if c >= need:
            continue
        best = None
        rng = range(255, -1, -1) if dark_bg else range(0, 256)
        for v in rng:
            cand = (v / 255,) * 3
            cl = luminance(cand)
            if (max(cl, bgl) + 0.05) / (min(cl, bgl) + 0.05) >= need:
                best = cand
            else:
                if best is not None:
                    break
        if best is not None:
            print('  nearest passing neutral at %.1f:1 -> %s (%.2f:1)'
                  % (need, rgb_hex(best), contrast(best, hex_rgb(bg))))


def report_room(d, h, arcmin, xratio, units, font):
    print('\nText size — screen %.1f m tall, back row at %.1f m' % (h, d))
    for a in (12, 16, 18, 20, 24):
        mark = '  <-- target' if abs(a - arcmin) < 1e-9 else ''
        print('  %2d arcmin x-height  ->  %5.1f pt minimum%s' % (a, min_font(d, h, a, xratio, units), mark))
    if font:
        got = arcmin_of(font, d, h, xratio, units)
        need = min_font(d, h, arcmin, xratio, units)
        print('\n  Your %.0f pt text = %.1f arcmin at the back row  [%s]'
              % (font, got, 'PASS' if font >= need else 'FAIL, need %.0f pt' % need))

def main():
    p = argparse.ArgumentParser(description='Audit slides for low-vision readability.')
    p.add_argument('--colors', help='comma-separated hex colours to check for CVD confusability')
    p.add_argument('--contrast', nargs=2, metavar=('FG', 'BG'), help='foreground and background hex')
    p.add_argument('--room', action='store_true', help='text-size table for a room')
    p.add_argument('--distance', type=float, default=15.0, help='back-row distance in m (default 15)')
    p.add_argument('--screen-height', type=float, default=2.0, help='screen height in m (default 2.0)')
    p.add_argument('--arcmin', type=float, default=18.0, help='target x-height in arcmin (default 18)')
    p.add_argument('--x-ratio', type=float, default=0.52, help='x-height / font-size (default 0.52)')
    p.add_argument('--slide-height', type=float, default=540.0, help='authored slide height in pt (default 540)')
    p.add_argument('--font', type=float, help='a font size to check, in slide units')
    a = p.parse_args()
    if not (a.colors or a.contrast or a.room):
        p.print_help()
        return 1
    if a.colors:
        report_colors([x for x in a.colors.split(',') if x.strip()])
    if a.contrast:
        report_contrast(*a.contrast)
    if a.room:
        report_room(a.distance, a.screen_height, a.arcmin, a.x_ratio, a.slide_height, a.font)
    print()
    return 0

if __name__ == '__main__':
    sys.exit(main())
