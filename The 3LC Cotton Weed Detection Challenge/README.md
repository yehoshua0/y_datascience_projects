# Cotton Weed Detection - Competition Dataset

## 🏆 Achievement: 9th Place on Private Leaderboard

**Final Score: 0.84962 mAP@50 (Public) | 0.83013 mAP@50 (Private)**

This repository contains the solution that achieved **9th place** in the 3LC Cotton Weed Detection Challenge. The approach focused on data-centric AI principles, leveraging the 3LC platform for systematic data quality improvement and experiment tracking.

### Competition Progression

| Iteration | CV Score (Local) | Public LB Score | Notes |
|-----------|------------------|-----------------|-------|
| Experiment 1 | 0.784 | 0.80563 | Baseline approach |
| Experiment 2 | 0.807 | 0.84565 | Data quality improvements |
| Experiment 3 | 0.804 | **0.84962** | **Best public LB score** |
| Experiment 4 | 0.820 | 0.84683 | Further tuning |

**Final Private Leaderboard: 0.83013 (9th Place)**

📓 **Solution Notebook**: [`3lc-cwdc-notebooka8d14588d3-code.ipynb`](3lc-cwdc-notebooka8d14588d3-code.ipynb)  
📝 **Technical Write-up**: [`WRITE-UP.md`](WRITE-UP.md) - Detailed methodology and insights

### Submission Documentation
- 📋 [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) - Complete submission requirements
- 🔧 [`KAGGLE_ENVIRONMENT.md`](KAGGLE_ENVIRONMENT.md) - Development environment details
- 📌 [`SUBMISSION_NOTES.md`](SUBMISSION_NOTES.md) - Context for judges

> **Note**: This solution was developed entirely on Kaggle notebooks. See [`KAGGLE_ENVIRONMENT.md`](KAGGLE_ENVIRONMENT.md) for details on why local 3LC project folders and dashboard screenshots are not applicable.

---

## Quick Start

### 📚 For Learning (Start Here)
1. **Download** this dataset from Kaggle
2. **Open** `cotton_weed_starter_notebook.ipynb`
3. **Follow** the step-by-step workflow to understand the concepts

### 🚀 For Fast Iteration (After Learning)
Once you understand the workflow, use the scripts for faster experimentation:
1. **Edit** `train.py` or `predict.py` configuration section
2. **Run** the script:
```bash
# Train model
python train.py

# Generate predictions
python predict.py

# Submit to Kaggle
# Upload submission.csv
```

## Overview

- **Task**: Multi-class weed detection (3 classes)
- **Format**: YOLO with normalized coordinates
- **Model**: YOLOv8n only (edge device constraints)
- **Focus**: Data-centric AI approach

## Dataset Structure

```
cotton_weed_competition_dataset/
├── train/                    # 542 training images + labels
├── val/                      # 133 validation images + labels
├── test/images/              # 170 test images (no labels)
├── dataset.yaml              # YOLO configuration
├── cotton_weed_starter_notebook.ipynb  # Interactive tutorial
├── train.py                  # Training script 
├── predict.py                # Prediction script
├── sample_submission.csv
└── README.md
```

## Classes

- **0**: Carpetweed - Mat-forming annual weed
- **1**: Morning Glory - Climbing vine
- **2**: Palmer Amaranth - Herbicide-resistant "super weed"

## Submission Format

CSV file with columns: `image_id,prediction_string`

**Prediction string**: Space-separated values for each detection:
```
class_id confidence x_center y_center width height
```

**Example**:
```csv
image_id,prediction_string
20190613_6062W_CM_29,0 0.95 0.5 0.3 0.2 0.4 1 0.87 0.7 0.6 0.15 0.25
20200624_iPhone6_SY_132,no box
```

**Requirements**:
- Column names must be lowercase
- Coordinates normalized to [0, 1]
- Use `no box` for images with no detections

## Competition Rules

### ✅ Allowed
- YOLOv8n model only (REQUIRED)
- Hyperparameter tuning and augmentation
- Data corrections and improvements
- 3 submissions per day

### ❌ Prohibited
- Larger models (YOLOv8s, YOLOv8m, etc.)
- Model ensembles or stacking
- Test-time augmentation (TTA)

### Why These Constraints?

Real edge devices have fixed computational, power, and thermal budgets. This competition simulates production constraints where hardware is deployed first, and improvements must come from **data-centric AI** strategies rather than model architecture changes.

---

## Getting Started

### Prerequisites

```bash
# Install core dependencies
pip install -r requirements.txt
pip install 3lc ultralytics tlc-ultralytics pandas

# Authenticate with 3LC
3lc login <your_api_key>

# Start 3LC service (keep running in separate terminal)
3lc service
```

**System Requirements:**
- Python 3.11+
- PyTorch 2.6.0+ with CUDA support (recommended)
- GPU: NVIDIA T4 or better (for training)
- 16GB+ RAM

### Two Ways to Work

#### Option 1: Solution Notebook (Recommended)
**Best for:** Understanding the winning approach, reproducing results

Use [`3lc-cwdc-notebooka8d14588d3-code.ipynb`](3lc-cwdc-notebooka8d14588d3-code.ipynb):
- Complete winning solution implementation
- Data registration with 3LC
- Training with experiment tracking
- Prediction generation and submission formatting

**Expected Runtime:** ~25-30 minutes on Kaggle T4 GPU

#### Option 2: Starter Notebook (For Learning)
**Best for:** First-time users, learning concepts


Start with `cotton_weed_starter_notebook.ipynb`:
- Interactive cells with explanations
- Visual examples and analysis
- Step-by-step guidance through the full pipeline
- Learn 3LC Dashboard workflows

