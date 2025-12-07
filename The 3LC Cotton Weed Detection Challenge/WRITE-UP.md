# Cotton Weed Detection Challenge - Solution Write-up

## 🏆 Competition Result

**Final Ranking: 9th Place on Private Leaderboard**  
**Final Score: 0.84962 mAP@50 (Public) | 0.83013 mAP@50 (Private)**

---

## Competition Progression

During the competition, multiple experiments were conducted with iterative improvements. Below are the key submissions on the **Public Leaderboard**:

| Iteration | CV Score (Local) | Public LB Score | Notes |
|-----------|------------------|-----------------|-------|
| Experiment 1 | 0.784 | 0.80563 | Baseline approach |
| Experiment 2 | 0.807 | 0.84565 | Data quality improvements |
| Experiment 3 | 0.804 | **0.84962** | **Best public LB score** |
| Experiment 4 | 0.820 | 0.84683 | Further tuning |

**Final Private Leaderboard Score: 0.83013 (9th Place)**

> **Note**: CV (Cross-Validation) scores are local validation metrics, while LB (Leaderboard) scores are evaluated on Kaggle's test set using COCO mAP@0.5 methodology.

---

## Executive Summary

This document outlines the data-centric AI approach that achieved 9th place in the 3LC Cotton Weed Detection Challenge. The solution leverages YOLOv8n (the only permitted model) combined with systematic data quality improvement using the 3LC platform for dataset versioning, experiment tracking, and error analysis.

**Key Success Factors:**
- Data-centric methodology focusing on quality over model complexity
- Systematic use of 3LC Dashboard for error analysis and data refinement
- Strategic hyperparameter tuning within competition constraints
- Iterative improvement cycle: train → analyze → fix data → retrain

---

## Challenge Overview

### Objective
Detect three weed species in cotton fields:
- **Class 0**: Carpetweed (mat-forming annual weed)
- **Class 1**: Morning Glory (climbing vine)
- **Class 2**: Palmer Amaranth (herbicide-resistant "super weed")

### Constraints
- **Model**: YOLOv8n only (fixed architecture, ~3M parameters)
- **No Ensembles**: Single model submissions only
- **No TTA**: Test-time augmentation prohibited
- **Evaluation**: mAP@0.5 using COCO methodology
- **Submissions**: 3 per day maximum

### Dataset
- **Training**: 542 images (~2,000 weed instances)
- **Validation**: 133 images (~500 weed instances)
- **Test**: 170 images (labels withheld)
- **Format**: YOLO format with normalized coordinates [0, 1]

---

## Solution Approach

### 1. Data-Centric AI Philosophy

Given the fixed model architecture constraint, **all performance improvements came from data quality**:

1. **Baseline Training** → Establish performance benchmark
2. **Error Analysis** → Use 3LC Dashboard to identify systematic issues
3. **Data Refinement** → Fix labeling errors, missing annotations, bbox inaccuracies
4. **Iterative Retraining** → Validate improvements and repeat

This mirrors real-world production AI where model capacity is often constrained by deployment requirements (edge devices, latency, cost).

### 2. Technical Implementation

#### Environment Setup
```python
# Core dependencies
!pip install 3lc
!pip install ultralytics
!pip install tlc-ultralytics

# 3LC authentication
!3lc login <api-key>
```

#### Dataset Registration with 3LC

The solution uses 3LC's data versioning system to track dataset improvements:

```python
import tlc

# Register YOLO dataset with 3LC
train_table = tlc.Table.from_yolo(
    dataset_yaml_file="dataset_fixed.yaml",
    split="train",
    task="detect",
    dataset_name="cotton_weed_competition_dataset",
    project_name="kaggle_cotton_weed_detection",
    table_name="cotton_weed_competition_dataset-train1"
)

val_table = tlc.Table.from_yolo(
    dataset_yaml_file="dataset_fixed.yaml",
    split="val",
    task="detect",
    dataset_name="cotton_weed_competition_dataset",
    project_name="kaggle_cotton_weed_detection",
    table_name="cotton_weed_competition_dataset-val1"
)
```

**Benefits:**
- Version control for datasets (track changes over iterations)
- Automatic integration with 3LC Dashboard for visualization
- Seamless experiment tracking and comparison

#### Model Training Configuration

```python
from tlc_ultralytics import YOLO, Settings

# Training configuration
RUN_NAME = "yolov8n_baseline"
EPOCHS = 30
BATCH_SIZE = 16
IMAGE_SIZE = 640  # Competition requirement
DEVICE = 0  # GPU

# 3LC experiment tracking
settings = Settings(
    project_name="kaggle_cotton_weed_detection",
    run_name=RUN_NAME,
    run_description="Baseline YOLOv8n with default hyperparameters",
    image_embeddings_dim=2
)

# Load pretrained YOLOv8n
model = YOLO("yolov8n.pt")

# Train with 3LC integration
results = model.train(
    tables={"train": train_table, "val": val_table},
    name=RUN_NAME,
    epochs=EPOCHS,
    imgsz=IMAGE_SIZE,
    batch=BATCH_SIZE,
    device=DEVICE,
    workers=4,
    settings=settings,
    val=True
)
```

