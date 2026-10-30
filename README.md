# ANKO – Plateforme de cartographie foncière (MULCV)

Plateforme web statique dédiée à la modernisation des lotissements en Côte d'Ivoire.
Aucun serveur : tout fonctionne sur **GitHub Pages**.

| Page | Fichier | Contenu |
|---|---|---|
| Présentation | `index.html` | Accueil, enjeux, structures partenaires |
| Présentation des activités | `activites.html` | Séances de travail, données reçues par direction |
| Cartographie | `cartographie.html` | Carte, recherche, filtres de localité, plan géoréférencé |
| Tableau de bord | `dashboard.html` | Statistiques, liste des lotissements, base des actes |
| Bibliothèque | `bibliotheque.html` | Catalogue physique / numérique par direction |
| Administration | `admin.html` | Dépôt de fichiers sans code (via GitHub) |

> **Les données actuelles sont FICTIVES** (63 lotissements d'exemple). Remplacez-les par les vraies (voir plus bas).

## Voir le site en local

```bash
python -m http.server 8000
```

Puis ouvrir <http://localhost:8000>. (Ouvrir les fichiers par double-clic ne marche pas : le navigateur bloque la lecture des JSON.)

## Mise en ligne sur GitHub Pages

1. Créer un dépôt GitHub, y envoyer tout ce dossier.
2. **Settings → Pages → Deploy from a branch → `main` / `(root)`**.
3. Le site est disponible sur `https://<compte>.github.io/<depot>/`.

## Remplacer les données par les vraies

### Liste des lotissements et actes (Excel)
Page **Administration** → étape 2 : glisser le fichier Excel/CSV. Colonnes attendues (première feuille) :

- `data/lotissements.json` : `id, nom, source (DTC|DMISSA|DUDU|SECTEUR), direction_secteur, district, region, departement, sous_prefecture, localite, num_arrete, date_arrete, etat (approuvé|non approuvé|annulé), statut (normal|régularisation), nb_ilots, nb_lots, demandeur, conforme, habite, milieu (urbain|village), conflit, actes` (oui/non).
- `data/actes.json` : `id_acte, type_acte, num_acte, titulaire, date_acte, lotissement_id, lotissement, ilot, lot, superficie_m2`.

La géométrie déjà connue (position, plan) est conservée pour les `id` existants.

### Couches SIG (Shapefile / GeoPackage → GeoJSON)
```bash
pip install geopandas
python tools/convert_shapefile.py --lots lots.shp --ilots ilots.shp --lotissements contours.shp
```
La projection (UTM 29N, 30N…) est lue dans chaque fichier et convertie en WGS84. Champs attendus : voir l'en-tête du script.
Un lotissement n'apparaît **sur la carte** que si `sur_carte = oui`, avec ses contours dans `lotissements.geojson` et son `centre`.

### Plans de lotissement géoréférencés (GeoTIFF)
```bash
python tools/geotiff_to_tiles.py plan_L0001.tif L0001
```
(à lancer depuis la *OSGeo4W Shell* de QGIS). Renseigner ensuite `plan_tuiles` et `plan_bounds` pour le lotissement (voir l'en-tête du script).

### Bibliothèque, séances, logos, arrêtés
Page **Administration**, étapes 3 à 5. Les fichiers (PDF, Word, DWG) sont stockés dans le dépôt (limite GitHub : 100 Mo par fichier).

## Configuration

`data/config.json` : nom de la plateforme, **partenaires** (ajoutez-en autant que voulu, avec leur logo), directions régionales du Secteur MULCV, et nombre de lotissements annoncé par direction (texte « plus de 513 lotissements »).

## Page Administration : mise en place du jeton

1. GitHub → *Settings → Developer settings → Fine-grained tokens → Generate*.
2. Limiter au dépôt ANKO, permission **Contents : Read and write**.
3. Coller le jeton dans l'étape 1 de la page admin. Il reste dans l'onglet seulement.

> Limite à connaître : la page admin est publique (comme le site) mais inutilisable sans jeton ; seul le jeton protège l'écriture. Ne le partagez qu'avec les administrateurs.

## Régénérer les données d'exemple

```bash
python tools/generate_sample_data.py
```

## Technologies
HTML / CSS / JavaScript, [Leaflet](https://leafletjs.com), [SheetJS](https://sheetjs.com) (import Excel), fonds de carte OpenStreetMap et Esri.
