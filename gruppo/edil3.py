# -*- coding: utf-8 -*-
"""Edil Trend, versione 6: sito a più pagine (ogni voce del menu ha la sua pagina), stile RenovateHub, logo vero.
Ogni servizio e ogni lavoro del gruppo ha una pagina dedicata; la villa three.js (src/villa3d.js) vive in
"Come lavoriamo" e si carica solo quando la sezione si avvicina. Immagini WebP in più larghezze (build2.rimg).
Identità: THEME = "a" (grafite + verde del logo, neutri caldi), "b" (pietra fredda), "c" (scuro).
Si cambia con la costante THEME o con la variabile EDIL_THEME. Niente recensioni, voti, garanzie o prezzi inventati.
Uso: python3 -E -s edil3.py [cartella]  (predefinita out/ediltrend-v6)."""
import hashlib, os, shutil, sys
from PIL import Image
import build2 as b2
from build2 import E, P, ADDR, PHONE, TEL, MAIL, WA, SITES, ICONS, find_src

THEME = os.environ.get("EDIL_THEME", "d")   # "d" = scelta della titolare (6 nov 2026)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "ediltrend-v6")
BASE = SITES["ediltrend"]          # indirizzo del sito: unico punto da cambiare con il dominio vero
YEARS = 2026 - 1999
LOGO_W, LOGO_H = 1600, 264         # proporzioni del logo vero (src/logo/ediltrend-logo-*.png)

# ---------- identità sullo stesso logo (grafite #333132 + verde #01A187, mai ricolorato) ----------
GF = "https://fonts.googleapis.com/css2?family={}&display=swap"
THEMES = {
    "a": dict(name="A · Grafite e verde, neutri caldi", font=GF.format("Outfit:wght@500;600&family=Inter:wght@400..700"), fh="Outfit", fb="Inter",
              v=dict(bg="#F3F0EA", paper="#FFFFFF", ink="#333132", onink="#FFFFFF", dark="#333132", ondark="#F4F1EC", dkmuted="#C4BEB5", soft="#DDEFE9",
                     acc="#01A187", onacc="#FFFFFF", accdk="#00785F", muted="#67625C", line="#E0DAD0", card2="#ECE7DF", photo="none"), hdr="#333132"),
    "b": dict(name="B · Pietra fredda, verde solo negli accenti", font=GF.format("Manrope:wght@400..700"), fh="Manrope", fb="Manrope",
              v=dict(bg="#ECECE8", paper="#FFFFFF", ink="#2C2B2C", onink="#FFFFFF", dark="#3A3D3D", ondark="#EEF0EE", dkmuted="#BCC1BE", soft="#D9DEDA",
                     acc="#01A187", onacc="#FFFFFF", accdk="#00785F", muted="#5F6361", line="#D6D8D3", card2="#E2E3DE", photo="saturate(.82) contrast(1.04)"), hdr="#2C2B2C"),
    "c": dict(name="C · Scuro grafite, verde pieno", font=GF.format("Space+Grotesk:wght@500;600&family=Inter:wght@400..700"), fh="Space Grotesk", fb="Inter",
              v=dict(bg="#262526", paper="#333132", ink="#F2EFEA", onink="#262526", dark="#1B1A1B", ondark="#F2EFEA", dkmuted="#B3ADA5", soft="#01A187",
                     acc="#01A187", onacc="#FFFFFF", accdk="#3CC9AD", muted="#B8B2AA", line="#444142", card2="#3C3A3B", photo="saturate(1.06) contrast(1.03)"), hdr="#1B1A1B"),
    # D = via di mezzo tra B e C scelta dalla titolare: pietra calda + grafite, un po' più del verde del logo (fasce verdi, icone, numeri, hover)
    "d": dict(name="D · Pietra calda e grafite, più verde del logo", font=GF.format("Space+Grotesk:wght@500;600&family=Manrope:wght@400..700"), fh="Space Grotesk", fb="Manrope",
              v=dict(bg="#E6E0D7", paper="#F8F5F0", ink="#2A2829", onink="#FFFFFF", dark="#333132", ondark="#F3F0EB", dkmuted="#D0CAC1", soft="#CDE9E0",
                     acc="#01A187", onacc="#0B2420", accdk="#006B55", muted="#55514C", line="#D2CBC0", card2="#DAD3C9", photo="none", band="#0B6E5E"), hdr="#333132",
              css=""".cta{background:var(--band);color:#fff}.cta .tag,.cta p{color:#E2F4EE}.cta .tag::before{background:#fff}.cta .btn{background:#fff;color:#1f1e1f}
.gb{background:var(--band)}.gb .tag,.gb .lead{color:#D8F0E8}.gb .tag::before{background:#A7EBDA}.gb .tl li{border-color:#ffffff33}.gb .tl li::before{color:#A7EBDA}.gb .btn:not(.w):not(.g){background:#fff;color:#1f1e1f}
.svc a:hover,.wk a:hover{box-shadow:0 0 0 2px var(--acc),0 30px 50px -34px #0006}.pill a.on{background:#01A18766}.wg>div:hover{box-shadow:0 0 0 2px var(--acc)}
.ftr{box-shadow:inset 0 4px 0 var(--acc)}.facts{background:var(--paper)}.kv div{border-top:3px solid var(--acc)}.chain .me a{color:#0B2420}"""),
}
TH = THEMES[THEME]
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         f'<link rel="stylesheet" href="{TH["font"]}">')
IMPORTMAP = ('<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin><script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",'
             '"three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>')
AR = '<i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></i>'
CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m7.5 12.5 3 3 6-6"/></svg>'
PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg>'

def root_vars():
    v = TH["v"]
    return (":root{" + "".join(f"--{k}:{x};" for k, x in v.items()) + f'--fh:"{TH["fh"]}",Arial,sans-serif;--fb:"{TH["fb"]}",Arial,sans-serif;--r:24px;'
            "--dk70:color-mix(in srgb,var(--dark) 72%,transparent);--dk85:color-mix(in srgb,var(--dark) 86%,transparent)}")

