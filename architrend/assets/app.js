(function(){
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{threshold:.15});
document.querySelectorAll(".reveal").forEach(function(x){io.observe(x)});
function sendReq(d,box,okHtml,waText){return fetch("https://crm-newtrends.2-29-109-125.sslip.io/api/pubblico/richiesta",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)}).then(function(r){if(!r.ok)throw 0;box.innerHTML=okHtml},function(){box.innerHTML="<h3>Non siamo riusciti a inviare la richiesta.</h3><p>Mandacela su WhatsApp con un tocco, è già scritta.</p><a class='btn' target='_blank' rel='noopener' href='https://wa.me/41768232203?text="+encodeURIComponent(waText)+"'>Manda su WhatsApp</a>"})}
var mb=document.querySelector("[data-menu]");if(mb)mb.addEventListener("click",function(){var n=document.querySelector(".nav");var o=n.classList.toggle("open");mb.setAttribute("aria-expanded",o)});

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
})();