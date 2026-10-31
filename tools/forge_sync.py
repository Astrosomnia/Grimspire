"""Write Grimspire Forge sprites into the repo as kits.

  python tools/forge_sync.py <docs-dir-or-files...> [--out art/forge] [--prune]

Inputs are Forge sprite docs: the JSON files ArtifactData writes for the Forge's `sprites` collection
(read with out_dir), or .forge.json files saved from the Forge. Each sprite becomes art/forge/<CODE_name>/:

  <base>.forge.json        the source doc, re-importable into the Forge (drop it on the plate)
  <base>_body.png etc.     x12 sheets, frames left to right (body, emissive, trim, guts when present)
  native/<base>_*.png      the same sheets at 1 art px
  <base>_aseprite.json     Aseprite sprite-sheet JSON for native/<base>_body.png, points as slices
  manifest.json            code, name, size, frames, fps, points (x12 and native), notes, ready

art/forge/index.json lists every sprite with its code, slot in the game and ready flag.
--prune removes kit folders whose sprite is no longer in the inputs.
"""
import argparse, json, os, shutil, sys
from forge_common import ART, LAYERS, SLOTS, base_name, code_of, frames, has_pixels, load_doc, sheet

MCOL = {'grip': '#ff3b3bff', 'muzzle': '#3dff8bff', 'pivot': '#ffd84aff', 'shoulder': '#3ff3ffff',
        'elbow': '#ff2e88ff', 'hand': '#ffb21eff', 'hip': '#a0ff46ff', 'knee': '#9fb4d8ff'}


def write_kit(doc, out):
    code, name = code_of(doc)
    base = base_name(doc)
    d = os.path.join(out, base)
    os.makedirs(os.path.join(d, 'native'), exist_ok=True)
    w, h, n = doc['w'], doc['h'], len(doc['frames'])
    files = {}
    for key, label in LAYERS:
        ims = frames(doc, key)
        if key != 'body' and not has_pixels(ims):
            continue
        sheet(ims).save(os.path.join(d, 'native', f'{base}_{label}.png'))
        sheet(ims, ART).save(os.path.join(d, f'{base}_{label}.png'))
        files[label] = f'{base}_{label}.png'
    pts = {k: v for k, v in (doc.get('markers') or {}).items() if v}
    dur = round(1000 / (doc.get('fps') or 8))
    ase = {'frames': [{'filename': f'{base} {i}', 'frame': {'x': i * w, 'y': 0, 'w': w, 'h': h}, 'rotated': False,
                       'trimmed': False, 'spriteSourceSize': {'x': 0, 'y': 0, 'w': w, 'h': h},
                       'sourceSize': {'w': w, 'h': h}, 'duration': dur} for i in range(n)],
           'meta': {'app': 'Grimspire Forge', 'version': '1', 'image': f'native/{base}_body.png', 'format': 'RGBA8888',
                    'size': {'w': w * n, 'h': h}, 'scale': '1',
                    'frameTags': [{'name': base, 'from': 0, 'to': n - 1, 'direction': 'forward'}],
                    'layers': [{'name': l, 'opacity': 255, 'blendMode': 'normal'} for l in files],
                    'slices': [{'name': k, 'color': MCOL.get(k, '#ffffffff'),
                                'keys': [{'frame': 0, 'bounds': {'x': p[0], 'y': p[1], 'w': 1, 'h': 1}}]} for k, p in pts.items()]}}
    json.dump(ase, open(os.path.join(d, f'{base}_aseprite.json'), 'w'), indent=1)
    man = {'code': code, 'name': name, 'id': base, 'source': 'Grimspire Forge', 'pixel_scale': ART,
           'native_frame': [w, h], 'frame_px': [w * ART, h * ART], 'frames': n, 'fps': doc.get('fps') or 8,
           'units': 'points in x12 PNG pixels, top-left origin; points_native in art px',
           'files': files, 'native_dir': 'native/',
           'points': {k: [p[0] * ART, p[1] * ART] for k, p in pts.items()}, 'points_native': pts,
           'feet_row_native': doc.get('base'), 'slot': SLOTS.get(code), 'ready': bool(doc.get('ready')),
           'notes': doc.get('notes') or '', 'frame_notes': [f.get('note') or '' for f in doc['frames']],
           'updated': doc.get('updated')}
    json.dump(man, open(os.path.join(d, 'manifest.json'), 'w'), indent=2)
    src = {k: v for k, v in doc.items() if k not in ('review',)}
    json.dump(src, open(os.path.join(d, f'{base}.forge.json'), 'w'))
    return base, man


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('inputs', nargs='+')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(__file__), '..', 'art', 'forge'))
    ap.add_argument('--prune', action='store_true')
    a = ap.parse_args()
    paths = []
    for p in a.inputs:
        if os.path.isdir(p):
            for root, _, fs in os.walk(p):
                paths += [os.path.join(root, f) for f in fs if f.endswith('.json')]
        else:
            paths.append(p)
    os.makedirs(a.out, exist_ok=True)
    index, seen = [], set()
    for p in sorted(paths):
        try:
            doc = load_doc(p)
        except Exception as e:
            print('skip', e, file=sys.stderr)
            continue
        base, man = write_kit(doc, a.out)
        if base in seen:
            print(f'warning: two sprites share the name {base}; the later one won', file=sys.stderr)
        seen.add(base)
        index.append({'id': base, 'code': man['code'], 'name': man['name'], 'slot': man['slot'], 'ready': man['ready'],
                      'frames': man['frames'], 'size': man['native_frame']})
    if a.prune:
        for d in os.listdir(a.out):
            if os.path.isdir(os.path.join(a.out, d)) and d not in seen:
                shutil.rmtree(os.path.join(a.out, d))
                print('pruned', d)
    # the index covers every kit in the folder, not just this run's inputs
    index = []
    for d in sorted(os.listdir(a.out)):
        mp = os.path.join(a.out, d, 'manifest.json')
        if os.path.exists(mp):
            m = json.load(open(mp))
            index.append({'id': m['id'], 'code': m['code'], 'name': m['name'], 'slot': m['slot'], 'ready': m['ready'],
                          'frames': m['frames'], 'size': m['native_frame']})
    json.dump(index, open(os.path.join(a.out, 'index.json'), 'w'), indent=1)
    ready = [x['id'] for x in index if x['ready']]
    print(f'{len(index)} sprites written to {a.out}; ready for the game: {", ".join(ready) or "none"}')


if __name__ == '__main__':
    main()
