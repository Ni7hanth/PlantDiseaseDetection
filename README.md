# Plant Disease Detection System
### Final Year Project — Complete Technical Report

---

## Project Overview

| Item | Detail |
|------|--------|
| **Title** | Plant Disease Detection System for Sustainable Agriculture |
| **Objective** | Detect plant diseases from leaf images using Deep Learning, estimate severity, and recommend treatments |
| **Dataset** | PlantVillage — 87,000 images, 38 classes, 14 crop types |
| **Model** | MobileNetV2 (Transfer Learning) + Custom Classification Head |
| **Accuracy** | ~96% validation accuracy |
| **UI** | Streamlit web application |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   INPUT: Leaf Image                     │
└──────────────────────────┬──────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              PREPROCESSING PIPELINE                     │
│  • Resize to 224×224 pixels                            │
│  • MobileNetV2 normalization (pixel values -1 to +1)   │
│  • Data augmentation (training only)                    │
└──────────────────────────┬──────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│           MOBILENETV2 + CLASSIFICATION HEAD             │
│  • MobileNetV2 backbone (pre-trained on ImageNet)       │
│  • GlobalAveragePooling → Dense(512) → Dense(256)       │
│  • Softmax output: 38 disease classes                   │
└──────────────────────────┬──────────────────────────────┘
                           ↓
           ┌───────────────┼───────────────┐
           ↓               ↓               ↓
    ┌──────────┐    ┌────────────┐   ┌──────────────┐
    │ SEVERITY │    │  GRAD-CAM  │   │  KNOWLEDGE   │
    │ESTIMATOR │    │ HEATMAP XAI│   │     BASE     │
    │(novelty) │    │            │   │(treatments)  │
    └──────────┘    └────────────┘   └──────────────┘
           ↓               ↓               ↓
┌─────────────────────────────────────────────────────────┐
│                  STRUCTURED OUTPUT                      │
│  • Disease name + confidence                           │
│  • Severity level + infected area %                    │
│  • Progression forecast (days)                         │
│  • Treatment plan (organic / chemical / preventive)    │
│  • Heatmap overlay image                               │
│  • CSV log for Tableau                                 │
└─────────────────────────────────────────────────────────┘
```

---

## Model Improvements (Over Baseline)

### Baseline (Your Original Model)
- Custom CNN from scratch: 5 conv blocks → Dense(1500) → softmax
- Image size: 128×128
- 10 epochs, fixed learning rate 0.0001
- No data augmentation
- ~96% validation accuracy

### Enhanced Model
| Aspect | Baseline | Enhanced |
|--------|----------|---------|
| Architecture | Custom CNN | MobileNetV2 Transfer Learning |
| Image Size | 128×128 | 224×224 (native for MobileNetV2) |
| Parameters | ~15M | ~3.5M (more efficient) |
| Training | 10 fixed epochs | 2-phase + early stopping |
| Augmentation | None | Flip, rotate, zoom, brightness |
| LR Strategy | Fixed | ReduceLROnPlateau scheduler |
| Generalization | Good | Better (ImageNet pretrained features) |

**Why MobileNetV2?**
- Pre-trained on 1.2M ImageNet images — already knows edges, textures, shapes
- Inverted residual blocks are efficient and accurate
- 5-10× fewer parameters than VGG/ResNet — runs on CPU in deployment

---

## Novelty Feature: Disease Progression & Treatment System

### How It Works (Step-by-Step for Viva)

**Step 1 — Disease Detection**
The CNN classifies the leaf into one of 38 disease classes with a confidence score (0-100%).

**Step 2 — Infected Area Estimation**
- The leaf image is converted to HSV color space
- Brown, yellow-brown, and dark pixel regions are segmented using color thresholds
- These correspond to diseased tissue vs. healthy green tissue
- Result: "X% of leaf area is infected"

**Step 3 — Severity Classification**
```
severity_score = (0.6 × infected_area_ratio) + (0.4 × (1 - model_confidence))

