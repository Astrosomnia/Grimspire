#!/usr/bin/env python3
"""Readability checks for a piece of art (see docs/ART-READABILITY.md). Used by tools/bk_import.py on every part.

    python3 tools/art_check.py <library version id> [...]      # e.g. asset-30663904acde901ec8905590 (original S01)

Measures the Body (or the Back for Back-only parts), at the size it's drawn in game:
- colours: distinct opaque colours. Kit parts usually 4-12; a painted or generated image runs to hundreds.
- near: share of colours that have another within 4 RGB steps. Gradients and downscaling make these; hand-placed
  pixel art has almost none.
- lone: share of pixels whose colour matches none of their 4 neighbours (grain, dithering, resampling noise).
- soft: share of edge pixels with partial alpha (a resampled edge).
- detail: at game pixels (art scaled by 27/50 x game_scale), the share of neighbouring pixels whose brightness
  differs by 6+ (out of 255). Calibrated on the 1x K05d bridge Jarred liked (0.28); above 0.35 reads as grain on a
  kit part. Landmarks and statues may run higher (the original S01 saint head is 0.37).

Verdict: fail on the downscale tells (near, lone, soft, colours over 32); warn on detail over the tier's line or
13-32 colours; otherwise pass. Tiers: kit parts (K, BK, R) 0.28 / 0.35; statues and landmarks (S, and anything passed
as --tier landmark) 0.40 / 0.45, since a face is meant to hold more.
"""
import base64, io, json, subprocess, sys
import numpy as np
from PIL import Image

LIMITS = dict(colours_warn=12, colours_fail=32, near_fail=.3, lone_warn=.05, lone_fail=.12, soft_fail=.01,
              detail_warn=.28, detail_fail=.35)


def measure(im, game_scale=1.0, tier='kit'):
    dw, df = (.40, .45) if tier == 'landmark' else (LIMITS['detail_warn'], LIMITS['detail_fail'])
    a = np.asarray(im.convert('RGBA')).astype(int)
    A = a[..., 3]
    op = A >= 128
    if not op.any():
        return None
    uniq = np.unique(a[op][:, :3], axis=0)
    near = 0.0
    if len(uniq) > 1:
        d = np.sqrt(((uniq[:, None, :] - uniq[None, :, :]) ** 2).sum(-1))
        np.fill_diagonal(d, 999)
        near = float((d.min(1) <= 4).mean())
    soft = float(((A > 0) & (A < 255)).sum() / max(1, (A > 0).sum()))
    c = a[..., :3]
    same = np.zeros(A.shape, bool)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        same |= (np.roll(np.roll(c, dy, 0), dx, 1) == c).all(-1)
    lone = float((op & ~same).sum() / max(1, op.sum()))
    s = 27 / 50 * game_scale
    g = im.convert('RGBA').resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.BOX)
    G = np.asarray(g).astype(float)
    L = .299 * G[..., 0] + .587 * G[..., 1] + .114 * G[..., 2]
    O = G[..., 3] >= 128
    n = k = 0
    for ax in (0, 1):
        o = O & np.roll(O, -1, ax)
        if ax == 0:
            o[-1, :] = False
        else:
            o[:, -1] = False
        n += o.sum()
        k += (o & (abs(L - np.roll(L, -1, ax)) >= 6)).sum()
    detail = float(k / max(1, n))
    m = dict(colours=int(len(uniq)), near=round(near, 2), lone=round(lone, 3), soft=round(soft, 3), detail=round(detail, 3))
    notes, v = [], 'pass'
    if near > LIMITS['near_fail'] or lone > LIMITS['lone_fail'] or soft > LIMITS['soft_fail'] or len(uniq) > LIMITS['colours_fail']:
        v = 'fail'
        notes.append('looks painted or downscaled, not drawn on the grid')
    if detail > df:
        notes.append('detail reads as grain at play size')
        v = 'fail' if v == 'fail' else 'warn'
    elif detail > dw:
        notes.append(f'busier than the {tier} bar ({dw})')
        v = 'fail' if v == 'fail' else 'warn'
    if len(uniq) > LIMITS['colours_warn'] and v == 'pass':
        v, _ = 'warn', notes.append(f'{len(uniq)} colours on one part')
    if lone > LIMITS['lone_warn'] and v == 'pass':
        v, _ = 'warn', notes.append('scattered single pixels')
    m['verdict'], m['notes'] = v, notes
    return m


def check_doc(doc):
    fr = (doc.get('frames') or [{}])[0]
    src = fr.get('body')
    im = Image.open(io.BytesIO(base64.b64decode(src.split(',', 1)[1]))) if src else None
    if im is None or not (np.asarray(im.convert('RGBA'))[..., 3] >= 128).any():
        b = fr.get('back')
        im = Image.open(io.BytesIO(base64.b64decode(b.split(',', 1)[1]))) if b else None
    tier = 'landmark' if str(doc.get('code') or '').startswith('S') else 'kit'
    return measure(im, float(doc.get('game_scale') or 1), tier) if im else None


if __name__ == '__main__':
    root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    for vid in sys.argv[1:]:
        doc = json.loads(subprocess.run(['git', '-C', root, 'show', f'origin/art/weapon-lab:art/lab/hosted/library/{vid}.forge.json'],
                                        capture_output=True, check=True).stdout)
        print(vid, doc.get('name'), json.dumps(check_doc(doc)))
