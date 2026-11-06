# -*- coding: utf-8 -*-
"""Archi Trend, versione 5: stile Lunarch (Urbanist, linee sottili, foto a tutta larghezza) su più pagine,
con piccoli modelli three.js da plastico (src/archi3d.js) e tre proposte di contrasto da far scegliere alla direzione.
Niente premi, recensioni, fondatore o numeri inventati: solo fatti del gruppo e progetti veri (b2.P).
Uso: python3 -E -s arch3.py [cartella]   ·   tema: ARCHI_THEME=a|attuale|b|c (predefinito "a" = Bianco caldo e nero, scelto dalla direzione)."""
import hashlib, os, shutil, sys
from PIL import Image
import build2 as b2
from build2 import E, P, ADDR, PHONE, TEL, MAIL, WA, SITES, find_src

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "architrend-v5")
THEME = os.environ.get("ARCHI_THEME", "a")   # <- l'unico interruttore del look (scelto dalla direzione: A · Bianco caldo e nero)
FONT = "https://fonts.googleapis.com/css2?family=Urbanist:wght@400..600&display=swap"
IMPORTMAP = ('<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"}}</script>')
AR = '<svg class="ar" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>'

# ---------- temi: colori per tono di sezione (ta / tb = sezioni alternate, tx = fascia d'accento, tf = piede) ----------
DARK = dict(bg="#0A0A0A", bg2="#171717", bg3="#262626", fg="#FFFFFF", mid="#A3A3A3", dim="#737373", line="#262626", acc="#B8962E")
DARK2 = dict(DARK, mid="#C4C4C4", dim="#9A9A9A", line="#2E2E2E", bg2="#1A1A1A", bg3="#2A2A2A")  # nero con testi più chiari
WARM = dict(bg="#F5F2EC", bg2="#FFFFFF", bg3="#EBE6DD", fg="#141414", mid="#45433F", dim="#66625B", line="#DDD7CC", acc="#8A6B1C")
STONE = dict(bg="#E6E1D8", bg2="#F3EFE8", bg3="#D8D2C6", fg="#1B1B1A", mid="#43413D", dim="#625E57", line="#CDC6B8", acc="#7E6328")
PAPER = dict(bg="#F3EFE8", bg2="#FFFFFF", bg3="#E6E1D8", fg="#1B1B1A", mid="#43413D", dim="#625E57", line="#DAD4C8", acc="#7E6328")
CHAR = dict(bg="#1F1F1D", bg2="#2A2A27", bg3="#363532", fg="#F4F1EB", mid="#CFCAC0", dim="#A29D93", line="#3A3935", acc="#C9A54C")
WHITE = dict(bg="#FAFAF7", bg2="#FFFFFF", bg3="#EEECE6", fg="#121212", mid="#474747", dim="#6A6A6A", line="#E2DFD7", acc="#2F6B62")
LGREY = dict(WHITE, bg="#F0EEE9", bg2="#FFFFFF", bg3="#E4E1DA")
GREEN = dict(bg="#2F6B62", bg2="#29605A", bg3="#245650", fg="#FFFFFF", mid="#DCE8E5", dim="#B3CCC7", line="#447D74", acc="#E2C877")
THEMES = {
    "attuale": dict(name="Attuale · nero", root=DARK, ta=DARK, tb=DARK, tx=DARK, tf=DARK),
    "a": dict(name="A · Bianco caldo e nero", root=DARK2, ta=WARM, tb=DARK2, tx=DARK2, tf=DARK2),
    "b": dict(name="B · Pietra e antracite", root=STONE, ta=STONE, tb=PAPER, tx=CHAR, tf=CHAR),
    "c": dict(name="C · Chiaro con verde Archi", root=WHITE, ta=WHITE, tb=LGREY, tx=GREEN, tf=dict(DARK, acc="#E2C877")),
}
T = THEMES[THEME]
LIGHT_ROOT = T["root"]["fg"] != "#FFFFFF"
def vars_(d): return ";".join(f"--{k}:{v}" for k, v in d.items())

