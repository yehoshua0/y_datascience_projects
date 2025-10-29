from pystac_client import Client
from odc.stac import load
import numpy as np
import pandas as pd
import xarray as xr
from tqdm import tqdm

# 1. STAC client
client = Client.open("https://earth-search.aws.element84.com/v1")
collection = "sentinel-2-l2a"

# 2. Geometry for cacao AOI
geometry = {
    'type': 'Polygon',
    'coordinates': [[
        [-75.25153082092892, -9.465163691321777],
        [-74.950508271378, -9.465163691321777],
        [-74.950508271378, -8.348714404017642],
        [-75.25153082092892, -8.348714404017642],
        [-75.25153082092892, -9.465163691321777]
    ]]
}

# 3. Date range and bands
date_range = "2020-01-01/2020-01-10"
bands_to_keep = ['red', 'nir', 'swir16', 'swir22', 'blue', 'green',
                 'rededge1', 'rededge2', 'rededge3', 'nir08']

# 4. STAC search + load
search = client.search(
    collections=[collection],
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

# 5. Sample coordinates
y_coords = data.y.values
x_coords = data.x.values
all_coords = [(i, j) for i in range(len(y_coords)) for j in range(len(x_coords))]

np.random.seed(42)
sample_idx = np.random.choice(len(all_coords), size=100, replace=False)
sampled_indices = [all_coords[i] for i in sample_idx]

# 6. Extract pixel samples
samples = []
pixel_names = []
for idx, (i, j) in enumerate(tqdm(sampled_indices, desc="Sampling pixels"), 1):
    y = y_coords[i]
    x = x_coords[j]
    pixel_name = f"PIXEL_{idx:04d}"
    pixel_data = data.isel(y=i, x=j)
    pixel_names.append(pixel_name)
    samples.append(pixel_data)

stacked = xr.concat(samples, dim="pixel")
stacked = stacked.assign_coords(pixel=("pixel", pixel_names))

# 7. Compute all values
print("Computing pixel data...")
stacked = stacked.compute()

# 8. Convert to DataFrame
print("Converting to DataFrame...")

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
            "crop_type": "cocoa"  # 👈 updated
        })
        records.append(row)

df = pd.DataFrame(records)
df.to_csv("s2_cocoa_dask.csv", index=False)  # 👈 updated output file name
print("✅ Done: s2_cocoa_dask.csv written.")
