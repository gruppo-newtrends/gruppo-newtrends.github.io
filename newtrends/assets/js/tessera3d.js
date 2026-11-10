// Tessera Gold in 3D (three.js r160, servito dal sito). Caricato solo sulla pagina Community Gold, solo quando la tessera è visibile.
// Senza WebGL o con «riduci animazioni» resta la tessera 2D. Trascina per girarla, tocca per voltarla, inclina il telefono (se il browser lo permette).
import * as THREE from './three.module.min.js';

const host = document.querySelector('[data-tessera3d]');
if (host) init(host);

function roundRect(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }

function loadImg(src) { return new Promise(res => { const i = new Image(); i.onload = () => res(i); i.onerror = () => res(null); i.src = src; }); }

async function faces(d) {
  const W = 1024, H = Math.round(1024 / 1.586), R = 46;
  const logo = await loadImg(d.logo);
  const serif = getComputedStyle(document.documentElement).getPropertyValue('--f-display') || 'Georgia, serif';
  const sans = getComputedStyle(document.body).fontFamily || 'Arial, sans-serif';
  const mk = draw => { const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d'); g.save(); roundRect(g, 0, 0, W, H, R); g.clip(); draw(g); g.restore(); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; };
  const front = mk(g => {
    const gr = g.createLinearGradient(0, 0, W, H); gr.addColorStop(0, '#22396C'); gr.addColorStop(.55, '#0C1D44'); gr.addColorStop(1, '#07112A'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
    const rg = g.createRadialGradient(W * .85, H * .1, 10, W * .85, H * .1, W * .6); rg.addColorStop(0, '#9DBEF233'); rg.addColorStop(1, '#9DBEF200'); g.fillStyle = rg; g.fillRect(0, 0, W, H);
    g.strokeStyle = '#E6CF9F55'; g.lineWidth = 3; roundRect(g, 22, 22, W - 44, H - 44, R - 18); g.stroke();
    if (logo) { const lw = W * .42; g.drawImage(logo, 64, 58, lw, lw * logo.height / logo.width); }
    const cg = g.createLinearGradient(W - 160, 60, W - 64, 130); cg.addColorStop(0, '#F3E7C9'); cg.addColorStop(1, '#C9AE76'); g.fillStyle = cg; roundRect(g, W - 160, 58, 96, 72, 14); g.fill();
    g.strokeStyle = '#00000030'; g.lineWidth = 2; for (const y of [82, 106]) { g.beginPath(); g.moveTo(W - 160, y); g.lineTo(W - 64, y); g.stroke(); }
    g.fillStyle = '#DCE8FF'; g.font = `500 26px ${sans}`; g.letterSpacing = '10px'; g.fillText('COMMUNITY', 64, H * .5); g.letterSpacing = '0px';
    g.fillStyle = '#E6CF9F'; g.font = `italic 400 150px ${serif}`; g.fillText('Gold', 58, H * .5 + 140);
    g.fillStyle = '#FFFFFF'; g.font = `600 34px ${sans}`; g.fillText(d.name, 64, H - 64);
    g.fillStyle = '#E6CF9F'; g.font = `500 28px ${sans}`; g.textAlign = 'right'; g.fillText('NT-G-0001', W - 64, H - 64);
  });
  const back = mk(g => {
    g.fillStyle = '#FFFFFF'; g.fillRect(0, 0, W, H);
    g.fillStyle = '#0C1830'; g.font = `600 44px ${sans}`; g.fillText(d.name, 64, 120);
    g.fillStyle = '#3D4862'; g.font = `400 30px ${sans}`; d.lines.forEach((l, k) => g.fillText(l, 64, 180 + k * 46));
    g.strokeStyle = '#CAD4E3'; g.lineWidth = 3; roundRect(g, W - 300, 70, 236, 236, 18); g.stroke();
    g.fillStyle = '#0C1D44'; const cell = 26; [[0, 0], [0, 6], [6, 0], [2, 3], [3, 2], [4, 4], [3, 5], [5, 3], [1, 4], [4, 1], [6, 6], [2, 6]].forEach(([r, c]) => g.fillRect(W - 280 + c * (cell + 3), 90 + r * (cell + 3), cell, cell));
    g.fillStyle = '#395591'; g.font = `500 24px ${sans}`; g.fillText(d.foot, 64, H - 60);
  });
  return { front, back };
}

async function init(host) {
  const rm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const test = document.createElement('canvas');
  if (rm || !(test.getContext('webgl2') || test.getContext('webgl'))) return;   // resta la tessera 2D
  const d = JSON.parse(host.dataset.tessera3d);
  const { front, back } = await faces(d);
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'low-power' });
  renderer.setPixelRatio(Math.min(2, devicePixelRatio || 1)); renderer.outputColorSpace = THREE.SRGBColorSpace;
  const canvas = renderer.domElement; canvas.className = 't3d'; canvas.setAttribute('role', 'img'); canvas.setAttribute('aria-label', d.label);
  const scene = new THREE.Scene(); const cam = new THREE.PerspectiveCamera(30, 1, .1, 50); cam.position.set(0, 0, 6.2);
  const w = 3.2, h = w / 1.586, r = .16, depth = .035;
  const shape = new THREE.Shape(); shape.moveTo(-w / 2 + r, -h / 2); shape.lineTo(w / 2 - r, -h / 2); shape.quadraticCurveTo(w / 2, -h / 2, w / 2, -h / 2 + r); shape.lineTo(w / 2, h / 2 - r);
  shape.quadraticCurveTo(w / 2, h / 2, w / 2 - r, h / 2); shape.lineTo(-w / 2 + r, h / 2); shape.quadraticCurveTo(-w / 2, h / 2, -w / 2, h / 2 - r); shape.lineTo(-w / 2, -h / 2 + r); shape.quadraticCurveTo(-w / 2, -h / 2, -w / 2 + r, -h / 2);
  const edge = new THREE.Mesh(new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: false, curveSegments: 10 }), new THREE.MeshStandardMaterial({ color: 0xC9AE76, metalness: .8, roughness: .35 }));
  edge.position.z = -depth / 2;
  const card = new THREE.Group(); card.add(edge);
  const face = (tex, z, flip) => { const g = new THREE.ShapeGeometry(shape, 10); const uv = g.attributes.uv, p = g.attributes.position;
    for (let k = 0; k < uv.count; k++) uv.setXY(k, p.getX(k) / w + .5, p.getY(k) / h + .5);   // il retro è girato di 180°: stessa mappa
    const m = new THREE.Mesh(g, new THREE.MeshPhysicalMaterial({ map: tex, roughness: .42, metalness: .05, clearcoat: .6, clearcoatRoughness: .25 })); m.position.z = z; if (flip) m.rotation.y = Math.PI; return m; };
  card.add(face(front, depth / 2 + .001, false)); card.add(face(back, -depth / 2 - .001, true));
  // riflesso che attraversa la tessera
  const sheenMat = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, uniforms: { t: { value: -1 } },
    vertexShader: 'varying vec2 v; void main(){ v = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: 'uniform float t; varying vec2 v; void main(){ float x = v.x + v.y * .45 - t; float a = smoothstep(.0,.09,x) * (1.0 - smoothstep(.09,.2,x)); gl_FragColor = vec4(vec3(1.0,.96,.86), a * .32); }' });
  const sg = new THREE.ShapeGeometry(shape, 10); { const uv = sg.attributes.uv, p = sg.attributes.position; for (let k = 0; k < uv.count; k++) uv.setXY(k, p.getX(k) / w + .5, p.getY(k) / h + .5); }
  const sheen = new THREE.Mesh(sg, sheenMat); sheen.position.z = depth / 2 + .004; card.add(sheen);
  scene.add(card);
  scene.add(new THREE.HemisphereLight(0xDCE8FF, 0x0C1D44, 1.5));
  const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(2.5, 3, 4); scene.add(key);
  const rim = new THREE.DirectionalLight(0x9DBEF2, .8); rim.position.set(-3, -1, 2); scene.add(rim);

  // al posto della tessera 2D (resta nel codice per chi non vede il 3D)
  const flat = host.querySelector('.tessera'); host.classList.add('is3d'); host.prepend(canvas); if (flat) flat.setAttribute('aria-hidden', 'true');
  function size() { const W = host.clientWidth; const H = Math.round(W / 1.25); renderer.setSize(W, H, false); canvas.style.width = W + 'px'; canvas.style.height = H + 'px'; cam.aspect = W / H; cam.updateProjectionMatrix(); }
  size(); addEventListener('resize', size);

  let ry = -.35, rx = .12, vy = 0, vx = 0, target = 0, drag = null, moved = 0, tiltX = 0, tiltY = 0, visible = true, last = performance.now(), t0 = last;
  canvas.addEventListener('pointerdown', e => { drag = { x: e.clientX, y: e.clientY }; moved = 0; canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener('pointermove', e => { if (!drag) return; const dx = e.clientX - drag.x, dy = e.clientY - drag.y; drag = { x: e.clientX, y: e.clientY }; moved += Math.abs(dx) + Math.abs(dy); vy = dx * .012; vx = dy * .006; ry += vy; rx = Math.max(-.5, Math.min(.5, rx + vx)); });
  canvas.addEventListener('pointerup', () => { if (moved < 6) target += Math.PI; else target = Math.round((ry) / Math.PI) * Math.PI; drag = null; });
  canvas.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); target += Math.PI; } });
  canvas.tabIndex = 0;
  addEventListener('deviceorientation', e => { if (e.gamma == null) return; tiltY = Math.max(-.35, Math.min(.35, e.gamma / 90)); tiltX = Math.max(-.25, Math.min(.25, (e.beta - 45) / 120)); }, { passive: true });
  new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible) { last = performance.now(); requestAnimationFrame(loop); } }).observe(canvas);
  function loop(now) {
    if (!visible || document.hidden) return;
    const dt = Math.min(.05, (now - last) / 1000); last = now; const tt = (now - t0) / 1000;
    if (!drag) { ry += (target + Math.sin(tt * .6) * .18 + tiltY - ry) * Math.min(1, dt * 3.2); rx += (.1 + Math.sin(tt * .45) * .05 + tiltX - rx) * Math.min(1, dt * 3); }
    card.rotation.set(rx, ry, 0); card.position.y = Math.sin(tt * .9) * .04;
    sheenMat.uniforms.t.value = ((tt * .28) % 1.6) - .3;
    renderer.render(scene, cam); requestAnimationFrame(loop);
  }
  document.addEventListener('visibilitychange', () => { if (!document.hidden && visible) { last = performance.now(); requestAnimationFrame(loop); } });
  requestAnimationFrame(loop);
}
