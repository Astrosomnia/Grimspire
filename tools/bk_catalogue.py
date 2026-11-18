#!/usr/bin/env python3
"""The building parts catalogue: every BK part that is drawn (parts.json) or briefed (BUILDING-PARTS-CONTRACT.md from
section 8 on; the early BK13-BK33 ids were superseded), with its category, brief, and whether the lab's generator places it.
Writes art/experiments/bay-kit/catalogue.json, which the Building parts library reads. bk_import.py runs it."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.join(ROOT, 'art', 'experiments', 'bay-kit')
CATS = [  # (name, codes)
    ('Walls and piers', [1, 2, 3, 4, 5, 60, 61, 62, 66, 69, 74]),
    ('Floors and arches', [6, 7, 8, 75, 127]),
    ('Back walls', [9, 10, 11, 70, 71, 72, 76, 77, 78]),
    ('Base', [12]),
    ('Stairs and ladders', [40, 41, 42, 43, 44, 45, 47, 117]),
    ('Roofs and crowns', [50, 51, 52, 53, 54, 55, 110, 111, 120, 122, 123, 125]),
    ('Outer wall shapes', [63, 64, 65, 90, 91, 92, 93, 94, 95, 96, 97, 98]),
    ('Bridges and aqueducts', [80, 81, 83, 84, 85, 86, 87, 88, 89, 118, 119, 126, 130]),
    ('Ruin and rubble', [73, 100, 101, 102, 103, 104, 105, 106, 107, 108]),
    ('Ornament', [112, 113, 114, 115, 116]),
    ('Cover and props', [140, 141, 142, 143]),
]
def cat_of(n):
    for name, codes in CATS:
        if n in codes: return name
    return 'Other'

def main():
    parts = json.load(open(os.path.join(KIT, 'parts.json')))['parts']
    lab = open(os.path.join(ROOT, 'experiments', 'building-lab.html')).read()
    used = set(re.findall(r"'(BK\d+)'", re.search(r"const used=\[(.*?)\];", lab).group(1)))
    brief, section = {}, 0
    for line in open(os.path.join(ROOT, 'docs', 'BUILDING-PARTS-CONTRACT.md')):
        m = re.match(r'##\s+(\d+)\.', line)
        if m: section = int(m.group(1))
        m = re.match(r'\|\s*(BK\d+)\b([^|]*)\|([^|]*)\|([^|]*)\|(.*)\|\s*$', line)
        if m and section >= 8:
            code = m.group(1); rest = m.group(2).strip()
            name, size, spec = (m.group(3).strip(), m.group(4).strip(), m.group(5).strip())
            if rest: name = rest.lstrip('·').strip() + ' · ' + name if not name else name
            brief[code] = {'name': name, 'size': size, 'spec': spec, 'section': section}
    out = {}
    for code in sorted(set(parts) | set(brief), key=lambda c: int(c[2:])):
        n = int(code[2:]); p = parts.get(code); b = brief.get(code, {})
        out[code] = {'cat': cat_of(n), 'name': b.get('name') or (p or {}).get('name') or code, 'brief': b or None,
                     'placed': code in used, 'drawn': bool(p), 'variants': sorted((p or {}).get('variants', {}).keys())}
    json.dump({'cats': [c for c, _ in CATS] + ['Other'], 'parts': out}, open(os.path.join(KIT, 'catalogue.json'), 'w'), indent=1)
    print(f"catalogue: {len(out)} parts, {sum(1 for v in out.values() if v['drawn'])} drawn, {sum(1 for v in out.values() if not v['drawn'])} awaiting art")

if __name__ == '__main__': main()
