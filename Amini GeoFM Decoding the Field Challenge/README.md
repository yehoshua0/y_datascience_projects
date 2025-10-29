# 🌾 Amini GeoFM Decoding the Field Challenge Solution

A high-performance agricultural land classification solution using Sentinel-2 multi-temporal imagery. The repo contains preprocessing utilities, example notebooks, and scripts to extract per-pixel time series and produce model-ready CSVs used to train ensemble models (GeoFM features + gradient boosting).

- Public LB Score: **0.967279452**
- Private LB Score: **0.983572624**

## Quick links

- Full example notebook: [notebooks/StarterNotebook.ipynb](Amini GeoFM Decoding the Field Challenge/notebooks/StarterNotebook.ipynb)
- Extended README / explanation: [README_ex.md](Amini GeoFM Decoding the Field Challenge/README_ex.md)
- Requirements: [requirements.txt](Amini GeoFM Decoding the Field Challenge/requirements.txt)
- Processed dataset (example): [data/processed/s2_all_shuffled.csv](Amini GeoFM Decoding the Field Challenge/data/processed/s2_all_shuffled.csv)
- Raw train CSV: [data/raw/TrainDataset.csv](Amini GeoFM Decoding the Field Challenge/data/raw/TrainDataset.csv)
- Example submission: [output/earth_fm_rf_submission.csv](Amini GeoFM Decoding the Field Challenge/output/earth_fm_rf_submission.csv) and [output/SampleSubmission.csv](Amini GeoFM Decoding the Field Challenge/output/SampleSubmission.csv)

## Repo layout

- data/
  - raw/ — source geojson/shapefiles and small CSVs ([data/raw/TrainDataset.csv](Amini GeoFM Decoding the Field Challenge/data/raw/TrainDataset.csv))
  - processed/ — per-pixel time series CSVs ([data/processed/s2_all_shuffled.csv](Amini GeoFM Decoding the Field Challenge/data/processed/s2_all_shuffled.csv))
- notebooks/ — experimentation and starter notebooks ([notebooks/StarterNotebook.ipynb](Amini GeoFM Decoding the Field Challenge/notebooks/StarterNotebook.ipynb))
- scripts/ — data extraction & conversion utilities:
  - [scripts/get_s2_data_utils.py](Amini GeoFM Decoding the Field Challenge/scripts/get_s2_data_utils.py)
  - [scripts/s2_cocoa.py](Amini GeoFM Decoding the Field Challenge/scripts/s2_cocoa.py)
  - [scripts/s2_oil.py](Amini GeoFM Decoding the Field Challenge/scripts/s2_oil.py)
  - [scripts/s2_rubber.py](Amini GeoFM Decoding the Field Challenge/scripts/s2_rubber.py)
  - [scripts/tmp.py](Amini GeoFM Decoding the Field Challenge/scripts/tmp.py) — contains [`SatelliteDataProcessor`](Amini GeoFM Decoding the Field Challenge/scripts/tmp.py)
- env/ — included virtual environment (optional)
- output/ — sample submission and exports

## Main utilities

- Pixel/time-series extraction and CSV conversion: the scripts in [scripts/](Amini GeoFM Decoding the Field Challenge/scripts) create the per-pixel temporal dataset used for modeling. See [scripts/get_s2_data_utils.py](Amini GeoFM Decoding the Field Challenge/scripts/get*s2_data_utils.py) and the `s2*\*` scripts for examples.
- `SatelliteDataProcessor` in [scripts/tmp.py](Amini GeoFM Decoding the Field Challenge/scripts/tmp.py) is a reusable class for STAC search, loading with ODC, chunked xarray processing and pixel time-series extraction. See the class docstring and `main()` example in that file.

## Quickstart (local)

1. Create & activate Python env (recommended):
   - python -m venv .venv && source .venv/bin/activate (Windows: .\.venv\Scripts\Activate.ps1)
2. Install dependencies:
   - pip install -r requirements.txt
3. Inspect or run the starter notebook:
   - open [notebooks/StarterNotebook.ipynb](Amini GeoFM Decoding the Field Challenge/notebooks/StarterNotebook.ipynb)
4. Run extraction scripts (examples):
   - python scripts/s2_oil.py
   - python scripts/s2_cocoa.py
   - python scripts/s2_rubber.py
   - Or use the high-level processor in [scripts/tmp.py](Amini GeoFM Decoding the Field Challenge/scripts/tmp.py)

## Reproduce model input

- Generated CSVs in data/processed (e.g. [s2_all_shuffled.csv](Amini GeoFM Decoding the Field Challenge/data/processed/s2_all_shuffled.csv)) are the primary inputs for downstream feature engineering and model training demonstrated in the notebooks.

## Notes & tips

- The repo includes a pre-baked virtualenv under `env/` for convenience; prefer creating a fresh venv and installing via [requirements.txt](Amini GeoFM Decoding the Field Challenge/requirements.txt).
- For large STAC downloads / Sentinel-2 processing, ensure sufficient disk space and consider running on a machine with >16 GB RAM.
- Use the example output [output/earth_fm_rf_submission.csv](Amini GeoFM Decoding the Field Challenge/output/earth_fm_rf_submission.csv) as a template for submission formatting.

## Where to look first

1. [notebooks/StarterNotebook.ipynb](Amini GeoFM Decoding the Field Challenge/notebooks/StarterNotebook.ipynb) — end-to-end example.
2. [scripts/tmp.py](Amini GeoFM Decoding the Field Challenge/scripts/tmp.py) — `SatelliteDataProcessor` and helper functions.
3. [scripts/get_s2_data_utils.py](Amini GeoFM Decoding the Field Challenge/scripts/get_s2_data_utils.py) — utilities to merge and prepare per-crop CSVs.

## Reproduce results

Follow the notebook workflow: extract pixel timeseries → compute features → train model(s) → export predictions. See [README_ex.md](Amini GeoFM Decoding the Field Challenge/README_ex.md) for more detailed reproduction steps and model details.