CSS = (b2.COMMON_CSS + """
html{scroll-behavior:smooth}html.lenis,html.lenis body{height:auto}.lenis.lenis-smooth{scroll-behavior:auto!important}html,body{overflow-x:clip}body{background:var(--bg);color:var(--ink);font:400 1rem/1.6 var(--fb);-webkit-font-smoothing:antialiased}
@media (prefers-reduced-motion:no-preference){@view-transition{navigation:auto}main{animation:pe .55s cubic-bezier(.2,.7,.2,1) both}@keyframes pe{from{opacity:0}}}
.wrap{max-width:1320px;margin:0 auto;padding:0 clamp(16px,4vw,60px)}
h1,h2,h3{font-family:var(--fh);font-weight:600;letter-spacing:-.03em;line-height:1.06;margin:0;text-wrap:balance}
h2{font-size:clamp(2rem,1.3rem + 2.4vw,3.2rem)}h3{letter-spacing:-.015em}
.tag{display:flex;align-items:center;gap:8px;font-weight:600;font-size:.88rem;color:var(--muted);margin-bottom:14px;letter-spacing:.01em}.tag::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--acc)}.dk .tag{color:var(--dkmuted)}
.lead{color:var(--muted);max-width:56ch;margin:0}.dk .lead{color:var(--dkmuted)}
.sec{padding:clamp(64px,8vw,110px) 0}.dk{background:var(--dark);color:var(--ondark);border-radius:var(--r);margin:0 8px}
.head{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:20px 60px;align-items:start;margin-bottom:46px}.head .lead{margin-top:8px}.head .r{display:grid;gap:26px;justify-items:start}
@media (max-width:860px){.head{grid-template-columns:1fr}}
img{filter:var(--photo)}.logo img{filter:none}
/* bottoni */
.btn{display:inline-flex;align-items:center;gap:12px;padding:5px 5px 5px 18px;border-radius:999px;background:var(--ink);color:var(--onink);font:600 1rem var(--fb);text-decoration:none;border:1px solid transparent;cursor:pointer;transition:transform .25s,background .25s}
.btn i{width:32px;height:32px;border-radius:50%;background:var(--acc);color:var(--onacc);display:grid;place-items:center;transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.btn i svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2}.btn:hover i{transform:rotate(-45deg)}.btn:active{transform:scale(.97)}
.btn.w{background:#fff;color:#2a2929}.btn.g{background:var(--acc);color:var(--onacc)}.btn.g i{background:#fff;color:#2a2929}
.btn.o{background:transparent;border-color:#ffffffb3;color:#fff;padding:9px 16px}.btn.o:hover{background:#ffffff1a}
.dk .btn:not(.w):not(.g){background:var(--ondark);color:var(--dark)}
/* header: trasparente sopra la foto, pieno quando scorri (niente sfocatura: costa durante lo scorrimento) */
.hdr{position:fixed;top:8px;left:8px;right:8px;z-index:60;border-radius:0 0 18px 18px;transition:background-color .3s,box-shadow .3s}
.hdr.s{background:HDRf2;box-shadow:0 10px 30px -18px #0008}
.hdr .wrap{display:flex;align-items:center;gap:20px;height:76px;max-width:none;padding:0 clamp(16px,2.6vw,38px)}
.logo{display:flex;align-items:center;text-decoration:none;flex:none}.logo img{height:28px;width:auto}
.pill{position:absolute;left:50%;transform:translateX(-50%);display:flex;gap:2px;padding:5px;border-radius:999px;background:#ffffff1f;border:1px solid #ffffff33}
.pill a{color:#ffffffd9;text-decoration:none;padding:7px 13px;border-radius:999px;font-size:.94rem;font-weight:500;white-space:nowrap;transition:background .2s,color .2s}.pill a:hover{color:#fff;background:#ffffff14}.pill a.on{background:#ffffff2e;color:#fff}
.hdr .btn{margin-left:auto}.menu{display:none}
@media (max-width:1240px){.pill{display:none}.menu{display:inline-flex;margin-left:auto;background:#ffffff26;border:1px solid #ffffff40;color:#fff;border-radius:999px;padding:9px 16px;font:600 .95rem var(--fb);cursor:pointer}.hdr .btn{margin-left:0}
 .pill.open{display:flex;flex-direction:column;position:absolute;top:82px;left:0;right:0;transform:none;background:HDRfa;border-radius:18px;padding:10px;animation:mo .25s ease}.pill.open a{padding:13px 16px;font-size:1.05rem}@keyframes mo{from{opacity:0;transform:translateY(-6px)}}}
@media (max-width:560px){.hdr .btn{display:none}.logo img{height:22px}}
/* hero (home e pagine interne) */
.hero{padding:8px}.hero .f{position:relative;min-height:calc(100svh - 16px);border-radius:var(--r);overflow:hidden;color:#fff;display:flex;flex-direction:column;justify-content:flex-end;isolation:isolate;background:var(--dark)}
.hero .f>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;transform:scale(1.06);animation:hz 2.4s cubic-bezier(.2,.7,.2,1) forwards}@keyframes hz{to{transform:none}}
.hero .f::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,#1b1a1b80 0%,#1b1a1b00 30%,#1b1a1b40 55%,#1b1a1be0 100%)}
.hero .b{padding:0 clamp(18px,2.6vw,38px) 22px}.hero .top{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,520px);gap:24px 60px;align-items:end;padding-bottom:30px;border-bottom:1px solid #ffffff40}
.hero h1{font-size:clamp(2.5rem,1.2rem + 4.4vw,4.9rem);line-height:1.02}.hero h1 span{display:block;opacity:0;transform:translateY(26px);animation:up 1s cubic-bezier(.2,.7,.2,1) forwards}.hero h1 span+span{animation-delay:.15s}
.hero .top p{margin:0;color:#F1EEE9;opacity:0;animation:up 1s ease .4s forwards}@keyframes up{to{opacity:1;transform:none}}
.hero .bot{display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;padding-top:22px;opacity:0;animation:up 1s ease .55s forwards}
.hero .acts{display:flex;gap:14px;flex-wrap:wrap}.checks{display:flex;gap:28px;flex-wrap:wrap;list-style:none;margin:0;padding:0;font-weight:600}
.checks li{display:flex;align-items:center;gap:10px}.checks svg{width:22px;height:22px}.checks circle{fill:var(--acc)}.checks path{fill:none;stroke:#fff;stroke-width:2.2}
.hero.sm .f{min-height:min(76svh,680px)}.hero.noph .f{min-height:min(60svh,520px);background:radial-gradient(90% 120% at 85% 0%,color-mix(in srgb,var(--acc) 30%,transparent),transparent 60%),repeating-linear-gradient(90deg,#ffffff0a 0 1px,transparent 1px 80px),var(--dark)}.hero.noph .f::after{display:none}.hero.sm h1{font-size:clamp(2.3rem,1.3rem + 3.4vw,4.2rem)}.hero.sm .top{border-bottom:0;padding-bottom:8px}
.crumbs{display:flex;flex-wrap:wrap;gap:6px 10px;list-style:none;margin:0 0 18px;padding:0;font-size:.9rem;color:#ffffffc7;opacity:0;animation:up .8s ease forwards}
.crumbs a{color:#fff;text-decoration:none;border-bottom:1px solid #ffffff59}.crumbs a:hover{border-color:#fff}.crumbs li+li::before{content:"/";margin-right:10px;opacity:.6}
@media (max-width:860px){.hero .top{grid-template-columns:1fr}.checks{gap:14px 20px;font-size:.92rem}}
/* card servizi */
.svc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}@media (max-width:980px){.svc{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:620px){.svc{grid-template-columns:1fr}}
.svc a{background:var(--paper);border-radius:20px;padding:6px;text-decoration:none;display:flex;flex-direction:column;transition:transform .4s cubic-bezier(.2,.7,.2,1),box-shadow .4s}.svc a:hover{transform:translateY(-6px);box-shadow:0 30px 50px -34px #0006}
.svc .ph{position:relative;aspect-ratio:415/240;border-radius:15px;overflow:hidden;background:var(--card2)}.svc img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}.svc a:hover img{transform:scale(1.05)}
.chip{position:absolute;left:12px;top:12px;display:flex;align-items:center;gap:7px;background:var(--dk70);color:#fff;border-radius:999px;padding:5px 12px;font-weight:600;font-size:.85rem}.chip::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--acc)}
.svc .t{padding:20px 16px 16px;display:grid;gap:8px;flex:1}.svc h3{font-size:1.26rem}.svc p{margin:0;color:var(--muted)}
.more{display:inline-flex;align-items:center;gap:10px;font-weight:600;margin-top:auto;padding-top:12px}.more i{width:24px;height:24px;border-radius:50%;background:var(--ink);color:var(--onink);display:grid;place-items:center;transition:transform .3s,background .3s}.more i svg{width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:2.2}
a:hover .more i{transform:rotate(-45deg);background:var(--acc);color:var(--onacc)}
/* prima e dopo */
.ba{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.ba.two{grid-template-columns:repeat(2,minmax(0,1fr))}@media (max-width:980px){.ba{grid-template-columns:1fr 1fr}}@media (max-width:620px){.ba,.ba.two{grid-template-columns:1fr}}
.cmp{position:relative;aspect-ratio:427/470;border-radius:20px;overflow:hidden;--x:50%;user-select:none;touch-action:pan-y;cursor:ew-resize;background:var(--card2)}.cmp.wide{aspect-ratio:4/3}
.cmp img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;pointer-events:none}.cmp .a{clip-path:inset(0 0 0 var(--x))}
.cmp .ln{position:absolute;top:0;bottom:0;left:var(--x);width:2px;background:#fff;transform:translateX(-1px)}.cmp .hd{position:absolute;top:50%;left:var(--x);width:48px;height:48px;border-radius:50%;background:#fff;transform:translate(-50%,-50%);display:grid;place-items:center;box-shadow:0 6px 20px #0005;color:#2a2929;font-weight:700;letter-spacing:4px}
.cmp input{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:ew-resize;margin:0}.cmp input:focus-visible+.hd{outline:3px solid var(--acc);outline-offset:3px}
.cmp .lb{position:absolute;top:16px;padding:6px 14px;border-radius:999px;font-weight:600;font-size:.88rem;pointer-events:none;background:var(--dk70);color:#fff}.cmp .l1{left:16px}.cmp .l2{right:16px;background:var(--acc)}
.ba h3{font-size:1.18rem;margin:16px 4px 4px}.ba p{margin:0 4px;color:var(--muted);font-size:.95rem}.dk .ba p{color:var(--dkmuted)}
/* perché noi */
.why{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:clamp(30px,6vw,100px)}@media (max-width:900px){.why{grid-template-columns:1fr}}
.why .ph{position:relative;margin-top:30px;border-radius:20px;overflow:hidden;aspect-ratio:538/260}.why .ph img{width:100%;height:100%;object-fit:cover}
.why .ph div{position:absolute;inset:auto 0 0 0;padding:18px 20px;color:#fff;background:linear-gradient(0deg,#1b1a1bd0,transparent)}.why .ph b{font-size:1.15rem}
.wg{display:grid;grid-template-columns:1fr 1fr;gap:20px}@media (max-width:560px){.wg{grid-template-columns:1fr}}
.wg>div{background:var(--paper);color:var(--ink);border-radius:20px;padding:20px;min-height:200px;display:flex;flex-direction:column;transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s}.wg>div:hover{transform:translateY(-4px);box-shadow:0 24px 40px -30px #0007}
.wg svg{width:42px;height:42px;padding:10px;border-radius:10px;background:var(--acc);stroke:var(--onacc);fill:none;stroke-width:1.7}
.wg h3{font-size:1.15rem;margin:auto 0 8px;padding-top:18px}.wg p{margin:0;color:var(--muted);font-size:.97rem}.wg p a{color:var(--accdk);text-decoration:none}.wg .no{font-weight:700;color:var(--accdk)}
/* come lavoriamo: sezione fissata, la villa si costruisce */
.proc{position:relative;height:430vh;padding:0}.proc .st{position:sticky;top:0;height:100svh;display:flex;flex-direction:column;padding:104px 0 18px;overflow:hidden}
.proc .head{margin-bottom:26px}
.steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0 24px;position:relative;margin-bottom:22px}
.steps::before,.steps .fill{content:"";position:absolute;left:0;top:18px;height:1px;background:#ffffff26;right:0}.steps .fill{transform-origin:0 50%;transform:scaleX(var(--p,0));background:var(--acc);height:2px}
.pstep{position:relative;opacity:.4;transition:opacity .45s}.pstep.on{opacity:1}
.pstep span{display:inline-block;background:#ffffff26;color:var(--ondark);border-radius:999px;padding:9px 13px;font-weight:600;font-size:.86rem;position:relative;transition:background .45s,color .45s}.pstep.on span{background:var(--acc);color:var(--onacc)}
.pstep h3{font-size:1.15rem;margin:20px 0 6px}.pstep p{margin:0;color:var(--dkmuted);font-size:.95rem;max-width:30ch}
.stage3d{position:relative;flex:1;min-height:0;border-radius:20px;overflow:hidden;background:#24221f}.stage3d canvas{display:block;width:100%!important;height:100%!important}
.stage3d>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.proc.has3d .stage3d>img{display:none}
.stage3d .bar{position:absolute;left:20px;right:20px;top:18px;height:2px;border-radius:2px;background:#ffffff33;overflow:hidden}.stage3d .bar i{display:block;height:100%;width:100%;transform-origin:0 50%;transform:scaleX(0);background:var(--acc)}
.cap3d{position:absolute;left:16px;bottom:16px;background:var(--dk85);color:#fff;border-radius:999px;padding:8px 14px;font-weight:600;font-size:.85rem}.proc:not(.has3d) .bar,.proc:not(.has3d) .cap3d{display:none}
@media (max-width:860px){.proc{height:380vh}.proc .st{padding-top:96px}.proc .head{margin-bottom:14px}.proc .head .lead{display:none}.proc h2{font-size:2rem}
 .steps{gap:0 8px;margin-bottom:14px}.pstep span{padding:7px 9px;font-size:.74rem}.pstep h3,.pstep p{display:none}.pstep.cur h3,.pstep.cur p{display:block;position:absolute;left:0;width:calc(400% + 24px)}
 .pstep:nth-child(3).cur h3,.pstep:nth-child(3).cur p{left:calc(-100% - 8px)}.pstep:nth-child(4).cur h3,.pstep:nth-child(4).cur p{left:calc(-200% - 16px)}.pstep:nth-child(5).cur h3,.pstep:nth-child(5).cur p{left:calc(-300% - 24px)}
 .pstep.cur h3{top:44px;margin:0}.pstep.cur p{top:72px;max-width:none}.steps{padding-bottom:84px}}
/* anteprima del 3D in home (solo una foto: three.js non si carica in home) */
.teaser{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:clamp(24px,4vw,60px);align-items:center;padding:clamp(56px,6vw,90px) 0}@media (max-width:900px){.teaser{grid-template-columns:1fr}}
.teaser .ph{position:relative;border-radius:18px;overflow:hidden;aspect-ratio:16/10;display:block}.teaser .ph img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}.teaser .ph:hover img{transform:scale(1.04)}
.teaser .ph span{position:absolute;left:16px;bottom:16px;background:var(--acc);color:var(--onacc);border-radius:999px;padding:8px 14px;font-weight:600;font-size:.9rem}
.tl{list-style:none;padding:0;margin:26px 0 30px;display:grid;gap:10px;counter-reset:s}.tl li{display:flex;gap:14px;align-items:baseline;counter-increment:s;border-top:1px solid #ffffff22;padding-top:10px;font-weight:500}.tl li::before{content:"0" counter(s);font-weight:600;color:var(--acc)}
/* lavori */
.wk{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}@media (max-width:980px){.wk{grid-template-columns:1fr 1fr}}@media (max-width:620px){.wk{grid-template-columns:1fr}}
.wk a{background:var(--paper);border-radius:20px;padding:6px 6px 20px;display:flex;flex-direction:column;gap:6px;text-decoration:none;transition:transform .4s cubic-bezier(.2,.7,.2,1),box-shadow .4s}.wk a:hover{transform:translateY(-6px);box-shadow:0 30px 50px -34px #0006}
.wk a[hidden]{display:none}.wk .ph{border-radius:15px;overflow:hidden;aspect-ratio:369/230;background:var(--card2);position:relative}.wk img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}.wk a:hover img{transform:scale(1.05)}
.wk .k{font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--accdk);font-weight:700;padding:12px 14px 0}.wk h3{font-size:1.22rem;padding:0 14px}.wk p{margin:0;padding:0 14px;color:var(--muted);font-size:.96rem}.wk .more{padding:6px 14px 0}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 26px}.tabs button{border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;padding:9px 16px;font:600 .95rem var(--fb);cursor:pointer;transition:background .2s,color .2s}
.tabs button[aria-pressed=true]{background:var(--ink);color:var(--onink);border-color:var(--ink)}
.facts{display:grid;grid-template-columns:repeat(3,1fr);margin-top:20px;border:1px solid var(--line);border-radius:12px;overflow:hidden}.facts div{padding:18px;text-align:center;font-weight:600;font-size:1.02rem}.facts div+div{border-left:1px solid var(--line)}
.facts b{display:block;font-family:var(--fh);font-size:2rem;letter-spacing:-.03em;color:var(--accdk)}
@media (max-width:620px){.facts{grid-template-columns:1fr}.facts div+div{border-left:0;border-top:1px solid var(--line)}}
.revhead{display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;margin-bottom:40px}.revhead .lead{max-width:40ch}
/* banner del gruppo */
.band{position:relative;border-radius:20px;overflow:hidden;color:#fff;min-height:342px;display:flex;align-items:center;isolation:isolate;background:var(--dark)}
.band>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}.band::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,#1b1a1bf0 0%,#1b1a1bb3 45%,#1b1a1b22 100%)}
.band .tx{padding:clamp(28px,4vw,60px);max-width:680px}.band h2{margin-bottom:18px}.band p{color:#E6E2DC;margin:0 0 24px}.band .tag{color:#E6E2DC}
.band .glass{position:absolute;right:60px;bottom:60px;background:#1b1a1bb8;border:1px solid #ffffff26;border-radius:12px;padding:16px 18px}.band .glass b{display:block;font-size:1.15rem}
@media (max-width:860px){.band .glass{display:none}}
/* catena del gruppo */
.chain{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;list-style:none;padding:0;margin:34px 0 0}@media (max-width:860px){.chain{grid-template-columns:1fr 1fr}}@media (max-width:480px){.chain{grid-template-columns:1fr}}
.chain a{display:grid;gap:6px;height:100%;background:var(--paper);color:var(--ink);border-radius:16px;padding:18px;text-decoration:none;transition:transform .3s}.chain a:hover{transform:translateY(-3px)}.chain small{color:var(--accdk);font-weight:700}.chain b{font-size:1.1rem}.chain span{color:var(--muted);font-size:.94rem}
.chain .me a{background:var(--acc);color:var(--onacc)}.chain .me span,.chain .me small{color:inherit;opacity:.85}
/* zone */
.zones{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(30px,4vw,50px);align-items:center}@media (max-width:900px){.zones{grid-template-columns:1fr}}
.map{background:var(--dark);border-radius:20px;aspect-ratio:620/520;position:relative;overflow:hidden}.map svg{position:absolute;inset:0;width:100%;height:100%}
.map .lab{position:absolute;transform:translate(-50%,-140%);background:#fff;color:#2a2929;border-radius:999px;padding:5px 13px;font-size:.88rem;white-space:nowrap}
.map .lab::after{content:"";position:absolute;left:50%;top:calc(100% + 10px);width:9px;height:9px;border-radius:50%;background:var(--acc);border:2px solid #fff;transform:translateX(-50%);box-shadow:0 0 0 5px #ffffff22}
.places{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;list-style:none;padding:0;margin:26px 0 30px}
.places li{display:flex;align-items:center;gap:8px;background:var(--paper);border-radius:999px;padding:9px 14px;transition:transform .25s}.places li:hover{transform:translateY(-2px)}.places a{text-decoration:none}.places svg{width:18px;height:18px;flex:none;fill:var(--acc);stroke:var(--paper);stroke-width:1.2}
/* esperienza */
.gua{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(30px,5vw,80px)}@media (max-width:900px){.gua{grid-template-columns:1fr}}
.ring{width:240px;height:240px;border-radius:50%;border:1px dashed #ffffff66;display:grid;place-items:center;margin:46px 0 0 clamp(0px,10vw,130px)}
.ring div{width:188px;height:188px;border-radius:50%;background:var(--acc);color:var(--onacc);display:grid;place-content:center;text-align:center}
.ring b{font-family:var(--fh);font-size:3.2rem;line-height:1;letter-spacing:-.04em}.ring small{font-weight:700;font-size:1rem;line-height:1.3}.ring small span{opacity:.8;display:block}
.gl{display:grid;gap:20px;align-content:start}.gl div{display:flex;align-items:center;gap:16px;border:1px solid #ffffff2e;border-radius:12px;padding:12px 14px;font-weight:600;font-size:1.08rem}
.gl svg{width:42px;height:42px;padding:10px;border-radius:8px;background:var(--acc);stroke:var(--onacc);fill:none;stroke-width:1.8;flex:none}.gua .note{color:var(--dkmuted);margin:40px 0 0}
/* domande */
.faq{max-width:872px;margin:0 auto}.faq>h2{text-align:center;margin-bottom:40px}.faq>.tag{justify-content:center}.faq h3{font-size:1.4rem;margin:44px 0 16px}.faq h3:first-child{margin-top:0}
.faq details{background:var(--paper);border-radius:12px;margin-bottom:14px;transition:box-shadow .3s}.faq details[open]{box-shadow:0 20px 40px -30px #0006}
.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:20px;padding:18px 18px 18px 20px;font-weight:600;font-size:1.06rem}.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";flex:none;width:38px;height:38px;border-radius:8px;background:var(--ink);color:var(--onink);display:grid;place-items:center;font-size:1.5rem;font-weight:400;transition:transform .35s,background .3s}.faq details[open] summary::after{transform:rotate(45deg);background:var(--acc);color:var(--onacc)}
.faq details p{margin:0;padding:0 20px 20px;color:var(--muted);max-width:68ch}.faq details p a,.lead a{color:var(--accdk)}
.faq .all{text-align:center;margin-top:30px}
/* pagine di dettaglio */
.split{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(30px,5vw,80px);align-items:start}@media (max-width:900px){.split{grid-template-columns:1fr}}
.split .ph{border-radius:20px;overflow:hidden;aspect-ratio:4/3;background:var(--card2)}.split .ph img{width:100%;height:100%;object-fit:cover}
.prose p{margin:0 0 16px;color:var(--muted);font-size:1.06rem;max-width:62ch}.prose p.big{font-size:clamp(1.2rem,1rem + .6vw,1.5rem);color:var(--ink);line-height:1.4}.prose p a{color:var(--accdk)}
.ticks{list-style:none;padding:0;margin:20px 0 30px;display:grid;gap:12px}.ticks li{display:flex;gap:12px;align-items:flex-start}.ticks svg{width:22px;height:22px;flex:none;margin-top:2px}.ticks circle{fill:var(--acc)}.ticks path{fill:none;stroke:var(--onacc);stroke-width:2.2}.ticks a{color:var(--ink)}
.kv{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr));gap:12px;margin:0 0 40px}
.kv div{background:var(--paper);border-radius:16px;padding:18px}.kv small{display:block;color:var(--muted);font-size:.84rem;font-weight:600;margin-bottom:6px;letter-spacing:.02em}.kv b{font-size:1.08rem;font-weight:600}
.pn{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;border-top:1px solid var(--line);margin-top:56px;padding-top:24px}.pn a{text-decoration:none;display:grid;gap:4px;max-width:46%}.pn small{color:var(--muted)}.pn b{font-size:1.1rem;transition:color .2s}.pn a:last-child{text-align:right;margin-left:auto}
.pn a:hover b{color:var(--accdk)}
.note2{font-size:.88rem;color:var(--muted);margin-top:16px}.note2 a{color:var(--accdk)}
.contacts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:30px}@media (max-width:900px){.contacts{grid-template-columns:1fr 1fr}}@media (max-width:480px){.contacts{grid-template-columns:1fr}}
.contacts>*{background:var(--paper);border-radius:16px;padding:18px;text-decoration:none;display:grid;gap:4px;transition:transform .3s}.contacts a:hover{transform:translateY(-3px)}.contacts small{color:var(--muted);font-weight:600}.contacts b{font-size:1.06rem;font-weight:600;overflow-wrap:anywhere}
/* preventivo */
.cfg{background:var(--paper);border-radius:var(--r);padding:clamp(24px,4.5vw,60px)}.cfg .prog{height:3px;background:var(--line);margin:26px 0 28px;border-radius:2px;position:relative;overflow:hidden}.cfg .prog i{position:absolute;inset:0;background:var(--acc);transform-origin:0 50%;transform:scaleX(.25);transition:transform .5s}
.q{display:none}.q.on{display:block;animation:qin .45s ease}@keyframes qin{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.q .step{display:inline-block;background:var(--soft);color:var(--ink);border-radius:999px;padding:6px 12px;font-weight:700;font-size:.8rem}.q h3{font-size:clamp(1.4rem,1.1rem + 1.2vw,2rem);margin:14px 0 22px;font-weight:500}
.tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}@media (max-width:800px){.tiles{grid-template-columns:1fr 1fr}}@media (max-width:420px){.tiles{grid-template-columns:1fr}}
.tiles button{background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:16px;text-align:left;font:600 1rem var(--fb);color:var(--ink);cursor:pointer;display:flex;gap:12px;align-items:center;transition:transform .2s,background .2s,border-color .2s}
.tiles button svg{width:24px;height:24px;stroke:currentColor;fill:none;stroke-width:1.6;flex:none}.tiles button:hover{transform:translateY(-2px);border-color:var(--acc)}.tiles button[aria-pressed=true]{background:var(--ink);color:var(--onink);border-color:var(--ink)}
.nav2{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:24px;flex-wrap:wrap}.back{background:none;border:0;font:500 1rem var(--fb);color:var(--muted);cursor:pointer}
.cfg label{display:grid;gap:6px;font-weight:600;font-size:.9rem}.cfg input,.cfg textarea{font:400 1rem var(--fb);padding:.8rem .9rem;border:1px solid var(--line);border-radius:10px;background:var(--bg);width:100%;color:var(--ink)}
.cfg input:focus,.cfg textarea:focus{outline:2px solid var(--acc);outline-offset:1px}.cfg .row{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:14px}@media (max-width:560px){.cfg .row{grid-template-columns:1fr}}
.cfg .check{display:flex;gap:10px;font-weight:400;margin-top:12px}.cfg .check input{width:18px;height:18px;flex:none;margin-top:3px;accent-color:var(--acc)}.cfg .check a{color:var(--accdk)}
.cfg [aria-invalid=true]{border-color:#C2410C;outline-color:#C2410C}.cfg .err{color:#C2410C;font-weight:700}.sum{color:var(--muted);margin:-8px 0 18px}.sum b{color:var(--ink)}
/* invito finale sopra il piede scuro */
.cta{position:relative;z-index:2;background:var(--soft);color:#2a2929;border-radius:var(--r);padding:clamp(28px,4vw,56px) clamp(24px,4vw,50px);display:grid;grid-template-columns:1fr 1fr;gap:24px 40px;align-items:center;margin-bottom:-186px}
.cta .tag{color:#3d3a3a}.cta .tag::before{background:#2a2929}.cta .btn{background:#2a2929;color:#fff}
@media (max-width:800px){.cta{grid-template-columns:1fr;margin-bottom:-120px}}.cta p{color:#3d3a3a;margin:0 0 22px}
.cta ul{display:flex;gap:10px 22px;flex-wrap:wrap;list-style:none;padding:0;margin:22px 0 0;font-weight:500}.cta li+li::before{content:"•";margin-right:22px;margin-left:-12px}
.ftr{background:var(--dark);color:var(--ondark);border-radius:var(--r) var(--r) 0 0;margin:0 8px;padding:250px 0 26px}@media (max-width:800px){.ftr{padding-top:170px}}
.ftr .g{display:grid;grid-template-columns:1.5fr 1fr 1.1fr 1.1fr 1.2fr;gap:30px}@media (max-width:1000px){.ftr .g{grid-template-columns:1fr 1fr}}@media (max-width:520px){.ftr .g{grid-template-columns:1fr}}
.ftr .logo img{height:30px}.ftr p{color:var(--dkmuted);max-width:32ch}.ftr b{display:block;color:var(--ondark);font-size:1.08rem;margin-bottom:14px}.ftr ul{list-style:none;padding:0;margin:0;display:grid;gap:8px}.ftr a{color:var(--dkmuted);text-decoration:none}.ftr a:hover{color:var(--ondark)}
.ftr .bt{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;border-top:1px solid #ffffff26;margin-top:50px;padding-top:24px;color:var(--dkmuted)}
.plain{max-width:820px;margin:0 auto;padding:40px 20px 80px}.plain h1{font-size:2.8rem;margin-bottom:20px}.small{font-size:.86rem;color:var(--muted)}
.wa{background:#1F7A4D}
/* senza JavaScript: niente configuratore (restano telefono, email e WhatsApp), menu nel piede */
html:not(.js) .cfg .q,html:not(.js) .cfg .prog,html:not(.js) .hdr .menu,html:not(.js) .b3d{display:none}html:not(.js) .nojs{display:block!important}.nojs{display:none}
.b3d,.scrub{display:none}.lite .b3d{display:inline-flex;position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:2}.lite .b3d[hidden]{display:none}
.lite .proc.has3d .scrub{display:block;position:absolute;left:20px;right:20px;bottom:64px;width:calc(100% - 40px);accent-color:var(--acc);z-index:2}
/* modalità leggera: niente sezione fissata né animazioni legate allo scorrimento, niente ombre e zoom, solo dissolvenze */
.lite .proc{height:auto}.lite .proc .st{position:static;height:auto;padding:clamp(50px,6vw,90px) 0}.lite .stage3d{flex:none;aspect-ratio:16/9;min-height:260px}
.lite .pstep{opacity:1}.lite .pstep span{background:var(--acc);color:var(--onacc)}.lite .steps .fill{display:none}
@media (max-width:860px){.lite .pstep h3,.lite .pstep p{display:block;position:static;width:auto}.lite .steps{grid-template-columns:1fr 1fr;gap:16px;padding-bottom:0}.lite .pstep h3{margin-top:10px}}
.lite *,.lite *::before,.lite *::after{box-shadow:none!important}.lite img{transition:none!important}.lite a:hover img,.lite .hero .f>img{transform:none!important;animation:none!important}
.lite .svc a:hover,.lite .wk a:hover,.lite .wg>div:hover,.lite .chain a:hover,.lite .contacts a:hover{transform:none}
/* animazioni di entrata allo scorrimento (anche in modalità leggera: solo opacità e spostamento, una volta) */
.js .rv{opacity:0;transform:translateY(18px);transition:opacity .6s cubic-bezier(.2,.7,.2,1),transform .6s cubic-bezier(.2,.7,.2,1);will-change:opacity,transform}
.js .rv.rvi{transform:translateY(14px) scale(.975)}.js .rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.js .rv{opacity:1;transform:none;transition:none}}
.si{width:44px;height:44px;border-radius:12px;background:var(--acc);display:grid;place-items:center;margin-bottom:4px}.si svg{width:24px;height:24px;stroke:var(--onacc);fill:none;stroke-width:1.7}
.get{background:var(--paper);border-radius:20px;padding:clamp(22px,3vw,36px)}.get h2{font-size:clamp(1.6rem,1.2rem + 1.2vw,2.2rem);margin:16px 0 4px}
.hero.noph .f{min-height:0}.noph .b{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,560px);gap:30px 50px;align-items:end;padding-top:112px;padding-bottom:clamp(22px,3vw,38px)}.noph .top{grid-template-columns:1fr}
.hph{border-radius:16px;overflow:hidden;aspect-ratio:4/3;background:var(--card2)}.hph img{width:100%;height:100%;object-fit:cover}
@media (max-width:900px){.noph .b{grid-template-columns:1fr;padding-top:100px}}
@media (prefers-reduced-motion:reduce){.hero h1 span,.hero .top p,.hero .bot,.crumbs{opacity:1;transform:none}.hero .f>img{transform:none}}
""" + TH.get("css", "")).replace("HDR", TH["hdr"])

