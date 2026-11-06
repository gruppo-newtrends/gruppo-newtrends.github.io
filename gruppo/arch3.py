# -*- coding: utf-8 -*-
"""Archi Trend, versione 4: struttura e stile come lunarch.framer.website (nero, Urbanist, linee sottili, foto a tutta larghezza),
ma con animazioni leggere (solo comparsa morbida) e pensato per far contattare lo studio: invito in alto, dopo i lavori,
dopo il processo, barra fissa sul telefono e modulo breve collegato al CRM.
Niente premi, recensioni, fondatore o numeri inventati: solo fatti del gruppo e progetti veri.
Uso: python3 -E -s arch3.py [cartella]  (predefinita out/architrend-v4)."""
import hashlib, os, shutil, sys
from PIL import Image
import build2 as b2
from build2 import E, P, ADDR, PHONE, TEL, MAIL, WA, SITES, find_src

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "architrend-v4")
FONT = "https://fonts.googleapis.com/css2?family=Urbanist:wght@300;400;500;600&display=swap"
AR = '<svg class="ar" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>'

CSS = b2.COMMON_CSS + """
:root{--bg:#0A0A0A;--bg2:#171717;--bg3:#262626;--fg:#fff;--mid:#A3A3A3;--dim:#737373;--line:#262626;--gold:#B8962E}
html{scroll-behavior:smooth}html,body{overflow-x:clip}body{background:var(--bg);color:var(--fg);font:400 1.02rem/1.6 Urbanist,Arial,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:1320px;margin:0 auto;padding:0 clamp(18px,4vw,84px)}
h1,h2,h3{font-family:Urbanist,Arial,sans-serif;font-weight:500;letter-spacing:-.02em;line-height:1.1;margin:0;text-wrap:balance}
h2{font-size:clamp(2rem,1.4rem + 2vw,3rem)}h3{font-weight:500}p{margin:0}.mid{color:var(--mid)}
/* linee verticali sottili ai lati della pagina, come nel riferimento */
main{position:relative}main::before,main::after{content:"";position:fixed;top:0;bottom:0;width:1px;background:var(--line);z-index:0;pointer-events:none}main::before{left:max(16px,calc(50% - 660px))}main::after{right:max(16px,calc(50% - 660px))}
@media (max-width:700px){main::before,main::after{display:none}}
section{position:relative;z-index:1}.sec{padding:clamp(72px,9vw,120px) 0;border-top:1px solid var(--line)}
.chip{display:inline-block;background:var(--bg3);color:#D4D4D4;font-weight:600;font-size:.82rem;letter-spacing:.04em;text-transform:uppercase;padding:7px 9px;margin-bottom:22px}
.btn{display:inline-flex;align-items:center;gap:10px;background:#fff;color:#0A0A0A;padding:13px 24px;font:500 1rem Urbanist,Arial;text-decoration:none;border:1px solid #fff;cursor:pointer;transition:background .25s,color .25s}
.btn:hover{background:transparent;color:#fff}.btn.ghost{background:transparent;color:#fff;border-color:#525252}.btn.ghost:hover{border-color:#fff}
.ar{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.8;transition:transform .3s}.btn:hover .ar,a:hover>.ar{transform:translate(2px,-2px)}
/* header */
.hdr{position:fixed;top:0;left:0;right:0;z-index:60;transition:background .3s,border-color .3s;border-bottom:1px solid transparent}.hdr.s{background:#0A0A0Ae6;backdrop-filter:blur(14px);border-color:var(--line)}
.hdr .wrap{display:flex;align-items:center;gap:28px;height:70px}.logo{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font:500 1.45rem/1 Urbanist;letter-spacing:-.02em}.logo svg{width:30px;height:30px}
.nav{display:flex;gap:30px;margin-left:auto}.nav a{color:#fff;text-decoration:none;font-size:1rem;opacity:.9}.nav a:hover{opacity:1;text-decoration:underline;text-underline-offset:6px}
.hdr .btn{padding:9px 16px}.menu{display:none}
@media (max-width:960px){.nav{display:none}.hdr .btn{margin-left:auto}.menu{display:inline-flex;background:none;border:1px solid #525252;color:#fff;padding:9px 14px;font:500 .95rem Urbanist}
 .nav.open{display:flex;flex-direction:column;position:absolute;top:70px;left:0;right:0;background:#0A0A0A;border-bottom:1px solid var(--line);padding:14px 20px 20px;gap:16px}}
@media (max-width:420px){.hdr .btn{display:none}.menu{margin-left:auto}}
/* hero */
.hero{position:relative;min-height:100svh;display:flex;align-items:flex-end;isolation:isolate;overflow:hidden}
.hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;animation:hz 2.4s cubic-bezier(.2,.7,.2,1) both}@keyframes hz{from{transform:scale(1.06)}}
.hero::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,#0A0A0A99 0%,#0A0A0A00 22%,#0A0A0A55 50%,#0A0A0Af5 100%),linear-gradient(90deg,#0A0A0Ab3 0%,#0A0A0A40 45%,#0A0A0A00 70%)}
.hero .wrap{width:100%;padding-bottom:clamp(40px,7vh,80px)}.hero h1{font-size:clamp(2.5rem,1.4rem + 3.6vw,4.2rem);max-width:15ch}
.hero p{max-width:56ch;margin:22px 0 32px;color:#E5E5E5;font-size:1.12rem}.hero .acts{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.trust{display:flex;gap:10px 26px;flex-wrap:wrap;margin-top:34px;padding-top:20px;border-top:1px solid #ffffff2e;color:#D4D4D4;font-size:.95rem}.trust b{color:#fff;font-weight:600}
.up{opacity:0;transform:translateY(18px);animation:up .9s cubic-bezier(.2,.7,.2,1) forwards}.up.d1{animation-delay:.12s}.up.d2{animation-delay:.24s}.up.d3{animation-delay:.36s}@keyframes up{to{opacity:1;transform:none}}
/* introduzione */
.intro{text-align:center;max-width:820px;margin:0 auto}.intro p{font-size:clamp(1.35rem,1.1rem + .9vw,1.9rem);line-height:1.35;color:#fff}.intro p span{color:var(--dim)}.intro .btn{margin-top:34px}
/* competenze: tre colonne con linee */
.exp{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.exp>div{padding:34px clamp(18px,2.4vw,34px) 0;display:flex;flex-direction:column;gap:14px;border-left:1px solid var(--line)}.exp>div:first-child{border-left:0}
.exp small{color:var(--dim);font-size:.95rem}.exp h3{font-size:1.45rem}.exp p{color:var(--mid)}.exp img{margin:22px calc(-1 * clamp(18px,2.4vw,34px)) 0;width:calc(100% + 2 * clamp(18px,2.4vw,34px));aspect-ratio:436/250;object-fit:cover;filter:grayscale(.15)}
@media (max-width:900px){.exp{grid-template-columns:1fr}.exp>div{border-left:0;border-top:1px solid var(--line);padding-bottom:0}.exp>div:first-child{border-top:0}}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr))}.stats div{padding:34px clamp(18px,2.4vw,32px);border-left:1px solid var(--line)}.stats div:first-child{border-left:0}
.stats b{display:block;font-size:2rem;font-weight:500;color:#D4D4D4}.stats span{color:var(--dim)}@media (max-width:800px){.stats{grid-template-columns:1fr 1fr}.stats div:nth-child(3){border-left:0}.stats div:nth-child(n+3){border-top:1px solid var(--line)}}
/* lavori: foto a tutta larghezza, senza effetti pesanti */
.wt{text-align:center;padding:clamp(60px,8vw,110px) 0}.wt h2{font-size:clamp(2.2rem,1.4rem + 2.6vw,3.4rem)}.wt p{margin-top:14px}
.work{position:relative;display:block;height:min(88vh,820px);min-height:440px;overflow:hidden;color:#fff;text-decoration:none;isolation:isolate}
.work img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;transition:transform 1.6s cubic-bezier(.2,.7,.2,1)}.work:hover img{transform:scale(1.03)}
.work::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,#0A0A0A00 45%,#0A0A0Ad9 100%)}
.work .t{position:absolute;left:0;right:0;bottom:0}.work .wrap{padding-bottom:44px}.tags{display:flex;gap:8px;margin-bottom:14px}.tags span{background:#ffffff26;backdrop-filter:blur(8px);font-size:.78rem;font-weight:600;letter-spacing:.06em;padding:5px 9px}
.work h3{font-size:clamp(1.8rem,1.3rem + 1.6vw,2.7rem)}.work p{color:#D4D4D4;margin-top:8px}
.after{display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;padding:34px 0}.after p{font-size:1.2rem}
/* progetto e realtà */
.ba{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}@media (max-width:980px){.ba{grid-template-columns:1fr 1fr}}@media (max-width:620px){.ba{grid-template-columns:1fr}}
.cmp{position:relative;aspect-ratio:4/3;overflow:hidden;--x:50%;touch-action:pan-y;cursor:ew-resize;background:var(--bg2)}.cmp img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;pointer-events:none}.cmp .a{clip-path:inset(0 0 0 var(--x))}
.cmp .ln{position:absolute;top:0;bottom:0;left:var(--x);width:1px;background:#fff}.cmp .hd{position:absolute;top:50%;left:var(--x);width:44px;height:44px;border-radius:50%;background:#fff;color:#0A0A0A;transform:translate(-50%,-50%);display:grid;place-items:center;font-weight:600;letter-spacing:3px}
.cmp input{position:absolute;inset:0;width:100%;height:100%;opacity:0;margin:0;cursor:ew-resize}.cmp input:focus-visible+.hd{outline:2px solid var(--gold);outline-offset:3px}
.cmp .lb{position:absolute;top:12px;background:#0A0A0Ab3;font-size:.78rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:5px 9px;pointer-events:none}.cmp .l1{left:12px}.cmp .l2{right:12px}
.ba h3{font-size:1.15rem;margin-top:14px}.ba p{color:var(--dim);font-size:.95rem}
/* processo: fasi a fisarmonica e immagine che cambia */
.proc{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(30px,5vw,80px);align-items:start}@media (max-width:900px){.proc{grid-template-columns:1fr}}
.acc details{border-bottom:1px solid var(--line)}.acc summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:24px 0;font-size:1.3rem;font-weight:500;color:var(--mid);transition:color .25s}
.acc summary::-webkit-details-marker{display:none}.acc summary::after{content:"";width:9px;height:9px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:rotate(45deg);transition:transform .3s;margin-right:4px}
.acc details[open] summary{color:#fff}.acc details[open] summary::after{transform:rotate(-135deg)}.acc details p{color:var(--mid);padding:0 0 24px;max-width:52ch}.acc summary:hover{color:#fff}
.pimg{position:sticky;top:96px;aspect-ratio:4/3;overflow:hidden;background:var(--bg2)}.pimg img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .6s}.pimg img.on{opacity:1}
.pimg span{position:absolute;left:12px;bottom:12px;background:#0A0A0Ab3;font-size:.8rem;padding:6px 10px}
/* perché noi */
.why{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border-top:1px solid var(--line);margin-top:50px}@media (max-width:760px){.why{grid-template-columns:1fr}}
.why div{padding:34px clamp(18px,2.4vw,34px);border-bottom:1px solid var(--line)}.why div:nth-child(odd){border-right:1px solid var(--line)}@media (max-width:760px){.why div:nth-child(odd){border-right:0}}
.why svg{width:30px;height:30px;stroke:var(--gold);fill:none;stroke-width:1.4}.why h3{font-size:1.3rem;margin:20px 0 10px}.why p{color:var(--mid)}
/* citazione del gruppo */
.quote{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:clamp(30px,5vw,70px);align-items:center}@media (max-width:900px){.quote{grid-template-columns:1fr}}
.quote blockquote{margin:0;font-size:clamp(1.6rem,1.2rem + 1.4vw,2.4rem);line-height:1.25}.quote p{color:var(--mid);margin-top:22px;max-width:54ch}.quote img{width:100%;aspect-ratio:4/5;object-fit:cover}
.chain{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border:1px solid var(--line);margin-top:34px;list-style:none;padding:0}
.chain li{border-left:1px solid var(--line)}.chain li:nth-child(odd){border-left:0}.chain li:nth-child(n+3){border-top:1px solid var(--line)}.chain a{display:grid;gap:6px;padding:20px;text-decoration:none;height:100%}.chain small{color:var(--dim)}.chain b{font-weight:500;font-size:1.1rem}.chain span{color:var(--mid);font-size:.93rem}
.chain .me a{background:#fff;color:#0A0A0A}.chain .me span,.chain .me small{color:#525252}
/* domande */
.faq{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.3fr);gap:clamp(30px,5vw,80px)}@media (max-width:900px){.faq{grid-template-columns:1fr}}.faq .mid{margin-top:16px;max-width:42ch}
.faq details{border-bottom:1px solid var(--line)}.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:20px;padding:20px 0;font-size:1.08rem;font-weight:500}.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-size:1.4rem;line-height:1;color:var(--mid);transition:transform .3s}.faq details[open] summary::after{transform:rotate(45deg)}.faq details p{color:var(--mid);padding:0 0 22px;max-width:62ch}
/* contatti */
.ct{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.2fr);gap:clamp(30px,5vw,80px);align-items:start}@media (max-width:900px){.ct{grid-template-columns:1fr}}
.direct{display:grid;gap:12px;margin-top:30px}.direct a{display:flex;align-items:center;justify-content:space-between;gap:12px;border:1px solid var(--line);padding:16px 18px;text-decoration:none;transition:border-color .25s}.direct a:hover{border-color:#fff}
.direct small{display:block;color:var(--dim);font-size:.82rem;letter-spacing:.06em;text-transform:uppercase}.direct b{font-weight:500;font-size:1.1rem}
.form{background:var(--bg2);padding:clamp(20px,3vw,32px)}.form h3{font-size:1.3rem;margin-bottom:26px}
.form label{display:grid;gap:8px;font-size:.82rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#D4D4D4;margin-bottom:18px}
.form input,.form select,.form textarea{font:400 1rem Urbanist,Arial;color:#fff;background:var(--bg3);border:1px solid transparent;padding:13px 14px;width:100%;border-radius:0;text-transform:none;letter-spacing:0}
.form select{appearance:none;background-image:linear-gradient(45deg,transparent 50%,#A3A3A3 50%),linear-gradient(135deg,#A3A3A3 50%,transparent 50%);background-position:calc(100% - 20px) 50%,calc(100% - 15px) 50%;background-size:5px 5px;background-repeat:no-repeat}
.form input:focus,.form select:focus,.form textarea:focus{outline:0;border-color:#fff}.form input::placeholder,.form textarea::placeholder{color:#737373}
.form .row{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media (max-width:560px){.form .row{grid-template-columns:1fr}}
.radio{display:flex;gap:30px;margin:-6px 0 18px}.radio label{flex-direction:row;display:flex;align-items:center;gap:8px;text-transform:none;letter-spacing:0;font-size:1rem;font-weight:400;margin:0}.radio input{width:18px;height:18px;accent-color:#fff}
.form .check{display:flex;gap:10px;text-transform:none;letter-spacing:0;font-size:.92rem;font-weight:400;color:var(--mid);align-items:flex-start}.form .check input{width:18px;height:18px;flex:none;margin-top:2px;accent-color:#fff}.form .check a{color:#fff}
.form .btn{width:100%;justify-content:center;margin-top:8px}.form [aria-invalid=true]{border-color:#F87171}.form .err{color:#FCA5A5;font-weight:600;margin-bottom:10px}.form .ok h3{font-size:1.6rem;margin-bottom:10px}
/* invito finale */
.band{position:relative;min-height:440px;display:flex;align-items:flex-end;overflow:hidden;isolation:isolate}.band img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}
.band::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,#0A0A0Ae6,#0A0A0A33)}.band .wrap{width:100%;padding-bottom:56px}.band p{max-width:52ch;color:#D4D4D4;margin:14px 0 26px}
/* piede */
.ftr{border-top:1px solid var(--line);padding:70px 0 26px;position:relative;z-index:1;background:var(--bg)}.ftr .g{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:36px}@media (max-width:800px){.ftr .g{grid-template-columns:1fr}}
.ftr p{color:var(--mid);max-width:40ch;margin-top:16px}.ftr small{display:block;color:var(--dim);font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;margin:0 0 8px}.ftr ul{list-style:none;padding:0;margin:0;display:grid;gap:10px}
.ftr a{color:#fff;text-decoration:none}.ftr a:hover{text-decoration:underline}.ftr .info{display:grid;gap:18px}.ftr .bt{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;border-top:1px solid var(--line);margin-top:56px;padding-top:22px;color:var(--dim);font-size:.92rem}
/* barra fissa sul telefono: chiamata e consulenza sempre a portata */
.mbar{display:none}@media (max-width:700px){.mbar{display:grid;grid-template-columns:1fr 1.4fr;gap:8px;position:fixed;left:10px;right:10px;bottom:calc(10px + env(safe-area-inset-bottom,0px));z-index:70;transition:transform .35s}
 .mbar a{display:flex;align-items:center;justify-content:center;gap:8px;padding:13px;font-weight:600;text-decoration:none;border:1px solid #fff}.mbar a:first-child{background:#0A0A0Ae6;color:#fff;backdrop-filter:blur(10px)}.mbar a:last-child{background:#fff;color:#0A0A0A}
 .mbar.hide{transform:translateY(140%)}.wa{display:none}body{padding-bottom:70px}}
.plain{max-width:820px;margin:0 auto;padding:150px 20px 80px}.plain h1{font-size:2.6rem;margin-bottom:20px}.plain p{color:var(--mid);margin-bottom:14px}.small{font-size:.86rem;color:var(--dim)}
.sub{height:70px}.wa{background:#1F7A4D}
"""

