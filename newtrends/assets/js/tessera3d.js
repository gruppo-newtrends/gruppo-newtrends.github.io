// Tessera Gold in 3D (three.js r160, servito dal sito). Caricato solo sulla pagina Circuito Gold, solo quando la tessera è visibile.
// Senza WebGL o con «riduci animazioni» resta la tessera 2D. Trascina per girarla, tocca per voltarla, inclina il telefono (se il browser lo permette).
import * as THREE from './three.module.min.js';

const host = document.querySelector('[data-tessera3d]');   // v5: nella pagina Circuito Gold è il riquadro .cg5-stage della prima schermata
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
    g.fillStyle = '#DCE8FF'; g.font = `500 26px ${sans}`; g.letterSpacing = '10px'; g.fillText('CIRCUITO', 64, H * .5); g.letterSpacing = '0px';
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
  if (document.fonts && document.fonts.ready) await Promise.race([document.fonts.ready, new Promise(r => setTimeout(r, 1500))]);
  const { front, back } = await faces(d);
  const lite = document.documentElement.classList.contains('lite');
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'low-power' });
  renderer.setPixelRatio(Math.min(lite ? 1.5 : 2, devicePixelRatio || 1)); renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  const canvas = renderer.domElement; canvas.className = 't3d'; canvas.setAttribute('role', 'img'); canvas.setAttribute('aria-label', d.label);
  const scene = new THREE.Scene(); const cam = new THREE.PerspectiveCamera(30, 1, .1, 50); cam.position.set(0, 0, 6.2);

  // v5: luce da studio (riflessi morbidi su vernice e bordo oro), fatta in codice: tre pannelli luminosi in una stanza blu notte
  const pmrem = new THREE.PMREMGenerator(renderer);
  const env = new THREE.Scene(); env.background = new THREE.Color(0x0a1633);
  const panel = (c, i, w, h, x, y, z) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(i), side: THREE.DoubleSide })); m.position.set(x, y, z); m.lookAt(0, 0, 0); env.add(m); };
  panel(0xffffff, 3.2, 6, 2.2, 0, 5, 3);      // luce principale dall'alto
  panel(0x9DBEF2, 1.6, 2, 6, -6, 0, 2);       // azzurro di lato
  panel(0xE6CF9F, 2.0, 2, 5, 6, -1, 1.5);     // caldo dall'altro lato
  panel(0xffffff, .5, 8, 8, 0, 0, -7);
  scene.environment = pmrem.fromScene(env, .035).texture;

  const w = 3.2, h = w / 1.586, r = .16, depth = .04;
  const shape = new THREE.Shape(); shape.moveTo(-w / 2 + r, -h / 2); shape.lineTo(w / 2 - r, -h / 2); shape.quadraticCurveTo(w / 2, -h / 2, w / 2, -h / 2 + r); shape.lineTo(w / 2, h / 2 - r);
  shape.quadraticCurveTo(w / 2, h / 2, w / 2 - r, h / 2); shape.lineTo(-w / 2 + r, h / 2); shape.quadraticCurveTo(-w / 2, h / 2, -w / 2, h / 2 - r); shape.lineTo(-w / 2, -h / 2 + r); shape.quadraticCurveTo(-w / 2, -h / 2, -w / 2 + r, -h / 2);
  const edge = new THREE.Mesh(new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: false, curveSegments: 12 }), new THREE.MeshStandardMaterial({ color: 0xD9BD84, metalness: 1, roughness: .26, envMapIntensity: 1.4 }));
  edge.position.z = -depth / 2;
  const card = new THREE.Group(); card.add(edge);
  const face = (tex, z, flip, back) => { const g = new THREE.ShapeGeometry(shape, 12); const uv = g.attributes.uv, p = g.attributes.position;
    for (let k = 0; k < uv.count; k++) uv.setXY(k, p.getX(k) / w + .5, p.getY(k) / h + .5);   // il retro è girato di 180°: stessa mappa
    const m = new THREE.Mesh(g, new THREE.MeshPhysicalMaterial({ map: tex, roughness: back ? .55 : .38, metalness: back ? 0 : .15, clearcoat: 1, clearcoatRoughness: back ? .4 : .12, envMapIntensity: back ? .5 : .9 })); m.position.z = z; if (flip) m.rotation.y = Math.PI; return m; };
  card.add(face(front, depth / 2 + .001, false, false)); card.add(face(back, -depth / 2 - .001, true, true));
  // riflesso che attraversa la tessera
  const sheenMat = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, uniforms: { t: { value: -1 } },
    vertexShader: 'varying vec2 v; void main(){ v = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: 'uniform float t; varying vec2 v; void main(){ float x = v.x + v.y * .45 - t; float a = smoothstep(.0,.12,x) * (1.0 - smoothstep(.12,.26,x)); gl_FragColor = vec4(vec3(1.0,.95,.84), a * .22); }' });
  const sg = new THREE.ShapeGeometry(shape, 12); { const uv = sg.attributes.uv, p = sg.attributes.position; for (let k = 0; k < uv.count; k++) uv.setXY(k, p.getX(k) / w + .5, p.getY(k) / h + .5); }
  const sheen = new THREE.Mesh(sg, sheenMat); sheen.position.z = depth / 2 + .004; card.add(sheen);
  scene.add(card);
  // ombra morbida sotto la tessera
  const sc = document.createElement('canvas'); sc.width = sc.height = 128; { const g = sc.getContext('2d'); const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(0,0,0,.55)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); }
  const shadow = new THREE.Mesh(new THREE.PlaneGeometry(3.4, .7), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(sc), transparent: true, depthWrite: false }));
  shadow.position.set(0, -1.55, -.4); scene.add(shadow);
  scene.add(new THREE.HemisphereLight(0xDCE8FF, 0x0C1D44, .55));
  const key = new THREE.DirectionalLight(0xffffff, 1.1); key.position.set(2.5, 3, 4); scene.add(key);
  const rim = new THREE.DirectionalLight(0x9DBEF2, .7); rim.position.set(-3, -1, 2); scene.add(rim);

  // al posto della tessera 2D (resta nel codice per chi non vede il 3D); il riquadro ha già la sua misura: niente salti
  const flat = host.querySelector('.tessera'); host.prepend(canvas);
  function size() { const W = host.clientWidth, H = host.clientHeight || Math.round(W / 1.2); renderer.setSize(W, H, false); cam.aspect = W / H;
    const t = Math.tan(THREE.MathUtils.degToRad(cam.fov / 2)); cam.position.z = Math.max((w / .74) / (2 * t * cam.aspect), (h / .62) / (2 * t)); cam.updateProjectionMatrix(); }
  size(); addEventListener('resize', size);
  renderer.render(scene, cam);
  requestAnimationFrame(() => { host.classList.add('is3d'); if (flat) { flat.setAttribute('aria-hidden', 'true'); flat.tabIndex = -1; } });

  // v5: rotazione lenta continua quando nessuno la tocca; trascina per girarla, tocca per voltarla, poi riparte da sola
  let ry = -.35, rx = .1, target = ry, drag = null, moved = 0, tiltX = 0, tiltY = 0, px = 0, py = 0, visible = true, last = performance.now(), t0 = last, auto = true, resume = 0;
  let idleT = 0, base = 0;
  canvas.addEventListener('pointerdown', e => { drag = { x: e.clientX, y: e.clientY }; moved = 0; auto = false; canvas.setPointerCapture(e.pointerId); canvas.style.cursor = 'grabbing'; });
  canvas.addEventListener('pointermove', e => { const b = canvas.getBoundingClientRect(); px = ((e.clientX - b.left) / b.width - .5); py = ((e.clientY - b.top) / b.height - .5);
    if (!drag) return; const dx = e.clientX - drag.x, dy = e.clientY - drag.y; drag = { x: e.clientX, y: e.clientY }; moved += Math.abs(dx) + Math.abs(dy); ry += dx * .012; rx = Math.max(-.5, Math.min(.5, rx + dy * .006)); target = ry; });
  canvas.addEventListener('pointerleave', () => { px = py = 0; });
  const release = () => { if (!drag) return; target = moved < 6 ? Math.round(ry / Math.PI) * Math.PI + Math.PI : Math.round(ry / Math.PI) * Math.PI; drag = null; resume = performance.now() + 3500; canvas.style.cursor = ''; };
  canvas.addEventListener('pointerup', release); canvas.addEventListener('pointercancel', release);
  canvas.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); auto = false; target = Math.round(ry / Math.PI) * Math.PI + Math.PI; resume = performance.now() + 3500; } });
  canvas.tabIndex = 0;
  addEventListener('deviceorientation', e => { if (e.gamma == null) return; tiltY = Math.max(-.3, Math.min(.3, e.gamma / 90)); tiltX = Math.max(-.2, Math.min(.2, (e.beta - 45) / 120)); }, { passive: true });
  new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible) { last = performance.now(); requestAnimationFrame(loop); } }).observe(canvas);
  function loop(now) {
    if (!visible || document.hidden) return;
    const dt = Math.min(.05, (now - last) / 1000); last = now; const tt = (now - t0) / 1000;
    if (!drag) {
      if (!auto && now > resume && Math.abs(target - ry) < .02) { auto = true; base = Math.round(ry / (Math.PI * 2)) * Math.PI * 2; idleT = 0; }
      if (auto) {   // fronte che oscilla piano; ogni 14 s un giro completo lento (mostra anche il retro)
        idleT += dt; const c = idleT % 14, turn = c > 10.5 ? (1 - Math.cos(Math.PI * Math.min(1, (c - 10.5) / 3.5))) / 2 : 0;
        const goal = base + (Math.floor(idleT / 14) + turn) * Math.PI * 2 + Math.sin(idleT * .42) * .42; ry += (goal - ry) * Math.min(1, dt * 2.2); target = ry;
      } else ry += (target - ry) * Math.min(1, dt * 4);
      rx += (.1 + Math.sin(tt * .45) * .05 + tiltX - py * .25 - rx) * Math.min(1, dt * 3);
    }
    card.rotation.set(rx, ry + tiltY + px * .3, Math.sin(tt * .3) * .02);
    const bob = Math.sin(tt * .9) * .05; card.position.y = .06 + bob;
    shadow.scale.set(.45 + .55 * Math.abs(Math.cos(ry)), 1, 1); shadow.material.opacity = .75 - bob * 2;
    key.position.set(2.5 + px * 3, 3 - py * 3, 4);
    sheenMat.uniforms.t.value = ((tt * .22) % 1.8) - .4;
    renderer.render(scene, cam); requestAnimationFrame(loop);
  }
  document.addEventListener('visibilitychange', () => { if (!document.hidden && visible) { last = performance.now(); requestAnimationFrame(loop); } });
  requestAnimationFrame(loop);
}