CSS = b2.COMMON_CSS + f"""
:root{{{vars_(T['root'])}}}.ta{{{vars_(T['ta'])}}}.tb{{{vars_(T['tb'])}}}.tx{{{vars_(T['tx'])}}}.tf{{{vars_(T['tf'])}}}
.ta,.tb,.tx,.tf{{background:var(--bg);color:var(--fg)}}
""" + """
html{scroll-behavior:smooth}html.lenis,html.lenis body{height:auto}.lenis.lenis-smooth{scroll-behavior:auto!important}.lenis.lenis-stopped{overflow:hidden}html,body{overflow-x:clip}body{background:var(--bg);color:var(--fg);font:400 1.02rem/1.6 Urbanist,Arial,sans-serif;-webkit-font-smoothing:antialiased}
main{animation:pe .55s ease both}@keyframes pe{from{opacity:0}}
.wrap{max-width:1320px;margin:0 auto;padding:0 clamp(18px,4vw,84px)}
h1,h2,h3{font-family:Urbanist,Arial,sans-serif;font-weight:500;letter-spacing:-.02em;line-height:1.1;margin:0;text-wrap:balance}
h2{font-size:clamp(2rem,1.4rem + 2vw,3rem)}h3{font-weight:500}p{margin:0}.mid{color:var(--mid)}
section{position:relative}.sec{padding:clamp(72px,9vw,120px) 0;border-top:1px solid var(--line)}
.chip{display:inline-block;background:var(--bg3);color:var(--fg);font-weight:600;font-size:.82rem;letter-spacing:.04em;text-transform:uppercase;padding:7px 9px;margin-bottom:22px}
.lead{color:var(--mid);max-width:58ch;margin-top:16px;font-size:1.08rem}
.btn{display:inline-flex;align-items:center;gap:10px;background:var(--fg);color:var(--bg);padding:13px 24px;font:500 1rem Urbanist,Arial;text-decoration:none;border:1px solid var(--fg);cursor:pointer;transition:background .25s,color .25s}
.btn:hover{background:transparent;color:var(--fg)}.btn.ghost{background:transparent;color:var(--fg);border-color:var(--dim)}.btn.ghost:hover{border-color:var(--fg)}
.ar{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.8;transition:transform .3s;flex:none}.btn:hover .ar,a:hover>.ar,a:hover .ar{transform:translate(2px,-2px)}
.link{display:inline-flex;align-items:center;gap:8px;color:var(--fg);text-decoration:none;font-weight:500;border-bottom:1px solid var(--dim);padding-bottom:3px}.link:hover{border-color:var(--fg)}
/* header: trasparente sulla foto, pieno (senza sfocatura) quando scorri */
.hdr{position:fixed;top:0;left:0;right:0;z-index:60;transition:background .3s,border-color .3s;border-bottom:1px solid transparent;color:var(--fg)}
.hdr:not(.s){--fg:#fff;--bg:#0A0A0A;--dim:#ffffff80;--line:#ffffff30}.hdr.s{background:var(--bg);border-color:var(--line)}
.hdr .wrap{display:flex;align-items:center;gap:28px;height:70px}.logo{display:flex;align-items:center;text-decoration:none}.logo img{height:30px;width:auto}.logo .lk{display:none}
.nav{display:flex;gap:26px;margin-left:auto}.nav a{color:var(--fg);text-decoration:none;font-size:1rem;opacity:.86;position:relative;padding:4px 0}
.nav a::after{content:"";position:absolute;left:0;right:0;bottom:-2px;height:1px;background:currentColor;transform:scaleX(0);transform-origin:left;transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.nav a:hover,.nav a[aria-current]{opacity:1}.nav a:hover::after,.nav a[aria-current]::after{transform:none}
.hdr .btn{padding:9px 16px}.menu{display:none}
@media (max-width:1080px){.nav{display:none}.hdr .btn{margin-left:auto}.menu{display:inline-flex;background:none;border:1px solid var(--dim);color:var(--fg);padding:9px 14px;font:500 .95rem Urbanist;cursor:pointer}
 .nav.open{display:flex;flex-direction:column;position:absolute;top:70px;left:0;right:0;background:var(--bg);border-bottom:1px solid var(--line);padding:14px 20px 22px;gap:14px;animation:dd .3s ease}@keyframes dd{from{opacity:0;transform:translateY(-6px)}}.nav.open a{font-size:1.15rem}}
@media (max-width:420px){.hdr .btn{display:none}.menu{margin-left:auto}}
/* hero della home */
.hero{position:relative;min-height:100svh;display:flex;align-items:flex-end;isolation:isolate;overflow:hidden;color:#fff;background:#0A0A0A}
.hero>img,.phero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;animation:hz 2.4s cubic-bezier(.2,.7,.2,1) both}@keyframes hz{from{transform:scale(1.06)}}
.hero::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,#0A0A0A99 0%,#0A0A0A00 22%,#0A0A0A55 50%,#0A0A0Af5 100%),linear-gradient(90deg,#0A0A0Ab3 0%,#0A0A0A40 45%,#0A0A0A00 70%)}
.hero .wrap{width:100%;padding-bottom:clamp(40px,7vh,80px)}.hero h1{font-size:clamp(2.5rem,1.4rem + 3.6vw,4.2rem);max-width:15ch}
.hero p{max-width:56ch;margin:22px 0 32px;color:#E5E5E5;font-size:1.12rem}.acts{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.hero .btn,.phero .btn{--fg:#fff;--bg:#0A0A0A;--dim:#ffffff80}
.trust{display:flex;gap:10px 26px;flex-wrap:wrap;margin-top:34px;padding-top:20px;border-top:1px solid #ffffff2e;color:#D4D4D4;font-size:.95rem}.trust b{color:#fff;font-weight:600}
.up{opacity:0;transform:translateY(18px);animation:up .9s cubic-bezier(.2,.7,.2,1) forwards}.up.d1{animation-delay:.12s}.up.d2{animation-delay:.24s}.up.d3{animation-delay:.36s}@keyframes up{to{opacity:1;transform:none}}
/* testata delle pagine interne */
.phero{position:relative;min-height:min(64svh,620px);display:flex;align-items:flex-end;isolation:isolate;overflow:hidden;color:#fff;background:#141414}
.phero::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,#0A0A0Ab3 0%,#0A0A0A33 35%,#0A0A0Ae6 100%)}
.phero .wrap{width:100%;padding-top:110px;padding-bottom:clamp(34px,6vh,64px)}.phero h1{font-size:clamp(2.3rem,1.3rem + 3vw,3.8rem);max-width:20ch}.phero p{color:#E0E0E0;max-width:60ch;margin-top:16px;font-size:1.1rem}
.phero.short{min-height:300px}.phero .acts{margin-top:26px}
.crumbs{display:flex;flex-wrap:wrap;gap:6px;list-style:none;padding:0;margin:0 0 20px;font-size:.9rem;color:#CFCFCF}.crumbs li+li::before{content:"/";margin-right:6px;color:#8A8A8A}.crumbs a{color:#fff;text-decoration:none}.crumbs a:hover{text-decoration:underline}
/* introduzione e numeri */
.intro{text-align:center;max-width:820px;margin:0 auto}.intro p{font-size:clamp(1.35rem,1.1rem + .9vw,1.9rem);line-height:1.35;color:var(--fg)}.intro p span{color:var(--dim)}.intro .btn{margin-top:34px}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid var(--line);margin-top:60px}.stats div{padding:30px clamp(16px,2.4vw,32px);border-left:1px solid var(--line)}.stats div:first-child{border-left:0}
.stats b{display:block;font-size:2.2rem;font-weight:500;font-variant-numeric:tabular-nums}.stats span{color:var(--mid)}@media (max-width:800px){.stats{grid-template-columns:1fr 1fr}.stats div:nth-child(3){border-left:0}.stats div:nth-child(n+3){border-top:1px solid var(--line)}}
/* modello 3D */
.m3{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:clamp(30px,5vw,80px);align-items:center}@media (max-width:900px){.m3{grid-template-columns:1fr}}
.stage{position:relative;aspect-ratio:4/3;background:var(--bg2);border:1px solid var(--line);overflow:hidden;touch-action:pan-y;cursor:grab;outline:0}.stage.grab{cursor:grabbing}.stage:focus-visible{outline:2px solid var(--acc);outline-offset:3px}
.stage canvas{position:absolute;inset:0;width:100%!important;height:100%!important;display:block}.stage>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.stage.has3d>img{display:none}
.stage .hint{position:absolute;left:12px;bottom:12px;background:var(--bg);color:var(--fg);border:1px solid var(--line);font-size:.8rem;padding:6px 10px;pointer-events:none}.stage:not(.has3d) .hint{display:none}
.bul{list-style:none;padding:0;margin:26px 0 0;display:grid;gap:0;border-top:1px solid var(--line)}.bul li{padding:14px 0;border-bottom:1px solid var(--line);display:flex;gap:14px;align-items:center}.bul li b{color:var(--acc);font-weight:600;min-width:2ch}.bul a{text-decoration:none}.bul a:hover{text-decoration:underline}
/* servizi */
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}@media (max-width:980px){.cards{grid-template-columns:1fr 1fr}}@media (max-width:620px){.cards{grid-template-columns:1fr}}
.card{display:flex;flex-direction:column;background:var(--bg2);border:1px solid var(--line);text-decoration:none;color:var(--fg);transition:transform .45s cubic-bezier(.2,.7,.2,1),border-color .3s}.card:hover{transform:translateY(-4px);border-color:var(--dim)}
.card .ph{aspect-ratio:16/10;overflow:hidden;background:var(--bg3)}.card img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}.card:hover img{transform:scale(1.04)}
.card .t{padding:22px 22px 24px;display:flex;flex-direction:column;gap:10px;flex:1}.card small{color:var(--dim);font-size:.85rem;letter-spacing:.06em;text-transform:uppercase}.card h3{font-size:1.35rem}.card p{color:var(--mid)}.card .go{margin-top:auto;padding-top:10px;display:flex;align-items:center;gap:8px;font-weight:500}
/* lavori a tutta larghezza */
.wt{text-align:center;padding:clamp(60px,8vw,110px) 18px}.wt h2{font-size:clamp(2.2rem,1.4rem + 2.6vw,3.4rem)}.wt p{margin-top:14px}
.work{position:relative;display:block;height:min(80vh,760px);min-height:420px;overflow:hidden;color:#fff;text-decoration:none;isolation:isolate;background:#141414}
.work img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;transition:transform 1.6s cubic-bezier(.2,.7,.2,1)}.work:hover img{transform:scale(1.03)}
.work::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,#0A0A0A00 45%,#0A0A0Ad9 100%)}
.work .t{position:absolute;left:0;right:0;bottom:0}.work .wrap{padding-bottom:44px}.tags{display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap}.tags span{background:#0A0A0Aa6;color:#fff;font-size:.78rem;font-weight:600;letter-spacing:.06em;padding:5px 9px}
.work h3{font-size:clamp(1.8rem,1.3rem + 1.6vw,2.7rem)}.work p{color:#D4D4D4;margin-top:8px}.work .go{display:inline-flex;gap:8px;align-items:center;margin-top:16px;border-bottom:1px solid #ffffff80;padding-bottom:3px}
.after{display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;padding:34px 0}.after p{font-size:1.2rem}
/* griglia progetti con filtro */
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:28px}.tabs button{background:transparent;color:var(--fg);border:1px solid var(--line);padding:9px 16px;font:500 .95rem Urbanist;cursor:pointer;transition:border-color .25s,background .25s}.tabs button:hover{border-color:var(--fg)}.tabs button[aria-pressed=true]{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.pgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}@media (max-width:980px){.pgrid{grid-template-columns:1fr 1fr}}@media (max-width:620px){.pgrid{grid-template-columns:1fr}}
.pc{position:relative;display:block;aspect-ratio:4/3;overflow:hidden;color:#fff;text-decoration:none;isolation:isolate;background:#141414}.pc img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}.pc:hover img{transform:scale(1.05)}
.pc::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,#0A0A0A00 40%,#0A0A0Ae0 100%)}.pc .t{position:absolute;left:18px;right:18px;bottom:16px}.pc h3{font-size:1.3rem}.pc p{color:#D4D4D4;font-size:.95rem;margin-top:4px}.pc .tags{margin-bottom:10px}
.pc[hidden]{display:none}
/* scheda progetto */
.facts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.facts div{padding:22px clamp(14px,2vw,26px);border-left:1px solid var(--line)}.facts div:first-child{border-left:0}
.facts small{display:block;color:var(--dim);font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;margin-bottom:6px}.facts b{font-weight:500;font-size:1.1rem}
@media (max-width:800px){.facts{grid-template-columns:1fr 1fr}.facts div:nth-child(3){border-left:0}.facts div:nth-child(n+3){border-top:1px solid var(--line)}}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(30px,5vw,80px);align-items:start}@media (max-width:900px){.two{grid-template-columns:1fr}}
.big{font-size:clamp(1.3rem,1.1rem + .7vw,1.7rem);line-height:1.4}.note{font-size:.9rem;color:var(--dim);margin-top:18px}
.photo{width:100%;height:auto;background:var(--bg2)}
/* disegno e realtà, prima e dopo */
.ba{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}@media (max-width:980px){.ba{grid-template-columns:1fr 1fr}}@media (max-width:620px){.ba{grid-template-columns:1fr}}.ba.one{grid-template-columns:1fr;max-width:980px}
.cmp{position:relative;aspect-ratio:4/3;overflow:hidden;--x:50%;touch-action:pan-y;cursor:ew-resize;background:var(--bg2)}.cmp img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;pointer-events:none}.cmp .a{clip-path:inset(0 0 0 var(--x))}
.cmp .ln{position:absolute;top:0;bottom:0;left:var(--x);width:1px;background:#fff}.cmp .hd{position:absolute;top:50%;left:var(--x);width:44px;height:44px;border-radius:50%;background:#fff;color:#0A0A0A;transform:translate(-50%,-50%);display:grid;place-items:center;font-weight:600;letter-spacing:3px;transition:transform .25s}.cmp:hover .hd{transform:translate(-50%,-50%) scale(1.08)}
.cmp input{position:absolute;inset:0;width:100%;height:100%;opacity:0;margin:0;cursor:ew-resize}.cmp input:focus-visible+.hd{outline:2px solid var(--acc);outline-offset:3px}
.cmp .lb{position:absolute;top:12px;background:#0A0A0Ab3;color:#fff;font-size:.78rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:5px 9px;pointer-events:none}.cmp .l1{left:12px}.cmp .l2{right:12px}
.ba h3{font-size:1.15rem;margin-top:14px}.ba p{color:var(--dim);font-size:.95rem}
/* processo */
.steps4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid var(--line);list-style:none;padding:0;margin:40px 0 0}
.steps4 li{padding:26px clamp(14px,2vw,26px) 0;border-left:1px solid var(--line);display:grid;gap:10px;align-content:start}.steps4 li:first-child{border-left:0}.steps4 small{color:var(--acc);font-weight:600;letter-spacing:.06em}.steps4 h3{font-size:1.2rem}.steps4 p{color:var(--mid)}
@media (max-width:900px){.steps4{grid-template-columns:1fr 1fr}.steps4 li:nth-child(3){border-left:0}.steps4 li{padding-bottom:22px}}@media (max-width:520px){.steps4{grid-template-columns:1fr}.steps4 li{border-left:0;border-top:1px solid var(--line)}}
.morph{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:clamp(30px,5vw,80px);align-items:start}
.morph .stick{position:sticky;top:96px}.morph .stage{cursor:default;aspect-ratio:1/1}
.ph4 article{min-height:62vh;padding:30px 0;border-top:1px solid var(--line);opacity:.45;transition:opacity .5s}.ph4 article.on{opacity:1}.ph4 small{color:var(--acc);font-weight:600;letter-spacing:.06em}.ph4 h3{font-size:clamp(1.5rem,1.2rem + 1vw,2.1rem);margin:10px 0 14px}.ph4 p{color:var(--mid);max-width:50ch}.ph4 ul{color:var(--mid);padding-left:18px;margin:16px 0 0}.ph4 li{margin-bottom:6px}
.ph4 article:last-of-type{min-height:40vh}
@media (max-width:900px){.morph{grid-template-columns:1fr;gap:10px}.morph .stick{top:70px;z-index:2;background:var(--bg);padding:10px 0}.morph .stage{aspect-ratio:16/10}.ph4 article{min-height:48vh}}
/* perché noi */
.why{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border-top:1px solid var(--line);margin-top:50px}@media (max-width:760px){.why{grid-template-columns:1fr}}
.why div{padding:34px clamp(18px,2.4vw,34px);border-bottom:1px solid var(--line);transition:background .35s}.why div:hover{background:var(--bg2)}.why div:nth-child(odd){border-right:1px solid var(--line)}@media (max-width:760px){.why div:nth-child(odd){border-right:0}}
.why svg{width:30px;height:30px;stroke:var(--acc);fill:none;stroke-width:1.4}.why h3{font-size:1.3rem;margin:20px 0 10px}.why p{color:var(--mid)}
/* gruppo */
.quote{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:clamp(30px,5vw,70px);align-items:center}@media (max-width:900px){.quote{grid-template-columns:1fr}}
.quote blockquote{margin:0;font-size:clamp(1.6rem,1.2rem + 1.4vw,2.4rem);line-height:1.25}.quote p{color:var(--mid);margin-top:22px;max-width:54ch}.quote img{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover}
.chain{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border:1px solid var(--line);margin-top:34px;list-style:none;padding:0}
.chain li{border-left:1px solid var(--line)}.chain li:nth-child(odd){border-left:0}.chain li:nth-child(n+3){border-top:1px solid var(--line)}.chain a{display:grid;gap:6px;padding:20px;text-decoration:none;height:100%;transition:background .3s}.chain a:hover{background:var(--bg2)}.chain small{color:var(--dim)}.chain b{font-weight:500;font-size:1.1rem}.chain span{color:var(--mid);font-size:.93rem}
.chain .me a{background:var(--fg);color:var(--bg)}.chain .me span,.chain .me small{color:var(--bg);opacity:.75}
.dl{display:grid;grid-template-columns:auto 1fr;gap:12px 30px;margin:0;border-top:1px solid var(--line);padding-top:22px}.dl dt{color:var(--dim)}.dl dd{margin:0}
/* domande */
.faq{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.3fr);gap:clamp(30px,5vw,80px)}@media (max-width:900px){.faq{grid-template-columns:1fr}}.faq .mid{margin-top:16px;max-width:42ch}
.faq h3{font-size:.85rem;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin:34px 0 4px;font-weight:600}.faq h3:first-child{margin-top:0}
details.q{border-bottom:1px solid var(--line)}details.q summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:20px;padding:20px 0;font-size:1.08rem;font-weight:500;transition:color .25s}details.q summary:hover{color:var(--acc)}details.q summary::-webkit-details-marker{display:none}
details.q summary::after{content:"+";font-size:1.4rem;line-height:1;color:var(--mid);transition:transform .3s}details.q[open] summary::after{transform:rotate(45deg)}details.q p{color:var(--mid);padding:0 0 22px;max-width:62ch}
details.q[open] p{animation:qa .35s ease}@keyframes qa{from{opacity:0;transform:translateY(-4px)}}
/* contatti */
.ct{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.2fr);gap:clamp(30px,5vw,80px);align-items:start}@media (max-width:900px){.ct{grid-template-columns:1fr}}
.direct{display:grid;gap:12px;margin-top:30px}.direct a{display:flex;align-items:center;justify-content:space-between;gap:12px;border:1px solid var(--line);padding:16px 18px;text-decoration:none;transition:border-color .25s,background .25s}.direct a:hover{border-color:var(--fg);background:var(--bg2)}
.direct small{display:block;color:var(--dim);font-size:.82rem;letter-spacing:.06em;text-transform:uppercase}.direct b{font-weight:500;font-size:1.1rem}
.form{background:var(--bg2);border:1px solid var(--line);padding:clamp(20px,3vw,32px)}.form h3{font-size:1.3rem;margin-bottom:26px}
.form label{display:grid;gap:8px;font-size:.82rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--fg);margin-bottom:18px}
.form input,.form select,.form textarea{font:400 1rem Urbanist,Arial;color:var(--fg);background:var(--bg3);border:1px solid transparent;padding:13px 14px;width:100%;border-radius:0;text-transform:none;letter-spacing:0}
.form select{appearance:none;background-image:linear-gradient(45deg,transparent 50%,var(--mid) 50%),linear-gradient(135deg,var(--mid) 50%,transparent 50%);background-position:calc(100% - 20px) 50%,calc(100% - 15px) 50%;background-size:5px 5px;background-repeat:no-repeat}
.form input:focus,.form select:focus,.form textarea:focus{outline:0;border-color:var(--fg)}.form input::placeholder,.form textarea::placeholder{color:var(--dim)}
.form .row{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media (max-width:560px){.form .row{grid-template-columns:1fr}}
.radio{display:flex;gap:30px;margin:-6px 0 18px}.radio label{flex-direction:row;display:flex;align-items:center;gap:8px;text-transform:none;letter-spacing:0;font-size:1rem;font-weight:400;margin:0}.radio input{width:18px;height:18px;accent-color:var(--fg)}
.form .check{display:flex;gap:10px;text-transform:none;letter-spacing:0;font-size:.92rem;font-weight:400;color:var(--mid);align-items:flex-start}.form .check input{width:18px;height:18px;flex:none;margin-top:2px;accent-color:var(--fg)}.form .check a{color:var(--fg)}
.form .btn{width:100%;justify-content:center;margin-top:8px}.form [aria-invalid=true]{border-color:#E5484D}.form .err{color:#E5484D;font-weight:600;margin-bottom:10px}.form .ok h3{font-size:1.6rem;margin-bottom:10px}
/* invito finale */
.band{position:relative;min-height:440px;display:flex;align-items:flex-end;overflow:hidden;isolation:isolate;color:#fff;background:#141414}.band img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}
.band::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,#0A0A0Ae6,#0A0A0A33)}.band .wrap{width:100%;padding-bottom:56px}.band p{max-width:52ch;color:#D4D4D4;margin:14px 0 26px}.band .btn{--fg:#fff;--bg:#0A0A0A}
/* piede */
.ftr{border-top:1px solid var(--line);padding:70px 0 26px}.ftr .g{display:grid;grid-template-columns:1.3fr 1fr 1fr 1fr;gap:36px}@media (max-width:900px){.ftr .g{grid-template-columns:1fr 1fr}}@media (max-width:560px){.ftr .g{grid-template-columns:1fr}}
.ftr .logo img{height:64px}.ftr p{color:var(--mid);max-width:40ch;margin-top:16px}.ftr small{display:block;color:var(--dim);font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;margin:0 0 10px}.ftr ul{list-style:none;padding:0;margin:0;display:grid;gap:9px}
.ftr a{color:var(--fg);text-decoration:none}.ftr a:hover{text-decoration:underline;text-underline-offset:4px}.ftr .info{display:grid;gap:16px;align-content:start}.ftr .bt{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;border-top:1px solid var(--line);margin-top:56px;padding-top:22px;color:var(--dim);font-size:.92rem}
/* barra fissa sul telefono */
.mbar{display:none}@media (max-width:700px){.mbar{display:grid;grid-template-columns:1fr 1.4fr;gap:8px;position:fixed;left:10px;right:10px;bottom:calc(10px + env(safe-area-inset-bottom,0px));z-index:70;transition:transform .35s}
 .mbar a{display:flex;align-items:center;justify-content:center;gap:8px;padding:13px;font-weight:600;text-decoration:none;border:1px solid #fff}.mbar a:first-child{background:#0A0A0Af0;color:#fff}.mbar a:last-child{background:#fff;color:#0A0A0A;border-color:#0A0A0A}
 .mbar.hide{transform:translateY(140%)}.wa{display:none}body{padding-bottom:70px}}
.plain{max-width:820px;margin:0 auto;padding:70px 20px 80px}.plain h2{font-size:2rem;margin-bottom:20px}.plain p{color:var(--mid);margin-bottom:14px}.plain a{color:var(--fg)}.small{font-size:.86rem;color:var(--dim)}
.wa{background:#1F7A4D}
/* ---- animazioni di entrata: opacità + 14px, 500 ms, a scalare di 70 ms ---- */
.js .rv{opacity:0;transform:translateY(14px);transition:opacity .5s cubic-bezier(.2,.7,.2,1),transform .55s cubic-bezier(.2,.7,.2,1);transition-delay:var(--d,0ms)}
.js .rv.vis{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.js .rv{opacity:1!important;transform:none!important;transition:none!important}.up{opacity:1!important;transform:none!important}}
/* ---- round 2: strumenti per i contatti ---- */
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.btn:active,.opts button:active,.chips button:active,.ctl button:active{transform:scale(.97)}.btn{transition:background .25s,color .25s,transform .2s}
button.link{background:none;border:0;border-bottom:1px solid var(--dim);font:inherit;color:var(--fg);cursor:pointer;padding:0 0 3px}
.trust2{margin-top:22px;color:#CFCFCF;font-size:.95rem}.trust2 a{color:#fff}.band .btn{--dim:#ffffff80}
/* questionario */
.quiz{background:var(--bg2);border:1px solid var(--line);padding:clamp(22px,3vw,36px);position:relative;min-height:380px}
.qprog{height:2px;background:var(--line);margin-bottom:26px}.qprog i{display:block;height:100%;width:0;background:var(--acc);transition:width .5s cubic-bezier(.2,.7,.2,1)}
.qz{display:none}.qz.on{display:block;animation:qzin .4s cubic-bezier(.2,.7,.2,1)}@keyframes qzin{from{opacity:0;transform:translateX(14px)}}.qz:focus{outline:0}
.qz small{color:var(--acc);font-weight:600;letter-spacing:.06em;text-transform:uppercase;font-size:.8rem}.qz h3{font-size:clamp(1.35rem,1.1rem + .9vw,1.8rem);margin:10px 0 22px}
.opts{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px}.opts button{text-align:left;background:var(--bg3);color:var(--fg);border:1px solid transparent;padding:14px 16px;font:500 1rem Urbanist,Arial;cursor:pointer;transition:border-color .2s,background .2s,transform .2s}
.opts button:hover{border-color:var(--fg)}.opts button[aria-pressed=true]{background:var(--fg);color:var(--bg)}
.qin{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.qin input{flex:1 1 220px;font:400 1rem Urbanist,Arial;color:var(--fg);background:var(--bg3);border:1px solid transparent;padding:13px 14px}.qin input:focus{outline:0;border-color:var(--fg)}
.back{background:none;border:0;color:var(--mid);font:500 .95rem Urbanist;cursor:pointer;margin-top:20px;padding:0}.back:hover{color:var(--fg)}
.qres{list-style:none;padding:0;margin:0 0 18px;border-top:1px solid var(--line)}.qres li{display:flex;justify-content:space-between;gap:16px;padding:10px 0;border-bottom:1px solid var(--line)}.qres span{color:var(--dim)}.qres b{font-weight:500;text-align:right}
.qend .acts{margin-top:20px}
.qsum{border:1px solid var(--line);background:var(--bg3);padding:14px 16px;margin-bottom:20px}.qsum ul{margin:8px 0 10px;padding-left:18px;color:var(--mid)}.qsum b{font-weight:600}
/* checklist */
.ckl fieldset,fieldset.ckl,fieldset.radio{border:0;padding:0;margin:0 0 18px;min-width:0}.ckl legend,.radio legend{font-size:.82rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;margin-bottom:10px;padding:0;color:var(--fg)}
.ckg{display:grid;grid-template-columns:1fr 1fr;gap:8px}@media (max-width:560px){.ckg{grid-template-columns:1fr}}
.ck{display:flex!important;gap:10px;align-items:flex-start;background:var(--bg3);padding:11px 12px;cursor:pointer;text-transform:none!important;letter-spacing:0!important;font-weight:400!important;font-size:.95rem!important;margin:0!important;transition:background .2s}
.ck input{width:18px!important;height:18px;flex:none;margin:2px 0 0;accent-color:var(--fg);padding:0!important}.ck:has(input:checked){background:var(--line)}
div.ckl{background:var(--bg2);border:1px solid var(--line);padding:clamp(20px,3vw,30px)}.ckf{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;margin-top:6px}.ckn{color:var(--mid);font-variant-numeric:tabular-nums}
fieldset.radio{display:flex;flex-wrap:wrap;gap:10px 22px}fieldset.radio legend{width:100%;float:left}fieldset.radio label{flex-direction:row;display:flex;align-items:center;gap:8px;text-transform:none;letter-spacing:0;font-size:1rem;font-weight:400;margin:0}
/* fasi con dettagli */
.p3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:22px;border-top:1px solid var(--line);padding-top:18px}.p3 b{font-weight:600;font-size:.82rem;letter-spacing:.06em;text-transform:uppercase}.p3 ul{margin:10px 0 0;padding-left:16px;color:var(--mid);font-size:.95rem}
.ph4 .p3{grid-template-columns:1fr;gap:14px}.ph4 .p3 ul{columns:2;column-gap:24px}@media (max-width:560px){.ph4 .p3 ul{columns:1}}
.docs{counter-reset:d;list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}.docs li{counter-increment:d;padding:15px 0 15px 44px;border-bottom:1px solid var(--line);position:relative}.docs li::before{content:counter(d,decimal-leading-zero);position:absolute;left:0;color:var(--acc);font-weight:600}
/* modello 3D con comandi */
.ctl{display:none;flex-wrap:wrap;gap:8px;align-items:center;margin-top:12px}.m3d.on3d .ctl{display:flex}.ctl>span{color:var(--dim);font-size:.9rem;margin-right:4px}
.ctl button{background:transparent;color:var(--mid);border:1px solid var(--line);padding:7px 12px;font:500 .9rem Urbanist;cursor:pointer;transition:border-color .2s,color .2s,background .2s}.ctl button[aria-pressed=true]{color:var(--fg);border-color:var(--fg)}.ctl button:hover{color:var(--fg)}
.rng{display:flex;align-items:center;gap:10px;margin-left:auto;color:var(--mid);font-size:.9rem}.rng input{accent-color:var(--acc);width:140px}.rng output{min-width:4ch;font-variant-numeric:tabular-nums;color:var(--fg)}
/* domande: ricerca e argomenti */
.fsearch{display:grid;gap:8px;margin-bottom:16px}.fsearch label{font-size:.82rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase}
.fsearch input{font:400 1.05rem Urbanist,Arial;color:var(--fg);background:var(--bg2);border:1px solid var(--line);padding:14px 16px;width:100%}.fsearch input:focus{outline:0;border-color:var(--fg)}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}.chips button{background:transparent;color:var(--fg);border:1px solid var(--line);padding:7px 13px;font:500 .9rem Urbanist;cursor:pointer;transition:border-color .2s,background .2s}.chips button:hover{border-color:var(--fg)}.chips button[aria-pressed=true]{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.fcount{color:var(--dim);font-size:.9rem;margin-bottom:10px}.fgroup[hidden],details.q[hidden]{display:none}.fnone{margin-top:20px}
/* finestra "ti richiamiamo" */
dialog.cbd{border:0;padding:0;max-width:560px;width:calc(100% - 28px);color:var(--fg);background:transparent}dialog.cbd::backdrop{background:#000000a6}
dialog.cbd .form{position:relative}dialog.cbd[open]{animation:dlg .35s cubic-bezier(.2,.7,.2,1)}@keyframes dlg{from{opacity:0;transform:translateY(14px)}}
.x{position:absolute;top:10px;right:10px;width:38px;height:38px;border:1px solid var(--line);background:transparent;color:var(--fg);font-size:1.3rem;cursor:pointer;line-height:1}.x:hover{border-color:var(--fg)}
/* invito fisso sul computer */
.dcta{--fg:#fff;--bg:#0A0A0A;--dim:#ffffff66;--line:#ffffff2e;position:fixed;left:50%;bottom:18px;z-index:55;display:flex;align-items:center;gap:12px;background:#0A0A0Af2;color:#fff;border:1px solid #ffffff2e;padding:8px 8px 8px 18px;transform:translate(-50%,180%);transition:transform .45s cubic-bezier(.2,.7,.2,1);box-shadow:0 12px 30px #0006}
.dcta.show{transform:translate(-50%,0)}.dcta .btn{padding:9px 14px;font-size:.95rem}.dcta .x{position:static;width:34px;height:34px;border-color:transparent}.dcta span{white-space:nowrap}
@media (max-width:700px){.dcta{display:none}}
/* ---- senza JavaScript: tutto leggibile, moduli sostituiti da telefono/email/WhatsApp ---- */
.nojs{display:none;margin-top:14px;padding:12px 14px;border:1px solid var(--line);color:var(--mid)}.nojs a{color:var(--fg)}
html:not(.js) .nojs{display:block}html:not(.js) .reveal{opacity:1;transform:none}
html:not(.js) form[data-lead] button[type=submit],html:not(.js) [data-cb],html:not(.js) .quiz,html:not(.js) .tabs,html:not(.js) .fsearch,html:not(.js) .chips,html:not(.js) .fcount,html:not(.js) .ckf,html:not(.js) .g3d,html:not(.js) .dcta{display:none!important}
@media (max-width:1080px){html:not(.js) .menu{display:none}html:not(.js) .hdr{position:absolute}html:not(.js) .nav{display:flex;flex-wrap:wrap;gap:6px 16px;position:absolute;top:70px;left:0;right:0;padding:10px 18px;background:#0A0A0Ae6}}
/* ---- modalità leggera (computer e telefoni vecchi): niente 3D automatico, niente zoom, ombre o spostamenti; solo dissolvenze semplici ---- */
.g3d{display:none;position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#0A0A0Ae6;color:#fff;border:1px solid #ffffff59;padding:12px 18px;font:500 1rem Urbanist,Arial;cursor:pointer}.g3d:hover{background:#0A0A0A}
.lite .stage:not(.has3d) .g3d{display:inline-flex}.lite .stage{cursor:default}.lite .stage.has3d{cursor:grab}
.lite .up{transform:none;animation-name:fd}@keyframes fd{from{opacity:0}to{opacity:1}}
.lite .hero>img,.lite .phero>img{animation:none}.lite .qz.on,.lite dialog.cbd[open],.lite .nav.open{animation:fd .3s ease}
.lite .card.vis:hover{transform:none}.lite .card img,.lite .pc img,.lite .work img{transition:none;transform:none!important}html:not(.lite) .ph4 article.rv.vis:not(.on){opacity:.45}
.lite .wa,.lite .dcta,.lite .cmp .hd{box-shadow:none}.lite .dcta{transition:none}.lite *{backdrop-filter:none!important;-webkit-backdrop-filter:none!important}
"""
if LIGHT_ROOT: CSS += ".hdr.s .logo .lw{display:none}.hdr.s .logo .lk{display:block}\n"
# animazioni di entrata anche in modalità leggera (richiesta della direzione). Se sul suo PC scattano, mettere False:
ANIM_LITE = True
if not ANIM_LITE: CSS += ".lite .rv{opacity:1!important;transform:none!important;transition:none!important}\n"

