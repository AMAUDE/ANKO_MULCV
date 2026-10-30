/* ANKO - fonctions communes */
const ANKO = {
  cfg: null,
  pages: [
    ["index.html", "Présentation"],
    ["activites.html", "Présentation des activités"],
    ["cartographie.html", "Cartographie"],
    ["dashboard.html", "Tableau de bord"],
    ["bibliotheque.html", "Bibliothèque"],
  ],
};

ANKO.load = (path) => fetch(path + "?v=" + Date.now()).then((r) => {
  if (!r.ok) throw new Error(path + " : " + r.status);
  return r.json();
});

ANKO.esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
ANKO.norm = (s) => String(s ?? "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim();
ANKO.fmtDate = (d) => (d ? new Date(d).toLocaleDateString("fr-FR", { day: "2-digit", month: "long", year: "numeric" }) : "-");
ANKO.fmtSize = (b) => (b > 1e6 ? (b / 1e6).toFixed(1) + " Mo" : Math.max(1, Math.round(b / 1024)) + " Ko");

/* libelles des sources */
ANKO.sourceLabel = (k) => (ANKO.cfg?.sources?.[String(k).toLowerCase()]?.label) || k;

ANKO.header = (active) => {
  const links = ANKO.pages.map(([h, t]) => `<a href="${h}" class="${h === active ? "active" : ""}">${t}</a>`).join("");
  document.getElementById("site-header").outerHTML = `
    <div class="tri"></div>
    <header class="site-header"><div class="container bar">
      <a class="brand" href="index.html" aria-label="ANKO - accueil">
        <svg width="38" height="38" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="9" fill="#F77F00"/>
          <path d="M8 29l7-17 6 12 4-7 7 12z" fill="#fff"/><circle cx="29" cy="12" r="3.2" fill="#009E60"/></svg>
        <span>ANKO<small>Cartographie foncière · MULCV</small></span></a>
      <button class="menu-toggle" aria-label="Menu" onclick="document.querySelector('.nav').classList.toggle('open')">☰</button>
      <nav class="nav">${links}</nav>
    </div></header>`;
};

ANKO.footer = () => {
  const f = document.getElementById("site-footer");
  if (!f) return;
  f.outerHTML = `<footer class="site-footer"><div class="container row">
    <span>© ${new Date().getFullYear()} ANKO · ${ANKO.esc(ANKO.cfg?.ministere || "MULCV")}</span>
    <span><a href="bibliotheque.html">Bibliothèque</a> · <a href="admin.html">Espace administrateur</a></span></div></footer>`;
};

ANKO.init = async (active) => {
  ANKO.header(active);
  try { ANKO.cfg = await ANKO.load("data/config.json"); } catch (e) { console.error(e); ANKO.cfg = { sources: {} }; }
  ANKO.footer();
  return ANKO.cfg;
};

/* lightbox photos */
ANKO.lightbox = (src, legende) => {
  let lb = document.getElementById("lightbox");
  if (!lb) {
    lb = document.createElement("div"); lb.id = "lightbox"; lb.className = "lightbox";
    lb.innerHTML = '<img alt=""><p></p>'; lb.onclick = () => lb.classList.remove("show");
    document.body.appendChild(lb);
    document.addEventListener("keydown", (e) => e.key === "Escape" && lb.classList.remove("show"));
  }
  lb.querySelector("img").src = src; lb.querySelector("img").alt = legende || "";
  lb.querySelector("p").textContent = legende || ""; lb.classList.add("show");
};

/* icones animees (SVG inline, blanc) */
ANKO.icons = {
  gps: ['GPS', '<path d="M32 8a16 16 0 0 1 16 16c0 12-16 32-16 32S16 36 16 24A16 16 0 0 1 32 8z"/><circle cx="32" cy="24" r="6"/><path d="M10 58h44"/>'],
  qgis: ['QGIS', '<circle cx="32" cy="32" r="22"/><path d="M10 32h44M32 10c-9 10-9 34 0 44M32 10c9 10 9 34 0 44"/>'],
  pc: ['Ordinateur', '<rect x="8" y="12" width="48" height="32" rx="3"/><path d="M22 54h20M32 44v10"/><path d="M16 36l8-10 8 6 10-12"/>'],
  shp: ['.shp', '<path d="M14 6h26l12 12v40H14z"/><path d="M40 6v12h12"/><path d="M22 44l6-12 8 6 6-10"/><circle cx="22" cy="44" r="2"/><circle cx="42" cy="28" r="2"/>'],
  xls: ['Excel', '<path d="M14 6h26l12 12v40H14z"/><path d="M40 6v12h12"/><path d="M22 28l12 18M34 28L22 46"/>'],
  doc: ['Word', '<path d="M14 6h26l12 12v40H14z"/><path d="M40 6v12h12"/><path d="M20 30l4 16 4-12 4 12 4-16"/>'],
  deci: ['Décideurs', '<circle cx="32" cy="18" r="9"/><path d="M14 56c0-12 8-20 18-20s18 8 18 20z"/><path d="M32 36l-4 8 4 8 4-8z"/>'],
  topo: ['Topographe', '<path d="M32 10l10 20H22z"/><path d="M32 30v10M20 58l12-18 12 18"/><circle cx="32" cy="10" r="3"/>'],
};
ANKO.iconSvg = (k) => `<svg viewBox="0 0 64 64" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">${ANKO.icons[k][1]}</svg>`;
ANKO.floatIcons = (keys) => {
  const pos = [[4, 10], [9, 52], [86, 8], [90, 48], [14, 76], [76, 74], [3, 30], [92, 76]];
  return `<div class="float-icons" aria-hidden="true">${keys.map((k, i) =>
    `<div class="ic" style="left:${pos[i % pos.length][0]}%;top:${pos[i % pos.length][1]}%;animation-delay:${(i * 0.9).toFixed(1)}s">${ANKO.iconSvg(k)}<span>${ANKO.icons[k][0]}</span></div>`).join("")}</div>`;
};

/* stats sur la liste des lotissements */
ANKO.criteria = [
  ["normal", "Lotissement normal", (l) => l.statut === "normal"],
  ["regul", "Régularisé", (l) => l.statut === "régularisation"],
  ["conforme", "Conforme", (l) => l.conforme],
  ["nonconforme", "Non conforme", (l) => !l.conforme],
  ["habite", "Habité", (l) => l.habite],
  ["nonhabite", "Non habité", (l) => !l.habite],
  ["urbain", "Urbain", (l) => l.milieu === "urbain"],
  ["village", "Village", (l) => l.milieu === "village"],
  ["conflit", "En conflit", (l) => l.conflit],
  ["actes", "Avec actes", (l) => l.actes],
];
ANKO.criteriaExtra = [
  ["approuve", "Approuvé", (l) => l.etat === "approuvé"],
  ["annule", "Annulé", (l) => l.etat === "annulé"],
  ["arrete", "Avec arrêté", (l) => !!l.num_arrete],
];
ANKO.levels = [["district", "District"], ["region", "Région"], ["departement", "Département"], ["sous_prefecture", "Sous-préfecture"], ["localite", "Localité"]];
