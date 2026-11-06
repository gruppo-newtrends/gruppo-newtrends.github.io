// Edil Trend: una villa ticinese che si costruisce mentre scorri le quattro fasi (three.js).
// 1 sopralluogo e tracciamento · 2 scavo, platea e struttura (con la gru) · 3 pietra, vetri, legno e tetto
// 4 piscina, giardino e luci della sera. Senza WebGL o con "riduci animazioni" resta la foto.
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const sec = document.querySelector(".proc"), box = document.querySelector(".stage3d");
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
if (sec && box && !reduce) start();

function start() {
  let R;
  const small = innerWidth < 760;
  // telefoni: niente antialias (lo schermo è già denso), pixel ratio basso, ombre e trame più piccole
  try { R = new THREE.WebGLRenderer({ antialias: !small, powerPreference: "high-performance" }); } catch (e) { return; }
  if (!R.getContext()) return;
  sec.classList.add("has3d");
  R.setPixelRatio(Math.min(small ? 1.25 : 1.5, devicePixelRatio || 1));
  R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFShadowMap; R.shadowMap.autoUpdate = true;
  R.toneMapping = THREE.ACESFilmicToneMapping; R.outputColorSpace = THREE.SRGBColorSpace;
  box.prepend(R.domElement);

  const scene = new THREE.Scene();
  const pm = new THREE.PMREMGenerator(R);
  scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
  const cam = new THREE.PerspectiveCamera(small ? 40 : 32, 1, 0.5, 400);

  // ---------- cielo: gradiente che passa dal giorno alla sera ----------
  const skyU = { top: { value: new THREE.Color() }, mid: { value: new THREE.Color() }, bot: { value: new THREE.Color() } };
  const sky = new THREE.Mesh(new THREE.SphereGeometry(180, 24, 12), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, uniforms: skyU,
    vertexShader: "varying vec3 v;void main(){v=normalize(position);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}",
    fragmentShader: "uniform vec3 top,mid,bot;varying vec3 v;void main(){float h=v.y;vec3 c=h>0.?mix(mid,top,smoothstep(0.,.55,h)):mix(mid,bot,smoothstep(0.,.25,-h));gl_FragColor=vec4(c,1.);}"
  }));
  scene.add(sky);
  scene.fog = new THREE.Fog(0xffffff, 70, 170);
  const DAY = { top: new THREE.Color("#8FA9BF"), mid: new THREE.Color("#E9DFD0"), bot: new THREE.Color("#B9AD9B") };
  const DUSK = { top: new THREE.Color("#28324A"), mid: new THREE.Color("#C99878"), bot: new THREE.Color("#2A2520") };

  const hemi = new THREE.HemisphereLight("#dfe8f0", "#6d5f4d", 0.7); scene.add(hemi);
  const sun = new THREE.DirectionalLight("#fff4e3", 2.6); sun.castShadow = true;
  sun.shadow.mapSize.set(small ? 512 : 1024, small ? 512 : 1024);
  Object.assign(sun.shadow.camera, { left: -26, right: 26, top: 26, bottom: -26, near: 1, far: 120 });
  sun.shadow.bias = -0.0003; sun.shadow.normalBias = 0.03; scene.add(sun, sun.target);

  // ---------- materiali con trame disegnate in codice ----------
  const TS = small ? 256 : 512;
  const tex = (draw, rep = 1, size = TS) => {
    const c = document.createElement("canvas"); c.width = c.height = size; const g = c.getContext("2d"); draw(g, size);
    const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep, rep);
    t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = small ? 2 : 4; return t;
  };
  const rnd = (() => { let s = 7; return () => (s = (s * 16807) % 2147483647) / 2147483647; })();
  const noise = (g, n, base, amp, a = 1) => { g.fillStyle = base; g.fillRect(0, 0, n, n); for (let i = 0; i < n * 22; i++) { const v = (rnd() - .5) * amp; g.fillStyle = `rgba(${v > 0 ? 255 : 0},${v > 0 ? 255 : 0},${v > 0 ? 255 : 0},${Math.abs(v) * a})`; g.fillRect(rnd() * n, rnd() * n, 1 + rnd() * 2, 1 + rnd() * 2); } };
  const tConcrete = tex((g, n) => { noise(g, n, "#B9B3AA", .12); g.strokeStyle = "rgba(0,0,0,.08)"; for (let y = 0; y < n; y += n / 4) { g.beginPath(); g.moveTo(0, y); g.lineTo(n, y); g.stroke(); } for (let i = 0; i < 18; i++) { g.fillStyle = "rgba(0,0,0,.12)"; g.beginPath(); g.arc(rnd() * n, rnd() * n, 2, 0, 7); g.fill(); } }, 2);
  const tRender = tex((g, n) => noise(g, n, "#EEEAE3", .05), 3);
  const tStone = tex((g, n) => {
    g.fillStyle = "#6E655B"; g.fillRect(0, 0, n, n);
    let y = 0; while (y < n) { const h = 22 + rnd() * 30; let x = -rnd() * 40; while (x < n) { const w = 40 + rnd() * 90, l = 120 + rnd() * 70;
      g.fillStyle = `rgb(${l | 0},${(l * .95) | 0},${(l * .87) | 0})`; g.fillRect(x + 2, y + 2, w - 4, h - 4);
      g.fillStyle = "rgba(255,255,255,.07)"; g.fillRect(x + 2, y + 2, w - 4, 3); x += w; } y += h; }
    for (let i = 0; i < n * 8; i++) { g.fillStyle = `rgba(0,0,0,${rnd() * .1})`; g.fillRect(rnd() * n, rnd() * n, 2, 2); }
  }, 1);
  const tWood = tex((g, n) => {
    g.fillStyle = "#8A5A3A"; g.fillRect(0, 0, n, n);
    for (let i = 0; i < 260; i++) { const y = rnd() * n; g.strokeStyle = `rgba(${rnd() > .5 ? "60,30,15" : "190,140,95"},${.15 + rnd() * .25})`; g.lineWidth = .5 + rnd() * 2; g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(n * .3, y + rnd() * 8 - 4, n * .7, y + rnd() * 8 - 4, n, y); g.stroke(); }
  }, 1);
  const tGrass = tex((g, n) => { noise(g, n, "#56663F", .5, .5); for (let i = 0; i < n * 12; i++) { g.fillStyle = `rgba(${rnd() > .5 ? "120,140,80" : "40,55,30"},.35)`; g.fillRect(rnd() * n, rnd() * n, 1, 3); } }, 14);
  const tEarth = tex((g, n) => noise(g, n, "#6B5640", .45, .6), 6);
  const tPaving = tex((g, n) => { noise(g, n, "#CFC6B8", .08); g.strokeStyle = "rgba(0,0,0,.18)"; g.lineWidth = 2; for (let i = 0; i <= n; i += n / 4) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, n); g.moveTo(0, i); g.lineTo(n, i); g.stroke(); } }, 6);
  const tTile = tex((g, n) => { g.fillStyle = "#2E6E7C"; g.fillRect(0, 0, n, n); g.strokeStyle = "rgba(255,255,255,.25)"; for (let i = 0; i <= n; i += n / 8) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, n); g.moveTo(0, i); g.lineTo(n, i); g.stroke(); } }, 3);

  const S = (o) => new THREE.MeshStandardMaterial({ roughness: .85, metalness: 0, ...o });
  const mat = {
    grass: S({ map: tGrass, color: "#ffffff" }), earth: S({ map: tEarth }), concrete: S({ map: tConcrete }),
    render: S({ map: tRender, roughness: .9 }), stone: S({ map: tStone, roughness: .95 }), paving: S({ map: tPaving, roughness: .8 }),
    wood: S({ map: tWood, roughness: .55 }), dark: S({ color: "#26231F", roughness: .45, metalness: .6 }), steel: S({ color: "#3A3733", roughness: .35, metalness: .8 }),
    glass: new THREE.MeshPhysicalMaterial({ color: "#A9BCC2", roughness: .04, metalness: .1, transparent: true, opacity: .42, envMapIntensity: 2.2, clearcoat: 1, clearcoatRoughness: .05 }),
    rail: new THREE.MeshPhysicalMaterial({ color: "#C9D6DA", roughness: .05, transparent: true, opacity: .22, envMapIntensity: 2 }),
    water: new THREE.MeshPhysicalMaterial({ color: "#3F9AAA", roughness: .03, metalness: .05, transparent: true, opacity: .9, emissive: new THREE.Color("#1C8FA3"), emissiveIntensity: 0, envMapIntensity: 2.5, clearcoat: 1 }),
    tile: S({ map: tTile, roughness: .3 }), crane: S({ color: "#E1A72E", roughness: .5, metalness: .3 }), stake: S({ color: "#C4552B", roughness: .6 }),
    leaf: S({ color: "#33472B", roughness: .95 }), leaf2: S({ color: "#7D8C62", roughness: .95 }), trunk: S({ color: "#5B4636" }),
    warm: S({ color: "#3a3026", emissive: new THREE.Color("#FFB768"), emissiveIntensity: 0, roughness: 1 }),
    sofa: S({ color: "#D9CFC0", roughness: 1 }), lamp: S({ color: "#fff", emissive: new THREE.Color("#FFC98A"), emissiveIntensity: 0 }),
    line: new THREE.MeshBasicMaterial({ color: "#F4E7CF", transparent: true, opacity: 0, depthWrite: false }),
  };

  // ---------- elementi che compaiono in base allo scorrimento ----------
  const items = [];
  const root = new THREE.Group(); scene.add(root);
  // geometria con l'origine alla base, così "cresce" dal basso
  const B = (w, h, d, m, x, y, z, t0, t1, mode = "grow", o = {}) => {
    const g = new THREE.BoxGeometry(w, h, d); g.translate(0, h / 2, 0);
    const me = new THREE.Mesh(g, m); me.position.set(x, y, z); me.castShadow = o.cast !== false; me.receiveShadow = true;
    root.add(me); items.push({ o: me, t0, t1, mode, y, x, z, out: o.out, dx: o.dx || 0, dz: o.dz || 0 }); return me;
  };
  const add = (obj, t0, t1, mode, o = {}) => { root.add(obj); items.push({ o: obj, t0, t1, mode, y: obj.position.y, x: obj.position.x, z: obj.position.z, out: o.out, dx: o.dx || 0, dz: o.dz || 0 }); return obj; };
  const uvScale = (me, sx, sy) => { const uv = me.geometry.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * sx, uv.getY(i) * sy); };

  // terreno
  const ground = new THREE.Mesh(new THREE.CircleGeometry(150, 64), mat.grass); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
  const dig = new THREE.Mesh(new THREE.PlaneGeometry(26, 20), mat.earth); dig.rotation.x = -Math.PI / 2; dig.position.set(0, .02, 1.5); dig.receiveShadow = true; add(dig, .1, .22, "pop2d", { out: [.3, .34] });

  // FASE 1 · tracciamento: perimetro e picchetti
  const P = [[-11, -7], [11, -7], [11, 10], [-11, 10]];
  const pts = []; P.forEach((p, i) => { const q = P[(i + 1) % 4]; pts.push(new THREE.Vector3(p[0], .06, p[1]), new THREE.Vector3(q[0], .06, q[1])); });
  [[-7, -4], [5, -4], [5, 4], [-7, 4]].forEach((p, i, a) => { const q = a[(i + 1) % 4]; pts.push(new THREE.Vector3(p[0], .06, p[1]), new THREE.Vector3(q[0], .06, q[1])); });
  const lines = new THREE.Group(); scene.add(lines);
  for (let i = 0; i < pts.length; i += 2) { const a = pts[i], b = pts[i + 1], len = a.distanceTo(b);
    const m = new THREE.Mesh(new THREE.PlaneGeometry(len, .14), mat.line); m.rotation.x = -Math.PI / 2; m.rotation.z = -Math.atan2(b.z - a.z, b.x - a.x);
    m.position.set((a.x + b.x) / 2, .05, (a.z + b.z) / 2); lines.add(m); }
  P.concat([[-7, -4], [5, -4], [5, 4], [-7, 4], [-6, 6], [6, 6], [-6, 9.5], [6, 9.5]]).forEach(([x, z], i) => B(.12, .9, .12, mat.stake, x, 0, z, .03 + i * .008, .08 + i * .008, "grow", { out: [.3, .36] }));

  // FASE 2 · platea, struttura, gru
  B(22, .4, 13, mat.concrete, 0, 0, -.5, .22, .3);                // platea dietro la piscina
  B(5, .4, 3.5, mat.concrete, -8.5, 0, 7.75, .24, .31); B(5, .4, 3.5, mat.concrete, 8.5, 0, 7.75, .24, .31);
  B(22, .4, .5, mat.concrete, 0, 0, 9.75, .25, .32);
  const pool = B(12, .03, 3.5, mat.tile, 0, .01, 7.75, .26, .32, "grow", { cast: false }); uvScale(pool, 1, 1);
  [[-6.9, -3.9], [-2.9, -3.9], [1.1, -3.9], [4.9, -3.9], [-6.9, 3.9], [-2.9, 3.9], [1.1, 3.9], [4.9, 3.9]].forEach(([x, z], i) => B(.3, 3.2, .3, mat.concrete, x, .4, z, .3 + i * .01, .38 + i * .01));
  B(3, 3.2, 3, mat.concrete, -1, .4, -2.4, .32, .4);                // vano scala
  B(18.4, .35, 10.6, mat.concrete, -.5, 3.6, 0, .4, .47, "drop");  // solaio del primo piano (sbalzo)
  for (let x = -3.85; x < 8; x += 4) B(.3, 3.05, .3, mat.concrete, x, 3.95, -4.35, .45, .5, "grow", { out: [.62, .66] });
  // gru a torre
  const crane = new THREE.Group(); crane.position.set(15, 0, -9);
  const cm = (w, h, d, x, y, z) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat.crane); m.position.set(x, y, z); m.castShadow = true; crane.add(m); return m; };
  for (let y = 0; y < 22; y += 1.6) { cm(.9, .08, .08, 0, y, .45); cm(.9, .08, .08, 0, y, -.45); cm(.08, .08, .9, .45, y, 0); cm(.08, .08, .9, -.45, y, 0); }
  [[.45, .45], [-.45, .45], [.45, -.45], [-.45, -.45]].forEach(([x, z]) => cm(.1, 22, .1, x, 11, z));
  const jib = new THREE.Group(); jib.position.y = 22; crane.add(jib);
  const jm = (w, h, d, x, y, z, m = mat.crane) => { const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); b.position.set(x, y, z); b.castShadow = true; jib.add(b); return b; };
  jm(24, .5, .7, -8, .25, 0); jm(7, .5, .7, 5, .25, 0); jm(2, 1.4, 1.2, 7.5, -.4, 0, mat.concrete); jm(1.4, 1.4, 1.4, 0, 1, 0, mat.dark);
  const cable = jm(.03, 10, .03, -15, -5, 0, mat.dark); const hook = jm(1.6, .25, .25, -15, -10, 0, mat.dark);
  add(crane, .2, .3, "rise", { out: [.78, .86] });

  // FASE 3 · pietra, vetri, intonaco, doghe di legno, tetto
  const back = B(12.4, 3.2, .45, mat.stone, -1, .4, -4.1, .52, .58); uvScale(back, 3, 1);
  const sideL = B(.55, 3.2, 10.5, mat.stone, -7.4, .4, 0, .5, .56); uvScale(sideL, 2.5, 1);
  // vetrate del piano terra, una alla volta
  for (let i = 0; i < 6; i++) { const x = -6.1 + i * 2 + 1; B(1.95, 3.1, .06, mat.glass, x - 1 + .02, .45, 4.05, .56 + i * .012, .6 + i * .012, "slide", { dz: 2.5, cast: false }); B(.07, 3.2, .12, mat.dark, x - 1, .4, 4.05, .56 + i * .012, .6 + i * .012); }
  B(.07, 3.2, .12, mat.dark, 4.95, .4, 4.05, .63, .66);
  for (let i = 0; i < 4; i++) B(.06, 3.1, 1.95, mat.glass, 5.05, .45, -3.9 + i * 2, .6 + i * .012, .64 + i * .012, "slide", { dx: 2.5, cast: false });
  // volume del primo piano: intonaco bianco con nastro finestrato
  const up = (w, h, d, x, y, z, t0, t1, m = mat.render) => B(w, h, d, m, x, y, z, t0, t1);
  up(12.3, 3.05, .3, 2, 3.95, -4.4, .62, .68);                    // parete nord
  up(.3, 3.05, 9, -4.1, 3.95, 0, .63, .69); up(.3, 3.05, 9, 8.1, 3.95, 0, .63, .69);
  up(12.3, .8, .3, 2, 3.95, 4.4, .64, .69); up(12.3, .55, .3, 2, 6.45, 4.4, .65, .7);
  B(12, 1.7, .05, mat.glass, 2, 4.75, 4.42, .66, .71, "slide", { dz: 2, cast: false });
  // doghe verticali in legno davanti al nastro
  for (let x = -3.7, i = 0; x < 7.8; x += .26, i++) B(.09, 3.1, .16, mat.wood, x, 3.95, 4.75, .68 + i * .0014, .7 + i * .0014, "grow");
  B(13.2, .32, 10, mat.render, 2, 7, 0, .7, .75, "drop");          // tetto
  B(13.3, .12, 10.1, mat.dark, 2, 7.32, 0, .72, .76, "drop");
  B(5.2, 1.05, .04, mat.rail, -6.5, 3.95, 5.25, .72, .75, "grow", { cast: false }); B(.04, 1.05, 10.4, mat.rail, -9.6, 3.95, 0, .72, .75, "grow", { cast: false });
  B(5.3, .07, .07, mat.steel, -6.5, 5, 5.25, .73, .75); B(.07, .07, 10.5, mat.steel, -9.6, 5, 0, .73, .75);
  // interni caldi dietro i vetri (si accendono alla fine)
  B(11.6, 2.9, .05, mat.warm, -1, .5, -3.8, .6, .62, "grow", { cast: false }); B(11.6, 2.6, .05, mat.warm, 2, 4.05, -4.2, .66, .68, "grow", { cast: false });
  B(3.6, .55, 1.1, mat.sofa, -3.5, .4, -1.2, .78, .82, "pop"); B(1.3, .45, 1.1, mat.sofa, -5.9, .4, .2, .79, .83, "pop"); B(2.8, .08, 1.2, mat.wood, 1.8, 1.15, 0, .8, .84, "pop");
  [-3.8, -1, 1.8].forEach((x, i) => { const l = new THREE.Mesh(new THREE.SphereGeometry(.22, 16, 12), mat.lamp); l.position.set(x, 2.9, -.5); add(l, .82 + i * .01, .86 + i * .01, "pop"); });

  // FASE 4 · piscina, terrazza, giardino, luci
  const water = B(11.9, .34, 3.4, mat.water, 0, .03, 7.75, .8, .88, "grow", { cast: false });
  B(5, .08, 9, mat.wood, 8.5, .4, 4.5, .82, .87, "grow"); B(9, .06, 2, mat.paving, -1, .4, 5.2, .82, .86, "grow", { cast: false });
  [[7.6, 7], [9.4, 7]].forEach(([x, z], i) => { B(.8, .3, 2, mat.sofa, x, .48, z, .86 + i * .01, .9 + i * .01, "pop"); });
  // alberi: cipressi e ulivi tondi, come nei giardini ticinesi
  const bumpy = (r, det) => { const g = new THREE.IcosahedronGeometry(r, det), p = g.attributes.position, v = new THREE.Vector3();
    for (let i = 0; i < p.count; i++) { v.fromBufferAttribute(p, i); const n = 1 + (Math.sin(v.x * 3.1) * Math.cos(v.y * 2.7) * Math.sin(v.z * 3.3)) * .09 + (rnd() - .5) * .05; p.setXYZ(i, v.x * n, v.y * n, v.z * n); }
    g.computeVertexNormals(); return g; };
  const cypress = (x, z, s, t) => { const g = new THREE.Group(); g.position.set(x, 0, z);
    const c = new THREE.Mesh(bumpy(1, 3), mat.leaf); c.scale.set(.75 * s, 3.4 * s, .75 * s); c.position.y = 3.2 * s; c.castShadow = true; g.add(c);
    const tr = new THREE.Mesh(new THREE.CylinderGeometry(.1 * s, .14 * s, 1, 8), mat.trunk); tr.position.y = .4; g.add(tr); add(g, t, t + .07, "pop"); };
  const olive = (x, z, s, t) => { const g = new THREE.Group(); g.position.set(x, 0, z);
    const tr = new THREE.Mesh(new THREE.CylinderGeometry(.12 * s, .22 * s, 2.4 * s, 8), mat.trunk); tr.position.y = 1.2 * s; tr.rotation.z = .12; tr.castShadow = true; g.add(tr);
    for (let i = 0; i < 4; i++) { const c = new THREE.Mesh(bumpy((.9 + rnd() * .5) * s, 3), mat.leaf2); c.scale.y = .75; c.position.set((rnd() - .5) * 1.8 * s, (2.6 + rnd() * .8) * s, (rnd() - .5) * 1.8 * s); c.castShadow = true; g.add(c); }
    add(g, t, t + .07, "pop"); };
  const tree = (x, z, s, t) => (s > 1.1 ? cypress : olive)(x, z, s, t);
  [[-13, -6], [-13, -2.5], [-13, 1], [-4, -11.5], [0, -11.5], [4, -11.5]].forEach(([x, z], i) => cypress(x, z, 1.25, .84 + i * .008));
  olive(-13.5, 7, 1.1, .86); olive(14, 4, 1.2, .87); olive(16, 11, .9, .9); olive(-17, 12, 1, .9);
  for (let x = -10; x <= 10; x += 2.5) B(2.3, .9, .9, mat.leaf, x, 0, -8.5, .86 + (x + 10) * .002, .9 + (x + 10) * .002, "grow");
  const lamps = [];
  [[-10.5, 10.6], [-5, 10.6], [5, 10.6], [10.5, 10.6], [11.5, 1], [-11.5, 1]].forEach(([x, z], i) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(.08, .08, .6, 8), mat.lamp); m.position.set(x, .3, z); add(m, .9 + i * .008, .93 + i * .008, "pop"); });
  const inLights = [[-3, 2.3, -1.5], [2.5, 2.3, -1], [2, 5.8, 0], [0, .1, 7.75]].map(([x, y, z], i) => { const l = new THREE.PointLight(i === 3 ? "#58D4E8" : "#FFB46A", 0, i === 3 ? 12 : 14, 1.6); l.position.set(x, y, z); scene.add(l); lamps.push(l); return l; });

  // ---------- scorrimento ----------
  const capEl = box.querySelector(".cap3d"), barEl = box.querySelector(".bar i");
  const NAMES = ["Sopralluogo e tracciamento", "Scavo, platea e struttura", "Pietra, vetrate e tetto", "Piscina, giardino e luci"];
  let target = 0, cur = -1, visible = false, raf = 0, w = 0, h = 0;
  const clamp = (v) => Math.max(0, Math.min(1, v)), ease = (k) => 1 - Math.pow(1 - k, 3), lerp = (a, b, k) => a + (b - a) * k;
  const readScroll = () => { const r = sec.getBoundingClientRect(); target = clamp(-r.top / Math.max(1, r.height - innerHeight)); };

  function apply(p) {
    for (const it of items) {
      let k = ease(clamp((p - it.t0) / (it.t1 - it.t0)));
      if (it.out) k *= 1 - ease(clamp((p - it.out[0]) / (it.out[1] - it.out[0])));
      const o = it.o; o.visible = k > .001; if (!o.visible) continue;
      if (it.mode === "grow") o.scale.set(1, Math.max(.001, k), 1);
      else if (it.mode === "drop") o.position.y = it.y + (1 - k) * 7;
      else if (it.mode === "slide") { o.position.x = it.x + (1 - k) * it.dx; o.position.z = it.z + (1 - k) * it.dz; o.scale.set(1, k < 1 ? .999 : 1, 1); }
      else if (it.mode === "rise") o.position.y = it.y - (1 - k) * 24;
      else if (it.mode === "pop") o.scale.setScalar(Math.max(.001, k));
      else if (it.mode === "pop2d") o.scale.set(Math.max(.001, k), Math.max(.001, k), 1);
    }
    mat.line.opacity = clamp(p / .05) * (1 - clamp((p - .26) / .06));
    jib.rotation.y = -.9 + p * 2.4; hook.position.y = -10 + Math.sin(p * 30) * 2; cable.scale.y = 1; cable.position.y = hook.position.y / 2;
    const d = clamp((p - .76) / .22), e = ease(d);
    skyU.top.value.copy(DAY.top).lerp(DUSK.top, e); skyU.mid.value.copy(DAY.mid).lerp(DUSK.mid, e); skyU.bot.value.copy(DAY.bot).lerp(DUSK.bot, e);
    scene.fog.color.copy(skyU.mid.value);
    sun.color.set("#fff4e3").lerp(new THREE.Color("#FF9A5A"), e); sun.intensity = lerp(2.6, 1.1, e);
    sun.position.set(lerp(-20, -30, e), lerp(30, 9, e), lerp(18, 22, e)); hemi.intensity = lerp(.7, .28, e);
    R.toneMappingExposure = lerp(1, .95, e);
    mat.warm.emissiveIntensity = e * 2.2; mat.lamp.emissiveIntensity = e * 4; mat.water.emissiveIntensity = e * .9;
    lamps.forEach((l, i) => l.intensity = e * (i === 3 ? 40 : 30));
    // camera: giro lento attorno al cantiere e avvicinamento
    const a = lerp(.95, .28, ease(p)), rad = lerp(small ? 48 : 40, small ? 42 : 33, ease(p)), el = lerp(15, 7.5, ease(p));
    cam.position.set(Math.sin(a) * rad, el, Math.cos(a) * rad); cam.lookAt(0, lerp(1.5, 3.2, p), 1);
    const i = Math.min(3, Math.floor(p * 4)); if (capEl) capEl.textContent = `${NAMES[i]} · ${Math.round(p * 100)}%`; if (barEl) barEl.style.width = (p * 100) + "%";
  }
  function size() { const r = box.getBoundingClientRect(); if (r.width === w && r.height === h) return; w = r.width; h = r.height; R.setSize(w, h, false); cam.aspect = w / h; cam.updateProjectionMatrix(); cur = -1; }
  function frame() {
    raf = 0; if (!visible) return; size();
    const nx = cur < 0 ? target : cur + (target - cur) * .12;
    if (Math.abs(nx - cur) > .0004 || cur < 0) { cur = Math.abs(nx - target) < .0004 ? target : nx; apply(cur); R.render(scene, cam); }
    if (cur !== target) raf = requestAnimationFrame(frame);
  }
  const kick = () => { readScroll(); if (!raf) raf = requestAnimationFrame(frame); };
  new IntersectionObserver((es) => { visible = es[0].isIntersecting; if (visible) kick(); }, { rootMargin: "200px" }).observe(box);
  addEventListener("scroll", kick, { passive: true }); addEventListener("resize", () => { w = 0; kick(); });
  readScroll(); size(); apply(target); R.render(scene, cam);
}
