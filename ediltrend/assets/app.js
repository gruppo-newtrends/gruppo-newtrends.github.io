(function(){
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{threshold:.15});
document.querySelectorAll(".reveal").forEach(function(x){io.observe(x)});
function sendReq(d,box,okHtml,waText){return fetch("https://crm-newtrends.2-29-109-125.sslip.io/api/pubblico/richiesta",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)}).then(function(r){if(!r.ok)throw 0;box.innerHTML=okHtml},function(){box.innerHTML="<h3>Non siamo riusciti a inviare la richiesta.</h3><p>Mandacela su WhatsApp con un tocco, è già scritta.</p><a class='btn' target='_blank' rel='noopener' href='https://wa.me/41768232203?text="+encodeURIComponent(waText)+"'>Manda su WhatsApp</a>"})}
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

var RM=matchMedia("(prefers-reduced-motion: reduce)").matches;
// header pieno quando si scorre
var hd=document.querySelector(".hdr");function hs(){hd.classList.toggle("s",scrollY>40)}addEventListener("scroll",hs,{passive:true});hs();
// prima/dopo: cursore trascinabile (anche da tastiera)
document.querySelectorAll(".cmp").forEach(function(c){var r=c.querySelector("input");function set(v){c.style.setProperty("--x",v+"%")}r.addEventListener("input",function(){set(r.value)});
 var down=false;function mv(e){var b=c.getBoundingClientRect();var x=(e.clientX-b.left)/b.width*100;x=Math.max(0,Math.min(100,x));r.value=x;set(x)}
 c.addEventListener("pointerdown",function(e){down=true;mv(e)});addEventListener("pointerup",function(){down=false});c.addEventListener("pointermove",function(e){if(down)mv(e)})});
// come lavoriamo: i passi si accendono con lo scorrimento della sezione fissata (solo trasformazioni, niente layout)
var prc=document.querySelector(".proc");if(prc){var ss=prc.querySelectorAll(".pstep"),sl=prc.querySelector(".steps"),li=-1,tk=0;
 function ps(){tk=0;var b=prc.getBoundingClientRect();if(b.bottom<0||b.top>innerHeight)return;var p=Math.max(0,Math.min(1,-b.top/Math.max(1,b.height-innerHeight)));var i=Math.min(3,Math.floor(p*4));
  if(i!==li){li=i;ss.forEach(function(s,j){s.classList.toggle("on",j<=i);s.classList.toggle("cur",j===i)})}sl.style.setProperty("--p",Math.min(1,p*1.33).toFixed(3))}
 addEventListener("scroll",function(){if(!tk)tk=requestAnimationFrame(ps)},{passive:true});ps()}
// three.js: si carica solo quando la sezione è vicina (e mai con "riduci animazioni")
var s3=document.querySelector(".stage3d[data-src]");if(s3&&!RM&&"IntersectionObserver" in window){var lo=new IntersectionObserver(function(es){if(!es[0].isIntersecting)return;lo.disconnect();
 var s=document.createElement("script");s.type="module";s.src=s3.dataset.src;document.body.appendChild(s)},{rootMargin:"900px 0px"});lo.observe(s3)}
// numeri veri che contano fino al valore (il testo finale è già nell'HTML)
if(!RM)document.querySelectorAll("[data-n]").forEach(function(b){var to=+b.dataset.n,suf=b.dataset.suf||"";new IntersectionObserver(function(es,o){if(!es[0].isIntersecting)return;o.disconnect();var t0=0;
 function f(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/1400);b.textContent=Math.round(to*(1-Math.pow(1-k,3)))+suf;if(k<1)requestAnimationFrame(f)}requestAnimationFrame(f)},{threshold:.6}).observe(b)});
// preventivo: il tipo di lavoro può arrivare dalla pagina del servizio (?lavoro=Bagno)
var lv=new URLSearchParams(location.search).get("lavoro");if(lv){var tb=document.querySelector('.q[data-k=lavoro] button[data-v="'+lv.replace(/"/g,"")+'"]');if(tb)tb.click()}
})();