JS = b2.COMMON_JS + r"""
var rm=matchMedia("(prefers-reduced-motion: reduce)").matches,H=document.documentElement,lite=H.classList.contains("lite");
// ---- animazioni di entrata (anche in modalità leggera; solo "riduci animazioni" le toglie) ----
var RV="main h2,main .chip,main .lead,main .big,main .intro p,main blockquote,main .note,main .faq .mid,main .wt p,.cards>*,.pgrid>*,.bul>li,.steps4>li,.why>div,.faq details.q,.faq .fgroup>h3,.facts>div,.stats>div,.docs>li,.chain>li,.ba>div,.direct>a,.dl,main .photo,.quote img,.quiz,main .form,div.ckl,.stage,.ph4 article,.work .t,.after,.band .wrap>*,main .acts,.tabs,.fsearch,.chips,.qsum,.m3d .ctl";
document.querySelectorAll(".reveal").forEach(function(x){x.classList.remove("reveal")});
var rvs=[];document.querySelectorAll(RV).forEach(function(x){if(x.closest(".hero,.phero,dialog")||(x.parentElement&&x.parentElement.closest(".rv")))return;x.classList.add("rv");rvs.push(x)});
rvs.forEach(function(x){var i=0,s=x.previousElementSibling;while(s){if(s.classList.contains("rv"))i++;s=s.previousElementSibling}if(i)x.style.setProperty("--d",Math.min(i,6)*70+"ms")});
function show(x){if(x.classList.contains("vis"))return;x.style.willChange="opacity,transform";x.classList.add("vis");setTimeout(function(){x.style.willChange=""},700+parseInt(x.style.getPropertyValue("--d")||0))}
H.classList.add("rv-ok");var seen=false;if(rm||!("IntersectionObserver" in window))rvs.forEach(show);
else{var rio=new IntersectionObserver(function(es){seen=true;es.forEach(function(e){if(e.isIntersecting){show(e.target);rio.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px",threshold:.08});rvs.forEach(function(x){rio.observe(x)});
 setTimeout(function(){if(!seen)rvs.forEach(show);else rvs.forEach(function(x){if(x.getBoundingClientRect().bottom<0)show(x)})},2500)}
// ---- scorrimento leggero a inerzia (Lenis), solo con mouse, non in modalità leggera né con "riduci animazioni" ----
var lenis=null,HDR=80;function goTo(el){if(lenis)lenis.scrollTo(el,{offset:-HDR});else el.scrollIntoView({behavior:rm?"auto":"smooth"})}
var nolenis=new URLSearchParams(location.search).get("lenis")==="0";
if(!lite&&!rm&&!nolenis&&!matchMedia("(pointer:coarse)").matches){addEventListener("load",function(){var s=document.createElement("script");s.src="https://cdn.jsdelivr.net/npm/lenis@1.3.27/dist/lenis.min.js";s.defer=true;s.onload=function(){if(!window.Lenis||H.classList.contains("lite"))return;
 lenis=new window.Lenis({lerp:.1,smoothWheel:true,syncTouch:false});window.__lenis=lenis;function rf(t){lenis.raf(t);requestAnimationFrame(rf)}requestAnimationFrame(rf);
 document.addEventListener("archi-lite",function(){lenis.destroy();lenis=null})};document.head.appendChild(s)})}
document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(!a||a.getAttribute("href").length<2)return;var t=document.getElementById(a.getAttribute("href").slice(1));if(!t)return;e.preventDefault();goTo(t);if(a.classList.contains("skip"))t.setAttribute("tabindex","-1"),t.focus({preventScroll:true})});
if(location.hash.length>1)addEventListener("load",function(){var t=document.getElementById(location.hash.slice(1));if(t)setTimeout(function(){window.scrollTo(0,t.getBoundingClientRect().top+scrollY-HDR)},50)});
var hd=document.querySelector(".hdr");function hs(){hd.classList.toggle("s",scrollY>30)}addEventListener("scroll",hs,{passive:true});hs();
// cursore disegno/realtà e prima/dopo
document.querySelectorAll(".cmp").forEach(function(c){var r=c.querySelector("input");function set(v){c.style.setProperty("--x",v+"%")}r.addEventListener("input",function(){set(r.value)});
 var down=false;function mv(e){var b=c.getBoundingClientRect();var x=Math.max(0,Math.min(100,(e.clientX-b.left)/b.width*100));r.value=x;set(x)}
 c.addEventListener("pointerdown",function(e){down=true;mv(e)});addEventListener("pointerup",function(){down=false});c.addEventListener("pointermove",function(e){if(down)mv(e)})});
// numeri veri che contano quando si vedono
document.querySelectorAll("[data-count]").forEach(function(b){if(rm||lite)return;var to=+b.dataset.count,from=+(b.dataset.from||0),suf=b.dataset.suf||"";b.textContent=from+suf;
 new IntersectionObserver(function(es,o){if(!es[0].isIntersecting)return;o.disconnect();var t0=0;function f(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/1400);b.textContent=Math.round(from+(to-from)*(1-Math.pow(1-k,3)))+suf;if(k<1)requestAnimationFrame(f)}requestAnimationFrame(f)},{threshold:.6}).observe(b)});
// progetti: filtro
document.querySelectorAll(".tabs button").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll(".tabs button").forEach(function(x){x.setAttribute("aria-pressed",x===b)});var f=b.dataset.f;document.querySelectorAll(".pc[data-f]").forEach(function(w){w.hidden=!!f&&w.dataset.f!==f})})});
// processo: fase attiva
var ph=document.querySelectorAll(".ph4 article");if(ph.length){var po=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)ph.forEach(function(a){a.classList.toggle("on",a===e.target)})})},{rootMargin:"-40% 0px -50% 0px"});ph.forEach(function(a){po.observe(a)})}
// modelli 3D: three.js si carica solo quando un modello è vicino allo schermo
// in modalità leggera niente three.js: resta la foto con il pulsante "Guarda in 3D"
var t3=document.querySelectorAll("[data-3d]"),l3=false;function load3d(){if(l3)return;l3=true;var s=document.createElement("script");s.type="module";s.src="assets/archi3d.js?v=V3D";document.body.appendChild(s)}
if(t3.length&&!lite){var lo=new IntersectionObserver(function(es){if(!es.some(function(e){return e.isIntersecting}))return;lo.disconnect();if(!H.classList.contains("lite"))load3d()},{rootMargin:"500px"});t3.forEach(function(x){lo.observe(x)})}
document.querySelectorAll("[data-g3d]").forEach(function(b){b.addEventListener("click",function(e){e.stopPropagation();var st=b.closest("[data-3d]");st.classList.add("want3d");b.textContent="Caricamento…";window.A3D_DEMAND=true;if(window.A3D)window.A3D(st);else load3d()})});
// primi fotogrammi lenti (computer vecchio): passa alla modalità leggera e ferma il 3D
var forced=null;try{forced=sessionStorage.getItem("atlite")}catch(e){}
if(!lite&&forced!=="0")addEventListener("load",function(){setTimeout(function(){var n=0,t0=0;function f(t){if(!t0)t0=t;if(++n<11)return requestAnimationFrame(f);if((t-t0)/10>50){H.classList.add("lite");lite=true;try{sessionStorage.setItem("atlite","1")}catch(e){}document.dispatchEvent(new Event("archi-lite"))}}requestAnimationFrame(f)},300)});
// barra del telefono: sparisce quando il modulo è già sullo schermo
var mb2=document.querySelector(".mbar"),fm=document.querySelector("#modulo");if(mb2&&fm)new IntersectionObserver(function(es){mb2.classList.toggle("hide",es[0].isIntersecting)},{threshold:.15}).observe(fm);
// ---- memoria breve della visita (questionario e documenti), solo nel browser ----
function sg(k){try{return JSON.parse(sessionStorage.getItem(k)||"null")}catch(e){return null}}function ss(k,v){try{v==null?sessionStorage.removeItem(k):sessionStorage.setItem(k,JSON.stringify(v))}catch(e){}}
// ---- tutti i moduli: stessa validazione, campi in più messi nel messaggio come righe "Etichetta: valore" ----
function valOf(x){if(x.tagName==="FIELDSET")return [].map.call(x.querySelectorAll("input:checked"),function(i){return i.value}).join("; ");return String(x.value||"").trim()}
document.querySelectorAll("form[data-lead]").forEach(function(f){f.addEventListener("submit",function(e){e.preventDefault();var bad=[],er=f.querySelector(".err");
 f.querySelectorAll("[aria-invalid]").forEach(function(x){x.removeAttribute("aria-invalid")});
 f.querySelectorAll("[required]").forEach(function(x){if(x.type==="checkbox"?!x.checked:!String(x.value).trim()){bad.push(x);x.setAttribute("aria-invalid","true")}});
 var em=f.email?f.email.value.trim():"",ph=f.phone?f.phone.value.trim():"",msg="Servono i campi segnati e il consenso.";
 if(f.dataset.need==="phone"){if(!ph){bad.push(f.phone);f.phone.setAttribute("aria-invalid","true");msg="Servono nome, telefono e il consenso."}}
 else if(!em&&!ph){bad.push(f.phone||f.email);(f.phone||f.email).setAttribute("aria-invalid","true");msg="Servono nome, telefono o email e il consenso."}
 if(em&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)){bad.push(f.email);f.email.setAttribute("aria-invalid","true");msg="Controlla l'indirizzo email."}
 if(ph&&ph.replace(/\D/g,"").length<7){bad.push(f.phone);f.phone.setAttribute("aria-invalid","true");msg="Controlla il numero di telefono."}
 if(bad.length){er.hidden=false;er.textContent=msg;bad[0].focus();return}
 var lines=[];f.querySelectorAll("[data-l]").forEach(function(x){var v=valOf(x);if(v)lines.push(x.dataset.l+": "+v)});
 if(f.hasAttribute("data-main")){var q=sg("atq");if(q&&q.length){lines.push("Dal questionario:");q.forEach(function(a){lines.push(a[0]+": "+a[1])})}}
 var kind=(f.kind&&f.kind.value)||f.dataset.kind||"Altro";
 var d={company:"architrend",name:f.name.value.trim(),email:em,phone:ph,kind:kind,town:f.town?f.town.value.trim():"",message:[f.message?f.message.value.trim():""].concat(lines).filter(Boolean).join("\n"),website:f.website.value,consent:true,newsletter:!!(f.newsletter&&f.newsletter.checked)};
 var box=f.parentNode;box.innerHTML="<div class='ok' tabindex='-1'><h3>Invio in corso…</h3></div>";box.querySelector(".ok").focus();
 sendReq(d,box.querySelector(".ok"),kind==="Richiamata"?"<h3>Grazie, ti richiamiamo.</h3><p class='mid'>Una persona dello studio ti chiama al numero che ci hai lasciato.</p>":"<h3>Grazie, abbiamo ricevuto la tua richiesta.</h3><p class='mid'>Un architetto di Archi Trend ti richiama per fissare il primo incontro.</p>","Archi Trend · "+kind+"\n"+d.name+" "+d.email+" "+d.phone+"\n"+d.town+"\n"+d.message);
 if(f.hasAttribute("data-main")){ss("atq",null);ss("atd",null)}})});
// ---- questionario "Che progetto hai?" ----
var mainF=document.querySelector("form[data-main]");
function fillMain(){if(!mainF)return;var q=sg("atq"),sum=document.querySelector(".qsum");if(q&&q.length){q.forEach(function(a){if(a[0]==="Tipo di progetto")[].forEach.call(mainF.kind.options,function(o){if(o.text===a[1])o.selected=true});if(a[0]==="Comune"&&!mainF.town.value)mainF.town.value=a[1]});
  if(sum){sum.hidden=false;sum.querySelector("ul").innerHTML=q.map(function(a){return "<li>"+a[0]+": <b>"+a[1].replace(/</g,"&lt;")+"</b></li>"}).join("")}}else if(sum)sum.hidden=true;
 var dd=sg("atd")||[];mainF.querySelectorAll(".ckl input").forEach(function(c){if(dd.indexOf(c.value)>=0)c.checked=true})}
fillMain();var qc=document.querySelector("[data-qclear]");if(qc)qc.addEventListener("click",function(){ss("atq",null);fillMain()});
document.querySelectorAll("[data-quiz]").forEach(function(z){var st=z.querySelectorAll(".qz"),bar=z.querySelector(".qprog i"),ans={},cur=0;
 function show(i){cur=i;st.forEach(function(x,j){x.classList.toggle("on",j===i)});bar.style.width=(i/(st.length-1)*100)+"%";
  if(i===st.length-1){var arr=[];st.forEach(function(x){var l=x.dataset.l;if(l&&ans[l])arr.push([l,ans[l]])});ss("atq",arr);z.querySelector(".qres").innerHTML=arr.map(function(a){return "<li><span>"+a[0]+"</span><b>"+a[1].replace(/</g,"&lt;")+"</b></li>"}).join("")||"<li>Nessuna risposta</li>";st[i].focus({preventScroll:true})}}
 st.forEach(function(x,i){x.querySelectorAll(".opts button").forEach(function(b){b.addEventListener("click",function(){x.querySelectorAll(".opts button").forEach(function(o){o.setAttribute("aria-pressed",o===b)});ans[x.dataset.l]=b.dataset.v;setTimeout(function(){show(i+1)},rm?0:220)})});
  var inp=x.querySelector(".qin input");function nx(){if(inp.value.trim())ans[x.dataset.l]=inp.value.trim();else delete ans[x.dataset.l];show(i+1)}
  if(inp){x.querySelector("[data-next]").addEventListener("click",nx);x.querySelector("[data-skip]").addEventListener("click",function(){inp.value="";nx()});inp.addEventListener("keydown",function(e){if(e.key==="Enter"){e.preventDefault();nx()}})}
  var bk=x.querySelector("[data-back]");if(bk)bk.addEventListener("click",function(){show(i-1)})});
 z.querySelector("[data-qreset]").addEventListener("click",function(){ans={};z.querySelectorAll(".opts button").forEach(function(o){o.removeAttribute("aria-pressed")});show(0)});
 z.querySelector("[data-qgo]").addEventListener("click",function(e){if(mainF){e.preventDefault();fillMain();goTo(document.getElementById("modulo"));setTimeout(function(){mainF.name.focus({preventScroll:true})},rm?0:500)}});show(0)});
// ---- checklist dei documenti ----
document.querySelectorAll("[data-ckl]").forEach(function(c){var bx=c.querySelectorAll("input"),n=c.querySelector(".ckn"),dd=sg("atd")||[];bx.forEach(function(b){b.checked=dd.indexOf(b.value)>=0});
 function up(){var v=[].filter.call(bx,function(b){return b.checked}).map(function(b){return b.value});ss("atd",v);n.textContent=v.length+" di "+bx.length}bx.forEach(function(b){b.addEventListener("change",up)});up()});
// ---- "ti richiamiamo noi": finestra con il modulo breve ----
var dlg=document.getElementById("richiamata");document.querySelectorAll("[data-cb]").forEach(function(b){b.addEventListener("click",function(){if(dlg&&dlg.showModal){dlg.showModal();if(lenis)lenis.stop();var i=dlg.querySelector("input[name=name]");if(i)i.focus()}else location.href="contatti.html"})});
if(dlg){dlg.addEventListener("close",function(){if(lenis)lenis.start()});dlg.querySelector("[data-cbclose]").addEventListener("click",function(){dlg.close()});dlg.addEventListener("click",function(e){if(e.target===dlg)dlg.close()})}
// ---- invito fisso sul computer: compare dopo il primo schermo, sparisce vicino ai moduli e al fondo, si può chiudere ----
var dc=document.querySelector(".dcta");if(dc){var near=0,closed=sg("atx");function dv(){dc.classList.toggle("show",!closed&&!near&&scrollY>innerHeight*.9)}
 var nio=new IntersectionObserver(function(es){es.forEach(function(e){e.target._v=e.isIntersecting});near=[].some.call(document.querySelectorAll(".exit,.form,.ftr,.quiz"),function(x){return x._v});dv()});document.querySelectorAll(".exit,.form,.ftr,.quiz").forEach(function(x){nio.observe(x)});
 addEventListener("scroll",dv,{passive:true});dc.querySelector("[data-dx]").addEventListener("click",function(){closed=true;ss("atx",true);dv()})}
// ---- domande: ricerca e argomenti ----
var fq=document.getElementById("fq");if(fq){var chips=document.querySelectorAll(".chips button"),topic="",cnt=document.querySelector(".fcount"),none=document.querySelector(".fnone");
 function nrm(t){return t.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"")}
 function run(){var q=nrm(fq.value.trim()),n=0;document.querySelectorAll(".fgroup").forEach(function(g){var vis=0;g.querySelectorAll("details").forEach(function(d){var ok=(!topic||g.dataset.t===topic)&&(!q||nrm(d.textContent).indexOf(q)>=0);d.hidden=!ok;if(ok)vis++});g.hidden=!vis;n+=vis});
  cnt.textContent=n===1?"1 domanda":n+" domande";none.hidden=n>0}
 fq.addEventListener("input",run);chips.forEach(function(b){b.addEventListener("click",function(){chips.forEach(function(x){x.setAttribute("aria-pressed",x===b)});topic=b.dataset.t;run()})})}
var pk=new URLSearchParams(location.search).get("tipo");if(mainF&&pk){[].forEach.call(mainF.kind.options,function(o){if(o.text===pk)o.selected=true})}
"""

