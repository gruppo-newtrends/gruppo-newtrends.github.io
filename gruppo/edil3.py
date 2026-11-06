# -*- coding: utf-8 -*-
"""Edil Trend, versione 5: struttura e stile come renovatehub.framer.website, con contenuti veri di Edil Trend
e una villa three.js che si costruisce mentre scorri "Come lavoriamo" (src/villa3d.js).
Niente recensioni, voti o garanzie inventate: al loro posto lavori, fatti e anni del gruppo.
Uso: python3 -E -s edil3.py [cartella]  (predefinita out/ediltrend-v5). Archi Trend non viene toccato."""
import hashlib, os, shutil, sys
from PIL import Image
import build2 as b2
from build2 import E, P, ADDR, PHONE, TEL, MAIL, WA, SITES, ICONS, find_src

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "ediltrend-v5")
YEARS = 2026 - 1999
FONTS = ('<link rel="preconnect" href="https://api.fontshare.com" crossorigin>'
         '<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap">')
IMPORTMAP = ('<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",'
             '"three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>')
AR = '<i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></i>'
CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m7.5 12.5 3 3 6-6"/></svg>'
PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg>'

CSS = b2.COMMON_CSS + """
:root{--cream:#EFEBE3;--paper:#fff;--ink:#1C1C18;--dark:#1C1C18;--beige:#EAD9BE;--muted:#6E6A5F;--line:#DDD6CA;--r:24px}
html{scroll-behavior:smooth}html,body{overflow-x:clip}body{background:var(--cream);color:var(--ink);font:500 1rem/1.55 Satoshi,Inter,Arial,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:1320px;margin:0 auto;padding:0 clamp(16px,4vw,60px)}
h1,h2,h3{font-family:Satoshi,Inter,Arial,sans-serif;font-weight:500;letter-spacing:-.035em;line-height:1.05;margin:0;text-wrap:balance}
h2{font-size:clamp(2.1rem,1.3rem + 2.6vw,3.4rem)}h3{font-weight:700;letter-spacing:-.02em}
.tag{display:block;font-weight:500;font-size:.9rem;color:var(--muted);margin-bottom:14px}.tag::before{content:"// "}.dk .tag{color:#B9B2A6}
.lead{color:var(--muted);max-width:52ch;margin:0}.dk .lead{color:#B9B2A6}
.sec{padding:clamp(70px,8vw,110px) 0}.dk{background:var(--dark);color:#F3EFE8;border-radius:var(--r);margin:0 8px}
.head{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:20px 60px;align-items:start;margin-bottom:46px}.head .lead{margin-top:8px}.head .r{display:grid;gap:26px;justify-items:start}
@media (max-width:860px){.head{grid-template-columns:1fr}}
/* bottoni: pillola con cerchio e freccia */
.btn{display:inline-flex;align-items:center;gap:12px;padding:5px 5px 5px 18px;border-radius:999px;background:var(--ink);color:#fff;font:700 1rem Satoshi,Arial;text-decoration:none;border:1px solid transparent;cursor:pointer;box-shadow:0 8px 20px -10px #0007;transition:transform .25s}
.btn i{width:32px;height:32px;border-radius:50%;background:#fff;color:var(--ink);display:grid;place-items:center;transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.btn i svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2}.btn:hover i{transform:rotate(-45deg)}.btn:active{transform:scale(.97)}
.btn.w{background:#fff;color:var(--ink)}.btn.w i{background:var(--ink);color:#fff}.btn.bg{background:var(--beige);color:var(--ink)}.btn.bg i{background:var(--ink);color:#fff}
.btn.o{background:transparent;border-color:#ffffffb3;color:#fff;padding:9px 16px;box-shadow:none}
/* header fisso: trasparente sopra la foto, vetro scuro quando scorri */
.hdr{position:fixed;top:8px;left:8px;right:8px;z-index:60;border-radius:0 0 18px 18px;transition:background .35s,backdrop-filter .35s}
.hdr.s{background:#2a2823a6;backdrop-filter:blur(18px) saturate(1.2);-webkit-backdrop-filter:blur(18px) saturate(1.2)}
.hdr .wrap{display:flex;align-items:center;gap:20px;height:78px;max-width:none;padding:0 clamp(16px,2.6vw,38px)}
.logo{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font:700 1.55rem/1 Satoshi,Arial;letter-spacing:-.03em}.logo svg{width:30px;height:30px}
.logo small{font:500 .72rem Satoshi;letter-spacing:.16em;opacity:.7;margin-left:2px;align-self:flex-end;padding-bottom:3px}
.pill{position:absolute;left:50%;transform:translateX(-50%);display:flex;gap:2px;padding:6px;border-radius:999px;background:#ffffff1f;border:1px solid #ffffff3d;backdrop-filter:blur(12px)}
.pill a{color:#ffffffd9;text-decoration:none;padding:7px 16px;border-radius:999px;font-size:.98rem;transition:background .2s,color .2s}.pill a:hover{color:#fff}.pill a.on{background:#ffffff26;border:1px solid #ffffff40;color:#fff;padding:6px 15px}
.hdr .btn{margin-left:auto}.menu{display:none}
@media (max-width:1000px){.pill{display:none}.menu{display:inline-flex;margin-left:auto;background:#ffffff26;border:1px solid #ffffff40;color:#fff;border-radius:999px;padding:9px 16px;font:700 .95rem Satoshi;backdrop-filter:blur(10px)}.hdr .btn{display:none}
 .pill.open{display:flex;flex-direction:column;position:absolute;top:84px;left:0;right:0;transform:none;background:#1C1C18f2;border-radius:18px;padding:10px}.pill.open a{padding:12px 16px}}
/* hero */
.hero{padding:8px}.hero .f{position:relative;min-height:calc(100svh - 16px);border-radius:var(--r);overflow:hidden;color:#fff;display:flex;flex-direction:column;justify-content:flex-end;isolation:isolate;background:#2b2620}
.hero .f>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;transform:scale(1.06);animation:hz 2.6s cubic-bezier(.2,.7,.2,1) forwards}@keyframes hz{to{transform:none}}
.hero .f::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,#1C1C1866 0%,#1C1C1800 30%,#1C1C1833 55%,#1C1C18d9 100%),#2a201622}
.hero .b{padding:0 clamp(18px,2.6vw,38px) 22px}.hero .top{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,520px);gap:24px 60px;align-items:end;padding-bottom:30px;border-bottom:1px solid #ffffff40}
.hero h1{font-size:clamp(2.6rem,1.2rem + 4.6vw,5rem);line-height:1.02}.hero h1 span{display:block;opacity:0;transform:translateY(26px);animation:up 1s cubic-bezier(.2,.7,.2,1) forwards}.hero h1 span+span{animation-delay:.15s}
.hero .top p{margin:0;color:#F1ECE4;opacity:0;animation:up 1s ease .45s forwards}@keyframes up{to{opacity:1;transform:none}}
.hero .bot{display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;padding-top:22px;opacity:0;animation:up 1s ease .6s forwards}
.hero .acts{display:flex;gap:14px;flex-wrap:wrap}.checks{display:flex;gap:28px;flex-wrap:wrap;list-style:none;margin:0;padding:0;font-weight:700}
.checks li{display:flex;align-items:center;gap:10px}.checks svg{width:22px;height:22px}.checks circle{fill:#fff}.checks path{fill:none;stroke:var(--ink);stroke-width:2.2}
@media (max-width:860px){.hero .top{grid-template-columns:1fr}.checks{gap:14px 20px;font-size:.92rem}}
/* servizi */
.svc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}@media (max-width:980px){.svc{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:620px){.svc{grid-template-columns:1fr}}
.svc a{background:#fff;border-radius:20px;padding:6px;text-decoration:none;display:flex;flex-direction:column;transition:transform .4s cubic-bezier(.2,.7,.2,1),box-shadow .4s}.svc a:hover{transform:translateY(-6px);box-shadow:0 30px 50px -34px #1C1C1866}
.svc .ph{position:relative;aspect-ratio:415/226;border-radius:15px;overflow:hidden}.svc img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}.svc a:hover img{transform:scale(1.06)}
.chip{position:absolute;left:12px;top:12px;display:flex;align-items:center;gap:7px;background:#ffffff59;backdrop-filter:blur(10px);color:#fff;border-radius:999px;padding:5px 12px;font-weight:700;font-size:.88rem}.chip::before{content:"";width:5px;height:5px;border-radius:50%;background:#fff}
.svc .t{padding:22px 16px 18px;display:grid;gap:10px;flex:1}.svc h3{font-size:1.28rem}.svc p{margin:0;color:var(--muted)}
.more{display:inline-flex;align-items:center;gap:10px;font-weight:700;margin-top:auto;padding-top:14px}.more i{width:24px;height:24px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;transition:transform .3s}.more i svg{width:13px;height:13px;fill:none;stroke:#fff;stroke-width:2.2}.svc a:hover .more i{transform:rotate(-45deg)}
/* prima e dopo */
.ba{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}@media (max-width:980px){.ba{grid-template-columns:1fr 1fr}}@media (max-width:620px){.ba{grid-template-columns:1fr}}
.cmp{position:relative;aspect-ratio:427/470;border-radius:20px;overflow:hidden;--x:50%;user-select:none;touch-action:pan-y;cursor:ew-resize;background:#2b2620}
.cmp img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;pointer-events:none}.cmp .a{clip-path:inset(0 0 0 var(--x))}
.cmp .ln{position:absolute;top:0;bottom:0;left:var(--x);width:2px;background:#fff;transform:translateX(-1px)}.cmp .hd{position:absolute;top:50%;left:var(--x);width:48px;height:48px;border-radius:50%;background:#fff;transform:translate(-50%,-50%);display:grid;place-items:center;box-shadow:0 6px 20px #0005;color:var(--ink);font-weight:700;letter-spacing:4px}
.cmp input{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:ew-resize;margin:0}.cmp input:focus-visible+.hd{outline:3px solid var(--beige);outline-offset:3px}
.cmp .lb{position:absolute;top:16px;padding:6px 16px;border-radius:999px;font-weight:700;font-size:.9rem;backdrop-filter:blur(10px);pointer-events:none}.cmp .l1{left:16px;background:#1C1C18a6;color:#fff}.cmp .l2{right:16px;background:#ffffff8c;color:#fff}
.ba h3{font-size:1.2rem;margin:18px 4px 4px}.ba p{margin:0 4px;color:#B9B2A6;font-size:.95rem}
/* perché noi */
.why{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:clamp(30px,6vw,100px)}@media (max-width:900px){.why{grid-template-columns:1fr}}
.why .ph{position:relative;margin-top:30px;border-radius:20px;overflow:hidden;aspect-ratio:538/240}.why .ph img{width:100%;height:100%;object-fit:cover}
.why .ph div{position:absolute;inset:auto 0 0 0;padding:18px 20px;color:#fff;background:linear-gradient(0deg,#1C1C18cc,transparent)}.why .ph b{font-size:1.15rem}
.wg{display:grid;grid-template-columns:1fr 1fr;gap:20px}@media (max-width:560px){.wg{grid-template-columns:1fr}}
.wg div{background:#fff;border-radius:20px;padding:20px;min-height:228px;display:flex;flex-direction:column;transition:transform .35s}.wg div:hover{transform:translateY(-4px)}
.wg svg{width:42px;height:42px;padding:10px;border-radius:10px;background:var(--ink);stroke:#fff;fill:none;stroke-width:1.7;box-shadow:0 8px 16px -8px #000a}
.wg h3{font-size:1.15rem;margin:auto 0 8px}.wg p{margin:0;color:var(--muted);font-size:.97rem}
/* come lavoriamo: sezione fissata, la villa si costruisce */
.proc{position:relative;height:430vh;padding:0}.proc .st{position:sticky;top:0;height:100svh;display:flex;flex-direction:column;padding:104px 0 18px;overflow:hidden}
.proc .head{margin-bottom:26px}.proc h2{font-weight:700}
.steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0 24px;position:relative;margin-bottom:22px}
.steps::before,.steps .fill{content:"";position:absolute;left:0;top:18px;height:1px;background:#ffffff26;right:0}.steps .fill{right:auto;width:var(--p,0%);background:repeating-linear-gradient(90deg,#EAD9BE 0 3px,transparent 3px 5px)}
.pstep{position:relative;opacity:.38;transition:opacity .45s}.pstep.on{opacity:1}
.pstep span{display:inline-block;background:#6E6A5F;color:var(--ink);border-radius:999px;padding:9px 13px;font-weight:700;font-size:.88rem;position:relative;transition:background .45s}.pstep.on span{background:var(--beige)}
.pstep h3{font-size:1.15rem;margin:20px 0 6px}.pstep p{margin:0;color:#D8D1C5;font-size:.95rem;max-width:30ch}
.stage3d{position:relative;flex:1;min-height:0;border-radius:20px;overflow:hidden;background:#24211c}.stage3d canvas{display:block;width:100%!important;height:100%!important}
.stage3d>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.proc.has3d .stage3d>img{display:none}
.stage3d .bar{position:absolute;left:20px;right:20px;top:18px;height:2px;border-radius:2px;background:#ffffff33}.stage3d .bar i{display:block;height:100%;width:0;background:var(--beige);border-radius:2px}
.cap3d{position:absolute;left:16px;bottom:16px;background:#1C1C18b3;backdrop-filter:blur(8px);color:#fff;border-radius:999px;padding:8px 14px;font-weight:700;font-size:.85rem}.proc:not(.has3d) .bar,.proc:not(.has3d) .cap3d{display:none}
@media (max-width:860px){.proc{height:380vh}.proc .st{padding-top:96px}.proc .head{margin-bottom:14px}.proc .head .lead{display:none}.proc h2{font-size:2rem}
 .steps{gap:0 8px;margin-bottom:14px}.pstep span{padding:7px 9px;font-size:.74rem}.pstep h3,.pstep p{display:none}.pstep.cur h3,.pstep.cur p{display:block;position:absolute;left:0;width:calc(400% + 24px)}
 .pstep:nth-child(3).cur h3,.pstep:nth-child(3).cur p{left:calc(-100% - 8px)}.pstep:nth-child(4).cur h3,.pstep:nth-child(4).cur p{left:calc(-200% - 16px)}.pstep:nth-child(5).cur h3,.pstep:nth-child(5).cur p{left:calc(-300% - 24px)}
 .pstep.cur h3{top:44px;margin:0}.pstep.cur p{top:72px;max-width:none}.steps{padding-bottom:84px}}
/* lavori (al posto delle recensioni) */
.wk{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}@media (max-width:980px){.wk{grid-template-columns:1fr 1fr}}@media (max-width:620px){.wk{grid-template-columns:1fr}}
.wk article{background:#fff;border-radius:20px;padding:30px 30px 24px;display:flex;flex-direction:column;gap:16px}.wk .k{font-size:.82rem;letter-spacing:.12em;text-transform:uppercase;color:#C3922E;font-weight:700}
.wk q{quotes:none;font-size:1.05rem}.wk img{border-radius:14px;aspect-ratio:369/200;object-fit:cover;width:100%}.wk .who{display:flex;gap:12px;align-items:center}.wk .who span{width:46px;height:46px;border-radius:50%;background:var(--beige);display:grid;place-items:center;font-weight:700}
.wk .who b{display:block}.wk .who small{color:var(--muted);font-size:.95rem}
.facts{display:grid;grid-template-columns:repeat(3,1fr);margin-top:20px;border:1px solid var(--line);border-radius:12px;overflow:hidden}.facts div{padding:18px;text-align:center;font-weight:700;font-size:1.08rem}.facts div+div{border-left:1px solid var(--line)}
@media (max-width:620px){.facts{grid-template-columns:1fr}.facts div+div{border-left:0;border-top:1px solid var(--line)}}
.revhead{display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;margin-bottom:40px}.revhead .lead{max-width:40ch}
/* banner del gruppo */
.band{position:relative;border-radius:20px;overflow:hidden;color:#fff;min-height:342px;display:flex;align-items:center;isolation:isolate}
.band>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}.band::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,#1C1C18f0 0%,#1C1C18b3 45%,#1C1C1822 100%)}
.band .tx{padding:clamp(28px,4vw,60px);max-width:680px}.band h2{margin-bottom:18px}.band p{color:#E6E0D6;margin:0 0 24px}.band .tag{color:#E6E0D6}
.band .glass{position:absolute;right:60px;bottom:60px;background:#ffffff2e;backdrop-filter:blur(14px);border:1px solid #ffffff26;border-radius:12px;padding:16px 18px}.band .glass b{display:block;font-size:1.15rem}
@media (max-width:860px){.band .glass{display:none}}
/* zone */
.zones{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(30px,4vw,50px);align-items:center}@media (max-width:900px){.zones{grid-template-columns:1fr}}
.map{background:var(--dark);border-radius:20px;aspect-ratio:620/520;position:relative;overflow:hidden}.map svg{position:absolute;inset:0;width:100%;height:100%}
.map .lab{position:absolute;transform:translate(-50%,-140%);background:#fff;border-radius:999px;padding:5px 13px;font-size:.88rem;white-space:nowrap}
.map .lab::after{content:"";position:absolute;left:50%;top:calc(100% + 10px);width:9px;height:9px;border-radius:50%;background:#fff;border:2px solid var(--ink);transform:translateX(-50%);box-shadow:0 0 0 5px #ffffff22}
.places{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;list-style:none;padding:0;margin:26px 0 30px}
.places li{display:flex;align-items:center;gap:8px;background:#fff;border-radius:999px;padding:9px 14px}.places svg{width:18px;height:18px;flex:none;fill:var(--ink);stroke:#fff;stroke-width:1.2}
/* esperienza */
.gua{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(30px,5vw,80px)}@media (max-width:900px){.gua{grid-template-columns:1fr}}
.ring{width:240px;height:240px;border-radius:50%;border:1px dashed #ffffff66;display:grid;place-items:center;margin:46px 0 0 clamp(0px,10vw,130px);animation:spin 40s linear infinite}
.ring div{width:188px;height:188px;border-radius:50%;background:var(--beige);color:var(--ink);display:grid;place-content:center;text-align:center;animation:spin 40s linear infinite reverse}
.ring b{font-size:3.2rem;line-height:1;letter-spacing:-.04em}.ring small{font-weight:700;font-size:1rem;line-height:1.3}.ring small span{color:#6E6A5F;display:block}@keyframes spin{to{transform:rotate(360deg)}}
.gl{display:grid;gap:20px;align-content:start}.gl div{display:flex;align-items:center;gap:16px;border:1px solid #ffffff2e;border-radius:12px;padding:12px 14px;font-weight:700;font-size:1.1rem}
.gl svg{width:42px;height:42px;padding:10px;border-radius:8px;background:var(--beige);stroke:var(--ink);fill:none;stroke-width:1.8;flex:none}.gua .note{color:#D8D1C5;margin:40px 0 0}
/* domande */
.faq{max-width:872px;margin:0 auto}.faq h2{text-align:center;margin-bottom:40px}.faq .tag{text-align:center}
.faq details{background:#fff;border-radius:12px;margin-bottom:20px;transition:box-shadow .3s}.faq details[open]{box-shadow:0 20px 40px -30px #1C1C1866}
.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:20px;padding:18px 18px 18px 20px;font-weight:700;font-size:1.08rem}.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";flex:none;width:40px;height:40px;border-radius:8px;background:var(--ink);color:#fff;display:grid;place-items:center;font-size:1.5rem;font-weight:400;transition:transform .35s}.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{margin:0;padding:0 20px 20px;color:var(--muted);max-width:68ch}
/* preventivo */
.cfg{background:#fff;border-radius:var(--r);padding:clamp(24px,4.5vw,60px)}.cfg .prog{height:2px;background:var(--line);margin:26px 0 28px;border-radius:2px;position:relative}.cfg .prog i{position:absolute;left:0;top:0;height:2px;background:var(--ink);width:25%;transition:width .5s}
.q{display:none}.q.on{display:block;animation:qin .45s ease}@keyframes qin{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.q .step{display:inline-block;background:var(--beige);border-radius:999px;padding:6px 12px;font-weight:700;font-size:.8rem}.q h3{font-size:clamp(1.4rem,1.1rem + 1.2vw,2rem);margin:14px 0 22px;font-weight:500}
.tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}@media (max-width:800px){.tiles{grid-template-columns:1fr 1fr}}@media (max-width:420px){.tiles{grid-template-columns:1fr}}
.tiles button{background:var(--cream);border:1px solid transparent;border-radius:14px;padding:16px;text-align:left;font:700 1rem Satoshi;color:var(--ink);cursor:pointer;display:flex;gap:12px;align-items:center;transition:transform .2s,background .2s}
.tiles button svg{width:24px;height:24px;stroke:var(--ink);fill:none;stroke-width:1.6;flex:none}.tiles button:hover{transform:translateY(-2px);background:#E6E0D4}.tiles button[aria-pressed=true]{background:var(--ink);color:#fff}.tiles button[aria-pressed=true] svg{stroke:#fff}
.nav2{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:24px}.back{background:none;border:0;font:500 1rem Satoshi;color:var(--muted);cursor:pointer}
.cfg label{display:grid;gap:6px;font-weight:700;font-size:.9rem}.cfg input,.cfg textarea{font:500 1rem Satoshi;padding:.8rem .9rem;border:1px solid var(--line);border-radius:10px;background:var(--cream);width:100%;color:var(--ink)}
.cfg input:focus,.cfg textarea:focus{outline:2px solid var(--ink);outline-offset:1px}.cfg .row{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:14px}@media (max-width:560px){.cfg .row{grid-template-columns:1fr}}
.cfg .check{display:flex;gap:10px;font-weight:500;margin-top:12px}.cfg .check input{width:18px;height:18px;flex:none;margin-top:3px;accent-color:var(--ink)}
.cfg [aria-invalid=true]{border-color:#B4532A}.cfg .err{color:#B4532A;font-weight:700}.sum{color:var(--muted);margin:-8px 0 18px}.sum b{color:var(--ink)}
/* invito finale sopra il piede scuro */
.cta{position:relative;z-index:2;background:var(--beige);border-radius:var(--r);padding:clamp(28px,4vw,56px) clamp(24px,4vw,50px);display:grid;grid-template-columns:1fr 1fr;gap:24px 40px;align-items:center;margin-bottom:-186px}
@media (max-width:800px){.cta{grid-template-columns:1fr;margin-bottom:-120px}}.cta p{color:#6E6A5F;margin:0 0 22px}
.cta ul{display:flex;gap:10px 22px;flex-wrap:wrap;list-style:none;padding:0;margin:22px 0 0;font-weight:500}.cta li+li::before{content:"•";margin-right:22px;margin-left:-12px}
.ftr{background:var(--dark);color:#E9E3D9;border-radius:var(--r) var(--r) 0 0;margin:0 8px;padding:250px 0 26px}@media (max-width:800px){.ftr{padding-top:170px}}
.ftr .g{display:grid;grid-template-columns:1.6fr 1fr 1fr 1.2fr;gap:30px}@media (max-width:900px){.ftr .g{grid-template-columns:1fr 1fr}}@media (max-width:520px){.ftr .g{grid-template-columns:1fr}}
.ftr .logo{font-size:1.8rem}.ftr p{color:#CFC8BC;max-width:32ch}.ftr b{display:block;color:#fff;font-size:1.15rem;margin-bottom:14px}.ftr ul{list-style:none;padding:0;margin:0;display:grid;gap:8px}.ftr a{color:#CFC8BC;text-decoration:none}.ftr a:hover{color:#fff}
.ftr .bt{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;border-top:1px solid #ffffff26;margin-top:50px;padding-top:24px;color:#CFC8BC}
.plain{max-width:820px;margin:0 auto;padding:150px 20px 80px}.plain h1{font-size:2.8rem;margin-bottom:20px}.small{font-size:.86rem;color:var(--muted)}
.sub{background:var(--dark);height:96px;margin:8px 8px 0;border-radius:var(--r)}
.wa{background:#1F7A4D}
"""

