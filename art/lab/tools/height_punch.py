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


def despeckle(height, body, passes=2, tol=14):
    """Replace only isolated speckle: a pixel that differs by more than tol from all but at most one of its
    8 neighbours takes their median. Lines (mortar, step edges) have two matching neighbours along them and stay."""
    m = body[:, :, 3] > 127
    h = height[:, :, 0].astype(int)
    H, W = h.shape
    for _ in range(passes):
        pad = np.pad(h, 1, mode='edge'); mp = np.pad(m, 1)
        nb = np.stack([pad[1 + dy:H + 1 + dy, 1 + dx:W + 1 + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx])
        nm = np.stack([mp[1 + dy:H + 1 + dy, 1 + dx:W + 1 + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx])
        close = ((np.abs(nb - h[None]) <= tol) & nm).sum(0)
        med = np.median(np.where(nm, nb, np.nan), axis=0)
        fix = m & (close <= 1) & (nm.sum(0) >= 5)
        h = np.where(fix, np.nan_to_num(med, nan=h).round().astype(int), h)
    out = height.copy(); out[:, :, 0] = out[:, :, 1] = out[:, :, 2] = np.clip(h, 0, 255)
    out[:, :, 3] = np.where(m, 255, 0)
    return out


def deblob(height, body, area=24):
    """Remove bumps and pits smaller than `area` pixels (grayscale area opening + closing). Long features such
    as mortar lines, step edges and rib lines exceed the area and survive; dapple and pimples don't."""
    from skimage.morphology import area_opening, area_closing
    m = body[:, :, 3] > 127
    h = fill_outside(height[:, :, 0].astype(float), m, 4)
    h = np.clip(h, 0, 255).astype(np.uint8)
    h = area_closing(area_opening(h, area_threshold=area), area_threshold=area)
    out = height.copy(); out[:, :, 0] = out[:, :, 1] = out[:, :, 2] = h
    out[:, :, 3] = np.where(m, 255, 0)
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
    p.add_argument('--deblob', type=int, default=0, help='remove bumps/pits smaller than this many pixels, keep lines and range (ignores the other options)')
    p.add_argument('--despeckle', action='store_true', help='only remove isolated speckle; keep lines and the original range (ignores the other options)')
    a = p.parse_args()
    d = json.load(open(a.inp))
    for f in d['frames']:
        if not f.get('height'):
            raise SystemExit('no Height layer to punch')
        H, B = dec(f['height']), dec(f['body'])
        f['height'] = enc(deblob(H, B, a.deblob) if a.deblob else despeckle(H, B) if a.despeckle else punch(H, B, a))
    flags = f'deblob {a.deblob}' if a.deblob else 'despeckle only' if a.despeckle else f"stretch {a.stretch[0]:g}-{a.stretch[1]:g}, curve {a.curve:g}, flatten {a.flatten}, levels {a.levels}, recess {a.recess:g}, detail {a.detail:g}"
    d['notes'] = (d.get('notes') or '').rstrip() + f"\n\nHeight punched with height_punch.py ({flags}). {a.note}".rstrip()
    json.dump(d, open(a.out, 'w'))
    print(a.out, flags)


if __name__ == '__main__':
    main()