NAV = [("studio.html", "Studio", "studio"), ("servizi.html", "Servizi", "servizi"), ("progetti.html", "Progetti", "progetti"), ("processo.html", "Processo", "processo"), ("domande.html", "Domande", "domande"), ("contatti.html", "Contatti", "contatti")]

def logo(full=False, dark_ok=True):
    f = "architrend-logo-bianco.webp" if full else "architrend-logo-bianco-corto.webp"
    k = f.replace("bianco", "scuro"); w, h = (458, 128) if full else (292, 60)  # file ridotti al doppio della misura mostrata
    return (f'<a class="logo" href="index.html" aria-label="Archi Trend SA, home"><img class="lw" src="assets/{f}" alt="Archi Trend SA" width="{w}" height="{h}">'
            + (f'<img class="lk" src="assets/{k}" alt="" width="{w}" height="{h}" loading="lazy">' if dark_ok and LIGHT_ROOT else "") + '</a>')

def header(cur):
    return (f'<header class="hdr"><div class="wrap">{logo()}<nav class="nav" aria-label="Principale">'
            + "".join(f'<a href="{h}"{" aria-current=page" if k == cur else ""}>{t}</a>' for h, t, k in NAV)
            + f'</nav><a class="btn" href="contatti.html">Prenota una consulenza</a><button class="menu" data-menu aria-expanded="false" aria-label="Apri il menu">Menu</button></div></header>')

def crumbs(items):
    li = "".join(f'<li><a href="{h}">{E(t)}</a></li>' if h else f'<li aria-current="page">{E(t)}</li>' for h, t in [("index.html", "Home")] + items)
    return f'<nav aria-label="Percorso"><ol class="crumbs">{li}</ol></nav>'

def phero(img, crumb, title, lead="", acts="", short=False):
    return (f'<section class="phero{" short" if short else ""}">{img}<div class="wrap">{crumbs(crumb)}<h1 class="up">{title}</h1>'
            + (f'<p class="up d1">{lead}</p>' if lead else "") + (f'<div class="acts up d2">{acts}</div>' if acts else "") + "</div></section>")

def footer():
    links = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t, _ in NAV)
    return f"""<footer class="ftr tf"><div class="wrap"><div class="g"><div>{logo(True, False)}<p>Studio di architettura del Gruppo New Trends a Lugano: progettazione, licenze edilizie, direzione lavori, perizie e interni.</p></div>
<div><small>Il sito</small><ul><li><a href="index.html">Home</a></li>{links}<li><a href="privacy.html">Privacy</a></li></ul></div>
<div class="info"><div><small>Telefono</small><a href="tel:{TEL}">{PHONE}</a></div><div><small>Email</small><a href="mailto:{MAIL}">{MAIL}</a></div><div><small>Studio</small>{ADDR}</div></div>
<div><small>Il gruppo</small><ul><li><a href="{SITES['newtrends']}">New Trends · Immobiliare</a></li><li><a href="{SITES['architrend']}">Archi Trend · Architettura</a></li><li><a href="{SITES['ediltrend']}">Edil Trend · Costruzioni</a></li></ul></div></div>
<div class="bt"><span>© Archi Trend SA · Parte del Gruppo New Trends</span><span>Lugano, Svizzera</span></div></div></footer>"""

# modalità leggera per computer e telefoni vecchi: pochi core, poca memoria, risparmio dati, "riduci animazioni" o ?lite=1 (?lite=0 la toglie)
LITE_HEAD = ('<script>(function(h){if(!("IntersectionObserver" in window))return;h.classList.add("js");setTimeout(function(){if(!h.classList.contains("rv-ok"))h.classList.remove("js")},2500);try{var n=navigator,l=new URLSearchParams(location.search).get("lite"),s=sessionStorage;'
             'if(l==="1"||l==="0")s.setItem("atlite",l);var f=s.getItem("atlite");'
             'var a=(n.hardwareConcurrency&&n.hardwareConcurrency<=4)||(n.deviceMemory&&n.deviceMemory<=4)||(n.connection&&n.connection.saveData)||matchMedia("(prefers-reduced-motion: reduce)").matches;'
             'if(f==="1"||(f!=="0"&&a))h.classList.add("lite")}catch(e){}})(document.documentElement)</script>')

