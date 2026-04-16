"""
=============================================================
 Plant Disease Detection System — Enhanced Streamlit App
=============================================================
Features:
  ✅ Disease Detection (38 classes, MobileNetV2)
  ✅ Severity Estimation (Early / Moderate / Severe)
  ✅ Grad-CAM Explainability (visual heatmap)
  ✅ Progression Forecast (days to next stage)
  ✅ Treatment Recommendation (organic / chemical / preventive)
  ✅ Farming Tips
  ✅ CSV Export for Tableau Dashboard
  ✅ Top-3 predictions display

Run:  streamlit run app.py
"""

import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import json, os, base64
from PIL import Image
import io

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Plant Disease Detection System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #1a5c2a, #2d8a4a);
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
.severity-early    { background:#fff3cd; border-left:5px solid #ffc107; padding:12px; border-radius:6px; }
.severity-moderate { background:#ffe0cc; border-left:5px solid #fd7e14; padding:12px; border-radius:6px; }
.severity-severe   { background:#f8d7da; border-left:5px solid #dc3545; padding:12px; border-radius:6px; }
.severity-healthy  { background:#d4edda; border-left:5px solid #28a745; padding:12px; border-radius:6px; }
.treatment-card    { background:#f0f7ff; border:1px solid #bee3f8; border-radius:8px; padding:14px; margin:6px 0; }
.metric-card       { background:#ffffff; border-radius:10px; padding:16px; box-shadow:0 2px 8px rgba(0,0,0,0.1); text-align:center; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🌿 Navigation")
page = st.sidebar.radio("Select Page", [
    "🏠 Home",
    "🔍 Disease Detection",
    "📊 Analytics Dashboard",
    "ℹ️ About",
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Quick Stats")
log_path = "outputs/predictions_log.csv"
if os.path.exists(log_path):
    df_log = pd.read_csv(log_path)
    st.sidebar.metric("Total Scans", len(df_log))
    st.sidebar.metric("Diseases Found",
                       len(df_log[df_log["is_healthy"] == False]))
else:
    st.sidebar.metric("Total Scans", 0)

# ── Model Loading ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model_path = "models/plant_disease_model.keras"
    if not os.path.exists(model_path):
        # Fallback: try baseline model path
        model_path = "trained_plant_disease_model.keras"
    return tf.keras.models.load_model(model_path)

@st.cache_resource
def load_predictor():
    from modules.prediction_pipeline import PlantDiseasePredictor
    model_path = "models/plant_disease_model.keras"
    if not os.path.exists(model_path):
        model_path = "trained_plant_disease_model.keras"
    return PlantDiseasePredictor(model_path)


# ── HOME PAGE ─────────────────────────────────────────────────────────────────
if page == "🏠 Home":
    st.markdown("""
    <div class="main-header">
        <h1>🌿 Plant Disease Detection System</h1>
        <p>AI-Powered Detection · Severity Assessment · Treatment Recommendations</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h2>38</h2><p>Disease Classes</p></div>',
                    unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h2>96%+</h2><p>Model Accuracy</p></div>',
                    unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h2>14</h2><p>Crop Types</p></div>',
                    unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h2>3</h2><p>Severity Levels</p></div>',
                    unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚀 Key Features")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🔬 Core AI Features**
        - MobileNetV2 Transfer Learning model
        - Real-time disease classification (38 classes)
        - Top-3 prediction confidence display
        - Grad-CAM visual explanation heatmap

        **📈 Novelty Feature**
        - Disease severity: Early / Moderate / Severe
        - Progression timeline: days to next stage
        - Urgency-based action alerts
        """)
    with col2:
        st.markdown("""
        **💊 Recommendation Engine**
        - Organic treatment options
        - Chemical treatment with dosage
        - Preventive measures
        - Crop-specific farming tips

        **📊 Analytics**
        - CSV export for Tableau dashboard
        - Disease distribution analytics
        - Severity trend tracking
        """)

    st.markdown("---")
    st.info("👈 Select **Disease Detection** from the sidebar to analyze a leaf image.")


# ── DETECTION PAGE ────────────────────────────────────────────────────────────
elif page == "🔍 Disease Detection":
    st.markdown("## 🔍 Disease Detection & Analysis")
    st.markdown("Upload a clear photo of a plant leaf for instant AI diagnosis.")

    uploaded_file = st.file_uploader(
        "📷 Choose a leaf image (JPG / PNG)",
        type=["jpg", "jpeg", "png"],
        help="Best results: clear, well-lit photo of a single leaf against neutral background"
    )

    if uploaded_file:
        col_img, col_result = st.columns([1, 1])

        with col_img:
            st.markdown("### 📸 Uploaded Image")
            pil_img = Image.open(uploaded_file).convert("RGB")
            st.image(pil_img, caption="Input Leaf Image", use_column_width=True)

        with col_result:
            st.markdown("### ⚙️ Analysis")
            with st.spinner("🔄 Running AI analysis…"):
                try:
                    predictor = load_predictor()
                    uploaded_file.seek(0)
                    result = predictor.predict(uploaded_file,
                                               image_name=uploaded_file.name)
                    st.success("✅ Analysis complete!")
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.stop()

            severity = result["severity"]
            s_level  = severity["level"]

            # Disease name
            if result["is_healthy"]:
                st.markdown(f'<div class="severity-healthy">'
                            f'<h3>✅ {result["common_name"]}</h3>'
                            f'<p>{severity["description"]}</p></div>',
                            unsafe_allow_html=True)
            else:
                css_class = f"severity-{s_level}"
                icon = {"early": "🟡", "moderate": "🟠", "severe": "🔴"}.get(s_level, "⚪")
                st.markdown(f'<div class="{css_class}">'
                            f'<h3>{icon} {result["common_name"]}</h3>'
                            f'<p><b>Severity:</b> {s_level.upper()}</p>'
                            f'<p>{severity["description"]}</p></div>',
                            unsafe_allow_html=True)

            st.markdown("---")
            # Metrics row
            m1, m2, m3 = st.columns(3)
            m1.metric("Confidence", f"{severity['confidence_pct']}%")
            m2.metric("Infected Area", f"{severity['infected_area_pct']}%")
            m3.metric("Pathogen", result["pathogen"].split(" ")[0]
                      if result["pathogen"] != "N/A" else "N/A")

        # ── Full Results Below ────────────────────────────────────────────────
        if not result["is_healthy"]:
            st.markdown("---")
            tab1, tab2, tab3, tab4 = st.tabs([
                "🗓️ Progression Forecast",
                "💊 Treatment Plan",
                "🔬 AI Explanation",
                "📊 Top-3 Predictions",
            ])

            with tab1:
                p = result["progression"]
                st.markdown("#### Disease Progression Forecast (if untreated)")
                st.warning(p.get("urgency", ""))
                st.markdown(f"""
                | Stage | Timeline |
                |-------|----------|
                | **Current** | {p.get('current_stage', 'N/A')} |
                | **Next Stage** | {p.get('next_stage', 'N/A')} in ~{p.get('days_to_next', 'N/A')} days |
                | **Severe** | in ~{p.get('then_severe_in', 'N/A')} days |
                """)
                st.info(p.get("forecast", ""))

            with tab2:
                t = result["treatment"]
                st.markdown("#### 🌿 Organic Treatment")
                for item in t.get("organic", []):
                    st.markdown(f'<div class="treatment-card">🌱 {item}</div>',
                                unsafe_allow_html=True)

                st.markdown("#### 🧪 Chemical Treatment")
                for item in t.get("chemical", []):
                    st.markdown(f'<div class="treatment-card">⚗️ {item}</div>',
                                unsafe_allow_html=True)

                st.markdown("#### 🛡️ Preventive Measures")
                for item in t.get("preventive", []):
                    st.markdown(f'<div class="treatment-card">🔒 {item}</div>',
                                unsafe_allow_html=True)

                st.markdown("#### 💡 Farming Tips")
                for tip in result.get("farming_tips", []):
                    st.info(tip)

            with tab3:
                col_h, col_exp = st.columns([1, 1])
                with col_h:
                    if result.get("heatmap_base64"):
                        st.markdown("**Grad-CAM Heatmap** — Red = model focus area")
                        img_bytes = base64.b64decode(result["heatmap_base64"])
                        st.image(img_bytes, caption="AI Attention Map",
                                 use_column_width=True)
                    else:
                        st.info("Heatmap not available for this prediction.")
                with col_exp:
                    st.markdown(result["explanation"])

            with tab4:
                st.markdown("#### Top-3 Model Predictions")
                for i, pred in enumerate(result["top3_predictions"]):
                    rank_color = ["🥇", "🥈", "🥉"][i]
                    st.markdown(
                        f"{rank_color} **{pred['common_name']}** — "
                        f"`{pred['probability']}%` confidence"
                    )
                    st.progress(pred["probability"] / 100)

        # ── Export Button ─────────────────────────────────────────────────────
        st.markdown("---")
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            result_json = json.dumps({k: v for k, v in result.items()
                                       if k != "heatmap_base64"}, indent=2)
            st.download_button(
                "📥 Download JSON Result",
                data=result_json,
                file_name="disease_result.json",
                mime="application/json",
            )
        with col_dl2:
            if os.path.exists(log_path):
                with open(log_path, "rb") as f:
                    st.download_button(
                        "📊 Download CSV (Tableau Export)",
                        data=f.read(),
                        file_name="predictions_log.csv",
                        mime="text/csv",
                    )


# ── ANALYTICS DASHBOARD ───────────────────────────────────────────────────────
elif page == "📊 Analytics Dashboard":
    st.markdown("## 📊 Detection Analytics Dashboard")

    if not os.path.exists(log_path):
        st.info("No predictions yet. Run some detections first to see analytics.")
        st.stop()

    df = pd.read_csv(log_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Scans",       len(df))
    col2.metric("Diseases Found",    len(df[df["is_healthy"] == False]))
    col3.metric("Healthy Plants",    len(df[df["is_healthy"] == True]))
    col4.metric("Avg Confidence",    f"{df['confidence_pct'].mean():.1f}%")

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Disease Distribution")
        diseased = df[df["is_healthy"] == False]
        if not diseased.empty:
            dist = diseased["common_name"].value_counts().head(10)
            st.bar_chart(dist)

    with c2:
        st.markdown("#### Severity Breakdown")
        severity_counts = df["severity_level"].value_counts()
        st.bar_chart(severity_counts)

    st.markdown("#### Recent Detections")
    display_cols = ["timestamp", "common_name", "plant_type",
                    "severity_level", "confidence_pct", "infected_area_pct"]
    st.dataframe(df[display_cols].sort_values("timestamp", ascending=False).head(20),
                 use_container_width=True)

    st.markdown("---")
    if os.path.exists(log_path):
        with open(log_path, "rb") as f:
            st.download_button("📥 Export Full CSV for Tableau",
                               f.read(), "predictions_log.csv", "text/csv")


# ── ABOUT PAGE ────────────────────────────────────────────────────────────────
elif page == "ℹ️ About":
    st.markdown("## ℹ️ About This System")
    st.markdown("""
    ### Plant Disease Detection System for Sustainable Agriculture

    **Architecture:** MobileNetV2 (Transfer Learning) + Custom Classification Head

    **Dataset:** PlantVillage — 87,000 images, 38 disease/healthy classes, 14 crop types

    **Novelty Feature:** Disease Progression & Treatment Recommendation System
    - Predicts disease severity (Early / Moderate / Severe) using CNN confidence + image analysis
    - Forecasts how fast the disease will worsen if untreated
    - Provides structured organic, chemical, and preventive treatment plans

    **Explainable AI:** Grad-CAM heatmaps showing which leaf regions drove the prediction

    **Tech Stack:**
    | Component | Technology |
    |-----------|------------|
    | Model | MobileNetV2 + TensorFlow/Keras |
    | XAI | Grad-CAM |
    | Severity | HSV color segmentation + confidence |
    | UI | Streamlit |
    | Analytics | Pandas + Streamlit charts |
    | Export | CSV → Tableau |

    **Future Enhancements:**
    - 📱 Mobile app (React Native / Flutter)
    - 🌐 REST API deployment (FastAPI)
    - 🔄 Real-time camera detection
    - 🌡️ IoT sensor integration (soil, weather)
    - 🗺️ GPS-based regional disease heatmaps
    """)
