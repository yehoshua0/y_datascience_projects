# Dictionnaire contenant une AOI par culture
aoi_dict = {
    "oil": {
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-75.6526, -9.0840],
                [-74.5510, -9.0840],
                [-74.5510, -8.0746],
                [-75.6526, -8.0746],
                [-75.6526, -9.0840]
            ]]
        }
    },
    "cocoa": {
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-75.2515, -9.4651],
                [-74.9505, -9.4651],
                [-74.9505, -8.3487],
                [-75.2515, -8.3487],
                [-75.2515, -9.4651]
            ]]
        }
    },
    "rubber": {
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-75.0, -9.3],
                [-74.8, -9.3],
                [-74.8, -8.8],
                [-75.0, -8.8],
                [-75.0, -9.3]
            ]]
        }
    }
}


from pystac_client import Client
from odc.stac import load
import numpy as np
import pandas as pd
import xarray as xr
from tqdm import tqdm

def run_extraction(crop_type, geometry, date_range, output_file, nb_pixels=100, seed=42):
    print(f"\n📦 Processing {crop_type.upper()}")

    bands_to_keep = ['red', 'nir', 'swir16', 'swir22', 'blue', 'green',
                     'rededge1', 'rededge2', 'rededge3', 'nir08']

    client = Client.open("https://earth-search.aws.element84.com/v1")
    search = client.search(
        collections=["sentinel-2-l2a"],
        intersects=geometry,
        datetime=date_range
    )

    data = load(
        search.items(),
        geopolygon=geometry,
        groupby="solar_day",
        chunks={},
        bands=bands_to_keep
    )

    y_coords = data.y.values
    x_coords = data.x.values
    all_coords = [(i, j) for i in range(len(y_coords)) for j in range(len(x_coords))]

    np.random.seed(seed)
    sample_idx = np.random.choice(len(all_coords), size=min(nb_pixels, len(all_coords)), replace=False)
    sampled_indices = [all_coords[i] for i in sample_idx]

    samples = []
    pixel_names = []
    for idx, (i, j) in enumerate(tqdm(sampled_indices, desc=f"Sampling {crop_type} pixels"), 1):
        y = y_coords[i]
        x = x_coords[j]
        pixel_name = f"{crop_type.upper()}_PIXEL_{idx:04d}"
        pixel_data = data.isel(y=i, x=j)
        pixel_names.append(pixel_name)
        samples.append(pixel_data)

    stacked = xr.concat(samples, dim="pixel")
    stacked = stacked.assign_coords(pixel=("pixel", pixel_names))

    print("🧠 Computing data...")
    stacked = stacked.compute()

    print("📄 Converting to DataFrame...")
    records = []
    for pixel_id in tqdm(stacked.pixel.values, desc="Writing rows"):
        pixel_data = stacked.sel(pixel=pixel_id)
        for t in stacked.time.values:
            row = {band: pixel_data[band].sel(time=t).item() for band in bands_to_keep}
            row.update({
                "unique_id": pixel_id,
                "y": float(pixel_data.y),
                "x": float(pixel_data.x),
                "time": str(t),
                "crop_type": crop_type
            })
            records.append(row)

    df = pd.DataFrame(records)
    df.to_csv(output_file, index=False)
    print(f"✅ Saved: {output_file}")


# Paramètres généraux
date_range = "2020-01-01/2020-01-10"

# Lancement automatique
for crop_type, info in aoi_dict.items():
    geometry = info["geometry"]
    output_file = f"./../data/processed/s2_{crop_type}_dask.csv"
    
    run_extraction(
        crop_type=crop_type,
        geometry=geometry,
        date_range=date_range,
        output_file=output_file,
        nb_pixels=100  # tu peux ajuster à 50 ou 300
    )

import pandas as pd

# Liste des fichiers à fusionner
files = ["./../data/processed/s2_oil_dask.csv", "./../data/processed/s2_cocoa_dask.csv", "./../data/processed/s2_rubber_dask.csv"]

# Chargement et concaténation
df_all = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Mélange aléatoire des lignes
df_all = df_all.sample(frac=1, random_state=42).reset_index(drop=True)

# Sauvegarde dans un fichier final
df_all.to_csv("./../data/processed/s2_all_shuffled.csv", index=False)

print("✅ Fichier combiné créé : s2_all_shuffled.csv")
