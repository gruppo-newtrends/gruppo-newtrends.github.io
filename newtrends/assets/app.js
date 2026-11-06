
(function(){
var C=window.NT||{};var L=C.i18n||{};
function $(s,r){return (r||document).querySelector(s)}
function $$(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))}
function store(k,v){try{if(v===undefined){return JSON.parse(localStorage.getItem(k)||"null")}localStorage.setItem(k,JSON.stringify(v))}catch(e){return null}}
// header
var hdr=$(".hdr");function onS(){if(hdr&&document.body.classList.contains("home")){hdr.classList.toggle("solid",window.scrollY>40)}}
window.addEventListener("scroll",onS,{passive:true});onS();
// drawer
var dr=$("#drawer");$$("[data-open-drawer]").forEach(function(b){b.addEventListener("click",function(){dr.hidden=false;b.setAttribute("aria-expanded","true");var c=$("[data-close-drawer]",dr);c&&c.focus()})});
$$("[data-close-drawer]").forEach(function(b){b.addEventListener("click",function(){dr.hidden=true;var o=$("[data-open-drawer]");o&&o.setAttribute("aria-expanded","false");o&&o.focus()})});
document.addEventListener("keydown",function(e){if(e.key==="Escape"&&dr&&!dr.hidden){dr.hidden=true}});
$$(".langs a").forEach(function(a){a.addEventListener("click",function(){try{localStorage.setItem("nt_lang",a.getAttribute("hreflang"))}catch(e){}})});
// image fallback
$$("img[data-fallback]").forEach(function(im){function fb(){if(im.dataset.done)return;im.dataset.done=1;im.src=im.dataset.fallback;var t=im.parentNode.querySelector(".zph");if(t)t.hidden=false}
 im.addEventListener("error",fb);if(im.complete&&im.naturalWidth===0)fb()});
$$("img[data-hide-on-error]").forEach(function(im){function h(){im.hidden=true;var f=im.parentNode.querySelector(".fallback");if(f)f.hidden=false}im.addEventListener("error",h);if(im.complete&&im.naturalWidth===0)h()});
// tabs generic
$$("[data-tabs]").forEach(function(g){var bs=$$("button[role=tab]",g);bs.forEach(function(b){b.addEventListener("click",function(){bs.forEach(function(x){x.setAttribute("aria-selected",x===b?"true":"false")});
 var grp=g.getAttribute("data-tabs");$$("[data-panel-of='"+grp+"']").forEach(function(p){p.hidden=p.getAttribute("data-panel")!==b.getAttribute("data-key")});
 if(grp==="search"){var f=$("#hero-search");if(f){f.elements.c.value=b.getAttribute("data-key");var ps=f.elements.p;$$("option",ps).forEach(function(o){o.hidden=o.dataset.c&&o.dataset.c!==b.getAttribute("data-key")});ps.value=""}}
})})});
// hero search -> listings
var hs=$("#hero-search");if(hs){hs.addEventListener("submit",function(e){e.preventDefault();var q={};["c","z","t","r","p"].forEach(function(k){if(hs.elements[k]&&hs.elements[k].value)q[k]=hs.elements[k].value});
 try{sessionStorage.setItem("nt_q",JSON.stringify(q))}catch(x){}
 var s=Object.keys(q).map(function(k){return k+"="+encodeURIComponent(q[k])}).join("&");location.href=hs.getAttribute("action")+(s?"?"+s:"")})}
