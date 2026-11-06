# -*- coding: utf-8 -*-
"""Velocità del sito New Trends (newtrends/) senza cambiare i contenuti: idempotente, si può rilanciare.
- crea versioni WebP delle foto locali (assets/img/<nome>-<w>.webp)
- miniature del menu Zone (96x64) -> WebP 192 px invece del JPEG da 1400 px
- foto grandi -> srcset WebP + sizes (i JPEG restano nella cartella)
- toglie backdrop-filter (sfocatura costosa durante lo scorrimento) con sfondo un po' più pieno
Uso: python3 strumenti/nt_perf.py"""
import glob, os, re
from PIL import Image
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "newtrends")
IMG = os.path.join(ROOT, "assets", "img")
W = {}
for f in sorted(glob.glob(os.path.join(IMG, "*.jpg"))):
    n = os.path.splitext(os.path.basename(f))[0]; im = Image.open(f).convert("RGB"); W[n] = []
    for w in (192, 480, 960, 1400, 2400):
        if w > im.width: continue
        out = os.path.join(IMG, f"{n}-{w}.webp")
        if not os.path.exists(out): (im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)).save(out, "WEBP", quality=74, method=5)
        W[n].append(w)
TAG = re.compile(r'<img src="((?:\.\./)?)assets/img/([a-z]+)\.jpg"([^>]*)>')
def fix(m):
    pre, n, rest = m.groups()
    if "srcset" in rest or n not in W: return m.group(0)
    if 'width="96"' in rest: return f'<img src="{pre}assets/img/{n}-192.webp"{rest}>'
    ws = [w for w in W[n] if w >= 480]; sizes = "100vw" if n == "hero" else "(max-width:700px) 100vw, (max-width:1100px) 50vw, 33vw"
    ss = ", ".join(f"{pre}assets/img/{n}-{w}.webp {w}w" for w in ws)
    dec = "" if "decoding" in rest else ' decoding="async"'
    return f'<img src="{pre}assets/img/{n}-{ws[min(1, len(ws) - 1)]}.webp" srcset="{ss}" sizes="{sizes}"{rest}{dec}>'
ch = 0
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    s = open(f, encoding="utf-8").read(); t = TAG.sub(fix, s)
    if t != s: open(f, "w", encoding="utf-8").write(t); ch += 1
css = os.path.join(ROOT, "assets", "site.css"); s = open(css).read()
t = (s.replace("background:color-mix(in srgb,var(--paper) 92%,transparent);backdrop-filter:blur(10px)", "background:color-mix(in srgb,var(--paper) 97%,transparent)")
      .replace("background:color-mix(in srgb,var(--paper) 94%,transparent);color:var(--ink);border-color:var(--line);backdrop-filter:blur(10px)", "background:color-mix(in srgb,var(--paper) 98%,transparent);color:var(--ink);border-color:var(--line)")
      .replace("background:color-mix(in srgb,var(--paper) 96%,transparent);color:var(--ink);border-color:var(--line);backdrop-filter:blur(10px)", "background:var(--paper);color:var(--ink);border-color:var(--line)")
      .replace("background:#0000001f;backdrop-filter:blur(4px)", "background:#00000040"))
if t != s: open(css, "w").write(t)
print("pagine cambiate", ch, "css", t != s)
