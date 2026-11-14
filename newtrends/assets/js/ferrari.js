/* Residenza Ferrari: entrate allo scorrimento, parallasse leggera, scelta dell'unità nel modulo. Niente animazioni con «riduci animazioni» o modalità leggera. */
(function(){
var d=document,h=d.documentElement,still=h.classList.contains("lite")||matchMedia("(prefers-reduced-motion: reduce)").matches;
var els=[].slice.call(d.querySelectorAll(".rf [data-rv]"));
if(still||!("IntersectionObserver" in window)){els.forEach(function(e){e.classList.add("in")})}
else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px",threshold:.08});
 els.forEach(function(e){io.observe(e)});
 setTimeout(function(){els.forEach(function(e){var r=e.getBoundingClientRect();if(r.top<innerHeight&&r.bottom>0)e.classList.add("in")})},2500)}
// parallasse: copertina e due foto grandi (solo transform, una volta per frame)
if(!still){var par=[].slice.call(d.querySelectorAll(".rf [data-par]")),tick=false;
 function upd(){tick=false;var vh=innerHeight;par.forEach(function(e){var r=e.getBoundingClientRect();if(r.bottom<0||r.top>vh)return;
  if(e.classList.contains("rf-hero-bg")){e.style.transform="translate3d(0,"+(scrollY*.25).toFixed(1)+"px,0)";return}
  var k=parseFloat(e.getAttribute("data-par"))||.05;var c=(r.top+r.height/2-vh/2);if(e.closest(".in"))e.style.transform="translate3d(0,"+(c*k).toFixed(1)+"px,0) scale(1.1)"})}
 addEventListener("scroll",function(){if(!tick){tick=true;requestAnimationFrame(upd)}},{passive:true})}
// «Richieda informazioni» su una unità: la sceglie nel modulo (il CRM ricava il rif. da «immobile-3006-x»)
var sel=d.getElementById("rf-unit"),rif=d.getElementById("rf-rif");
function sync(){if(sel&&rif)rif.value=sel.value}
if(sel){sel.addEventListener("change",sync);sync()}
[].slice.call(d.querySelectorAll("[data-unit]")).forEach(function(a){a.addEventListener("click",function(){if(sel){sel.value=a.getAttribute("data-unit");sync()}
 setTimeout(function(){var n=d.getElementById("rf-name");if(n)try{n.focus({preventScroll:true})}catch(e){}},700)})});
})();
