// Circuito Gold v5: entrate allo scorrimento, sezione fissa «Come funziona», parallasse leggera sulle foto, contatori, scelta a bottoni nel modulo.
// Solo transform/opacity. Con «riduci animazioni» niente movimento (la classe cg5-anim non c'è) e «Come funziona» resta una lista normale.
(function () {
  window.CG5 = 1;
  var H = document.documentElement, rm = matchMedia('(prefers-reduced-motion: reduce)').matches, lite = H.classList.contains('lite');
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var root = document.querySelector('.cg5'), hdr = document.querySelector('.hdr');
  function setHdr() { if (root && hdr) root.style.setProperty('--hdr', hdr.offsetHeight + 'px'); }
  setHdr();

  // modulo: «Cosa vuoi fare?» a bottoni (la select vera resta e viene inviata)
  $$('.cg5-form').forEach(function (f) {
    var sel = f.querySelector('select[name=intent]'), seg = f.querySelector('.cg5-seg');
    if (!sel || !seg) return;
    seg.hidden = false; f.classList.add('cg5-seg-on');
    $$('button', seg).forEach(function (b) {
      b.addEventListener('click', function () {
        sel.value = b.dataset.v;
        $$('button', seg).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      });
    });
  });

  // entrate: gruppi [data-rg], elementi [data-r] con ritardo a scalare
  var rs = $$('.cg5 [data-r]');
  rs.forEach(function (e) {
    var g = e.closest('[data-rg]'), k = g ? $$('[data-r]', g).indexOf(e) : 0;
    e.style.setProperty('--d', (Math.min(k, 6) * 0.08) + 's');
  });
  if (!rm && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });
    rs.forEach(function (e) { io.observe(e); });
  } else rs.forEach(function (e) { e.classList.add('in'); });

  // contatori (4,9 · 35 · 700+)
  if (!rm && 'IntersectionObserver' in window) $$('.cg5 [data-count]').forEach(function (b) {
    var to = parseFloat(b.dataset.count), dec = String(b.dataset.count).indexOf('.') > -1, suf = b.dataset.suf || '', fin = b.textContent;
    new IntersectionObserver(function (es, o) {
      if (!es[0].isIntersecting) return; o.disconnect(); var t0 = null;
      (function f(t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 1400), v = to * (1 - Math.pow(1 - k, 3));
        b.textContent = k < 1 ? (dec ? v.toFixed(1).replace('.', ',') : Math.round(v) + suf) : fin; if (k < 1) requestAnimationFrame(f); })(performance.now());
    }, { threshold: 0.6 }).observe(b);
  });

  // «Come funziona»: sezione fissa, il passo attivo segue lo scorrimento
  var how = document.querySelector('.cg5-how'), steps = how ? $$('.cg5-step', how) : [], rail = how && how.querySelector('.cg5-rail'), ol = how && how.querySelector('.cg5-steps');
  var pinOn = false;
  function layoutPin() {
    if (!pinOn) return;
    var mob = innerWidth <= 900;
    if (!mob && rail && ol) { rail.style.setProperty('--rt', ol.offsetTop + 'px'); rail.style.setProperty('--rh', ol.offsetHeight + 'px'); }
    if (mob) { // spazio per la figura tra il titolo e il testo del passo
      var copy = how.querySelector('.cg5-how-copy'), r = how.querySelector('.cg5-rail'), top = r.offsetTop + 22, txt = 0;
      steps.forEach(function (s) { txt = Math.max(txt, s.querySelector('div').offsetHeight); });
      var bottom = txt + 96 + 26;
      steps.forEach(function (s) { var v = s.querySelector('.cg5-vin'); v.style.setProperty('--vt', top + 'px'); v.style.setProperty('--vb', bottom + 'px'); });
    }
  }
  if (how && steps.length && !rm) { how.classList.add('is-pin'); pinOn = true; steps[0].classList.add('is-on'); layoutPin(); }

  // parallasse: foto con data-par (spostamento in px = velocità × distanza dal centro dello schermo)
  var par = (!rm && !lite) ? $$('.cg5 [data-par]') : [], vis = new Set();
  if (par.length && 'IntersectionObserver' in window) {
    var pio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) vis.add(e.target); else vis.delete(e.target); }); }, { rootMargin: '120px 0px' });
    par.forEach(function (p) { pio.observe(p); });
  }
  var stage = document.querySelector('.cg5-stage'), hero = document.querySelector('.cg5-hero');
  var ticking = false, cur = -1;
  function upd() {
    ticking = false; var vh = innerHeight;
    if (pinOn) {
      var r = how.getBoundingClientRect(), pinH = how.querySelector('.cg5-pin').offsetHeight, top = hdr ? hdr.offsetHeight : 76;
      var p = Math.max(0, Math.min(1, (top - r.top) / Math.max(1, r.height - pinH)));
      var k = p < 0.34 ? 0 : p < 0.67 ? 1 : 2;
      if (rail) rail.style.setProperty('--p', p.toFixed(3));
      if (k !== cur) { cur = k; steps.forEach(function (s, j) { s.classList.toggle('is-on', j === k); }); }
    }
    vis.forEach(function (el) {
      var b = el.parentNode.getBoundingClientRect(), c = (b.top + b.height / 2 - vh / 2);
      el.style.setProperty('--py', (c * parseFloat(el.dataset.par)).toFixed(1) + 'px');
    });
    if (stage && hero && !rm && !lite) { // la tessera sale piano mentre la prima schermata esce
      var y = scrollY, hh = hero.offsetHeight;
      if (y < hh * 1.2) stage.style.transform = 'translate3d(0,' + (y * -0.12).toFixed(1) + 'px,0)';
    }
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', function () { setHdr(); layoutPin(); onScroll(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { layoutPin(); onScroll(); });
  upd();
})();
