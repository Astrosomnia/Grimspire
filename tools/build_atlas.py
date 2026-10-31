"""Pack Forge kits marked ready into the game's embedded props atlas.

  python tools/build_atlas.py <game.html> [--kits art/forge] [--out game.html] [--only W04,C01] [--dry]

<game.html> is the game source (the Grimspire artifact, or index.html). For every kit in art/forge whose
manifest says ready and whose code has a slot in the game (forge_common.SLOTS), the sprite's first frame
(body with trim, at the atlas's own scale) and its emissive layer are added to the props atlas, and the
slot's rects and points are pointed at them. Untouched sprites stay exactly where they are.

Re-running is safe: a slot already packed from the same kit version is skipped. Packing a newer version
adds it again (the old pixels stay in the atlas, unused); run with --compact to rebuild the atlas from the
rects still in use when that waste matters.

Render only: nothing in the sim changes, so no GV bump is needed. Check the result in the Proving ground.
"""
import argparse, base64, io, json, os, re, sys
from PIL import Image
from forge_common import POINTS, SLOTS

ATLAS = "b.onload=()=>{SPR.props=b;done()};b.src='data:image/png;base64,"


def find_P(s):
    i = s.index('const SPR={ready:false,')
    p = s.index('P:{', i) + 2
    d = 0
    for k in range(p, len(s)):
        if s[k] == '{': d += 1
        elif s[k] == '}':
            d -= 1
            if d == 0:
                return p, k + 1
    raise ValueError('SPR.P not found')


def up_of(s):
    i = s.index('const SPR={ready:false,')
    m = re.search(r',up:(\d+),', s[i:i + 400000])
    return int(m.group(1))


def load_atlas(s):
    i = s.index(ATLAS) + len(ATLAS)
    j = s.index("'", i)
    return i, j, Image.open(io.BytesIO(base64.b64decode(s[i:j]))).convert('RGBA')


def kit_images(kdir, man):
    base = man['id']
    nat = os.path.join(kdir, 'native')
    w, h = man['native_frame']
    def first(label):
        p = os.path.join(nat, f'{base}_{label}.png')
        return Image.open(p).convert('RGBA').crop((0, 0, w, h)) if os.path.exists(p) else None
    body = first('body') or Image.new('RGBA', (w, h))
    trim = first('trim')
    if trim: body.alpha_composite(trim)
    return body, first('emissive')


class Shelf:
    """Shelf packer that appends rows under the existing atlas."""
    def __init__(self, atlas, pad=2):
        self.a = atlas; self.pad = pad; self.x = 0; self.y = atlas.height + pad; self.row = 0
    def place(self, im):
        W = max(self.a.width, im.width)
        if self.x + im.width > W:
            self.x = 0; self.y += self.row + self.pad; self.row = 0
        x, y = self.x, self.y
        need_w, need_h = max(self.a.width, x + im.width), max(self.a.height, y + im.height)
        if (need_w, need_h) != self.a.size:
            n = Image.new('RGBA', (need_w, need_h)); n.paste(self.a, (0, 0)); self.a = n
        self.a.paste(im, (x, y))
        self.x += im.width + self.pad; self.row = max(self.row, im.height)
        return [x, y, im.width, im.height]


def compact(P, atlas):
    """Rebuild the atlas from the rects still referenced, top to bottom."""
    out = Image.new('RGBA', (atlas.width, 1)); sh = Shelf(out); sh.y = 0
    for k in sorted(P, key=lambda k: (P[k]['r'][1], P[k]['r'][0])):
        x, y, w, h = P[k]['r']
        P[k]['r'] = sh.place(atlas.crop((x, y, x + w, y + h)))
    return sh.a


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('game')
    ap.add_argument('--kits', default=os.path.join(os.path.dirname(__file__), '..', 'art', 'forge'))
    ap.add_argument('--out')
    ap.add_argument('--only', help='comma-separated codes to pack (still must be ready)')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--compact', action='store_true')
    a = ap.parse_args()
    s = open(a.game).read()
    p0, p1 = find_P(s)
    P = json.loads(s[p0:p1])
    u = up_of(s)
    ai, aj, atlas = load_atlas(s)
    shelf = Shelf(atlas)
    only = set(c.strip().upper() for c in a.only.split(',')) if a.only else None
    done, skipped = [], []
    for kd in sorted(os.listdir(a.kits)) if os.path.isdir(a.kits) else []:
        mp = os.path.join(a.kits, kd, 'manifest.json')
        if not os.path.exists(mp): continue
        man = json.load(open(mp))
        code = man.get('code')
        if not man.get('ready') or (only and code not in only): continue
        slot = SLOTS.get(code)
        if not slot or slot not in P:
            skipped.append(f'{kd} (no slot in the game for {code})'); continue
        tag = f"{man['id']}@{man.get('updated')}"
        if P[slot].get('forge') == tag:
            skipped.append(f'{kd} (already packed)'); continue
        body, emis = kit_images(os.path.join(a.kits, kd), man)
        big = lambda im: im.resize((im.width * u, im.height * u), Image.NEAREST)
        e = dict(P[slot]); e['r'] = shelf.place(big(body)); e['forge'] = tag
        pts = man.get('points_native') or {}
        fmap = dict(POINTS.get(slot, {}))
        if 'g' in P[slot]: fmap.setdefault('grip', 'g')
        if 'm' in P[slot]: fmap.setdefault('muzzle', 'm')
        for fp, field in fmap.items():
            if pts.get(fp): e[field] = [float(pts[fp][0]), float(pts[fp][1])]
        P[slot] = e
        if emis is not None and emis.getbbox():
            P[slot + '_e'] = {'r': shelf.place(big(emis))}
        elif slot + '_e' in P:
            P[slot + '_e'] = {'r': shelf.place(Image.new('RGBA', (body.width * u, body.height * u)))}
        done.append(f'{kd} -> {slot}')
    atlas = shelf.a
    if a.compact:
        atlas = compact(P, atlas)
    for d in done: print('packed', d)
    for k in skipped: print('skipped', k)
    if not done and not a.compact:
        print('nothing to pack'); return
    print(f'atlas {atlas.width}x{atlas.height}')
    if a.dry: return
    b = io.BytesIO(); atlas.save(b, 'PNG', optimize=True)
    s = s[:ai] + base64.b64encode(b.getvalue()).decode() + s[aj:]
    p0, p1 = find_P(s)
    s = s[:p0] + json.dumps(P, separators=(',', ':')) + s[p1:]
    open(a.out or a.game, 'w').write(s)
    print('wrote', a.out or a.game)


if __name__ == '__main__':
    main()