**Key Parameters:**
- **Model**: YOLOv8n (COCO pretrained weights)
- **Input Size**: 640×640 (competition standard)
- **Batch Size**: 16 (optimized for Kaggle T4 GPU)
- **Epochs**: 30 (baseline), adjusted in later iterations
- **Device**: Kaggle GPU T4×2

#### Prediction Generation

```python
# Generate predictions on test set
test_results = model.predict(
    source="test/images",
    save=False,
    save_txt=True,
    save_conf=True,
    conf=0,  # No confidence threshold filtering
    imgsz=640,
    project="predictions",
    name="predictions"
)
```

#### Kaggle Submission Format

The solution includes robust CSV generation with proper format validation:

```python
# Convert YOLO predictions to Kaggle format
# YOLO format: class xc yc w h conf
# Kaggle format: class conf xc yc w h

submission_data = []
for image_id in test_images:
    pred_file = f"predictions/labels/{image_id}.txt"
    
    if pred_file exists and has content:
        boxes = []
        for line in pred_file:
            class_id, xc, yc, w, h, conf = line.split()
            # Reorder: move confidence to second position
            box = f"{class_id} {conf} {xc} {yc} {w} {h}"
            boxes.append(box)
        
        prediction_string = " ".join(boxes)
    else:
        prediction_string = "no box"
    
    submission_data.append({
        "image_id": image_id,
        "prediction_string": prediction_string
    })

# Save submission
pd.DataFrame(submission_data).to_csv("submission.csv", index=False)
```

---

## 3. Iterative Improvement Strategy

### Baseline Performance
- **Initial mAP@50**: ~45-55% (typical for out-of-the-box YOLOv8n)
- **Identified Issues**:
  - Missing annotations (false negatives)
  - Mislabeled instances (class confusion)
  - Inaccurate bounding boxes (poor localization)
  - Class imbalance

### Data Quality Improvements

Using the **3LC Dashboard**, the following systematic improvements were made:

1. **Error Pattern Analysis**
   - Reviewed false positives and false negatives
   - Identified systematic labeling errors
   - Found missing annotations in challenging cases

2. **Data Corrections**
   - Fixed mislabeled instances
   - Added missing bounding boxes
   - Corrected bbox coordinates for better localization
   - Resolved class confusion cases

3. **Augmentation Strategy**
   - Mosaic augmentation (1.0) for scale variation
   - Copy-paste (0.1) for occlusion handling
   - Mixup (0.05) for generalization
   - HSV augmentation for lighting robustness

### Hyperparameter Tuning

Within competition constraints, the following were optimized:

```python
# Final optimized configuration
model.train(
    tables=tables,
    epochs=30,
    imgsz=640,
    batch=16,
    # Augmentation
    mosaic=1.0,
    copy_paste=0.1,
    mixup=0.05,
    hsv_h=0.015,
    hsv_s=0.7,
    hsv_v=0.4,
    degrees=10,
    translate=0.1,
    scale=0.5,
    fliplr=0.5,
    # Training dynamics
    lr0=0.01,
    warmup_epochs=3,
    patience=20
)
```

---

## 4. Results and Performance

### Final Metrics

| Metric | Score |
|--------|-------|
| **Public Leaderboard mAP@50** | **0.84962** |
| **Private Leaderboard mAP@50** | **0.83013** |
| **Ranking** | **9th Place** |
| Local Validation mAP@50 | 80.3% |
| Training mAP@50 | 97.0% |

### Training Performance (50 epochs, 0.748 hours)

**Validation Set Results (133 images, 269 instances):**

| Class | Precision | Recall | mAP@50 | mAP@50-95 | Instances |
|-------|-----------|--------|--------|-----------|-----------|
| **All Classes** | 0.836 | 0.678 | **0.803** | 0.629 | 269 |
| Carpetweed | 0.803 | 0.554 | 0.716 | 0.507 | 110 |
| Morning Glory | 0.899 | 0.829 | 0.890 | 0.730 | 70 |
| Palmer Amaranth | 0.808 | 0.652 | 0.802 | 0.651 | 89 |

**Training Set Results (542 images, 969 instances):**