JS = b2.E_JS.replace("cfg.querySelector(\".q.on\");box.innerHTML=\"<div class='done'><h3>Invio in corso…</h3></div>\"",
                     "cfg.querySelector(\".q.on\");box.innerHTML=\"<div class='done'><h3>Invio in corso…</h3></div>\"") + r"""
// header: vetro scuro quando si scorre
var hd=document.querySelector(".hdr");function hs(){hd.classList.toggle("s",scrollY>40)}addEventListener("scroll",hs,{passive:true});hs();
// prima/dopo: cursore trascinabile (anche da tastiera)
document.querySelectorAll(".cmp").forEach(function(c){var r=c.querySelector("input");function set(v){c.style.setProperty("--x",v+"%")}r.addEventListener("input",function(){set(r.value)});
 var down=false;function mv(e){var b=c.getBoundingClientRect();var x=((e.touches?e.touches[0].clientX:e.clientX)-b.left)/b.width*100;x=Math.max(0,Math.min(100,x));r.value=x;set(x)}
 c.addEventListener("pointerdown",function(e){down=true;mv(e)});addEventListener("pointerup",function(){down=false});c.addEventListener("pointermove",function(e){if(down)mv(e)})});
// come lavoriamo: i passi si accendono con lo scorrimento della sezione fissata
var pr=document.querySelector(".proc");if(pr){var ss=pr.querySelectorAll(".pstep"),sl=pr.querySelector(".steps");
 function ps(){var b=pr.getBoundingClientRect(),p=Math.max(0,Math.min(1,-b.top/Math.max(1,b.height-innerHeight)));var i=Math.min(3,Math.floor(p*4));
  ss.forEach(function(s,j){s.classList.toggle("on",j<=i)});ss.forEach(function(s,j){s.classList.toggle("cur",j===i)});sl.style.setProperty("--p",(Math.min(1,p*1.33)*100)+"%")}
 addEventListener("scroll",ps,{passive:true});ps()}
"""