def page(title, desc, body, v, cur):
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="{T['root']['bg']}">
{LITE_HEAD}<link rel="icon" href="favicon.png" type="image/png">{b2.FONTS}<link rel="preload" as="style" href="{FONT}" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="{FONT}"></noscript><link rel="stylesheet" href="assets/site.css?v={v}">{IMPORTMAP}</head>
<body><a class="skip" href="#main">Vai al contenuto</a>{header(cur)}{body}{footer()}<a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Scrivici su WhatsApp">WhatsApp</a>
<div class="mbar"><a href="tel:{TEL}">Chiama</a><a href="contatti.html">Prenota una consulenza</a></div>{callback_dialog()}{dcta()}
<script src="assets/app.js?v={v}" defer></script></body></html>"""

ICON = {"misura": '<path d="M3 17 17 3l4 4L7 21H3zM14 6l4 4M10 10l2 2M7 13l2 2"/>', "chiaro": '<path d="M4 5h16v11H8l-4 4z"/><path d="M8 9h8M8 12h5"/>',
        "calma": '<path d="M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z"/><path d="m8 12 3 3 5-6"/>', "tempi": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/>'}

# ---------- contenuti ----------
SERV = [  # slug, titolo, breve, foto (progetto, "bp" o ritaglio), preset 3D, testo, cosa comprende, progetti collegati, tipo nel modulo
    ("progettazione", "Progettazione residenziale", "Case, ville e palazzine pensate su misura per il terreno, per chi ci abiterà e per il valore dell'immobile nel tempo.",
     ("optima", None), "residenziale",
     "Partiamo dal terreno, dalle regole del Comune e da chi abiterà la casa. Studiamo volumi, orientamento e viste, poi sviluppiamo piante, facciate e materiali fino al progetto definitivo. Lavorando nel Gruppo New Trends progettiamo con uno sguardo al mercato: ogni scelta deve sostenere il valore dell'immobile.",
     ["Studio del terreno e delle possibilità edificatorie", "Studio dei volumi e prime varianti", "Progetto di massima con stima dei costi", "Progetto definitivo: piante, sezioni e facciate", "Scelta dei materiali e delle finiture"], ["optima", "greenhorse", "aurea"], "Nuova casa o villa"),
    ("licenze", "Licenze e domanda di costruzione", "Prepariamo la documentazione e seguiamo la domanda di costruzione con il Comune, fino alla licenza.",
     ("greenhorse", "bp"), "licenze",
     "Ogni intervento deve rispettare il piano regolatore e le norme edilizie del Comune e del Cantone. Verifichiamo cosa si può costruire, prepariamo i piani e i documenti della domanda e restiamo il riferimento per il Comune durante la procedura, comprese le richieste di completamento e le eventuali opposizioni.",
     ["Verifica del piano regolatore e delle norme", "Piani e documenti per la domanda di costruzione", "Contatti con l'ufficio tecnico comunale", "Risposte alle richieste di completamento", "Supporto in caso di opposizioni"], ["ferrari", "miracolli", "greenhorse"], "Licenza o domanda di costruzione"),
    ("direzione-lavori", "Direzione lavori", "Seguiamo il cantiere fino alla consegna, con Edil Trend o con l'impresa che scegli tu.",
     ("ferrari", None), "direzione",
     "La direzione lavori controlla che il cantiere segua il progetto, i costi e i tempi concordati. Coordiniamo imprese e artigiani, verifichiamo la qualità delle opere e teniamo informato il committente fino al collaudo e alla consegna. Possiamo lavorare con Edil Trend, l'impresa generale del gruppo, o con l'impresa che preferisci.",
     ["Appalti e confronto delle offerte", "Programma dei lavori e riunioni di cantiere", "Controllo di qualità, costi e tempi", "Coordinamento di imprese e artigiani", "Collaudo e consegna"], ["ferrari", "synthesis", "maraini"], "Altro"),
    ("perizie", "Perizie e valutazioni tecniche", "Valutazioni dello stato di un immobile per chi deve comprare, vendere, ristrutturare o investire.",
     ("magliaso", (0, .06, .5, .94)), "perizie",
     "Prima di comprare, vendere o ristrutturare conviene sapere com'è davvero un immobile. Visitiamo l'edificio, controlliamo lo stato delle parti visibili e i documenti disponibili e ti consegniamo una valutazione tecnica chiara, con gli interventi da considerare. Con New Trends, la fiduciaria immobiliare del gruppo, la valutazione tecnica si può affiancare a quella di mercato.",
     ["Sopralluogo e rilievo dello stato", "Verifica dei documenti disponibili", "Interventi necessari e priorità", "Rapporto scritto e chiaro", "Su richiesta, con la valutazione di mercato di New Trends"], ["magliaso", "corteglia", "motta"], "Perizia"),
    ("ristrutturazioni", "Ristrutturazioni", "Progetti che ridanno qualità e valore a case, appartamenti e stabili esistenti.",
     ("montagnola", (.5, .5, 1, 1)), "ristrutturazioni",
     "Ristrutturare significa lavorare con ciò che esiste: struttura, impianti, vincoli e spesso persone che ci abitano. Rileviamo lo stato, proponiamo cosa conviene cambiare e cosa tenere e seguiamo autorizzazioni e cantiere. Il gruppo ha ristrutturato e valorizzato palazzine, ville e appartamenti nel Luganese.",
     ["Rilievo dello stato esistente", "Proposte di intervento e stima dei costi", "Autorizzazioni, se necessarie", "Direzione lavori", "Valorizzazione per vendita o affitto, con il gruppo"], ["magliaso", "montagnola", "pregassona"], "Ristrutturazione"),
    ("interni", "Interni", "Spazi, luce e materiali degli ambienti, dalla distribuzione delle stanze alle finiture.",
     ("pregassona", None), "interni",
     "Gli interni decidono come si vive una casa ogni giorno. Studiamo la distribuzione degli spazi, la luce, cucine e bagni, materiali e finiture, in un nuovo progetto o in una ristrutturazione, con disegni chiari per scegliere con calma prima del cantiere.",
     ["Distribuzione degli spazi", "Cucine e bagni", "Materiali, colori e finiture", "Luce naturale e illuminazione", "Disegni per l'esecuzione"], ["pregassona", "motta", "montagnola"], "Interni"),
]
STEPS = [("Ascolto e sopralluogo", "Ci incontriamo, visitiamo il terreno o l'immobile e mettiamo in chiaro esigenze, budget e tempi. Il primo incontro è senza impegno.",
          ["Le tue esigenze e il budget", "Visita del terreno o dell'immobile", "Prima verifica delle norme"]),
         ("Concept", "Prime idee, volumi e materiali: ti mostriamo come potrebbe essere, con una stima dei costi già dall'inizio.", ["Studio dei volumi", "Varianti da confrontare", "Stima dei costi"]),
         ("Progetto e licenza", "Sviluppiamo il progetto definitivo e seguiamo la domanda di costruzione con il Comune.", ["Progetto definitivo", "Domanda di costruzione", "Rapporti con il Comune"]),
         ("Direzione lavori e consegna", "Seguiamo il cantiere fino alla consegna, con Edil Trend o con l'impresa che preferisci.", ["Appalti e programma", "Controllo di qualità, costi e tempi", "Collaudo e consegna"])]
WHY = [("misura", "Progetti su misura per te", "Ogni pianta, materiale e dettaglio parte da come vivi e da cosa ti serve davvero, non da un modello già pronto."),
       ("chiaro", "Chiarezza a ogni passo", "Dal primo incontro alla consegna sai sempre a che punto siamo, cosa viene dopo e perché."),
       ("calma", "Un percorso senza stress", "Coordiniamo noi tecnici, Comune e impresa: tu prendi le decisioni importanti, al resto pensiamo noi."),
       ("tempi", "Tempi e costi sotto controllo", "Progettiamo con uno sguardo al mercato e al budget, per evitare ritardi e spese che non servono.")]
FAQ = [  # (id, argomento, [(domanda, risposta)]) · risposte prudenti: il Comune e il Cantone decidono, niente prezzi né date promesse
    ("inizio", "Primo passo", [
        ("Quanto costa il primo incontro?", "Il primo incontro è senza impegno: ascoltiamo il progetto, guardiamo insieme terreno o immobile e ti diciamo come possiamo aiutarti."),
        ("Quando conviene coinvolgere l'architetto?", "Il prima possibile, idealmente prima di comprare il terreno o l'immobile: così sai subito cosa si può costruire e quali costi aspettarti."),
        ("Cosa devo portare al primo incontro?", "Quello che hai: indirizzo o numero di mappale, l'estratto del registro fondiario, eventuali piani esistenti, foto, idee e un'idea del budget. Se non hai ancora nulla va bene lo stesso."),
        ("Potete lavorare su un progetto che ho già?", "Sì. Possiamo rivedere, completare o sviluppare un progetto esistente, mantenendo l'idea di partenza."),
        ("Cosa succede dopo che vi ho scritto?", "Ti richiamiamo per conoscere il progetto e fissare un primo incontro, in studio a Lugano o sul posto. Poi ti proponiamo come procedere, con un'offerta scritta per le prestazioni che ti servono.")]),
    ("terreno", "Terreno e fattibilità", [
        ("Posso sapere cosa si può costruire prima di comprare un terreno?", "Sì. Verifichiamo piano regolatore, zona, indici, distanze e vincoli e, in genere con un primo studio dei volumi, ti diciamo cosa ci si può realizzare. È il momento migliore per coinvolgerci."),
        ("Cosa sono gli indici di sfruttamento e di occupazione?", "Sono valori fissati dal piano regolatore del Comune: limitano quanta superficie si può costruire e quanta parte del terreno si può occupare. Insieme a distanze e altezze definiscono il volume possibile."),
        ("Cosa serve per uno studio di fattibilità?", "Di solito basta l'indirizzo o il numero di mappale. Sono utili anche l'estratto del registro fondiario, eventuali servitù conosciute e le tue idee su cosa vorresti costruire."),
        ("Il terreno è in pendenza: è un problema?", "Non necessariamente: molte case nel Luganese sono su un pendio. Cambiano accessi, scavi e muri, e quindi i costi: li valutiamo già nello studio iniziale."),
        ("Cosa sono servitù e vincoli?", "Sono diritti o limiti che pesano su un terreno: iscritti a registro fondiario, come un diritto di passo, oppure previsti dalle norme, come distanze o protezione del paesaggio. Possono cambiare il progetto, per questo li verifichiamo all'inizio.")]),
    ("licenza", "Licenza edilizia", [
        ("Vi occupate anche della domanda di costruzione?", "Sì, prepariamo la documentazione e seguiamo la domanda di costruzione con il Comune fino alla licenza."),
        ("Quali documenti servono per la domanda di costruzione?", "In genere il modulo ufficiale, i piani del progetto (situazione, piante, sezioni e facciate), l'estratto del piano catastale, il calcolo degli indici e una relazione tecnica; secondo l'intervento anche documenti su energia, antincendio o smaltimento delle acque. L'elenco esatto lo stabiliscono il Comune e il Cantone."),
        ("Che differenza c'è tra domanda di costruzione e notifica?", "Per interventi di poca importanza può bastare una procedura semplificata, la notifica; per gli altri serve la domanda ordinaria. Quale procedura vale lo stabiliscono le norme e il Comune: te lo diciamo dopo aver visto il progetto."),
        ("La domanda viene pubblicata?", "Di solito la domanda ordinaria viene pubblicata e i vicini possono consultarla e fare opposizione entro il termine previsto. In molti casi vanno posate anche le modine, le sagome che mostrano il volume sul terreno."),
        ("Cosa succede se un vicino fa opposizione?", "Ti spieghiamo cosa contesta, valutiamo con te se e come adattare il progetto e seguiamo la risposta nella procedura comunale."),
        ("Chi firma i piani della domanda?", "I piani vengono firmati da te come committente e dal progettista. Se il terreno non è ancora tuo, di solito serve anche il consenso del proprietario.")]),
    ("costi", "Costi e onorari", [
        ("Come si calcolano gli onorari dell'architetto?", "Di solito per fasi di prestazione, dal progetto preliminare alla direzione lavori, spesso con riferimento alle norme SIA. L'onorario può essere una percentuale sul costo dell'opera, un importo forfettario o a tempo: si concorda nell'offerta scritta, prima di iniziare."),
        ("Mi dite subito quanto costerà costruire?", "Già nella fase di concept ti diamo una stima dei costi, che diventa più precisa man mano che il progetto si definisce. I prezzi definitivi arrivano dalle offerte delle imprese."),
        ("Quali costi ci sono oltre a costruzione e onorari?", "In genere tasse comunali per la licenza, allacciamenti, eventuali specialisti come ingegnere civile o geologo, assicurazioni e, se compri, le spese notarili e di registro. Te le elenchiamo nella stima, così non arrivano a sorpresa."),
        ("Posso affidarvi solo una parte del lavoro?", "Sì: puoi chiederci solo lo studio di fattibilità, solo il progetto e la licenza, solo la direzione lavori o una perizia. L'offerta indica con chiarezza cosa comprende.")]),
    ("tempi", "Tempi", [
        ("Quanto tempo serve per ottenere la licenza?", "Dipende dal Comune, dal tipo di intervento e da eventuali opposizioni o richieste di completamento. Dopo aver visto il progetto ti diamo una stima realistica, senza promettere date che non dipendono da noi."),
        ("Da cosa dipendono i tempi del progetto?", "Dalle decisioni da prendere insieme, dalla complessità dell'intervento, dagli specialisti coinvolti, dalla procedura comunale e dalla disponibilità delle imprese. Un programma chiaro aiuta a tenerli sotto controllo."),
        ("Quanto dura il cantiere?", "Dipende da dimensione, tipo di costruzione e stagione. Il programma dei lavori dettagliato lo prepariamo con l'impresa prima dell'inizio e lo aggiorniamo durante il cantiere.")]),
    ("ristrutturazione", "Ristrutturazione", [
        ("Serve una licenza per ristrutturare?", "Dipende dall'intervento: lavori interni senza modifiche importanti spesso seguono una procedura semplice o nessuna, mentre cambi di facciata, volume, destinazione o struttura in genere richiedono una domanda. Lo verifichiamo con te e con il Comune."),
        ("Si può ristrutturare abitando in casa?", "A volte sì, organizzando il cantiere per zone o per fasi. Dipende dai lavori: te lo diciamo dopo il sopralluogo."),
        ("Conviene ristrutturare o demolire e ricostruire?", "Dipende dallo stato dell'edificio, dalle norme di oggi e dai costi. Con un rilievo dello stato e una stima delle due strade ti aiutiamo a confrontarle."),
        ("Fate perizie prima di un acquisto?", "Sì: visitiamo l'immobile, controlliamo lo stato delle parti visibili e i documenti disponibili e ti diamo una valutazione tecnica chiara, con gli interventi da considerare.")]),
    ("gruppo", "Cantiere e gruppo", [
        ("Dovete costruire per forza con Edil Trend?", "No. Con Edil Trend hai un solo gruppo dal progetto alle chiavi, ma possiamo dirigere i lavori anche con l'impresa che scegli tu."),
        ("Chi sceglie le imprese?", "Tu, sulla base delle offerte che raccogliamo e confrontiamo con te. In alternativa puoi affidare tutta l'opera a Edil Trend, l'impresa generale del gruppo."),
        ("Cosa fa la direzione lavori?", "Controlla che il cantiere segua progetto, costi e tempi, coordina imprese e artigiani, verifica la qualità delle opere e ti tiene informato fino alla consegna."),
        ("Che legame avete con New Trends ed Edil Trend?", "Siamo aziende dello stesso gruppo, con sede in Via Pretorio 11 a Lugano: New Trends per la consulenza e l'intermediazione immobiliare, Archi Trend per la progettazione, Edil Trend per la costruzione. Puoi affidarci tutto il percorso o solo una parte."),
        ("Posso vendere o affittare l'immobile finito con il gruppo?", "Sì, se lo desideri: New Trends, la fiduciaria immobiliare del gruppo, segue vendita, affitto e il dopo."),
        ("In quali zone lavorate?", "Soprattutto nel Luganese e nel resto del Ticino.")]),
]
FQ = {i: items for i, _, items in FAQ}
def fqpick(*keys): return [FQ[t][n] for t, n in keys]
DOCS = ["Estratto del registro fondiario", "Indirizzo o numero di mappale", "Piani esistenti dell'immobile", "Foto del terreno o dell'immobile", "Idee, riferimenti o foto di case che ti piacciono", "Un budget indicativo", "Un progetto o uno studio precedente"]
DOMANDA = ["Modulo ufficiale della domanda di costruzione", "Piano di situazione ed estratto del piano catastale", "Piante, sezioni e facciate del progetto", "Calcolo degli indici (sfruttamento, occupazione) e delle distanze", "Relazione tecnica", "Secondo l'intervento: documenti su energia, antincendio, smaltimento delle acque", "In molti casi: modine (sagome) posate sul terreno"]
DOPO = [("Ti richiamiamo", "Ti chiamiamo per conoscere il progetto e capire da dove partire."), ("Primo incontro", "In studio a Lugano o sul posto, senza impegno: guardiamo insieme terreno, immobile o idea."),
        ("Proposta scritta", "Ti diciamo cosa serve, in quali fasi e ti mandiamo un'offerta scritta per le prestazioni."), ("Si parte", "Se decidi di andare avanti, iniziamo dalla fase che ti serve: anche solo una.")]
QUIZ = [("Tipo di progetto", "Che progetto hai in mente?", ["Nuova casa o villa", "Palazzina o residenza", "Ristrutturazione", "Interni", "Perizia", "Licenza o domanda di costruzione", "Altro"]),
        ("Terreno o immobile", "Hai già il terreno o l'immobile?", ["Sì, è già mio", "Sto per comprarlo", "Lo sto ancora cercando", "Non serve (interni o perizia)"]),
        ("Comune", "In quale Comune?", None),
        ("Budget indicativo", "Che budget hai in mente, tutto compreso?", ["Fino a CHF 500'000", "CHF 500'000 – 1 milione", "CHF 1 – 2 milioni", "Oltre CHF 2 milioni", "Non lo so ancora"]),
        ("Tempi", "Quando vorresti iniziare?", ["Il prima possibile", "Entro 6 mesi", "Entro un anno", "Sto solo valutando"])]
KINDS = ["Nuova casa o villa", "Palazzina o residenza", "Ristrutturazione", "Interni", "Perizia", "Licenza o domanda di costruzione", "Altro"]
SFAQ = {"progettazione": (("terreno", 0), ("terreno", 1), ("costi", 0)), "licenze": (("licenza", 1), ("licenza", 2), ("licenza", 3), ("tempi", 0)),
        "direzione-lavori": (("gruppo", 2), ("gruppo", 1), ("tempi", 2)), "perizie": (("ristrutturazione", 3), ("costi", 3), ("terreno", 4)),
        "ristrutturazioni": (("ristrutturazione", 0), ("ristrutturazione", 1), ("ristrutturazione", 2)), "interni": (("inizio", 3), ("costi", 3), ("ristrutturazione", 1))}
LABEL3D = {"residenziale": "una villa su due piani con piscina", "licenze": "il volume dentro la sagoma ammessa e il confine del terreno", "direzione": "un edificio in costruzione con la gru",
           "perizie": "un edificio esistente in sezione", "ristrutturazioni": "una casa esistente con il nuovo ampliamento", "interni": "una stanza in spaccato con gli arredi"}
ORDER = ["ferrari", "greenhorse", "optima", "synthesis", "maraini", "miracolli", "aurea", "duelaghi", "fortuna", "magliaso", "corteglia", "motta", "pregassona", "montagnola"]

PHASES = [  # per ogni fase: cosa succede, cosa ricevi, cosa ti chiediamo
    (["Primo incontro in studio o sul posto", "Visita del terreno o dell'immobile", "Prima verifica di piano regolatore e vincoli"],
     ["Una prima valutazione di cosa si può fare", "La proposta di come procedere", "Un'offerta scritta per le prestazioni"],
     ["Indirizzo o numero di mappale", "Estratto del registro fondiario, se ce l'hai", "Piani esistenti, foto, idee e budget indicativo"]),
    (["Studio dei volumi sul terreno", "Varianti da confrontare insieme", "Prime scelte di materiali e spazi"],
     ["Schizzi, volumi e piante di massima", "Una prima stima dei costi", "Le varianti messe a confronto"],
     ["Le tue priorità e le scelte tra le varianti", "Un riscontro sul budget"]),
    (["Progetto definitivo e coordinamento con gli specialisti", "Preparazione della domanda di costruzione", "Rapporti con il Comune durante la procedura"],
     ["Piani completi del progetto", "Il dossier della domanda", "Aggiornamenti sullo stato della procedura"],
     ["Firma dei piani e della domanda", "Le scelte su materiali e finiture"]),
    (["Raccolta e confronto delle offerte delle imprese", "Programma dei lavori e riunioni di cantiere", "Controllo di qualità, costi e tempi fino al collaudo"],
     ["Il confronto delle offerte", "Programma e verbali di cantiere", "Collaudo e consegna dell'opera"],
     ["L'approvazione delle offerte e dei contratti", "Le decisioni che servono durante il cantiere"]),
]

NOJS = (f'<p class="nojs">Il modulo ha bisogno di JavaScript. Puoi scriverci o chiamarci: <a href="tel:{TEL}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a> · <a href="https://wa.me/{WA}">WhatsApp</a></p>')

def ul(items): return "<ul>" + "".join(f"<li>{E(x)}</li>" for x in items) + "</ul>"

def dopo_html(tone="tb"):
    li = "".join(f'<li class="reveal"><small>{i + 1:02d}</small><h3>{E(t)}</h3><p>{E(d)}</p></li>' for i, (t, d) in enumerate(DOPO))
    return (f'<section class="sec {tone}"><div class="wrap"><span class="chip">Dopo il primo contatto</span><h2>Cosa succede dopo che ci contatti</h2>'
            f'<p class="lead">Nessun impegno finché non hai un\'offerta scritta e chiara.</p><ol class="steps4">{li}</ol>'
            f'<div class="acts" style="margin-top:36px"><a class="btn" href="contatti.html">Prenota una consulenza gratuita {AR}</a><button type="button" class="btn ghost" data-cb>Ti richiamiamo noi</button></div></div></section>')

def quiz_html():
    steps = []
    for i, (lab, q, opts) in enumerate(QUIZ):
        head = f'<small>Domanda {i + 1} di {len(QUIZ)}</small><h3>{E(q)}</h3>'
        if opts: body = '<div class="opts">' + "".join(f'<button type="button" data-v="{E(o)}">{E(o)}</button>' for o in opts) + "</div>"
        else: body = ('<div class="qin"><label class="sr" for="qz-town">Comune</label><input id="qz-town" placeholder="es. Lugano, Collina d\'Oro, Tesserete" autocomplete="address-level2">'
                      '<button type="button" class="btn" data-next>Avanti</button><button type="button" class="link" data-skip>Salta</button></div>')
        back = '<button type="button" class="back" data-back>← Indietro</button>' if i else ""
        steps.append(f'<div class="qz{" on" if i == 0 else ""}" data-l="{E(lab)}">{head}{body}{back}</div>')
    end = ('<div class="qz qend" tabindex="-1"><small>Fatto</small><h3>Ecco il tuo progetto, in breve</h3><ul class="qres"></ul>'
           '<p class="mid">Lo alleghiamo alla richiesta: così al primo contatto sappiamo già da dove partire.</p>'
           f'<div class="acts"><a class="btn" href="contatti.html#modulo" data-qgo>Continua con la richiesta {AR}</a><button type="button" class="btn ghost" data-qreset>Ricomincia</button></div></div>')
    return (f'<div class="quiz reveal" data-quiz aria-live="polite"><div class="qprog" aria-hidden="true"><i></i></div>{"".join(steps)}{end}</div>')

def checklist_html(in_form=False):
    boxes = "".join(f'<label class="ck"><input type="checkbox" value="{E(d)}"><span>{E(d)}</span></label>' for d in DOCS)
    if in_form:
        return f'<fieldset class="ckl" data-l="Documenti già disponibili"><legend>Cosa hai già? (facoltativo)</legend><div class="ckg">{boxes}</div></fieldset>'
    return (f'<div class="ckl reveal" data-ckl><fieldset><legend>Spunta quello che hai già</legend><div class="ckg">{boxes}</div></fieldset>'
            f'<div class="ckf"><span class="ckn" aria-live="polite">0 di {len(DOCS)}</span><a class="btn" href="contatti.html#modulo" data-ckgo>Invia la lista con la richiesta {AR}</a></div>'
            '<p class="note">Non serve avere tutto: ci basta sapere da dove partiamo.</p></div>')

def domanda_html(tone="tb"):
    return (f'<section class="sec {tone}"><div class="wrap two"><div class="reveal"><span class="chip">Domanda di costruzione</span><h2>I documenti che di solito servono</h2>'
            '<p class="lead">L\'elenco esatto lo stabiliscono il Comune e il Cantone, secondo il tipo di intervento. Li prepariamo noi: a te chiediamo soprattutto firme, documenti di proprietà e decisioni.</p></div>'
            '<ol class="docs reveal">' + "".join(f"<li>{E(d)}</li>" for d in DOMANDA) + "</ol></div></section>")

def consent(): return ('<input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">'
                       '<label class="check"><input type="checkbox" name="consent" required><span>Acconsento a essere ricontattato da Archi Trend SA secondo l\'<a href="privacy.html">informativa privacy</a>.</span></label>')

RLAB = {"Quando preferisci?": "Fascia oraria preferita", "Cosa vorresti costruire?": "Destinazione", "Il terreno è già tuo?": "Terreno già di proprietà", "Hai già lavorato con un architetto?": "Ha già lavorato con un architetto"}
def radios(label, name, opts):
    return (f'<fieldset class="radio" data-l="{E(RLAB.get(label, label))}"><legend>{E(label)}</legend>' + "".join(f'<label><input type="radio" name="{name}" value="{E(o)}">{E(o)}</label>' for o in opts) + "</fieldset>")

def fattib_html(tone="tb"):
    return f"""<section class="sec {tone}" id="fattibilita"><div class="wrap ct"><div class="reveal"><span class="chip">Fattibilità del terreno</span><h2>Cosa si può costruire sul tuo terreno?</h2>