**Workflow (3 Phases):**
1. **Setup** (30 min): Install dependencies, register dataset with 3LC
2. **Baseline** (60 min): Train YOLOv8n, generate predictions, submit
3. **Iterate** (ongoing): Analyze errors → Fix data → Retrain → Improve

#### Option 2: Scripts (Best for Iteration)
**Best for:** Fast experimentation, quick iterations, automation

Use `train.py` and `predict.py` after learning the concepts. Both scripts use **edit-in-place configuration**:

**Training:**
1. Open `train.py` in your editor
2. Edit the CONFIGURATION section:
```python
# 3LC Table URLs (get from Dashboard)
TRAIN_TABLE_URL = "your/train/table/url"
VAL_TABLE_URL = "your/val/table/url"

# Run configuration
RUN_NAME = "baseline_v1"  # Change for each experiment
EPOCHS = 30  # Number of training epochs
BATCH_SIZE = 16  # Batch size
USE_AUGMENTATION = False  # Set to True to enable augmentation
```
3. Run the script:
```bash
python train.py
```

**Prediction:**
1. Open `predict.py` in your editor
2. Edit the CONFIGURATION section:
```python
# Model weights path (from training)
MODEL_WEIGHTS = "runs/detect/baseline_v1/weights/best.pt"

# Inference settings
CONFIDENCE_THRESHOLD = 0  # Adjust as needed
OUTPUT_CSV = "submission.csv"  # Output file name
```
3. Run the script:
```bash
python predict.py
```

**No command-line arguments to remember!** Just edit the configuration and run.

### Which Should I Use?

| Scenario | Use |
|----------|-----|
| First time with competition | **Notebook** - Learn concepts |
| Understanding 3LC Dashboard | **Notebook** - Visual guides |
| Rapid training iterations | **Scripts** - Faster workflow |
| Testing hyperparameters | **Scripts** - Edit & run |
| Batch experiments | **Scripts** - Automation friendly |
| Team collaboration | **Both** - Notebook for onboarding, scripts for work |

**💡 Recommended:** Start with the notebook, switch to scripts once comfortable!

## Data-Centric AI Approach

Since the model is fixed, **all improvements come from data**:

1. Train baseline model
2. Use 3LC Dashboard to identify issues (missing labels, mislabels, bbox errors)
3. Fix data problems
4. Retrain with improved data
5. Submit and repeat

This mirrors real production AI where model capacity is constrained.

## Performance Results

### Final Metrics (9th Place Solution)

| Metric | Score |
|--------|-------|
| **Public Leaderboard mAP@50** | **0.84962** |
| **Private Leaderboard mAP@50** | **0.83013** |
| **Ranking** | **9th Place** |
| Local Validation mAP@50 | 80.3% |
| Training mAP@50 | 97.0% |

### Per-Class Performance (Validation Set)

| Class | Precision | Recall | mAP@50 | Instances |
|-------|-----------|--------|--------|-----------|
| **All Classes** | 0.836 | 0.678 | **0.803** | 269 |
| Carpetweed | 0.803 | 0.554 | 0.716 | 110 |
| Morning Glory | 0.899 | 0.829 | 0.890 | 70 |
| Palmer Amaranth | 0.808 | 0.652 | 0.802 | 89 |

### Expected Performance Ranges

| Approach | Local (YOLO) | Kaggle (COCO) |
|----------|--------------|---------------|
| Baseline | 55-65% | 30-45% |
| Optimized | 70-85% | 45-65% |
| **This Solution** | **~85%** | **83.013%** |

**Note**: Kaggle scores are typically 10-15% lower because COCO evaluation is stricter than YOLO's native validation.

## Common Issues

| Issue | Solution |
|-------|----------|
| Kaggle score much lower than local | Normal! COCO evaluation is stricter |
| CSV submission rejected | Check lowercase column names: `image_id,prediction_string` |
| Invalid coordinate range | Ensure all coordinates are in [0, 1] |
| Model not improving | Use 3LC Dashboard for error analysis - it's likely a data issue |

## Submission Guidelines

- **3 submissions per day** maximum
- Select **up to 2 final submissions** for judging
- Leaderboard: **50% public, 50% private** (prevents overfitting)
- Evaluation: **mAP@0.5** using COCO methodology

## Dataset Details

- **Training**: 542 images, ~2,000 weed instances
- **Validation**: 133 images, ~500 weed instances
- **Test**: 170 images (labels withheld)
- **Resolution**: 1024×768 to 4032×3024 pixels
- **Quality**: Intentional label imperfections (production reality)

## Script Features

Both `train.py` and `predict.py` are production-quality scripts with:

✅ **Edit-in-place configuration** - Modify settings at top of file  
✅ **Clear structure** - All options in one CONFIGURATION section  
✅ **Validation** - Checks formats and catches errors early  
✅ **Progress tracking** - Clear status messages throughout  
✅ **Safe operations** - Creates backups instead of deleting  
✅ **Modular code** - Easy to customize if needed  


## Resources

- **3LC Documentation**: https://docs.3lc.ai/
- **YOLOv8 Guide**: https://docs.ultralytics.com/
- **Competition Forum**: Ask questions, share insights

## Acknowledgments

Special thanks to:
- **3LC Team** for organizing this competition and providing an excellent data-centric AI platform
- **Kaggle** for hosting the competition and providing free GPU resources
- **All Participants** for making this a great learning experience

---

**Ready to begin?** Open `cotton_weed_starter_notebook.ipynb` and follow the workflow! 🌾