def crop(src, dst, box, w):
    im = Image.open(src).convert("RGB"); W, H = im.size
    im = im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H)))
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(dst, quality=82, optimize=True)

def logo(cls=""):
    return (f'<a class="logo {cls}" href="index.html" aria-label="Edil Trend SA, home"><svg viewBox="0 0 30 30" aria-hidden="true"><path d="M3 27V11L15 4l12 7v16" fill="none" stroke="currentColor" stroke-width="2.4"/>'
            '<path d="M10 27v-9h10v9" fill="#C3922E"/></svg>Edil Trend</a>')

def header(cur):
    L = [("index.html", "Home", "home"), ("index.html#servizi", "Servizi", "svc"), ("index.html#lavori", "Lavori", "works"), ("index.html#come", "Come lavoriamo", "how"), ("index.html#zone", "Zone", "zone")]
    return (f'<header class="hdr"><div class="wrap">{logo()}<nav class="pill nav" aria-label="Principale">'
            + "".join(f'<a href="{h}"{" class=on" if k == cur else ""}>{t}</a>' for h, t, k in L)
            + f'</nav><a class="btn w" href="index.html#contatti">Contattaci {AR}</a><button class="menu" data-menu aria-expanded="false">Menu</button></div></header>')

def page(title, desc, body, v):
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#1C1C18">
<link rel="icon" href="favicon.svg" type="image/svg+xml">{FONTS}<link rel="stylesheet" href="assets/site.css?v={v}">{IMPORTMAP}</head>
<body><a class="skip" href="#main">Vai al contenuto</a>{body}<a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Scrivici su WhatsApp">WhatsApp</a>
<script src="assets/app.js?v={v}" defer></script></body></html>"""

def footer():
    return f"""<footer class="ftr"><div class="wrap"><div class="g"><div>{logo()}<p>Impresa generale del Gruppo New Trends a Lugano: costruiamo e ristrutturiamo case fatte per durare, dal 1999.</p></div>
