#!/usr/bin/env python3
"""Genere les donnees FICTIVES d'exemple d'ANKO (aucune dependance).

    python tools/generate_sample_data.py

Ecrit dans data/ et assets/. A remplacer par vos vraies donnees
(voir README.md : convert_shapefile.py / convert_excel.py).
"""
import json, math, os, random

random.seed(2026)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def p(*parts):
    path = os.path.join(ROOT, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def dump(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


def esc_xml(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ------------------------------------------------------------------ geographie
LOCALITES = [
    # district, region, departement, sous-prefecture, localite, lat, lon
    ("District Autonome d'Abidjan", "Abidjan", "Abidjan", "Bingerville", "Bingerville", 5.355, -3.885),
    ("District Autonome d'Abidjan", "Abidjan", "Abidjan", "Songon", "Songon", 5.320, -4.270),
    ("District Autonome d'Abidjan", "Abidjan", "Abidjan", "Anyama", "Anyama", 5.495, -4.050),
    ("Lagunes", "Grands-Ponts", "Dabou", "Dabou", "Dabou", 5.325, -4.375),
    ("Lagunes", "Agnéby-Tiassa", "Agboville", "Agboville", "Agboville", 5.930, -4.220),
    ("Lagunes", "La Mé", "Adzopé", "Adzopé", "Adzopé", 6.105, -3.860),
    ("Comoé", "Sud-Comoé", "Grand-Bassam", "Grand-Bassam", "Grand-Bassam", 5.210, -3.740),
    ("Comoé", "Sud-Comoé", "Aboisso", "Aboisso", "Aboisso", 5.470, -3.210),
    ("Bas-Sassandra", "San-Pédro", "San-Pédro", "San-Pédro", "San-Pédro", 4.750, -6.650),
    ("Bas-Sassandra", "Gbôklé", "Sassandra", "Sassandra", "Sassandra", 4.950, -6.090),
    ("Sassandra-Marahoué", "Haut-Sassandra", "Daloa", "Daloa", "Daloa", 6.880, -6.450),
    ("Sassandra-Marahoué", "Marahoué", "Bouaflé", "Bouaflé", "Bouaflé", 6.990, -5.740),
    ("District Autonome de Yamoussoukro", "Yamoussoukro", "Yamoussoukro", "Yamoussoukro", "Yamoussoukro", 6.820, -5.280),
    ("Vallée du Bandama", "Gbêkê", "Bouaké", "Bouaké", "Bouaké", 7.690, -5.030),
    ("Vallée du Bandama", "Hambol", "Katiola", "Katiola", "Katiola", 8.140, -5.100),
    ("Zanzan", "Gontougo", "Bondoukou", "Bondoukou", "Bondoukou", 8.040, -2.800),
    ("Savanes", "Poro", "Korhogo", "Korhogo", "Korhogo", 9.460, -5.630),
    ("Montagnes", "Tonkpi", "Man", "Man", "Man", 7.410, -7.550),
    ("Denguélé", "Kabadougou", "Odienné", "Odienné", "Odienné", 9.510, -7.560),
    ("Gôh-Djiboua", "Gôh", "Gagnoa", "Gagnoa", "Gagnoa", 6.130, -5.950),
]
QUARTIERS = ["Résidentiel", "Extension Nord", "Akwaba", "Les Cocotiers", "Cité Verte", "Plateau Dokui",
             "Nouveau Quartier", "Koko", "Les Palmiers", "Extension Sud", "Cité de la Paix", "Belle Vue",
             "Zone Commerciale", "Les Manguiers", "Riviera Extension"]
SOURCES = ["DTC"] * 5 + ["DMISSA"] * 3 + ["DUDU"] * 3 + ["SECTEUR"] * 2
DR = ["DR Abidjan", "DR Bouaké", "DR Daloa", "DR San-Pédro", "DR Korhogo", "DR Man", "DR Yamoussoukro"]
PRENOMS = ["Kouadio", "Aya", "Yao", "Adjoua", "Koffi", "Amenan", "Kouassi", "Awa", "Mamadou", "Fatoumata",
           "Séka", "Marie", "Ibrahim", "Salimata", "N'Guessan", "Affoué", "Ouattara", "Bintou", "Jean", "Clarisse"]
NOMS = ["Kouamé", "Traoré", "Koné", "Bamba", "Yao", "Coulibaly", "Diallo", "Konan", "Touré", "N'Dri",
        "Kra", "Soro", "Gnahoré", "Aka", "Zadi", "Dosso", "Tano", "Brou", "Ehui", "Sanogo"]
TYPES_ACTE = ["ACD", "Attestation villageoise", "Lettre d'attribution", "Certificat de propriété",
              "Arrêté de concession provisoire"]


def nom_complet():
    return f"{random.choice(PRENOMS)} {random.choice(NOMS)}"


# ------------------------------------------------------------------ lotissements
LON_SCALE = 1.0
W, H, GAP = 0.00022, 0.00022, 0.00012


def rect(lon0, lat0, lon1, lat1):
    r = lambda v: round(v, 6)
    return [[[r(lon0), r(lat0)], [r(lon1), r(lat0)], [r(lon1), r(lat1)], [r(lon0), r(lat1)], [r(lon0), r(lat0)]]]


lotissements, f_lotiss, f_ilots, f_lots = [], [], [], []
n = 0
for (dist, reg, dep, sp, loc, lat, lon) in LOCALITES:
    for k in range(random.randint(2, 4)):
        n += 1
        lid = f"L{n:04d}"
        source = random.choice(SOURCES)
        etat = random.choices(["approuvé", "non approuvé", "annulé"], [60, 30, 10])[0]
        has_arrete = etat != "non approuvé" or random.random() < 0.2
        yr = random.randint(2008, 2025)
        sur_carte = random.random() < 0.8
        row = {
            "id": lid,
            "nom": f"Lotissement {random.choice(QUARTIERS)} {loc} {random.choice(['I', 'II', 'III', ''])}".strip(),
            "source": source,
            "direction_secteur": random.choice(DR) if source == "SECTEUR" else "",
            "district": dist, "region": reg, "departement": dep, "sous_prefecture": sp, "localite": loc,
            "num_arrete": f"{random.randint(100, 999)}/MCLU/DGUF/{yr}" if has_arrete else "",
            "date_arrete": f"{yr}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}" if has_arrete else "",
            "arrete_pdf": "",
            "etat": etat,
            "statut": random.choices(["normal", "régularisation"], [65, 35])[0],
            "demandeur": random.choice([f"Commune de {loc}", f"Chefferie de {loc}", nom_complet(),
                                        f"SCI {random.choice(NOMS)}"]),
            "conforme": random.random() < 0.7,
            "habite": random.random() < 0.6,
            "milieu": random.choices(["urbain", "village"], [55, 45])[0],
            "conflit": random.random() < 0.12,
            "actes": False,
            "sur_carte": sur_carte,
            "centre": [lat, lon],
            "plan_image": "", "plan_bounds": None, "plan_tuiles": "", "nb_ilots": 0, "nb_lots": 0,
        }
        if has_arrete:
            row["arrete_pdf"] = f"data/arretes/{lid}.pdf"
        if sur_carte:
            o_lat = lat + random.uniform(-0.012, 0.012)
            o_lon = lon + random.uniform(-0.012, 0.012)
            rows_i, cols_i = random.choice([(2, 2), (2, 3), (3, 3), (2, 4)])
            lots_x, lots_y = 3, 2
            iw, ih = lots_x * W, lots_y * H
            for r_i in range(rows_i):
                for c_i in range(cols_i):
                    ilot_no = r_i * cols_i + c_i + 1
                    x0 = o_lon + c_i * (iw + GAP)
                    y1 = o_lat - r_i * (ih + GAP)
                    f_ilots.append({"type": "Feature", "properties": {"lotissement_id": lid, "ilot": ilot_no},
                                    "geometry": {"type": "Polygon", "coordinates": rect(x0, y1 - ih, x0 + iw, y1)}})
                    lot_no = 0
                    for ly in range(lots_y):
                        for lx in range(lots_x):
                            lot_no += 1
                            lx0, ly1 = x0 + lx * W, y1 - ly * H
                            dem = nom_complet() if random.random() < 0.85 else ""
                            f_lots.append({"type": "Feature",
                                           "properties": {"lotissement_id": lid, "ilot": ilot_no, "lot": lot_no,
                                                          "demandeur": dem, "superficie_m2": random.choice([400, 500, 600, 800]),
                                                          "acte": ""},
                                           "geometry": {"type": "Polygon", "coordinates": rect(lx0, ly1 - H, lx0 + W, ly1)}})
            tw = cols_i * (iw + GAP) - GAP
            th = rows_i * (ih + GAP) - GAP
            pad = 0.00015
            b = [o_lon - pad, o_lat - th - pad, o_lon + tw + pad, o_lat + pad]
            f_lotiss.append({"type": "Feature", "properties": {"id": lid},
                             "geometry": {"type": "Polygon", "coordinates": rect(*b)}})
            row["nb_ilots"] = rows_i * cols_i
            row["nb_lots"] = rows_i * cols_i * lots_x * lots_y
            row["centre"] = [round((b[1] + b[3]) / 2, 6), round((b[0] + b[2]) / 2, 6)]
            mp = 0.00012
            row["plan_bounds"] = [[round(b[1] - mp, 6), round(b[0] - mp, 6)], [round(b[3] + mp, 6), round(b[2] + mp, 6)]]
            row["plan_image"] = f"data/plans/{lid}.svg"
        else:
            row["nb_ilots"] = random.randint(4, 40)
            row["nb_lots"] = row["nb_ilots"] * random.randint(6, 14)
        lotissements.append(row)

# actes
by_lotiss = {l["id"]: l for l in lotissements}
cands = [f for f in f_lots if f["properties"]["demandeur"]]
random.shuffle(cands)
actes = []
for i, f in enumerate(cands[: int(len(cands) * 0.18)], 1):
    pr = f["properties"]
    t = random.choice(TYPES_ACTE)
    pr["acte"] = t
    by_lotiss[pr["lotissement_id"]]["actes"] = True
    actes.append({
        "id_acte": f"A{i:05d}", "type_acte": t,
        "num_acte": f"{random.randint(1000, 9999)}/{random.randint(2010, 2025)}",
        "titulaire": pr["demandeur"],
        "date_acte": f"{random.randint(2010, 2025)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "lotissement_id": pr["lotissement_id"], "lotissement": by_lotiss[pr["lotissement_id"]]["nom"],
        "ilot": pr["ilot"], "lot": pr["lot"], "superficie_m2": pr["superficie_m2"],
    })

# plans SVG (stand-in d'un GeoTIFF georeference)
lots_by = {}
for f in f_lots:
    lots_by.setdefault(f["properties"]["lotissement_id"], []).append(f)
for l in lotissements:
    if not l["sur_carte"]:
        continue
    (la0, lo0), (la1, lo1) = l["plan_bounds"]
    Wp = 900
    Hp = int(Wp * (la1 - la0) / ((lo1 - lo0) * math.cos(math.radians(la0))))
    X = lambda lo: (lo - lo0) / (lo1 - lo0) * Wp
    Y = lambda la: (la1 - la) / (la1 - la0) * Hp
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wp} {Hp}" width="{Wp}" height="{Hp}">',
             f'<rect width="{Wp}" height="{Hp}" fill="#fbf6e6"/>']
    for f in lots_by[l["id"]]:
        c = f["geometry"]["coordinates"][0]
        pts = " ".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in c)
        parts.append(f'<polygon points="{pts}" fill="#fffdf4" stroke="#8a4b0f" stroke-width="1"/>')
        cx = sum(a for a, _ in c[:4]) / 4
        cy = sum(b for _, b in c[:4]) / 4
        parts.append(f'<text x="{X(cx):.1f}" y="{Y(cy) + 3:.1f}" font-size="9" text-anchor="middle" fill="#5a3410" font-family="Arial">{f["properties"]["lot"]}</text>')
    parts.append(f'<text x="12" y="22" font-size="15" font-weight="bold" fill="#1b3a57" font-family="Arial">PLAN DE LOTISSEMENT (exemple) - {esc_xml(l["nom"])}</text></svg>')
    with open(p("data", "plans", f"{l['id']}.svg"), "w", encoding="utf-8") as fh:
        fh.write("".join(parts))


