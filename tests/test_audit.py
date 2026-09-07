#!/usr/bin/env python3
"""Check the colour and size maths against published reference values.

    python3 tests/test_audit.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from audit import (hex_rgb, contrast, simulate, rgb_lab, ciede2000,
                   min_font, arcmin_of)

FAILED = []

def check(label, got, want, tol):
    ok = abs(got - want) <= tol
    print("%s %-44s got %8.3f  want %8.3f" % ("PASS" if ok else "FAIL", label, got, want))
    if not ok:
        FAILED.append(label)

# WCAG reference contrast values
check("black on white", contrast(hex_rgb('#000'), hex_rgb('#fff')), 21.0, 0.01)
check("white on white", contrast(hex_rgb('#fff'), hex_rgb('#fff')), 1.0, 0.001)
check("#767676 on white (WCAG AA floor)", contrast(hex_rgb('#767676'), hex_rgb('#fff')), 4.54, 0.02)
check("#595959 on white (WCAG AAA floor)", contrast(hex_rgb('#595959'), hex_rgb('#fff')), 7.00, 0.03)

# Greys carry no chroma, so dichromat simulation must leave them alone
grey = hex_rgb('#808080')
for kind in ('protan', 'deutan', 'tritan'):
    d = ciede2000(rgb_lab(grey), rgb_lab(simulate(grey, kind)))
    check("grey unchanged by %s" % kind, d, 0.0, 1.0)

# A colour must be identical to itself
check("dE2000 of a colour with itself",
      ciede2000(rgb_lab(hex_rgb('#d62728')), rgb_lab(hex_rgb('#d62728'))), 0.0, 1e-9)

# The classic matplotlib red/green pair should collapse under deuteranopia
red, green = hex_rgb('#d62728'), hex_rgb('#2ca02c')
check("tab10 red vs green, normal vision",
      ciede2000(rgb_lab(red), rgb_lab(green)), 71.8, 1.0)
check("tab10 red vs green, deuteranopia",
      ciede2000(rgb_lab(simulate(red, 'deutan')), rgb_lab(simulate(green, 'deutan'))), 5.0, 1.0)

# The recommended replacement pair should survive it
blue, orange = hex_rgb('#0072b2'), hex_rgb('#d55e00')
check("Okabe-Ito blue vs vermillion, deuteranopia",
      ciede2000(rgb_lab(simulate(blue, 'deutan')), rgb_lab(simulate(orange, 'deutan'))), 62.4, 1.0)

# Text size: converting a font size to an angle and back must round trip
f = min_font(15, 2.0, 18)
check("min_font / arcmin_of round trip", arcmin_of(f, 15, 2.0), 18.0, 0.05)
check("18 arcmin at 15 m on a 2 m screen (pt)", f, 40.8, 0.5)

print()
if FAILED:
    print("%d check(s) failed: %s" % (len(FAILED), ", ".join(FAILED)))
    sys.exit(1)
print("All checks passed.")
