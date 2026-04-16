"""
=============================================================
 Tableau Export Utility
=============================================================
Generates:
  1. predictions_log.csv — main output from the pipeline
  2. tableau_summary.csv — aggregated for dashboard
  3. sample_data.csv     — realistic demo data for Tableau

Tableau Calculated Fields Guide is printed at the end.
"""

import pandas as pd
import numpy as np
import os, datetime, random

# ── Sample Demo Data Generator ────────────────────────────────────────────────

DISEASES = [
    ("Tomato___Early_blight",           "Tomato Early Blight",    "Fungus",   "Tomato"),
    ("Tomato___Late_blight",            "Tomato Late Blight",     "Oomycete", "Tomato"),
    ("Tomato___Bacterial_spot",         "Bacterial Spot",         "Bacteria", "Tomato"),
    ("Potato___Late_blight",            "Potato Late Blight",     "Oomycete", "Potato"),
    ("Potato___Early_blight",           "Potato Early Blight",    "Fungus",   "Potato"),
    ("Corn_(maize)___Common_rust_",     "Common Rust",            "Fungus",   "Corn"),
    ("Apple___Apple_scab",              "Apple Scab",             "Fungus",   "Apple"),
    ("Grape___Black_rot",               "Grape Black Rot",        "Fungus",   "Grape"),
    ("Tomato___Leaf_Mold",              "Leaf Mold",              "Fungus",   "Tomato"),
    ("Tomato___healthy",                "Healthy Tomato",         "N/A",      "Tomato"),
    ("Potato___healthy",                "Healthy Potato",         "N/A",      "Potato"),
    ("Corn_(maize)___healthy",          "Healthy Corn",           "N/A",      "Corn"),
]

REGIONS  = ["Tamil Nadu", "Maharashtra", "Punjab", "Karnataka", "Andhra Pradesh",
             "West Bengal", "Uttar Pradesh", "Rajasthan"]
SEVERITY = ["early", "moderate", "severe"]


def generate_sample_data(n: int = 200) -> pd.DataFrame:
    """Generate n realistic sample predictions for Tableau demo."""
    random.seed(42)
    rows = []
    base_date = datetime.datetime(2024, 1, 1)

    for i in range(n):
        disease = random.choices(DISEASES, weights=[
            10, 8, 7, 9, 7, 6, 5, 4, 4, 15, 12, 13
        ])[0]
        class_name, common_name, pathogen, plant_type = disease
        is_healthy = "healthy" in class_name.lower()

        timestamp = base_date + datetime.timedelta(days=random.randint(0, 365),
                                                    hours=random.randint(6, 20))
        confidence    = round(random.uniform(0.78, 0.99), 3)
        infected_area = round(random.uniform(0, 0.6) if not is_healthy else 0, 3)
        severity_level = "healthy" if is_healthy else random.choices(
            SEVERITY, weights=[40, 35, 25])[0]
        severity_score = (
            0.0 if is_healthy else
            round(random.uniform(0.0, 0.25) if severity_level == "early" else
                  random.uniform(0.25, 0.55) if severity_level == "moderate" else
                  random.uniform(0.55, 1.0), 3)
        )
        region        = random.choice(REGIONS)
        days_moderate = random.randint(5, 14) if not is_healthy else ""
        days_severe   = random.randint(12, 25) if not is_healthy else ""

        rows.append({
            "timestamp":          timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "date":               timestamp.strftime("%Y-%m-%d"),
            "month":              timestamp.strftime("%B %Y"),
            "week":               f"Week {timestamp.isocalendar()[1]}",
            "image_name":         f"leaf_{i+1:04d}.jpg",
            "predicted_class":    class_name,
            "common_name":        common_name,
            "pathogen_type":      pathogen,
            "plant_type":         plant_type,
            "confidence_pct":     round(confidence * 100, 1),
            "infected_area_pct":  round(infected_area * 100, 1),
            "severity_level":     severity_level,
            "severity_score":     severity_score,
            "is_healthy":         is_healthy,
            "region":             region,
            "days_to_moderate":   days_moderate,
            "days_to_severe":     days_severe,
            "accuracy_pct":       round(confidence * 100, 1),  # proxy for Tableau
        })

    return pd.DataFrame(rows)


def generate_tableau_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create aggregated summary for Tableau calculated fields demo."""
    summary = df.groupby(["common_name", "plant_type", "severity_level"]).agg(
        count=("image_name", "count"),
        avg_confidence=("confidence_pct", "mean"),
        avg_infected_area=("infected_area_pct", "mean"),
    ).reset_index()
    summary["avg_confidence"]    = summary["avg_confidence"].round(1)
    summary["avg_infected_area"] = summary["avg_infected_area"].round(1)
    return summary


def print_tableau_guide():
    """Print Tableau dashboard setup guide."""
    guide = """
╔══════════════════════════════════════════════════════════════════════╗
║         TABLEAU DASHBOARD SETUP GUIDE                              ║
╚══════════════════════════════════════════════════════════════════════╝