<div><b>Il sito</b><ul><li><a href="index.html">Home</a></li><li><a href="index.html#servizi">Servizi</a></li><li><a href="progetti.html">Lavori</a></li><li><a href="index.html#come">Come lavoriamo</a></li><li><a href="index.html#zone">Zone</a></li></ul></div>
<div><b>Il gruppo</b><ul><li><a href="{SITES['newtrends']}">New Trends · Immobiliare</a></li><li><a href="{SITES['architrend']}">Archi Trend · Architettura</a></li><li><a href="{SITES['ediltrend']}">Edil Trend · Costruzioni</a></li></ul></div>
<div><b>Contatti</b><ul><li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li>{ADDR}</li></ul></div></div>
<div class="bt"><span>© Edil Trend SA · Parte del Gruppo New Trends</span><span><a href="privacy.html">Privacy</a></span></div></div></footer>"""

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    A = os.path.join(OUT, "assets"); I = os.path.join(A, "img"); os.makedirs(I)
    img = {}
    def put(name, src, w, box=(0, 0, 1, 1)): crop(src, os.path.join(I, name), box, w); img[name] = "assets/img/" + name; return img[name]
    pr = lambda k: find_src(P[k][4])
    put("hero.jpg", pr("greenhorse"), 2000)
    put("s-nuove.jpg", pr("ferrari"), 900); put("s-impresa.jpg", pr("maraini"), 900); put("s-capomastro.jpg", pr("synthesis"), 900)
    put("s-ristr.jpg", pr("motta"), 700, (.45, 0, 1, 1)); put("s-cucine.jpg", pr("pregassona"), 700); put("s-facciate.jpg", pr("magliaso"), 600, (.5, .06, 1, .94))
    put("b1-pre.jpg", pr("magliaso"), 600, (0, .06, .5, .94)); put("b1-post.jpg", pr("magliaso"), 600, (.5, .06, 1, .94))
    put("b2-pre.jpg", pr("montagnola"), 600, (.5, 0, 1, .5)); put("b2-post.jpg", pr("montagnola"), 600, (.5, .5, 1, 1))
    bp = os.path.join(b2.BP, "residenza-optima-montagnola-bp.jpg"); ph = os.path.join(b2.BP, "residenza-optima-montagnola-ph.jpg")
    put("b3-pre.jpg", bp, 900); put("b3-post.jpg", ph, 900)
    put("why.jpg", pr("optima"), 1100); put("w1.jpg", pr("maraini"), 800); put("w2.jpg", pr("fortuna"), 800); put("w3.jpg", pr("ferrari"), 800)
    put("band.jpg", pr("aurea"), 1600); put("proc.jpg", pr("greenhorse"), 1400)
    shutil.copy(os.path.join(HERE, "src", "villa3d.js"), os.path.join(A, "villa3d.js"))
    open(os.path.join(OUT, "favicon.svg"), "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30"><rect width="30" height="30" rx="7" fill="#1C1C18"/><path d="M6 25V12l9-5 9 5v13" fill="none" stroke="#fff" stroke-width="2.2"/><path d="M11 25v-7h8v7" fill="#C3922E"/></svg>')

    services = [("Nuove costruzioni", "Case, ville e palazzine residenziali, dalle fondazioni alle finiture.", "Costruzione", "s-nuove.jpg"),
                ("Impresa generale", "Un solo contratto per tutta l'opera: coordiniamo gli artigiani e rispondiamo noi del risultato.", "Costruzione", "s-impresa.jpg"),
                ("Opere di capomastro", "Platee, murature, tramezze, aperture e intonaci, eseguiti con cura.", "Costruzione", "s-capomastro.jpg"),
                ("Ristrutturazioni complete", "Appartamenti, case e stabili: ridiamo valore a ciò che esiste.", "Ristrutturazione", "s-ristr.jpg"),
                ("Bagni e cucine", "Le stanze che usi ogni giorno, rifatte con materiali che durano.", "Ristrutturazione", "s-cucine.jpg"),
                ("Facciate e tetti", "Isolamento, intonaci e coperture per una casa protetta e più efficiente.", "Ristrutturazione", "s-facciate.jpg")]
    sv = "".join(f'<a class="reveal" href="#contatti"><div class="ph"><img src="{img[f]}" alt="" loading="lazy"><span class="chip">{E(t)}</span></div><div class="t"><h3>{E(a)}</h3><p>{E(b)}</p><span class="more">Scopri di più {AR}</span></div></a>' for a, b, t, f in services)
    bas = [("b1", "Palazzina a Magliaso", "Ristrutturazione, messa a reddito e rivendita", "Prima", "Dopo"),
           ("b2", "Appartamento a Montagnola", "Ristrutturazione e valorizzazione", "Prima", "Dopo"),
           ("b3", "Residenza Optima, Montagnola", "Dal progetto all'edificio costruito", "Progetto", "Costruito")]
    ba = "".join(f'<div class="reveal"><div class="cmp"><img src="{img[k + "-pre.jpg"]}" alt="{E(t)}: {E(l1).lower()}" loading="lazy"><img class="a" src="{img[k + "-post.jpg"]}" alt="{E(t)}: {E(l2).lower()}" loading="lazy">'
                 f'<span class="ln"></span><span class="lb l1">{l1}</span><span class="lb l2">{l2}</span><input type="range" min="0" max="100" value="50" aria-label="Confronta {E(l1).lower()} e {E(l2).lower()}: {E(t)}"><span class="hd" aria-hidden="true">‹›</span></div><h3>{E(t)}</h3><p>{E(s)}</p></div>' for k, t, s, l1, l2 in bas)
    why = [("prezzo", "Prezzo scritto.", "Voci e quantità nero su bianco prima di iniziare: sai sempre quanto spendi."),
           ("uno", "Un solo referente.", "Un capocantiere che coordina tutti gli artigiani e un numero da chiamare."),
           ("ordine", "Cantiere in ordine.", "Programma dei lavori chiaro, pulizia e rispetto di chi abita vicino."),
           ("dopo", "Dopo la consegna.", "Restiamo il tuo riferimento anche quando il cantiere è chiuso.")]
    wy = "".join(f'<div class="reveal"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[i]}</svg><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i, a, b in why)
    steps = [("Sopralluogo", "Veniamo sul posto, misuriamo e ascoltiamo cosa ti serve davvero."),
             ("Preventivo e contratto", "Voci, prezzi e tempi scritti e firmati prima di aprire il cantiere."),
             ("Il cantiere", "Un capocantiere coordina tutti gli artigiani e ti tiene aggiornato."),
             ("La consegna", "Collaudo insieme, ogni dettaglio sistemato. Poi restiamo il tuo riferimento.")]
    st = "".join(f'<div class="pstep{" on cur" if i == 0 else ""}"><span>STEP {i + 1:02d}</span><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i, (a, b) in enumerate(steps))
    works = [("maraini", "w1.jpg"), ("fortuna", "w2.jpg"), ("ferrari", "w3.jpg")]
    wk = "".join(f'<article class="reveal"><span class="k">{E(P[k][2])}</span><q>{E(P[k][3])}</q><img src="{img[f]}" alt="{E(P[k][0])}, {E(P[k][1])}" loading="lazy"><div class="who"><span>{E(P[k][0].split()[-1][0])}</span><div><b>{E(P[k][0])}</b><small>{E(P[k][1])}</small></div></div></article>' for k, f in works)
    # zone: posizioni approssimative sul Luganese (x,y in % della mappa)
    Z = [("Tesserete", 55, 20), ("Vezia", 48, 38), ("Savosa", 54, 42), ("Lugano", 60, 55), ("Pregassona", 70, 46), ("Muzzano", 38, 58), ("Collina d'Oro", 44, 70), ("Montagnola", 36, 72), ("Grancia", 52, 78), ("Magliaso", 18, 74), ("Corteglia", 66, 92)]
    show = {"Tesserete", "Lugano", "Montagnola", "Magliaso", "Savosa"}
    dots = "".join(f'<circle cx="{x}" cy="{y}" r=".55"/>' for x in range(2, 100, 3) for y in range(2, 100, 3) if ((x - 50) ** 2 / 2400 + (y - 52) ** 2 / 2600) < 1)
    lake = '<path d="M30 62c6-4 12-2 18 0s10 6 16 4 8-8 14-6 6 8 2 12-10 3-14 6-4 10-10 10-6-6-10-8-10 0-14-3-6-11-2-15z" fill="#ffffff14"/>'
    mp = (f'<div class="map reveal" role="img" aria-label="Le zone del Luganese dove ha lavorato il gruppo"><svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><g fill="#ffffff2e">{dots}</g>{lake}</svg>'
          + "".join(f'<span class="lab" style="left:{x}%;top:{y}%">{E(n)}</span>' for n, x, y in Z if n in show) + "</div>")
    places = "".join(f'<li>{PIN}{E(n)}</li>' for n, _, _ in Z)
    faqs = [("Fate anche piccoli lavori?", "Sì, anche opere di muratura e piccole ristrutturazioni. Raccontaci il lavoro e ti diciamo come possiamo aiutarti."),
            ("Il sopralluogo e il preventivo si pagano?", "No: il sopralluogo e il preventivo sono senza impegno."),
            ("Serve un architetto?", "Per i lavori che richiedono una licenza ti affianchiamo Archi Trend, lo studio di architettura del gruppo, oppure lavoriamo con il tuo architetto."),
            ("Chi seguo durante il cantiere?", "Un capocantiere di riferimento: coordina gli artigiani e ti aggiorna sull'avanzamento."),
            ("In quali zone lavorate?", "Soprattutto nel Luganese e nel resto del Ticino.")]
    fq = "".join(f'<details class="reveal"{" open" if i == 0 else ""}><summary>{E(q)}</summary><p>{E(a)}</p></details>' for i, (q, a) in enumerate(faqs))
    tiles = lambda items: '<div class="tiles">' + "".join(f'<button type="button" data-v="{E(v)}" aria-pressed="false">{f"<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\">{ICONS[ic]}</svg>" if ic else ""}<span>{E(v)}</span></button>' for v, ic in items) + "</div>"
    cfg = f"""<div class="cfg reveal" id="preventivo"><span class="tag">Preventivo</span><h2>Raccontaci il lavoro.</h2><p class="lead" style="margin-top:12px">Quattro domande, un minuto. Poi ti chiamiamo per il sopralluogo, senza impegno.</p><div class="prog" aria-hidden="true"><i></i></div>