JS = b2.COMMON_JS + r"""
var hd=document.querySelector(".hdr");function hs(){hd.classList.toggle("s",scrollY>30)}addEventListener("scroll",hs,{passive:true});hs();
document.querySelectorAll(".cmp").forEach(function(c){var r=c.querySelector("input");function set(v){c.style.setProperty("--x",v+"%")}r.addEventListener("input",function(){set(r.value)});
 var down=false;function mv(e){var b=c.getBoundingClientRect();var x=Math.max(0,Math.min(100,(e.clientX-b.left)/b.width*100));r.value=x;set(x)}
 c.addEventListener("pointerdown",function(e){down=true;mv(e)});addEventListener("pointerup",function(){down=false});c.addEventListener("pointermove",function(e){if(down)mv(e)})});
// processo: si apre una fase alla volta e cambia l'immagine accanto
var acc=document.querySelectorAll(".acc details"),pim=document.querySelectorAll(".pimg img"),pcap=document.querySelector(".pimg span");
acc.forEach(function(d,i){d.addEventListener("toggle",function(){if(!d.open)return;acc.forEach(function(o){if(o!==d)o.open=false});pim.forEach(function(p,j){p.classList.toggle("on",j===i)});if(pcap)pcap.textContent=pim[i].alt})});
// barra del telefono: sparisce quando il modulo è già sullo schermo
var mb2=document.querySelector(".mbar"),fm=document.querySelector("#contatti");if(mb2&&fm)new IntersectionObserver(function(es){mb2.classList.toggle("hide",es[0].isIntersecting)},{threshold:.15}).observe(fm);
// modulo: arriva nel CRM come richiesta di Archi Trend
var f=document.querySelector(".form form");if(f)f.addEventListener("submit",function(e){e.preventDefault();var bad=[];f.querySelectorAll("[aria-invalid]").forEach(function(x){x.removeAttribute("aria-invalid")});
 f.querySelectorAll("[required]").forEach(function(x){if(x.type==="checkbox"?!x.checked:!String(x.value).trim()){bad.push(x);x.setAttribute("aria-invalid","true")}});
 if(!f.email.value.trim()&&!f.phone.value.trim()){bad.push(f.phone);f.phone.setAttribute("aria-invalid","true")}var er=f.querySelector(".err");
 if(bad.length){er.hidden=false;er.textContent="Servono nome, telefono o email e il consenso.";bad[0].focus();return}
 var had=(f.querySelector("[name=had]:checked")||{}).value||"";
 var d={company:"architrend",name:f.name.value,email:f.email.value,phone:f.phone.value,kind:f.kind.value||"Altro",town:f.town.value,message:[f.message.value,had?"Ha già lavorato con un architetto: "+had:""].filter(Boolean).join("\n"),website:f.website.value,consent:true,newsletter:f.newsletter.checked};
 var box=f.parentNode;box.innerHTML="<div class='ok'><h3>Invio in corso…</h3></div>";
 sendReq(d,box.querySelector(".ok"),"<h3>Grazie, abbiamo ricevuto il tuo progetto.</h3><p class='mid'>Un architetto di Archi Trend ti richiama per fissare il primo incontro.</p>","Archi Trend · "+d.kind+"\n"+d.name+" "+d.email+" "+d.phone+"\n"+d.town+"\n"+d.message)});
"""

