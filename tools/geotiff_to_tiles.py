#!/usr/bin/env python3
"""Transforme un plan de lotissement GeoTIFF georeference en tuiles web legeres.

Necessite GDAL (inclus avec QGIS : lancez ce script depuis la "OSGeo4W Shell").
Exemple :
    python tools/geotiff_to_tiles.py plan_L0001.tif L0001

Resultat : data/plans/L0001/{z}/{x}/{y}.png
Puis, dans data/lotissements.json (ou via l'Excel), pour ce lotissement :
    "plan_tuiles": "data/plans/L0001/{z}/{x}/{y}.png",  "sur_carte": true
et renseignez "plan_bounds": [[lat_min, lon_min], [lat_max, lon_max]] pour le cadrage.
(Les bornes s'affichent avec :  gdalinfo -proj4 plan_L0001.tif  -> "Lower Left / Upper Right" en WGS84.)
"""
import os, shutil, subprocess, sys

if len(sys.argv) != 3:
    sys.exit(__doc__)
tif, lid = sys.argv[1], sys.argv[2]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(root, "data", "plans", lid)
exe = shutil.which("gdal2tiles.py") or shutil.which("gdal2tiles")
if not exe:
    sys.exit("gdal2tiles introuvable : lancez depuis la OSGeo4W Shell de QGIS.")
cmd = [sys.executable, exe] if exe.endswith(".py") else [exe]
subprocess.check_call(cmd + ["--xyz", "-z", "14-21", "--processes", "4", "-w", "none", tif, out])
print("Tuiles ecrites dans", out)
print(f'plan_tuiles = "data/plans/{lid}/{{z}}/{{x}}/{{y}}.png"')