JS = b2.E_JS + r"""
var RM=matchMedia("(prefers-reduced-motion: reduce)").matches,H=document.documentElement,LITE=function(){return H.classList.contains("lite")};
// header pieno quando si scorre
var hd=document.querySelector(".hdr");function hs(){hd.classList.toggle("s",scrollY>40)}addEventListener("scroll",hs,{passive:true});hs();
// prima/dopo: cursore trascinabile (anche da tastiera)
document.querySelectorAll(".cmp").forEach(function(c){var r=c.querySelector("input");function set(v){c.style.setProperty("--x",v+"%")}r.addEventListener("input",function(){set(r.value)});
 var down=false;function mv(e){var b=c.getBoundingClientRect();var x=(e.clientX-b.left)/b.width*100;x=Math.max(0,Math.min(100,x));r.value=x;set(x)}
 c.addEventListener("pointerdown",function(e){down=true;mv(e)});addEventListener("pointerup",function(){down=false});c.addEventListener("pointermove",function(e){if(down)mv(e)})});
// come lavoriamo: i passi si accendono con lo scorrimento della sezione fissata (solo trasformazioni, niente layout)
var prc=document.querySelector(".proc");if(prc){var ss=prc.querySelectorAll(".pstep"),sl=prc.querySelector(".steps"),li=-1,tk=0;
 function ps(){tk=0;if(LITE())return;var b=prc.getBoundingClientRect();if(b.bottom<0||b.top>innerHeight)return;var p=Math.max(0,Math.min(1,-b.top/Math.max(1,b.height-innerHeight)));var i=Math.min(3,Math.floor(p*4));
  if(i!==li){li=i;ss.forEach(function(s,j){s.classList.toggle("on",j<=i);s.classList.toggle("cur",j===i)})}sl.style.setProperty("--p",Math.min(1,p*1.33).toFixed(3))}
 addEventListener("scroll",function(){if(!tk)tk=requestAnimationFrame(ps)},{passive:true});ps()}
// three.js: si carica solo quando la sezione è vicina (e mai con "riduci animazioni")
// in modalità leggera niente three.js: foto vera e un pulsante "Guarda in 3D" per caricarlo solo se lo chiedi
var s3=document.querySelector(".stage3d[data-src]");function load3d(){if(!s3||s3.dataset.on)return;s3.dataset.on=1;var s=document.createElement("script");s.type="module";s.src=s3.dataset.src;document.body.appendChild(s)}
if(s3){var b3=s3.querySelector(".b3d");if(b3)b3.addEventListener("click",function(){window.FORCE3D=1;b3.hidden=true;load3d()});
 if(!LITE()&&"IntersectionObserver" in window){var lo=new IntersectionObserver(function(es){if(!es[0].isIntersecting||LITE())return;lo.disconnect();load3d()},{rootMargin:"900px 0px"});lo.observe(s3)}}
// primi fotogrammi lenti (computer vecchio): passa alla modalità leggera
if(!LITE()&&!H.classList.contains("full"))addEventListener("load",function(){var k=0,t0=0;function fr(t){if(!t0)t0=t;if(++k<11)return requestAnimationFrame(fr);if((t-t0)/10>50){H.classList.add("lite");if(window.LENIS){window.LENIS.destroy();window.LENIS=null}}}requestAnimationFrame(fr)});
// numeri veri che contano fino al valore (il testo finale è già nell'HTML)
if(!RM&&!LITE())document.querySelectorAll("[data-n]").forEach(function(b){var to=+b.dataset.n,suf=b.dataset.suf||"";new IntersectionObserver(function(es,o){if(!es[0].isIntersecting)return;o.disconnect();var t0=0;
 function f(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/1400);b.textContent=Math.round(to*(1-Math.pow(1-k,3)))+suf;if(k<1)requestAnimationFrame(f)}requestAnimationFrame(f)},{threshold:.6}).observe(b)});
// entrata di titoli, testi, card, immagini e voci di elenco: classe "rv", ritardo a scalare nei gruppi, una sola volta
(function(){var SEL="main h2,main h3,main .lead,main .prose>p,main .tag,.svc>a,.wk>a,.wg>div,.ba>div,.facts>div,.places li,.ticks li,.tl li,.kv>div,.contacts>*,.chain li,.split>.ph,.why .ph,.teaser .ph,.get,.cmp,.faq details,.pn a,.ftr .g>div,.map,.band,.cfg,.steps .pstep,.revhead,.head>div";
 var lite=LITE(),els=[].slice.call(document.querySelectorAll(SEL)).filter(function(e){return !e.closest(".hero,.hdr,.q,.reveal")&&(lite||!e.closest(".proc .st"))});
 els=els.filter(function(e){return !els.some(function(o){return o!==e&&o.contains(e)})});   // niente doppie entrate annidate
 var all=els.concat([].slice.call(document.querySelectorAll(".reveal")));
 if(RM||!("IntersectionObserver" in window)){all.forEach(function(e){e.classList.add("in")});return}
 els.forEach(function(e){e.classList.add("rv");if(/^(IMG|PICTURE)$/.test(e.tagName)||e.classList.contains("ph")||e.classList.contains("cmp")||e.classList.contains("map"))e.classList.add("rvi")});
 all.forEach(function(e){var p=e.parentNode,sib=[].filter.call(p.children,function(c){return c.classList.contains("rv")||c.classList.contains("reveal")}),i=sib.indexOf(e);if(i>0)e.style.transitionDelay=Math.min(i,6)*75+"ms"});
 function done(e){setTimeout(function(){e.style.transitionDelay="";e.classList.remove("rv","rvi")},1300)}
 var ob=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add("in");ob.unobserve(x.target);done(x.target)}})},{threshold:.12,rootMargin:"0px 0px -5% 0px"});
 all.forEach(function(e){ob.observe(e)});
 // rete di sicurezza: se si salta oltre (ancore, scorrimento velocissimo) ciò che è già sopra o sullo schermo compare comunque
 var tm=0;function chk(){tm=0;var h=innerHeight,left=0;all.forEach(function(e){if(e.classList.contains("in"))return;left++;if(e.getBoundingClientRect().top<h){e.classList.add("in");ob.unobserve(e);done(e)}});if(!left)removeEventListener("scroll",sc)}
 function sc(){if(!tm)tm=setTimeout(chk,250)}addEventListener("scroll",sc,{passive:true})})();
// scorrimento a inerzia leggero (Lenis) solo con mouse, mai su touch, in modalità leggera o con "riduci animazioni"
if(!LITE()&&!RM&&!matchMedia("(pointer: coarse)").matches){var ls=document.createElement("script");ls.src="https://cdn.jsdelivr.net/npm/lenis@1.3.27/dist/lenis.min.js";ls.async=true;
 ls.onload=function(){if(LITE()||!window.Lenis)return;var L=window.LENIS=new Lenis({lerp:.1,smoothWheel:true,syncTouch:false});(function r(t){if(window.LENIS){L.raf(t);requestAnimationFrame(r)}})(performance.now());
  document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(!a||!window.LENIS)return;var id=a.getAttribute("href"),el=id.length>1&&document.getElementById(id.slice(1));if(!el)return;e.preventDefault();L.scrollTo(el,{offset:-96})})};document.head.appendChild(ls)}
// preventivo: il tipo di lavoro può arrivare dalla pagina del servizio (?lavoro=Bagno)
var lv=new URLSearchParams(location.search).get("lavoro");if(lv){var tb=document.querySelector('.q[data-k=lavoro] button[data-v="'+lv.replace(/"/g,"")+'"]');if(tb)tb.click()}
""".replace('pr.style.width=((i+1)/qs.length*100)+"%"', 'pr.style.transform="scaleX("+((i+1)/qs.length)+")"').replace('pr.style.width="100%"', 'pr.style.transform="scaleX(1)"')