def crop(src, dst, w):
    im = Image.open(src).convert("RGB")
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(dst, quality=82, optimize=True)

def logo():
    return ('<a class="logo" href="index.html" aria-label="Archi Trend SA, home"><svg viewBox="0 0 30 30" aria-hidden="true"><circle cx="15" cy="15" r="13" fill="none" stroke="#fff" stroke-width="2.2"/>'
            '<path d="M8.5 21 15 8l6.5 13M11 16.5h8" fill="none" stroke="#fff" stroke-width="2.2" stroke-linejoin="round"/></svg>Archi Trend</a>')

def header():
    L = [("index.html#progetti", "Progetti"), ("index.html#studio", "Studio"), ("index.html#processo", "Processo"), ("index.html#domande", "Domande")]
    return (f'<header class="hdr"><div class="wrap">{logo()}<nav class="nav" aria-label="Principale">' + "".join(f'<a href="{h}">{t}</a>' for h, t in L)
            + f'</nav><a class="btn" href="index.html#contatti">Prenota una consulenza</a><button class="menu" data-menu aria-expanded="false">Menu</button></div></header>')

def page(title, desc, body, v):
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#0A0A0A">
<link rel="icon" href="favicon.svg" type="image/svg+xml">{b2.FONTS}<link rel="stylesheet" href="{FONT}"><link rel="stylesheet" href="assets/site.css?v={v}"></head>
<body><a class="skip" href="#main">Vai al contenuto</a>{body}<a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Scrivici su WhatsApp">WhatsApp</a>
<div class="mbar"><a href="tel:{TEL}">Chiama</a><a href="index.html#contatti">Prenota una consulenza</a></div>
<script src="assets/app.js?v={v}" defer></script></body></html>"""

def footer():
    return f"""<footer class="ftr"><div class="wrap"><div class="g"><div>{logo()}<p>Studio di architettura del Gruppo New Trends a Lugano: progettazione, licenze edilizie, direzione lavori, perizie e interni.</p></div>
