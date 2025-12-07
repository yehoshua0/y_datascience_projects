# Kaggle Environment Note

This solution was developed entirely on **Kaggle notebooks** using cloud GPU resources.

## Development Environment

- **Platform**: Kaggle Notebooks
- **GPU**: NVIDIA T4 x2
- **Python**: 3.11
- **3LC Integration**: Installed via `pip install 3lc`
- **Data**: Cotton Weed Competition Dataset from Kaggle

## Why No Local 3LC Project Folder?

All work was performed in Kaggle's cloud environment, not on a local machine. The notebook itself serves as the complete record of:

- **3LC Table Registration**: Dataset versioning and management
- **Training Runs**: Experiment tracking with 3LC Settings
- **Metrics Collection**: Performance monitoring and validation
- **Iterative Improvements**: Data quality refinement cycles

## Evidence of 3LC Usage

The notebook demonstrates 3LC integration throughout:

1. **Data Registration** (Cells 6-7): Creating 3LC Tables from YOLO format
2. **Training Configuration** (Cell 11): Using `tlc_ultralytics.YOLO` with `Settings`
3. **Experiment Tracking**: Run names, descriptions, and metrics
4. **Output Logs**: Training progress and validation results

## Reproducibility

To reproduce this solution:

1. Upload `3lc-cwdc-notebook-code.ipynb` to Kaggle
2. Enable GPU accelerator (T4 recommended)
3. Install dependencies: `!pip install 3lc ultralytics tlc-ultralytics`
4. Authenticate with 3LC: `!3lc login <api_key>`
5. Run all cells sequentially
6. Results will match the submitted scores

## Alternative to Dashboard Screenshots

Since the work was done in Kaggle's cloud environment, we provide:

- **Notebook Output Cells**: Complete training logs and metrics
- **Training Logs File**: `training_logs.txt` with detailed progress
- **Performance Tables**: Results documented in WRITE-UP.md
- **Submission Files**: Final predictions and validation results

The notebook outputs provide the same information that dashboard screenshots would show, including training curves, validation metrics, and experiment comparisons.

---

**Note**: This approach is common for Kaggle competitions where participants work entirely in cloud notebooks rather than local environments.