# ---------- contenuti (solo fatti veri del gruppo e di P) ----------
SERVICES = [  # slug, titolo, breve, categoria, foto (chiave P, ritaglio), testo, cosa comprende, lavori collegati, tipo per il preventivo
    ("nuove-costruzioni", "Nuove costruzioni", "Case, ville e palazzine residenziali, dalle fondazioni alle finiture.", "Costruzione", ("ferrari", None),
     "Costruiamo case unifamiliari, ville e palazzine residenziali. Partiamo dal progetto approvato, tuo o di Archi Trend, e seguiamo il cantiere dalle fondazioni fino alle finiture e alla consegna delle chiavi.",
     ["Scavi, fondazioni e platea", "Struttura portante e murature", "Coordinamento di tutti gli artigiani fino alle finiture", "Collaudo e consegna insieme a te"],
     ["ferrari", "optima", "greenhorse", "fortuna"], "Nuova costruzione"),
    ("impresa-generale", "Impresa generale", "Un solo contratto per tutta l'opera: coordiniamo gli artigiani e rispondiamo noi del risultato.", "Costruzione", ("maraini", None),
     "Come impresa generale ci occupiamo dell'intera opera con un solo contratto. Scegliamo e coordiniamo gli artigiani, teniamo il programma dei lavori e siamo il tuo unico interlocutore dal primo giorno alla consegna.",
     ["Un solo contratto e un solo referente", "Programma dei lavori condiviso", "Coordinamento di imprese e artigiani", "Capitolato, prezzo e tempi scritti prima di iniziare"],
     ["maraini", "synthesis", "aurea", "miracolli"], "Nuova costruzione"),
    ("opere-di-capomastro", "Opere di capomastro", "Platee, murature, tramezze, aperture e intonaci, eseguiti con cura.", "Costruzione", ("montagnola", (0, 0, .5, .5)),
     "Le opere di capomastro sono il cuore del mestiere: getti, murature, tramezze, nuove aperture e intonaci. Le eseguiamo sia dentro un cantiere completo sia come lavoro a sé.",
     ["Platee, solette e getti in calcestruzzo", "Murature portanti e tramezze", "Nuove aperture e demolizioni", "Intonaci interni ed esterni"],
     ["synthesis", "duelaghi", "miracolli"], "Opere di muratura"),
    ("ristrutturazioni", "Ristrutturazioni complete", "Appartamenti, case e stabili: ridiamo valore a ciò che esiste.", "Ristrutturazione", ("motta", (.45, 0, 1, 1)),
     "Ristrutturiamo appartamenti, case e palazzine, anche per chi vuole metterli a reddito o rivenderli. Dal sopralluogo iniziale alle finiture, con un capocantiere che coordina tutti i lavori.",
     ["Sopralluogo e rilievo dello stato attuale", "Demolizioni, impianti e nuove distribuzioni interne", "Pavimenti, intonaci e finiture", "Consegna pulita, pronta da abitare o da affittare"],
     ["magliaso", "montagnola", "motta", "pregassona", "corteglia"], "Appartamento intero"),
    ("bagni-e-cucine", "Bagni e cucine", "Le stanze che usi ogni giorno, rifatte con materiali che durano.", "Ristrutturazione", ("pregassona", None),
     "Bagni e cucine sono i lavori in cui l'organizzazione conta di più, perché si resta qualche giorno senza una stanza essenziale. Pianifichiamo bene prima, poi lavoriamo in ordine e puliti.",
     ["Sopralluogo e misure", "Demolizione e nuovi impianti", "Rivestimenti, sanitari e mobili", "Pulizia finale e consegna"],
     ["pregassona", "montagnola", "motta"], "Bagno"),
    ("facciate-e-tetti", "Facciate e tetti", "Isolamento, intonaci e coperture per una casa protetta e più efficiente.", "Ristrutturazione", ("magliaso", (.5, .06, 1, .94)),
     "Rinnoviamo facciate e coperture: intonaci, isolamento e tetti. Sono lavori che proteggono l'edificio e ne cambiano l'aspetto, come nella palazzina di Magliaso.",
     ["Ponteggi e messa in sicurezza", "Risanamento e nuovi intonaci di facciata", "Isolamento termico", "Lavori su coperture e lattonerie"],
     ["magliaso", "corteglia"], "Facciata o tetto"),
]
CAT = {"new": "Nuova costruzione", "ren": "Ristrutturazione"}
SICON = {"nuove-costruzioni": "nuova", "impresa-generale": "uno", "opere-di-capomastro": "muratura", "ristrutturazioni": "appartamento", "bagni-e-cucine": "bagno", "facciate-e-tetti": "facciata"}
SBA = {"facciate-e-tetti": ("magliaso", 0), "ristrutturazioni": ("montagnola", 0), "opere-di-capomastro": ("montagnola", 1)}   # prima/dopo veri per servizio
GET = ["Sopralluogo e preventivo senza impegno", "Preventivo con voci e quantità scritte", "Prezzo, tempi e capitolato firmati prima di iniziare", "Un capocantiere di riferimento che ti aggiorna", "Collaudo e consegna insieme, poi restiamo il tuo riferimento"]
ORDER = ["ferrari", "greenhorse", "optima", "maraini", "synthesis", "miracolli", "aurea", "duelaghi", "fortuna", "magliaso", "montagnola", "motta", "pregassona", "corteglia"]
SLUG = {k: "lavoro-" + k + ".html" for k in ORDER}
# prima/dopo veri: le foto originali sono composizioni "situazione precedente / attuale"
BA = {"magliaso": [("Palazzina a Magliaso", "La facciata prima e dopo la ristrutturazione", (0, .06, .5, .94), (.5, .06, 1, .94), "Prima", "Dopo")],
      "montagnola": [("Appartamento a Montagnola", "Lo stesso ambiente durante e dopo i lavori", (.5, 0, 1, .5), (.5, .5, 1, 1), "Prima", "Dopo"),
                     ("Appartamento a Montagnola", "Dalla muratura grezza all'ambiente finito", (0, 0, .5, .5), (0, .5, .5, 1), "Prima", "Dopo")]}
