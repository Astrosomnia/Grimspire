#!/usr/bin/env python3
"""Validate committed art release hashes and Forge attachment metadata. No writes."""
import base64,hashlib,json,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def validate():
    count=0
    catalog=json.loads((ROOT/'catalog.json').read_text())
    assert len({r['id'] for r in catalog['releases']})==len(catalog['releases'])
    assert catalog['current_review'] in {r['id'] for r in catalog['releases']}
    for release in catalog['releases']:
        path=(ROOT/release['manifest']).resolve()
        assert ROOT in path.parents, 'Manifest path escapes Lab'
        m=json.loads(path.read_text()); assert m['release']==release['id']
        codes=set()
        for asset in m['assets']:
            code=asset['code'];assert code not in codes;codes.add(code)
            for variant,info in asset['variants'].items():
                p=(path.parent/info['path']).resolve();assert path.parent==p.parent
                raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==info['sha256'],str(p)+' hash mismatch'
                d=json.loads(raw);assert d['forge']==1 and d['code']==code
                w,h=d['w'],d['h'];assert [w,h]==info['native_size'] and 0<w<=1024 and 0<h<=1024
                for point in d['markers'].values():
                    if point is not None: assert len(point)==2 and 0<=point[0]<w and 0<=point[1]<h
                for frame in d['frames']:
                    for layer in ['body','emis','trim','guts']:
                        if not frame.get(layer):continue
                        png=base64.b64decode(frame[layer].split(',',1)[1],validate=True)
                        assert png[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',png[16:24])==(w,h)
                if info['status']=='approved': assert all(info['checks'].values()), 'Approved variant has unresolved checks'
                count+=1
    print(f'Validated {count} Forge variants: hashes, dimensions, PNGs, mappings, anchors and approval checks.')

if __name__=='__main__':
    try:validate()
    except (AssertionError,KeyError,ValueError,OSError) as e:sys.exit(f'Art validation failed: {e}')