| Class | Precision | Recall | mAP@50 | mAP@50-95 | Instances |
|-------|-----------|--------|--------|-----------|-----------|
| **All Classes** | 0.960 | 0.912 | **0.970** | 0.870 | 969 |
| Carpetweed | 0.948 | 0.854 | 0.950 | 0.819 | 391 |
| Morning Glory | 0.973 | 0.927 | 0.978 | 0.907 | 308 |
| Palmer Amaranth | 0.960 | 0.956 | 0.984 | 0.884 | 270 |

**Inference Speed:** 0.2ms preprocess + 3.2ms inference + 1.2ms postprocess per image


### Key Success Factors

1. **Data Quality Over Quantity**: Systematic error correction yielded significant gains
2. **3LC Platform**: Dashboard visualization enabled efficient error analysis
3. **Iterative Refinement**: Multiple train-analyze-fix cycles
4. **Strategic Augmentation**: Targeted augmentations for real-world variations
5. **Hyperparameter Optimization**: Fine-tuning within constraints

---

## 5. Tools and Technologies

### Core Stack
- **Model**: YOLOv8n (Ultralytics)
- **Data Platform**: 3LC (dataset versioning, experiment tracking, error analysis)
- **Framework**: PyTorch 2.6.0
- **Hardware**: Kaggle GPU T4×2
- **Language**: Python 3.11

### Key Libraries
```
3lc==2.20.1
ultralytics==latest
tlc-ultralytics==latest
torch==2.6.0+cu124
torchvision==0.21.0+cu124
```

---

## 6. Lessons Learned

### What Worked Well
✅ **Data-centric approach**: Fixing data quality issues had the highest ROI  
✅ **3LC Dashboard**: Visual error analysis was invaluable for identifying patterns  
✅ **Systematic iteration**: Structured train-analyze-fix cycles prevented random experimentation  
✅ **Augmentation**: Mosaic and copy-paste significantly improved robustness  

### Challenges Faced
⚠️ **Model Constraint**: YOLOv8n capacity limits performance ceiling  
⚠️ **Small Dataset**: 542 training images required careful augmentation  
⚠️ **Class Imbalance**: Some weed types had fewer examples  
⚠️ **Label Quality**: Initial dataset had intentional imperfections  

### Future Improvements
If the competition allowed:
- Larger model (YOLOv8s/m) would likely improve performance
- Test-time augmentation (TTA) for ensemble-like predictions
- Active learning to prioritize which samples to label/fix
- Semi-supervised learning with unlabeled data

---

## 7. Reproducibility

### Running the Solution

1. **Setup Environment**
   ```bash
   pip install 3lc ultralytics tlc-ultralytics
   3lc login <your-api-key>
   ```

2. **Run the Notebook**
   - Open `3lc-cwdc-notebook-code.ipynb`
   - Execute cells sequentially
   - Monitor training in 3LC Dashboard

3. **Generate Submission**
   - Predictions saved to `predictions/labels/`
   - Submission CSV: `submission.csv`
   - Upload to Kaggle

### Expected Runtime
- **Environment Setup**: ~5 minutes
- **Dataset Registration**: ~2 minutes
- **Training (30 epochs)**: ~15-20 minutes on Kaggle T4
- **Inference**: ~2 minutes
- **Total**: ~25-30 minutes

---

## 8. Conclusion

This solution demonstrates that **data quality is paramount** when model architecture is constrained. By leveraging the 3LC platform for systematic data improvement and experiment tracking, we achieved **9th place (0.83013 mAP@50)** using only the smallest YOLOv8 variant.

The approach is directly applicable to real-world production scenarios where:
- Model size is constrained (edge devices, mobile, embedded systems)
- Inference latency matters
- Data quality issues are common
- Iterative improvement is necessary

**Key Takeaway**: In data-centric AI, the path to better performance is through better data, not just better models.

---

## References

- **3LC Documentation**: https://docs.3lc.ai/
- **YOLOv8 Guide**: https://docs.ultralytics.com/
- **Competition**: The 3LC Cotton Weed Detection Challenge
- **Solution Notebook**: `3lc-cwdc-notebook-code.ipynb`

---

## Acknowledgments

I would like to express my sincere gratitude to:

- **3LC Team** for organizing this excellent competition and providing the powerful 3LC platform for data-centric AI development
- **Kaggle** for hosting the competition and providing free GPU resources that made this work possible
- **Competition Organizers** for designing a challenging, real-world problem that emphasizes data quality over model complexity
- **Ultralytics** for the YOLOv8 framework
- **All Participants** for the engaging competition and shared learning experience

This competition was an invaluable learning experience in data-centric AI methodology and the importance of systematic data quality improvement.

---

**Author**: ATD  
**Date**: December 2025  
**Competition**: 3LC Cotton Weed Detection Challenge  
**Result**: 9th Place (0.83013 mAP@50)
