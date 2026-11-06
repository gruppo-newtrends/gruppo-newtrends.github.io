// Edil Trend: una casa che si costruisce mentre scorri le cinque fasi (three.js).
// Fase 1 picchetti · 2 platea · 3 struttura · 4 muri, tetto e vetri · 5 finiture, giardino e luci.
// Se WebGL non c'è o l'utente ha chiesto meno animazioni, resta la versione con le foto.
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";

const sec = document.querySelector(".build"), box = document.querySelector(".frame3d");
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
if (sec && box && !reduce) start();

function start() {
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false }); } catch (e) { return; }
  if (!renderer.getContext()) return;
  sec.classList.add("has3d");
  renderer.setPixelRatio(Math.min(2, devicePixelRatio || 1));
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05; renderer.outputColorSpace = THREE.SRGBColorSpace;
  box.prepend(renderer.domElement);
  const BG = new THREE.Color(box.dataset.bg || "#EDE7DE");
  const scene = new THREE.Scene(); scene.background = BG; scene.fog = new THREE.Fog(BG, 46, 95);
  const cam = new THREE.PerspectiveCamera(30, 1, 0.1, 200);
  scene.add(new THREE.HemisphereLight("#ffffff", box.dataset.bg ? "#6b5f52" : "#cdbba5", box.dataset.bg ? 1.15 : 0.95));
  const sun = new THREE.DirectionalLight("#fff3e2", 1.7); sun.position.set(16, 26, 12); sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -22, right: 22, top: 22, bottom: -22, near: 1, far: 80 }); sun.shadow.bias = -0.0004; scene.add(sun);

  const M = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.85, metalness: 0, ...o });
  const mat = { ground: M(box.dataset.ground || "#E4DACB"), lot: M(box.dataset.lot || "#EFE8DD"), concrete: M("#CFC8BE"), white: M("#F6F3EE", { roughness: 0.7 }), wood: M("#B08362", { roughness: 0.6 }),
    dark: M("#5A534C", { roughness: 0.5, metalness: 0.3 }), glass: M("#BFD3DA", { roughness: 0.05, metalness: 0.2, transparent: true, opacity: 0.38 }),
    green: M("#8E9C7A"), green2: M("#76866A"), trunk: M("#7B6250"), stake: M("#8C4A2F"), water: M("#9FC3CC", { roughness: 0.15, transparent: true, opacity: 0.85 }),
    warm: new THREE.MeshStandardMaterial({ color: "#E9E1D4", emissive: new THREE.Color("#ffcf8a"), emissiveIntensity: 0, roughness: 0.9 }) };

  const ground = new THREE.Mesh(new THREE.PlaneGeometry(140, 140), mat.ground); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
  const lot = new THREE.Mesh(new THREE.PlaneGeometry(26, 19), mat.lot); lot.rotation.x = -Math.PI / 2; lot.position.y = 0.01; lot.receiveShadow = true; scene.add(lot);

  const parts = [];
  // a mesh whose origin is at its base, so it can "grow" from the ground
  function block(w, h, d, x, y, z, m, a, b, mode = "grow") {
    const g = new THREE.BoxGeometry(w, h, d); g.translate(0, h / 2, 0);
    const mm = m.clone(); const mesh = new THREE.Mesh(g, mm); mesh.position.set(x, y, z); mesh.castShadow = true; mesh.receiveShadow = true;
    scene.add(mesh); parts.push({ mesh, a, b, mode, y0: y, op: mm.opacity ?? 1 }); return mesh;
  }
  const stagger = (i, n, a, b) => [a + (b - a) * (i / n) * 0.6, a + (b - a) * (i / n) * 0.6 + (b - a) * 0.4];

  // 1 · picchetti e tracciamento
  [[-7, -4.5], [7, -4.5], [-7, 4.5], [7, 4.5]].forEach(([x, z], i) => { const [a, b] = stagger(i, 4, 0.02, 0.14); const s = block(0.12, 1.1, 0.12, x, 0, z, mat.stake, a, b, "drop"); s.userData.out = [0.34, 0.42]; });
  // 2 · scavo e platea
  block(14.6, 0.5, 9.6, 0, 0, 0, mat.concrete, 0.16, 0.3);
  // 3 · struttura: pilastri, solai
  const colsG = []; for (const x of [-7, -2.4, 2.4, 7]) for (const z of [-4.5, 4.5]) colsG.push([x, z]);
  colsG.forEach(([x, z], i) => { const [a, b] = stagger(i, colsG.length, 0.32, 0.42); block(0.32, 3, 0.32, x, 0.5, z, mat.concrete, a, b); });
  block(15, 0.32, 10, 0, 3.5, 0, mat.concrete, 0.41, 0.46, "drop");
  const colsU = []; for (const x of [-7, -2.4, 2.4]) for (const z of [-4.5, 4.5]) colsU.push([x, z]);
  colsU.forEach(([x, z], i) => { const [a, b] = stagger(i, colsU.length, 0.46, 0.54); block(0.3, 2.9, 0.3, x, 3.82, z, mat.concrete, a, b); });
  block(10.6, 0.3, 10.2, -2.2, 6.72, 0, mat.concrete, 0.53, 0.58, "drop");
  // 4 · muri, tetto e vetri
  const W = [[14.6, 3, 0.25, 0, 0.5, -4.6], [0.25, 3, 9.2, -7.2, 0.5, 0], [0.25, 3, 9.2, 7.2, 0.5, 0], [3.2, 3, 0.25, -5.6, 0.5, 4.6], [2.2, 3, 0.25, 6.1, 0.5, 4.6],
             [10.4, 2.9, 0.25, -2.2, 3.82, -4.6], [0.25, 2.9, 9.2, -7.2, 3.82, 0], [0.25, 2.9, 9.2, 2.8, 3.82, 0]];
  W.forEach((w, i) => { const [a, b] = stagger(i, W.length, 0.58, 0.7); block(...w, mat.white, a, b); });
  block(11.4, 0.45, 11, -2.2, 7.02, 0.3, mat.white, 0.7, 0.75, "drop");              // tetto con sporto
  block(15.4, 0.25, 0.9, 0, 3.5, 5.0, mat.white, 0.7, 0.75, "drop");                 // pensilina piano terra
  block(9.6, 2.9, 0.06, -0.8, 0.5, 4.62, mat.glass, 0.72, 0.8, "fade");               // vetrate piano terra
  block(6.6, 2.7, 0.06, -3.6, 3.9, 4.62, mat.glass, 0.74, 0.82, "fade");              // vetrate primo piano
  const glow1 = block(9.4, 2.7, 0.05, -0.8, 0.6, 4.3, mat.warm, 0.78, 1, "glow");      // luci interne
  const glow2 = block(6.4, 2.5, 0.05, -3.6, 4.0, 4.3, mat.warm, 0.8, 1, "glow");
  // 5 · finiture: legno, ringhiere, terrazza, giardino
  block(3.6, 2.9, 0.18, 1.0, 3.82, 4.72, mat.wood, 0.78, 0.85);                       // rivestimento in legno
  block(0.18, 2.9, 4.6, 2.95, 3.82, 2.3, mat.wood, 0.79, 0.86);
  block(4.3, 1.0, 0.05, 5.0, 3.82, 4.85, mat.glass, 0.8, 0.86, "fade");               // parapetto terrazza
  block(4.6, 0.12, 9.4, 5.0, 3.68, 0, mat.wood, 0.78, 0.84, "drop");                  // terrazza
  for (let i = 0; i < 8; i++) block(0.04, 2.9, 0.04, -7.1 + i * 1.35, 0.5, 4.75, mat.dark, 0.76 + i * 0.004, 0.8 + i * 0.004);  // montanti
  block(6, 0.05, 3.2, 5.5, 0.02, 8.6, mat.water, 0.84, 0.9, "fade");                  // piscina
  block(15, 0.06, 2.2, 0, 0.02, 6.2, mat.lot.clone(), 0.83, 0.88, "fade");            // marciapiede
  const trees = [[-11, 7, 1.3], [-11.5, -3, 1.6], [11.5, -4, 1.4], [12, 6.5, 1.1], [-4, 9.5, 1.0]];
  trees.forEach(([x, z, s], i) => {
    const [a, b] = stagger(i, trees.length, 0.86, 0.97);
    block(0.22 * s, 1.6 * s, 0.22 * s, x, 0, z, mat.trunk, a, b);
    const g = new THREE.SphereGeometry(1.25 * s, 18, 14); g.translate(0, 1.25 * s, 0);
    const crown = new THREE.Mesh(g, (i % 2 ? mat.green : mat.green2).clone()); crown.position.set(x, 1.4 * s, z); crown.castShadow = true; scene.add(crown); parts.push({ mesh: crown, a: a + 0.02, b: b + 0.02, mode: "grow", y0: 1.4 * s, op: 1 });
  });
  for (let i = 0; i < 6; i++) block(2.2, 0.8, 0.7, -9 + i * 3.6, 0, -8.4, mat.green2, 0.88 + i * 0.01, 0.94 + i * 0.01);   // siepe

  const ease = t => 1 - Math.pow(1 - t, 3);
  function apply(p) {
    for (const o of parts) {
      const t = Math.min(1, Math.max(0, (p - o.a) / (o.b - o.a))), e = ease(t), m = o.mesh;
      m.visible = t > 0;
      if (o.mode === "grow") m.scale.y = Math.max(0.001, e);
      if (o.mode === "drop") { m.position.y = o.y0 + (1 - e) * 3.2; m.material.transparent = e < 1 || o.op < 1; m.material.opacity = o.op * e; }
      if (o.mode === "fade") { m.material.transparent = true; m.material.opacity = o.op * e; }
      if (o.mode === "glow") { const g = Math.min(1, Math.max(0, (p - 0.9) / 0.1)); m.material.emissiveIntensity = ease(g) * 1.3; }
      if (m.userData.out) { const [a, b] = m.userData.out; const k = Math.min(1, Math.max(0, (p - a) / (b - a))); if (k > 0) { m.material.transparent = true; m.material.opacity = 1 - k; m.visible = k < 1 && t > 0; } }
    }
    const ang = -0.85 + p * 1.15, r = 50 - p * 8, h = 19 - p * 5;
    cam.position.set(Math.sin(ang) * r, h, Math.cos(ang) * r); cam.lookAt(0, 2.4 + p * 0.8, 0.5);
  }
  function size() { const w = box.clientWidth, h = box.clientHeight; renderer.setSize(w, h, false); cam.aspect = w / h; cam.updateProjectionMatrix(); }
  new ResizeObserver(() => { size(); draw(); }).observe(box); size();

  const label = box.querySelector(".cap3d"), barI = box.querySelector(".bar i");
  const names = ["Tracciamento sul terreno", "Scavo e platea", "Struttura in cemento armato", "Muri, tetto e serramenti", "Finiture, giardino e consegna"];
  let target = 0, cur = -1, raf = 0;
  const stepsEl = [...sec.querySelectorAll(".stepb")];
  function progress() {
    const start = innerHeight * 0.82; let sum = 0;     // a phase starts when its text enters the lower part of the screen
    for (const el of stepsEl) { const r = el.getBoundingClientRect(); sum += Math.min(1, Math.max(0, (start - r.top) / Math.max(1, r.height * 0.9))); }
    return stepsEl.length ? sum / stepsEl.length : 0;
  }
  function draw() { apply(Math.max(0, cur)); renderer.render(scene, cam); }
  function tick() {
    raf = 0; cur = cur < 0 ? target : cur + (target - cur) * 0.12;
    draw();
    const ph = Math.min(4, Math.floor(cur * 5 - 0.0001 < 0 ? 0 : cur * 5));
    if (label) label.textContent = names[ph] + " · " + Math.round(cur * 100) + "%";
    if (barI) barI.style.width = Math.round(cur * 100) + "%";
    if (Math.abs(target - cur) > 0.0008) raf = requestAnimationFrame(tick);
  }
  function onScroll() { target = progress(); if (!raf) raf = requestAnimationFrame(tick); }
  addEventListener("scroll", onScroll, { passive: true }); addEventListener("resize", onScroll); onScroll();
  window.__casa3d = { progress: () => cur, set: p => { target = p; cur = p; draw(); } };
}
