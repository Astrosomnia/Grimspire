#!/usr/bin/env python3
"""Pull every building-kit part (BK##) from the Forge Library into the building lab.

    python3 tools/bk_import.py            # reads origin/art/weapon-lab (git fetch it first)
    python3 tools/bk_import.py --ref <git ref>

Scans art/lab/hosted/library.json on the art branch for entries whose code is BK + digits. Variants are versions
inside an asset, named "... — a", "— b" ("— a+" is slot a's adorned version: same shape, more ornament); the newest entry for each code + letter wins, so a fixed variant replaces
the old one and a new letter adds a variant. Writes each layer as a PNG to art/experiments/bay-kit/ and a manifest,
parts.json, that the lab reads. Safe to rerun whenever new parts land: it rewrites the folder from the Library.
"""
import argparse, base64, hashlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art_check import check_doc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'art', 'experiments', 'bay-kit')
LAYERS = ('body', 'height', 'back', 'guts', 'emis', 'cloth', 'trim')


def git_show(ref, path):
    return subprocess.run(['git', '-C', ROOT, 'show', f'{ref}:{path}'], check=True, capture_output=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', default='origin/art/weapon-lab')
    a = ap.parse_args()
    lib = json.loads(git_show(a.ref, 'art/lab/hosted/library.json'))
    commit = subprocess.run(['git', '-C', ROOT, 'rev-parse', a.ref], capture_output=True, text=True).stdout.strip()
    pick = {}  # (code, letter) -> entry; later entries win
    for e in lib['entries']:
        code = str(e.get('code') or '')
        if not re.fullmatch(r'BK\d{2,3}', code):
            continue
        m = re.search(r'[—-]\s*([a-z]\+?)\s*$', str(e.get('name') or ''))
        pick[(code, m.group(1) if m else 'a')] = e
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith('.png') or f == 'parts.json':
            os.remove(os.path.join(OUT, f))
    parts = {}
    for (code, letter), e in sorted(pick.items()):
        doc = json.loads(git_show(a.ref, e['path']))
        fr = (doc.get('frames') or [{}])[0]
        vid = f'{code}{letter[0]}' + ('_ad' if letter.endswith('+') else '')
        layers = {}
        for ly in LAYERS:
            v = fr.get(ly)
            if not v or not str(v).startswith('data:image/png;base64,'):
                continue
            raw = base64.b64decode(v.split(',', 1)[1])
            if ly == 'body' and len(raw) < 200 and fr.get('back'):
                pass  # an empty Body on a Back-only part is still written; the lab ignores it
            fn = f'{vid}_{ly}.png'
            open(os.path.join(OUT, fn), 'wb').write(raw)
            layers[ly] = fn
        p = parts.setdefault(code, {'name': re.sub(r'\s*[—-]\s*[a-z]\+?\s*$', '', doc.get('name', code)), 'w': doc.get('w'), 'h': doc.get('h'), 'variants': {}})
        p['variants'][letter] = {'layers': layers, 'version': e['id'], 'w': doc.get('w'), 'h': doc.get('h'),
                                 'pivot': (doc.get('markers') or {}).get('pivot'), 'ready': bool(doc.get('ready')), 'check': check_doc(doc)}
    man = {'source': a.ref, 'commit': commit, 'count': sum(len(p['variants']) for p in parts.values()), 'parts': parts}
    json.dump(man, open(os.path.join(OUT, 'parts.json'), 'w'), indent=1)
    print(f"{man['count']} variants in {len(parts)} parts from {a.ref} {commit[:7]} -> {os.path.relpath(OUT, ROOT)}")
    for code, p in parts.items():
        print(f"  {code} {p['name']}: " + ' '.join(f"{v}:{(e['check'] or {}).get('verdict','-')}" for v, e in sorted(p['variants'].items())))
        for v, e in sorted(p['variants'].items()):
            c = e['check'] or {}
            if c.get('verdict') != 'pass':
                print(f"      {code}{v} {c.get('verdict')}: colours {c.get('colours')} near {c.get('near')} lone {c.get('lone')} detail {c.get('detail')} · {'; '.join(c.get('notes', []))}")


if __name__ == '__main__':
    main()
    import bk_masks; bk_masks.main()  # collision from art for the parts that take it
    import bk_catalogue; bk_catalogue.main()  # the parts library's catalogue
