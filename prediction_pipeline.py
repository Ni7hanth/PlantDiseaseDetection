"""
=============================================================
 Unified Prediction Pipeline
=============================================================
Pipeline:
  Image Input
      ↓
  Preprocess (resize, normalize for MobileNetV2)
      ↓
  CNN Prediction → disease class + confidence
      ↓
  Severity Estimation (area analysis + confidence score)
      ↓
  Grad-CAM Heatmap Generation
      ↓
  Progression Prediction
      ↓
  Treatment Recommendation (from Knowledge Base)
      ↓
  Structured Output (dict + CSV log)

Usage:
    from modules.prediction_pipeline import PlantDiseasePredictor
    predictor = PlantDiseasePredictor("models/plant_disease_model.keras")
    result = predictor.predict("path/to/leaf.jpg")
"""

import os, json, csv, datetime
import numpy as np
import tensorflow as tf
from PIL import Image

# Internal modules
from modules.disease_knowledge_base import get_disease_info
from modules.severity_xai import (
    estimate_infected_area,
    estimate_severity,
    predict_progression,
    generate_gradcam,
    overlay_heatmap,
    image_to_base64,
    generate_xai_explanation,
)

# ── Class Labels (PlantVillage 38 classes) ────────────────────────────────────
CLASS_NAMES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust',
    'Apple___healthy', 'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
    'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
    'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy',
]