# ------------------------------------------------------------------ PDF minimal
def make_pdf(path, lines):
    def esc(s):
        return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    stream = "BT /F1 13 Tf 56 780 Td 20 TL\n" + "".join(f"({esc(t)}) Tj T*\n" for t in lines) + "ET"
    sb = stream.encode("cp1252", "replace")
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
            b"<< /Length %d >>\nstream\n" % len(sb) + sb + b"\nendstream",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"]
    out, offs = bytearray(b"%PDF-1.4\n"), []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    x = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for o in offs:
        out += b"%010d 00000 n \n" % o
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF" % (len(objs) + 1, x)
    with open(path, "wb") as fh:
        fh.write(out)


for l in lotissements:
    if l["arrete_pdf"]:
        make_pdf(p("data", "arretes", f"{l['id']}.pdf"),
                 ["REPUBLIQUE DE COTE D'IVOIRE", "ARRETE DE LOTISSEMENT (DOCUMENT D'EXEMPLE)", "",
                  f"N° {l['num_arrete']}", f"Lotissement : {l['nom']}", f"Localité : {l['localite']}", "",
                  "Document fictif genere pour la demonstration de la plateforme ANKO."])

# ------------------------------------------------------------------ bibliotheque
BIB_SRC = {"dtc": "DTC", "dmissa": "DMISSA", "dudu": "DUDU", "secteur": "Secteur MULCV"}
bib = {}
for key, label in BIB_SRC.items():
    docs = [{"titre": t, "reference": f"{label}/DOC/{random.randint(100, 999)}", "annee": random.randint(2005, 2025),
             "localisation": f"Archives {label} - armoire {random.randint(1, 9)}"}
            for t in ["Registre des lotissements", "Dossiers d'approbation", "Correspondances officielles", "Procès-verbaux de bornage"]]
    cartes = [{"titre": t, "reference": f"{label}/CAR/{random.randint(100, 999)}", "annee": random.randint(2005, 2025),
               "localisation": f"Cartothèque {label} - tiroir {random.randint(1, 12)}"}
              for t in ["Plan d'ensemble du territoire", "Carte des lotissements approuvés", "Planches cadastrales 1/5000"]]
    num = {"pdf": [], "word": [], "dwg": []}
    for ext, titles in [("pdf", ["Rapport d'activités", "Liste des lotissements transmis", "Arrêtés scannés"]),
                        ("word", ["Note méthodologique", "Compte rendu de transmission"]),
                        ("dwg", ["Plan masse lotissement (exemple)", "Fond de plan cadastral (exemple)"])]:
        for t in titles:
            slug = t.lower().replace(" ", "_").replace("'", "").replace("é", "e").replace("è", "e").replace("(", "").replace(")", "")
            rel = f"data/bibliotheque/{key}/{ext}/{slug}.{'docx' if ext == 'word' else ext}"
            full = p(*rel.split("/"))
            if ext == "pdf":
                make_pdf(full, [f"{label} - {t}", "", "Document d'exemple (ANKO)."])
            else:
                with open(full, "w", encoding="utf-8") as fh:
                    fh.write("Fichier d'exemple ANKO : remplacez-le par le vrai document.\n")
            num[ext].append({"titre": t, "fichier": rel, "taille": os.path.getsize(full),
                             "date": f"{random.randint(2022, 2026)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"})
    bib[key] = {"physique": {"documents": docs, "cartes": cartes}, "numerique": num}

