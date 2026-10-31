"""Shared bits for the Forge pipeline: reading Forge sprite docs and the game's slot map.

A Forge doc is what the Grimspire Forge saves to its library (and what "Save .json" writes):
  {forge:1, code, name, w, h, fps, base, pixel_scale:12, ready, markers:{grip:[x,y]|null, ...},
   notes, frames:[{body, emis, trim, guts, note}]}
Layers are PNG data URLs at 1 art px (null when empty). Points are in art px, top-left origin.
"""
import base64, io, json, re
from PIL import Image

ART = 12  # source px per art px

# Forge code -> sprite key in the game's props atlas (same table as FORGE_KEYS in the game)
SLOTS = {
    'W01': 'mortar', 'W02': 'rail', 'W03': 'scatter', 'W04': 'bolter', 'W05': 'las', 'W06': 'flamer',
    'W07': 'chain', 'W08': 'fist', 'W09': 'lance', 'W10': 'rope', 'W11': 'cutter', 'W12': 'frag',
    'W13': 'sun', 'W14': 'mine', 'W15': 'nuke', 'W16': 'fab', 'W18': 'minigun', 'W19': 'sentry',
    'W20': 'drone', 'W21': 'teleport', 'P01': 'shell', 'C01': 'crate', 'C02': 'chute', 'C03': 'ship',
    'C04': 'tank', 'M01': 'martyr',
}
# Forge point -> atlas field, per slot (weapons default to grip->g, muzzle->m when the slot has them)
POINTS = {
    'chute': {'pivot': 'a'},
    'ship': {'pivot': 'hatch', 'muzzle': 'exh'},
    'sentry': {'pivot': 'p', 'muzzle': 'l'},
}
LAYERS = [('body', 'body'), ('emis', 'emissive'), ('trim', 'trim'), ('guts', 'guts')]

# Trooper sheet: Forge code -> (row of frames in SPR.T, frame count). Rows: 0 body, 1 trim, 2 emissive.
# The game draws only the torso (T08) now; the others are kept in step so the sheet matches the Forge.
TROOP = {'T01': ('walk', 4), 'T02': ('idle', 3), 'T03': ('jump', 3), 'T04': ('knocked', 3), 'T05': ('swim', 2), 'T08': ('torso', 1)}
# A Forge trooper art pixel (fx, fy) covers trooper-sheet pixels (3fx-11, 3fy-9) to +3 inside its frame
TROOP_SCALE, TROOP_OFF = 3, (-11, -9)
# Leg pieces in the legs sheet, swung in code from RIG. Frame 1 near leg, frame 2 far leg.
LEGS = {'A03': 'thigh', 'A04': 'shin'}


def slug(s):
    return re.sub(r'[^a-z0-9]+', '_', (s or 'sprite').lower()).strip('_') or 'sprite'


def code_of(doc):
    code = (doc.get('code') or '').upper()
    name = doc.get('name') or ''
    m = re.match(r'^([A-Za-z]\d{2})[\s_-]+(.+)$', name)
    if not re.fullmatch(r'[A-Z]\d{2}', code) and m:
        code, name = m.group(1).upper(), m.group(2)
    elif m and m.group(1).upper() == code:
        name = m.group(2)
    return (code if re.fullmatch(r'[A-Z]\d{2}', code) else ''), name


def base_name(doc):
    code, name = code_of(doc)
    return (code + '_' if code else '') + slug(name)


def img(url, w, h):
    """A data URL (or None) as an RGBA image of the doc's size."""
    if not url:
        return Image.new('RGBA', (w, h))
    im = Image.open(io.BytesIO(base64.b64decode(url.split(',', 1)[1]))).convert('RGBA')
    if im.size != (w, h):
        c = Image.new('RGBA', (w, h)); c.paste(im, (0, 0)); im = c
    return im


def load_doc(path):
    d = json.load(open(path))
    # ArtifactData out_dir files may wrap the doc; Forge's own .json is the doc itself
    if 'forge' not in d and isinstance(d.get('data'), dict):
        d = d['data']
    if not d.get('forge') or not isinstance(d.get('frames'), list):
        raise ValueError(f'{path}: not a Forge sprite')
    return d


def frames(doc, key):
    w, h = doc['w'], doc['h']
    return [img(f.get(key), w, h) for f in doc['frames']]


def sheet(ims, scale=1):
    w, h = ims[0].size
    s = Image.new('RGBA', (w * len(ims), h))
    for i, im in enumerate(ims):
        s.paste(im, (i * w, 0))
    return s.resize((s.width * scale, s.height * scale), Image.NEAREST) if scale != 1 else s


def has_pixels(ims):
    return any(im.getbbox() for im in ims)
