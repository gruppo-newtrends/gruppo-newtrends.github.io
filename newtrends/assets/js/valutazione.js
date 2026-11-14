/* VALUTAZIONE ONLINE New Trends (14.11.2026): percorso in 6 passi + stima indicativa calcolata NEL BROWSER.
   Dati: window.NTVAL_DATA (mediane aggregate CHF/m² dal CRM, scritte nella pagina dal generatore; nessun dato personale).
   Testi: window.NTVAL_T (lingua della pagina). Invio: un solo POST al CRM (window.NT.endpoint) quando si preme «Invia»;
   niente salvato sul dispositivo, niente strumenti di misura.
   Il motore (stima, regioneNPA, cantoneNPA) è lo stesso in node per le prove: module.exports. */
(function (root) {
  "use strict";
  var V = {};

  // ---------------- motore ----------------
  V.norm = function (s) {
    s = String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
    return s.replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
  };
  // NPA ticinese -> regione (stessa tabella di esporta_valutazione.py e app/valutazione_online.py)
  V.regioneNPA = function (npa) {
    var n = parseInt(String(npa || "").trim().slice(0, 4), 10);
    if (!(n >= 1000 && n <= 9999)) return null;
    if (n >= 6534 && n <= 6565) return null;
    if ([6523, 6524, 6526, 6527].indexOf(n) > -1) return "Valli";
    if ((n >= 6500 && n <= 6533) || (n >= 6582 && n <= 6584) || [6592, 6593, 6594, 6599, 6702].indexOf(n) > -1) return "Bellinzonese";
    if ((n >= 6571 && n <= 6579) || (n >= 6595 && n <= 6598) || (n >= 6600 && n <= 6699)) return "Locarnese";
    if (n >= 6700 && n <= 6799) return "Valli";
    if ((n >= 6800 && n <= 6823) || n === 6827 || (n >= 6900 && n <= 6999)) return "Luganese";
    if (n >= 6825 && n <= 6899) return "Mendrisiotto";
    return null;
  };
  // cantone indicativo dal NPA (i numeri postali non seguono sempre i confini: la persona conferma nel menu)
  var CANT = [[1000, 1199, "VD"], [1200, 1299, "GE"], [1300, 1599, "VD"], [1600, 1799, "FR"], [1800, 1869, "VD"], [1870, 1999, "VS"], [2000, 2349, "NE"],
    [2350, 2399, "JU"], [2400, 2499, "NE"], [2500, 2799, "BE"], [2800, 2999, "JU"], [3000, 3899, "BE"], [3900, 3999, "VS"], [4000, 4099, "BS"], [4100, 4499, "BL"],
    [4500, 4799, "SO"], [4800, 4899, "AG"], [4900, 4999, "BE"], [5000, 5999, "AG"], [6000, 6299, "LU"], [6300, 6349, "ZG"], [6350, 6399, "NW"], [6400, 6449, "SZ"],
    [6450, 6499, "UR"], [6534, 6565, "GR"], [6500, 6999, "TI"], [7000, 7799, "GR"], [8000, 8199, "ZH"], [8200, 8299, "SH"], [8300, 8499, "ZH"], [8500, 8599, "TG"],
    [8600, 8749, "ZH"], [8750, 8799, "GL"], [8800, 8899, "SZ"], [8900, 8999, "ZH"], [9000, 9099, "SG"], [9100, 9199, "AR"], [9200, 9499, "SG"], [9500, 9599, "TG"], [9600, 9699, "SG"]];
  V.cantoneNPA = function (npa) {
    var n = parseInt(String(npa || "").trim().slice(0, 4), 10);
    if (!(n >= 1000 && n <= 9999)) return "";
    if (V.regioneNPA(n)) return "TI";
    for (var i = 0; i < CANT.length; i++) if (n >= CANT[i][0] && n <= CANT[i][1]) return CANT[i][2];
    return "";
  };
  function fascia(tab, x) { for (var i = 0; i < tab.length; i++) if (x >= tab[i][0]) return tab[i][1]; return tab[tab.length - 1][1]; }
  function arrot(x, deal) { var s = deal === "affitto" ? 50 : (x < 1e6 ? 5000 : 10000); return Math.round(x / s) * s; }

  /* x = {deal, tipo, npa, comune, mq, anno, annoRistr, stato, piano, esterno:[], box, esterni, vista, energia}
     -> {ok:true, min, max, punto, fonte, base, n, p, area, fattori:[[chiave, valore]], posti} | {ok:false, motivo} */
  V.stima = function (D, x) {
    var F = D.fattori, deal = x.deal === "affitto" ? "affitto" : "vendita", tipo = x.tipo;
    if (tipo === "terreno") return { ok: false, motivo: "terreno" };
    var g = tipo === "appartamento" ? "appartamento" : tipo === "commerciale" ? "commerciale" : "casa";
    var reg = V.regioneNPA(x.npa);
    if (!reg) return { ok: false, motivo: "fuori" };
    var mq = +x.mq;
    if (!(mq >= 15 && mq <= 3000)) return { ok: false, motivo: "mq" };
    var blk = (D[deal] || {})[g];
    if (!blk) return { ok: false, motivo: "tipo" };
    var com = blk.comuni[V.norm(x.comune)];
    if (com && com.r !== reg) com = null;
    var rm = blk.regioni[reg] || null, fonte, base, n, p;
    if (!rm && D.indice[deal] && D.indice[deal][reg]) rm = { m: blk.ticino.m * D.indice[deal][reg], n: blk.ticino.n, p: blk.ticino.p, ind: true };
    if (com) { base = rm ? 0.6 * com.m + 0.4 * rm.m : com.m; fonte = "comune"; n = com.n; p = com.p; }
    else if (rm) { base = rm.m; fonte = "regione"; n = rm.n; p = rm.p; }
    else return { ok: false, motivo: "regione", regione: reg };
    var fx = [], f = 1;
    function add(k, v) { if (v && v !== 1) { fx.push([k, v]); f *= v; } }
    var anno = Math.max(+x.anno || 0, +x.annoRistr || 0);
    if (anno > 1800) add("anno", fascia(F.anno, anno));
    add("mq", fascia(deal === "affitto" && F.mq_affitto && F.mq_affitto[g] ? F.mq_affitto[g] : F.mq[g], mq));
    if (F.tipo[tipo]) add("tipo", F.tipo[tipo]);
    if (x.stato && F.stato[x.stato]) add("stato", F.stato[x.stato]);
    if (g === "appartamento" && x.piano && F.piano[x.piano]) add("piano", F.piano[x.piano]);
    if (g !== "commerciale") {
      var tab = g === "casa" ? F.esterno_casa : F.esterno, es = (x.esterno || []).filter(function (e) { return tab[e]; });
      if (!es.length) add("esterno", tab.nessuno);
      else { var best = Math.max.apply(null, es.map(function (e) { return tab[e]; })); add("esterno", best * (g === "appartamento" ? 1 + 0.01 * (es.length - 1) : 1)); }
      if (x.vista && F.vista[x.vista]) add("vista", F.vista[x.vista]);
      if (x.energia && F.energia[x.energia]) add("energia", F.energia[x.energia]);
    }
    f = Math.min(F.limiti[1], Math.max(F.limiti[0], f));
    var caro = reg === "Luganese" || reg === "Locarnese" ? 0 : 1, PP = F.posto[deal];
    var posti = (Math.min(+x.box || 0, 6)) * PP.box[caro] + (Math.min(+x.esterni || 0, 6)) * PP.esterno[caro];
    var punto = base * f * mq + posti;
    var w = F.ampiezza[fonte] + (tipo === "rustico" ? F.ampiezza.rustico : 0) + ((mq > 300 || mq < 30) ? F.ampiezza.taglia : 0) + (deal === "affitto" ? (F.ampiezza.affitto || 0) : 0) + (g === "casa" ? (F.ampiezza.casa || 0) : 0);
    return { ok: true, deal: deal, regione: reg, fonte: fonte, base: Math.round(base * (deal === "affitto" ? 10 : 1)) / (deal === "affitto" ? 10 : 1), n: n, p: p,
      fattore: Math.round(f * 1000) / 1000, fattori: fx, posti: posti, punto: arrot(punto, deal), min: arrot(punto * (1 - w), deal), max: arrot(punto * (1 + w), deal), w: w };
  };

  if (typeof module !== "undefined" && module.exports) { module.exports = V; return; }
  root.NTVAL = V;

  // ---------------- interfaccia ----------------
  var d = document, T = root.NTVAL_T || {}, D = root.NTVAL_DATA, C = root.NT || {};
  var app = d.querySelector("[data-val]");
  if (!app || !D) return;
  var $ = function (s, el) { return (el || d).querySelector(s); }, $$ = function (s, el) { return Array.prototype.slice.call((el || d).querySelectorAll(s)); };
  var steps = $$(".vstep", app), cur = 0, N = steps.length, bar = $(".vprog i", app), lab = $(".vprog-l", app), form = $("form.vform", app);
  var lang = d.documentElement.lang || "it", sep = lang === "en" ? "," : "'";
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function chf(n) { return "CHF " + String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, sep); }
  function val(name) { var el = form.elements[name]; if (!el) return ""; if (el.length && !el.tagName) { var r = $$('[name="' + name + '"]:checked', form).map(function (x) { return x.value; }); return el[0].type === "checkbox" ? r : (r[0] || ""); } return String(el.value || "").trim(); }
  function tipo() { return val("tipo"); }
  function show(i, focus) {
    cur = Math.max(0, Math.min(N - 1, i));
    steps.forEach(function (s, k) { s.hidden = k !== cur; });
    if (bar) bar.style.width = Math.round((cur + 1) / N * 100) + "%";
    if (lab) lab.textContent = (T.passo || "Passo") + " " + (cur + 1) + " / " + N;
    app.setAttribute("data-step", cur + 1);
    var t = tipo();
    $$("[data-solo]", app).forEach(function (el) { el.hidden = el.getAttribute("data-solo").split(" ").indexOf(t) < 0; });
    $$("[data-deal-t]", app).forEach(function (el) { var k = el.getAttribute("data-deal-t") + (val("deal") === "affitto" ? "_aff" : ""); if (T[k]) el.textContent = T[k]; });
    if (focus) { var h = $("h2", steps[cur]); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); } app.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" }); }
  }
  function err(step, msg, el) {
    var e = $(".verr", step); if (e) { e.textContent = msg || ""; e.hidden = !msg; }
    $$("[aria-invalid]", step).forEach(function (x) { x.removeAttribute("aria-invalid"); });
    if (el) { el.setAttribute("aria-invalid", "true"); el.focus(); }
    return !msg;
  }
  function check(i) {
    var s = steps[i], f = form.elements, t = tipo();
    if (i === 0 && !val("deal")) return err(s, T.e_scelta, $$('[name="deal"]', s)[0]);
    if (i === 1 && !t) return err(s, T.e_scelta, $$('[name="tipo"]', s)[0]);
    if (i === 2) {
      if (!/^\d{4}$/.test(val("npa"))) return err(s, T.e_npa, f.npa);
      if (!/^[A-Za-zÀ-ÿ'’ .()\/-]{2,60}$/.test(val("comune"))) return err(s, T.e_comune, f.comune);
      if (!V.regioneNPA(val("npa")) && !val("cantone")) return err(s, T.e_cantone, f.cantone);
    }
    if (i === 3) {
      var mq = +val("mq");
      if (!(mq >= 15 && mq <= (t === "terreno" ? 100000 : 3000))) return err(s, T.e_mq, f.mq);
      var a = val("anno"), r = val("anno_ristr"), y = new Date().getFullYear() + 3;
      if (a && !(+a >= 1500 && +a <= y)) return err(s, T.e_anno, f.anno);
      if (r && !(+r >= 1900 && +r <= y)) return err(s, T.e_anno, f.anno_ristr);
    }
    if (i === 4 && !val("entro")) return err(s, T.e_scelta, $$('[name="entro"]', s)[0]);
    if (i === 5) {
      if (val("nome").length < 2) return err(s, T.e_nome, f.nome);
      var tel = val("telefono").replace(/[^\d+]/g, ""), em = val("email");
      if (tel.replace(/\D/g, "").length < 9) return err(s, T.e_tel, f.telefono);
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)) return err(s, T.e_email, f.email);
      if (!f.consenso.checked) return err(s, T.e_consenso, f.consenso);
    }
    return err(s, "");
  }
  // NPA: regione o cantone
  var npa = form.elements.npa, cant = $(".vcant", app), regOut = $(".vreg", app);
  function npaInfo() {
    var v = val("npa"), r = /^\d{4}$/.test(v) ? V.regioneNPA(v) : null, c = /^\d{4}$/.test(v) ? V.cantoneNPA(v) : "";
    if (regOut) { regOut.textContent = r ? (T.regione || "") + " " + r + " · Ticino" : (c && c !== "TI" ? (T.fuori_ti || "") : ""); regOut.hidden = !regOut.textContent; }
    if (cant) { cant.hidden = !(/^\d{4}$/.test(v) && !r); var sel = form.elements.cantone; if (sel && !r && c && !sel.dataset.toccato) sel.value = c === "TI" ? "" : c; }
  }
  if (npa) { npa.addEventListener("input", npaInfo); npaInfo(); }
  form.addEventListener("change", function (e) { var st = e.target.closest(".vstep"), er = st && $(".verr", st); if (er && !er.hidden) { er.hidden = true; e.target.removeAttribute("aria-invalid"); } });
  if (form.elements.cantone) form.elements.cantone.addEventListener("change", function () { this.dataset.toccato = 1; });
  // scelte a schede: avanti da solo dopo la scelta (passi 1 e 2)
  $$('.vcards input[type="radio"]', app).forEach(function (r) {
    r.addEventListener("change", function () { var i = steps.indexOf(r.closest(".vstep")); if (i < 2) setTimeout(function () { if (check(i)) show(i + 1, true); }, 180); });
  });
  $$("[data-next]", app).forEach(function (b) { b.addEventListener("click", function () { if (check(cur)) show(cur + 1, true); }); });
  $$("[data-prev]", app).forEach(function (b) { b.addEventListener("click", function () { show(cur - 1, true); }); });
  var start = $("[data-start]", d);
  if (start) start.addEventListener("click", function (e) { e.preventDefault(); app.hidden = false; app.classList.add("on"); show(0, true); });

  function input() {
    return { deal: val("deal"), tipo: tipo(), npa: val("npa"), comune: val("comune"), mq: +val("mq"), anno: +val("anno") || 0, annoRistr: +val("anno_ristr") || 0,
      stato: val("stato"), piano: val("piano"), esterno: val("esterno"), box: +val("box") || 0, esterni: +val("esterni") || 0, vista: val("vista"), energia: val("energia") };
  }
  function code() { var t = new Date(); return "NT-V" + String(t.getFullYear()).slice(2) + String(t.getMonth() + 1).padStart(2, "0") + String(t.getDate()).padStart(2, "0") + "-" + Math.random().toString(36).slice(2, 6).toUpperCase(); }
  function optText(name) { var el = form.elements[name]; if (!el) return ""; if (el.tagName === "SELECT") return el.value ? el.options[el.selectedIndex].text : ""; var r = $$('[name="' + name + '"]:checked', form).map(function (x) { var l = x.closest("label"), b = l && l.querySelector("b"); return (b || l) ? (b || l).textContent.trim().replace(/\s+/g, " ") : x.value; }); return r.join(", "); }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    for (var i = 0; i < N; i++) if (!check(i)) { show(i, true); check(i); return; }
    var x = input(), r = V.stima(D, x), k = code(), btn = $('button[type="submit"]', form);
    btn.disabled = true; btn.textContent = T.invio || "…";
    var reg = V.regioneNPA(x.npa), cn = reg ? "TI" : val("cantone");
    var stima = r.ok ? { min: r.min, max: r.max, punto: r.punto, unita: r.deal === "affitto" ? "CHF/mese" : "CHF", fonte: r.fonte, base: r.base, n: r.n, p: r.p, fattore: r.fattore } : { motivo: r.motivo };
    var righe = [T.m_head + " (" + k + ")", T.l_deal + ": " + optText("deal"), T.l_tipo + ": " + optText("tipo"), T.l_dove + ": " + [val("via"), x.npa + " " + val("comune")].filter(Boolean).join(", ") + (reg ? " (" + reg + ")" : " (" + cn + ")"),
      T.l_mq + ": " + x.mq + " m²" + (val("locali") ? " · " + val("locali") + " " + T.locali_u : "")];
    if (r.ok) righe.push(T.l_stima + ": " + chf(r.min) + " – " + chf(r.max) + (r.deal === "affitto" ? " " + T.al_mese : ""));
    var payload = { company: C.company || "newtrends", name: val("nome"), email: val("email"), phone: val("telefono"), kind: "Proprietario · valutazione online", town: val("comune"),
      message: righe.join("\n"), consent: true, newsletter: false, website: val("website"),
      valutazione: { v: 1, codice: k, pagina: location.pathname, lingua_pagina: lang, deal: x.deal, tipo: x.tipo, npa: x.npa, comune: val("comune"), via: val("via"), regione: reg || "", cantone: cn,
        mq: x.mq, locali: val("locali"), piano: x.piano, anno: x.anno || "", anno_ristr: x.annoRistr || "", stato: x.stato, esterno: x.esterno, box: x.box, esterni: x.esterni, vista: x.vista, energia: x.energia,
        entro: val("entro"), motivo: val("motivo"), mandato: val("mandato"), lingua: val("lingua") || lang, nota: val("nota").slice(0, 800), consenso: true, stima: stima } };
    var done = function (ok) { risultato(r, x, k, ok, righe); };
    if (!C.endpoint) return done(false);
    var ctl = "AbortController" in root ? new AbortController() : null, to = setTimeout(function () { if (ctl) ctl.abort(); }, 20000);
    fetch(C.endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload), signal: ctl ? ctl.signal : undefined })
      .then(function (res) { clearTimeout(to); done(res.ok); }, function () { clearTimeout(to); done(false); });
  });

  function risultato(r, x, k, inviato, righe) {
    var out = $(".vres", app), aff = x.deal === "affitto";
    steps.forEach(function (s) { s.hidden = true; });
    $(".vprog", app).hidden = true; out.hidden = false;
    var h = "";
    if (r.ok) {
      h += '<p class="eyebrow">' + (aff ? T.r_eyebrow_aff : T.r_eyebrow) + "</p>";
      h += '<p class="vrange"><span>' + chf(r.min) + ' <span class="vdash">–</span></span><span>' + chf(r.max) + "</span>" + (aff ? '<small>' + T.al_mese_netto + "</small>" : "") + "</p>";
      h += '<p class="vlead">' + T.r_lead.replace("{dove}", esc(x.comune) + " (" + r.regione + ")") + "</p>";
      var fl = r.fattori.map(function (a) { var p = Math.round((a[1] - 1) * 100); return "<li><span>" + (T["f_" + a[0]] || a[0]) + "</span><b>" + (p > 0 ? "+" : "") + p + "%</b></li>"; }).join("");
      h += '<details class="vcome"><summary>' + T.r_come + "</summary><div>";
      h += "<p>" + (r.fonte === "comune" ? T.r_base_comune : T.r_base_regione).replace("{base}", chf(r.base) + (aff ? T.mq_mese : "/m²")).replace("{n}", r.n).replace("{p}", r.p).replace("{comune}", esc(x.comune)).replace("{regione}", r.regione) + "</p>";
      if (fl) h += '<ul class="vfx">' + fl + "</ul>";
      if (r.posti) h += "<p>" + T.r_posti.replace("{chf}", chf(r.posti)) + "</p>";
      h += "<p>" + T.r_forbice.replace("{w}", Math.round(r.w * 100)) + "</p></div></details>";
    } else {
      h += '<p class="eyebrow">' + T.r_eyebrow_no + "</p><h2>" + T.r_no_t + "</h2>";
      h += '<p class="vlead">' + (T["r_no_" + r.motivo] || T.r_no_regione).replace("{regione}", r.regione || "") + "</p>";
    }
    h += '<div class="vdisc"><b>' + T.d_t + "</b><p>" + T.d_txt + "</p></div>";
    h += '<div class="vnext"><h3>' + T.n_t + '</h3><ol><li><b>' + T.n1 + "</b><span>" + T.n1d + "</span></li><li><b>" + T.n2 + "</b><span>" + T.n2d + "</span></li><li><b>" + T.n3 + "</b><span>" + T.n3d + "</span></li></ol></div>";
    h += '<details class="vcosti"><summary>' + (aff ? T.c_t_aff : T.c_t) + "</summary><div>" + (aff ? T.c_aff : T.c_vend) + "</div></details>";
    h += inviato ? '<p class="vok" role="status">' + T.ok.replace("{code}", "<code>" + k + "</code>") + "</p>"
      : '<p class="vko" role="alert">' + T.ko.replace("{code}", "<code>" + k + "</code>") + "</p>";
    h += '<div class="vacts"><a class="btn btn-gold" href="tel:+41919210031">' + T.chiama + ' +41 91 921 00 31</a><a class="btn btn-line" href="https://wa.me/' + (C.wa || "41768232203") + "?text=" + encodeURIComponent(inviato ? T.wa_txt.replace("{code}", k) : righe.join("\n")) + '" target="_blank" rel="noopener">WhatsApp</a></div>';
    out.innerHTML = h;
    var t0 = $("h2, .vrange", out); if (t0) { t0.setAttribute("tabindex", "-1"); t0.focus({ preventScroll: true }); }
    app.scrollIntoView({ behavior: "auto", block: "start" });
  }
  // con #valuta nell'indirizzo (link dal menu o dal link in bio) il percorso si apre subito
  if (/^#(start|inizia|valuta)/.test(location.hash) && start) start.click();
})(typeof window !== "undefined" ? window : this);
