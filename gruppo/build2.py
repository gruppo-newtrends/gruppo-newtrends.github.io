# -*- coding: utf-8 -*-
"""Siti Archi Trend ed Edil Trend, versione 2: ognuno con un percorso e interazioni sue.
Archi Trend = "dal disegno alla realtà" (piani tecnici che diventano foto, cursore progetto/realtà, percorso che si accende,
"che progetto hai in mente?", galleria orizzontale). Edil Trend = "il cantiere che sale" (titolo a mattoni, fascia lavori,
edificio che si costruisce scorrendo, configuratore del preventivo a passi, lavori filtrabili).
Uso: python3 -E -s build2.py -> out/architrend, out/ediltrend. Testi solo su fatti del registro e del portfolio new-trends.ch."""
import hashlib, html, os, shutil
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out"); E = html.escape
IMG = os.path.join(HERE, "src", "img", "progetti"); BP = os.path.join(HERE, "src", "blueprint")
SITES = {"newtrends": "https://gruppo-newtrends.github.io/newtrends/it/", "architrend": "https://gruppo-newtrends.github.io/architrend/", "ediltrend": "https://gruppo-newtrends.github.io/ediltrend/"}
GROUP = [("newtrends", "New Trends", "Immobiliare"), ("architrend", "Archi Trend", "Architettura"), ("ediltrend", "Edil Trend", "Costruzioni")]
PHONE, TEL, ADDR, MAIL, WA = "+41 91 921 00 31", "+41919210031", "Via Pretorio 11, 6900 Lugano", "info@new-trends.ch", "41768232203"
P = {  # progetti del gruppo come descritti su new-trends.ch/portfolio.html
    "ferrari": ("Residenza Ferrari", "Tesserete", "8 appartamenti · in costruzione", "Progetto, direzione lavori, marketing e vendita.", "residenza-ferrari-tesserete", "new"),
    "synthesis": ("Residenza Synthesis", "Vezia", "8 appartamenti e 4 spazi commerciali", "Sviluppo, progettazione, direzione lavori e vendita.", "e441867e-5-1-768x514-3", "new"),
    "optima": ("Residenza Optima", "Montagnola", "6 appartamenti", "Progetto, realizzazione, vendita e prima amministrazione.", "residenza-optima-montagnola", "new"),
    "greenhorse": ("Residenza Green Horse", "Muzzano", "12 appartamenti · in costruzione", "Progetto, marketing e vendita.", "residenza-green-horse-muzzano", "new"),
    "maraini": ("Residenza Maraini", "Savosa", "24 appartamenti", "Acquisizione, progettazione, realizzazione e vendita.", "c4db19e3-Residenza-Maraini", "new"),
    "miracolli": ("Residenza Miracolli", "Savosa · Porza", "8 appartamenti", "Business plan, licenza, costruzione e vendita.", "95c0aada-1-1-1", "new"),
    "aurea": ("Residenza Aurea", "Collina d'Oro", "20 appartamenti", "Dalla compravendita del terreno fino alla consegna.", "740a0781-Residenza-Aurea", "new"),
    "duelaghi": ("Residenza Due Laghi", "Muzzano · Breganzona", "6 appartamenti", "Sviluppati con una regia completa.", "9e7013d0-Residenza-due-Laghi", "new"),
    "fortuna": ("Villaggio Fortuna", "Grancia", "12 villette e 27 lotti", "Realizzazione di 8 villette singole e 4 a schiera.", "e916ea83-Villaggio-Fortuna-a-Grancia", "new"),
    "magliaso": ("Palazzina", "Magliaso", "Ristrutturazione", "Ristrutturazione, messa a reddito e rivendita.", "palazzina-magliaso", "ren"),
    "corteglia": ("Villa", "Corteglia", "Ristrutturazione", "Ristrutturazione e valorizzazione.", "villa-corteglia", "ren"),
    "motta": ("Appartamento", "Lugano · Via Motta", "Ristrutturazione", "Ristrutturazione e messa a reddito.", "via-motta", "ren"),
    "pregassona": ("Appartamento", "Pregassona", "Ristrutturazione", "Ristrutturazione e riposizionamento.", "appartamento-pregassona", "ren"),
    "montagnola": ("Appartamento", "Montagnola", "Ristrutturazione", "Ristrutturazione e valorizzazione.", "appartamento-montagnola", "ren"),
}
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'

def save_img(src, dst, w):
    im = Image.open(src).convert("RGB")
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(dst, quality=80, optimize=True)

def find_src(stem):
    for f in os.listdir(IMG):
        if os.path.splitext(f)[0] == stem: return os.path.join(IMG, f)
    raise FileNotFoundError(stem)

# ---------- parti comuni ----------
COMMON_CSS = """*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}body{margin:0}img{max-width:100%;display:block}a{color:inherit}
.skip{position:absolute;left:-999px}.skip:focus{left:12px;top:12px;background:#fff;color:#000;padding:8px 12px;z-index:999}
.gbar{background:#0C1D44;color:#EEF2FA;font:500 .82rem/1 "Instrument Sans",Arial,sans-serif;position:relative;z-index:60}
.gbar .in{max-width:1320px;margin:0 auto;padding:0 20px;display:flex;align-items:center;gap:6px 16px;min-height:36px;flex-wrap:wrap}
.gbar b{font-weight:600;margin-right:auto}.gbar nav{display:flex;gap:4px;flex-wrap:wrap}
.gbar a,.gbar span{text-decoration:none;padding:.3rem .65rem;border-radius:999px;color:#AAB7D4}.gbar a:hover{color:#fff;background:#ffffff14}
.gbar a[aria-current]{color:#fff;background:#ffffff26}.gbar span{opacity:.55}
@media (max-width:620px){.gbar b,.gbar span{display:none}.gbar nav{width:100%;justify-content:center}}
.reveal{opacity:0;transform:translateY(24px);transition:opacity .8s cubic-bezier(.2,.7,.2,1),transform .8s cubic-bezier(.2,.7,.2,1)}.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}.reveal{opacity:1;transform:none}}
.wa{position:fixed;right:18px;bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:50;background:#1F7A4D;color:#fff;border-radius:999px;padding:.8rem 1.1rem;font:700 .95rem "Instrument Sans",Arial,sans-serif;text-decoration:none;box-shadow:0 10px 30px #0004}
.hp{position:absolute;left:-9999px}
"""
COMMON_JS = r"""
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{threshold:.15});
document.querySelectorAll(".reveal").forEach(function(x){io.observe(x)});
function sendReq(d,box,okHtml,waText){return fetch("https://crm-newtrends.2-29-109-125.sslip.io/api/pubblico/richiesta",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)}).then(function(r){if(!r.ok)throw 0;box.innerHTML=okHtml},function(){box.innerHTML="<h3>Non siamo riusciti a inviare la richiesta.</h3><p>Mandacela su WhatsApp con un tocco, è già scritta.</p><a class='btn' target='_blank' rel='noopener' href='https://wa.me/WA_NUM?text="+encodeURIComponent(waText)+"'>Manda su WhatsApp</a>"})}
var mb=document.querySelector("[data-menu]");if(mb)mb.addEventListener("click",function(){var n=document.querySelector(".nav");var o=n.classList.toggle("open");mb.setAttribute("aria-expanded",o)});
""".replace("WA_NUM", WA)

def gbar(co):
    links = "".join(f'<a href="{SITES[k]}"{" aria-current=\"page\"" if k == co else ""}>{n}</a>' for k, n, _ in GROUP)
    return f'<div class="gbar"><div class="in"><b>Gruppo New Trends</b><nav aria-label="Aziende del gruppo">{links}<span>Altre aziende del gruppo: presto</span></nav></div></div>'

def doc(co, title, desc, fonts, css, body, js, v):
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#0C1D44">
<link rel="icon" href="favicon.svg" type="image/svg+xml">{FONTS}<link rel="stylesheet" href="{fonts}"><link rel="stylesheet" href="assets/site.css?v={v}"></head>
<body><a class="skip" href="#main">Vai al contenuto</a>{gbar(co)}{body}<a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Scrivici su WhatsApp">WhatsApp</a>
<script src="assets/app.js?v={v}" defer></script></body></html>"""

def chain(co, cls):
    items = [("newtrends", "New Trends", "trova il terreno o l'immobile e consiglia"), ("architrend", "Archi Trend", "progetta e ottiene la licenza"),
             ("ediltrend", "Edil Trend", "costruisce o ristruttura"), ("newtrends", "New Trends", "vende, affitta e segue il dopo")]
    return f'<ol class="{cls}">' + "".join(f'<li class="{"me" if k == co else ""}"><a href="{SITES[k]}"><small>{n + 1:02d}</small><b>{E(t)}</b><span>{E(d)}</span></a></li>' for n, (k, t, d) in enumerate(items)) + "</ol>"

def footer(legal, kind, accent_cls):
    return f"""<footer class="ftr"><div class="in"><div><b>{E(legal)}</b><p>{E(kind)}. Parte del Gruppo New Trends, a Lugano dal 1991.</p><p>{ADDR}<br><a href="tel:{TEL}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a></p></div>
<div><b>Il gruppo</b><ul>{"".join(f'<li><a href="{SITES[k]}">{n} · {d}</a></li>' for k, n, d in GROUP)}</ul></div>
<div><b>Il sito</b><ul><li><a href="index.html#percorso">Come lavoriamo</a></li><li><a href="progetti.html">Progetti</a></li><li><a href="index.html#contatti">Contatti</a></li><li><a href="privacy.html">Privacy</a></li></ul></div>
<p class="legal">© {E(legal)} · {ADDR}</p></div></footer>"""

def privacy(legal):
    return f"""<section class="plain"><h1>Informativa sulla privacy</h1>