# ------------------------------------------------------------------ visuels
PALETTE = {"dtc": "#009E60", "dmissa": "#0B3C6B", "dudu": "#C45A00", "secteur": "#7A2E8E", "mulcv": "#F77F00"}


def badge(name, color, text):
    with open(p("assets", "logos", f"{name}.svg"), "w", encoding="utf-8") as fh:
        size = 34 if len(text) <= 4 else 24
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><circle cx="100" cy="100" r="96" fill="{color}"/>'
                 f'<circle cx="100" cy="100" r="82" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="6 6"/>'
                 f'<text x="100" y="{100 + size / 3}" font-family="Arial" font-weight="bold" font-size="{size * 1.4}" fill="#fff" text-anchor="middle">{esc_xml(text)}</text></svg>')


for k, c in PALETTE.items():
    badge(k, c, k.upper() if k != "secteur" else "SMC")

seances = [
    ("2026-02-12", "Séance de lancement du projet", "Cabinet du MULCV, Abidjan-Plateau",
     "Présentation des objectifs de la plateforme de cartographie foncière et répartition des rôles entre directions.", "#F77F00"),
    ("2026-03-05", "Atelier de collecte avec la DTC", "Salle de réunion DTC",
     "Inventaire des lotissements détenus par la DTC et définition du format d'échange des données.", "#009E60"),
    ("2026-03-26", "Atelier DMISSA et DUDU", "Direction de l'Urbanisme",
     "Recensement des arrêtés, plans et fichiers numériques fournis par la DMISSA et la DUDU.", "#0B3C6B"),
    ("2026-04-16", "Séance avec les directions régionales", "Visioconférence",
     "Collecte des lotissements du Secteur MULCV, par direction régionale.", "#7A2E8E"),
    ("2026-05-07", "Restitution et démonstration d'ANKO", "Cabinet du MULCV",
     "Présentation de la première version de la plateforme aux décideurs et recueil des retours.", "#C45A00"),
]
out_seances = []
for i, (d, t, lieu, desc, color) in enumerate(seances, 1):
    imgs = []
    for j in range(1, 4):
        rel = f"assets/seances/s{i}-{j}.svg"
        with open(p("assets", "seances", f"s{i}-{j}.svg"), "w", encoding="utf-8") as fh:
            fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
                     f'<stop offset="0" stop-color="{color}"/><stop offset="1" stop-color="#0B2545"/></linearGradient></defs>'
                     f'<rect width="800" height="520" fill="url(#g)"/><g fill="#fff" fill-opacity=".85"><circle cx="300" cy="230" r="42"/>'
                     f'<circle cx="400" cy="210" r="48"/><circle cx="500" cy="230" r="42"/><rect x="240" y="280" width="320" height="110" rx="40"/></g>'
                     f'<text x="400" y="450" font-family="Arial" font-size="26" fill="#fff" text-anchor="middle">Photo de séance (à remplacer) {j}/3</text></svg>')
        imgs.append({"src": rel, "legende": f"{t} - photo {j}"})
    out_seances.append({"id": f"S{i}", "date": d, "titre": t, "lieu": lieu, "description": desc, "images": imgs})

