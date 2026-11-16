#!/usr/bin/env python3
"""Bake rock grit into a Forge piece's Body: the same dots and blotches the lit shader used to add to all stone
before 16 Nov, now only on the pieces that want it (rocks).

  python3 grit.py IN.forge.json OUT.forge.json [--dots 0.07 --dot-dark 0.4 --blotch 0.2 --blotch-dark 0.22 --cell 3]

Seeded by the piece code, so it's the same every run. Works on the art's own pixel grid. Alpha untouched.
"""
import argparse, base64, io, json, zlib
import numpy as np
from PIL import Image


def dec(u):
    return np.array(Image.open(io.BytesIO(base64.b64decode(u.split(',', 1)[1]))).convert('RGBA')).astype(float)


def enc(a):
    b = io.BytesIO()
    Image.fromarray(np.clip(a, 0, 255).round().astype('uint8'), 'RGBA').save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('inp'); p.add_argument('out')
    p.add_argument('--dots', type=float, default=0.07)
    p.add_argument('--dot-dark', type=float, default=0.4)
    p.add_argument('--blotch', type=float, default=0.2)
    p.add_argument('--blotch-dark', type=float, default=0.22)
    p.add_argument('--cell', type=int, default=3)
    a = p.parse_args()
    d = json.load(open(a.inp))
    rng = np.random.default_rng(zlib.crc32((d.get('code') or 'x').encode()))
    for f in d['frames']:
        b = dec(f['body']); H, W = b.shape[:2]; m = b[..., 3] > 127
        k = np.ones((H, W))
        k[rng.random((H, W)) < a.dots] *= 1 - a.dot_dark
        cells = rng.random(((H + a.cell - 1) // a.cell, (W + a.cell - 1) // a.cell)) < a.blotch
        k[np.kron(cells, np.ones((a.cell, a.cell), bool))[:H, :W]] *= 1 - a.blotch_dark
        b[..., :3][m] *= k[m][:, None]
        f['body'] = enc(b)
    d['notes'] = (d.get('notes') or '').rstrip() + f'\n\nGrit baked with grit.py (dots {a.dots:g} at {a.dot_dark:g}, blotches {a.blotch:g} at {a.blotch_dark:g}); the shader no longer adds it to all stone.'
    json.dump(d, open(a.out, 'w'))
    print(a.out)


if __name__ == '__main__':
    main()
