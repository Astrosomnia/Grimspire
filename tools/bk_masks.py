#!/usr/bin/env python3
"""Collision from art: turn the Body alpha of chosen BK parts into rectangles on a 4 px grid and write them into
experiments/building-lab.html between the BK_MASKS markers. Run by bk_import.py after every import, so a redrawn part
brings its own collision. A 4x4 cell is solid when at least half its pixels are opaque. Rows of runs are merged downward."""
import json, os, re
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.join(ROOT, 'art', 'experiments', 'bay-kit')
LAB = os.path.join(ROOT, 'experiments', 'building-lab.html')
# parts whose collision the lab takes from the drawing (the rest keep the generator's own shapes)
CODES = ['BK40a', 'BK41a', 'BK43a', 'BK50a', 'BK50b', 'BK60a', 'BK61a', 'BK63a', 'BK63b', 'BK63c', 'BK64a', 'BK65a']
G = 4

def rects(path):
    im = Image.open(path).convert('RGBA'); w, h = im.size; a = im.split()[3].load()
    rows = []
    for gy in range(0, h, G):
        runs, x0 = [], None
        for gx in range(0, w + G, G):
            on = False
            if gx < w:
                n = sum(1 for y in range(gy, min(gy + G, h)) for x in range(gx, min(gx + G, w)) if a[x, y] > 127)
                on = n * 2 >= G * G
            if on and x0 is None: x0 = gx
            if not on and x0 is not None: runs.append((x0, gx - x0)); x0 = None
        rows.append(runs)
    out, open_ = [], {}
    for i, runs in enumerate(rows + [[]]):
        nxt = {}
        for r in runs:
            nxt[r] = open_.pop(r, i)
        for (x, w_), y0 in open_.items(): out.append([x, y0 * G, w_, (i - y0) * G])
        open_ = nxt
    return out

def main():
    parts = json.load(open(os.path.join(KIT, 'parts.json')))['parts']
    m = {}
    for cv in CODES:
        code, v = cv[:-1], cv[-1]
        e = parts.get(code, {}).get('variants', {}).get(v)
        if not e or 'body' not in e['layers']: continue
        m[cv] = {'w': e['w'], 'h': e['h'], 'r': rects(os.path.join(KIT, e['layers']['body']))}
    js = 'const MASK=' + json.dumps(m, separators=(',', ':')) + ';'
    s = open(LAB).read()
    s2 = re.sub(r'(// BK_MASKS_BEGIN[^\n]*\n).*?(\n// BK_MASKS_END)', lambda k: k.group(1) + js + k.group(2), s, flags=re.S)
    assert s2 != s or js in s, 'BK_MASKS markers missing'
    open(LAB, 'w').write(s2)
    print('masks:', ', '.join(f"{k} {len(v['r'])}" for k, v in m.items()))

if __name__ == '__main__': main()