if severity_score < 0.25:  → EARLY
elif severity_score < 0.55: → MODERATE
else:                       → SEVERE
```

**Step 4 — Progression Forecast**
Each disease in the knowledge base has disease-specific progression timelines:
```python
"Tomato Late Blight": {
    "early_to_moderate": 3 days,
    "moderate_to_severe": 4 days
}
```
The system tells the farmer: *"If untreated, this will reach SEVERE stage in 7 days."*

**Step 5 — Treatment Recommendation**
The knowledge base stores structured treatments for all 38 classes:
- **Organic**: Natural/bio pesticides, cultural methods
- **Chemical**: Fungicide/bactericide with dosage
- **Preventive**: Crop rotation, resistant varieties, irrigation changes

---

## Explainable AI (Grad-CAM)

### What is Grad-CAM?
Gradient-weighted Class Activation Mapping — a technique that shows **which pixels** most influenced the model's prediction.

### How It Works
1. Forward pass: image → model → prediction
2. Backward pass: compute gradients of the predicted class score w.r.t. the last convolutional feature map
3. Pool the gradients spatially → weight each feature map channel
4. Create weighted sum of feature maps → resize to original image size
5. Overlay as a heatmap: **RED = model was most focused here**

### Why This Matters
- **Transparency**: Farmer/expert can verify if model is looking at the disease lesion (correct) or background (incorrect)
- **Trust**: Shows the reasoning, not just the answer
- **Debugging**: Helps identify model failures

---

## Tableau Dashboard Guide

### Required CSV Columns
| Column | Type | Description |
|--------|------|-------------|
| timestamp | DateTime | When prediction was made |
| common_name | String | Disease name |
| plant_type | String | Crop type |
| severity_level | String | early/moderate/severe/healthy |
| confidence_pct | Float | Model confidence % |
| infected_area_pct | Float | % leaf infected |
| is_healthy | Boolean | Disease-free flag |
| region | String | Geographic area |
| days_to_severe | Integer | Urgency metric |

### Calculated Fields
```
Disease Count:      COUNT([Predicted Class])
Severity Order:     IF [Severity Level]="severe" THEN 3
                    ELSEIF [Severity Level]="moderate" THEN 2
                    ELSE 1 END
Health Rate %:      SUM(IF [Is Healthy]="True" THEN 1 ELSE 0 END)
                    / COUNT([Image Name]) * 100
Accuracy %:         AVG([Confidence Pct])
```

### Dashboard Sheets
1. **Disease Distribution** — Horizontal bar chart (most common diseases)
2. **Severity Breakdown** — Pie/donut chart (early/moderate/severe split)
3. **Accuracy Over Time** — Line chart (monthly average confidence)
4. **Region-wise Heatmap** — Cross-tab: Region × Disease × Count
5. **Infection vs Confidence** — Scatter plot

---

## Future Enhancements

| Feature | Description | Priority |
|---------|-------------|----------|
| Mobile App | Flutter/React Native app with camera integration | High |
| REST API | FastAPI backend for third-party integration | High |
| Real-time Detection | Live webcam/drone feed processing | Medium |
| IoT Integration | Soil moisture + temperature sensors for context | Medium |
| GPS Disease Maps | Regional disease spread visualization | Medium |
| Weather Correlation | Integrate weather data to predict outbreak risk | High |
| LLM Chatbot | Conversational disease Q&A for farmers | Low |
| Satellite Imagery | Detect crop stress at field level | Future |

---

## File Structure

```
plant_disease_system/
├── app.py                          ← Main Streamlit web application
├── requirements.txt                ← Python dependencies
├── tableau_export.py               ← Tableau data generator + guide
│
├── modules/
│   ├── model_training.py           ← Enhanced CNN training (MobileNetV2)
│   ├── disease_knowledge_base.py   ← Treatment & progression database
│   ├── severity_xai.py             ← Severity estimator + Grad-CAM XAI
│   └── prediction_pipeline.py      ← End-to-end prediction pipeline
│
├── models/
│   └── plant_disease_model.keras   ← Trained model (generated by training)
│
└── outputs/
    ├── predictions_log.csv         ← Auto-generated prediction history
    ├── sample_data.csv             ← Demo data for Tableau
    └── tableau_summary.csv         ← Aggregated summary data
```

---

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Generate sample data for Tableau
python tableau_export.py

# 3. Launch web application
streamlit run app.py
```

---

