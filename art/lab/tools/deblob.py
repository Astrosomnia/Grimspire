#!/usr/bin/env python3
"""Remove dapple from a Forge piece: small clusters of tone (and the matching bumps in the Height) merge into
their surroundings, while lines and edges (mortar, steps, ribs, outlines) stay.

  python3 deblob.py IN.forge.json OUT.forge.json [--area 16] [--height-area 24]

Body and Back: the piece's tones are ranked dark to light and a grayscale area opening + closing runs on that
rank image, so any light or dark cluster smaller than --area pixels takes the tone around it. No new colours are
invented. Height: the same on its grey values with --height-area. Alpha is untouched. Areas are in source pixels
(a 2x piece's 16 px is 4 game pixels).
"""
import argparse, base64, io, json
import numpy as np
from PIL import Image
from skimage.morphology import area_opening, area_closing


def dec(u):
    return np.array(Image.open(io.BytesIO(base64.b64decode(u.split(',', 1)[1]))).convert('RGBA'))


def enc(a):
    b = io.BytesIO()
    Image.fromarray(a.astype('uint8'), 'RGBA').save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


def tones(layer, area):
    m = layer[..., 3] > 127
    if not m.any() or area <= 0:
        return layer
    cols, inv = np.unique(layer[..., :3][m].reshape(-1, 3), axis=0, return_inverse=True)
    if len(cols) > 64:  # painterly layer: rank by luminance bands instead of exact colours
        L = layer[..., :3].astype(float) @ [.299, .587, .114]
        img = np.clip(L, 0, 255).astype(np.uint8)
        img[~m] = int(np.median(img[m]))
        out = area_closing(area_opening(img, area_threshold=area), area_threshold=area)
        res = layer.copy()
        scale = np.where(L > 0, out / np.maximum(L, 1), 1)[..., None]
        res[..., :3] = np.clip(layer[..., :3] * scale, 0, 255)
        return res
    order = np.argsort(cols.astype(float) @ [.299, .587, .114])
    rank = np.empty(len(cols), int); rank[order] = np.arange(len(cols))
    idx = np.zeros(m.shape, np.uint8)
    idx[m] = rank[inv.ravel()]
    # outside the silhouette: copy the nearest inside value so the filter doesn't treat the edge as a blob
    fill = idx.copy(); known = m.copy()
    for _ in range(6):
        if known.all(): break
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sh = np.roll(np.roll(fill, dy, 0), dx, 1); kn = np.roll(np.roll(known, dy, 0), dx, 1)
            g = ~known & kn; fill[g] = sh[g]; known |= g
    out = area_closing(area_opening(fill, area_threshold=area), area_threshold=area)
    res = layer.copy()
    res[..., :3][m] = cols[order][out[m]]
    return res


def height(layer, body, area):
    m = body[..., 3] > 127
    h = layer[..., 0].copy(); h[~m] = int(np.median(h[m])) if m.any() else 0
    h = area_closing(area_opening(h, area_threshold=area), area_threshold=area)
    res = layer.copy(); res[..., 0] = res[..., 1] = res[..., 2] = h; res[..., 3] = np.where(m, 255, 0)
    return res


def main():
    p = argparse.ArgumentParser()
    p.add_argument('inp'); p.add_argument('out')
    p.add_argument('--area', type=int, default=16)
    p.add_argument('--height-area', type=int, default=24)
    p.add_argument('--emis-snap', type=int, default=0, help='rebuild lit glass from the drawing\'s dark openings within this many px of the painted glow (0 = off)')
    p.add_argument('--emis-area', type=int, default=40, help='fill gaps in lit glass smaller than this (0 = off)')
    a = p.parse_args()
    d = json.load(open(a.inp))
    for f in d['frames']:
        body = dec(f['body'])
        f['body'] = enc(tones(body, a.area))
        if f.get('back'): f['back'] = enc(tones(dec(f['back']), a.area))
        if f.get('height'): f['height'] = enc(height(dec(f['height']), body, a.height_area))
        if f.get('emis') and a.emis_snap:
            # lit glass: window openings are holes in the Body, and the game only lights solid stone. Fill the
            # enclosed openings around the painted glow with dark glass and light them, so the glow fits the tracery.
            from scipy.ndimage import binary_dilation, binary_fill_holes, distance_transform_edt
            e = dec(f['emis']); lit = e[..., 3] > 40; bm = dec(f['body'])[..., 3] > 127
            near = binary_dilation(lit, iterations=a.emis_snap)
            glass = binary_fill_holes(bm) & ~bm & near
            glass |= lit & bm & near & False
            if glass.any():
                B = dec(f['body']); bmask = B[..., 3] > 127
                L = B[..., :3].astype(float) @ [.299, .587, .114]
                darkest = B[..., :3][bmask][np.argmin(L[bmask])]
                B[glass, :3] = darkest; B[glass, 3] = 255
                f['body'] = enc(B)
                if f.get('height'):
                    Hh = dec(f['height']); lo = Hh[..., 0][bmask].min(); Hh[glass, :3] = lo; Hh[glass, 3] = 255; f['height'] = enc(Hh)
                _, (iy, ix) = distance_transform_edt(~lit, return_indices=True)
                e2 = e.copy(); e2[glass] = e[iy[glass], ix[glass]]; e2[glass, 3] = np.maximum(e2[glass, 3], 200)
                f['emis'] = enc(e2)
        if f.get('emis') and a.emis_area:
            # fill pinholes in lit glass: gaps smaller than emis_area inside a lit region take the region's colour
            e = dec(f['emis']); lit = e[..., 3] > 40
            from skimage.morphology import remove_small_holes
            filled = remove_small_holes(lit, area_threshold=a.emis_area) & ~lit
            if filled.any():
                from scipy.ndimage import distance_transform_edt
                _, (iy, ix) = distance_transform_edt(~lit, return_indices=True)
                e[filled] = e[iy[filled], ix[filled]]
                f['emis'] = enc(e)
    d['notes'] = (d.get('notes') or '').rstrip() + f'\n\nDe-dappled with deblob.py (tone clusters under {a.area} px, Height bumps under {a.height_area} px merged; lines kept).'
    json.dump(d, open(a.out, 'w'))
    print(a.out)


if __name__ == '__main__':
    main()
