// Archi Trend: piccoli modelli three.js "da plastico" (volumi bianchi con spigoli sottili).
// Ogni contenitore [data-3d="preset"] diventa un modello: si gira trascinando (o con le frecce), ruota piano da solo
// e si ferma quando esce dallo schermo. [data-3d="morph"] = dal disegno all'edificio, guidato dallo scorrimento.
// Viene caricato da app.js solo quando il modello è vicino allo schermo. In modalità leggera (html.lite) parte solo con "Guarda in 3D":
// allora niente animazioni legate allo scorrimento né rotazione automatica, e il disegno/edificio del processo è mostrato già costruito.
import * as THREE from "three";

const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
// mentre la pagina scorre, la rotazione automatica si ferma (niente lavoro extra durante lo scorrimento)
let scrolling = 0; addEventListener("scroll", () => { scrolling = performance.now(); }, { passive: true });
const idle = window.requestIdleCallback || ((f) => setTimeout(f, 60));
const H = document.documentElement, inst = [];
const isLite = () => H.classList.contains("lite");
window.A3D = (el) => init(el, true);
document.querySelectorAll("[data-3d]").forEach((el) => { if (el.classList.contains("want3d")) init(el, true); else if (!reduce && !isLite()) idle(() => { if (!isLite()) init(el, false); }, { timeout: 800 }); });
// il sito ha scoperto che il computer è lento: ferma i modelli partiti da soli
document.addEventListener("archi-lite", () => inst.forEach((i) => { if (!i.demand) i.stop(); }));

function css(el, name, fb) { const v = getComputedStyle(el).getPropertyValue(name).trim(); return v || fb; }