$$("a[data-q]").forEach(function(a){a.addEventListener("click",function(){try{sessionStorage.setItem("nt_q",a.getAttribute("data-q"))}catch(x){}})});
// favourites
var favs=store("nt_favs")||[];
function paintFav(){$$(".fav").forEach(function(b){var on=favs.indexOf(b.dataset.id)>-1;b.setAttribute("aria-pressed",on?"true":"false");b.setAttribute("aria-label",on?L.saved:L.save)})}
$$(".fav").forEach(function(b){b.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();var i=favs.indexOf(b.dataset.id);if(i>-1)favs.splice(i,1);else favs.push(b.dataset.id);store("nt_favs",favs);paintFav();if(window.ntFilter)ntFilter()})});paintFav();
// listings filter
var lg=$("#lgrid");if(lg){var fm=$("#lfilters");var q={};
 try{var sp=new URLSearchParams(location.search);sp.forEach(function(v,k){q[k]=v})}catch(x){}
 if(!Object.keys(q).length){try{q=JSON.parse(sessionStorage.getItem("nt_q")||"{}")||{}}catch(x){q={}}}
 try{sessionStorage.removeItem("nt_q")}catch(x){}
 ["c","z","t","r","p","s","f"].forEach(function(k){if(q[k]&&fm.elements[k]){fm.elements[k].value=q[k]}});
 var onlyFav=false;var fb=$("#onlyfav");
 if(fb)fb.addEventListener("click",function(){onlyFav=!onlyFav;fb.setAttribute("aria-pressed",onlyFav);ntFilter()});
 var cards=$$(".card",lg);
 window.ntFilter=function(){var c=fm.elements.c.value,z=fm.elements.z.value,t=fm.elements.t.value,r=parseFloat(fm.elements.r.value||0),p=parseFloat(fm.elements.p.value||0),s=fm.elements.s.value,f=fm.elements.f?fm.elements.f.value:"";
  var n=0;cards.forEach(function(el){var d=el.dataset;var ok=(!c||d.c===c)&&(!z||d.z===z)&&(!t||d.t===t)&&(!r||parseFloat(d.r||0)>=r)&&(!p||(parseFloat(d.p)<=p))&&(!f||(" "+d.f+" ").indexOf(" "+f+" ")>-1)&&(!onlyFav||favs.indexOf(d.id)>-1);
   if(d.sold==="1"&&(c||p))ok=false;el.hidden=!ok;if(ok)n++});
  var srt=cards.slice().sort(function(a,b){var A=a.dataset,B=b.dataset;if(A.sold!==B.sold)return A.sold==="1"?1:-1;
   if(s==="pa")return A.p-B.p;if(s==="pd")return B.p-A.p;if(s==="area")return (B.a||0)-(A.a||0);return A.o-B.o});
  srt.forEach(function(el){lg.appendChild(el)});
  $("#lcount").textContent=n+" "+L.results;$("#lempty").hidden=n>0;
  $$("option[data-c]",fm.elements.p).forEach(function(o){o.hidden=!!c&&o.dataset.c!==c})};
 fm.addEventListener("change",ntFilter);fm.addEventListener("submit",function(e){e.preventDefault()});
 $("#lreset").addEventListener("click",function(){fm.reset();onlyFav=false;fb&&fb.setAttribute("aria-pressed","false");ntFilter()});
 ntFilter()}
// gold switch
$$("[data-switch]").forEach(function(g){var bs=$$("button",g);bs.forEach(function(b){b.addEventListener("click",function(){bs.forEach(function(x){x.setAttribute("aria-selected",x===b?"true":"false")});$$("[data-gpanel]").forEach(function(p){p.hidden=p.dataset.gpanel!==b.dataset.key})})})});
// copy
function copyText(txt,btn){function ok(){var o=btn.textContent;btn.textContent=L.copied;setTimeout(function(){btn.textContent=o},1600)}
 try{navigator.clipboard.writeText(txt).then(ok,function(){sel(btn)})}catch(e){sel(btn)}}
