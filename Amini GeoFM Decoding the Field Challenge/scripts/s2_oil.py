from pystac_client import Client
from odc.stac import load
import numpy as np
import pandas as pd
import xarray as xr
from tqdm import tqdm

# 1. STAC search setup
client = Client.open("https://earth-search.aws.element84.com/v1")
collection = "sentinel-2-l2a"

geometry = {
    "type": "Polygon",
    "coordinates": [[
        [-75.6526, -9.0840],
        [-74.5510, -9.0840],
        [-74.5510, -8.0746],
        [-75.6526, -8.0746],
        [-75.6526, -9.0840]
    ]]
}
date_range = "2020-01-01/2020-01-10"

bands_to_keep = ['red', 'nir', 'swir16', 'swir22', 'blue', 'green',
                 'rededge1', 'rededge2', 'rededge3', 'nir08']

# 2. Search & load STAC with only required bands and use Dask
search = client.search(
    collections=[collection],
    intersects=geometry,
    datetime=date_range
)
data = load(
    search.items(),
    geopolygon=geometry,
    groupby="solar_day",
    chunks={},  # Enables Dask (lazy load)
    bands=bands_to_keep
)

# 3. Get coordinates and sample N random pixels
y_coords = data.y.values
x_coords = data.x.values
all_coords = [(i, j) for i in range(len(y_coords)) for j in range(len(x_coords))]

# Pick 100 pixels
np.random.seed(42)
sample_idx = np.random.choice(len(all_coords), size=100, replace=False)
sampled_indices = [all_coords[i] for i in sample_idx]

# 4. Extract all sampled pixels over time and bands
print("Loading all sampled pixels using Dask...")

samples = []
pixel_names = []

for idx, (i, j) in enumerate(tqdm(sampled_indices, desc="Sampling pixels"), 1):
    y = y_coords[i]
    x = x_coords[j]
    pixel_name = f"PIXEL_{idx:04d}"
    pixel_data = data.isel(y=i, x=j)
    pixel_names.append(pixel_name)
    samples.append(pixel_data)

# Stack all samples into one Dataset
stacked = xr.concat(samples, dim="pixel")
stacked = stacked.assign_coords(pixel=("pixel", pixel_names))

# 5. Compute all values in one go
print("Computing pixel data...")
stacked = stacked.compute()

# 6. Convert to DataFrame
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
            "crop_type": "oil"
        })
        records.append(row)

df = pd.DataFrame(records)
df.to_csv("s2_oil_dask.csv", index=False)
print("✅ Done: s2_oil_dask.csv written.")