FAQ = [
    ("Preventivo e costi", [
        ("Il sopralluogo e il preventivo si pagano?", "No: il sopralluogo e il preventivo sono senza impegno."),
        ("Come si arriva al prezzo?", "Dopo il sopralluogo prepariamo un preventivo con voci e quantità scritte. Prezzo, tempi e capitolato li mettiamo per iscritto e li firmiamo prima di aprire il cantiere."),
        ("Cosa mi serve per chiedere un preventivo?", "Bastano l'indirizzo, cosa vorresti fare e quando. Se li hai, aiutano anche foto, misure indicative e i piani dell'immobile. Puoi iniziare dal <a href=\"preventivo.html\">configuratore</a> in un minuto."),
        ("E se durante i lavori cambia qualcosa?", "Se emerge un imprevisto o decidi di cambiare una scelta, te lo spieghiamo prima di procedere, così decidi tu sapendo cosa cambia."),
    ]),
    ("I lavori", [
        ("Fate anche piccoli lavori?", "Sì, anche opere di muratura e piccole ristrutturazioni. Raccontaci il lavoro e ti diciamo come possiamo aiutarti."),
        ("Che lavori fate?", "Nuove costruzioni, impresa generale, opere di capomastro, ristrutturazioni complete, bagni e cucine, facciate e tetti. Trovi ogni servizio nella pagina <a href=\"servizi.html\">Servizi</a>."),
        ("Chi seguo durante il cantiere?", "Un capocantiere di riferimento: coordina gli artigiani e ti aggiorna sull'avanzamento."),
        ("Posso restare in casa durante i lavori?", "Dipende dal lavoro. Ne parliamo al sopralluogo e organizziamo il cantiere di conseguenza."),
    ]),
    ("Progetto e permessi", [
        ("Serve un architetto?", "Per i lavori che richiedono una licenza ti affianchiamo Archi Trend, lo studio di architettura del gruppo, oppure lavoriamo con il tuo architetto."),
        ("Serve una licenza edilizia?", "Dipende dal tipo di lavoro e dal Comune. Lo verifichiamo con te all'inizio e, se serve, la domanda di costruzione la segue Archi Trend o il tuo architetto."),
        ("Ho già un progetto: potete costruirlo?", "Sì. Partiamo dal tuo progetto e dai documenti che hai, e prepariamo il preventivo su quella base."),
    ]),
    ("Zone e gruppo", [
        ("In quali zone lavorate?", "Soprattutto nel Luganese e nel resto del Ticino. Trovi alcuni comuni in cui il gruppo ha lavorato nella pagina <a href=\"zone.html\">Zone</a>."),
        ("Che cos'è il Gruppo New Trends?", "È il gruppo di aziende di Lugano di cui fa parte Edil Trend: New Trends per l'immobiliare, Archi Trend per l'architettura ed Edil Trend per la costruzione. Puoi seguire tutto il percorso, dal terreno alle chiavi, con un solo gruppo."),
        ("Come vi contatto?", f"Chiamaci al <a href=\"tel:{TEL}\">{PHONE}</a>, scrivi a <a href=\"mailto:{MAIL}\">{MAIL}</a>, su WhatsApp, oppure compila il <a href=\"preventivo.html\">modulo del preventivo</a>."),
    ]),
]
STEPS = [("Sopralluogo", "Veniamo sul posto, misuriamo e ascoltiamo cosa ti serve davvero."),
         ("Preventivo e contratto", "Voci, prezzi e tempi scritti e firmati prima di aprire il cantiere."),
         ("Il cantiere", "Un capocantiere coordina tutti gli artigiani e ti tiene aggiornato."),
         ("La consegna", "Collaudo insieme, ogni dettaglio sistemato. Poi restiamo il tuo riferimento.")]
WHY = [("prezzo", "Prezzo scritto.", "Voci e quantità nero su bianco prima di iniziare: sai sempre quanto spendi."),
       ("uno", "Un solo referente.", "Un capocantiere che coordina tutti gli artigiani e un numero da chiamare."),
       ("ordine", "Cantiere in ordine.", "Programma dei lavori chiaro, pulizia e rispetto di chi abita vicino."),
       ("dopo", "Dopo la consegna.", "Restiamo il tuo riferimento anche quando il cantiere è chiuso.")]
# zone: posizioni approssimative sul Luganese (x,y in % della mappa) e lavori del gruppo in quel comune
Z = [("Tesserete", 55, 20, ["ferrari"]), ("Vezia", 48, 38, ["synthesis"]), ("Savosa", 54, 42, ["maraini", "miracolli"]), ("Lugano", 60, 55, ["motta"]), ("Pregassona", 70, 46, ["pregassona"]),
     ("Muzzano", 38, 58, ["greenhorse", "duelaghi"]), ("Collina d'Oro", 44, 70, ["aurea"]), ("Montagnola", 36, 72, ["optima", "montagnola"]), ("Grancia", 52, 78, ["fortuna"]),
     ("Magliaso", 18, 74, ["magliaso"]), ("Corteglia", 66, 92, ["corteglia"])]

NAV = [("index.html", "Home", "home"), ("chi-siamo.html", "Chi siamo", "about"), ("servizi.html", "Servizi", "svc"), ("lavori.html", "Lavori", "works"),
       ("come-lavoriamo.html", "Come lavoriamo", "how"), ("zone.html", "Zone", "zone"), ("domande.html", "Domande", "faq")]

def dtitle(k):
    n, place = P[k][0], P[k][1]
    return n if n.startswith(("Residenza", "Villaggio")) else f"{n} a {place.replace('Lugano · ', '')}"

def logo():
    return f'<a class="logo" href="index.html" aria-label="Edil Trend SA, home"><img src="assets/logo-bianco.webp" alt="Edil Trend" width="{LOGO_W // 8}" height="{LOGO_H // 8}"></a>'

def header(cur):
    return (f'<header class="hdr"><div class="wrap">{logo()}<nav class="pill nav" aria-label="Principale">'
            + "".join(f'<a href="{h}"{" class=on aria-current=page" if k == cur else ""}>{t}</a>' for h, t, k in NAV)
            + f'</nav><a class="btn w" href="preventivo.html">Preventivo {AR}</a><button class="menu" data-menu aria-expanded="false">Menu</button></div></header>')

# modalità leggera automatica (PC e telefoni vecchi, risparmio dati, riduci animazioni): classe "lite" su <html> prima che la pagina si disegni.
# ?lite=1 la forza, ?lite=0 la spegne (prove). Senza JavaScript manca la classe "js" e tutto resta visibile.
LITE_HEAD = '(function(d){var n=navigator,c=n.connection||{},q=location.search,f=q.indexOf("lite=0")>-1,l=q.indexOf("lite=1")>-1||(!f&&((n.hardwareConcurrency&&n.hardwareConcurrency<=4)||(n.deviceMemory&&n.deviceMemory<=4)||c.saveData||matchMedia("(prefers-reduced-motion: reduce)").matches));d.className+=" js"+(l?" lite":"")+(f?" full":"")})(document.documentElement)'