<div class="info"><div><small>Telefono</small><a href="tel:{TEL}">{PHONE}</a></div><div><small>Email</small><a href="mailto:{MAIL}">{MAIL}</a></div><div><small>Studio</small>{ADDR}</div></div>
<div><small>Il gruppo</small><ul><li><a href="{SITES['newtrends']}">New Trends · Immobiliare</a></li><li><a href="{SITES['architrend']}">Archi Trend · Architettura</a></li><li><a href="{SITES['ediltrend']}">Edil Trend · Costruzioni</a></li><li><a href="privacy.html">Privacy</a></li></ul></div></div>
<div class="bt"><span>© Archi Trend SA · Parte del Gruppo New Trends</span><span>Lugano, Svizzera</span></div></div></footer>"""

ICON = {"misura": '<path d="M3 17 17 3l4 4L7 21H3zM14 6l4 4M10 10l2 2M7 13l2 2"/>', "chiaro": '<path d="M4 5h16v11H8l-4 4z"/><path d="M8 9h8M8 12h5"/>',
        "calma": '<path d="M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z"/><path d="m8 12 3 3 5-6"/>', "tempi": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/>'}

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    A = os.path.join(OUT, "assets"); I = os.path.join(A, "img"); os.makedirs(I)
    img = {}
    def put(name, src, w): crop(src, os.path.join(I, name), w); img[name] = "assets/img/" + name; return img[name]
    pr = lambda k: find_src(P[k][4]); bpf = lambda k, s: os.path.join(b2.BP, P[k][4][:40] + f"-{s}.jpg")
    put("hero.jpg", pr("ferrari"), 2048)
    put("e1.jpg", pr("optima"), 900); put("e2.jpg", bpf("greenhorse", "bp"), 900); put("e3.jpg", pr("motta"), 900)
    works = [("greenhorse", ["RESIDENZIALE", "IN COSTRUZIONE"]), ("optima", ["RESIDENZIALE", "REALIZZATO"]), ("miracolli", ["RESIDENZIALE", "REALIZZATO"])]
    for k, _ in works: put(f"w-{k}.jpg", pr(k), 2000)
    for k in ("ferrari", "maraini", "synthesis"): put(f"b-{k}-bp.jpg", bpf(k, "bp"), 900); put(f"b-{k}-ph.jpg", bpf(k, "ph"), 900)
    for i, k in enumerate(("aurea", "optima", "greenhorse", "ferrari")): put(f"p{i}.jpg", bpf(k, "bp" if i < 3 else "ph"), 1100)
    put("q.jpg", pr("duelaghi"), 900); put("band.jpg", pr("aurea"), 1800)
    open(os.path.join(OUT, "favicon.svg"), "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30"><rect width="30" height="30" fill="#0A0A0A"/><circle cx="15" cy="15" r="11" fill="none" stroke="#fff" stroke-width="2"/><path d="M9.8 20 15 9.5 20.2 20M11.8 16.4h6.4" fill="none" stroke="#fff" stroke-width="2"/></svg>')

    exp = [("01", "Progettazione residenziale", "Case, ville e palazzine pensate su misura per il terreno, per chi ci abiterà e per il valore dell'immobile nel tempo.", "e1.jpg", "Residenza Optima, Montagnola"),
           ("02", "Licenze e direzione lavori", "Domanda di costruzione, rapporti con il Comune e direzione del cantiere fino alla consegna, con Edil Trend o con l'impresa che scegli tu.", "e2.jpg", "Piano della Residenza Green Horse"),
           ("03", "Perizie, ristrutturazioni e interni", "Valutazioni tecniche, progetti di ristrutturazione e interni che ridanno qualità e valore a ciò che esiste.", "e3.jpg", "Appartamento in Via Motta, Lugano")]
    ex = "".join(f'<div class="reveal"><small>{n}</small><h3>{E(t)}</h3><p>{E(d)}</p><img src="{img[f]}" alt="{E(a)}" loading="lazy"></div>' for n, t, d, f, a in exp)
    wk = "".join(f'<a class="work" href="#contatti"><img src="{img["w-" + k + ".jpg"]}" alt="{E(P[k][0])}, {E(P[k][1])}" loading="lazy"><div class="t"><div class="wrap reveal"><div class="tags">{"".join(f"<span>{t}</span>" for t in tags)}</div><h3>{E(P[k][0])}</h3><p>{E(P[k][1])} · {E(P[k][2])}</p></div></div></a>' for k, tags in works)
    ba = "".join(f'<div class="reveal"><div class="cmp"><img src="{img["b-" + k + "-bp.jpg"]}" alt="{E(P[k][0])}: progetto" loading="lazy"><img class="a" src="{img["b-" + k + "-ph.jpg"]}" alt="{E(P[k][0])}: realizzato" loading="lazy"><span class="ln"></span><span class="lb l1">Progetto</span><span class="lb l2">Realtà</span><input type="range" min="0" max="100" value="50" aria-label="Confronta progetto e realtà: {E(P[k][0])}"><span class="hd" aria-hidden="true">‹›</span></div><h3>{E(P[k][0])}</h3><p>{E(P[k][1])} · {E(P[k][2])}</p></div>' for k in ("ferrari", "maraini", "synthesis"))
    steps = [("Fase 01 · Ascolto e sopralluogo", "Ci incontriamo, visitiamo il terreno o l'immobile e mettiamo in chiaro esigenze, budget e tempi. Il primo incontro è senza impegno.", "p0.jpg", "Residenza Aurea, Collina d'Oro · studio dei volumi"),
             ("Fase 02 · Concept", "Prime idee, volumi e materiali: ti mostriamo come potrebbe essere, con una stima dei costi già dall'inizio.", "p1.jpg", "Residenza Optima, Montagnola · concept"),
             ("Fase 03 · Progetto e licenza", "Sviluppiamo il progetto definitivo e seguiamo la domanda di costruzione con il Comune.", "p2.jpg", "Residenza Green Horse, Muzzano · progetto"),
             ("Fase 04 · Direzione lavori e consegna", "Seguiamo il cantiere fino alla consegna, con Edil Trend o con l'impresa che preferisci.", "p3.jpg", "Residenza Ferrari, Tesserete · realizzazione")]
    acc = "".join(f'<details{" open" if i == 0 else ""}><summary>{E(t)}</summary><p>{E(d)}</p></details>' for i, (t, d, _, _) in enumerate(steps))
    pim = "".join(f'<img class="{"on" if i == 0 else ""}" src="{img[f]}" alt="{E(a)}" loading="lazy">' for i, (_, _, f, a) in enumerate(steps)) + f'<span>{E(steps[0][3])}</span>'
    why = [("misura", "Progetti su misura per te", "Ogni pianta, materiale e dettaglio parte da come vivi e da cosa ti serve davvero, non da un modello già pronto."),
           ("chiaro", "Chiarezza a ogni passo", "Dal primo incontro alla consegna sai sempre a che punto siamo, cosa viene dopo e perché."),
           ("calma", "Un percorso senza stress", "Coordiniamo noi tecnici, Comune e impresa: tu prendi le decisioni importanti, al resto pensiamo noi."),
           ("tempi", "Tempi e costi sotto controllo", "Progettiamo con uno sguardo al mercato e al budget, per evitare ritardi e spese che non servono.")]
    wy = "".join(f'<div class="reveal"><svg viewBox="0 0 24 24" aria-hidden="true">{ICON[i]}</svg><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i, a, b in why)
    faqs = [("Potete lavorare su un progetto che ho già?", "Sì. Possiamo rivedere, completare o sviluppare un progetto esistente, mantenendo l'idea di partenza."),
            ("Quando conviene coinvolgere l'architetto?", "Il prima possibile, idealmente prima di comprare il terreno o l'immobile: così sai subito cosa si può costruire e quanto costa."),
            ("Vi occupate anche della domanda di costruzione?", "Sì, prepariamo la documentazione e seguiamo la domanda di costruzione con il Comune fino alla licenza."),
            ("Dovete costruire per forza con Edil Trend?", "No. Con Edil Trend hai un solo gruppo dal progetto alle chiavi, ma possiamo dirigere i lavori anche con l'impresa che scegli tu."),
            ("Quanto costa il primo incontro?", "Il primo incontro è senza impegno: ascoltiamo il progetto e ti diciamo come possiamo aiutarti."),
            ("Fate anche perizie e ristrutturazioni?", "Sì: perizie tecniche, progetti di ristrutturazione e interni, per privati e investitori."),
            ("In quali zone lavorate?", "Soprattutto nel Luganese e nel resto del Ticino.")]
    fq = "".join(f'<details{" open" if i == 0 else ""}><summary>{E(q)}</summary><p>{E(a)}</p></details>' for i, (q, a) in enumerate(faqs))
    kinds = ["Nuova casa o villa", "Palazzina o residenza", "Ristrutturazione", "Interni", "Perizia", "Licenza o domanda di costruzione", "Altro"]
    form = f"""<div class="form reveal"><h3>Raccontaci il progetto: ti richiamiamo per fissare il primo incontro.</h3><form novalidate>