function sel(btn){var t=btn.parentNode.querySelector("[data-copy-src]");if(!t)return;var r=document.createRange();r.selectNodeContents(t);var s=window.getSelection();s.removeAllRanges();s.addRange(r)}
$$("[data-copy]").forEach(function(b){b.addEventListener("click",function(){copyText(b.getAttribute("data-copy"),b)})});
// forms
function code(){var d=new Date();return "NT-"+String(d.getFullYear()).slice(2)+String(d.getMonth()+1).padStart(2,"0")+String(d.getDate()).padStart(2,"0")+"-"+Math.random().toString(36).slice(2,6).toUpperCase()}
$$("form[data-form]").forEach(function(f){f.addEventListener("submit",function(e){e.preventDefault();var bad=[];
 $$("[aria-invalid]",f).forEach(function(x){x.removeAttribute("aria-invalid")});
 $$("[required]",f).forEach(function(x){var v=x.type==="checkbox"?x.checked:String(x.value||"").trim();if(!v){bad.push(x);x.setAttribute("aria-invalid","true")}});
 var em=f.elements.email,ph=f.elements.phone;if(em&&ph&&!String(em.value).trim()&&!String(ph.value).trim()){bad.push(ph);ph.setAttribute("aria-invalid","true");em.setAttribute("aria-invalid","true")}
 var er=$(".err",f);if(bad.length){if(er){er.hidden=false;er.textContent=L.err}bad[0].focus();return}if(er)er.hidden=true;
 var data={form:f.getAttribute("data-form"),page:location.pathname,lang:document.documentElement.lang,code:code()};
 $$("input,select,textarea",f).forEach(function(x){if(!x.name||x.type==="checkbox")return;var lab=x.closest("label");data[x.name]=x.value});
 var lines=[L.waHead+" ("+data.code+")"];Object.keys(data).forEach(function(k){if(["form","page","lang","code"].indexOf(k)>-1||!data[k])return;var lab=f.querySelector("[name='"+k+"']");var name=lab&&lab.closest("label")?lab.closest("label").firstChild.textContent.trim():k;var val=data[k];if(lab&&lab.tagName==="SELECT"){val=lab.options[lab.selectedIndex].text}lines.push(name+": "+val)});
 var txt=lines.join("\n");var wa="https://wa.me/"+C.wa+"?text="+encodeURIComponent(txt);
 var box=document.createElement("div");box.className="done";box.setAttribute("role","status");
 function render(live){box.innerHTML="<h3>"+L.okT+"</h3><p>"+L.ok+" <code>"+data.code+"</code></p><p>"+(live?L.okLive:L.okWa)+"</p><div class='acts'><a class='btn btn-gold' target='_blank' rel='noopener' href='"+wa+"'>"+L.waBtn+"</a><button type='button' class='btn btn-line btn-sm'>"+L.copy+"</button></div><pre data-copy-src hidden></pre>";
  box.querySelector("pre").textContent=txt;box.querySelector("button").addEventListener("click",function(){copyText(txt,this)})}
 if(C.endpoint){fetch(C.endpoint,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)}).then(function(r){render(r.ok)},function(){render(false)})}else{render(false)}
 f.replaceWith(box);box.scrollIntoView({behavior:"smooth",block:"center"})})});
// affordability
var cf=$("#calc");if(cf){var pr=parseFloat(cf.dataset.price);var sl=$("#own");function fmt(n){return "CHF "+Math.round(n).toLocaleString(C.numLocale).replace(/,/g,C.sep)}
 function upd(){var ownP=parseFloat(sl.value)/100;var own=pr*ownP,mort=pr-own;var second=Math.max(0,mort-pr*2/3);var cost=mort*.05+pr*.01+second/15;
  $("#c_own").textContent=fmt(own)+" ("+Math.round(ownP*100)+"%)";$("#c_mort").textContent=fmt(mort);$("#c_cost").textContent=fmt(cost);$("#c_inc").textContent=fmt(cost*3)}
 sl.addEventListener("input",upd);upd()}
})();

// menu a tendina: apre dopo 80 ms al passaggio del mouse, chiude 220 ms dopo l'uscita (si può scendere sul pannello), anche da tastiera; Esc chiude
(function(){var items=document.querySelectorAll("[data-mega]");if(!items.length)return;var hdr=document.querySelector(".hdr"),cur=null,ot,ct;
 function set(it,on){it.classList.toggle("open",on);it.firstElementChild.setAttribute("aria-expanded",on?"true":"false")}
 function open(it){clearTimeout(ct);if(cur&&cur!==it)set(cur,false);cur=it;set(it,true);if(hdr)hdr.classList.add("mega-open")}
 function close(it){set(it,false);if(cur===it)cur=null;if(!cur&&hdr)hdr.classList.remove("mega-open")}
 items.forEach(function(it){
  it.addEventListener("mouseenter",function(){clearTimeout(ct);clearTimeout(ot);ot=setTimeout(function(){open(it)},cur?0:80)});
  it.addEventListener("mouseleave",function(){clearTimeout(ot);ct=setTimeout(function(){close(it)},220)});
  it.addEventListener("focusin",function(){open(it)});
  it.addEventListener("focusout",function(e){if(!it.contains(e.relatedTarget))close(it)});
  it.querySelectorAll(".mega a").forEach(function(a){a.addEventListener("click",function(){close(it)})})});
 document.addEventListener("keydown",function(e){if(e.key==="Escape"&&cur){var a=cur.firstElementChild;close(cur);a.focus()}});
})();