📁 Connect to: predictions_log.csv (or sample_data.csv for demo)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CALCULATED FIELDS TO CREATE IN TABLEAU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Disease Count
   Formula: COUNT([Predicted Class])
   Use in:  Bar chart of most common diseases

2. Severity Category (Ordered)
   Formula: IF [Severity Level] = "severe" THEN 3
            ELSEIF [Severity Level] = "moderate" THEN 2
            ELSEIF [Severity Level] = "early" THEN 1
            ELSE 0 END
   Use in:  Sorting severity levels correctly on charts

3. Accuracy %
   Formula: AVG([Confidence Pct])
   Use in:  Line chart tracking model accuracy over time

4. Infected Plants
   Formula: COUNTIF([Is Healthy] = FALSE)
   Or:      SUM(IF [Is Healthy] = "False" THEN 1 ELSE 0 END)
   Use in:  KPI cards

5. Disease Spread Rate (days)
   Formula: AVG([Days To Severe])
   Use in:  Comparing how fast different diseases spread

6. Health Rate %
   Formula: SUM(IF [Is Healthy] = "True" THEN 1 ELSE 0 END)
            / COUNT([Image Name]) * 100
   Use in:  Donut chart

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDED CHARTS & SHEETS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sheet 1 — Disease Distribution (Bar Chart)
  Rows:    Common Name
  Columns: Disease Count (calculated field)
  Color:   Plant Type
  Filter:  Is Healthy = False
  Sort:    Descending by count

Sheet 2 — Severity Breakdown (Pie or Donut)
  Mark type: Pie
  Angle:   COUNT([Image Name])
  Color:   Severity Level
  Colors:  early=Yellow, moderate=Orange, severe=Red, healthy=Green

Sheet 3 — Accuracy Over Time (Line Chart)
  Rows:    Accuracy % (calculated field)
  Columns: Month (Date field, formatted as Month Year)
  Mark:    Line

Sheet 4 — Region-wise Disease Heatmap (Map)
  Mark type: Map (if lat/long available) OR Text Table
  Rows:    Region
  Columns: Common Name
  Values:  Disease Count
  Color:   Severity Category

Sheet 5 — Infection Area vs Confidence (Scatter)
  Rows:    Infected Area Pct
  Columns: Confidence Pct
  Color:   Severity Level
  Size:    Severity Score

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DASHBOARD LAYOUT SUGGESTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────┐
│  [KPI: Total Scans] [Diseases] [Healthy] [Avg Accuracy] │
├────────────────────────┬────────────────────────────────┤
│  Disease Distribution  │  Severity Breakdown (Pie)      │
│  (Horizontal Bar)      │                                │
├────────────────────────┴────────────────────────────────┤
│           Accuracy Over Time (Line Chart)               │
├────────────────────────┬────────────────────────────────┤
│  Region/Plant Heatmap  │  Infection Area vs Confidence  │
└────────────────────────┴────────────────────────────────┘
"""
    print(guide)


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)

    print("Generating sample data…")
    df_sample = generate_sample_data(200)
    df_sample.to_csv("outputs/sample_data.csv", index=False)
    print(f"  ✅ outputs/sample_data.csv ({len(df_sample)} rows)")

    df_summary = generate_tableau_summary(df_sample)
    df_summary.to_csv("outputs/tableau_summary.csv", index=False)
    print(f"  ✅ outputs/tableau_summary.csv ({len(df_summary)} rows)")

    print_tableau_guide()

    # Print schema
    print("\n📋 CSV SCHEMA (predictions_log.csv):")
    print("─" * 50)
    schema = {
        "timestamp":         "DATETIME  — prediction date and time",
        "date":              "DATE      — date only (for time filters)",
        "month":             "STRING    — 'January 2024' format",
        "image_name":        "STRING    — source image filename",
        "predicted_class":   "STRING    — full PlantVillage class name",
        "common_name":       "STRING    — human-readable disease name",
        "pathogen_type":     "STRING    — Fungus / Bacteria / Virus / N/A",
        "plant_type":        "STRING    — Tomato / Potato / Corn etc.",
        "confidence_pct":    "FLOAT     — model confidence (0-100%)",
        "infected_area_pct": "FLOAT     — % leaf area showing disease",
        "severity_level":    "STRING    — early / moderate / severe / healthy",
        "severity_score":    "FLOAT     — composite score (0-1)",
        "is_healthy":        "BOOLEAN   — True if no disease detected",
        "region":            "STRING    — geographic region (if collected)",
        "days_to_moderate":  "INTEGER   — days until moderate stage if untreated",
        "days_to_severe":    "INTEGER   — days until severe stage if untreated",
        "accuracy_pct":      "FLOAT     — confidence % (proxy for accuracy chart)",
    }
    for col, desc in schema.items():
        print(f"  {col:<25} {desc}")