def page(title, desc, body, v, name, three=False):
    canon = BASE + ("" if name == "index.html" else name)
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="{TH['hdr']}"><link rel="canonical" href="{canon}">
<script>{LITE_HEAD}</script><link rel="icon" href="favicon.png" type="image/png"><link rel="apple-touch-icon" href="apple-touch-icon.png">{FONTS}<link rel="stylesheet" href="assets/site.css?v={v}">{IMPORTMAP if three else ""}</head>
<body><a class="skip" href="#main">Vai al contenuto</a>{body}<a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Scrivici su WhatsApp">WhatsApp</a>
<script src="assets/app.js?v={v}" defer></script></body></html>"""

def footer():
    col = lambda t, items: f'<div><b>{t}</b><ul>' + "".join(f'<li><a href="{h}">{E(n)}</a></li>' for h, n in items) + "</ul></div>"
    return f"""<footer class="ftr"><div class="wrap"><div class="g"><div>{logo()}<p style="margin-top:18px">Impresa generale del Gruppo New Trends a Lugano: costruiamo e ristrutturiamo case fatte per durare, dal 1999.</p></div>
{col("Il sito", [(h, t) for h, t, _ in NAV] + [("preventivo.html", "Preventivo e contatti")])}
{col("Servizi", [("servizio-" + s[0] + ".html", s[1]) for s in SERVICES])}
{col("Il gruppo", [(SITES['newtrends'], "New Trends · Immobiliare"), (SITES['architrend'], "Archi Trend · Architettura"), (SITES['ediltrend'], "Edil Trend · Costruzioni")])}
<div><b>Contatti</b><ul><li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li>{ADDR}</li></ul></div></div>
<div class="bt"><span>© Edil Trend SA · Parte del Gruppo New Trends</span><span><a href="privacy.html">Privacy</a></span></div></div></footer>"""

def cta(title="Pronto a costruire o rinnovare casa?", text="Il passo successivo è semplice: prenota un sopralluogo gratuito e parliamo del tuo progetto.", href="preventivo.html"):
    return (f'<section><div class="wrap"><div class="cta reveal"><div><span class="tag">Iniziamo</span><h2>{E(title)}</h2></div>'
            f'<div><p>{E(text)}</p><a class="btn" href="{href}">Richiedi il sopralluogo {AR}</a><ul><li>Gratuito</li><li>Senza impegno</li><li>Risponde una persona</li></ul></div></div></div></section>')

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    A = os.path.join(OUT, "assets"); I = os.path.join(A, "img"); os.makedirs(I)
    img = {}
    def R(name, src, widths=(480, 960, 1600), box=None): img[name] = b2.rimg(src, I, name, widths, box); return img[name]
    def T(name, alt="", sizes="100vw", lazy=True, cls=""): return b2.imgtag(img[name], alt, sizes, lazy, cls)
    pr = lambda k: find_src(P[k][4])
    S3 = "(max-width:620px) 92vw, (max-width:980px) 46vw, 410px"; S2 = "(max-width:900px) 92vw, 620px"; SH = "calc(100vw - 16px)"
    # immagini (WebP in 2-3 larghezze)
    R("hero", pr("greenhorse"), (640, 1200, 2000))
    for k in ORDER:
        if k == "magliaso": R("p-" + k, pr(k), (480, 960), (.5, .06, 1, .94))
        elif k == "montagnola": R("p-" + k, pr(k), (480, 960), (.5, .5, 1, 1))
        elif k == "corteglia": R("p-" + k, pr(k), (480, 960), (0, 0, .5, .5))
        else: R("p-" + k, pr(k), (480, 960, 1600))
    for s in SERVICES:
        k, box = s[4]; R("s-" + s[0], pr(k), (480, 960), box)
    for k, lst in BA.items():
        for i, (_, _, b1, b2_, _, _) in enumerate(lst): R(f"ba-{k}-{i}-a", pr(k), (480, 800), b1); R(f"ba-{k}-{i}-b", pr(k), (480, 800), b2_)
    R("why", pr("optima"), (480, 960)); R("band", pr("aurea"), (640, 980)); R("proc", pr("greenhorse"), (640, 1200, 1600))
    # logo vero (non ricolorato) e favicon: il "re" verde su grafite
    for f, n in (("ediltrend-logo-bianco.png", "logo-bianco"), ("ediltrend-logo-scuro.png", "logo-scuro")):
        im = Image.open(os.path.join(HERE, "src", "logo", f)).convert("RGBA"); im.resize((480, round(480 * LOGO_H / LOGO_W)), Image.LANCZOS).save(os.path.join(A, n + ".webp"), "WEBP", quality=90, method=6)
    lg = Image.open(os.path.join(HERE, "src", "logo", "ediltrend-logo-scuro.png")).convert("RGBA").crop((838, 58, 1172, 264))
    for sz, fn in ((64, "favicon.png"), (180, "apple-touch-icon.png")):
        c = Image.new("RGBA", (sz, sz), (0x33, 0x31, 0x32, 255)); w = round(sz * .78); h = round(lg.height * w / lg.width); r2 = lg.resize((w, h), Image.LANCZOS)
        c.paste(r2, ((sz - w) // 2, (sz - h) // 2), r2); c.save(os.path.join(OUT, fn))
    shutil.copy(os.path.join(HERE, "src", "villa3d.js"), os.path.join(A, "villa3d.js"))

    # ---------- blocchi riusati ----------
    big = lambda im: img[im]["w"] >= 900      # foto troppo piccole: niente foto a tutta larghezza (sarebbe sgranata)
    def hero_sm(crumbs, h1, lead, im, alt):
        cr = '<ol class="crumbs">' + "".join(f'<li><a href="{h}">{E(t)}</a></li>' if h else f'<li aria-current="page">{E(t)}</li>' for h, t in crumbs) + "</ol>"
        ph = T(im, alt, SH, False) if im and big(im) else ""
        side = f'<div class="hph">{T(im, alt, "(max-width:900px) 92vw, 560px", False)}</div>' if im and not ph else ""   # foto piccola: in cornice, mai sgranata
        return (f'<section class="hero sm{"" if ph else " noph"}"><div class="f">{ph}<div class="b"><div><nav aria-label="Percorso">{cr}</nav><div class="top"><h1><span>{E(h1)}</span></h1>'
                f'<p>{E(lead)}</p></div></div>{side}</div></div></section>')
    def svc_cards(items):
        return '<div class="svc">' + "".join(f'<a class="reveal" href="servizio-{s[0]}.html"><div class="ph">{T("s-" + s[0], "", S3)}<span class="chip">{E(s[3])}</span></div><div class="t"><span class="si">{G(ICONS[SICON[s[0]]])}</span><h3>{E(s[1])}</h3><p>{E(s[2])}</p><span class="more">Scopri di più {AR}</span></div></a>' for s in items) + "</div>"
    def work_cards(keys):
        return '<div class="wk">' + "".join(f'<a class="reveal work" data-f="{P[k][5]}" href="{SLUG[k]}"><div class="ph">{T("p-" + k, P[k][0] + ", " + P[k][1], S3)}</div><span class="k">{E(CAT[P[k][5]])} · {E(P[k][1])}</span><h3>{E(dtitle(k))}</h3><p>{E(P[k][2])}</p><span class="more">Vedi il lavoro {AR}</span></a>' for k in keys) + "</div>"
    def ba_block(k, i, link=False):
        t, s, _, _, l1, l2 = BA[k][i]
        inner = (f'<div class="cmp{"" if link else " wide"}">{T(f"ba-{k}-{i}-a", t + ": " + l1.lower(), S3)}{T(f"ba-{k}-{i}-b", t + ": " + l2.lower(), S3, cls="a")}'
                 f'<span class="ln"></span><span class="lb l1">{l1}</span><span class="lb l2">{l2}</span><input type="range" min="0" max="100" value="50" aria-label="Confronta {l1.lower()} e {l2.lower()}: {E(t)}"><span class="hd" aria-hidden="true">‹›</span></div>')
        cap = f'<h3>{E(t)}</h3><p>{E(s)}</p>' + (f'<p style="margin-top:8px"><a href="{SLUG[k]}" style="color:inherit;font-weight:600">Vedi il lavoro →</a></p>' if link else "")
        return f'<div class="reveal">{inner}{cap}</div>'
    G = lambda d: f'<svg viewBox="0 0 24 24" aria-hidden="true">{d}</svg>'
    wy = "".join(f'<div class="reveal">{G(ICONS[i])}<h3>{E(a)}</h3><p>{E(b)}</p></div>' for i, a, b in WHY)
    stepcards = "".join(f'<div class="reveal"><span class="no">STEP {j + 1:02d}</span><h3>{E(a)}</h3><p>{E(b)}</p></div>' for j, (a, b) in enumerate(STEPS))
    chain = b2.chain("ediltrend", "chain")
    fqd = lambda items, op=True: "".join(f'<details class="reveal"{" open" if op and i == 0 else ""}><summary>{E(q)}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(items))
    dots = "".join(f'<circle cx="{x}" cy="{y}" r=".55"/>' for x in range(2, 100, 3) for y in range(2, 100, 3) if ((x - 50) ** 2 / 2400 + (y - 52) ** 2 / 2600) < 1)
    lake = '<path d="M30 62c6-4 12-2 18 0s10 6 16 4 8-8 14-6 6 8 2 12-10 3-14 6-4 10-10 10-6-6-10-8-10 0-14-3-6-11-2-15z" fill="#ffffff14"/>'
    def mapbox(show):
        return (f'<div class="map reveal" role="img" aria-label="Le zone del Luganese dove ha lavorato il gruppo"><svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><g fill="#ffffff2e">{dots}</g>{lake}</svg>'
                + "".join(f'<span class="lab" style="left:{x}%;top:{y}%">{E(n)}</span>' for n, x, y, _ in Z if n in show) + "</div>")
    places = "".join(f'<li>{PIN}<a href="{SLUG[ks[0]]}">{E(n)}</a></li>' for n, _, _, ks in Z)
    exp = (f'<section class="sec dk"><div class="wrap gua"><div class="reveal"><span class="tag">La nostra esperienza</span><h2>{YEARS} anni di cantieri, scritti nero su bianco.</h2>'
           f'<div class="ring" aria-hidden="true"><div><b data-n="{YEARS}">{YEARS}</b><small>ANNI<span>DI ESPERIENZA</span></small></div></div></div>'
           f'<div><div class="gl"><div class="reveal">{G(ICONS["prezzo"])}Sopralluogo e preventivo senza impegno</div><div class="reveal">{G(ICONS["ordine"])}Prezzo scritto prima di iniziare</div><div class="reveal">{G(ICONS["dopo"])}Tempi e capitolato messi per iscritto</div></div>'
           f'<p class="note">Il preventivo è senza impegno e i consigli sono onesti. Prezzo, tempi e capitolato li firmiamo prima di aprire il cantiere, e restiamo il tuo riferimento anche dopo la consegna.</p></div></div></section>')
    facts = '<div class="facts reveal"><div><b>1999</b>l\'anno di fondazione</div><div><b data-n="100" data-suf="+">100+</b>unità realizzate dal gruppo</div><div><b data-n="300" data-suf="+">300+</b>professionisti in rete</div></div>'
    band = (f'<section style="padding-bottom:clamp(70px,8vw,110px)"><div class="wrap"><div class="band reveal">{T("band", "", "(max-width:900px) 100vw, 1200px")}<div class="tx"><span class="tag">Gruppo New Trends</span><h2>Dal terreno alle chiavi, un solo gruppo.</h2>'
            f'<p>New Trends trova il terreno o l\'immobile, Archi Trend progetta e ottiene la licenza, Edil Trend costruisce, New Trends vende o affitta. Un unico interlocutore per tutto il percorso.</p><a class="btn w" href="{SITES["newtrends"]}">Scopri il gruppo {AR}</a></div>'
            f'<div class="glass"><b>3 aziende</b>un solo percorso</div></div></div></section>')
    tiles = lambda items: '<div class="tiles">' + "".join(f'<button type="button" data-v="{E(v)}" aria-pressed="false">{G(ICONS[ic]) if ic else ""}<span>{E(v)}</span></button>' for v, ic in items) + "</div>"
    cfg = f"""<div class="cfg reveal" id="preventivo"><span class="tag">Preventivo</span><h2>Raccontaci il lavoro.</h2><p class="lead" style="margin-top:12px">Quattro domande, un minuto. Poi ti chiamiamo per il sopralluogo, senza impegno.</p><p class="nojs lead" style="margin-top:16px">Il configuratore funziona con JavaScript attivo. Puoi anche chiamarci al <a href="tel:{TEL}">{PHONE}</a> o scrivere a <a href="mailto:{MAIL}">{MAIL}</a>.</p><div class="prog" aria-hidden="true"><i></i></div>
<div class="q" data-k="lavoro"><span class="step">STEP 01 / 04</span><h3>Di che lavoro si tratta?</h3>{tiles([("Bagno", "bagno"), ("Cucina", "cucina"), ("Appartamento intero", "appartamento"), ("Casa", "casa"), ("Facciata o tetto", "facciata"), ("Opere di muratura", "muratura"), ("Nuova costruzione", "nuova"), ("Altro", "altro")])}</div>
<div class="q" data-k="misura"><span class="step">STEP 02 / 04</span><h3>Quanto è grande la superficie?</h3>{tiles([("Meno di 30 m²", None), ("30–80 m²", None), ("80–150 m²", None), ("Più di 150 m²", None), ("Non lo so ancora", None)])}<div class="nav2"><button class="back" type="button">← Indietro</button></div></div>
<div class="q" data-k="quando"><span class="step">STEP 03 / 04</span><h3>Quando vorresti iniziare?</h3>{tiles([("Il prima possibile", None), ("Entro 3 mesi", None), ("Tra 3 e 6 mesi", None), ("Sto valutando", None)])}<div class="nav2"><button class="back" type="button">← Indietro</button></div></div>
<div class="q" data-k="contatti"><span class="step">STEP 04 / 04</span><h3>Dove possiamo ricontattarti?</h3><p class="sum"></p><form novalidate><div class="row"><label>Nome e cognome<input name="name" autocomplete="name" required></label><label>Comune del lavoro<input name="town" placeholder="es. Lugano"></label></div>
<div class="row"><label>Email<input name="email" type="email" autocomplete="email"></label><label>Telefono<input name="phone" type="tel" autocomplete="tel"></label></div>
<label>Altre informazioni (facoltativo)<textarea name="message" rows="2" placeholder="es. bagno al secondo piano, senza ascensore"></textarea></label><input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
<label class="check"><input type="checkbox" name="consent" required><span>Acconsento a essere ricontattato da Edil Trend SA secondo l'<a href="privacy.html">informativa privacy</a>.</span></label>
<label class="check"><input type="checkbox" name="newsletter"><span>Desidero ricevere occasionalmente novità del Gruppo New Trends (facoltativo).</span></label><p class="err" hidden role="alert"></p>
<div class="nav2"><button class="back" type="button">← Indietro</button><button class="btn" type="submit">Richiedi il sopralluogo {AR}</button></div></form></div></div>"""
    st = "".join(f'<div class="pstep{" on cur" if i == 0 else ""}"><span>STEP {i + 1:02d}</span><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i, (a, b) in enumerate(STEPS))
    end = f"</main>{footer()}"
    gap = '<div style="height:clamp(70px,8vw,110px)"></div>'
    pages = {}

    # ---------- HOME: riassunto con link alle pagine ----------
    home = f"""{header("home")}<section class="hero"><div class="f">{T("hero", "Residenza Green Horse, Muzzano", SH, False)}
