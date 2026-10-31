"""Deterministic release builder. No network, Git mutations, or browser dependencies."""
import base64, hashlib, json, math, re, struct
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SLOTS={'W01','W02','W03','W04','W05','W06','W07','W08'}
DEFAULTS={'darkness':.66,'emissive':1.0,'bloom':0.0,'scale':1.0,'glowColor':'#59edff'}

def settings(raw):
    result={**DEFAULTS,**raw}
    if set(result)!=set(DEFAULTS):raise ValueError('Unknown lighting setting')
    for k,lo,hi in [('darkness',0,1),('emissive',0,2),('bloom',0,30),('scale',.05,4)]:
        n=result[k]
        if isinstance(n,bool) or not isinstance(n,(float,int)) or not math.isfinite(n) or not lo<=n<=hi:raise ValueError('Invalid '+k)
    if not re.fullmatch(r'#[0-9a-fA-F]{6}',result['glowColor']):raise ValueError('Invalid glow colour')
    return result

def sprite(d):
    if d.get('forge')!=1:raise ValueError('Expected Forge document')
    w,h=d.get('w'),d.get('h')
    if not all(type(n) is int and 0<n<=1024 for n in [w,h]):raise ValueError('Invalid sprite dimensions')
    if not isinstance(d.get('frames'),list) or not 1<=len(d['frames'])<=64:raise ValueError('Expected 1–64 frames')
    if not isinstance(d.get('markers'),dict):raise ValueError('Missing attachment points')
    for p in d['markers'].values():
        if p is not None and (not isinstance(p,list) or len(p)!=2 or not all(type(n) in (int,float) and math.isfinite(n) for n in p) or not 0<=p[0]<w or not 0<=p[1]<h):raise ValueError('Attachment outside canvas')
    if not (d['markers'].get('grip') or d['markers'].get('pivot')):raise ValueError('Set a grip or pivot before game testing')
    if type(d.get('fps',8)) not in (int,float) or not 1<=d.get('fps',8)<=60:raise ValueError('FPS must be 1–60')
    for f in d['frames']:
        if not isinstance(f,dict):raise ValueError('Invalid frame')
        for key in ['body','emis','trim','guts']:
            src=f.get(key)
            if not src:continue
            if not isinstance(src,str) or not src.startswith('data:image/png;base64,'):raise ValueError('Only embedded PNG layers are supported')
            data=base64.b64decode(src.split(',',1)[1],validate=True)
            if data[:8]!=b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',data[16:24])!=(w,h):raise ValueError('PNG dimensions differ from canvas')
    return d

def digest(raw):return hashlib.sha256(raw).hexdigest()
def encode(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()

def clean_source(source):
    start='// BEGIN GRIMSPIRE_ART_ADAPTER\n'
    end='// END GRIMSPIRE_ART_ADAPTER\n'
    if start not in source:return source
    if source.count(start)!=1 or source.count(end)!=1:raise ValueError('Ambiguous existing art adapter')
    a=source.index(start);b=source.index(end,a)+len(end)
    return source[:a]+source[b:]

def build(payload,source=None,runtime=None):
    source=clean_source(source if source is not None else (ROOT/'game.html').read_text())
    runtime=runtime if runtime is not None else (ROOT/'runtime.js').read_text()
    if not payload['assets']:raise ValueError('Save a weapon first')
    for slot,d in payload['assets'].items():
        if slot not in SLOTS:raise ValueError('Unknown preview slot')
        sprite(d)
    payload={**payload,'settings':settings(payload['settings'])}
    # Insertion is deliberately strict: a changed game architecture needs a review.
    needle='requestAnimationFrame(frame);\nif(document.fonts'
    if source.count(needle)!=1 or 'const LAB_PAYLOAD=' in source:raise ValueError('Game hook changed; refresh adapter and retest')
    packed=encode(payload).decode().replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    if '</script' in runtime.lower():raise ValueError('Runtime must be JavaScript only')
    hook='// BEGIN GRIMSPIRE_ART_ADAPTER\nconst LAB_PAYLOAD='+packed+';\n'+runtime+'\n// END GRIMSPIRE_ART_ADAPTER\n'
    return source.replace(needle,hook+needle).encode()
