(function(){
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{threshold:.15});
document.querySelectorAll(".reveal").forEach(function(x){io.observe(x)});
function sendReq(d,box,okHtml,waText){return fetch("https://crm-newtrends.179-237-67-3.sslip.io/api/pubblico/richiesta",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)}).then(function(r){if(!r.ok)throw 0;box.innerHTML=okHtml},function(){box.innerHTML="<h3>Non siamo riusciti a inviare la richiesta.</h3><p>Mandacela su WhatsApp con un tocco, è già scritta.</p><a class='btn' target='_blank' rel='noopener' href='https://wa.me/41768232203?text="+encodeURIComponent(waText)+"'>Manda su WhatsApp</a>"})}
var mb=document.querySelector("[data-menu]");if(mb)mb.addEventListener("click",function(){var n=document.querySelector(".nav");var o=n.classList.toggle("open");mb.setAttribute("aria-expanded",o)});

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
 function done(e){setTimeout(function(){e.style.transitionDelay="";e.classList.remove("rv","rvi","reveal")},1300)}   // poi tornano libere le animazioni al passaggio del mouse
 var ob=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add("in");ob.unobserve(x.target);done(x.target)}})},{threshold:.12,rootMargin:"0px 0px -5% 0px"});
 all.forEach(function(e){ob.observe(e)});
 // rete di sicurezza: se si salta oltre (ancore, scorrimento velocissimo) ciò che è già sopra o sullo schermo compare comunque
 var tm=0;function chk(){tm=0;var h=innerHeight,left=0;all.forEach(function(e){if(e.classList.contains("in"))return;left++;if(e.getBoundingClientRect().top<h){e.classList.add("in");ob.unobserve(e);done(e)}});if(!left)removeEventListener("scroll",sc)}
 function sc(){if(!tm)tm=setTimeout(chk,250)}addEventListener("scroll",sc,{passive:true})})();
// scorrimento a inerzia leggero (Lenis) solo con mouse, mai su touch, in modalità leggera o con "riduci animazioni"
if(!LITE()&&!RM&&!matchMedia("(pointer: coarse)").matches){var ls=document.createElement("script");ls.src="https://cdn.jsdelivr.net/npm/lenis@1.3.27/dist/lenis.min.js";ls.async=true;
 ls.onload=function(){if(LITE()||!window.Lenis)return;var L=window.LENIS=new Lenis({lerp:.1,smoothWheel:true,syncTouch:false});(function r(t){if(window.LENIS){L.raf(t);requestAnimationFrame(r)}})(performance.now());
  document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(!a||!window.LENIS)return;var id=a.getAttribute("href"),el=id.length>1&&document.getElementById(id.slice(1));if(!el)return;e.preventDefault();L.scrollTo(el,{offset:-96})})};document.head.appendChild(ls)}
// segnali al passaggio del mouse: evidenziatore che scivola nel menu, luce che segue il cursore sulle card, pulsanti principali "magnetici"
(function(){if(!matchMedia("(hover: hover) and (pointer: fine)").matches)return;var pill=document.querySelector(".pill");
 if(pill){var hl=document.createElement("span");hl.className="hl";hl.setAttribute("aria-hidden","true");pill.insertBefore(hl,pill.firstChild);
  [].forEach.call(pill.querySelectorAll("a"),function(a){a.addEventListener("mouseenter",function(){pill.style.setProperty("--hx",a.offsetLeft+"px");pill.style.setProperty("--hw",a.offsetWidth+"px");pill.classList.add("hov")})});
  pill.addEventListener("mouseleave",function(){pill.classList.remove("hov")})}
 if(RM||LITE())return;
 [].forEach.call(document.querySelectorAll(".svc a,.wk a,.get"),function(c){var sp=document.createElement("span");sp.className="spot";sp.setAttribute("aria-hidden","true");c.insertBefore(sp,c.firstChild);var tk=0,ev;
  c.addEventListener("pointermove",function(e){ev=e;if(tk)return;tk=requestAnimationFrame(function(){tk=0;var r=c.getBoundingClientRect();c.style.setProperty("--mx",(ev.clientX-r.left)+"px");c.style.setProperty("--my",(ev.clientY-r.top)+"px")})})});
 [].forEach.call(document.querySelectorAll(".hero .btn.w,.cta .btn,.btn.g"),function(b){var tk=0,ev;b.addEventListener("pointermove",function(e){ev=e;if(tk)return;tk=requestAnimationFrame(function(){tk=0;if(LITE())return;var r=b.getBoundingClientRect();
  b.style.transform="translate("+((ev.clientX-r.left-r.width/2)*.12).toFixed(1)+"px,"+((ev.clientY-r.top-r.height/2)*.22-2).toFixed(1)+"px)"})});b.addEventListener("pointerleave",function(){b.style.transform=""})})})();
// lavori: messaggio se un filtro non trova niente
var emp=document.querySelector(".empty");if(emp)document.querySelectorAll(".tabs button").forEach(function(b){b.addEventListener("click",function(){var n=[].filter.call(document.querySelectorAll(".wk .work"),function(w){return !w.hidden}).length;emp.classList.toggle("on",!n)})});
// preventivo: il tipo di lavoro può arrivare dalla pagina del servizio (?lavoro=Bagno)
var lv=new URLSearchParams(location.search).get("lavoro");if(lv){var tb=document.querySelector('.q[data-k=lavoro] button[data-v="'+lv.replace(/"/g,"")+'"]');if(tb)tb.click()}
})();