<p>{E(legal)}, {ADDR}, tratta i dati che ci invii (nome, email, telefono, comune e messaggio) solo per rispondere alla tua richiesta e, se lo hai scelto, per inviarti novità del Gruppo New Trends.</p>
<p>I dati restano sul server del gruppo in Svizzera e sono condivisi solo con le aziende del Gruppo New Trends che servono per la tua richiesta. Non li vendiamo e non li cediamo a terzi.</p>
<p>Puoi chiedere in ogni momento di vederli, correggerli o cancellarli scrivendo a <a href="mailto:{MAIL}">{MAIL}</a>. Vale la legge svizzera sulla protezione dei dati (LPD).</p>
<p class="small">Testo da verificare con la direzione prima della pubblicazione definitiva.</p></section>"""

# ===================== ARCHI TREND =====================
A_FONT = "https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..600;1,6..96,400..500&family=Instrument+Sans:wght@400..700&display=swap"
A_CSS = COMMON_CSS + """
:root{--ink:#10241F;--paper:#F5F2EA;--sheet:#FBFAF6;--green:#2F6B62;--green-d:#1E4A43;--mint:#A9D6CC;--bp:#12344A;--bp-line:#DEEEFC;--line:#D7D1C3;--muted:#4B5A55}
body{background:var(--paper);color:var(--ink);font:1.05rem/1.6 "Instrument Sans",Arial,sans-serif}
.in{max-width:1320px;margin:0 auto;padding:0 20px}
.hdr{position:sticky;top:0;z-index:40;background:#F5F2EAee;backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.hdr .in{display:flex;align-items:center;gap:24px;height:72px}
.logo{display:flex;align-items:center;gap:12px;text-decoration:none}
.logo svg{width:38px;height:38px}.logo b{font:500 1.3rem/1 "Bodoni Moda",Georgia,serif;letter-spacing:.14em;text-transform:uppercase}.logo small{display:block;font:500 .7rem/1.2 "Instrument Sans",Arial,sans-serif;color:var(--muted);letter-spacing:.06em}
.nav{display:flex;gap:2px;margin-left:auto}.nav a{text-decoration:none;padding:.5rem .8rem;border-radius:8px;font-weight:500}.nav a:hover{background:#2F6B6214;color:var(--green-d)}
.btn{display:inline-flex;align-items:center;gap:10px;font:600 .95rem "Instrument Sans",Arial,sans-serif;letter-spacing:.02em;padding:.95rem 1.5rem;border-radius:2px;border:2px solid transparent;text-decoration:none;cursor:pointer;background:var(--green);color:#fff;transition:transform .2s,background .2s}
.btn:hover{background:var(--green-d)}.btn.ghost{background:transparent;border-color:currentColor;color:inherit}.btn.ghost:hover{background:#ffffff14}
.menu{display:none;margin-left:auto;background:none;border:1px solid var(--line);border-radius:8px;padding:.5rem .8rem;font-weight:600;font-size:.95rem;font-family:inherit}
@media (max-width:900px){.nav,.hdr .btn{display:none}.menu{display:inline-flex}.nav.open{display:flex;position:absolute;top:72px;left:0;right:0;flex-direction:column;background:var(--paper);padding:12px 20px 20px;border-bottom:1px solid var(--line)}}
h1,h2,h3{font-family:"Bodoni Moda",Georgia,serif;font-weight:400;letter-spacing:-.02em;line-height:1.05;margin:0;text-wrap:balance}
h2{font-size:clamp(2rem,1.3rem + 2.6vw,3.6rem)}h2 i,h1 i{color:var(--green);font-style:italic}
.tag{font:600 .74rem/1 "Instrument Sans",Arial,sans-serif;letter-spacing:.18em;text-transform:uppercase;color:var(--green);display:inline-flex;gap:10px;align-items:center;margin-bottom:16px}
.tag::before{content:"";width:28px;height:1px;background:currentColor}
.lead{font-size:clamp(1.05rem,1rem + .3vw,1.25rem);color:var(--muted);max-width:60ch}
section{position:relative}.sec{padding:clamp(64px,8vw,120px) 0}
/* hero: il disegno che diventa realtà */
.hero{min-height:calc(100svh - 108px);display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);align-items:center;gap:clamp(24px,4vw,64px);max-width:1320px;margin:0 auto;padding:40px 20px 56px}
@media (max-width:900px){.hero{grid-template-columns:1fr;min-height:0}}
.hero h1{font-size:clamp(2.6rem,1.6rem + 4vw,5.2rem);font-weight:400}.hero h1 i{font-weight:400}
.hero .lead{margin:22px 0 30px}.hero .acts{display:flex;gap:12px;flex-wrap:wrap}.hero .btn.ghost{color:var(--ink)}
.stage{position:relative;aspect-ratio:16/10;border-radius:4px;overflow:hidden;box-shadow:0 40px 80px -40px #10241f80;background:var(--bp)}
.stage img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.stage .bp{clip-path:inset(0 100% 0 0);animation:draw 2.2s cubic-bezier(.6,.1,.3,1) .3s forwards}
.stage .ph{clip-path:inset(0 0 0 100%);animation:real 1.6s cubic-bezier(.6,.1,.3,1) 2.9s forwards}
.stage .scan{position:absolute;top:0;bottom:0;width:2px;background:var(--mint);box-shadow:0 0 18px var(--mint);left:0;opacity:0;animation:scan 1.6s cubic-bezier(.6,.1,.3,1) 2.9s forwards}
@keyframes draw{to{clip-path:inset(0 0 0 0)}}@keyframes real{to{clip-path:inset(0 0 0 0)}}@keyframes scan{0%{left:100%;opacity:1}90%{opacity:1}100%{left:0;opacity:0}}
.stage .dim{position:absolute;left:4%;right:4%;bottom:5%;height:14px;border-left:1px solid #fff9;border-right:1px solid #fff9;font:600 .7rem "Instrument Sans",Arial,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#fff;text-align:center;opacity:0;animation:fade .6s ease 1.6s forwards}
.stage .dim::before{content:"";position:absolute;left:0;right:0;top:7px;border-top:1px dashed #fff9}.stage .dim span{position:relative;background:var(--bp);padding:0 8px}
.stage .cap{display:none}
@keyframes fade{to{opacity:1}}
@media (max-width:600px){.stage .dim{display:none}}
/* numeri */
.facts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-block:1px solid var(--line);max-width:1320px;margin:0 auto}
.facts div{padding:26px 20px;border-right:1px solid var(--line)}.facts div:last-child{border:0}.facts b{display:block;font:400 clamp(2rem,1.4rem + 1.8vw,3rem)/1 "Bodoni Moda",Georgia,serif}.facts span{color:var(--muted);font-size:.95rem}
@media (max-width:800px){.facts{grid-template-columns:repeat(2,minmax(0,1fr))}.facts div:nth-child(2){border-right:0}.facts div{border-bottom:1px solid var(--line)}}
/* progetto / realtà */
.cmp{position:relative;aspect-ratio:16/9;max-height:78vh;width:100%;overflow:hidden;border-radius:4px;user-select:none;touch-action:pan-y;cursor:ew-resize;background:var(--bp)}
.cmp img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;pointer-events:none}
.cmp .top{clip-path:inset(0 calc(100% - var(--x,50%)) 0 0)}
.cmp .h{position:absolute;top:0;bottom:0;left:var(--x,50%);width:2px;background:#fff;transform:translateX(-1px)}
.cmp .h button{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:54px;height:54px;border-radius:50%;border:0;background:#fff;color:var(--green-d);font-weight:700;font-size:1.1rem;font-family:inherit;box-shadow:0 8px 24px #0005;cursor:ew-resize}
.cmp .l{position:absolute;top:16px;font:500 .75rem "Instrument Sans",Arial,sans-serif;color:#fff;background:#0009;padding:6px 10px;border-radius:4px}.cmp .l.a{left:16px}.cmp .l.b{right:16px}
/* percorso */
.path{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:clamp(24px,5vw,80px)}
@media (max-width:900px){.path{grid-template-columns:1fr}}
.path .pin{position:sticky;top:120px;align-self:start}
@media (max-width:900px){.path .pin{position:static}}
.big{font:400 clamp(4.5rem,3rem + 6vw,8rem)/1 "Bodoni Moda",Georgia,serif;font-style:italic;color:var(--green);transition:opacity .3s}
.meter{display:flex;gap:6px;margin-top:20px}.meter i{flex:1;height:4px;background:var(--line);border-radius:4px;transition:background .4s}.meter i.on{background:var(--green)}
.phase{min-height:62vh;display:flex;flex-direction:column;justify-content:center;border-top:1px solid var(--line);padding:24px 0;opacity:.35;transition:opacity .5s}
.phase.on{opacity:1}.phase h3{font-size:clamp(1.8rem,1.2rem + 1.8vw,2.8rem);margin:6px 0 12px}.phase p{color:var(--muted);max-width:52ch;margin:0}
.phase ul{list-style:none;padding:0;margin:16px 0 0;display:flex;flex-wrap:wrap;gap:8px}.phase li{font:500 .85rem "Instrument Sans",Arial,sans-serif;color:var(--muted)}.phase li+li::before{content:"·";margin-right:8px;color:var(--green)}
@media (max-width:900px){.phase{min-height:0;opacity:1}}
/* che progetto hai in mente */
.quiz{background:var(--green-d);color:#EAF4FB;border-radius:6px;padding:clamp(24px,4vw,56px)}
.quiz h2 i{color:var(--mint)}.opts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:28px 0}
@media (max-width:900px){.opts{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:520px){.opts{grid-template-columns:1fr}}
.opts button{text-align:left;background:transparent;border:1px solid #ffffff40;color:#fff;border-radius:2px;padding:20px;cursor:pointer;font-weight:600;font-size:1.02rem;font-family:inherit;transition:background .2s,transform .2s,border-color .2s}
.opts button small{display:none}
.opts button:hover{background:#ffffff12}.opts button[aria-pressed=true]{background:#fff;color:var(--green-d);border-color:#fff}
.opts button[aria-pressed=true] small{color:var(--bp)}
.answer{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:end;border-top:1px dashed #ffffff40;padding-top:24px;min-height:120px}
@media (max-width:700px){.answer{grid-template-columns:1fr}}
.answer ol{margin:8px 0 0;padding-left:20px;color:#CFE3F1}.answer .btn{background:#fff;color:var(--green-d)}
/* progetti orizzontali */
.rail{display:flex;gap:20px;overflow-x:auto;scroll-snap-type:x mandatory;padding:8px 20px 28px;scrollbar-width:thin;cursor:grab}
.rail.drag{cursor:grabbing;scroll-snap-type:none}.rail::-webkit-scrollbar{height:6px}.rail::-webkit-scrollbar-thumb{background:var(--line);border-radius:6px}
.card{flex:0 0 min(78vw,440px);scroll-snap-align:start}.card .ph{position:relative;aspect-ratio:4/3;overflow:hidden;border-radius:4px;background:var(--bp)}
.card .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .6s}.card .ph .b{opacity:0}
.card:hover .ph .b,.card:focus-within .ph .b{opacity:1}
.card small{display:block;font:500 .75rem "Instrument Sans",Arial,sans-serif;color:var(--green);margin:14px 0 4px}.card h3{font-size:1.5rem}.card p{color:var(--muted);margin:6px 0 0;font-size:.95rem}
.hint{font:500 .78rem "Instrument Sans",Arial,sans-serif;color:var(--muted)}
/* servizi come tavole */
.sheets{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line);margin-top:36px}
@media (max-width:900px){.sheets{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:560px){.sheets{grid-template-columns:1fr}}
.sheets article{background:var(--sheet);padding:26px;position:relative;transition:background .3s}.sheets article:hover{background:#fff}
.sheets small{font:500 .72rem "Instrument Sans",Arial,sans-serif;color:var(--green)}.sheets h3{font-size:1.45rem;margin:10px 0 8px}.sheets p{margin:0;color:var(--muted)}
/* catena */
.chain{list-style:none;padding:0;margin:32px 0 0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;border-top:1px solid var(--line)}
@media (max-width:800px){.chain{grid-template-columns:1fr 1fr}}
.chain a{display:grid;gap:4px;padding:20px 16px;text-decoration:none;border-right:1px solid var(--line);height:100%}.chain li:last-child a{border:0}
.chain small{font:500 .75rem "Instrument Sans",Arial,sans-serif;color:var(--muted)}.chain b{font:400 1.45rem "Bodoni Moda",Georgia,serif}.chain span{color:var(--muted);font-size:.95rem}
.chain .me a{background:var(--green);color:#fff}.chain .me small,.chain .me span{color:#DDEFEA}
/* contatti */
.contact{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(24px,5vw,80px)}@media (max-width:900px){.contact{grid-template-columns:1fr}}
.contact dl{margin:28px 0 0;display:grid;gap:14px}.contact dt{font:500 .72rem "Instrument Sans",Arial,sans-serif;color:var(--green);text-transform:uppercase}.contact dd{margin:2px 0 0}
form.f{background:var(--green-d);color:#fff;border-radius:2px;padding:clamp(24px,3vw,44px);display:grid;gap:16px}
.f .row{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media (max-width:560px){.f .row{grid-template-columns:1fr}}
.f label{display:grid;gap:6px;font-weight:600;font-size:.92rem}.f input,.f select,.f textarea{font:1rem "Instrument Sans",Arial;padding:.9rem 1rem;border:0;border-radius:6px;background:#fff;color:var(--ink);width:100%}
.f textarea{min-height:110px}.f input:focus,.f select:focus,.f textarea:focus{outline:3px solid var(--mint);outline-offset:1px}
.f .check{display:flex;gap:10px;font-weight:400;color:#DDEFEA}.f .check input{width:18px;height:18px;flex:none;margin-top:3px;accent-color:var(--mint)}
.f .btn{background:#fff;color:var(--green-d);justify-content:center}.f .err{margin:0;color:#FFD2C4;font-weight:600}.f [aria-invalid=true]{box-shadow:0 0 0 3px #FF9B8A}
.done{background:var(--green-d);color:#fff;border-radius:6px;padding:40px}.done h3{font-size:1.8rem}.done .btn{background:var(--mint);color:var(--bp)}
.ftr{background:var(--ink);color:#B9C7C2;padding:56px 0 32px;font-size:.95rem}.ftr .in{display:grid;grid-template-columns:2fr 1fr 1fr;gap:28px}@media (max-width:800px){.ftr .in{grid-template-columns:1fr}}
.ftr b{color:#fff}.ftr a{color:#E8F0EC;text-decoration:none}.ftr ul{list-style:none;padding:0;margin:8px 0 0;display:grid;gap:6px}.ftr .legal{grid-column:1/-1;border-top:1px solid #ffffff1f;padding-top:16px;font-size:.85rem}
.plain{max-width:820px;margin:0 auto;padding:64px 20px}.plain h1{font-size:2.6rem;margin-bottom:20px}.small{font-size:.85rem;color:var(--muted)}
.phead{max-width:1320px;margin:0 auto;padding:56px 20px 8px}.phead h1{font-size:clamp(2.4rem,1.6rem + 3vw,4.4rem);font-weight:300}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px 22px;max-width:1320px;margin:28px auto 0;padding:0 20px 80px}
@media (max-width:900px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:560px){.grid{grid-template-columns:1fr}}.grid .card{flex:none}

/* titoli in sans serif, serif solo sulle parole importanti (in corsivo) */
h1,h2,h3,.facts b,.big,.chain b,.phase h3,.sheets h3,.card h3,.stepb h3,.svc h3,.work h3,.tel{font-family:"Instrument Sans",Arial,sans-serif!important;font-weight:600!important;letter-spacing:-.025em!important;font-style:normal}
h1 em,h2 em,h3 em,h1 i,h2 i{font-family:"Bodoni Moda",Georgia,serif!important;font-weight:400!important;font-style:italic!important;letter-spacing:-.005em!important}
.big{font-weight:500!important}.chain small{font-family:"Instrument Sans",Arial,sans-serif!important;font-style:normal!important;font-size:.72rem!important;font-weight:600!important;letter-spacing:.18em!important;text-transform:uppercase}
.hero h1{letter-spacing:-.035em!important}
"""
A_JS = COMMON_JS + r"""
// cursore progetto / realtà
document.querySelectorAll(".cmp").forEach(function(c){var on=false;function set(x){var r=c.getBoundingClientRect();var p=Math.max(2,Math.min(98,(x-r.left)/r.width*100));c.style.setProperty("--x",p+"%");c.querySelector("button").setAttribute("aria-valuenow",Math.round(p))}
 c.addEventListener("pointerdown",function(e){on=true;c.setPointerCapture(e.pointerId);set(e.clientX)});c.addEventListener("pointermove",function(e){if(on)set(e.clientX)});c.addEventListener("pointerup",function(){on=false});
 var b=c.querySelector("button");b.addEventListener("keydown",function(e){var v=parseFloat(getComputedStyle(c).getPropertyValue("--x"))||50;if(e.key==="ArrowLeft"){c.style.setProperty("--x",Math.max(2,v-5)+"%");e.preventDefault()}if(e.key==="ArrowRight"){c.style.setProperty("--x",Math.min(98,v+5)+"%");e.preventDefault()}});
 // una piccola dimostrazione quando entra nello schermo
 var shown=false;new IntersectionObserver(function(es){if(es[0].isIntersecting&&!shown&&!matchMedia("(prefers-reduced-motion: reduce)").matches){shown=true;var t0=null;function step(t){if(!t0)t0=t;var k=(t-t0)/1800;var p=50+Math.sin(k*Math.PI*2)*28*(1-k);c.style.setProperty("--x",p+"%");if(k<1)requestAnimationFrame(step);else c.style.setProperty("--x","50%")}requestAnimationFrame(step)}},{threshold:.5}).observe(c)});
// percorso: il numero grande e la barra seguono la fase sullo schermo
var phases=document.querySelectorAll(".phase"),big=document.querySelector(".big"),bars=document.querySelectorAll(".meter i"),ttl=document.querySelector(".pin .ttl");
if(phases.length){var po=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var i=+e.target.dataset.i;phases.forEach(function(p,j){p.classList.toggle("on",j===i)});bars.forEach(function(b,j){b.classList.toggle("on",j<=i)});big.textContent=String(i+1).padStart(2,"0");if(ttl)ttl.textContent=e.target.dataset.t}})},{rootMargin:"-45% 0px -45% 0px"});phases.forEach(function(p){po.observe(p)})}
// che progetto hai in mente
var ans={"nuovo":["Per una casa nuova partiamo dal terreno.",["Verifica del piano regolatore: cosa e quanto si può costruire","Studio di fattibilità con un primo budget","Progetto e domanda di costruzione","Appalti e direzione lavori fino alla consegna"],"Nuova costruzione"],
 "ampliare":["Per ampliare serve quasi sempre una licenza.",["Rilievo di quello che esiste","Soluzioni di ampliamento e costi","Domanda di costruzione","Direzione lavori"],"Ristrutturazione o ampliamento"],
 "ristrutturare":["Per ristrutturare partiamo da un sopralluogo.",["Sopralluogo e rilievo","Progetto degli interventi e budget","Verifica se serve una licenza","Coordinamento delle imprese"],"Ristrutturazione o ampliamento"],
 "terreno":["Prima di comprare un terreno, conviene sapere cosa ci si può fare.",["Verifica del piano regolatore e dei vincoli","Volumetria possibile e prima idea di progetto","Stima dei costi di costruzione","Parere per la banca o per la trattativa"],"Studio di fattibilità"]};
document.querySelectorAll(".opts button").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll(".opts button").forEach(function(x){x.setAttribute("aria-pressed",x===b)});var a=ans[b.dataset.k];var box=document.querySelector(".answer");
 box.innerHTML="<div><b style='font:600 1.45rem \"Instrument Sans\",Arial,sans-serif;letter-spacing:-.02em'>"+a[0]+"</b><ol>"+a[1].map(function(s){return "<li>"+s+"</li>"}).join("")+"</ol></div><a class='btn' href='#contatti' data-kind='"+a[2]+"'>Parliamone →</a>";
 box.querySelector("a").addEventListener("click",function(){var s=document.querySelector("form.f select[name=kind]");if(s)s.value=this.dataset.kind})})});
// galleria trascinabile
document.querySelectorAll(".rail").forEach(function(r){var x0,s0,dn=false,mv=false;r.addEventListener("pointerdown",function(e){if(e.pointerType!=="mouse")return;dn=true;mv=false;x0=e.clientX;s0=r.scrollLeft});
 window.addEventListener("pointermove",function(e){if(!dn)return;if(Math.abs(e.clientX-x0)>4){mv=true;r.classList.add("drag")}r.scrollLeft=s0-(e.clientX-x0)});window.addEventListener("pointerup",function(){dn=false;r.classList.remove("drag")});
 r.addEventListener("click",function(e){if(mv){e.preventDefault();e.stopPropagation()}},true)});
// modulo
document.querySelectorAll("form.f").forEach(function(f){f.addEventListener("submit",function(e){e.preventDefault();var bad=[];f.querySelectorAll("[aria-invalid]").forEach(function(x){x.removeAttribute("aria-invalid")});
 f.querySelectorAll("[required]").forEach(function(x){if(x.type==="checkbox"?!x.checked:!String(x.value).trim()){bad.push(x);x.setAttribute("aria-invalid","true")}});
 if(!f.email.value.trim()&&!f.phone.value.trim()){bad.push(f.email);f.email.setAttribute("aria-invalid","true")}
 var er=f.querySelector(".err");if(bad.length){er.hidden=false;er.textContent="Servono nome, email o telefono e il consenso.";bad[0].focus();return}
 var d={company:"architrend",name:f.name.value,email:f.email.value,phone:f.phone.value,kind:f.kind.value,town:f.town.value,message:f.message.value,website:f.website.value,consent:true,newsletter:f.newsletter.checked};
 var box=document.createElement("div");box.className="done";box.innerHTML="<h3>Invio…</h3>";f.replaceWith(box);
 sendReq(d,box,"<h3>Grazie, abbiamo il tuo progetto.</h3><p>Un architetto di Archi Trend ti richiama per fissare il primo incontro.</p>","Archi Trend · "+d.kind+"\n"+d.name+" "+d.email+" "+d.phone+"\n"+d.town+"\n"+d.message)})});
"""

def archi(d, imgs):
    c = dict(legal="Archi Trend SA", kind="Architettura e progettazione")
    logo = '<svg viewBox="0 0 40 40" aria-hidden="true"><rect x="1" y="1" width="38" height="38" fill="none" stroke="#2F6B62" stroke-width="1.5"/><path d="M8 31 20 9l12 22M13 22h14" fill="none" stroke="#2F6B62" stroke-width="2"/></svg>'
    hdr = f"""<header class="hdr"><div class="in"><a class="logo" href="index.html" aria-label="Archi Trend SA, home">{logo}<span><b>Archi Trend</b><small>ARCHITETTURA · LUGANO · DAL 2009</small></span></a>
<nav class="nav" aria-label="Principale"><a href="index.html#realta">Progetto e realtà</a><a href="index.html#percorso">Come lavoriamo</a><a href="index.html#idea">La tua idea</a><a href="progetti.html">Progetti</a><a href="index.html#contatti">Contatti</a></nav>
<a class="btn" href="index.html#contatti">Prenota un incontro</a><button class="menu" data-menu aria-expanded="false">Menu</button></div></header>"""
    phases = [("Ascolto", "Primo incontro", "Ci racconti come vuoi vivere la casa. Visitiamo il terreno o l'immobile.", ["sopralluogo", "desideri", "budget"]),
              ("Fattibilità", "Cosa si può fare", "Verifichiamo piano regolatore, vincoli e costi prima di disegnare una sola linea.", ["piano regolatore", "volumetria", "stima costi"]),
              ("Progetto", "Il disegno", "Dallo schizzo al progetto definitivo, scegliendo insieme spazi, luce e materiali.", ["schizzi", "3D", "materiali"]),
              ("Licenza", "La domanda di costruzione", "Prepariamo i piani, depositiamo la domanda e seguiamo pubblicazione e risposte del Comune.", ["piani", "pubblicazione", "licenza"]),
              ("Appalti", "Le imprese giuste", "Raccogliamo e confrontiamo i preventivi. Edil Trend è un'opzione, non un obbligo.", ["capitolato", "offerte", "confronto"]),
              ("Cantiere", "Direzione lavori", "Seguiamo il cantiere fino al collaudo: qualità, tempi e costi sotto controllo.", ["riunioni", "controllo costi", "collaudo"])]
    ph = "".join(f'<div class="phase{" on" if i == 0 else ""}" data-i="{i}" data-t="{E(t)}"><span class="tag">{i + 1:02d} · {E(t)}</span><h3>{E(h)}</h3><p>{E(p)}</p><ul>{"".join(f"<li>{E(x)}</li>" for x in li)}</ul></div>' for i, (t, h, p, li) in enumerate(phases))
    services = [("Progettazione architettonica", "Case, palazzine e ampliamenti, dal concetto al progetto esecutivo."), ("Domanda di costruzione", "Piani, deposito, pubblicazione, eventuali opposizioni e licenza."),
                ("Direzione lavori", "Imprese e artigiani coordinati, con qualità, tempi e costi controllati."), ("Rilievi e fattibilità", "Cosa si può costruire su un terreno, prima di investire."),
                ("Perizie e stime", "Valutazioni tecniche e immobiliari per vendite, eredità e banche."), ("Interni", "Distribuzione degli spazi, materiali e finiture.")]
    sv = "".join(f'<article class="reveal"><small>{i + 1:02d}</small><h3>{E(a)}</h3><p>{E(b)}</p></article>' for i, (a, b) in enumerate(services))
    card = lambda k: f'<article class="card"><div class="ph"><img src="assets/img/{imgs[k][0]}" alt="{E(P[k][0])}, {E(P[k][1])}" loading="lazy">{f"<img class=\"b\" src=\"assets/img/{imgs[k][1]}\" alt=\"\" loading=\"lazy\">" if imgs[k][1] else ""}</div><small>{E(P[k][1]).upper()} · {E(P[k][2])}</small><h3>{E(P[k][0])}</h3><p>{E(P[k][3])}</p></article>'
    keys = ["ferrari", "synthesis", "greenhorse", "maraini", "optima", "miracolli", "aurea", "duelaghi"]
    form = f"""<form class="f" novalidate><label>Nome e cognome<input name="name" autocomplete="name" required></label>
<div class="row"><label>Email<input name="email" type="email" autocomplete="email"></label><label>Telefono<input name="phone" type="tel" autocomplete="tel"></label></div>
<div class="row"><label>Il progetto<select name="kind"><option>Nuova costruzione</option><option>Ristrutturazione o ampliamento</option><option>Domanda di costruzione</option><option>Studio di fattibilità</option><option>Perizia o stima</option><option>Interni</option><option>Altro</option></select></label><label>Comune<input name="town" placeholder="es. Lugano"></label></div>
<label>Raccontaci l'idea<textarea name="message" placeholder="Cosa vorresti costruire o cambiare, e in che tempi"></textarea></label><input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
<label class="check"><input type="checkbox" name="consent" required><span>Acconsento a essere ricontattato da Archi Trend SA secondo l'<a href="privacy.html" style="color:#fff">informativa privacy</a>.</span></label>
<label class="check"><input type="checkbox" name="newsletter"><span>Voglio ricevere ogni tanto novità e progetti del Gruppo New Trends (facoltativo).</span></label><p class="err" hidden role="alert"></p><button class="btn" type="submit">Prenota il primo incontro</button></form>"""
    contact = f"""<section class="sec" id="contatti"><div class="in contact"><div class="reveal"><span class="tag">Contatti</span><h2>Parliamo della <i>tua idea</i></h2><p class="lead">Ti richiamiamo per un primo incontro, in ufficio o sul posto.</p>
<dl><dt>Studio</dt><dd>{ADDR}</dd><dt>Telefono</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd><dt>Email</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd><dt>Orari</dt><dd>Lu–Ve 08:30–18:30</dd></dl></div><div class="reveal">{form}</div></div></section>"""
    home = f"""{hdr}<main id="main">
<section class="hero"><div><span class="tag">Archi Trend SA · Gruppo New Trends</span><h1>Ogni casa inizia <i>da una linea.</i></h1>
<p class="lead">Siamo lo studio di architettura del Gruppo New Trends. Disegniamo, otteniamo la licenza e seguiamo il cantiere: un solo referente dal primo schizzo alla consegna.</p>
<div class="acts"><a class="btn" href="#idea">Che progetto hai in mente?</a><a class="btn ghost" href="#realta">Dal disegno alla realtà</a></div></div>
<div class="stage" aria-label="Residenza Ferrari a Tesserete: prima il disegno, poi il progetto"><img class="bp" src="assets/img/{imgs['ferrari'][1]}" alt=""><img class="ph" src="assets/img/{imgs['ferrari'][0]}" alt="Residenza Ferrari, Tesserete"><i class="scan"></i><div class="dim"><span>Residenza Ferrari · Tesserete</span></div></div></section>
<div class="facts"><div><b>2009</b><span>Archi Trend SA a Lugano</span></div><div><b>1991</b><span>il Gruppo New Trends</span></div><div><b>100+</b><span>unità abitative realizzate dal gruppo</span></div><div><b>300+</b><span>professionisti nella rete</span></div></div>
<section class="sec" id="realta"><div class="in"><div class="reveal" style="display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;margin-bottom:28px"><div><span class="tag">Progetto e realtà</span><h2>Trascina e guarda <i>il disegno diventare casa</i></h2></div><p class="hint">Trascina per confrontare</p></div>
<div class="cmp reveal" style="--x:50%"><img src="assets/img/{imgs['optima'][0]}" alt="Residenza Optima a Montagnola"><img class="top" src="assets/img/{imgs['optima'][1]}" alt=""><span class="l a">Progetto</span><span class="l b">Realizzato</span><div class="h"><button type="button" role="slider" aria-label="Sposta tra disegno e realtà" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">↔</button></div></div>
<p class="hint" style="margin-top:12px">Residenza Optima, Montagnola · 6 appartamenti</p></div></section>
<section class="sec" id="percorso" style="background:var(--sheet);border-block:1px solid var(--line)"><div class="in path"><div class="pin"><span class="tag">Come lavoriamo</span><div class="big" aria-hidden="true">01</div><p class="ttl" style="font:600 1.4rem 'Instrument Sans',Arial,sans-serif;letter-spacing:-.02em;margin:4px 0 0">Ascolto</p><div class="meter" aria-hidden="true">{"<i></i>" * 6}</div><p class="lead" style="margin-top:22px">Sei fasi, sempre lo stesso referente. Scorri per seguirle.</p></div><div>{ph}</div></div></section>
<section class="sec"><div class="in"><div class="reveal"><span class="tag">Servizi</span><h2>Cosa disegniamo <i>per te</i></h2></div><div class="sheets">{sv}</div></div></section>
<section class="sec" id="idea"><div class="in"><div class="quiz reveal"><span class="tag" style="color:#CFE7E1">La tua idea</span><h2>Che progetto <i>hai in mente?</i></h2><p class="lead" style="color:#DCEDE8">Scegli la tua situazione: ti diciamo da dove si parte.</p>
<div class="opts" role="group" aria-label="La tua situazione"><button type="button" data-k="nuovo" aria-pressed="false"><small>A</small>Costruire una casa nuova</button><button type="button" data-k="ampliare" aria-pressed="false"><small>B</small>Ampliare la mia casa</button><button type="button" data-k="ristrutturare" aria-pressed="false"><small>C</small>Ristrutturare</button><button type="button" data-k="terreno" aria-pressed="false"><small>D</small>Capire cosa fare su un terreno</button></div>
<div class="answer" aria-live="polite"><p style="margin:0;color:#DCEDE8">Scegli una delle quattro situazioni.</p></div></div></div></section>
<section class="sec" style="padding-bottom:40px"><div class="in reveal" style="display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap"><div><span class="tag">Progetti del gruppo</span><h2>Linee <i>che sono diventate case</i></h2></div><p class="hint">Passa sopra una foto per vedere il progetto</p></div>
<div class="rail" style="max-width:1360px;margin:28px auto 0">{"".join(card(k) for k in keys)}</div><div class="in"><a class="btn ghost" href="progetti.html" style="color:var(--ink)">Tutti i progetti →</a></div></section>
<section class="sec"><div class="in"><span class="tag">Gruppo New Trends</span><h2>Dal terreno alle chiavi, <i>un solo gruppo</i></h2>{chain("architrend", "chain")}</div></section>
{contact}</main>{footer(c['legal'], c['kind'], '')}"""
    pj = f"""{hdr}<main id="main"><div class="phead"><span class="tag">Progetti del gruppo</span><h1>Linee <i>che sono diventate case</i></h1><p class="lead">Residenze del Gruppo New Trends in Ticino. Passa sopra una foto per vedere il disegno.</p></div>
<div class="grid">{"".join(card(k) for k in keys)}</div>{contact}</main>{footer(c['legal'], c['kind'], '')}"""
    pv = f"""{hdr}<main id="main">{privacy(c['legal'])}</main>{footer(c['legal'], c['kind'], '')}"""
    return {"index.html": ("Archi Trend SA · Architettura a Lugano", "Studio di architettura del Gruppo New Trends a Lugano: progetto, licenza edilizia e direzione lavori.", home),
            "progetti.html": ("Progetti · Archi Trend SA", "Progetti del Gruppo New Trends.", pj), "privacy.html": ("Privacy · Archi Trend SA", "Informativa privacy.", pv)}

# ===================== EDIL TREND (mashup Strukt + RenovateHub) =====================
E_FONT = "https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700&family=Instrument+Sans:wght@400..700&display=swap"
E_CSS = COMMON_CSS + """
:root{--ink:#1A1A17;--cream:#EFEBE3;--beige:#EAD9BE;--paper:#F7F4EE;--dark:#1A1A17;--dark2:#24221E;--terra:#B8562C;--terra-d:#94431F;--line:#DED6C8;--muted:#6A645B;--r:22px}
html,body{overflow-x:clip}body{background:var(--cream);color:var(--ink);font:1.04rem/1.6 "Instrument Sans",Arial,sans-serif}.in{max-width:1360px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:"Inter Tight","Instrument Sans",Arial,sans-serif;font-weight:600;letter-spacing:-.035em;line-height:1.02;margin:0;text-wrap:balance}
h2{font-size:clamp(2.1rem,1.3rem + 3vw,4rem)}h2 .soft,h1 .soft{color:#9A938A}
.lbl{display:inline-flex;align-items:center;gap:8px;font:600 .74rem "Instrument Sans";letter-spacing:.14em;text-transform:uppercase;background:#fff;color:var(--ink);padding:7px 12px;border-radius:999px;margin-bottom:20px}
.lbl::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--terra)}.dark .lbl{background:#ffffff14;color:#EDE6DB}
.lead{font-size:clamp(1.05rem,1rem + .3vw,1.2rem);color:var(--muted);max-width:56ch}.dark .lead{color:#B8B0A4}
.sec{padding:clamp(72px,9vw,124px) 0}.dark{background:var(--dark);color:#F1EDE6}
.head2{display:flex;justify-content:space-between;align-items:end;gap:20px 48px;flex-wrap:wrap;margin-bottom:44px}.head2 .lead{max-width:44ch;margin:0}
/* bottoni: pillola con cerchio-freccia */
.btn{display:inline-flex;align-items:center;gap:12px;font:600 .98rem "Instrument Sans";padding:.5rem .55rem .5rem 1.25rem;border-radius:999px;text-decoration:none;cursor:pointer;border:1px solid transparent;background:var(--ink);color:#fff;transition:background .25s,transform .25s}
.btn i{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:#fff;color:var(--ink);font-style:normal;transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.btn:hover i{transform:translateX(3px) rotate(-45deg)}.btn.light{background:#fff;color:var(--ink)}.btn.light i{background:var(--ink);color:#fff}
.btn.terra{background:var(--terra)}.btn.terra:hover{background:var(--terra-d)}.btn.terra i{color:var(--terra)}.btn.ghost{background:transparent;border-color:#ffffff66;color:#fff}.btn.ghost i{background:#ffffff22;color:#fff}
/* header: logo, pillola di navigazione, CTA */
.hdr{position:absolute;top:0;left:0;right:0;z-index:40;padding:22px 0}.hdr .in{display:flex;align-items:center;gap:20px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff;font:600 1.3rem "Inter Tight";letter-spacing:-.02em}.logo svg{width:26px;height:26px}
.pill{display:flex;gap:2px;margin:0 auto;background:#ffffff1f;border:1px solid #ffffff33;backdrop-filter:blur(14px);border-radius:999px;padding:5px}
.pill a{color:#fff;text-decoration:none;padding:.5rem 1rem;border-radius:999px;font-weight:500;font-size:.95rem;transition:background .2s}.pill a:hover,.pill a.on{background:#ffffff26}
.menu{display:none;margin-left:auto;background:#ffffff26;border:1px solid #ffffff40;color:#fff;border-radius:999px;padding:.55rem 1rem;font-weight:600;font-family:inherit;backdrop-filter:blur(10px)}
@media (max-width:980px){.pill,.hdr .btn{display:none}.menu{display:inline-flex}.pill.open{display:flex;position:absolute;top:76px;left:20px;right:20px;flex-direction:column;background:#1A1A17f2;border-radius:18px;padding:10px}}
/* hero: foto in cornice arrotondata, titolo bicolore, scheda contatto, numeri */
.hero{padding:10px 10px 0}.hero .frame{position:relative;border-radius:var(--r);overflow:hidden;min-height:calc(100svh - 56px);padding-top:110px;display:flex;flex-direction:column;justify-content:flex-end;color:#fff;isolation:isolate;background:var(--dark)}
.hero .frame>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;transform:scale(1.08);animation:hz 2.4s cubic-bezier(.2,.7,.2,1) forwards}@keyframes hz{to{transform:scale(1)}}
.hero .frame::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,#1A1A17cc 0%,#1A1A1788 45%,#1A1A1700 80%),linear-gradient(180deg,#1A1A1777 0%,#1A1A1711 35%,#1A1A17dd 100%)}
.hero .body{padding:0 clamp(20px,3vw,44px) 28px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:end}
@media (max-width:900px){.hero .body{grid-template-columns:1fr}}
.hero h1{font-size:clamp(2.7rem,1.2rem + 6vw,7.4rem);letter-spacing:-.05em;line-height:.95}
.hero h1 span{display:block;opacity:0;transform:translateY(30px);animation:up 1.1s cubic-bezier(.2,.7,.2,1) forwards}.hero h1 span:nth-child(2){animation-delay:.18s}.hero h1 .soft{color:#ffffffbf}
@media (max-width:600px){.hero h1{font-size:clamp(2.3rem,10.5vw,3.2rem)}.hero .card{display:none}}
@keyframes up{to{opacity:1;transform:none}}
.hero .sub{max-width:46ch;color:#EDE6DB;margin:22px 0 26px;opacity:0;animation:up 1s ease .5s forwards}.hero .acts{display:flex;gap:12px;flex-wrap:wrap;opacity:0;animation:up 1s ease .65s forwards}
.card{background:#fff;color:var(--ink);border-radius:16px;width:min(340px,100%);overflow:hidden;box-shadow:0 30px 60px -30px #0008;opacity:0;animation:up 1s ease .9s forwards}
.card .t{display:flex;gap:12px;align-items:center;padding:16px 18px}.card .av{width:44px;height:44px;border-radius:50%;background:var(--beige);display:grid;place-items:center;font:700 .95rem "Inter Tight";color:var(--terra-d);position:relative}
.card .av::after{content:"";position:absolute;right:0;bottom:2px;width:11px;height:11px;border-radius:50%;background:#2E9B5B;border:2px solid #fff}
.card b{display:block;font:600 1.02rem "Inter Tight"}.card small{color:var(--muted);font-size:.85rem}
.card .row{display:flex;justify-content:space-between;border-top:1px solid var(--line);padding:10px 18px;font-size:.82rem;color:var(--muted)}.card .row b{display:inline;font:600 .82rem "Instrument Sans";color:#2E9B5B}
.card a{display:flex;justify-content:space-between;align-items:center;background:var(--ink);color:#fff;text-decoration:none;padding:14px 18px;font-weight:600}.card a span{background:var(--terra);width:30px;height:30px;border-radius:50%;display:grid;place-items:center}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;border-top:1px solid #ffffff33;margin:0 clamp(20px,3vw,44px);padding:16px 0 22px;font-size:.88rem;color:#CFC7BB;position:relative}
.stats b{color:#fff;font-weight:600;margin-right:6px}.stats::after{content:"";position:absolute;left:0;right:0;bottom:6px;height:8px;background:repeating-linear-gradient(90deg,#ffffff40 0 1px,transparent 1px 22px)}
@media (max-width:800px){.stats{grid-template-columns:1fr 1fr}}
/* chi siamo + numeri */
.about{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(28px,5vw,80px);align-items:start}@media (max-width:900px){.about{grid-template-columns:1fr}}
.about h2{font-size:clamp(1.9rem,1.2rem + 2.2vw,3.1rem)}
.big{background:#fff;border-radius:var(--r);padding:28px}.big .n{font:600 clamp(4rem,3rem + 4vw,7rem)/1 "Inter Tight";letter-spacing:-.05em}.big .n em{font-style:normal;color:var(--terra)}
.meter{margin-top:18px;display:grid;gap:12px}.meter div{display:grid;grid-template-columns:1fr auto;gap:6px;font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.meter i{grid-column:1/-1;height:3px;background:var(--line);position:relative}.meter i::after{content:"";position:absolute;inset:0 auto 0 0;width:var(--w);background:var(--ink);transform-origin:left;transform:scaleX(0);transition:transform 1.4s cubic-bezier(.2,.7,.2,1)}.in-view .meter i::after{transform:scaleX(1)}
.duo{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line);margin-top:20px}.duo div{padding:18px 0}.duo div+div{border-left:1px solid var(--line);padding-left:18px}.duo b{display:block;font:600 2rem "Inter Tight";letter-spacing:-.03em}.duo span{font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.quote{position:relative;border-radius:var(--r);overflow:hidden;min-height:420px;display:flex;align-items:flex-end;color:#fff}.quote img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.quote div{position:relative;margin:18px;background:#1A1A17b3;backdrop-filter:blur(10px);border-radius:16px;padding:22px 24px}.quote p{font:500 1.3rem/1.35 "Inter Tight";letter-spacing:-.01em;margin:0 0 10px}.quote small{color:#CFC7BB}
/* servizi a schede con foto */
.svc{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}@media (max-width:1000px){.svc{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:560px){.svc{grid-template-columns:1fr}}
.svc a{background:#fff;border-radius:18px;overflow:hidden;text-decoration:none;display:flex;flex-direction:column;transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s}
.svc a:hover{transform:translateY(-6px);box-shadow:0 30px 50px -30px #1A1A1755}.svc .ph{aspect-ratio:4/3;overflow:hidden;margin:8px;border-radius:12px}.svc img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}.svc a:hover img{transform:scale(1.06)}
.svc .tx{padding:8px 18px 18px;display:grid;gap:6px;flex:1}.svc small{display:flex;justify-content:space-between;color:var(--muted);font-size:.78rem;letter-spacing:.12em;text-transform:uppercase}.svc h3{font-size:1.25rem;letter-spacing:-.02em}.svc p{margin:0;color:var(--muted);font-size:.94rem}
.svc .go{margin-top:auto;display:flex;justify-content:space-between;align-items:center;padding-top:14px;font-weight:600;font-size:.9rem}.svc .go i{width:32px;height:32px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;font-style:normal;transition:transform .3s}.svc a:hover .go i{transform:rotate(-45deg)}
/* processo: casa 3D + step a pillole */
.build{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(24px,4vw,64px)}@media (max-width:900px){.build{grid-template-columns:1fr}}
.frame3d{position:sticky;top:20px;align-self:start;aspect-ratio:1/1;max-height:84vh;width:100%;overflow:hidden;border-radius:var(--r);background:var(--dark2);z-index:2}
.frame3d canvas{display:block;width:100%!important;height:100%!important}.frame3d .bar{position:absolute;left:22px;right:22px;top:22px;height:2px;background:#ffffff22;border-radius:2px}.frame3d .bar i{display:block;height:2px;background:var(--beige);width:0;border-radius:2px}
.frame3d .cap3d{position:absolute;left:18px;bottom:18px;font-weight:600;font-size:.85rem;color:#fff;background:#1A1A17b3;backdrop-filter:blur(8px);padding:9px 14px;border-radius:999px}
.frame{display:none}.build:not(.has3d) .frame3d{display:none}.build:not(.has3d) .frame{display:block;position:sticky;top:20px;aspect-ratio:1/1;border-radius:var(--r);overflow:hidden}
.build:not(.has3d) .frame img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1s}.build:not(.has3d) .frame img.on{opacity:1}.frame .bar,.frame .cap{display:none}
.stepb{min-height:64vh;display:flex;flex-direction:column;justify-content:center;opacity:.35;transition:opacity .5s}.stepb.on{opacity:1}
.stepb .st{align-self:flex-start;background:#ffffff1a;color:#EDE6DB;border-radius:999px;padding:7px 14px;font-weight:700;font-size:.82rem;letter-spacing:.06em;transition:background .4s,color .4s}.stepb.on .st{background:var(--beige);color:var(--ink)}
.stepb h3{font-size:clamp(1.7rem,1.2rem + 1.6vw,2.6rem);margin:18px 0 10px}.stepb p{color:#B8B0A4;max-width:42ch;margin:0}.stepb .you{margin-top:14px;color:#EDE6DB}.stepb .you b{color:var(--beige)}
@media (max-width:900px){.frame3d{top:12px;aspect-ratio:auto;height:44vh}.stepb{min-height:62vh}}
/* perché noi */
.why{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(24px,5vw,72px)}@media (max-width:900px){.why{grid-template-columns:1fr}}
.why .ph{border-radius:var(--r);overflow:hidden;aspect-ratio:4/3;margin-top:24px}.why .ph img{width:100%;height:100%;object-fit:cover}
.why .grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media (max-width:560px){.why .grid{grid-template-columns:1fr}}
.why .grid div{background:#fff;border-radius:18px;padding:24px;transition:transform .3s}.why .grid div:hover{transform:translateY(-4px)}.why .grid svg{width:38px;height:38px;padding:8px;border-radius:10px;background:var(--ink);stroke:#fff;fill:none;stroke-width:1.6}
.why h3{font-size:1.12rem;margin:30px 0 6px;letter-spacing:-.02em}.why p{margin:0;color:var(--muted);font-size:.94rem}
/* configuratore in scheda scura */
.cfg{background:var(--dark);color:#F1EDE6;border-radius:var(--r);padding:clamp(26px,4.5vw,64px)}.cfg h2{margin-bottom:6px}
.prog{height:2px;background:#ffffff22;margin:28px 0 30px;border-radius:2px;position:relative}.prog i{position:absolute;left:0;top:0;height:2px;background:var(--beige);width:25%;transition:width .5s ease}
.q{display:none}.q.on{display:block;animation:qin .5s ease}@keyframes qin{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.q .step{display:inline-block;background:var(--beige);color:var(--ink);border-radius:999px;padding:5px 12px;font-weight:700;font-size:.78rem}.q h3{font-size:clamp(1.5rem,1.1rem + 1.4vw,2.2rem);margin:14px 0 22px}
.tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}@media (max-width:800px){.tiles{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:460px){.tiles{grid-template-columns:1fr}}
.tiles button{background:#ffffff0d;border:1px solid #ffffff26;border-radius:14px;padding:18px 16px;text-align:left;font-family:inherit;font-weight:500;font-size:1rem;color:#F1EDE6;cursor:pointer;display:flex;gap:12px;align-items:center;transition:background .2s,border-color .2s,transform .2s}
.tiles button svg{width:24px;height:24px;stroke:var(--beige);fill:none;stroke-width:1.5;flex:none}.tiles button:hover{background:#ffffff17;transform:translateY(-2px)}
.tiles button[aria-pressed=true]{background:var(--beige);color:var(--ink);border-color:var(--beige)}.tiles button[aria-pressed=true] svg{stroke:var(--ink)}
.cfg .nav2{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:26px}.back{background:none;border:0;font-family:inherit;font-weight:500;color:#B8B0A4;cursor:pointer}.back:hover{color:#fff}
.cfg label{display:grid;gap:6px;font-weight:500;font-size:.88rem;color:#B8B0A4}.cfg input,.cfg textarea{font:1rem "Instrument Sans";padding:.85rem 0;border:0;border-bottom:1px solid #ffffff33;border-radius:0;background:transparent;width:100%;color:#fff}
.cfg input:focus,.cfg textarea:focus{outline:0;border-color:var(--beige)}.cfg .row{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-bottom:18px}@media (max-width:560px){.cfg .row{grid-template-columns:1fr}}
.cfg .check{display:flex;gap:10px;font-weight:400;margin-top:12px}.cfg .check input{width:18px;height:18px;flex:none;accent-color:var(--beige);margin-top:3px}.cfg .check a{color:#fff}
.cfg [aria-invalid=true]{border-color:#FF9B8A}.cfg .err{color:#FFB4A6;font-weight:600}.sum{color:#B8B0A4;margin:-8px 0 20px}.sum b{color:#fff;font-weight:600}.done h3{font-size:2rem}
.cfg .btn{background:var(--beige);color:var(--ink)}.cfg .btn i{background:var(--ink);color:#fff}
/* lavori */
.tabs{display:inline-flex;gap:4px;background:#fff;border-radius:999px;padding:5px;margin-bottom:26px}.tabs button{background:none;border:0;border-radius:999px;padding:.55rem 1.1rem;font-family:inherit;font-size:.95rem;font-weight:600;color:var(--muted);cursor:pointer}
.tabs button[aria-pressed=true]{background:var(--ink);color:#fff}
.works{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}@media (max-width:900px){.works{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:560px){.works{grid-template-columns:1fr}}
.work{position:relative;border-radius:18px;overflow:hidden;aspect-ratio:4/3.2;background:var(--dark);color:#fff}.work img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}.work:hover img{transform:scale(1.06)}
.work .t{position:absolute;left:10px;right:10px;bottom:10px;background:#1A1A17b8;backdrop-filter:blur(10px);border-radius:12px;padding:14px 16px;transform:translateY(calc(100% - 64px));transition:transform .5s cubic-bezier(.2,.7,.2,1)}.work:hover .t,.work:focus-within .t{transform:none}
.work small{font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--beige)}.work h3{font-size:1.15rem;margin:4px 0 8px;letter-spacing:-.02em}.work p{margin:0;font-size:.9rem;color:#D8D0C4}.work[hidden]{display:none}
/* FAQ */
.faq{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:clamp(24px,5vw,72px)}@media (max-width:900px){.faq{grid-template-columns:1fr}}
.faq details{background:#fff;border-radius:14px;margin-bottom:10px;padding:0 20px;transition:background .3s}.faq details[open]{background:var(--dark);color:#fff}
.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:16px;align-items:center;padding:18px 0;font-weight:600}.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";flex:none;width:30px;height:30px;border-radius:8px;background:var(--ink);color:#fff;display:grid;place-items:center;font-size:1.2rem;transition:transform .3s}.faq details[open] summary::after{content:"–";background:var(--beige);color:var(--ink)}
.faq details p{margin:0 0 18px;color:#CFC7BB}
/* catena del gruppo */
.chain{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}@media (max-width:800px){.chain{grid-template-columns:1fr 1fr}}
.chain a{display:grid;gap:6px;padding:22px;text-decoration:none;background:#fff;border-radius:18px;height:100%;transition:transform .3s}.chain a:hover{transform:translateY(-4px)}
.chain small{font-weight:700;font-size:.78rem;color:var(--muted)}.chain b{font:600 1.3rem "Inter Tight";letter-spacing:-.02em}.chain span{color:var(--muted);font-size:.94rem}
.chain .me a{background:var(--terra);color:#fff}.chain .me small,.chain .me span{color:#F6DFD2}
/* CTA finale + footer */
.cta{background:var(--beige);border-radius:var(--r);padding:clamp(28px,5vw,64px);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:28px;align-items:end}@media (max-width:800px){.cta{grid-template-columns:1fr}}
.cta h2{font-size:clamp(2rem,1.3rem + 2.6vw,3.6rem)}.cta .soft{color:#8F7F69}.cta ul{list-style:none;padding:0;margin:16px 0 0;display:flex;gap:18px;flex-wrap:wrap;font-weight:600;font-size:.92rem}.cta li::before{content:"✓ ";color:var(--terra)}
.ftr{background:var(--dark);color:#A9A196;margin:10px;border-radius:var(--r);padding:56px 0 24px;font-size:.95rem;overflow:hidden}.ftr .in{display:grid;grid-template-columns:2fr 1fr 1fr;gap:28px}@media (max-width:800px){.ftr .in{grid-template-columns:1fr}}
.ftr b{color:#fff;font-weight:600}.ftr a{color:#E8E1D6;text-decoration:none}.ftr ul{list-style:none;padding:0;margin:8px 0 0;display:grid;gap:6px}.ftr .legal{grid-column:1/-1;border-top:1px solid #ffffff1a;padding-top:16px;font-size:.85rem}
.ftr .word{grid-column:1/-1;font:700 clamp(4rem,14vw,15rem)/.8 "Inter Tight";letter-spacing:-.06em;color:#ffffff0d;margin:24px 0 -8px;white-space:nowrap}
.plain{max-width:820px;margin:0 auto;padding:140px 20px 72px}.plain h1{font-size:2.8rem;margin-bottom:20px}.small{font-size:.85rem;color:var(--muted)}
.subhdr{background:var(--dark);padding-bottom:10px}
"""
E_JS = COMMON_JS + r"""
// barre e numeri che partono quando si vedono
document.querySelectorAll(".about").forEach(function(a){new IntersectionObserver(function(es,o){if(es[0].isIntersecting){a.classList.add("in-view");o.disconnect()}},{threshold:.3}).observe(a)});
document.querySelectorAll("[data-count]").forEach(function(b){new IntersectionObserver(function(es,o){if(!es[0].isIntersecting)return;o.disconnect();var to=+b.dataset.count,suf=b.dataset.suf||"",t0=null;
 function f(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/1500);b.textContent=Math.round(to*(1-Math.pow(1-k,3)))+suf;if(k<1)requestAnimationFrame(f)}requestAnimationFrame(f)},{threshold:.6}).observe(b)});
// fasi: pillola attiva, foto di riserva se manca il 3D
var steps=document.querySelectorAll(".stepb"),pics=document.querySelectorAll(".frame img");
if(steps.length){var so=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var i=+e.target.dataset.i;steps.forEach(function(s,j){s.classList.toggle("on",j===i)});pics.forEach(function(p,j){p.classList.toggle("on",j===i)})}})},{rootMargin:"-45% 0px -45% 0px"});steps.forEach(function(s){so.observe(s)})}
// configuratore
var cfg=document.querySelector(".cfg");if(cfg){var qs=cfg.querySelectorAll(".q"),pr=cfg.querySelector(".prog i"),st={},cur=0;
 function show(i){cur=i;qs.forEach(function(q,j){q.classList.toggle("on",j===i)});pr.style.width=((i+1)/qs.length*100)+"%";var s=cfg.querySelector(".sum");if(s)s.innerHTML=[st.lavoro,st.misura,st.quando].filter(Boolean).map(function(x){return "<b>"+x+"</b>"}).join(" · ")}
 cfg.querySelectorAll(".tiles button").forEach(function(b){b.addEventListener("click",function(){var q=b.closest(".q");q.querySelectorAll(".tiles button").forEach(function(x){x.setAttribute("aria-pressed",x===b)});st[q.dataset.k]=b.dataset.v;setTimeout(function(){show(cur+1)},260)})});
 cfg.querySelectorAll(".back").forEach(function(b){b.addEventListener("click",function(){show(Math.max(0,cur-1))})});
 cfg.querySelector("form").addEventListener("submit",function(e){e.preventDefault();var f=e.target,bad=[];f.querySelectorAll("[aria-invalid]").forEach(function(x){x.removeAttribute("aria-invalid")});
  f.querySelectorAll("[required]").forEach(function(x){if(x.type==="checkbox"?!x.checked:!String(x.value).trim()){bad.push(x);x.setAttribute("aria-invalid","true")}});
  if(!f.email.value.trim()&&!f.phone.value.trim()){bad.push(f.email);f.email.setAttribute("aria-invalid","true")}var er=f.querySelector(".err");
  if(bad.length){er.hidden=false;er.textContent="Servono nome, email o telefono e il consenso.";bad[0].focus();return}
  var d={company:"ediltrend",name:f.name.value,email:f.email.value,phone:f.phone.value,kind:st.lavoro||"Altro",town:f.town.value,message:["Dimensione: "+(st.misura||"—"),"Quando: "+(st.quando||"—"),f.message.value].join("\n"),website:f.website.value,consent:true,newsletter:f.newsletter.checked};
  var box=cfg.querySelector(".q.on");box.innerHTML="<div class='done'><h3>Invio in corso…</h3></div>";pr.style.width="100%";
  sendReq(d,box.querySelector(".done"),"<h3>Grazie, richiesta ricevuta.</h3><p class='lead'>Ti chiamiamo per fissare il sopralluogo. Il preventivo è senza impegno.</p>","Edil Trend · "+d.kind+"\n"+d.name+" "+d.email+" "+d.phone+"\n"+d.town+"\n"+d.message)});show(0)}
// lavori filtrabili
document.querySelectorAll(".tabs button").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll(".tabs button").forEach(function(x){x.setAttribute("aria-pressed",x===b)});var f=b.dataset.f;document.querySelectorAll(".work").forEach(function(w){w.hidden=!!f&&w.dataset.f!==f})})});
"""
ICONS = {
    "bagno": '<path d="M4 12h16v3a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM6 12V6a2 2 0 0 1 4 0"/>', "cucina": '<path d="M4 4h16v16H4zM4 10h16M9 14h6"/>',
    "appartamento": '<path d="M5 21V4h14v17M9 8h2M13 8h2M9 12h2M13 12h2M10 21v-4h4v4"/>', "casa": '<path d="M3 11 12 4l9 7M6 10v10h12V10"/>',
    "facciata": '<path d="M4 20V8l8-4 8 4v12M8 20v-6h8v6M4 12h16"/>', "muratura": '<path d="M3 6h18v4H3zM3 14h18v4H3zM9 6v4M15 10v4M9 14v4"/>',
    "nuova": '<path d="M4 20h16M6 20V9l6-5 6 5v11"/>', "altro": '<path d="M12 5v14M5 12h14"/>',
    "prezzo": '<path d="M5 4h10l4 4v12H5zM9 12h6M9 16h4"/>', "uno": '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c1-4 4-6 7-6s6 2 7 6"/>',
    "ordine": '<path d="M4 7h16M4 12h10M4 17h7"/>', "dopo": '<path d="M12 3 4 7v5c0 5 3.5 8 8 9 4.5-1 8-4 8-9V7z"/><path d="m9 12 2 2 4-4"/>',
}
ARROW = '<i aria-hidden="true">→</i>'

def edil(d, imgs):
    c = dict(legal="Edil Trend SA", kind="Impresa generale e costruzioni")
    logo = '<svg viewBox="0 0 26 26" aria-hidden="true"><path d="M3 23V9l10-6 10 6v14" fill="none" stroke="#fff" stroke-width="2.2"/><path d="M9 23v-8h8v8" fill="#B8562C"/></svg>'
    def hdr(cur="home"):
        links = [("index.html", "Home", "home"), ("index.html#servizi", "Servizi", "svc"), ("index.html#cantiere", "Come lavoriamo", "how"), ("index.html#lavori", "Lavori", "works"), ("index.html#faq", "Domande", "faq")]
        return f"""<header class="hdr"><div class="in"><a class="logo" href="index.html" aria-label="Edil Trend SA, home">{logo}Edil Trend</a>
<nav class="pill nav" aria-label="Principale">{"".join(f'<a href="{h}" class="{"on" if k == cur else ""}">{t}</a>' for h, t, k in links)}</nav>
<a class="btn light" href="index.html#preventivo">Preventivo {ARROW}</a><button class="menu" data-menu aria-expanded="false">Menu</button></div></header>"""
    steps = [("Il sopralluogo", "Veniamo sul posto, misuriamo e ascoltiamo cosa ti serve davvero.", "un appuntamento sul posto", "synthesis"),
             ("Il preventivo", "Voci, quantità e prezzi scritti con chiarezza, senza sorprese.", "un preventivo dettagliato", "optima"),
             ("Il contratto", "Prezzo, tempi e capitolato firmati prima di aprire il cantiere.", "date e prezzo concordati", "miracolli"),
             ("Il cantiere", "Un capocantiere coordina tutti gli artigiani e ti tiene aggiornato.", "un solo referente", "ferrari"),
             ("La consegna", "Collaudo insieme, ogni dettaglio sistemato. Dopo, restiamo il tuo riferimento.", "le chiavi e l'assistenza", "motta")]
    frame = '<div class="frame">' + "".join(f'<img class="{"on" if i == 0 else ""}" src="assets/img/{imgs[k][0]}" alt="" loading="lazy">' for i, (_, _, _, k) in enumerate(steps)) + '</div>'
    sb = "".join(f'<div class="stepb{" on" if i == 0 else ""}" data-i="{i}"><span class="st">STEP {i + 1:02d}</span><h3>{E(h)}</h3><p>{E(p)}</p><p class="you">Ricevi: <b>{E(y)}</b></p></div>' for i, (h, p, y, _) in enumerate(steps))
    services = [("Impresa generale", "Un solo contratto per tutta l'opera: coordiniamo gli artigiani e rispondiamo noi del risultato.", "Chiavi in mano", "maraini"),
                ("Nuove costruzioni", "Case, ville e palazzine residenziali, dalle fondazioni alle finiture.", "Residenziale", "ferrari"),
                ("Ristrutturazioni", "Appartamenti, case di nucleo e stabili: ridiamo valore a ciò che esiste.", "Rinnovo", "motta"),
                ("Opere di capomastro", "Murature, tramezze, aperture e intonaci, eseguiti con cura.", "Muratura", "magliaso")]
    sv = "".join(f'<a class="reveal" href="#preventivo"><div class="ph"><img src="assets/img/{imgs[k][0]}" alt="" loading="lazy"></div><div class="tx"><small><span>{i + 1:02d}</span><span>{E(tag)}</span></small><h3>{E(a)}</h3><p>{E(b)}</p><span class="go">Richiedi un preventivo <i>→</i></span></div></a>' for i, (a, b, tag, k) in enumerate(services))
    why = [("prezzo", "Prezzo scritto", "Voci e quantità nero su bianco prima di iniziare: sai sempre quanto spendi."), ("uno", "Un solo referente", "Un capocantiere che coordina tutto e un numero da chiamare."),
           ("ordine", "Cantiere in ordine", "Programma lavori chiaro, pulizia e rispetto di chi abita vicino."), ("dopo", "Dopo la consegna", "Restiamo il tuo riferimento anche quando il cantiere è chiuso.")]
    wy = "".join(f'<div class="reveal"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[ic]}</svg><h3>{E(a)}</h3><p>{E(b)}</p></div>' for ic, a, b in why)
    tiles = lambda items: '<div class="tiles">' + "".join(f'<button type="button" data-v="{E(v)}" aria-pressed="false">{f"<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\">{ICONS[ic]}</svg>" if ic else ""}<span>{E(v)}</span></button>' for v, ic in items) + "</div>"
    cfg = f"""<div class="cfg reveal dark"><span class="lbl">Preventivo</span><h2>Hai un progetto? <span class="soft">Costruiamolo insieme.</span></h2><p class="lead">Quattro domande, un minuto. Poi ti chiamiamo per il sopralluogo, senza impegno.</p><div class="prog" aria-hidden="true"><i></i></div>
<div class="q" data-k="lavoro"><span class="step">STEP 01 / 04</span><h3>Di che lavoro si tratta?</h3>{tiles([("Bagno", "bagno"), ("Cucina", "cucina"), ("Appartamento intero", "appartamento"), ("Casa", "casa"), ("Facciata o tetto", "facciata"), ("Opere di muratura", "muratura"), ("Nuova costruzione", "nuova"), ("Altro", "altro")])}</div>
<div class="q" data-k="misura"><span class="step">STEP 02 / 04</span><h3>Quanto è grande la superficie?</h3>{tiles([("Meno di 30 m²", None), ("30–80 m²", None), ("80–150 m²", None), ("Più di 150 m²", None), ("Non lo so ancora", None)])}<div class="nav2"><button class="back" type="button">← Indietro</button></div></div>
<div class="q" data-k="quando"><span class="step">STEP 03 / 04</span><h3>Quando vorresti iniziare?</h3>{tiles([("Il prima possibile", None), ("Entro 3 mesi", None), ("Tra 3 e 6 mesi", None), ("Sto valutando", None)])}<div class="nav2"><button class="back" type="button">← Indietro</button></div></div>
<div class="q" data-k="contatti"><span class="step">STEP 04 / 04</span><h3>Dove possiamo ricontattarti?</h3><p class="sum"></p><form novalidate><div class="row"><label>Nome e cognome<input name="name" autocomplete="name" required></label><label>Comune del lavoro<input name="town" placeholder="es. Lugano"></label></div>
<div class="row"><label>Email<input name="email" type="email" autocomplete="email"></label><label>Telefono<input name="phone" type="tel" autocomplete="tel"></label></div>
<label>Altre informazioni (facoltativo)<textarea name="message" rows="2" placeholder="es. bagno al secondo piano, senza ascensore"></textarea></label><input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
<label class="check"><input type="checkbox" name="consent" required><span>Acconsento a essere ricontattato da Edil Trend SA secondo l'<a href="privacy.html">informativa privacy</a>.</span></label>
<label class="check"><input type="checkbox" name="newsletter"><span>Desidero ricevere occasionalmente novità del Gruppo New Trends (facoltativo).</span></label><p class="err" hidden role="alert"></p>
<div class="nav2"><button class="back" type="button">← Indietro</button><button class="btn" type="submit">Richiedi il sopralluogo {ARROW}</button></div></form></div></div>"""
    works = ["maraini", "fortuna", "optima", "miracolli", "ferrari", "magliaso", "corteglia", "motta", "pregassona", "montagnola"]
    wk = "".join(f'<article class="work reveal" data-f="{P[k][5]}" tabindex="0"><img src="assets/img/{imgs[k][0]}" alt="{E(P[k][0])}, {E(P[k][1])}" loading="lazy"><div class="t"><small>{E(P[k][1])}</small><h3>{E(P[k][0])}</h3><p>{E(P[k][2])} · {E(P[k][3])}</p></div></article>' for k in works)
    tabs = '<div class="tabs" role="group" aria-label="Filtra i lavori"><button type="button" data-f="" aria-pressed="true">Tutti</button><button type="button" data-f="new" aria-pressed="false">Nuove costruzioni</button><button type="button" data-f="ren" aria-pressed="false">Ristrutturazioni</button></div>'
    faqs = [("Fate anche piccoli lavori?", "Sì, anche opere di muratura e piccole ristrutturazioni. Raccontaci il lavoro e ti diciamo come possiamo aiutarti."),
            ("Il sopralluogo e il preventivo si pagano?", "No: per ristrutturazioni e costruzioni il sopralluogo e il preventivo sono senza impegno."),
            ("Serve un architetto?", "Per i lavori che richiedono una licenza ti affianchiamo Archi Trend, lo studio di architettura del gruppo, oppure lavoriamo con il tuo architetto."),
            ("Chi seguo durante il cantiere?", "Un capocantiere di riferimento: coordina gli artigiani e ti aggiorna sull'avanzamento."),
            ("In quali zone lavorate?", "Soprattutto nel Luganese e nel resto del Ticino.")]
    fq = "".join(f'<details{" open" if i == 0 else ""}><summary>{E(q)}</summary><p>{E(a)}</p></details>' for i, (q, a) in enumerate(faqs))
    home = f"""<section class="hero" id="main-hero"><div class="frame">{hdr()}<img src="assets/img/{imgs['greenhorse'][0]}" alt="" fetchpriority="high">
<div class="body"><div><h1><span class="soft">Case costruite</span><span>per durare.</span></h1>
<p class="sub">Impresa generale del Gruppo New Trends a Lugano: nuove costruzioni, ristrutturazioni e opere di capomastro, con prezzo scritto e tempi chiari dal 1999.</p>
<div class="acts"><a class="btn light" href="#preventivo">Richiedi un preventivo {ARROW}</a><a class="btn ghost" href="#lavori">Vedi i lavori {ARROW}</a></div></div>
<div class="card" aria-label="Contatto diretto"><div class="t"><span class="av">ET</span><div><b>Ufficio tecnico</b><small>Edil Trend SA · Lugano</small></div></div><div class="row"><b>● Risponde una persona</b><span>Lu–Ve 08:30–18:30</span></div><a href="#preventivo">Prenota un sopralluogo <span>→</span></a></div></div>
<div class="stats"><span><b>Dal 1999</b>a Lugano</span><span><b data-count="100" data-suf="+">100+</b>unità del gruppo</span><span><b data-count="300" data-suf="+">300+</b>professionisti in rete</span><span><b>1</b>referente per cantiere</span></div></div></section>
<main id="main">
<section class="sec"><div class="in about"><div class="reveal"><span class="lbl">Chi siamo</span><h2>Rendiamo il cantiere <span class="soft">prevedibile dal primo giorno.</span></h2>
<div class="big" style="margin-top:28px"><div class="n">1<em>.</em></div><p class="lead" style="margin:8px 0 0">Un solo contratto e un solo referente, dalla platea alle finiture.</p>
<div class="meter"><div><span>Prezzo scritto prima di iniziare</span><span>sempre</span><i style="--w:100%"></i></div><div><span>Artigiani coordinati da noi</span><span>tutti</span><i style="--w:100%"></i></div></div>
<div class="duo"><div><b data-count="100" data-suf="+">100+</b><span>unità realizzate dal gruppo</span></div><div><b>1999</b><span>anno di fondazione</span></div></div></div></div>
<div class="quote reveal"><img src="assets/img/{imgs['ferrari'][0]}" alt="Residenza Ferrari, Tesserete" loading="lazy"><div><p>«Un buon cantiere comincia da un buon preventivo: per questo lo scriviamo voce per voce, prima di aprire il cantiere.»</p><small>Edil Trend SA · Impresa generale</small></div></div></div></section>
<section class="sec" id="servizi" style="padding-top:0"><div class="in"><div class="head2"><div><span class="lbl">Servizi</span><h2>Dalla platea alle finiture, <span class="soft">un'impresa sola.</span></h2></div><p class="lead">Coordiniamo tutto il ciclo del lavoro, così non devi tenere insieme imprese e artigiani diversi.</p></div><div class="svc">{sv}</div></div></section>
<section class="sec dark" id="cantiere"><div class="in"><div class="head2"><div><span class="lbl">Come lavoriamo</span><h2>Semplice, <span class="soft" style="color:#8C857B">dall'inizio alla fine.</span></h2></div><p class="lead">Scorri: mentre leggi le fasi, la casa si costruisce davanti a te.</p></div>
<div class="build"><div class="frame3d" data-bg="#24221E" data-ground="#2C2925" data-lot="#34302B" aria-label="Una casa che si costruisce mentre scorri le cinque fasi"><div class="bar"><i></i></div><span class="cap3d">Tracciamento sul terreno · 0%</span></div>{frame}<div>{sb}</div></div></div></section>
<section class="sec"><div class="in why"><div class="reveal"><span class="lbl">Perché noi</span><h2>Perché i clienti <span class="soft">ci affidano la loro casa.</span></h2><p class="lead" style="margin-top:16px">Niente scorciatoie, niente sorprese: un lavoro fatto con chiarezza e cura.</p><div class="ph"><img src="assets/img/{imgs['optima'][0]}" alt="Residenza Optima, Montagnola" loading="lazy"></div></div><div class="grid">{wy}</div></div></section>
<section class="sec" id="preventivo" style="padding-top:0"><div class="in">{cfg}</div></section>
<section class="sec" id="lavori" style="padding-top:0"><div class="in"><div class="head2"><div><span class="lbl">Lavori del gruppo</span><h2>Costruito con cura, <span class="soft">consegnato con precisione.</span></h2></div>{tabs}</div><div class="works">{wk}</div>
<p class="small" style="margin-top:18px">Progetti seguiti dalle aziende del Gruppo New Trends. Passa sopra una foto per i dettagli.</p></div></section>
<section class="sec" id="faq" style="padding-top:0"><div class="in faq"><div><span class="lbl">Domande</span><h2>Domande, <span class="soft">risposte.</span></h2><p class="lead" style="margin-top:16px">Non trovi quello che cerchi? Chiamaci al <a href="tel:{TEL}">{PHONE}</a>.</p></div><div>{fq}</div></div></section>
<section class="sec" style="padding-top:0"><div class="in"><div class="head2"><div><span class="lbl">Gruppo New Trends</span><h2>Dal terreno alle chiavi, <span class="soft">un solo gruppo.</span></h2></div></div>{chain("ediltrend", "chain")}</div></section>
<section class="sec" id="contatti" style="padding-top:0"><div class="in"><div class="cta reveal"><div><span class="lbl">Iniziamo</span><h2>Pronto a costruire <span class="soft">o rinnovare casa?</span></h2><ul><li>Sopralluogo senza impegno</li><li>Preventivo scritto</li><li>Un solo referente</li></ul></div>
<div style="display:grid;gap:14px;justify-items:start"><p style="margin:0;font-size:1.05rem">{ADDR}<br><a href="tel:{TEL}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a></p><a class="btn" href="#preventivo">Richiedi un preventivo {ARROW}</a></div></div></div></section>
</main>{footer(c['legal'], c['kind'], '').replace('<p class="legal">', '<div class="word" aria-hidden="true">EDIL TREND</div><p class="legal">')}<script type="module" src="assets/casa3d.js"></script>"""
    sub = f'<div class="subhdr">{hdr("works")}<div style="height:96px"></div></div>'
    pv = f"""{sub}<main id="main">{privacy(c['legal'])}</main>{footer(c['legal'], c['kind'], '')}"""
    pj = f"""{sub}<main id="main"><section class="sec"><div class="in"><span class="lbl">Lavori del gruppo</span><h1 style="font-size:clamp(2.6rem,1.6rem + 3.6vw,4.8rem);margin-bottom:26px">Costruito con cura, <span class="soft">consegnato con precisione.</span></h1>{tabs}<div class="works">{wk}</div></div></section></main>{footer(c['legal'], c['kind'], '')}"""
    return {"index.html": ("Edil Trend SA · Impresa generale a Lugano", "Impresa generale del Gruppo New Trends a Lugano: nuove costruzioni, ristrutturazioni e opere di capomastro.", home),
            "progetti.html": ("Lavori · Edil Trend SA", "Lavori del Gruppo New Trends.", pj), "privacy.html": ("Privacy · Edil Trend SA", "Informativa privacy.", pv)}

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    for co, fn, css, js, font, color, letter in (("architrend", archi, A_CSS, A_JS, A_FONT, "#2F6B62", "A"), ("ediltrend", edil, E_CSS, E_JS, E_FONT, "#B4532A", "E")):
        d = os.path.join(OUT, co); os.makedirs(os.path.join(d, "assets", "img"))
        open(os.path.join(d, "assets", "site.css"), "w").write(css); open(os.path.join(d, "assets", "app.js"), "w").write("(function(){" + js + "})();")
        open(os.path.join(d, "favicon.svg"), "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="{color}"/><text x="32" y="43" font-family="Georgia,serif" font-size="30" fill="#fff" text-anchor="middle">{letter}T</text></svg>')
        imgs = {}
        for k, p in P.items():
            stem = p[4]; ph = stem[:40] + "-ph.jpg"; bp = stem[:40] + "-bp.jpg"
            save_img(find_src(stem), os.path.join(d, "assets", "img", ph), 1400 if k in ("ferrari", "greenhorse", "optima") else 1000)
            has_bp = os.path.exists(os.path.join(BP, bp))
            if has_bp: save_img(os.path.join(BP, bp), os.path.join(d, "assets", "img", bp), 1400)
            imgs[k] = (ph, bp if has_bp else None)
        v = hashlib.sha256((css + js).encode()).hexdigest()[:10]
        for name, (t, desc, body) in fn(d, imgs).items():
            open(os.path.join(d, name), "w").write(doc(co, t, desc, font, css, body, js, v))
        open(os.path.join(d, "contatti.html"), "w").write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=index.html#contatti"><a href="index.html#contatti">Contatti</a>')
        open(os.path.join(d, "servizi.html"), "w").write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=index.html"><a href="index.html">Home</a>')
        open(os.path.join(d, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
        if co == "ediltrend": shutil.copy(os.path.join(HERE, "src", "casa3d.js"), os.path.join(d, "assets", "casa3d.js"))
    print("ok")

if __name__ == "__main__":
    build()
