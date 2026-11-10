(function(){
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{threshold:.15});
document.querySelectorAll(".reveal").forEach(function(x){io.observe(x)});
function sendReq(d,box,okHtml,waText){return fetch("https://crm-newtrends.179-237-67-3.sslip.io/api/pubblico/richiesta",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)}).then(function(r){if(!r.ok)throw 0;box.innerHTML=okHtml},function(){box.innerHTML="<h3>Non siamo riusciti a inviare la richiesta.</h3><p>Mandacela su WhatsApp con un tocco, è già scritta.</p><a class='btn' target='_blank' rel='noopener' href='https://wa.me/41768232203?text="+encodeURIComponent(waText)+"'>Manda su WhatsApp</a>"})}
var mb=document.querySelector("[data-menu]");if(mb)mb.addEventListener("click",function(){var n=document.querySelector(".nav");var o=n.classList.toggle("open");mb.setAttribute("aria-expanded",o)});

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

// ---- reazioni al mouse: evidenziatore del menu, pulsanti "magnetici" e luce sulle schede (non in modalità leggera) ----
var fine=matchMedia("(hover:hover) and (pointer:fine)").matches;
var nv=document.querySelector(".hdr .nav");if(nv&&fine){var hl=document.createElement("i");hl.className="hl";hl.setAttribute("aria-hidden","true");nv.appendChild(hl);
 function mv(a){hl.style.transform="translateX("+a.offsetLeft+"px) scaleX("+(a.offsetWidth/100)+")"}
 nv.querySelectorAll("a").forEach(function(a){a.addEventListener("mouseenter",function(){if(innerWidth<=1080)return;mv(a);nv.classList.add("hlon")});a.addEventListener("focus",function(){if(innerWidth>1080){mv(a);nv.classList.add("hlon")}})});
 nv.addEventListener("mouseleave",function(){nv.classList.remove("hlon")});nv.addEventListener("focusout",function(){nv.classList.remove("hlon")})}
if(fine&&!rm&&!lite){document.querySelectorAll(".hero .btn:not(.ghost),.band .btn:not(.ghost),.dcta .btn:not(.ghost),.phero .btn:not(.ghost)").forEach(function(b){var r=0;
  b.addEventListener("mousemove",function(e){if(r)return;r=requestAnimationFrame(function(){r=0;var q=b.getBoundingClientRect(),x=(e.clientX-q.left-q.width/2)/q.width,y=(e.clientY-q.top-q.height/2)/q.height;b.style.setProperty("--mx",(x*8).toFixed(1)+"px");b.style.setProperty("--my",(y*6).toFixed(1)+"px")})});
  b.addEventListener("mouseleave",function(){b.style.setProperty("--mx","0px");b.style.setProperty("--my","0px")})});
 document.querySelectorAll(".card").forEach(function(c){var sp=document.createElement("i");sp.className="spot";sp.setAttribute("aria-hidden","true");c.prepend(sp);var r=0;
  c.addEventListener("mousemove",function(e){if(r)return;r=requestAnimationFrame(function(){r=0;var q=c.getBoundingClientRect();sp.style.setProperty("--sx",(e.clientX-q.left)+"px");sp.style.setProperty("--sy",(e.clientY-q.top)+"px")})})})}
var hd=document.querySelector(".hdr");function hs(){hd.classList.toggle("s",scrollY>30)}addEventListener("scroll",hs,{passive:true});hs();
// cursore disegno/realtà e prima/dopo
document.querySelectorAll(".cmp").forEach(function(c){var r=c.querySelector("input");function set(v){c.style.setProperty("--x",v+"%")}r.addEventListener("input",function(){set(r.value)});
 var down=false;function mv(e){var b=c.getBoundingClientRect();var x=Math.max(0,Math.min(100,(e.clientX-b.left)/b.width*100));r.value=x;set(x)}
 c.addEventListener("pointerdown",function(e){down=true;mv(e)});addEventListener("pointerup",function(){down=false});c.addEventListener("pointermove",function(e){if(down)mv(e)})});
// numeri veri che contano quando si vedono
document.querySelectorAll("[data-count]").forEach(function(b){if(rm||lite)return;var to=+b.dataset.count,from=+(b.dataset.from||0),suf=b.dataset.suf||"";b.textContent=from+suf;
 new IntersectionObserver(function(es,o){if(!es[0].isIntersecting)return;o.disconnect();var t0=0;function f(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/1400);b.textContent=Math.round(from+(to-from)*(1-Math.pow(1-k,3)))+suf;if(k<1)requestAnimationFrame(f)}requestAnimationFrame(f)},{threshold:.6}).observe(b)});
// progetti: filtro
document.querySelectorAll(".tabs button").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll(".tabs button").forEach(function(x){x.setAttribute("aria-pressed",x===b)});var f=b.dataset.f,n=0;document.querySelectorAll(".pgrid .pc[data-f]").forEach(function(w){w.hidden=!!f&&w.dataset.f!==f;if(!w.hidden)n++});var pn=document.querySelector(".pnone");if(pn)pn.hidden=n>0})});
var frs=document.querySelector("[data-freset]");if(frs)frs.addEventListener("click",function(){document.querySelector('.tabs button[data-f=""]').click()});
// processo: fase attiva
var ph=document.querySelectorAll(".ph4 article");if(ph.length){var po=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)ph.forEach(function(a){a.classList.toggle("on",a===e.target)})})},{rootMargin:"-40% 0px -50% 0px"});ph.forEach(function(a){po.observe(a)})}
// modelli 3D: three.js si carica solo quando un modello è vicino allo schermo
// in modalità leggera niente three.js: resta la foto con il pulsante "Guarda in 3D"
var t3=document.querySelectorAll("[data-3d]"),l3=false;function load3d(){if(l3)return;l3=true;var s=document.createElement("script");s.type="module";s.src="assets/archi3d.js?v=a25b92ef82";document.body.appendChild(s)}
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
})();