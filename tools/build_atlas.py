"""Pack Forge kits marked ready into the game's embedded atlases: props, trooper frames and leg pieces.

  python tools/build_atlas.py <game.html> [--kits art/forge] [--out game.html] [--only W04,C01] [--dry]

<game.html> is the game source (the Grimspire artifact, or index.html). For every kit in art/forge whose
manifest says ready and whose code has a slot in the game (forge_common.SLOTS), the sprite's first frame
(body with trim, at the atlas's own scale) and its emissive layer are added to the props atlas, and the
slot's rects and points are pointed at them. Untouched sprites stay exactly where they are.

Re-running is safe: a slot already packed from the same kit version is skipped. Packing a newer version
adds it again (the old pixels stay in the atlas, unused); run with --compact to rebuild the atlas from the
rects still in use when that waste matters.

Trooper sprites (T01-T05, T08 torso) replace their frames in the trooper sheet in place. The thigh (A03)
and shin (A04) rebuild the legs sheet and the RIG numbers: each piece is centred on its joint point (Hip for the
thigh, Knee for the shin), the thigh's Knee sets where the shin hangs, and the torso's Hip sets where the legs
attach. Frame 1 of a leg piece is the near leg, frame 2 the far leg.

Render only: nothing in the sim changes, so no GV bump is needed. Check the result in the Proving ground.
"""
import argparse, base64, io, json, os, re, sys
from PIL import Image
from forge_common import LEGS, POINTS, SLOTS, TROOP, TROOP_OFF, TROOP_SCALE

ATLAS = "b.onload=()=>{SPR.props=b;done()};b.src='data:image/png;base64,"
TATLAS = "a.onload=()=>{SPR.atlas=a;done()};a.src='data:image/png;base64,"
LATLAS = "l.onload=()=>{SPR.legs=l;done()};l.src='data:image/png;base64,"


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


def load_atlas(s, which=ATLAS):
    i = s.index(which) + len(which)
    j = s.index("'", i)
    return i, j, Image.open(io.BytesIO(base64.b64decode(s[i:j]))).convert('RGBA')


def put_atlas(s, which, im):
    i = s.index(which) + len(which); j = s.index("'", i)
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return s[:i] + base64.b64encode(b.getvalue()).decode() + s[j:]


def find_obj(s, start):
    """(start, end) of the {...} object literal that begins at or after `start`."""
    p = s.index('{', start); d = 0
    for k in range(p, len(s)):
        if s[k] == '{': d += 1
        elif s[k] == '}':
            d -= 1
            if d == 0: return p, k + 1


def kit_frames(kdir, man, label):
    p = os.path.join(kdir, 'native', f"{man['id']}_{label}.png")
    w, h = man['native_frame']
    if not os.path.exists(p): return [None] * man['frames']
    sh = Image.open(p).convert('RGBA')
    return [sh.crop((i * w, 0, i * w + w, h)) for i in range(man['frames'])]


def pack_trooper(s, kits, M):
    """Replace trooper-sheet frames in place. kits: [(kdir, man)]."""
    i = s.index('const SPR={ready:false,')
    meta = json.loads(s[slice(*find_obj(s, s.index('M:', i)))])
    T = json.loads(s[slice(*find_obj(s, s.index('T:', i)))])
    fw, fh = meta['frame']
    ai, aj, A = load_atlas(s, TATLAS)
    out = []
    for kdir, man in kits:
        row, n = TROOP[man['code']]
        if row not in T:
            out.append(f"skipped {man['id']} (no {row} row in the trooper sheet)"); continue
        c0, cnt = T[row]
        layers = [kit_frames(kdir, man, l) for l in ('body', 'trim', 'emissive')]
        for f in range(min(cnt, man['frames'])):
            x0 = (c0 + f) * fw
            for r, fr in enumerate(layers):
                frame = Image.new('RGBA', (fw, fh))
                if fr[f] is not None:
                    big = fr[f].resize((fr[f].width * TROOP_SCALE, fr[f].height * TROOP_SCALE), Image.NEAREST)
                    frame.paste(big, TROOP_OFF)
                A.paste(frame, (x0, r * fh))
        if man['frames'] != cnt:
            out.append(f"note {man['id']}: {man['frames']} frames, the sheet has {cnt}; packed {min(cnt, man['frames'])}")
        out.append(f"packed {man['id']} -> trooper {row}")
        if man['code'] == 'T08' and (man.get('points_native') or {}).get('hip'):
            M['hip'] = man['points_native']['hip']
    return put_atlas(s, TATLAS, A), out


