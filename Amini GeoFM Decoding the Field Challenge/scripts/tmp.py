import numpy as np
import pandas as pd
import geopandas as gpd
import xarray as xr
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import logging
from datetime import datetime
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from pystac_client import Client
from odc.stac import load
from odc.geo import Geometry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning)

class SatelliteDataProcessor:
    """
    Robust and efficient satellite data processor for crop classification.
    Handles GeoJSON input and produces CSV output with satellite time series.
    """
    
    def __init__(self, 
                 stac_url: str = "https://earth-search.aws.element84.com/v1",
                 collection: str = "sentinel-2-l2a",
                 bands: List[str] = None):
        """
        Initialize the processor.
        
        Args:
            stac_url: STAC API endpoint
            collection: Satellite collection name
            bands: List of bands to extract
        """
        self.stac_url = stac_url
        self.collection = collection
        self.bands = bands or ['red', 'nir', 'swir16', 'swir22', 'blue', 'green', 
                              'rededge1', 'rededge2', 'rededge3', 'nir08']
        self.client = None
        
    def _initialize_client(self) -> None:
        """Initialize STAC client with retry logic."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.client = Client.open(self.stac_url)
                logger.info(f"✅ Connected to STAC API: {self.stac_url}")
                return
            except Exception as e:
                logger.warning(f"⚠️ Connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise ConnectionError(f"Failed to connect to STAC API after {max_retries} attempts")
                time.sleep(2 ** attempt)  # Exponential backoff
    
    def extract_bbox_from_geojson(self, geojson_path: Union[str, Path]) -> Optional[Dict]:
        """
        Extract bounding box from GeoJSON file with robust error handling.
        
        Args:
            geojson_path: Path to GeoJSON file
            
        Returns:
            GeoJSON-style polygon dict or None if invalid
        """
        try:
            geojson_path = Path(geojson_path)
            if not geojson_path.exists():
                logger.error(f"❌ GeoJSON file not found: {geojson_path}")
                return None
                
            logger.info(f"📂 Reading GeoJSON: {geojson_path.name}")
            gdf = gpd.read_file(geojson_path)
            
            if gdf.empty:
                logger.error("❌ GeoJSON file is empty")
                return None
            
            # Robust geometry validation
            initial_count = len(gdf)
            gdf = gdf[gdf.geometry.notnull()]
            gdf = gdf[gdf.geometry.is_valid]
            gdf = gdf[gdf.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]
            
            if gdf.empty:
                logger.error("❌ No valid polygonal geometries found")
                return None
                
            valid_count = len(gdf)
            if valid_count < initial_count:
                logger.warning(f"⚠️ Filtered out {initial_count - valid_count} invalid geometries")
            
            # Ensure consistent CRS
            if gdf.crs is None:
                logger.warning("⚠️ No CRS found, assuming EPSG:4326")
                gdf = gdf.set_crs("EPSG:4326")
            elif gdf.crs.to_string() != "EPSG:4326":
                logger.info(f"🔄 Converting from {gdf.crs} to EPSG:4326")
                gdf = gdf.to_crs("EPSG:4326")
            
            # Calculate bounding box
            minx, miny, maxx, maxy = gdf.total_bounds
            
            # Validate bounds
            if not (-180 <= minx <= 180 and -180 <= maxx <= 180 and 
                   -90 <= miny <= 90 and -90 <= maxy <= 90):
                logger.error("❌ Invalid coordinate bounds")
                return None
            
            bbox_geometry = {
                "type": "Polygon",
                "coordinates": [[
                    [minx, miny], [maxx, miny], [maxx, maxy], [minx, maxy], [minx, miny]
                ]]
            }
            
            area = (maxx - minx) * (maxy - miny)
            logger.info(f"📐 Bounding box area: {area:.6f} degrees² ({valid_count} geometries)")
            
            return bbox_geometry
            
        except Exception as e:
            logger.error(f"❌ Error processing GeoJSON {geojson_path}: {e}")
            return None
    
    def search_satellite_data(self, 
                            geometry: Dict,
                            date_range: str,
                            max_items: int = 500,
                            cloud_cover_max: float = 20.0) -> Tuple[Optional[List], Optional[object]]:
        """
        Search satellite data with robust error handling.
        
        Args:
            geometry: GeoJSON geometry
            date_range: Date range string (e.g., "2020-01-01/2020-01-31")
            max_items: Maximum items to return
            cloud_cover_max: Maximum cloud cover percentage
            
        Returns:
            Tuple of (items, search_object) or (None, None) if failed
        """
        try:
            if self.client is None:
                self._initialize_client()
            
            query = {"eo:cloud_cover": {"lte": cloud_cover_max}} if cloud_cover_max is not None else {}
            
            logger.info(f"🔍 Searching {self.collection} for {date_range} (cloud cover ≤ {cloud_cover_max}%)")
            
            search = self.client.search(
                collections=[self.collection],
                intersects=geometry,
                datetime=date_range,
                query=query,
                max_items=max_items
            )
            
            items = search.item_collection()
            
            if not items:
                logger.warning("⚠️ No items found for the given criteria")
                return None, None
            
            # Validate available bands
            available_bands = set()
            for item in items[:5]:  # Check first 5 items
                available_bands.update(item.assets.keys())
            
            missing_bands = set(self.bands) - available_bands
            if missing_bands:
                logger.warning(f"⚠️ Missing bands: {missing_bands}")
                self.bands = [b for b in self.bands if b in available_bands]
                logger.info(f"📊 Using available bands: {self.bands}")
            
            logger.info(f"📦 Found {len(items)} items")
            return items, search
            
        except Exception as e:
            logger.error(f"❌ Error searching satellite data: {e}")
            return None, None
    
    def load_satellite_data(self, 
                          search_results: object,
                          geometry: Dict,
                          chunk_size: int = 2048) -> Optional[xr.Dataset]:
        """
        Load satellite data with optimized chunking and error handling.
        
        Args:
            search_results: Search results from STAC
            geometry: GeoJSON geometry for clipping
            chunk_size: Chunk size for Dask arrays
            
        Returns:
            xarray Dataset or None if failed
        """
        try:
            logger.info(f"📥 Loading satellite data with {len(self.bands)} bands")
            
            # Convert geometry to odc.geo.Geometry
            if isinstance(geometry, dict):
                geometry = Geometry(geometry, crs="EPSG:4326")
            
            # Optimized loading with chunking
            chunks = {"time": 1, "y": chunk_size, "x": chunk_size}
            
            data = load(
                search_results.items(),
                geopolygon=geometry,
                groupby="solar_day",
                chunks=chunks,
                bands=self.bands,
                resolution=10,  # 10m resolution for Sentinel-2
                resampling="bilinear",
                dtype="float32"  # Optimize memory usage
            )
            
            if data is None or len(data.data_vars) == 0:
                logger.error("❌ No data loaded")
                return None
            
            # Validate data
            total_pixels = data.sizes.get('x', 0) * data.sizes.get('y', 0)
            if total_pixels == 0:
                logger.error("❌ No spatial data found")
                return None
            
            logger.info(f"📊 Loaded data: {data.sizes} with {len(data.data_vars)} bands")
            logger.info(f"📅 Time range: {data.time.min().values} to {data.time.max().values}")
            
            return data
            
        except Exception as e:
            logger.error(f"❌ Error loading satellite data: {e}")
            return None
    
    def extract_pixel_timeseries(self, 
                               dataset: xr.Dataset,
                               n_samples: int = 300,
                               crop_type: str = "unknown",
                               seed: int = 42) -> Optional[pd.DataFrame]:
        """
        Extract pixel time series with optimized sampling and validation.
        
        Args:
            dataset: xarray Dataset
            n_samples: Number of pixels to sample
            crop_type: Crop type label
            seed: Random seed for reproducibility
            
        Returns:
            DataFrame with pixel time series or None if failed
        """
        try:
            np.random.seed(seed)
            
            # Validate dataset dimensions
            if 'x' not in dataset.dims or 'y' not in dataset.dims:
                logger.error("❌ Dataset missing spatial dimensions")
                return None
            
            ny, nx = len(dataset.y), len(dataset.x)
            total_pixels = ny * nx
            
            if total_pixels == 0:
                logger.error("❌ No spatial pixels found")
                return None
            
            # Adjust sample size if necessary
            n_samples = min(n_samples, total_pixels)
            if n_samples < n_samples:
                logger.warning(f"⚠️ Reducing sample size to {n_samples} (total pixels: {total_pixels})")
            
            logger.info(f"🎯 Sampling {n_samples} pixels from {total_pixels} total")
            
            # Efficient spatial sampling
            sampled_indices = np.random.choice(total_pixels, size=n_samples, replace=False)
            ys, xs = np.unravel_index(sampled_indices, shape=(ny, nx))
            
            # Create pixel identifiers
            pixel_ids = [f"PIXEL_{i+1:05d}" for i in range(n_samples)]
            
            # Efficient data selection
            stacked = dataset.isel(y=("pixel", ys), x=("pixel", xs))
            stacked = stacked.assign_coords(pixel=("pixel", pixel_ids))
            stacked = stacked.assign_coords(
                x=("pixel", dataset.x.values[xs]),
                y=("pixel", dataset.y.values[ys])
            )
            
            # Compute data in memory
            logger.info("💾 Computing data...")
            stacked = stacked.compute()
            
            # Convert to DataFrame
            df = stacked.to_dataframe().reset_index()
            
            # Clean up data
            df = df.dropna(subset=self.bands)  # Remove rows with NaN values
            
            if df.empty:
                logger.error("❌ No valid data after cleaning")
                return None
            
            # Add metadata
            df["crop_type"] = crop_type
            df = df.rename(columns={"pixel": "unique_id"})
            
            # Reorder columns to match expected format
            expected_cols = ["unique_id", "time", "x", "y", "crop_type"] + self.bands
            available_cols = [col for col in expected_cols if col in df.columns]
            df = df[available_cols]
            
            # Validate data ranges (for Sentinel-2, reflectance should be 0-1)
            for band in self.bands:
                if band in df.columns:
                    band_data = df[band]
                    if band_data.min() < 0 or band_data.max() > 1:
                        logger.warning(f"⚠️ {band} values outside expected range [0,1]: {band_data.min():.3f} to {band_data.max():.3f}")
            
            logger.info(f"✅ Extracted {len(df)} records for {crop_type}")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error extracting pixel timeseries: {e}")
            return None
    
    def process_crop_data(self, 
                         geojson_path: Union[str, Path],
                         date_range: str,
                         crop_type: str,
                         n_samples: int = 300,
                         cloud_cover_max: float = 20.0,
                         output_path: Optional[Union[str, Path]] = None) -> Optional[pd.DataFrame]:
        """
        Complete pipeline for processing one crop type.
        
        Args:
            geojson_path: Path to GeoJSON file
            date_range: Date range string
            crop_type: Crop type label
            n_samples: Number of samples to extract
            cloud_cover_max: Maximum cloud cover
            output_path: Optional output CSV path
            
        Returns:
            DataFrame or None if failed
        """
        logger.info(f"🌱 Processing {crop_type} data from {Path(geojson_path).name}")
        
        # Step 1: Extract bounding box
        bbox_geometry = self.extract_bbox_from_geojson(geojson_path)
        if bbox_geometry is None:
            return None
        
        # Step 2: Search satellite data
        items, search = self.search_satellite_data(
            bbox_geometry, date_range, cloud_cover_max=cloud_cover_max
        )
        if items is None:
            return None
        
        # Step 3: Load data
        dataset = self.load_satellite_data(search, bbox_geometry)
        if dataset is None:
            return None
        
        # Step 4: Extract pixel timeseries
        df = self.extract_pixel_timeseries(dataset, n_samples, crop_type)
        if df is None:
            return None
        
        # Step 5: Save if requested
        if output_path:
            output_path = Path(output_path)
            df.to_csv(output_path, index=False)
            logger.info(f"💾 Saved {len(df)} records to {output_path}")
        
        return df
    
    def process_multiple_crops(self, 
                             crop_configs: List[Dict],
                             output_combined: Optional[Union[str, Path]] = None,
                             max_workers: int = 2) -> Optional[pd.DataFrame]:
        """
        Process multiple crop types with parallel processing.
        
        Args:
            crop_configs: List of dicts with keys: geojson_path, date_range, crop_type, n_samples
            output_combined: Path for combined output CSV
            max_workers: Maximum parallel workers
            
        Returns:
            Combined DataFrame or None if failed
        """
        logger.info(f"🚀 Processing {len(crop_configs)} crop types with {max_workers} workers")
        
        results = []
        
        # Use ThreadPoolExecutor for I/O bound operations
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_config = {
                executor.submit(
                    self.process_crop_data,
                    config['geojson_path'],
                    config['date_range'],
                    config['crop_type'],
                    config.get('n_samples', 300),
                    config.get('cloud_cover_max', 20.0)
                ): config for config in crop_configs
            }
            
            # Collect results
            for future in as_completed(future_to_config):
                config = future_to_config[future]
                try:
                    result = future.result()
                    if result is not None:
                        results.append(result)
                        logger.info(f"✅ Completed {config['crop_type']}")
                    else:
                        logger.error(f"❌ Failed to process {config['crop_type']}")
                except Exception as e:
                    logger.error(f"❌ Error processing {config['crop_type']}: {e}")
        
        if not results:
            logger.error("❌ No successful results")
            return None
        
        # Combine results
        logger.info("🔄 Combining results...")
        combined_df = pd.concat(results, ignore_index=True)
        
        # Shuffle data
        combined_df = combined_df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        # Summary statistics
        logger.info("📊 Final dataset summary:")
        logger.info(f"   Total records: {len(combined_df)}")
        logger.info(f"   Crop types: {combined_df['crop_type'].value_counts().to_dict()}")
        logger.info(f"   Date range: {combined_df['time'].min()} to {combined_df['time'].max()}")
        
        # Save combined results
        if output_combined:
            output_combined = Path(output_combined)
            combined_df.to_csv(output_combined, index=False)
            logger.info(f"💾 Saved combined dataset to {output_combined}")
        
        return combined_df


def main():
    """
    Example usage of the robust satellite data processor.
    """
    # Initialize processor
    processor = SatelliteDataProcessor()
    
    # Define crop configurations
    crop_configs = [
        {
            'geojson_path': "OIL_GEOJSON",
            'date_range': '2020-01-01/2020-12-31',
            'crop_type': 'oil',
            # 'n_samples': 300,
            'cloud_cover_max': 20.0
        },
        {
            'geojson_path': "COCOA_GEOJSON",
            'date_range': '2019-01-01/2022-12-31',
            'crop_type': 'cocoa',
            # 'n_samples': 300,
            'cloud_cover_max': 20.0
        }
    ]
    
    # Process all crops
    combined_df = processor.process_multiple_crops(
        crop_configs,
        output_combined='satellite_data_combined.csv'
    )
    
    if combined_df is not None:
        print("✅ Processing completed successfully!")
        print(f"Final dataset shape: {combined_df.shape}")
        print(f"Columns: {list(combined_df.columns)}")
    else:
        print("❌ Processing failed!")


if __name__ == "__main__":
    main()