// 5 nov: entrate allo scroll, contatori, parallasse leggera, barra di avanzamento, barre di conversione, bottoni "magnetici"
(function(){var rm=matchMedia("(prefers-reduced-motion: reduce)").matches;
 var sel=".sec-head,.card,.path,.stat,.zone,.sit,.quote,.oitem,.step,.gpoint,.team-photo,.score,.alert,.val,.olist,.calc,.contact>div,.two>div,.gold-grid>div";
 var els=[].slice.call(document.querySelectorAll(sel)).filter(function(e){return !e.closest(".hdr,.mega,.drawer,.hero")});
 if(!rm&&"IntersectionObserver" in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{threshold:.12,rootMargin:"0px 0px -6% 0px"});
  els.forEach(function(e){var sib=[].slice.call(e.parentNode.children).filter(function(x){return x.matches(sel)});var k=sib.indexOf(e);e.style.setProperty("--d",(Math.min(k,5)*0.08)+"s");e.classList.add("rv");io.observe(e)})}
 if(!rm)document.querySelectorAll(".stat b").forEach(function(b){var m=b.textContent.match(/^(\d+)([.,]\d+)?(.*)$/);if(!m)return;var sep=m[2]?m[2][0]:"",to=parseFloat(m[1]+(m[2]?"."+m[2].slice(1):"")),suf=m[3];
  new IntersectionObserver(function(es,o){if(!es[0].isIntersecting)return;o.disconnect();var t0=null;function f(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/1500),v=to*(1-Math.pow(1-k,3));b.textContent=(sep?v.toFixed(1).replace(".",sep):Math.round(v))+suf;if(k<1)requestAnimationFrame(f)}requestAnimationFrame(f)},{threshold:.6}).observe(b)});
 var hb=document.querySelector(".hero-bg"),pr=document.querySelector(".sprog i"),cb=document.querySelector(".convbar"),mb=document.querySelector(".mobbar");
 var forms=[].slice.call(document.querySelectorAll("form.f,.done")),formVis=false,ticking=false;
 function upd(){ticking=false;var y=scrollY,h=document.documentElement.scrollHeight-innerHeight;if(pr)pr.style.transform="scaleX("+(h>0?Math.min(1,y/h):0)+")";
  if(hb&&!rm&&y<innerHeight*1.3)hb.style.transform="translateY("+(y*0.22)+"px)";
  formVis=[].slice.call(document.querySelectorAll("form.f,.done")).some(function(f){var r=f.getBoundingClientRect();return r.bottom>0&&r.top<innerHeight});
  if(cb)cb.classList.toggle("show",y>innerHeight*0.75&&!formVis);if(mb)mb.classList.toggle("show",y>240&&!formVis)}
 addEventListener("scroll",function(){if(!ticking){ticking=true;requestAnimationFrame(upd)}},{passive:true});upd();
 if(!rm&&matchMedia("(hover:hover)").matches)document.querySelectorAll(".btn-gold").forEach(function(b){b.addEventListener("mousemove",function(e){var r=b.getBoundingClientRect();b.style.transform="translate("+((e.clientX-r.left-r.width/2)*0.12).toFixed(1)+"px,"+((e.clientY-r.top-r.height/2)*0.25).toFixed(1)+"px)"});b.addEventListener("mouseleave",function(){b.style.transform=""})});
})();