<p class="lead">Mandaci Comune e dati principali: verifichiamo piano regolatore, zona, indici e vincoli e ti richiamiamo per spiegarti cosa ci si può fare. Meglio farlo prima di comprare.</p>
<ul class="bul"><li><b>01</b>Zona e indici del piano regolatore</li><li><b>02</b>Distanze, altezze e vincoli</li><li><b>03</b>Un primo volume possibile</li></ul></div>
<div class="form reveal"><h3>Richiedi una verifica di fattibilità</h3><form novalidate action="javascript:void 0" data-lead data-kind="Fattibilità del terreno">
<div class="row"><label>Comune del terreno<input name="town" placeholder="es. Muzzano" required></label><label>Superficie (m², se la sai)<input data-l="Superficie del terreno (m²)" inputmode="numeric" placeholder="es. 800"></label></div>
<label>Numero di mappale (facoltativo)<input data-l="Numero di mappale" placeholder="es. 1234"></label>
{radios("Cosa vorresti costruire?", "dest", ["Casa unifamiliare", "Più appartamenti", "Non lo so ancora"])}
{radios("Il terreno è già tuo?", "own", ["Sì", "Sto per comprarlo", "Lo sto cercando"])}
<div class="row"><label>Nome e cognome<input name="name" autocomplete="name" required></label><label>Telefono<input name="phone" type="tel" autocomplete="tel"></label></div>
<label>Email<input name="email" type="email" autocomplete="email"></label>{consent()}
<p class="err" hidden role="alert"></p>{NOJS}<button class="btn" type="submit">Richiedi la verifica {AR}</button></form></div></div></section>"""

def callback_dialog():
    return f"""<dialog class="cbd ta" id="richiamata" data-lenis-prevent aria-labelledby="cbt"><div class="form"><button type="button" class="x" data-cbclose aria-label="Chiudi">×</button><h3 id="cbt">Ti richiamiamo noi</h3><p class="mid" style="margin:-14px 0 20px">Lasciaci il numero e quando preferisci: ti chiamiamo per una prima chiacchierata, senza impegno.</p>
