#!/usr/bin/env python3
"""Render an image as a dichromat sees it, and build a labelled contact sheet.

  python3 simulate_cvd.py slide.png
  python3 simulate_cvd.py slide.png --out out/ --sheet sheet.png

Simulation follows Vienot, Brettel & Mollon (1999) and Brettel et al. (1997),
applied in linear-light RGB. Requires numpy and Pillow.
"""
import argparse, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

RGB2LMS = np.array([[17.8824, 43.5161, 4.11935],
                    [3.45565, 27.1554, 3.86714],
                    [0.0299566, 0.184309, 1.46709]])
LMS2RGB = np.linalg.inv(RGB2LMS)
SHIFT = {
    'protan': np.array([[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]]),
    'deutan': np.array([[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]]),
    'tritan': np.array([[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]]),
}

def _lin(a):
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)

def _srgb(a):
    a = np.clip(a, 0.0, 1.0)
    return np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055)

def simulate(img, kind):
    """img: PIL RGB image. kind: protan | deutan | tritan | grey"""
    a = np.asarray(img.convert('RGB'), dtype=np.float64) / 255.0
    lin = _lin(a)
    if kind == 'grey':
        y = lin @ np.array([0.2126, 0.7152, 0.0722])
        out = np.repeat(y[:, :, None], 3, axis=2)
    else:
        lms = lin @ RGB2LMS.T
        lms = lms @ SHIFT[kind].T
        out = lms @ LMS2RGB.T
    return Image.fromarray((_srgb(out) * 255).round().astype(np.uint8))

def _font(size):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
              '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
              '/System/Library/Fonts/Helvetica.ttc',
              'C:/Windows/Fonts/arialbd.ttf'):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()

def contact_sheet(img, kinds=('protan', 'deutan', 'grey'), cols=2, pad=24, label_h=46):
    panels = [('Normal vision', img)] + [(k.capitalize() if k != 'grey' else 'Greyscale',
                                          simulate(img, k)) for k in kinds]
    w, h = img.size
    rows = (len(panels) + cols - 1) // cols
    W = cols * w + (cols + 1) * pad
    H = rows * (h + label_h) + (rows + 1) * pad
    sheet = Image.new('RGB', (W, H), '#ffffff')
    d = ImageDraw.Draw(sheet)
    f = _font(max(18, h // 26))
    for i, (name, p) in enumerate(panels):
        r, c = divmod(i, cols)
        x = pad + c * (w + pad)
        y = pad + r * (h + label_h + pad)
        d.text((x, y + 4), name, fill='#111111', font=f)
        sheet.paste(p, (x, y + label_h))
        d.rectangle([x, y + label_h, x + w - 1, y + label_h + h - 1], outline='#cccccc')
    return sheet

def main():
    ap = argparse.ArgumentParser(description='Simulate colour-vision deficiency on an image.')
    ap.add_argument('image')
    ap.add_argument('--out', default='out', help='directory for individual simulations')
    ap.add_argument('--sheet', default=None, help='path for the side-by-side contact sheet')
    ap.add_argument('--kinds', default='protan,deutan,grey',
                    help='comma-separated: protan,deutan,tritan,grey')
    a = ap.parse_args()
    img = Image.open(a.image).convert('RGB')
    kinds = [k.strip() for k in a.kinds.split(',') if k.strip()]
    os.makedirs(a.out, exist_ok=True)
    stem = os.path.splitext(os.path.basename(a.image))[0]
    for k in kinds:
        p = os.path.join(a.out, '%s__%s.png' % (stem, k))
        simulate(img, k).save(p)
        print('wrote', p)
    sheet = a.sheet or os.path.join(a.out, '%s__sheet.png' % stem)
    contact_sheet(img, kinds).save(sheet)
    print('wrote', sheet)
    return 0

if __name__ == '__main__':
    sys.exit(main())