<div class="b"><div class="top"><h1><span>Dalle fondamenta</span><span>alle finiture perfette</span></h1><p>Costruiamo e ristrutturiamo case, ville e palazzine nel Luganese. Impresa generale del Gruppo New Trends dal 1999: un solo contratto, un prezzo scritto e tempi chiari, dal primo sopralluogo alla consegna delle chiavi.</p></div>
<div class="bot"><div class="acts"><a class="btn w" href="preventivo.html">Richiedi un preventivo gratuito {AR}</a><a class="btn o" href="lavori.html">Guarda i lavori</a></div>
<ul class="checks"><li>{CHECK}Qualità</li><li>{CHECK}Precisione</li><li>{CHECK}Esperienza</li><li>{CHECK}Affidabilità</li></ul></div></div></div></section>
<main id="main">
<section class="sec"><div class="wrap"><div class="head"><div><span class="tag">I nostri servizi</span><h2>Tutto quello che possiamo costruire per te</h2></div>
<div class="r"><p class="lead">Che sia una stanza o un edificio intero, seguiamo tutto noi sotto un unico tetto, dall'inizio alla fine.</p><a class="btn" href="servizi.html">Tutti i servizi {AR}</a></div></div>{svc_cards(SERVICES)}</div></section>
<section class="sec dk"><div class="wrap"><div class="head"><div><span class="tag">Prima e dopo</span><h2>Guarda la trasformazione.</h2></div>
<div class="r"><p class="lead">Trascina il cursore: sono foto vere di lavori di ristrutturazione del gruppo.</p><a class="btn" href="lavori.html">Tutti i lavori {AR}</a></div></div><div class="ba">{ba_block("magliaso", 0, True)}{ba_block("montagnola", 0, True)}{ba_block("montagnola", 1, True)}</div></div></section>
<section class="sec"><div class="wrap why"><div class="reveal"><span class="tag">Perché noi</span><h2>Perché le famiglie ci affidano la loro casa.</h2><p class="lead" style="margin-top:18px">Niente scorciatoie, niente sorprese: un cantiere fatto di chiarezza e di mestiere.</p>
<div class="ph">{T("why", "Residenza Optima, Montagnola", S2)}<div><b>Dal 1999</b><br>a Lugano, con il Gruppo New Trends</div></div><p style="margin-top:24px"><a class="btn" href="chi-siamo.html">Chi siamo {AR}</a></p></div><div class="wg">{wy}</div></div></section>
<section class="dk gb"><div class="wrap teaser"><div class="reveal"><span class="tag">Come lavoriamo</span><h2>Semplice, dall'inizio alla fine.</h2><ol class="tl">{"".join(f"<li>{E(a)}</li>" for a, _ in STEPS)}</ol>
<a class="btn" href="come-lavoriamo.html">Guarda la casa che si costruisce {AR}</a></div><a class="ph reveal" href="come-lavoriamo.html" aria-label="Come lavoriamo: modello 3D">{T("proc", "Residenza Green Horse, Muzzano", S2)}<span>Modello 3D: scorri e la casa si costruisce</span></a></div></section>
<section class="sec"><div class="wrap"><div class="revhead"><div><span class="tag">Lavori del gruppo</span><h2>Costruito con cura, consegnato con precisione.</h2></div><div style="display:grid;gap:18px;justify-items:start"><p class="lead">Alcuni dei progetti seguiti dalle aziende del Gruppo New Trends.</p><a class="btn" href="lavori.html">Tutti i lavori {AR}</a></div></div>{work_cards(["maraini", "fortuna", "ferrari"])}
{facts}</div></section>
{band}
<section style="padding-bottom:clamp(70px,8vw,110px)"><div class="wrap zones">{mapbox({"Tesserete", "Lugano", "Montagnola", "Magliaso", "Savosa"})}<div class="reveal"><span class="tag">Zone</span><h2>Di casa nel Luganese.</h2><p class="lead" style="margin-top:16px">Vicini, conosciuti e sempre a portata di mano. Questi sono alcuni dei comuni in cui il gruppo ha costruito o ristrutturato.</p>
<ul class="places">{places}</ul><a class="btn" href="zone.html">Le zone {AR}</a></div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="faq"><span class="tag">Domande</span><h2>Domande frequenti.</h2>{fqd(FAQ[0][1][:2] + FAQ[1][1][:1] + FAQ[2][1][:1])}<p class="all"><a class="btn" href="domande.html">Tutte le domande {AR}</a></p></div></div></section>
{cta()}{end}"""
    pages["index.html"] = ("Edil Trend SA · Impresa generale a Lugano", "Impresa generale del Gruppo New Trends a Lugano: nuove costruzioni, ristrutturazioni e opere di capomastro, dal 1999.", home, False)

    # ---------- CHI SIAMO ----------
    about = f"""{header("about")}{hero_sm([("index.html", "Home"), (None, "Chi siamo")], "Chi siamo", "Edil Trend SA è l'impresa generale del Gruppo New Trends, a Lugano dal 1999: costruiamo e ristrutturiamo con un solo contratto e un solo referente.", "p-miracolli", "Residenza Miracolli, Savosa e Porza")}
<main id="main"><section class="sec"><div class="wrap split"><div class="prose reveal"><span class="tag">La nostra storia</span><h2 style="margin-bottom:24px">Un'impresa di mestiere, dentro un gruppo che segue tutto il percorso.</h2>
<p class="big">Dal 1999 Edil Trend costruisce e ristruttura nel Luganese.</p><p>Siamo un'impresa generale: nuove costruzioni, opere di capomastro e ristrutturazioni, con un capocantiere che coordina gli artigiani e un preventivo scritto prima di iniziare.</p>
<p>Facciamo parte del Gruppo New Trends, nato a Lugano nel 1991. Nel gruppo ognuno ha il suo mestiere: New Trends per l'immobiliare, Archi Trend per il progetto, Edil Trend per il cantiere. Per chi costruisce o ristruttura vuol dire un solo gruppo dal terreno alle chiavi.</p>
<p><a class="btn" href="servizi.html">I nostri servizi {AR}</a></p></div><div class="ph reveal">{T("why", "Residenza Optima, Montagnola", S2)}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><span class="tag">I numeri</span><h2>Fatti, non promesse.</h2>{facts}</div></section>
<section class="sec dk"><div class="wrap"><span class="tag">Il gruppo</span><h2>Dal terreno alle chiavi.</h2><p class="lead" style="margin-top:14px">Quattro passaggi, tre aziende, un solo gruppo. Tocca un passaggio per aprire il sito dell'azienda.</p>{chain}</div></section>
<section class="sec"><div class="wrap why"><div class="reveal"><span class="tag">Come ci comportiamo</span><h2>Quattro regole di cantiere.</h2><p class="lead" style="margin-top:18px">Le stesse per un bagno e per una palazzina.</p><p style="margin-top:24px"><a class="btn" href="come-lavoriamo.html">Come lavoriamo {AR}</a></p></div><div class="wg">{wy}</div></div></section>
{exp}{gap}{cta()}{end}"""
    pages["chi-siamo.html"] = ("Chi siamo · Edil Trend SA", "Edil Trend SA, impresa generale del Gruppo New Trends a Lugano dal 1999: chi siamo e come lavoriamo.", about, False)

    # ---------- SERVIZI + una pagina per servizio ----------
    svcp = f"""{header("svc")}{hero_sm([("index.html", "Home"), (None, "Servizi")], "Servizi", "Dalla nuova costruzione al bagno da rifare: sei servizi, un solo referente e un preventivo scritto.", "s-nuove-costruzioni", "Residenza Ferrari, Tesserete")}
<main id="main"><section class="sec"><div class="wrap"><div class="head"><div><span class="tag">Costruzione</span><h2>Costruire dal nuovo.</h2></div><p class="lead">Case, ville e palazzine: come impresa generale o per le sole opere di capomastro.</p></div>{svc_cards(SERVICES[:3])}
<div class="head" style="margin-top:80px"><div><span class="tag">Ristrutturazione</span><h2>Ridare valore a ciò che esiste.</h2></div><p class="lead">Appartamenti, bagni e cucine, facciate e tetti.</p></div>{svc_cards(SERVICES[3:])}</div></section>
<section class="sec dk"><div class="wrap why" style="align-items:center"><div class="reveal"><span class="tag">Non sai da dove partire?</span><h2>Raccontaci il lavoro, al resto pensiamo noi.</h2><p class="lead" style="margin-top:18px">Quattro domande nel configuratore e ti richiamiamo per il sopralluogo, senza impegno.</p></div>
<div class="reveal"><a class="btn g" href="preventivo.html">Apri il configuratore {AR}</a></div></div></section>{gap}{cta()}{end}"""
    pages["servizi.html"] = ("Servizi · Edil Trend SA", "Nuove costruzioni, impresa generale, opere di capomastro, ristrutturazioni, bagni e cucine, facciate e tetti nel Luganese.", svcp, False)
    for s in SERVICES:
        slug, t, short, cat, _, text, incl, rel, kind = s
        others = [x for x in SERVICES if x[0] != slug and x[3] == cat] + [x for x in SERVICES if x[3] != cat]
        body = f"""{header("svc")}{hero_sm([("index.html", "Home"), ("servizi.html", "Servizi"), (None, t)], t, short, "s-" + slug, "")}
<main id="main"><section class="sec"><div class="wrap split"><div class="prose reveal"><span class="tag">{E(cat)}</span><h2 style="margin-bottom:24px">Cosa facciamo</h2><p class="big">{E(text)}</p>
<ul class="ticks">{"".join(f"<li>{CHECK}<span>{E(x)}</span></li>" for x in incl)}</ul>
<p><a class="btn g" href="preventivo.html?lavoro={E(kind)}">Chiedi un preventivo {AR}</a></p></div><div class="get reveal"><span class="si">{G(ICONS[SICON[slug]])}</span><h2>Cosa ricevi</h2><ul class="ticks">{"".join(f"<li>{CHECK}<span>{E(x)}</span></li>" for x in GET)}</ul>
<p class="small">Sono le regole con cui lavoriamo su ogni cantiere, piccolo o grande.</p></div></div>
{f'<div class="wrap" style="margin-top:70px"><span class="tag">Prima e dopo</span><h2 style="margin-bottom:30px">Un lavoro vero di questo tipo.</h2><div class="ba two">{ba_block(*SBA[slug], True)}</div></div>' if slug in SBA else ""}</section>
<section class="sec dk"><div class="wrap"><div class="head"><div><span class="tag">Come lo seguiamo</span><h2>Quattro passi, sempre gli stessi.</h2></div><div class="r"><p class="lead">Dal sopralluogo alla consegna, con prezzo e tempi scritti prima di iniziare.</p><a class="btn" href="come-lavoriamo.html">Come lavoriamo {AR}</a></div></div>
<div class="wg" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">{stepcards}</div></div></section>
<section class="sec"><div class="wrap"><div class="revhead"><div><span class="tag">Lavori del gruppo</span><h2>Lavori di questo tipo.</h2></div><p class="lead">Progetti del Gruppo New Trends collegati a questo servizio.</p></div>{work_cards(rel[:3])}</div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="revhead"><div><span class="tag">Altri servizi</span><h2>Potrebbe servirti anche.</h2></div><a class="btn" href="servizi.html">Tutti i servizi {AR}</a></div>{svc_cards(others[:3])}</div></section>
{cta(href="preventivo.html?lavoro=" + E(kind))}{end}"""
        pages[f"servizio-{slug}.html"] = (f"{t} · Servizi · Edil Trend SA", f"{short} Edil Trend SA, impresa generale a Lugano.", body, False)

    # ---------- LAVORI + una pagina per lavoro ----------
    tabs = '<div class="tabs" role="group" aria-label="Filtra i lavori"><button type="button" aria-pressed="true" data-f="">Tutti</button><button type="button" aria-pressed="false" data-f="new">Nuove costruzioni</button><button type="button" aria-pressed="false" data-f="ren">Ristrutturazioni</button></div>'
    works = f"""{header("works")}{hero_sm([("index.html", "Home"), (None, "Lavori")], "Lavori", "Residenze, villette e ristrutturazioni seguite dalle aziende del Gruppo New Trends nel Luganese.", "p-ferrari", "Residenza Ferrari, Tesserete")}