with open(p("assets", "parcelle-bg.svg"), "w", encoding="utf-8") as fh:
    segs = []
    for r in range(0, 14):
        for c in range(0, 24):
            x, y = c * 90 + random.randint(-8, 8), r * 70 + random.randint(-8, 8)
            w, h = random.randint(70, 86), random.randint(52, 66)
            segs.append(f'<path d="M{x} {y}l{w} {random.randint(-5, 5)}l{random.randint(-5, 5)} {h}l{-w} {random.randint(-5, 5)}z"/>')
    fh.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2200 980"><g fill="none" stroke="#ffffff" stroke-opacity=".28" stroke-width="1.4">'
             + "".join(segs) + '</g></svg>')

# ------------------------------------------------------------------ ecriture
fc = lambda feats: {"type": "FeatureCollection", "features": feats}
dump(p("data", "lotissements.json"), lotissements)
dump(p("data", "actes.json"), actes)
dump(p("data", "bibliotheque.json"), bib)
dump(p("data", "seances.json"), out_seances)
dump(p("data", "geo", "lotissements.geojson"), fc(f_lotiss))
dump(p("data", "geo", "ilots.geojson"), fc(f_ilots))
dump(p("data", "geo", "lots.geojson"), fc(f_lots))
print(f"{len(lotissements)} lotissements, {len(f_lots)} lots, {len(actes)} actes OK")