<div class="q" data-k="lavoro"><span class="step">STEP 01 / 04</span><h3>Di che lavoro si tratta?</h3>{tiles([("Bagno", "bagno"), ("Cucina", "cucina"), ("Appartamento intero", "appartamento"), ("Casa", "casa"), ("Facciata o tetto", "facciata"), ("Opere di muratura", "muratura"), ("Nuova costruzione", "nuova"), ("Altro", "altro")])}</div>
<div class="q" data-k="misura"><span class="step">STEP 02 / 04</span><h3>Quanto è grande la superficie?</h3>{tiles([("Meno di 30 m²", None), ("30–80 m²", None), ("80–150 m²", None), ("Più di 150 m²", None), ("Non lo so ancora", None)])}<div class="nav2"><button class="back" type="button">← Indietro</button></div></div>
<div class="q" data-k="quando"><span class="step">STEP 03 / 04</span><h3>Quando vorresti iniziare?</h3>{tiles([("Il prima possibile", None), ("Entro 3 mesi", None), ("Tra 3 e 6 mesi", None), ("Sto valutando", None)])}<div class="nav2"><button class="back" type="button">← Indietro</button></div></div>
<div class="q" data-k="contatti"><span class="step">STEP 04 / 04</span><h3>Dove possiamo ricontattarti?</h3><p class="sum"></p><form novalidate><div class="row"><label>Nome e cognome<input name="name" autocomplete="name" required></label><label>Comune del lavoro<input name="town" placeholder="es. Lugano"></label></div>
<div class="row"><label>Email<input name="email" type="email" autocomplete="email"></label><label>Telefono<input name="phone" type="tel" autocomplete="tel"></label></div>
<label>Altre informazioni (facoltativo)<textarea name="message" rows="2" placeholder="es. bagno al secondo piano, senza ascensore"></textarea></label><input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
<label class="check"><input type="checkbox" name="consent" required><span>Acconsento a essere ricontattato da Edil Trend SA secondo l'<a href="privacy.html">informativa privacy</a>.</span></label>
<label class="check"><input type="checkbox" name="newsletter"><span>Desidero ricevere occasionalmente novità del Gruppo New Trends (facoltativo).</span></label><p class="err" hidden role="alert"></p>
<div class="nav2"><button class="back" type="button">← Indietro</button><button class="btn" type="submit">Richiedi il sopralluogo {AR}</button></div></form></div></div>"""
    G = lambda d: f'<svg viewBox="0 0 24 24" aria-hidden="true">{d}</svg>'
    home = f"""{header("home")}<section class="hero"><div class="f"><img src="{img['hero.jpg']}" alt="Residenza Green Horse, Muzzano" fetchpriority="high">