<main id="main"><section class="sec"><div class="wrap"><div class="revhead"><div><span class="tag">Tutti i lavori</span><h2>Costruito con cura, consegnato con precisione.</h2></div><p class="lead">Tocca un lavoro per vedere i dettagli. I ruoli sono quelli descritti dal gruppo su new-trends.ch.</p></div>{tabs}{work_cards(ORDER)}{facts}</div></section>
<section class="sec dk"><div class="wrap"><div class="head"><div><span class="tag">Prima e dopo</span><h2>Guarda la trasformazione.</h2></div><p class="lead">Trascina il cursore: foto vere prima e dopo i lavori.</p></div><div class="ba">{ba_block("magliaso", 0, True)}{ba_block("montagnola", 0, True)}{ba_block("montagnola", 1, True)}</div></div></section>
{gap}{cta()}{end}"""
    pages["lavori.html"] = ("Lavori · Edil Trend SA", "Lavori del Gruppo New Trends nel Luganese: nuove residenze, villette e ristrutturazioni.", works, False)
    for i, k in enumerate(ORDER):
        n, place, size, role, _, cat = P[k]
        prv, nxt = ORDER[i - 1], ORDER[(i + 1) % len(ORDER)]
        bas = "".join(ba_block(k, j) for j in range(len(BA.get(k, []))))
        rel = [x for x in ORDER if P[x][5] == cat and x != k][:3]
        svc_rel = [s for s in SERVICES if k in s[7]][:3]
        status = "In costruzione" if "in costruzione" in size else ("Ristrutturato" if cat == "ren" else "Realizzato")
        title = dtitle(k)
        body = f"""{header("works")}{hero_sm([("index.html", "Home"), ("lavori.html", "Lavori"), (None, title)], title, role, "p-" + k, f"{n}, {place}")}
<main id="main"><section class="sec"><div class="wrap"><div class="kv reveal"><div><small>Luogo</small><b>{E(place)}</b></div><div><small>Tipo</small><b>{E(CAT[cat])}</b></div>{f'<div><small>Dimensione</small><b>{E(size.split(" · ")[0])}</b></div>' if cat == "new" else ""}<div><small>Stato</small><b>{E(status)}</b></div></div>
<div class="split"><div class="prose reveal"><span class="tag">Il lavoro</span><h2 style="margin-bottom:24px">{E(title)}</h2><p class="big">{E(role)}</p>
<p>Un progetto del Gruppo New Trends a {E(place)}. Il ruolo del gruppo è quello descritto su new-trends.ch. Per saperne di più o per un progetto simile, chiamaci al <a href="tel:{TEL}">{PHONE}</a>.</p>
{('<h3 style="font-size:1.2rem;margin-top:26px">Servizi collegati</h3><ul class="ticks">' + "".join(f'<li>{CHECK}<a href="servizio-{s[0]}.html">{E(s[1])}</a></li>' for s in svc_rel) + "</ul>") if svc_rel else ""}
<p style="margin-top:26px"><a class="btn g" href="preventivo.html">Hai un progetto simile? {AR}</a></p></div>{f'<div class="ph reveal">{T("p-" + k, f"{n}, {place}", S2)}</div>' if big("p-" + k) else f'<div class="get reveal"><span class="si">{G(ICONS["casa"])}</span><h2>In breve</h2><ul class="ticks"><li>{CHECK}<span>{E(size)}</span></li><li>{CHECK}<span>{E(place)}</span></li><li>{CHECK}<span>{E(role)}</span></li></ul></div>'}</div>
{f'<div style="margin-top:70px"><span class="tag">Prima e dopo</span><h2 style="margin-bottom:30px">Trascina il cursore.</h2><div class="ba two">{bas}</div></div>' if bas else ""}
<nav class="pn" aria-label="Altri lavori"><a href="{SLUG[prv]}"><small>← Lavoro precedente</small><b>{E(dtitle(prv))}</b></a><a href="{SLUG[nxt]}"><small>Lavoro successivo →</small><b>{E(dtitle(nxt))}</b></a></nav></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="revhead"><div><span class="tag">Altri lavori</span><h2>Guarda anche.</h2></div><a class="btn" href="lavori.html">Tutti i lavori {AR}</a></div>{work_cards(rel)}</div></section>
{cta()}{end}"""
        pages[SLUG[k]] = (f"{title} · Lavori · Edil Trend SA", f"{n} a {place}: {size}. {role}", body, False)

    # ---------- COME LAVORIAMO (qui vive la villa 3D) ----------
    how = f"""{header("how")}{hero_sm([("index.html", "Home"), (None, "Come lavoriamo")], "Come lavoriamo", "Niente stress e niente sorprese: un percorso chiaro in quattro passi, dalla prima idea alla consegna delle chiavi.", "proc", "Residenza Green Horse, Muzzano")}
<main id="main"><section class="dk proc" id="come"><div class="st"><div class="wrap" style="display:flex;flex-direction:column;flex:1;min-height:0;width:100%"><div class="head"><div><span class="tag">Scorri</span><h2>Guarda la casa che si costruisce.</h2></div><p class="lead">Un modello 3D di esempio: mentre scorri, la villa passa dal tracciamento alle luci della sera, come i quattro passi del nostro lavoro.</p></div>
<div class="steps"><i class="fill"></i>{st}</div>
<div class="stage3d" data-src="assets/villa3d.js?v=V3D" aria-label="Modello 3D di esempio: una villa che si costruisce mentre scorri le quattro fasi">{T("proc", "Residenza Green Horse, Muzzano", "100vw")}<div class="bar"><i></i></div><span class="cap3d">Sopralluogo e tracciamento · 0%</span><button class="b3d btn g" type="button">Guarda in 3D {AR}</button><input class="scrub" type="range" min="0" max="100" value="0" aria-label="Costruisci la casa: trascina"></div></div></div></section>
<section class="sec"><div class="wrap"><div class="head"><div><span class="tag">Passo per passo</span><h2>Cosa succede, e quando.</h2></div><p class="lead">Gli stessi quattro passi per un bagno e per una palazzina.</p></div>
<div class="wg" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">{stepcards}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap why"><div class="reveal"><span class="tag">Perché noi</span><h2>Un cantiere fatto di chiarezza e di mestiere.</h2><p class="lead" style="margin-top:18px">Prezzo, tempi e capitolato li firmiamo prima di aprire il cantiere.</p></div><div class="wg">{wy}</div></div></section>
{exp}{gap}{cta()}{end}"""
    pages["come-lavoriamo.html"] = ("Come lavoriamo · Edil Trend SA", "Sopralluogo, preventivo scritto, cantiere con un capocantiere, consegna: come lavora Edil Trend, con un modello 3D che si costruisce mentre scorri.", how, True)

    # ---------- ZONE ----------
    zl = "".join(f'<div class="reveal"><span class="no">{E(n)}</span><h3>{" · ".join(E(P[x][0]) for x in ks)}</h3><p>{"<br>".join(f"<a href=\"{SLUG[x]}\">{E(P[x][2])} →</a>" for x in ks)}</p></div>' for n, _, _, ks in Z)
    zone = f"""{header("zone")}{hero_sm([("index.html", "Home"), (None, "Zone")], "Zone", "Di casa nel Luganese: lavoriamo soprattutto qui e nel resto del Ticino.", "p-optima", "Residenza Optima, Montagnola")}
<main id="main"><section class="sec"><div class="wrap zones">{mapbox({n for n, _, _, _ in Z})}<div class="reveal"><span class="tag">Dove lavoriamo</span><h2>Vicini, conosciuti, a portata di mano.</h2><p class="lead" style="margin-top:16px">Questi sono alcuni dei comuni in cui il gruppo ha costruito o ristrutturato. Il tuo comune non c'è? Chiamaci: ti diciamo se possiamo seguirti.</p>
<ul class="places">{places}</ul><a class="btn" href="preventivo.html">Chiedi un sopralluogo {AR}</a></div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><span class="tag">Comune per comune</span><h2 style="margin-bottom:36px">I lavori del gruppo nella zona.</h2><div class="wg" style="grid-template-columns:repeat(auto-fill,minmax(240px,1fr))">{zl}</div></div></section>
{cta()}{end}"""
    pages["zone.html"] = ("Zone · Edil Trend SA", "Edil Trend lavora nel Luganese e nel resto del Ticino: Lugano, Tesserete, Vezia, Savosa, Muzzano, Collina d'Oro, Montagnola, Grancia, Magliaso.", zone, False)

    # ---------- DOMANDE ----------
    fq = "".join(f'<h3 class="reveal">{E(g)}</h3>{fqd(items, gi == 0)}' for gi, (g, items) in enumerate(FAQ))
    faqp = f"""{header("faq")}{hero_sm([("index.html", "Home"), (None, "Domande")], "Domande frequenti", "Preventivo, cantiere, permessi e zone: le risposte alle domande che ci fanno più spesso.", None, "")}
<main id="main"><section class="sec"><div class="wrap"><div class="faq">{fq}<p class="all lead" style="margin:40px auto 0">Non trovi la tua domanda? Chiamaci al <a href="tel:{TEL}">{PHONE}</a> o scrivici: risponde una persona.</p></div></div></section>
{cta()}{end}"""
    pages["domande.html"] = ("Domande frequenti · Edil Trend SA", "Preventivo, costi, cantiere, licenze e zone: le risposte di Edil Trend alle domande più frequenti.", faqp, False)

    # ---------- PREVENTIVO E CONTATTI ----------
    prev = f"""{header("prev")}{hero_sm([("index.html", "Home"), (None, "Preventivo e contatti")], "Preventivo e contatti", "Quattro domande, un minuto. Poi ti chiamiamo per fissare il sopralluogo, senza impegno.", "p-optima", "Residenza Optima, Montagnola")}
<main id="main"><section class="sec"><div class="wrap">{cfg}
<div class="contacts"><a class="reveal" href="tel:{TEL}"><small>Telefono</small><b>{PHONE}</b></a><a class="reveal" href="mailto:{MAIL}"><small>Email</small><b>{MAIL}</b></a><a class="reveal" href="https://wa.me/{WA}" target="_blank" rel="noopener"><small>WhatsApp</small><b>Scrivici un messaggio</b></a><div class="reveal"><small>Ufficio</small><b>{ADDR}</b></div></div>
<p class="note2">Le richieste arrivano all'ufficio del Gruppo New Trends a Lugano. Trattiamo i dati come spiegato nell'<a href="privacy.html">informativa privacy</a>.</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="faq"><span class="tag">Prima di scriverci</span><h2>Domande sul preventivo.</h2>{fqd(FAQ[0][1])}</div></div></section>{gap}{end}"""
    pages["preventivo.html"] = ("Preventivo e contatti · Edil Trend SA", "Richiedi un sopralluogo e un preventivo gratuito e senza impegno a Edil Trend SA, Lugano.", prev, False)

    pages["privacy.html"] = ("Privacy · Edil Trend SA", "Informativa privacy di Edil Trend SA.",
                             f'{header("")}<div style="height:104px;background:{TH["hdr"]};margin:8px 8px 0;border-radius:var(--r)"></div><main id="main">{b2.privacy("Edil Trend SA")}</main>{footer()}', False)

    v = hashlib.sha256((CSS + root_vars() + JS + open(os.path.join(HERE, "src", "villa3d.js")).read()).encode()).hexdigest()[:10]
    open(os.path.join(A, "site.css"), "w").write(root_vars() + CSS); open(os.path.join(A, "app.js"), "w").write("(function(){" + JS + "})();")
    for n, (t, d, body, three) in pages.items(): open(os.path.join(OUT, n), "w").write(page(t, d, body.replace("V3D", v), v, n, three))
    # vecchi indirizzi: continuano a funzionare
    for old, new in (("progetti.html", "lavori.html"), ("contatti.html", "preventivo.html")):
        open(os.path.join(OUT, old), "w").write(f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url={new}"><link rel="canonical" href="{new}"><a href="{new}">{new}</a>')
    open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
    print("ok", OUT, THEME, len(pages), "pagine")

if __name__ == "__main__":
    build()
