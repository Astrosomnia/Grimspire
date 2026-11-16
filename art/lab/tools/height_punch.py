#!/usr/bin/env python3
"""Give a Forge piece's Height layer more depth distinction.

  python3 height_punch.py IN.forge.json OUT.forge.json [options]

Modes (combine freely):
  --stretch LO HI   map the 2nd..98th percentile of the Height onto LO..HI (default 40 225)
  --curve K         S-curve around the middle; K>1 pushes values toward the ends (default 1.6)
  --flatten R       median-filter radius before anything else: wipes mortar lines and speckle so
                    the stretch exaggerates forms, not texture (0 = off, try 2-4)
  --levels N        quantise into N flat depth planes after flattening (0 = off, try 5-7)
  --recess A        push openings' rims and dark-in-Body areas down by up to A grey levels (0 = off)
  --detail D        add back D x the original fine texture at the end (0..1, default 0.25)

Alpha always stays exactly the Body's, so the result passes the Forge's exact-alignment check.
"""
import argparse, base64, io, json
import numpy as np
from PIL import Image, ImageFilter


def dec(u):
    return np.array(Image.open(io.BytesIO(base64.b64decode(u.split(',', 1)[1]))).convert('RGBA'))


def enc(a):
    b = io.BytesIO()
    Image.fromarray(a.astype('uint8'), 'RGBA').save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


def fill_outside(v, m, r):
    """Spread solid values into transparent pixels so filters don't drag edges toward 0."""
    out = v.copy()
    known = m.copy()
    for _ in range(r * 2 + 2):
        if known.all():
            break
        acc = np.zeros_like(out); cnt = np.zeros_like(out)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sh = np.roll(np.roll(out * known, dy, 0), dx, 1); kn = np.roll(np.roll(known, dy, 0), dx, 1)
            acc += sh; cnt += kn
        grow = (~known) & (cnt > 0)
        out[grow] = acc[grow] / cnt[grow]; known = known | grow
    return out


def punch(height, body, a):
    m = body[:, :, 3] > 127
    h = height[:, :, 0].astype(float)
    h0 = fill_outside(h, m, 4)
    base = h0
    if a.flatten:
        img = Image.fromarray(np.clip(h0, 0, 255).astype('uint8'))
        base = np.array(img.filter(ImageFilter.MedianFilter(a.flatten * 2 + 1))).astype(float)
    if a.recess:
        # dark parts of the drawing (window recesses, shadowed joints) and rims of holes sink
        lum = body[:, :, :3].astype(float) @ [0.3, 0.59, 0.11]
        lm = fill_outside(lum, m, 4)
        lm = np.array(Image.fromarray(np.clip(lm, 0, 255).astype('uint8')).filter(ImageFilter.MedianFilter(5))).astype(float)
        lo, hi = np.percentile(lm[m], [5, 60])
        dark = np.clip((hi - lm) / max(hi - lo, 1), 0, 1)
        base = base - a.recess * dark
    v = base[m]
    lo, hi = np.percentile(v, [2, 98])
    t = np.clip((base - lo) / max(hi - lo, 1e-6), 0, 1)
    if a.curve != 1:
        t = np.where(t < .5, .5 * (2 * t) ** a.curve, 1 - .5 * (2 * (1 - t)) ** a.curve)
    if a.levels:
        t = np.round(t * (a.levels - 1)) / (a.levels - 1)
    out = a.stretch[0] + t * (a.stretch[1] - a.stretch[0])
    if a.detail:
        out = out + a.detail * (h0 - base if a.flatten else 0)
    out = np.clip(np.round(out), 0, 255)
    res = np.zeros_like(height)
    res[:, :, 0] = res[:, :, 1] = res[:, :, 2] = out
    res[:, :, 3] = np.where(m, 255, 0)
    return res


def main():
    p = argparse.ArgumentParser()
    p.add_argument('inp'); p.add_argument('out')
    p.add_argument('--stretch', nargs=2, type=float, default=[40, 225])
    p.add_argument('--curve', type=float, default=1.6)
    p.add_argument('--flatten', type=int, default=0)
    p.add_argument('--levels', type=int, default=0)
    p.add_argument('--recess', type=float, default=0)
    p.add_argument('--detail', type=float, default=0.25)
    p.add_argument('--note', default='')
    a = p.parse_args()
    d = json.load(open(a.inp))
    for f in d['frames']:
        if not f.get('height'):
            raise SystemExit('no Height layer to punch')
        f['height'] = enc(punch(dec(f['height']), dec(f['body']), a))
    flags = f"stretch {a.stretch[0]:g}-{a.stretch[1]:g}, curve {a.curve:g}, flatten {a.flatten}, levels {a.levels}, recess {a.recess:g}, detail {a.detail:g}"
    d['notes'] = (d.get('notes') or '').rstrip() + f"\n\nHeight punched with height_punch.py ({flags}). {a.note}".rstrip()
    json.dump(d, open(a.out, 'w'))
    print(a.out, flags)


if __name__ == '__main__':
    main()