<form novalidate action="javascript:void 0" data-lead data-kind="Richiamata" data-need="phone"><div class="row"><label>Nome e cognome<input name="name" autocomplete="name" required></label><label>Telefono<input name="phone" type="tel" autocomplete="tel" placeholder="+41 79 000 00 00"></label></div>
{radios("Quando preferisci?", "slot", ["Mattina", "Mezzogiorno", "Pomeriggio", "Indifferente"])}
<label>Di cosa vuoi parlare? (facoltativo)<input data-l="Argomento" placeholder="es. terreno a Tesserete, ristrutturazione"></label>{consent()}
<p class="err" hidden role="alert"></p>{NOJS}<button class="btn" type="submit">Richiamatemi {AR}</button></form></div></dialog>"""

def dcta():
    return ('<div class="dcta" role="complementary" aria-label="Prenota una consulenza"><span>Primo incontro <b>senza impegno</b></span><a class="btn" href="contatti.html">Prenota una consulenza</a>'
            '<button type="button" class="btn ghost" data-cb>Ti richiamiamo noi</button><button type="button" class="x" data-dx aria-label="Nascondi">×</button></div>')

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    A = os.path.join(OUT, "assets"); I = os.path.join(A, "img"); os.makedirs(I)
    cache = {}
    def im(name, src, widths=(480, 960, 1600), box=None):
        if name not in cache: cache[name] = b2.rimg(src, I, name, widths, box)
        return cache[name]
    pr = lambda k: find_src(P[k][4]); bpf = lambda k, s: os.path.join(b2.BP, P[k][4][:40] + f"-{s}.jpg")
    has_bp = lambda k: os.path.exists(bpf(k, "bp"))
    tag = b2.imgtag
    # loghi: bianchi originali + versione scura ricolorata dallo stesso file (per le sezioni chiare)
    for f, hh in (("architrend-logo-bianco.png", 128), ("architrend-logo-bianco-corto.png", 60)):
        lg = Image.open(os.path.join(HERE, "src", "logo", f)).convert("RGBA"); lg = lg.resize((round(lg.width * hh / lg.height), hh), Image.LANCZOS)
        lg.save(os.path.join(A, f.replace(".png", ".webp")), "WEBP", lossless=True, method=6)
        px = lg.load()
        for y in range(lg.height):
            for x in range(lg.width):
                r, g, b, a = px[x, y]
                if a: px[x, y] = tuple(int(22 + (255 - c) * .8) for c in (r, g, b)) + (a,)
        lg.save(os.path.join(A, f.replace("bianco", "scuro").replace(".png", ".webp")), "WEBP", lossless=True, method=6)
    Image.open(os.path.join(HERE, "src", "logo", "architrend-icona.png")).resize((64, 64), Image.LANCZOS).save(os.path.join(OUT, "favicon.png"), optimize=True)
    shutil.copy(os.path.join(HERE, "src", "archi3d.js"), os.path.join(A, "archi3d.js"))

    SZ_FULL, SZ_CARD, SZ_HALF = "100vw", "(max-width:620px) 100vw, (max-width:980px) 50vw, 420px", "(max-width:900px) 100vw, 50vw"
    def stage(preset, fb, alt, label, hint="Trascina per ruotare"):
        return (f'<div class="stage" data-3d="{preset}" tabindex="0" role="img" aria-label="{E(label)}">{tag(fb, alt, SZ_HALF)}'
                + (f'<span class="hint">{hint}</span>' if hint else "") + '<button type="button" class="g3d" data-g3d>Guarda in 3D</button></div>')
    def kind(k): return "Ristrutturazione" if P[k][5] == "ren" else "Nuova costruzione"
    def status(k): return "In costruzione" if "in costruzione" in P[k][2] else "Realizzato"
    def size(k): return P[k][2].replace(" · in costruzione", "")
    def nm(k): return P[k][0] + (" a " + P[k][1] if P[k][0] in ("Palazzina", "Appartamento", "Villa") else "")
    def pcard(k):
        return (f'<a class="pc reveal" href="progetto-{k}.html" data-f="{P[k][5]}">{tag(im("p-" + k, pr(k)), nm(k) + ", " + P[k][1], SZ_CARD)}'
                f'<div class="t"><div class="tags"><span>{kind(k).upper()}</span><span>{status(k).upper()}</span></div><h3>{E(nm(k) if P[k][5] == "ren" else P[k][0])}</h3><p>{E(P[k][1])} · {E(size(k))}</p></div></a>')
    def slider(k, mode):
        if mode == "bp": a, b, l1, l2 = im(f"bp-{k}", bpf(k, "bp"), (480, 960)), im(f"ph-{k}", bpf(k, "ph"), (480, 960)), "Disegno", "Realtà"
        elif k == "magliaso": a, b, l1, l2 = im("m-pre", pr(k), (480,), (0, .06, .5, .94)), im("m-post", pr(k), (480,), (.5, .06, 1, .94)), "Prima", "Dopo"
        else: a, b, l1, l2 = im("mo-pre", pr(k), (350,), (.5, 0, 1, .5)), im("mo-post", pr(k), (350,), (.5, .5, 1, 1)), "Prima", "Dopo"
        return (f'<div class="cmp">{tag(a, nm(k) + ": " + l1.lower(), SZ_CARD)}{tag(b, nm(k) + ": " + l2.lower(), SZ_CARD, cls="a")}<span class="ln"></span><span class="lb l1">{l1}</span><span class="lb l2">{l2}</span>'
                f'<input type="range" min="0" max="100" value="50" aria-label="Confronta {l1.lower()} e {l2.lower()}: {E(nm(k))}"><span class="hd" aria-hidden="true">‹›</span></div>')
    def cta(sub="Diamo forma alla tua idea", text="Il primo incontro è senza impegno: raccontaci terreno, immobile o idea e ti diciamo come possiamo aiutarti."):
        return (f'<section class="band exit">{tag(im("band", pr("aurea"), (640, 820, 980)), "", SZ_FULL)}<div class="wrap reveal"><span class="chip">{E(sub)}</span><h2>Prenota una consulenza gratuita</h2><p>{text}</p>'
                f'<div class="acts"><a class="btn" href="contatti.html">Prenota la consulenza {AR}</a><button type="button" class="btn ghost" data-cb>Ti richiamiamo noi</button></div>'
                f'<p class="trust2">Senza impegno · <a href="tel:{TEL}">{PHONE}</a> · {ADDR}</p></div></section>')
    def faqblock(items): return "".join(f'<details class="q"{" open" if i == 0 else ""}><summary>{E(q)}</summary><p>{E(a)}</p></details>' for i, (q, a) in enumerate(items))
    def svc_img(p): return im("s-" + SERVSLUG[p], bpf(p[0], "bp") if p[1] == "bp" else pr(p[0]), (480, 900), p[1] if isinstance(p[1], tuple) else None)
    SERVSLUG = {s[3]: s[0] for s in SERV}
    chain = b2.chain("architrend", "chain")
    stats = ('<div class="stats reveal"><div><b data-count="2009" data-from="1991">2009</b><span>anno di fondazione</span></div><div><b data-count="100" data-suf="+">100+</b><span>unità realizzate dal gruppo</span></div>'
             '<div><b data-count="300" data-suf="+">300+</b><span>professionisti in rete</span></div><div><b>1</b><span>interlocutore dal progetto alle chiavi</span></div></div>')
    svc_cards = "".join(f'<a class="card reveal" href="servizio-{s}.html"><div class="ph">{tag(svc_img(p), "", SZ_CARD)}</div>'
                        f'<div class="t"><small>{i + 1:02d}</small><h3>{E(t)}</h3><p>{E(d)}</p><span class="go">Scopri il servizio {AR}</span></div></a>' for i, (s, t, d, p, *_r) in enumerate(SERV))
    why = "".join(f'<div class="reveal"><svg viewBox="0 0 24 24" aria-hidden="true">{ICON[i]}</svg><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i, a, b in WHY)
    steps4 = "".join(f'<li class="reveal"><small>FASE {i + 1:02d}</small><h3>{E(t)}</h3><p>{E(d)}</p></li>' for i, (t, d, _) in enumerate(STEPS))
    q_img = lambda: tag(im("q", pr("duelaghi"), (480, 980)), "Residenza Due Laghi, Muzzano", SZ_HALF, cls="reveal")
    pages = {}

    # ---- home ----
    works = [("greenhorse", "Residenziale"), ("optima", "Residenziale"), ("miracolli", "Residenziale")]
    wk = "".join(f'<a class="work" href="progetto-{k}.html">{tag(im("w-" + k, pr(k), (640, 900, 1440, 2000)), P[k][0] + ", " + P[k][1], SZ_FULL)}<div class="t"><div class="wrap reveal"><div class="tags"><span>{t.upper()}</span><span>{status(k).upper()}</span></div><h3>{E(P[k][0])}</h3><p>{E(P[k][1])} · {E(size(k))}</p><span class="go">Vedi il progetto {AR}</span></div></div></a>' for k, t in works)
    home = f"""<section class="hero">{tag(im("hero", pr("ferrari"), (640, 900, 1440, 2048)), "Residenza Ferrari, Tesserete", SZ_FULL, lazy=False)}<div class="wrap">
<h1 class="up">Progettiamo case che durano nel tempo</h1><p class="up d1">Archi Trend è lo studio di architettura del Gruppo New Trends a Lugano. Progetto, licenza e direzione lavori con un solo interlocutore, e uno sguardo sempre attento al valore dell'immobile.</p>
<div class="acts up d2"><a class="btn" href="contatti.html">Prenota una consulenza gratuita {AR}</a><a class="btn ghost" href="progetti.html">Guarda i progetti</a></div>
<div class="trust up d3"><span><b>Dal 2009</b> a Lugano</span><span><b>100+</b> unità realizzate dal gruppo</span><span>Primo incontro <b>senza impegno</b></span></div></div></section>
<main id="main">
<section class="sec ta"><div class="wrap"><div class="intro reveal"><p>In Archi Trend crediamo che un buon progetto inizi molto prima del primo disegno. <span>Parte dal capire il luogo, chi ci vivrà e il valore che la casa dovrà avere nel tempo. Per questo progettiamo con uno sguardo al mercato, insieme a chi poi costruisce e vende.</span></p><a class="btn ghost" href="studio.html">Conosci lo studio {AR}</a></div>{stats}</div></section>
<section class="sec tx"><div class="wrap m3"><div class="reveal"><span class="chip">Studio dei volumi</span><h2>Prima di disegnare, guardiamo i volumi.</h2><p class="lead">Ogni progetto parte da un modello semplice: quanto costruire, come disporlo sul terreno, dove mettere terrazze e vetrate per luce e vista. Gira il modello e guardalo da ogni lato.</p>
<ul class="bul"><li><b>01</b>Volumi e altezze ammesse</li><li><b>02</b>Orientamento, luce e vista</li><li><b>03</b>Terrazze, giardino e accessi</li></ul><p class="note">Modello di esempio, non un progetto reale.</p></div>
<div class="reveal m3d">{stage("massa", im("bp-aurea", bpf("aurea", "bp"), (480, 960)), "Disegno della Residenza Aurea, Collina d'Oro", "Modello 3D di una residenza a gradoni: trascina o usa le frecce per ruotarlo")}
<div class="ctl" role="group" aria-label="Comandi del modello"><span>Mostra</span><button type="button" aria-pressed="true" data-g="vol">Volumi</button><button type="button" aria-pressed="true" data-g="glass">Vetrate</button><button type="button" aria-pressed="true" data-g="terr">Terrazze e tetto</button><button type="button" aria-pressed="true" data-g="garden">Giardino</button>
<label class="rng">Costruzione <input type="range" min="0" max="100" value="100" data-p aria-label="Avanzamento della costruzione"><output>100%</output></label></div></div></div></section>
<section class="sec tb"><div class="wrap"><span class="chip">Cosa facciamo</span><h2>Servizi di architettura, dall'idea alle chiavi</h2><p class="lead" style="margin-bottom:40px">Puoi affidarci tutto il percorso o solo la parte che ti serve.</p><div class="cards">{svc_cards}</div></div></section>
<section class="ta" style="border-top:1px solid var(--line)"><div class="wt reveal"><h2>Progetti del gruppo</h2><p class="mid">Residenze progettate e realizzate dal Gruppo New Trends nel Luganese.</p></div>{wk}
<div class="wrap"><div class="after"><p>Hai un terreno o un immobile? Ti diciamo cosa ci si può costruire.</p><a class="btn" href="progetti.html">Tutti i progetti {AR}</a></div></div></section>
<section class="sec ta" id="questionario"><div class="wrap m3"><div class="reveal"><span class="chip">Un minuto</span><h2>Che progetto hai?</h2><p class="lead">Cinque domande veloci: tipo di progetto, terreno, Comune, budget e tempi. Le alleghiamo alla tua richiesta, così al primo contatto sappiamo già da dove partire.</p>
<ul class="bul"><li><b>01</b>Nessun dato personale fino all'ultimo passo</li><li><b>02</b>Puoi cambiare risposta quando vuoi</li><li><b>03</b>Ti risponde una persona dello studio</li></ul></div>{quiz_html()}{NOJS.replace("Il modulo ha", "Il questionario ha")}</div></section>
<section class="sec tb"><div class="wrap"><span class="chip">Il nostro processo</span><h2>Dall'idea al cantiere, in quattro fasi</h2><ol class="steps4">{steps4}</ol><p style="margin-top:40px"><a class="link" href="processo.html">Guarda il processo, fase per fase {AR}</a></p></div></section>
<section class="sec ta"><div class="wrap faq"><div><span class="chip">Domande</span><h2>Domande frequenti</h2><p class="mid">Le domande che ci fanno più spesso su progetto, tempi e costi.</p><p style="margin-top:22px"><a class="link" href="domande.html">Tutte le domande {AR}</a></p></div><div>{faqblock(fqpick(("inizio", 0), ("terreno", 0), ("costi", 0), ("licenza", 1), ("gruppo", 0)))}</div></div></section>{dopo_html("tb")}
<section class="sec tb"><div class="wrap"><div class="quote"><div class="reveal"><span class="chip">Gruppo New Trends</span><blockquote>“Progettare con uno sguardo al mercato: ogni scelta deve sostenere il valore e il risultato dell'immobile.”</blockquote>
<p>New Trends nasce a Lugano nel 1991. Oggi il gruppo riunisce New Trends SA per la consulenza e l'intermediazione immobiliare, Archi Trend SA per la progettazione ed Edil Trend SA per la realizzazione.</p>{chain}</div>{q_img()}</div></div></section>
{cta()}</main>"""
    pages["index.html"] = ("Archi Trend SA · Studio di architettura a Lugano", "Studio di architettura del Gruppo New Trends a Lugano: progettazione, licenze, direzione lavori, perizie e interni.", home, "home")

    # ---- studio ----
    st = f"""{phero(tag(im("st-hero", pr("synthesis"), (640, 768)), "Residenza Synthesis, Vezia", SZ_FULL, lazy=False), [(None, "Studio")], "Lo studio di architettura del Gruppo New Trends",
        "Dal 2009 a Lugano progettiamo case, ville e palazzine insieme a chi poi le costruisce e le vende.")}
<main id="main"><section class="sec ta"><div class="wrap"><div class="two"><div class="reveal"><span class="chip">Chi siamo</span><p class="big">Archi Trend SA è lo studio di architettura del Gruppo New Trends. Ci occupiamo di progettazione, licenze edilizie, direzione lavori, perizie e interni, per privati e investitori.</p></div>
<div class="reveal"><p class="mid">Lavorare in un gruppo che sviluppa, costruisce e vende immobili a Lugano dal 1991 ci dà uno sguardo particolare: un progetto deve essere bello e funzionare, ma anche reggere nel tempo i costi e il valore. Per questo progettiamo pensando al terreno, a chi abiterà la casa e al mercato.</p>
<dl class="dl" style="margin-top:28px"><dt>Ragione sociale</dt><dd>Archi Trend SA</dd><dt>Dal</dt><dd>2009</dd><dt>Sede</dt><dd>{ADDR}</dd><dt>Numero IDI</dt><dd>CHE-115.224.431</dd><dt>Gruppo</dt><dd>Gruppo New Trends</dd></dl></div></div>{stats}</div></section>
<section class="sec tb"><div class="wrap"><span class="chip">Perché sceglierci</span><h2>Lo studio giusto per il tuo progetto</h2><p class="lead">Progetto curato, comunicazione chiara e un gruppo che segue anche costruzione e vendita.</p><div class="why">{why}</div></div></section>
<section class="sec ta"><div class="wrap"><div class="quote"><div class="reveal"><span class="chip">Un solo gruppo</span><blockquote>Dal terreno alle chiavi, con chi conosce il territorio.</blockquote>
<p>New Trends trova il terreno o l'immobile e consiglia, Archi Trend progetta e ottiene la licenza, Edil Trend costruisce o ristruttura, New Trends vende, affitta e segue il dopo. Puoi affidarci tutto il percorso o solo una parte.</p>{chain}</div>{q_img()}</div></div></section>
{dopo_html("tb")}{cta("Parliamo del tuo progetto")}</main>"""
    pages["studio.html"] = ("Studio · Archi Trend SA", "Archi Trend SA, studio di architettura del Gruppo New Trends a Lugano dal 2009: chi siamo e come lavoriamo.", st, "studio")

    # ---- servizi ----
    sv = f"""{phero(tag(im("sv-hero", pr("optima"), (640, 820, 1000)), "Residenza Optima, Montagnola", SZ_FULL, lazy=False), [(None, "Servizi")], "Servizi di architettura", "Progettazione, licenze, direzione lavori, perizie, ristrutturazioni e interni. Tutto il percorso, oppure solo la parte che ti serve.")}
<main id="main"><section class="sec ta"><div class="wrap"><div class="cards">{svc_cards}</div></div></section>
<section class="sec tb"><div class="wrap"><span class="chip">Come lavoriamo</span><h2>Quattro fasi, decisioni chiare</h2><ol class="steps4">{steps4}</ol><p style="margin-top:40px"><a class="link" href="processo.html">Il processo nel dettaglio {AR}</a></p></div></section>{cta()}</main>"""
    pages["servizi.html"] = ("Servizi · Archi Trend SA", "Servizi di Archi Trend a Lugano: progettazione residenziale, licenze, direzione lavori, perizie, ristrutturazioni e interni.", sv, "servizi")
    for i, (s, t, d, p, preset, text, incl, rel, kd) in enumerate(SERV):
        hi = svc_img(p)
        extra = (fattib_html("tb") if s == "progettazione" else (domanda_html("tb") + fattib_html("ta") if s == "licenze" else ""))
        other = "".join(f'<li><a class="link" href="servizio-{s2}.html">{E(t2)} {AR}</a></li>' for s2, t2, *_ in SERV if s2 != s)
        body = f"""{phero(tag(hi, "", SZ_FULL, lazy=False), [("servizi.html", "Servizi"), (None, t)], E(t), E(d), f'<a class="btn" href="contatti.html?tipo={kd.replace(" ", "+")}">Chiedi una consulenza {AR}</a>')}