<div class="b"><div class="top"><h1><span>Dalle fondamenta</span><span>alle finiture perfette</span></h1><p>Costruiamo e ristrutturiamo case, ville e palazzine nel Luganese. Impresa generale del Gruppo New Trends dal 1999: un solo contratto, un prezzo scritto e tempi chiari, dal primo sopralluogo alla consegna delle chiavi.</p></div>
<div class="bot"><div class="acts"><a class="btn w" href="#contatti">Richiedi un preventivo gratuito {AR}</a><a class="btn o" href="#lavori">Guarda i lavori</a></div>
<ul class="checks"><li>{CHECK}Qualità</li><li>{CHECK}Precisione</li><li>{CHECK}Esperienza</li><li>{CHECK}Affidabilità</li></ul></div></div></div></section>
<main id="main">
<section class="sec" id="servizi"><div class="wrap"><div class="head"><div><span class="tag">I nostri servizi</span><h2>Tutto quello che possiamo costruire per te</h2></div>
<div class="r"><p class="lead">Che sia una stanza o un edificio intero, seguiamo tutto noi sotto un unico tetto, dall'inizio alla fine.</p><a class="btn" href="#contatti">Parlaci del lavoro {AR}</a></div></div><div class="svc">{sv}</div></div></section>
<section class="sec dk" id="lavori"><div class="wrap"><div class="head"><div><span class="tag">Prima e dopo</span><h2>Guarda la trasformazione.</h2></div>
<div class="r"><p class="lead">Trascina il cursore. Ogni lavoro parte da un'idea: ecco come è finito.</p><a class="btn bg" href="progetti.html">Tutti i lavori {AR}</a></div></div><div class="ba">{ba}</div></div></section>
<section class="sec"><div class="wrap why"><div class="reveal"><span class="tag">Perché noi</span><h2>Perché le famiglie ci affidano la loro casa.</h2><p class="lead" style="margin-top:18px">Niente scorciatoie, niente sorprese: un cantiere fatto di chiarezza e di mestiere.</p>
<div class="ph"><img src="{img['why.jpg']}" alt="Residenza Optima, Montagnola" loading="lazy"><div><b>Dal 1999</b><br>a Lugano, con il Gruppo New Trends</div></div></div><div class="wg">{wy}</div></div></section>
<section class="dk proc" id="come"><div class="st"><div class="wrap" style="display:flex;flex-direction:column;flex:1;min-height:0;width:100%"><div class="head"><div><span class="tag">Come lavoriamo</span><h2>Semplice, dall'inizio alla fine.</h2></div><p class="lead">Niente stress e niente sorprese: un percorso chiaro dalla prima idea alla consegna. Scorri e guarda la casa che si costruisce.</p></div>
<div class="steps"><i class="fill"></i>{st}</div>
<div class="stage3d" aria-label="Una villa che si costruisce mentre scorri le quattro fasi"><img src="{img['proc.jpg']}" alt="Residenza Green Horse, Muzzano" loading="lazy"><div class="bar"><i></i></div><span class="cap3d">Sopralluogo e tracciamento · 0%</span></div></div></div></section>
<section class="sec"><div class="wrap"><div class="revhead"><div><span class="tag">Lavori del gruppo</span><h2>Costruito con cura, consegnato con precisione.</h2></div><p class="lead">Alcuni dei progetti seguiti dalle aziende del Gruppo New Trends.</p></div><div class="wk">{wk}</div>
<div class="facts reveal"><div>Dal 1999 a Lugano</div><div>100+ unità realizzate dal gruppo</div><div>300+ professionisti in rete</div></div></div></section>
<section style="padding-bottom:clamp(70px,8vw,110px)"><div class="wrap"><div class="band reveal"><img src="{img['band.jpg']}" alt="" loading="lazy"><div class="tx"><span class="tag">Gruppo New Trends</span><h2>Dal terreno alle chiavi, un solo gruppo.</h2>
<p>New Trends trova il terreno o l'immobile, Archi Trend progetta e ottiene la licenza, Edil Trend costruisce, New Trends vende o affitta. Un unico interlocutore per tutto il percorso.</p><a class="btn w" href="{SITES['newtrends']}">Scopri il gruppo {AR}</a></div>
<div class="glass"><b>4 aziende</b>un solo percorso</div></div></div></section>
<section style="padding-bottom:clamp(70px,8vw,110px)" id="zone"><div class="wrap zones">{mp}<div class="reveal"><span class="tag">Zone</span><h2>Di casa nel Luganese.</h2><p class="lead" style="margin-top:16px">Vicini, conosciuti e sempre a portata di mano. Questi sono alcuni dei comuni in cui il gruppo ha costruito o ristrutturato.</p>
<ul class="places">{places}</ul><a class="btn" href="#contatti">Chiedi un sopralluogo {AR}</a></div></div></section>
<section class="sec dk"><div class="wrap gua"><div class="reveal"><span class="tag">La nostra esperienza</span><h2>{YEARS} anni di cantieri, scritti nero su bianco.</h2>
<div class="ring" aria-hidden="true"><div><b>{YEARS}</b><small>ANNI<span>DI ESPERIENZA</span></small></div></div></div>
<div><div class="gl"><div class="reveal">{G(ICONS['prezzo'])}Sopralluogo e preventivo senza impegno</div><div class="reveal">{G(ICONS['ordine'])}Prezzo scritto prima di iniziare</div><div class="reveal">{G(ICONS['dopo'])}Tempi e capitolato messi per iscritto</div></div>
<p class="note">Il preventivo è senza impegno e i consigli sono onesti. Prezzo, tempi e capitolato li firmiamo prima di aprire il cantiere, e restiamo il tuo riferimento anche dopo la consegna.</p></div></div></section>
<section class="sec" id="faq"><div class="wrap"><div class="faq"><span class="tag">Domande</span><h2>Domande frequenti.</h2>{fq}</div></div></section>
<section style="padding-bottom:clamp(70px,8vw,110px)"><div class="wrap">{cfg}</div></section>
<section id="contatti"><div class="wrap"><div class="cta reveal"><div><span class="tag">Iniziamo</span><h2>Pronto a costruire o rinnovare casa?</h2></div>
<div><p>Hai visto i lavori e come lavoriamo. Il passo successivo è semplice: prenota un sopralluogo gratuito e parliamo del tuo progetto.</p><a class="btn" href="#preventivo">Contattaci {AR}</a><ul><li>Gratuito</li><li>Senza impegno</li><li>Risponde una persona</li></ul></div></div></div></section>
</main>{footer()}<script type="module" src="assets/villa3d.js?v=V3D"></script>"""
    sub = header("works") + '<div class="sub"></div>'
    allw = ["maraini", "fortuna", "optima", "miracolli", "ferrari", "greenhorse", "aurea", "synthesis", "magliaso", "corteglia", "motta", "pregassona", "montagnola"]
    for k in allw: put(f"p-{k}.jpg", pr(k), 900)
    pj = "".join(f'<article class="reveal"><span class="k">{E(P[k][2])}</span><q>{E(P[k][3])}</q><img src="{img["p-" + k + ".jpg"]}" alt="{E(P[k][0])}, {E(P[k][1])}" loading="lazy"><div class="who"><span>{E(P[k][0].split()[-1][0])}</span><div><b>{E(P[k][0])}</b><small>{E(P[k][1])}</small></div></div></article>' for k in allw)
    pages = {"index.html": ("Edil Trend SA · Impresa generale a Lugano", "Impresa generale del Gruppo New Trends a Lugano: nuove costruzioni, ristrutturazioni e opere di capomastro.", home),
             "progetti.html": ("Lavori · Edil Trend SA", "Lavori del Gruppo New Trends.", f'{sub}<main id="main"><section class="sec"><div class="wrap"><span class="tag">Lavori del gruppo</span><h1 style="font-size:clamp(2.6rem,1.6rem + 3vw,4.4rem);margin-bottom:36px">Costruito con cura, consegnato con precisione.</h1><div class="wk">{pj}</div></div></section></main>{footer()}'),
             "privacy.html": ("Privacy · Edil Trend SA", "Informativa privacy.", f'{sub}<main id="main">{b2.privacy("Edil Trend SA")}</main>{footer()}')}
    v = hashlib.sha256((CSS + JS + open(os.path.join(HERE, "src", "villa3d.js")).read()).encode()).hexdigest()[:10]
    open(os.path.join(A, "site.css"), "w").write(CSS); open(os.path.join(A, "app.js"), "w").write("(function(){" + JS + "})();")
    for n, (t, d, body) in pages.items(): open(os.path.join(OUT, n), "w").write(page(t, d, body.replace("V3D", v), v))
    open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
    print("ok", OUT)

if __name__ == "__main__":
    build()