class PlantDiseasePredictor:
    """
    End-to-end prediction pipeline for plant disease detection,
    severity estimation, XAI, and treatment recommendation.
    """

    IMG_SIZE = (224, 224)       # MobileNetV2 input size
    LOG_PATH = "outputs/predictions_log.csv"

    def __init__(self, model_path: str):
        print(f"Loading model from: {model_path}")
        self.model       = tf.keras.models.load_model(model_path)
        self.class_names = CLASS_NAMES
        os.makedirs("outputs", exist_ok=True)
        self._init_log()

    # ── Internal Helpers ──────────────────────────────────────────────────────

    def _init_log(self):
        """Create CSV log file with headers if it doesn't exist."""
        if not os.path.exists(self.LOG_PATH):
            with open(self.LOG_PATH, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "image_name", "predicted_class", "common_name",
                    "pathogen_type", "confidence_pct", "infected_area_pct",
                    "severity_level", "severity_score", "plant_type",
                    "is_healthy", "days_to_moderate", "days_to_severe",
                ])

    def _load_image(self, image_source) -> tuple:
        """
        Load image from path (str) or file-like object.
        Returns (pil_image, np_array_original, np_array_preprocessed)
        """
        if isinstance(image_source, str):
            pil_img = Image.open(image_source).convert("RGB")
        else:
            pil_img = Image.open(image_source).convert("RGB")

        # Original for display
        orig_arr = np.array(pil_img.resize((224, 224)))

        # Preprocessed for model
        resized  = pil_img.resize(self.IMG_SIZE)
        arr      = np.array(resized, dtype=np.float32)
        arr      = tf.keras.applications.mobilenet_v2.preprocess_input(arr)
        batch    = np.expand_dims(arr, axis=0)   # (1, 224, 224, 3)

        return pil_img, orig_arr, batch

    def _log_prediction(self, result: dict, image_name: str):
        """Append prediction to CSV log for Tableau export."""
        p    = result["progression"]
        with open(self.LOG_PATH, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                result["timestamp"],
                image_name,
                result["class_name"],
                result["common_name"],
                result["pathogen"],
                result["severity"]["confidence_pct"],
                result["severity"]["infected_area_pct"],
                result["severity"]["level"],
                result["severity"]["severity_score"],
                result["plant_type"],
                result["is_healthy"],
                p.get("days_to_next", ""),
                p.get("then_severe_in", ""),
            ])

    # ── Public API ────────────────────────────────────────────────────────────

    def predict(self, image_source, image_name: str = "image.jpg",
                generate_heatmap: bool = True) -> dict:
        """
        Full prediction pipeline.

        Args:
            image_source: file path (str) or file-like object
            image_name:   label for logging
            generate_heatmap: whether to compute Grad-CAM

        Returns:
            Structured result dictionary with all fields.
        """
        # 1. Load image
        pil_img, orig_arr, batch = self._load_image(image_source)

        # 2. Model prediction
        predictions  = self.model.predict(batch, verbose=0)
        pred_index   = int(np.argmax(predictions[0]))
        confidence   = float(predictions[0][pred_index])
        class_name   = self.class_names[pred_index]

        # 3. Parse class name
        parts      = class_name.split("___")
        plant_type = parts[0].replace("_", " ").replace(",", "").strip()
        is_healthy = "healthy" in class_name.lower()

        # 4. Knowledge base lookup
        kb_entry   = get_disease_info(class_name)
        common_name = kb_entry.get("common_name", class_name)
        pathogen    = kb_entry.get("pathogen") or "N/A"

        # 5. Severity estimation
        infected_area = estimate_infected_area(orig_arr) if not is_healthy else 0.0
        severity      = estimate_severity(confidence, infected_area, is_healthy)

        # 6. Progression prediction
        progression = predict_progression(
            severity["level"],
            kb_entry.get("progression_days", {})
        )

        # 7. Treatment recommendation
        treatment   = kb_entry.get("treatment", {})
        farming_tips = kb_entry.get("farming_tips", [])

        # 8. Grad-CAM (XAI)
        heatmap_b64 = None
        if generate_heatmap and not is_healthy:
            try:
                heatmap = generate_gradcam(self.model, batch, pred_index)
                overlay = overlay_heatmap(orig_arr, heatmap)
                heatmap_b64 = image_to_base64(overlay)
            except Exception as e:
                print(f"Heatmap generation skipped: {e}")

        # 9. XAI text explanation
        explanation = generate_xai_explanation(
            common_name, severity["level"],
            severity["infected_area_pct"], severity["confidence_pct"]
        )

        # 10. Assemble result
        result = {
            "timestamp":      datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "class_name":     class_name,
            "common_name":    common_name,
            "plant_type":     plant_type,
            "pathogen":       pathogen,
            "is_healthy":     is_healthy,
            "severity":       severity,
            "progression":    progression,
            "treatment":      treatment,
            "farming_tips":   farming_tips,
            "explanation":    explanation,
            "heatmap_base64": heatmap_b64,
            "top3_predictions": self._top3(predictions[0]),
        }

        # 11. Log to CSV
        self._log_prediction(result, image_name)

        return result

    def _top3(self, probs: np.ndarray) -> list:
        """Return top-3 predictions with class names and probabilities."""
        top3_idx = np.argsort(probs)[::-1][:3]
        return [
            {
                "class":      self.class_names[i],
                "common_name": get_disease_info(self.class_names[i]).get("common_name", ""),
                "probability": round(float(probs[i]) * 100, 2),
            }
            for i in top3_idx
        ]

    def format_output(self, result: dict) -> str:
        """Return a clean human-readable text summary."""
        sep = "=" * 60
        s   = result["severity"]
        p   = result["progression"]
        t   = result["treatment"]

        lines = [
            sep,
            "  PLANT DISEASE DETECTION — RESULT SUMMARY",
            sep,
            f"  Plant       : {result['plant_type']}",
            f"  Disease     : {result['common_name']}",
            f"  Pathogen    : {result['pathogen']}",
            f"  Confidence  : {s['confidence_pct']}%",
            "",
            "── SEVERITY ──────────────────────────────────────────────",
            f"  Level       : {s['level'].upper()}",
            f"  Infected Area: {s['infected_area_pct']}% of leaf",
            f"  Description : {s['description']}",
            "",
            "── PROGRESSION (if untreated) ────────────────────────────",
            f"  {p.get('forecast', 'N/A')}",
            f"  Urgency     : {p.get('urgency', '')}",
            "",
            "── TREATMENT ─────────────────────────────────────────────",
            "  Organic:",
        ]
        for tip in t.get("organic", []):
            lines.append(f"    • {tip}")
        lines.append("  Chemical:")
        for tip in t.get("chemical", []):
            lines.append(f"    • {tip}")
        lines.append("  Preventive:")
        for tip in t.get("preventive", []):
            lines.append(f"    • {tip}")

        lines += [
            "",
            "── FARMING TIPS ──────────────────────────────────────────",
        ]
        for tip in result.get("farming_tips", []):
            lines.append(f"    💡 {tip}")

        lines.append(sep)
        return "\n".join(lines)
