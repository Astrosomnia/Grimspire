#!/usr/bin/env python3
"""Computed Height maps for BK parts, built from each part's own art so every part lights the same way:
  - bevel: distance in from the Body's silhouette (and from any hole), so every edge rounds over ~3 px
  - relief: the Body's local lightness (lighter than its surroundings = raised, darker = recessed: mortar, joints, slots)
  - form: the drawn Height, blurred, for the big shapes only (recessed panels, openings), where one exists
Writes <vid>_hgen.png beside the drawn maps and adds 'hgen' to parts.json. The lab and game keep using the drawn
Height until Jarred picks the computed one (the parts library shows both)."""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.join(ROOT, 'art', 'experiments', 'bay-kit')
BEVEL = 3.0

def compute(body, drawn=None):
    a = np.asarray(body.convert('RGBA'), dtype=np.float32) / 255.0
    solid = a[..., 3] > 0.5
    if not solid.any(): return None
    lum = 0.3 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2]
    dist = nd.distance_transform_edt(solid)                       # pixels in from the nearest transparent pixel
    bevel = np.clip(dist / BEVEL, 0, 1) ** 0.6
    # local relief: lightness against a 5 px neighbourhood of solid pixels only
    w = solid.astype(np.float32); k = 5
    mean = nd.uniform_filter(lum * w, k) / np.maximum(nd.uniform_filter(w, k), 1e-3)
    relief = np.clip((lum - mean) * 3.0, -0.5, 0.5)
    if drawn is not None:
        d = np.asarray(drawn.convert('RGBA'), dtype=np.float32) / 255.0
        form = np.where(d[..., 3] > 0.5, d[..., 0], 0.5)
        form = nd.gaussian_filter(form, 1.2); form = (form - form[solid].mean()) * 0.6
    else:
        form = 0.0
    h = 0.18 + 0.42 * bevel + 0.25 * relief + form + 0.15
    h = np.clip(h, 0, 1)
    out = np.zeros(a.shape, dtype=np.uint8); g = (h * 255).astype(np.uint8)
    out[..., 0] = out[..., 1] = out[..., 2] = g; out[..., 3] = np.where(solid, 255, 0)
    return Image.fromarray(out, 'RGBA')

def main(only=None):
    pj = os.path.join(KIT, 'parts.json'); man = json.load(open(pj)); n = 0
    for code, p in man['parts'].items():
        for v, e in p['variants'].items():
            L = e['layers']
            if 'body' not in L or (L.get('back') and not L.get('height')): continue   # back-only parts have no lit Body
            vid = L['body'][:-len('_body.png')]
            if only and vid not in only: continue
            im = compute(Image.open(os.path.join(KIT, L['body'])), Image.open(os.path.join(KIT, L['height'])) if L.get('height') else None)
            if im is None: continue
            im.save(os.path.join(KIT, vid + '_hgen.png')); L['hgen'] = vid + '_hgen.png'; n += 1
    json.dump(man, open(pj, 'w'), indent=1)
    print(f'computed heights: {n}')

if __name__ == '__main__': main(set(sys.argv[1:]) or None)