def centred(im, jx, jy):
    """Crop rows above the joint and pad sideways so the joint pixel is the horizontal centre."""
    w, h = im.size
    half = max(jx, w - 1 - jx)
    c = Image.new('RGBA', (2 * half + 1, h - jy))
    c.paste(im.crop((0, jy, w, h)), (half - jx, 0))
    return c


def pack_legs(s, kits, M):
    i = s.index('const RIG=')
    r0, r1 = find_obj(s, i)
    R = json.loads(s[r0:r1])
    res = R['res']
    pieces = {}
    for kdir, man in kits:
        part = LEGS[man['code']]
        pts = man.get('points_native') or {}
        j = pts.get('hip' if part == 'thigh' else 'knee')
        if not j:
            return s, [f"skipped {man['id']} (needs a {'Hip' if part == 'thigh' else 'Knee'} point)"]
        fr = [f for f in kit_frames(kdir, man, 'body') if f is not None]
        if not fr: return s, [f"skipped {man['id']} (empty)"]
        near = fr[0]; far = fr[1] if len(fr) > 1 else fr[0]
        pieces[part] = (centred(near, *j), centred(far, *j), pts, j)
    out = []
    # keep whatever isn't being replaced from the current sheet
    _, _, Lold = load_atlas(s, LATLAS)
    def old(part, farcol):
        x = int(R['farX'] * res) if farcol else 0
        if part == 'thigh': box = (x, 0, x + int(R['thW'] * res), int(R['thH'] * res))
        else: box = (x, int(R['shY'] * res), x + int(R['shW'] * res), int((R['shY'] + R['shH']) * res))
        return Lold.crop(box)
    k6 = 6  # legs-sheet px per art px
    imgs = {}
    for part in ('thigh', 'shin'):
        if part in pieces:
            n, f, pts, j = pieces[part]
            imgs[part] = [n.resize((n.width * k6, n.height * k6), Image.NEAREST), f.resize((f.width * k6, f.height * k6), Image.NEAREST)]
            if part == 'thigh':
                R['thW'], R['thH'] = n.width * k6 / res, n.height * k6 / res
                if pts.get('knee'): R['ov'] = R['thH'] - (pts['knee'][1] - j[1]) * k6 / res
            else:
                R['shW'], R['shH'] = n.width * k6 / res, n.height * k6 / res
            out.append(f"packed {part} (near and far)")
        else:
            imgs[part] = [old(part, False), old(part, True)]
    R['shY'] = R['thH'] + 2
    col = int(max(R['thW'], R['shW']) * res) + 4
    R['farX'] = col / res
    L = Image.new('RGBA', (col * 2, int((R['shY'] + R['shH']) * res)))
    for c in (0, 1):
        L.paste(imgs['thigh'][c], (c * col, 0))
        L.paste(imgs['shin'][c], (c * col, int(R['shY'] * res)))
    if M.get('hip'):
        hx, hy = M['hip']
        R['hip'] = [3 * hx + TROOP_OFF[0] + 1.5, 3 * hy + TROOP_OFF[1] + 1.5]
        out.append(f"legs attach at torso hip {M['hip']}")
    s = put_atlas(s, LATLAS, L)
    r0, r1 = find_obj(s, s.index('const RIG='))
    s = s[:r0] + json.dumps(R) + s[r1:]
    return s, out


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
    done, skipped, troop, legs = [], [], [], []
    for kd in sorted(os.listdir(a.kits)) if os.path.isdir(a.kits) else []:
        mp = os.path.join(a.kits, kd, 'manifest.json')
        if not os.path.exists(mp): continue
        man = json.load(open(mp))
        code = man.get('code')
        if not man.get('ready') or (only and code not in only): continue
        if code in TROOP: troop.append((os.path.join(a.kits, kd), man)); continue
        if code in LEGS: legs.append((os.path.join(a.kits, kd), man)); continue
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
    M, extra = {}, []
    if troop:
        s, o = pack_trooper(s, troop, M); extra += o
    if legs or M.get('hip'):
        s, o = pack_legs(s, legs, M); extra += o
    if a.compact:
        atlas = compact(P, atlas)
    for d in done: print('packed', d)
    for k in skipped: print('skipped', k)
    for k in extra: print(k)
    if not done and not a.compact and not extra:
        print('nothing to pack'); return
    if a.dry: return
    if not done and not a.compact:
        open(a.out or a.game, 'w').write(s); print('wrote', a.out or a.game); return
    print(f'atlas {atlas.width}x{atlas.height}')
    if a.dry: return
    s = put_atlas(s, ATLAS, atlas)
    p0, p1 = find_P(s)
    s = s[:p0] + json.dumps(P, separators=(',', ':')) + s[p1:]
    open(a.out or a.game, 'w').write(s)
    print('wrote', a.out or a.game)


if __name__ == '__main__':
    main()