<div class="row"><label>Nome e cognome<input name="name" autocomplete="name" placeholder="Mario Rossi" required></label><label>Telefono<input name="phone" type="tel" autocomplete="tel" placeholder="+41 79 000 00 00"></label></div>
<label>Email<input name="email" type="email" autocomplete="email" placeholder="nome@email.ch"></label>
<div class="row"><label>Tipo di progetto<select name="kind"><option value="">Scegli…</option>{"".join(f"<option>{E(k)}</option>" for k in kinds)}</select></label><label>Comune<input name="town" placeholder="es. Lugano"></label></div>
<label>Messaggio (facoltativo)<textarea name="message" rows="3" placeholder="es. terreno di 800 m² a Tesserete, vorrei una casa per 4 persone"></textarea></label>
<label style="margin-bottom:10px">Hai già lavorato con un architetto?</label><div class="radio"><label><input type="radio" name="had" value="sì">Sì</label><label><input type="radio" name="had" value="no">No</label></div>
<input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
<label class="check"><input type="checkbox" name="consent" required><span>Acconsento a essere ricontattato da Archi Trend SA secondo l'<a href="privacy.html">informativa privacy</a>.</span></label>
<label class="check"><input type="checkbox" name="newsletter"><span>Desidero ricevere occasionalmente novità del Gruppo New Trends (facoltativo).</span></label>
<p class="err" hidden role="alert"></p><button class="btn" type="submit">Prenota la consulenza gratuita {AR}</button></form></div>"""
    chain = b2.chain("architrend", "chain")
    home = f"""{header()}<section class="hero"><img src="{img['hero.jpg']}" alt="Residenza Ferrari, Tesserete" fetchpriority="high"><div class="wrap">
