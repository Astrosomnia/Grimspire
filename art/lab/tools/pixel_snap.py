#!/usr/bin/env python3
"""Snap a painterly Forge piece back to pixel art that matches the live kit.

  python3 pixel_snap.py IN.forge.json OUT.forge.json --ramp-from LIVE.forge.json [options]

What it does to Body (and Back, darker), leaving alpha, Emissive, Guts and Height alone:
  1. --smooth R    median filter (radius R) to kill painted speckle before quantising (default 1)
  2. ramp          tones come from the ramp piece's Body (the live piece it replaces, or any kit
                   piece of the same material), sorted dark to light; --tones N resamples that ramp
                   to N steps (N above the ramp's own count interpolates between its tones: more
                   fidelity, same palette family)
  3. quantise      each pixel goes to the ramp step at its brightness rank (histogram matched, so
                   the drawing's light and shadow land on the whole ramp)
  4. --clean K     K passes of a majority filter that removes lone pixels and 1-px noise, so tones
                   sit in clusters like hand-placed pixels (default 2)
  5. --outline     darkest ramp tone on the 1-px silhouette edge, like the kit's outlines (default on)
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


def lum(rgb):
    return rgb[..., :3].astype(float) @ [0.299, 0.587, 0.114]


def ramp_of(body, n):
    m = body[:, :, 3] > 127
    cols, cnt = np.unique(body[:, :, :3][m].reshape(-1, 3), axis=0, return_counts=True)
    if len(cols) > 24:  # painterly ramp source: take n luminance quantiles instead
        px = body[:, :, :3][m].astype(float); L = lum(px); o = np.argsort(L)
        idx = np.linspace(0, len(o) - 1, n + 2)[1:-1].astype(int)
        return np.array([px[o[max(0, i - 50):i + 50]].mean(0) for i in idx])
    cols = cols[cnt > cnt.sum() * 0.004]  # drop stray one-off colours
    cols = cols[np.argsort(lum(cols))].astype(float)
    if n == len(cols):
        return cols
    t = np.linspace(0, len(cols) - 1, n)
    lo = np.floor(t).astype(int); hi = np.minimum(lo + 1, len(cols) - 1); f = (t - lo)[:, None]
    return cols[lo] * (1 - f) + cols[hi] * f


def majority(idx, m, passes):
    H, W = idx.shape
    for _ in range(passes):
        pad = np.pad(np.where(m, idx, -1), 1, constant_values=-1)
        nb = np.stack([pad[1 + dy:H + 1 + dy, 1 + dx:W + 1 + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx])
        same = (nb == idx[None]).sum(0)
        # most common neighbour value
        best = idx.copy(); bestc = np.zeros_like(idx)
        for v in np.unique(idx[m]):
            c = (nb == v).sum(0); up = c > bestc; best[up] = v; bestc[up] = c[up]
        flip = m & (same <= 1) & (bestc >= 4)
        idx = np.where(flip, best, idx)
    return idx


def snap(layer, ramp, a, darken=1.0):
    m = layer[:, :, 3] > 127
    rgb = layer[:, :, :3]
    if a.smooth:
        rgb = np.array(Image.fromarray(rgb.astype('uint8')).filter(ImageFilter.MedianFilter(a.smooth * 2 + 1)))
    L = lum(rgb)
    v = L[m]; ranks = np.argsort(np.argsort(v)) / max(len(v) - 1, 1)
    n = len(ramp)
    q = np.zeros(L.shape, int); q[m] = np.minimum((ranks * n).astype(int), n - 1)
    q = majority(q, m, a.clean)
    if a.outline:
        pad = np.pad(m, 1)
        edge = m & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
        q[edge] = 0
    out = layer.copy()
    out[:, :, :3][m] = np.clip(np.round(ramp[q[m]] * darken), 0, 255)
    out[:, :, 3] = np.where(m, 255, 0)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument('inp'); p.add_argument('out')
    p.add_argument('--ramp-from', required=True)
    p.add_argument('--tones', type=int, default=0)
    p.add_argument('--smooth', type=int, default=1)
    p.add_argument('--clean', type=int, default=2)
    p.add_argument('--no-outline', dest='outline', action='store_false')
    p.add_argument('--back-darken', type=float, default=0.62)
    a = p.parse_args()
    d = json.load(open(a.inp)); r = json.load(open(a.ramp_from))
    rb = dec(r['frames'][0]['body'])
    base_n = len(np.unique(rb[:, :, :3][rb[:, :, 3] > 127].reshape(-1, 3), axis=0))
    n = a.tones or min(base_n, 8)
    ramp = ramp_of(rb, n)
    for f in d['frames']:
        f['body'] = enc(snap(dec(f['body']), ramp, a))
        if f.get('back'):
            f['back'] = enc(snap(dec(f['back']), ramp, a, a.back_darken))
    d['notes'] = (d.get('notes') or '').rstrip() + f"\n\nPixel-snapped with pixel_snap.py ({n} tones from {r.get('code')}, smooth {a.smooth}, clean {a.clean})."
    json.dump(d, open(a.out, 'w'))
    print(a.out, n, 'tones')


if __name__ == '__main__':
    main()