function init(el, demand) {
  if (el.classList.contains("has3d")) return;
  let R;
  const small = innerWidth < 760;
  try { R = new THREE.WebGLRenderer({ antialias: !small, alpha: true, powerPreference: "low-power" }); } catch (e) { return; }
  if (!R.getContext()) return;
  R.setPixelRatio(Math.min(small ? 1 : 1.5, devicePixelRatio || 1));
  R.outputColorSpace = THREE.SRGBColorSpace; R.localClippingEnabled = true;
  R.domElement.setAttribute("aria-hidden", "true");
  el.prepend(R.domElement); el.classList.add("has3d");

  const calm = demand && (isLite() || reduce); // su richiesta in modalità leggera: niente animazioni automatiche
  const preset = el.dataset["3d"] === "morph" && calm ? "massa" : el.dataset["3d"];
  const fg = new THREE.Color(css(el, "--fg", "#ffffff")), acc = new THREE.Color(css(el, "--acc", "#B8962E"));
  const light = fg.r + fg.g + fg.b < 1.5; // testo scuro = sfondo chiaro
  const scene = new THREE.Scene();
  const cam = new THREE.PerspectiveCamera(small ? 38 : 30, 1, .5, 300);
  scene.add(new THREE.HemisphereLight(0xffffff, light ? 0xb9b2a6 : 0x3a3a3a, light ? 1.5 : 1.25));
  const sun = new THREE.DirectionalLight(0xffffff, 1.6); sun.position.set(-14, 24, 12); scene.add(sun);

  const M = {
    paper: new THREE.MeshStandardMaterial({ color: light ? "#FBFAF7" : "#ECE9E3", roughness: .9 }),
    old: new THREE.MeshStandardMaterial({ color: light ? "#CFCAC1" : "#8E8A84", roughness: .95 }),
    wood: new THREE.MeshStandardMaterial({ color: "#C9A77C", roughness: .8 }),
    acc: new THREE.MeshStandardMaterial({ color: acc, roughness: .6 }),
    glass: new THREE.MeshStandardMaterial({ color: "#9FB4BC", roughness: .15, metalness: .1, transparent: true, opacity: .55 }),
    water: new THREE.MeshStandardMaterial({ color: "#6FA7B4", roughness: .2, transparent: true, opacity: .85 }),
    tree: new THREE.MeshStandardMaterial({ color: light ? "#AEB59F" : "#7D8670", roughness: 1, flatShading: true }),
    edge: new THREE.LineBasicMaterial({ color: light ? "#3A3833" : "#2A2826", transparent: true, opacity: .55 }),
    plan: new THREE.LineBasicMaterial({ color: light ? "#2F2D29" : "#E9E4DA", transparent: true, opacity: .9 }),
    ghost: new THREE.LineDashedMaterial({ color: acc, dashSize: .35, gapSize: .25 }),
  };
  // ombra morbida finta sotto il modello (niente shadow map)
  const sh = document.createElement("canvas"); sh.width = sh.height = 128; const g = sh.getContext("2d");
  const gr = g.createRadialGradient(64, 64, 4, 64, 64, 64); gr.addColorStop(0, light ? "rgba(0,0,0,.22)" : "rgba(0,0,0,.55)"); gr.addColorStop(1, "rgba(0,0,0,0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
  const shadow = new THREE.Mesh(new THREE.PlaneGeometry(34, 26), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(sh), transparent: true, depthWrite: false }));
  shadow.rotation.x = -Math.PI / 2; shadow.position.y = .01; scene.add(shadow);
  const grid = new THREE.GridHelper(40, 40, light ? 0xd6d0c4 : 0x2c2c2c, light ? 0xe4dfd6 : 0x1f1f1f); grid.position.y = 0; scene.add(grid);

  const root = new THREE.Group(); scene.add(root);
  const items = []; let G = "vol"; const off = new Set();
  const clip = preset === "perizie" ? [new THREE.Plane(new THREE.Vector3(-1, 0, 0), .4)] : null;
  // volume con base a terra (cresce dal basso) e spigoli disegnati
  const box = (w, h, d, x, y, z, m = M.paper, t0 = 0, t1 = 1, mode = "grow", edges = true) => {
    const geo = new THREE.BoxGeometry(w, h, d); geo.translate(0, h / 2, 0);
    const me = new THREE.Mesh(geo, clip && m !== M.acc ? clipMat(m) : m); me.position.set(x, y, z); root.add(me);
    if (edges) me.add(new THREE.LineSegments(new THREE.EdgesGeometry(geo), clip ? clipLine() : M.edge));
    items.push({ g: G, o: me, t0, t1, mode, y }); return me;
  };
  const clipMats = new Map();
  function clipMat(m) { if (!clipMats.has(m)) { const c = m.clone(); c.clippingPlanes = clip; c.side = THREE.DoubleSide; clipMats.set(m, c); } return clipMats.get(m); }
  let cl; function clipLine() { if (!cl) { cl = M.edge.clone(); cl.clippingPlanes = clip; } return cl; }
  const roof = (w, h, d, x, y, z, m = M.paper, t0 = 0, t1 = 1) => { // tetto a due falde
    const s = new THREE.Shape(); s.moveTo(-w / 2, 0); s.lineTo(w / 2, 0); s.lineTo(0, h); s.closePath();
    const geo = new THREE.ExtrudeGeometry(s, { depth: d, bevelEnabled: false }); geo.translate(0, 0, -d / 2);
    const me = new THREE.Mesh(geo, m); me.position.set(x, y, z); me.add(new THREE.LineSegments(new THREE.EdgesGeometry(geo), M.edge)); root.add(me);
    items.push({ g: G, o: me, t0, t1, mode: "drop", y }); return me;
  };
  const tree = (x, z, s = 1, t0 = .85) => {
    const gq = new THREE.Group(); gq.position.set(x, 0, z);
    const c = new THREE.Mesh(new THREE.IcosahedronGeometry(.9 * s, 0), M.tree); c.position.y = 1.6 * s; c.scale.y = 1.25; gq.add(c);
    const tr = new THREE.Mesh(new THREE.CylinderGeometry(.08 * s, .1 * s, 1, 5), M.wood); tr.position.y = .5 * s; gq.add(tr);
    root.add(gq); items.push({ g: G, o: gq, t0, t1: t0 + .1, mode: "pop", y: 0 });
  };
  const outline = (pts, y = .03, t0 = 0, t1 = .2, m = M.plan) => { // pianta disegnata a terra
    const v = []; pts.forEach((p, i) => { const q = pts[(i + 1) % pts.length]; v.push(p[0], y, p[1], q[0], y, q[1]); });
    const geo = new THREE.BufferGeometry(); geo.setAttribute("position", new THREE.Float32BufferAttribute(v, 3));
    const ln = new THREE.LineSegments(geo, m); if (m.isLineDashedMaterial) ln.computeLineDistances(); root.add(ln); items.push({ g: G, o: ln, t0, t1, mode: "draw", n: v.length / 3 }); return ln;
  };
  const wire = (w, h, d, x, y, z, t0 = .5, t1 = .8) => { // sagoma ammessa, tratteggiata
    const geo = new THREE.EdgesGeometry(new THREE.BoxGeometry(w, h, d)); geo.translate(0, h / 2, 0);
    const ln = new THREE.LineSegments(geo, M.ghost); ln.computeLineDistances(); ln.position.set(x, y, z); root.add(ln); items.push({ g: G, o: ln, t0, t1, mode: "grow", y }); return ln;
  };

  let view = { r: 34, el: .42, look: 2.2, yaw: .7 };
  // ---------- modelli ----------
  if (preset === "massa" || preset === "morph") {
    // residenza a gradoni su un pendio, come tante nel Luganese (modello di studio, non un progetto preciso)
    const m = preset === "morph";
    if (m) { outline([[-7, -4], [5, -4], [5, 4], [-7, 4]], .03, 0, .16); outline([[-4, -5], [7, -5], [7, 2.5], [-4, 2.5]], .04, .05, .2); outline([[-9, -6.5], [9, -6.5], [9, 7.5], [-9, 7.5]], .02, .08, .22); }
    const T = m ? [[.22, .38], [.36, .5], [.48, .62], [.6, .72], [.7, .8], [.78, .88]] : [[0, .3], [.15, .45], [.3, .6], [.45, .7], [.55, .8], [.65, .9]];
    box(12, 3, 8, -1, 0, 0, M.paper, ...T[0]);
    box(11, 3, 7.5, 1.5, 3, -1, M.paper, ...T[1]);
    box(7, 3, 6, 2.5, 6, -1.6, M.paper, ...T[2]);
    G = "glass"; box(11.6, 2.2, .08, -1, .4, 4.02, M.glass, ...T[3], "grow", false); box(10.6, 2.2, .08, 1.5, 3.4, 2.77, M.glass, ...T[3], "grow", false); box(6.6, 2.2, .08, 2.5, 6.4, 1.42, M.glass, ...T[3], "grow", false);
    G = "terr"; box(12.6, .22, 1.6, -1, 3, 4.6, M.paper, T[4][0], T[4][1], "drop"); box(11.4, .22, 1.4, 1.5, 6, 3.4, M.paper, T[4][0], T[4][1], "drop"); box(7.4, .25, 6.6, 2.5, 9, -1.6, M.acc, T[4][0], T[4][1], "drop");
    G = "garden"; box(6, .1, 2.4, -3, 0, 6.2, M.water, ...T[5], "grow", false); box(9, .12, 1.6, 4, 0, 6, M.wood, ...T[5]);
    [[-9, -5], [-9.5, 1], [9.5, -4], [10, 3.5], [-8, 7.5]].forEach(([x, z], i) => tree(x, z, 1 + (i % 2) * .25, (m ? .86 : .72) + i * .02));
    view = m ? { r: 36, el: .5, look: 3, yaw: .9 } : { r: 34, el: .38, look: 3.6, yaw: .7 };
  } else if (preset === "residenziale") {
    box(10, 3, 6, -1, 0, 0, M.paper, 0, .35); box(5, 3, 8, 5.5, 0, 1, M.paper, .15, .5); box(8, 3, 5.6, 0, 3, -.2, M.paper, .3, .6);
    box(8.8, .22, 6.6, 0, 6, -.2, M.acc, .55, .75, "drop"); box(9.6, 2.2, .08, -1, .4, 3.02, M.glass, .5, .75, "grow", false); box(7.6, 2.2, .08, 0, 3.4, 2.62, M.glass, .55, .8, "grow", false);
    box(7, .1, 3, -2, 0, 6, M.water, .7, .9, "grow", false); box(11, .12, 2, 1, 0, 3.8, M.wood, .7, .9);
    [[-8, -3], [-8.5, 3], [9.5, -3], [9, 6]].forEach(([x, z], i) => tree(x, z, 1, .75 + i * .04)); view = { r: 30, el: .4, look: 2.6, yaw: .8 };
  } else if (preset === "licenze") {
    outline([[-9, -7], [9, -7], [9, 7], [-9, 7]], .03, 0, .3); outline([[-6, -4], [6, -4], [6, 4], [-6, 4]], .04, .1, .35, M.ghost);
    wire(12, 9.5, 8, 0, 0, 0, .3, .55);
    box(11, 3, 7, 0, 0, 0, M.paper, .45, .7); box(9, 3, 6.5, .5, 3, -.25, M.paper, .55, .8); box(9.4, .22, 6.9, .5, 6, -.25, M.acc, .7, .9, "drop");
    view = { r: 32, el: .5, look: 3, yaw: .6 };
  } else if (preset === "direzione") {
    box(12, .3, 8, 0, 0, 0, M.paper, 0, .2); for (let x = -5.5; x <= 5.5; x += 3.66) for (const z of [-3.6, 3.6]) box(.35, 3, .35, x, .3, z, M.paper, .1, .4);
    box(12, .3, 8, 0, 3.3, 0, M.paper, .35, .5, "drop"); box(11.6, 3, 7.6, 0, .3, 0, M.old, .45, .65); for (let x = -5.5; x <= 5.5; x += 3.66) for (const z of [-3.6, 3.6]) box(.35, 3, .35, x, 3.6, z, M.paper, .55, .75);
    box(12, .3, 8, 0, 6.6, 0, M.acc, .7, .85, "drop");
    box(.5, 16, .5, 9, 0, -5, M.acc, .2, .5); box(14, .4, .4, 5, 16, -5, M.acc, .5, .7, "drop");
    view = { r: 34, el: .38, look: 4, yaw: .7 };
  } else if (preset === "perizie") {
    box(10, 3, 7, 0, 0, 0, M.old, 0, .4); box(10, 3, 7, 0, 3, 0, M.old, .1, .5); box(10, 3, 7, 0, 6, 0, M.old, .2, .6);
    roof(10.6, 2.6, 7.4, 0, 9, 0, M.old, .4, .7);
    for (const y of [3, 6]) box(9.8, .25, 6.8, .02, y - .12, 0, M.paper, .5, .8, "grow");
    const pl = new THREE.Mesh(new THREE.PlaneGeometry(9, 13), new THREE.MeshBasicMaterial({ color: acc, transparent: true, opacity: .18, side: THREE.DoubleSide, depthWrite: false }));
    pl.rotation.y = Math.PI / 2; pl.position.set(.4, 6, 0); root.add(pl); items.push({ g: G, o: pl, t0: .6, t1: .9, mode: "pop", y: 6 });
    view = { r: 34, el: .3, look: 5, yaw: 1.1 };
  } else if (preset === "ristrutturazioni") {
    box(8, 3, 7, -2, 0, 0, M.old, 0, .3); box(8, 3, 7, -2, 3, 0, M.old, .1, .4); roof(8.6, 2.6, 7.4, -2, 6, 0, M.old, .3, .55);
    box(5, 3, 6, 4.6, 0, .4, M.acc, .55, .8); box(4.8, 2.2, .08, 4.6, .4, 3.42, M.glass, .7, .9, "grow", false); box(5.4, .2, 6.4, 4.6, 3, .4, M.paper, .75, .95, "drop");
    [[-8.5, -3], [9, -3], [9.5, 4]].forEach(([x, z], i) => tree(x, z, 1, .8 + i * .04)); view = { r: 30, el: .36, look: 3, yaw: .6 };
  } else { // interni: stanza in spaccato
    box(12, .2, 9, 0, 0, 0, M.wood, 0, .3); box(12, 3.2, .2, 0, .2, -4.4, M.paper, .1, .4); box(.2, 3.2, 9, -5.9, .2, 0, M.paper, .15, .45);
    box(.22, 2.2, 3, -5.9, .7, 1, M.glass, .4, .6, "grow", false);
    box(4, .8, 1.6, -2.5, .2, -2.8, M.old, .45, .65); box(1.6, .8, 1.6, -4.6, .2, -.6, M.old, .5, .7); box(2.6, .1, 1.4, -2, .55, -.4, M.acc, .55, .75);
    box(4.5, .95, 1.4, 3, .2, -3.5, M.paper, .55, .75); box(3.2, .95, 1.2, 3.2, .2, 0, M.paper, .6, .8); box(3.6, .1, 1.6, 3.2, 1.15, 0, M.acc, .7, .85);
    box(3.6, 1.4, .12, -3, 1.7, -4.25, M.old, .7, .9); tree(-4.6, 3, .55, .8);
    view = { r: 22, el: .62, look: 0, yaw: .75 };
  }
  root.position.y = 0;

  // ---------- stato e disegno ----------
  const clamp = (v) => Math.max(0, Math.min(1, v)), ease = (k) => 1 - Math.pow(1 - k, 3);
  function apply(p) {
    for (const it of items) {
      const k = ease(clamp((p - it.t0) / Math.max(.001, it.t1 - it.t0))), o = it.o; o.visible = k > .002 && !off.has(it.g); if (!o.visible) continue;
      if (it.mode === "grow") o.scale.set(1, Math.max(.002, k), 1);
      else if (it.mode === "drop") o.position.y = it.y + (1 - k) * 6;
      else if (it.mode === "pop") o.scale.setScalar(Math.max(.002, k));
      else if (it.mode === "draw") o.geometry.setDrawRange(0, Math.max(2, Math.round(it.n * k / 2) * 2));
    }
  }
  let lastAuto = 0, yaw = view.yaw, pitch = view.el, w = 0, h = 0, p = 0, target = preset === "morph" ? 0 : 1, last = 0, idleT = 0, visible = false, raf = 0, drag = null, dirty = true;
  const morph = preset === "morph", stopped = { v: false }, sec = morph ? el.closest("[data-morph]") : null;
  function size() { const r = el.getBoundingClientRect(); if (Math.abs(r.width - w) < 1 && Math.abs(r.height - h) < 1) return; w = r.width; h = r.height; R.setSize(w, h, false); cam.aspect = w / Math.max(1, h); cam.updateProjectionMatrix(); dirty = true; }
  function readScroll() { if (!sec) return; const r = sec.getBoundingClientRect(); target = clamp((innerHeight * .55 - r.top) / Math.max(1, r.height - innerHeight * .3)); }
  function frame(t) {
    raf = 0; if (!visible) return; const dt = Math.min(64, t - (last || t)); last = t; size();
    if (Math.abs(target - p) > .0005) { p += (target - p) * (morph ? .12 : Math.min(1, dt / 900)); if (Math.abs(target - p) < .0005) p = target; apply(p); dirty = true; }
    const still = t - scrolling > 600; if (!lastAuto) lastAuto = t;
    if (!morph && !drag && still && !calm) { idleT += dt; if (idleT > 1800 && t - lastAuto > (small ? 40 : 32)) { yaw += (t - lastAuto) * .00018; lastAuto = t; dirty = true; } } else lastAuto = t;
    const yy = morph ? view.yaw + p * .9 : yaw;
    if (dirty) {
      const r = view.r * (small ? 1.2 : 1);
      cam.position.set(Math.sin(yy) * Math.cos(pitch) * r, Math.sin(pitch) * r, Math.cos(yy) * Math.cos(pitch) * r); cam.lookAt(0, view.look, 0);
      R.render(scene, cam); dirty = false;
    }
    if ((!morph && !calm) || Math.abs(target - p) > .0005) raf = requestAnimationFrame(frame);
  }
  const kick = () => { if (!raf && visible) raf = requestAnimationFrame(frame); };
  const io = new IntersectionObserver((es) => { visible = es[0].isIntersecting && !stopped.v; if (visible) { last = 0; readScroll(); kick(); } }, { rootMargin: "100px" }); io.observe(el);
  addEventListener("resize", () => { w = 0; kick(); });
  if (morph) addEventListener("scroll", () => { readScroll(); kick(); }, { passive: true });
  else {
    // trascina per ruotare (in orizzontale; in verticale la pagina continua a scorrere sul telefono)
    el.addEventListener("pointerdown", (e) => { drag = { x: e.clientX, y: e.clientY, yaw, pitch }; el.classList.add("grab"); idleT = 0; });
    addEventListener("pointermove", (e) => { if (!drag) return; yaw = drag.yaw - (e.clientX - drag.x) * .008; pitch = Math.max(.12, Math.min(1.2, drag.pitch + (e.clientY - drag.y) * .004)); dirty = true; kick(); });
    addEventListener("pointerup", () => { if (drag) { drag = null; idleT = 0; el.classList.remove("grab"); } });
    el.addEventListener("keydown", (e) => { const k = { ArrowLeft: -.15, ArrowRight: .15 }[e.key]; if (k) { yaw += k; idleT = 0; dirty = true; kick(); e.preventDefault(); } });
    p = calm ? 1 : 0; apply(p);
    // comandi accanto al modello: mostra/nascondi parti e avanzamento della costruzione
    const wrap = el.parentElement, ctl = wrap && wrap.querySelector(".ctl");
    if (ctl) {
      wrap.classList.add("on3d");
      ctl.querySelectorAll("[data-g]").forEach((b) => b.addEventListener("click", () => {
        const on = b.getAttribute("aria-pressed") !== "true"; b.setAttribute("aria-pressed", on); on ? off.delete(b.dataset.g) : off.add(b.dataset.g);
        apply(p); dirty = true; idleT = 0; kick(); }));
      const rg = ctl.querySelector("[data-p]"), out = ctl.querySelector("output");
      if (rg) rg.addEventListener("input", () => { target = rg.value / 100; if (out) out.textContent = rg.value + "%"; idleT = 0; kick(); });
    }
  }
  if (morph) { readScroll(); p = target; apply(p); }
  size(); dirty = true;
  const gb = el.querySelector(".g3d"); if (gb) gb.textContent = "Guarda in 3D";
  inst.push({ demand, stop() { stopped.v = true; visible = false; io.disconnect(); if (raf) cancelAnimationFrame(raf); R.dispose(); R.forceContextLoss(); R.domElement.remove(); el.classList.remove("has3d"); const w = el.parentElement; if (w) w.classList.remove("on3d"); } });
  if (demand) { visible = true; kick(); }
}