<h1 class="up">Progettiamo case che durano nel tempo</h1><p class="up d1">Archi Trend è lo studio di architettura del Gruppo New Trends a Lugano. Progetto, licenza e direzione lavori con un solo interlocutore, e uno sguardo sempre attento al valore dell'immobile.</p>
<div class="acts up d2"><a class="btn" href="#contatti">Prenota una consulenza gratuita {AR}</a><a class="btn ghost" href="#progetti">Guarda i progetti</a></div>
<div class="trust up d3"><span><b>Dal 2009</b> a Lugano</span><span><b>100+</b> unità realizzate dal gruppo</span><span>Primo incontro <b>senza impegno</b></span></div></div></section>
<main id="main">
<section class="sec" id="studio"><div class="wrap"><div class="intro reveal"><p>In Archi Trend crediamo che un buon progetto inizi molto prima del primo disegno. <span>Parte dal capire il luogo, chi ci vivrà e il valore che la casa dovrà avere nel tempo. Per questo progettiamo con uno sguardo al mercato, insieme a chi poi costruisce e vende.</span></p><a class="btn ghost" href="#contatti">Parliamo del tuo progetto {AR}</a></div></div></section>
<section style="border-top:1px solid var(--line)"><div class="wrap" style="padding-top:60px"><span class="chip">Cosa facciamo</span></div><div class="wrap" style="padding:0"><div class="exp">{ex}</div>
<div class="stats"><div><b>2009</b><span>anno di fondazione</span></div><div><b>100+</b><span>unità realizzate dal gruppo</span></div><div><b>300+</b><span>professionisti in rete</span></div><div><b>1</b><span>interlocutore dal progetto alle chiavi</span></div></div></div></section>
<section id="progetti" style="border-top:1px solid var(--line)"><div class="wt reveal"><h2>Progetti del gruppo</h2><p class="mid">Residenze progettate e realizzate dal Gruppo New Trends nel Luganese.</p></div>{wk}
<div class="wrap"><div class="after"><p>Hai un terreno o un immobile? Ti diciamo cosa ci si può costruire.</p><a class="btn" href="#contatti">Prenota una consulenza {AR}</a></div></div></section>
<section class="sec"><div class="wrap"><span class="chip">Dal progetto alla realtà</span><h2>Quello che disegniamo, lo vedi costruito.</h2><p class="mid" style="margin:14px 0 40px;max-width:56ch">Trascina il cursore per confrontare il progetto con l'edificio finito.</p><div class="ba">{ba}</div></div></section>
<section class="sec" id="processo"><div class="wrap"><span class="chip">Il nostro processo</span><h2>Dall'idea al cantiere</h2><p class="mid" style="margin:14px 0 40px;max-width:56ch">Un percorso chiaro in quattro fasi, con decisioni e costi sempre sotto controllo.</p>
<div class="proc"><div class="acc">{acc}<a class="btn" href="#contatti" style="margin-top:34px">Inizia dalla fase 01 {AR}</a></div><div class="pimg">{pim}</div></div></div></section>
<section class="sec"><div class="wrap"><span class="chip">Perché sceglierci</span><h2>Lo studio giusto per il tuo progetto</h2><p class="mid" style="margin-top:14px;max-width:60ch">Progetto curato, comunicazione chiara e un gruppo che segue anche costruzione e vendita: spazi pensati per durare e per valere.</p><div class="why">{wy}</div></div></section>
<section class="sec"><div class="wrap"><div class="quote"><div class="reveal"><span class="chip">Gruppo New Trends</span><blockquote>“Progettare con uno sguardo al mercato: ogni scelta deve sostenere il valore e il risultato dell'immobile.”</blockquote>
<p>New Trends nasce a Lugano nel 1991. Oggi il gruppo riunisce New Trends SA per la consulenza e l'intermediazione immobiliare, Archi Trend SA per la progettazione ed Edil Trend SA per la realizzazione.</p>{chain}</div><img class="reveal" src="{img['q.jpg']}" alt="Residenza Due Laghi, Muzzano" loading="lazy"></div></div></section>
<section class="sec" id="domande"><div class="wrap faq"><div><span class="chip">Domande</span><h2>Domande frequenti</h2><p class="mid">Le domande che ci fanno più spesso su progetto, tempi e costi. Non trovi la tua? Chiamaci al <a href="tel:{TEL}" style="color:#fff">{PHONE}</a>.</p></div><div>{fq}</div></div></section>
<section class="sec" id="contatti"><div class="wrap ct"><div class="reveal"><span class="chip">Contatti</span><h2>Creiamo qualcosa di eccezionale</h2><p class="mid" style="margin-top:16px;max-width:46ch">Il primo incontro è senza impegno. Scegli tu come preferisci sentirci.</p>
<div class="direct"><a href="tel:{TEL}"><span><small>Telefono</small><b>{PHONE}</b></span>{AR}</a><a href="https://wa.me/{WA}" target="_blank" rel="noopener"><span><small>WhatsApp</small><b>Scrivici un messaggio</b></span>{AR}</a><a href="mailto:{MAIL}"><span><small>Email</small><b>{MAIL}</b></span>{AR}</a></div>
<p class="small" style="margin-top:18px">{ADDR}</p></div>{form}</div></section>
<section class="band"><img src="{img['band.jpg']}" alt="" loading="lazy"><div class="wrap reveal"><h2>Diamo forma alla tua idea</h2><p>Dai primi schizzi alla consegna delle chiavi: progettiamo con cura e costruiamo con un gruppo che conosce il territorio.</p><a class="btn" href="#contatti">Prenota una consulenza {AR}</a></div></section>
</main>{footer()}"""
    pv = f'{header()}<div class="sub"></div><main id="main">{b2.privacy("Archi Trend SA")}</main>{footer()}'
    v = hashlib.sha256((CSS + JS).encode()).hexdigest()[:10]
    open(os.path.join(A, "site.css"), "w").write(CSS); open(os.path.join(A, "app.js"), "w").write("(function(){" + JS + "})();")
    for n, (t, d, body) in {"index.html": ("Archi Trend SA · Studio di architettura a Lugano", "Studio di architettura del Gruppo New Trends a Lugano: progettazione, licenze, direzione lavori, perizie e interni.", home),
                            "privacy.html": ("Privacy · Archi Trend SA", "Informativa privacy.", pv)}.items():
        open(os.path.join(OUT, n), "w").write(page(t, d, body, v))
    open(os.path.join(OUT, "progetti.html"), "w").write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=index.html#progetti"><a href="index.html#progetti">Progetti</a>')
    open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
    print("ok", OUT)

if __name__ == "__main__":
    build()
