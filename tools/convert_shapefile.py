#!/usr/bin/env python3
"""Convertit vos Shapefiles / GeoPackage en GeoJSON WGS84 pour ANKO.

La projection de chaque fichier est lue automatiquement (.prj / GeoPackage),
quelle qu'elle soit (UTM 29N, UTM 30N, etc.), puis convertie en EPSG:4326.

Installation :  pip install geopandas
Exemple :
    python tools/convert_shapefile.py --lots lots.shp --ilots ilots.shp --lotissements contours.shp
    python tools/convert_shapefile.py --lots donnees.gpkg --layer-lots lot

Champs attendus (noms exacts, a renommer dans QGIS si besoin) :
  lots   : lotissement_id, ilot, lot, demandeur, superficie_m2, acte
  ilots  : lotissement_id, ilot
  contours (lotissements) : id   (= id de data/lotissements.json)
"""
import argparse, os, sys

try:
    import geopandas as gpd
except ImportError:
    sys.exit("geopandas manque :  pip install geopandas")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def convert(src, layer, out_name, keep):
    g = gpd.read_file(src, layer=layer) if layer else gpd.read_file(src)
    if g.crs is None:
        sys.exit(f"{src} : aucune projection definie (.prj manquant). Definissez-la dans QGIS puis reexportez.")
    print(f"{src} : projection {g.crs} -> EPSG:4326, {len(g)} entites")
    g = g.to_crs(4326)
    cols = [c for c in keep if c in g.columns]
    missing = [c for c in keep if c not in g.columns]
    if missing:
        print(f"  attention, champs absents : {', '.join(missing)}")
    g = g[cols + ["geometry"]]
    g["geometry"] = g.geometry.simplify(0.0000005)   # ~5 cm, allege le fichier
    out = os.path.join(ROOT, "data", "geo", out_name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    g.to_file(out, driver="GeoJSON", COORDINATE_PRECISION=6)
    print("  ->", out)


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--lots"); ap.add_argument("--layer-lots")
ap.add_argument("--ilots"); ap.add_argument("--layer-ilots")
ap.add_argument("--lotissements"); ap.add_argument("--layer-lotissements")
a = ap.parse_args()
if not (a.lots or a.ilots or a.lotissements):
    ap.print_help(); sys.exit(1)
if a.lots: convert(a.lots, a.layer_lots, "lots.geojson", ["lotissement_id", "ilot", "lot", "demandeur", "superficie_m2", "acte"])
if a.ilots: convert(a.ilots, a.layer_ilots, "ilots.geojson", ["lotissement_id", "ilot"])
if a.lotissements: convert(a.lotissements, a.layer_lotissements, "lotissements.geojson", ["id"])