<main id="main"><section class="sec ta"><div class="wrap m3"><div class="reveal"><span class="chip">Servizio {i + 1:02d}</span><p class="big" style="font-size:clamp(1.15rem,1.05rem + .45vw,1.45rem);line-height:1.5">{E(text)}</p>
<ul class="bul">{"".join(f"<li><b>{j + 1:02d}</b>{E(x)}</li>" for j, x in enumerate(incl))}</ul></div>
<div class="reveal">{stage(preset, hi, t, "Modello 3D: " + LABEL3D[preset] + ". Trascina o usa le frecce per ruotarlo")}<p class="note">Modello di esempio per spiegare il servizio, non un progetto reale.</p></div></div></section>
<section class="sec tb"><div class="wrap"><span class="chip">Progetti del gruppo</span><h2>Lavori vicini a questo servizio</h2><p class="lead" style="margin-bottom:34px">Progetti seguiti dalle aziende del Gruppo New Trends.</p><div class="pgrid">{"".join(pcard(k) for k in rel)}</div></div></section>
{extra}<section class="sec ta"><div class="wrap faq"><div><span class="chip">Domande</span><h2>Domande su questo servizio</h2><p class="mid">Altre risposte nella pagina <a class="link" href="domande.html">Domande frequenti {AR}</a></p></div><div>{faqblock(fqpick(*SFAQ[s]))}</div></div></section>
<section class="sec tb"><div class="wrap two"><div><span class="chip">Altri servizi</span><h2>Ti serve anche altro?</h2></div><ul class="bul">{other}</ul></div></section>
{cta(t)}</main>"""
        pages[f"servizio-{s}.html"] = (f"{t} · Archi Trend SA", f"{t} a Lugano e in Ticino con Archi Trend SA. {d}", body, "servizi")

    # ---- progetti ----
    pj = f"""{phero(tag(im("w-greenhorse", pr("greenhorse"), (640, 900, 1440, 2000)), "Residenza Green Horse, Muzzano", SZ_FULL, lazy=False), [(None, "Progetti")], "Progetti del gruppo", "Residenze, villette e ristrutturazioni seguite dalle aziende del Gruppo New Trends nel Luganese.")}
<main id="main"><section class="sec ta"><div class="wrap"><div class="tabs" role="group" aria-label="Filtra i progetti"><button type="button" aria-pressed="true" data-f="">Tutti</button><button type="button" aria-pressed="false" data-f="new">Nuove costruzioni</button><button type="button" aria-pressed="false" data-f="ren">Ristrutturazioni</button></div>
<div class="pgrid">{"".join(pcard(k) for k in ORDER)}</div><p class="note">Ruoli come descritti nel portfolio del Gruppo New Trends.</p></div></section>
<section class="sec tb"><div class="wrap"><span class="chip">Disegno e realtà</span><h2>Quello che disegniamo, lo vedi costruito.</h2><p class="lead" style="margin-bottom:40px">Trascina il cursore per confrontare il disegno con l'edificio finito.</p><div class="ba">{"".join(f'<div class="reveal">{slider(k, "bp")}<h3>{E(P[k][0])}</h3><p>{E(P[k][1])} · {E(size(k))}</p></div>' for k in ("ferrari", "maraini", "synthesis"))}</div></div></section>{cta()}</main>"""
    pages["progetti.html"] = ("Progetti · Archi Trend SA", "Progetti del Gruppo New Trends nel Luganese: residenze, villette e ristrutturazioni.", pj, "progetti")
    for n, k in enumerate(ORDER):
        name, place, sz, role, _, cat = P[k]
        mode = "ba" if k in ("magliaso", "montagnola") else ("bp" if has_bp(k) else None)
        cmpb = ""
        if mode:
            c1, c2 = ("Prima e dopo", "Trascina il cursore per vedere com'era e com'è oggi.") if mode == "ba" else ("Disegno e realtà", "Trascina il cursore per confrontare il disegno con l'edificio.")
            cmpb = f'<section class="sec tb"><div class="wrap"><span class="chip">{c1}</span><h2>{E(nm(k))}</h2><p class="lead" style="margin-bottom:34px">{c2}</p><div class="ba one reveal">{slider(k, mode)}</div></div></section>'
        rel = [ORDER[(n + j) % len(ORDER)] for j in (1, 2, 3)]
        body = f"""{phero(tag(im("w-" + k, pr(k), (640, 900, 1440, 2000)), nm(k), SZ_FULL, lazy=False), [("progetti.html", "Progetti"), (None, nm(k))], E(nm(k)), E(place + " · " + sz.replace(" · ", ", ")))}
<main id="main"><section class="sec ta"><div class="wrap"><div class="facts reveal"><div><small>Comune</small><b>{E(place)}</b></div><div><small>Progetto</small><b>{E(size(k))}</b></div><div><small>Tipo</small><b>{kind(k)}</b></div><div><small>Stato</small><b>{status(k)}</b></div></div>
<div class="two" style="margin-top:50px"><div class="reveal"><span class="chip">Il ruolo del gruppo</span><p class="big">{E(role)}</p><p class="note">Progetto del Gruppo New Trends. Il ruolo è quello descritto nel portfolio del gruppo.</p>
<div class="acts" style="margin-top:28px"><a class="btn" href="contatti.html">Parliamo del tuo progetto {AR}</a><a class="btn ghost" href="progetti.html">Tutti i progetti</a></div></div>
<div class="reveal">{tag(im("p-" + k, pr(k)), nm(k), SZ_HALF, cls="photo")}</div></div></div></section>{cmpb}
<section class="sec {"ta" if cmpb else "tb"}"><div class="wrap"><span class="chip">Altri progetti</span><h2 style="margin-bottom:34px">Continua a guardare</h2><div class="pgrid">{"".join(pcard(r) for r in rel)}</div></div></section>{cta()}</main>"""
        pages[f"progetto-{k}.html"] = (f"{nm(k)}, {place} · Archi Trend SA", f"{nm(k)}, {place}: {sz}. {role}", body, "progetti")

    # ---- processo ----
    ph4 = "".join(f'<article{" class=on" if i == 0 else ""}><small>FASE {i + 1:02d}</small><h3>{E(t)}</h3><p>{E(d)}</p><div class="p3"><div><b>Cosa succede</b>{ul(PHASES[i][0])}</div><div><b>Cosa ricevi</b>{ul(PHASES[i][1])}</div><div><b>Cosa ti chiediamo</b>{ul(PHASES[i][2])}</div></div></article>' for i, (t, d, l) in enumerate(STEPS))
    pc = f"""{phero(tag(im("pc-hero", bpf("optima", "bp"), (640, 820, 1000)), "Disegno della Residenza Optima, Montagnola", SZ_FULL, lazy=False), [(None, "Processo")], "Dall'idea al cantiere", "Un percorso chiaro in quattro fasi, con decisioni e costi sempre sotto controllo. Scorri e guarda il disegno diventare edificio.")}
<main id="main"><section class="sec ta" data-morph><div class="wrap morph"><div class="stick">{stage("morph", im("bp-greenhorse", bpf("greenhorse", "bp"), (480, 960)), "Disegno della Residenza Green Horse, Muzzano", "Modello 3D: la pianta disegnata a terra diventa un edificio mentre scorri le quattro fasi", hint="")}</div>
<div class="ph4">{ph4}<a class="btn" href="contatti.html" style="margin-top:20px">Inizia dalla fase 01 {AR}</a></div></div></section>
<section class="sec tb"><div class="wrap two"><div class="reveal"><span class="chip">Prima del primo incontro</span><h2>Cosa portare</h2><p class="lead">Spunta quello che hai già e mandacelo con la richiesta: ci aiuta a preparare il primo incontro. Se non hai nulla, va bene lo stesso.</p></div><div>{checklist_html()}{NOJS.replace("Il modulo ha", "La lista ha")}</div></div></section>
{domanda_html("ta")}{dopo_html("tb")}
<section class="sec ta"><div class="wrap"><span class="chip">Perché funziona</span><h2>Meno sorprese, più decisioni chiare</h2><div class="why">{why}</div></div></section>
<section class="sec tb"><div class="wrap"><span class="chip">Disegno e realtà</span><h2>Quello che disegniamo, lo vedi costruito.</h2><p class="lead" style="margin-bottom:40px">Trascina il cursore per confrontare il disegno con l'edificio finito.</p><div class="ba">{"".join(f'<div class="reveal">{slider(k, "bp")}<h3>{E(P[k][0])}</h3><p>{E(P[k][1])} · {E(size(k))}</p></div>' for k in ("optima", "aurea", "duelaghi"))}</div></div></section>{cta()}</main>"""
    pages["processo.html"] = ("Processo · Archi Trend SA", "Come lavora Archi Trend: ascolto e sopralluogo, concept, progetto e licenza, direzione lavori e consegna.", pc, "processo")

    # ---- domande ----
    fqa = ('<div class="fsearch"><label for="fq">Cerca tra le domande</label><input id="fq" type="search" placeholder="es. licenza, onorari, terreno, opposizione" autocomplete="off"></div>'
           '<div class="chips" role="group" aria-label="Filtra per argomento"><button type="button" aria-pressed="true" data-t="">Tutte</button>' + "".join(f'<button type="button" aria-pressed="false" data-t="{i}">{E(g)}</button>' for i, g, _ in FAQ) + '</div>'
           f'<p class="fcount" aria-live="polite">{sum(len(x) for _, _, x in FAQ)} domande</p>'
           + "".join(f'<div class="fgroup" data-t="{i}"><h3>{E(g)}</h3>{faqblock(items).replace(" open>", ">")}</div>' for i, g, items in FAQ)
           + f'<p class="fnone" hidden>Nessuna domanda trovata. <a class="link" href="contatti.html">Chiedicelo direttamente {AR}</a></p>')
    dq = f"""{phero(tag(im("dq-hero", pr("aurea"), (640, 820, 980)), "Residenza Aurea, Collina d'Oro", SZ_FULL, lazy=False), [(None, "Domande")], "Domande frequenti", "Progetto, licenza, cantiere e costi: le risposte alle domande che ci fanno più spesso.", short=True)}
<main id="main"><section class="sec ta"><div class="wrap faq"><div><span class="chip">Domande</span><h2>Chiedici pure</h2><p class="mid">Non trovi la tua domanda? Chiamaci al <a class="link" href="tel:{TEL}">{PHONE}</a> o scrivici: il primo incontro è senza impegno.</p><div class="acts" style="margin-top:26px"><a class="btn" href="contatti.html">Scrivici {AR}</a><button type="button" class="btn ghost" data-cb>Ti richiamiamo noi</button></div></div><div class="fwrap">{fqa}</div></div></section>{dopo_html("tb")}{cta()}</main>"""
    pages["domande.html"] = ("Domande frequenti · Archi Trend SA", "Domande frequenti su progetto, licenza edilizia, direzione lavori e costi con Archi Trend a Lugano.", dq, "domande")

    # ---- contatti ----
    form = f"""<div class="form reveal" id="modulo"><h3>Raccontaci il progetto: ti richiamiamo per fissare il primo incontro.</h3><div class="qsum" hidden><b>Dal questionario</b><ul></ul><button type="button" class="link" data-qclear>Togli le risposte</button></div><form novalidate action="javascript:void 0" data-lead data-main data-kind="Altro">
<div class="row"><label>Nome e cognome<input name="name" autocomplete="name" placeholder="Mario Rossi" required></label><label>Telefono<input name="phone" type="tel" autocomplete="tel" placeholder="+41 79 000 00 00"></label></div>
<label>Email<input name="email" type="email" autocomplete="email" placeholder="nome@email.ch"></label>
<div class="row"><label>Tipo di progetto<select name="kind"><option value="">Scegli…</option>{"".join(f"<option>{E(k)}</option>" for k in KINDS)}</select></label><label>Comune<input name="town" placeholder="es. Lugano"></label></div>
<label>Messaggio (facoltativo)<textarea name="message" rows="3" placeholder="es. terreno di 800 m² a Tesserete, vorrei una casa per 4 persone"></textarea></label>
{checklist_html(True)}{radios("Hai già lavorato con un architetto?", "had", ["Sì", "No"])}{consent()}
<label class="check"><input type="checkbox" name="newsletter"><span>Desidero ricevere occasionalmente novità del Gruppo New Trends (facoltativo).</span></label>
<p class="err" hidden role="alert"></p>{NOJS}<button class="btn" type="submit">Prenota la consulenza gratuita {AR}</button></form></div>"""
    ct = f"""{phero(tag(im("ct-hero", pr("duelaghi"), (640, 820, 980)), "Residenza Due Laghi, Muzzano", SZ_FULL, lazy=False), [(None, "Contatti")], "Creiamo qualcosa di eccezionale", "Il primo incontro è senza impegno. Scegli tu come preferisci sentirci.", short=True)}
<main id="main"><section class="sec ta" id="contatti"><div class="wrap ct"><div class="reveal"><span class="chip">Contatti</span><h2>Parliamo del tuo progetto</h2><p class="mid" style="margin-top:16px;max-width:46ch">Raccontaci terreno, immobile o idea: ti richiamiamo per fissare il primo incontro in studio o sul posto.</p>
<div class="direct"><a href="tel:{TEL}"><span><small>Telefono</small><b>{PHONE}</b></span>{AR}</a><a href="https://wa.me/{WA}" target="_blank" rel="noopener"><span><small>WhatsApp</small><b>Scrivici un messaggio</b></span>{AR}</a><a href="mailto:{MAIL}"><span><small>Email</small><b>{MAIL}</b></span>{AR}</a></div>
<button type="button" class="btn ghost" data-cb style="margin-top:14px;width:100%;justify-content:center">Preferisci che ti richiamiamo noi?</button>
<dl class="dl" style="margin-top:28px"><dt>Studio</dt><dd>{ADDR}</dd><dt>Gruppo</dt><dd>Gruppo New Trends</dd></dl></div>{form}</div></section>
<section class="sec tb" id="questionario"><div class="wrap m3"><div class="reveal"><span class="chip">Un minuto</span><h2>Non sai da dove iniziare?</h2><p class="lead">Rispondi a cinque domande: le risposte si aggiungono al modulo qui sopra.</p></div>{quiz_html()}{NOJS.replace("Il modulo ha", "Il questionario ha")}</div></section>
{fattib_html("ta")}{dopo_html("tb")}{cta("Ancora dubbi?", "Chiamaci al " + PHONE + " o lasciaci il numero: ti richiamiamo noi.")}</main>"""
    pages["contatti.html"] = ("Contatti · Archi Trend SA", "Contatta Archi Trend SA a Lugano: telefono, WhatsApp, email o modulo per prenotare la consulenza gratuita.", ct, "contatti")
    pv = f'{phero(tag(im("ct-hero", pr("duelaghi"), (640, 820, 980)), "", SZ_FULL, lazy=False), [(None, "Privacy")], "Privacy", short=True)}<main id="main" class="ta">{b2.privacy("Archi Trend SA").replace("<h1>", "<h2>").replace("</h1>", "</h2>")}</main>'
    pages["privacy.html"] = ("Privacy · Archi Trend SA", "Informativa privacy di Archi Trend SA.", pv, "")

    js3 = open(os.path.join(HERE, "src", "archi3d.js")).read()
    v = hashlib.sha256((CSS + JS + js3).encode()).hexdigest()[:10]
    open(os.path.join(A, "site.css"), "w").write(CSS); open(os.path.join(A, "app.js"), "w").write("(function(){" + JS.replace("V3D", v) + "})();")
    for n, (t, d, body, cur) in pages.items(): open(os.path.join(OUT, n), "w").write(page(t, d, body, v, cur))
    open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
    print("ok", OUT, THEME, len(pages), "pagine")

if __name__ == "__main__":
    build()
