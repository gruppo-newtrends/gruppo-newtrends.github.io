# -*- coding: utf-8 -*-
"""New Trends: copie WebP locali delle foto esterne (onoffice e team su new-trends.ch), stesse immagini ma 5-20 volte più leggere.
Uso: python3 -I strumenti/nt_foto_esterne.py <cartella-download>  (nella cartella: file chiamati con sha1(url)[:12]).
Le pagine puntano poi a assets/img/ext/<hash>-<w>.webp con srcset; l'URL originale resta in data-fallback."""
import glob, hashlib, os, re, sys
from PIL import Image
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "newtrends"); OUTD = os.path.join(ROOT, "assets", "img", "ext"); os.makedirs(OUTD, exist_ok=True)
DL = sys.argv[1]; Image.MAX_IMAGE_PIXELS = 60_000_000
done = {}
def conv(url):
    h = hashlib.sha1(url.encode()).hexdigest()[:12]
    if h in done: return done[h]
    src = os.path.join(DL, h); ws = []
    if not os.path.exists(src): done[h] = None; return None
    im = Image.open(src); im = im.convert("RGB"); r = im.height / im.width
    for w in (480, 960, 1600):
        if w > im.width and ws: break
        w = min(w, im.width); out = os.path.join(OUTD, f"{h}-{w}.webp")
        if not os.path.exists(out): (im if w == im.width else im.resize((w, round(w * r)), Image.LANCZOS)).save(out, "WEBP", quality=72, method=5)
        ws.append(w)
    done[h] = (h, ws); return done[h]
TAG = re.compile(r'<img src="(https://(?:image\.onoffice\.de|www\.new-trends\.ch/images)/[^"]+)"([^>]*)>')
def fix(m, pre):
    url, rest = m.groups(); c = conv(url)
    if not c or "srcset" in rest: return m.group(0)
    h, ws = c; big = 'width="1600"' in rest or "team" in url
    sizes = "100vw" if big else "(max-width:700px) 92vw, 420px"
    ss = ", ".join(f"{pre}assets/img/ext/{h}-{w}.webp {w}w" for w in ws)
    fb = "" if "data-fallback" in rest else f' data-fallback="{url}"'
    return f'<img src="{pre}assets/img/ext/{h}-{ws[min(1, len(ws) - 1)]}.webp" srcset="{ss}" sizes="{sizes}"{fb}{rest}>'
n = 0
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    pre = "../" * (os.path.relpath(f, ROOT).count(os.sep))
    s = open(f, encoding="utf-8").read(); t = TAG.sub(lambda m: fix(m, pre), s)
    if t != s: open(f, "w", encoding="utf-8").write(t); n += 1
print("pagine", n, "foto", sum(1 for v in done.values() if v), "mancanti", [k for k, v in done.items() if not v])
