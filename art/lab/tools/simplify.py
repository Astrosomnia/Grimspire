#!/usr/bin/env python3
"""Halve the detail of a 2x-density Forge piece: bring it back to 1x density (game_scale 1) and clear stray pixels.

  python3 simplify.py IN.forge.json OUT.forge.json [--clean 2]

- Body, Back, Guts, Emissive: each 2x2 block becomes one pixel. The block's colour is its medoid (the real
  pixel closest to the block's average), so no new colours are invented and lone specks lose to their
  neighbours. A block is solid when at least 2 of its 4 pixels are.
- Height: block mean.
- --clean K: K passes of a majority filter on the Body (and Back) that recolours pixels which differ from
  nearly all their 8 neighbours, so tones sit in clusters.
- Alpha of Height/Back/Guts/Emissive is re-clipped to the new Body where the Forge requires it.
Same game size before and after: w and h halve, game_scale goes from 0.5 to 1.
"""
import argparse, base64, io, json
import numpy as np
from PIL import Image


def dec(u):
    return np.array(Image.open(io.BytesIO(base64.b64decode(u.split(',', 1)[1]))).convert('RGBA')).astype(int)


def enc(a):
    b = io.BytesIO()
    Image.fromarray(np.clip(a, 0, 255).astype('uint8'), 'RGBA').save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


def blocks(a):
    H, W = a.shape[:2]
    a = a[:H - H % 2, :W - W % 2]
    return a.reshape(H // 2, 2, W // 2, 2, 4).transpose(0, 2, 1, 3, 4).reshape(H // 2, W // 2, 4, 4)


def palette_of(a):
    m = a[..., 3] > 127
    cols, cnt = np.unique(a[..., :3][m].reshape(-1, 3), axis=0, return_counts=True)
    if len(cols) > 16:  # painterly: fall back to 8 luminance quantiles
        px = a[..., :3][m].astype(float); L = px @ [.299, .587, .114]; o = np.argsort(L)
        idx = np.linspace(0, len(o) - 1, 10)[1:-1].astype(int)
        return np.array([px[o[max(0, i - 40):i + 40]].mean(0) for i in idx]).round().astype(int)
    return cols[cnt > cnt.sum() * 0.003]


def mean_quant(a, pal):
    """Block average, then snap to the piece's own palette by brightness: texture averages out into flat planes."""
    B = blocks(a).astype(float)
    solid = B[..., 3] > 127
    n = np.maximum(solid.sum(-1, keepdims=True), 1)
    mean = (B[..., :3] * solid[..., None]).sum(-2) / n
    pl = pal.astype(float); Lp = pl @ [.299, .587, .114]; order = np.argsort(Lp); pl = pl[order]; Lp = Lp[order]
    Lm = mean @ [.299, .587, .114]
    # nearest palette tone by brightness, ties to the colour distance
    d = np.abs(Lm[..., None] - Lp[None, None, :]) * 3 + np.sqrt(((mean[..., None, :] - pl[None, None]) ** 2).sum(-1))
    out = np.zeros(mean.shape[:2] + (4,), int)
    out[..., :3] = pl[d.argmin(-1)].round().astype(int)
    out[..., 3] = np.where(solid.sum(-1) >= 2, 255, 0)
    return out


def medoid(a):
    B = blocks(a)                       # h, w, 4 px, rgba
    solid = B[..., 3] > 127
    rgb = B[..., :3].astype(float)
    n = np.maximum(solid.sum(-1, keepdims=True), 1)
    mean = (rgb * solid[..., None]).sum(-2) / n
    dist = ((rgb - mean[..., None, :]) ** 2).sum(-1) + np.where(solid, 0, 1e9)
    pick = dist.argmin(-1)
    out = np.take_along_axis(B, pick[..., None, None], axis=2)[:, :, 0, :].copy()
    keep = solid.sum(-1) >= 2
    out[..., 3] = np.where(keep, 255, 0)
    return out


def mean_block(a):
    B = blocks(a).astype(float)
    out = B.mean(2)
    out[..., 3] = np.where((B[..., 3] > 127).sum(-1) >= 2, 255, 0)
    return out.round().astype(int)


TH = 1


def clean(a, passes):
    m = a[..., 3] > 127
    if not passes or not m.any():
        return a
    cols, inv = np.unique(a[..., :3][m].reshape(-1, 3), axis=0, return_inverse=True)
    idx = np.full(m.shape, -1); idx[m] = inv.ravel()
    H, W = idx.shape
    for _ in range(passes):
        pad = np.pad(idx, 1, constant_values=-1)
        nb = np.stack([pad[1 + dy:H + 1 + dy, 1 + dx:W + 1 + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx])
        same = (nb == idx[None]).sum(0)
        cand = m & (same <= TH)
        if not cand.any():
            break
        ys, xs = np.nonzero(cand)
        for y, x in zip(ys, xs):
            v = nb[:, y, x]; v = v[v >= 0]
            if len(v) < 5: continue
            vals, cnt = np.unique(v, return_counts=True)
            if cnt.max() >= 4: idx[y, x] = vals[cnt.argmax()]
    out = a.copy()
    out[..., :3][m] = cols[idx[m]]
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument('inp'); p.add_argument('out')
    p.add_argument('--clean', type=int, default=2)
    p.add_argument('--mode', choices=['mean', 'medoid'], default='mean', help='mean: average blocks and requantise to the piece palette (flat planes); medoid: keep one real pixel per block')
    p.add_argument('--strength', type=int, default=1, help='recolour pixels with at most this many same-colour neighbours (1 = lone specks, 2-3 = also thin noise)')
    a = p.parse_args()
    global TH; TH = a.strength
    d = json.load(open(a.inp))
    if (d.get('game_scale') or 1) != 0.5:
        raise SystemExit(f"{d.get('code')}: only 2x-density pieces (game_scale 0.5) can be halved")
    for f in d['frames']:
        src = dec(f['body'])
        body = clean(mean_quant(src, palette_of(src)) if a.mode == 'mean' else medoid(src), a.clean)
        m = body[..., 3] > 0
        f['body'] = enc(body)
        for k in ('back', 'guts', 'emis'):
            if f.get(k):
                raw = dec(f[k])
                L = mean_quant(raw, palette_of(raw)) if (a.mode == 'mean' and k == 'back') else medoid(raw)
                if k == 'back': L = clean(L, a.clean)
                if k == 'guts': L[..., 3] = np.where(m, L[..., 3], 0)
                f[k] = enc(L)
        if f.get('height'):
            h = mean_block(dec(f['height']))
            h[..., 3] = np.where(m, 255, 0)
            f['height'] = enc(h)
    for k in ('w', 'h'):
        d[k] = d[k] // 2
    d['game_scale'] = 1
    if isinstance(d.get('base'), (int, float)):
        d['base'] = (int(d['base']) + 1) // 2 - 1   # bottom line, in source px
    for key in ('grip', 'muzzle', 'anchor', 'pivot'):
        if isinstance(d.get(key), dict):
            d[key] = {kk: (v / 2 if isinstance(v, (int, float)) else v) for kk, v in d[key].items()}
    d['notes'] = (d.get('notes') or '').rstrip() + '\n\nSimplified with simplify.py: back to 1x density (2x2 medoid), stray pixels cleaned. Same game size.'
    json.dump(d, open(a.out, 'w'))
    print(a.out, d['w'], 'x', d['h'])


if __name__ == '__main__':
    main()
