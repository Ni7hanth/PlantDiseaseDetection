"""
=============================================================
 Disease Knowledge Base
=============================================================
Maps each of the 38 PlantVillage classes to:
  • severity_indicators  -> visual cues used to estimate stage
  • progression_timeline -> days until next stage if untreated
  • treatment            -> organic, chemical, preventive
  • farming_tips
  • affected_area_threshold -> % leaf area to judge severity

This file is the backbone of the Novelty Feature:
  "Disease Progression & Treatment Recommendation System"
"""

DISEASE_KB: dict = {

    # ── APPLE ────────────────────────────────────────────────────────────────
    "Apple___Apple_scab": {
        "common_name": "Apple Scab",
        "pathogen": "Venturia inaequalis (Fungus)",
        "severity_indicators": {
            "early":    "Small olive-green spots on leaves/fruit surface (<10% area)",
            "moderate": "Dark, scabby lesions on 10-40% leaf area, slight fruit distortion",
            "severe":   "Heavy lesion coverage >40%, premature leaf drop, cracked fruit",
        },
        "progression_days": {"early_to_moderate": 7, "moderate_to_severe": 10},
        "treatment": {
            "organic":   ["Neem oil spray (2ml/L water, every 7 days)",
                          "Sulfur-based fungicide (wettable sulfur)",
                          "Prune and destroy infected leaves"],
            "chemical":  ["Captan 50 WP @ 2g/L water",
                          "Mancozeb 75 WP @ 2.5g/L water",
                          "Apply at 7-10 day intervals during wet weather"],
            "preventive":["Plant resistant varieties (Enterprise, Liberty)",
                          "Rake and remove fallen leaves in autumn",
                          "Improve air circulation by pruning"],
        },
        "farming_tips": [
            "Apply fungicide before rain events (protectant schedule).",
            "Avoid overhead irrigation — use drip irrigation.",
            "Monitor weather: scab spreads most during wet, cool spring.",
        ],
    },

    "Apple___Black_rot": {
        "common_name": "Apple Black Rot",
        "pathogen": "Botryosphaeria obtusa (Fungus)",
        "severity_indicators": {
            "early":    "Small purple spots (frogeye lesions) on leaves",
            "moderate": "Tan-brown lesions with purple borders, fruit spots appear",
            "severe":   "Fruit mummification, cankers on branches",
        },
        "progression_days": {"early_to_moderate": 10, "moderate_to_severe": 14},
        "treatment": {
            "organic":   ["Copper-based fungicide spray", "Remove mummified fruits"],
            "chemical":  ["Captan or Myclobutanil sprays at 10-day intervals"],
            "preventive":["Prune dead wood in late winter", "Avoid wounding bark"],
        },
        "farming_tips": ["Keep orchard floor clean of dead wood and mummies."],
    },

    "Apple___Cedar_apple_rust": {
        "common_name": "Cedar Apple Rust",
        "pathogen": "Gymnosporangium juniperi-virginianae (Fungus)",
        "severity_indicators": {
            "early":    "Yellow-orange spots on upper leaf surface",
            "moderate": "Tube-like structures (aecia) on leaf underside",
            "severe":   "Heavy defoliation, fruit infection",
        },
        "progression_days": {"early_to_moderate": 8, "moderate_to_severe": 12},
        "treatment": {
            "organic":   ["Sulfur spray every 7-10 days during infection period"],
            "chemical":  ["Myclobutanil or Triadimefon fungicide"],
            "preventive":["Remove nearby juniper/cedar hosts within 500m",
                          "Plant rust-resistant apple varieties"],
        },
        "farming_tips": ["Infection only occurs in spring — target spray timing."],
    },

    "Apple___healthy": {
        "common_name": "Healthy Apple",
        "pathogen": None,
        "severity_indicators": {"early": "N/A", "moderate": "N/A", "severe": "N/A"},
        "progression_days": {},
        "treatment": {"organic": [], "chemical": [], "preventive": ["Routine monitoring"]},
        "farming_tips": ["Continue regular inspection and balanced fertilization."],
    },

    # ── CORN ─────────────────────────────────────────────────────────────────
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "common_name": "Corn Gray Leaf Spot",
        "pathogen": "Cercospora zeae-maydis (Fungus)",
        "severity_indicators": {
            "early":    "Small tan rectangular lesions limited to lower leaves",
            "moderate": "Lesions expand and coalesce, moving up the canopy",
            "severe":   "Upper leaves infected, >50% leaf area necrotic",
        },
        "progression_days": {"early_to_moderate": 10, "moderate_to_severe": 10},
        "treatment": {
            "organic":   ["Improve field drainage and air flow"],
            "chemical":  ["Azoxystrobin + Propiconazole (Quilt Xcel)",
                          "Apply at VT/R1 growth stage"],
            "preventive":["Plant resistant hybrids", "Rotate with soybean or wheat",
                          "Reduce corn residue by tilling"],
        },
        "farming_tips": ["Gray leaf spot thrives in high humidity — avoid over-irrigation."],
    },

    "Corn_(maize)___Common_rust_": {
        "common_name": "Corn Common Rust",
        "pathogen": "Puccinia sorghi (Fungus)",
        "severity_indicators": {
            "early":    "Scattered cinnamon-brown pustules on both leaf surfaces",
            "moderate": "Dense pustules covering 20-40% of leaf area",
            "severe":   "Pustules burst releasing powdery spores, leaf yellowing >50%",
        },
        "progression_days": {"early_to_moderate": 7, "moderate_to_severe": 7},
        "treatment": {
            "organic":   ["Sulfur-based fungicide in early stage"],
            "chemical":  ["Triazole fungicides (Propiconazole, Tebuconazole)"],
            "preventive":["Plant rust-resistant corn hybrids",
                          "Early planting to avoid peak rust season"],
        },
        "farming_tips": ["Scout fields weekly from V6 stage."],
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        "common_name": "Northern Corn Leaf Blight",
        "pathogen": "Exserohilum turcicum (Fungus)",
        "severity_indicators": {
            "early":    "Small, oval gray-green lesions on lower leaves",
            "moderate": "Cigar-shaped lesions 2.5-15cm, moving to upper canopy",
            "severe":   "Entire plant canopy infected, gray sporulation visible",
        },
        "progression_days": {"early_to_moderate": 10, "moderate_to_severe": 12},
        "treatment": {
            "organic":   ["Crop rotation", "Remove infected debris"],
            "chemical":  ["Mancozeb 75WP or Azoxystrobin at tasseling stage"],
            "preventive":["Resistant hybrids are most effective solution"],
        },
        "farming_tips": ["Most critical window: protect leaves from ear up."],
    },

    "Corn_(maize)___healthy": {
        "common_name": "Healthy Corn",
        "pathogen": None,
        "severity_indicators": {"early": "N/A", "moderate": "N/A", "severe": "N/A"},
        "progression_days": {},
        "treatment": {"organic": [], "chemical": [], "preventive": ["Monitor weekly"]},
        "farming_tips": ["Maintain balanced NPK fertilization for healthy growth."],
    },

    # ── TOMATO ───────────────────────────────────────────────────────────────
    "Tomato___Bacterial_spot": {
        "common_name": "Tomato Bacterial Spot",
        "pathogen": "Xanthomonas vesicatoria (Bacteria)",
        "severity_indicators": {
            "early":    "Water-soaked circular spots on leaves/fruit",
            "moderate": "Dark brown spots with yellow halo, 10-30% leaf area",
            "severe":   "Leaf defoliation, scabby fruit lesions",
        },
        "progression_days": {"early_to_moderate": 5, "moderate_to_severe": 7},
        "treatment": {
            "organic":   ["Copper hydroxide spray (3g/L)",
                          "Avoid working in wet fields to prevent spread"],
            "chemical":  ["Copper-based bactericide + Mancozeb combination",
                          "Streptomycin (where legally permitted)"],
            "preventive":["Use certified disease-free seeds",
                          "Avoid overhead irrigation",
                          "2-3 year crop rotation"],
        },
        "farming_tips": ["Bacteria spread via rain splash — stake plants well above ground."],
    },

    "Tomato___Early_blight": {
        "common_name": "Tomato Early Blight",
        "pathogen": "Alternaria solani (Fungus)",
        "severity_indicators": {
            "early":    "Dark brown spots with concentric rings (target pattern) on older leaves",
            "moderate": "Multiple lesions per leaf, yellowing around spots, 20-40% area",
            "severe":   "Lesions merge, leaves yellow and drop, stem cankers visible",
        },
        "progression_days": {"early_to_moderate": 7, "moderate_to_severe": 7},
        "treatment": {
            "organic":   ["Neem oil (5ml/L) spray every 7 days",
                          "Baking soda solution (1 tsp/L water)"],
            "chemical":  ["Chlorothalonil 75WP @ 2g/L",
                          "Mancozeb + Carbendazim combination"],
            "preventive":["Mulch around plants to prevent soil splash",
                          "Remove lower infected leaves promptly",
                          "Avoid excess nitrogen fertilization"],
        },
        "farming_tips": ["Start fungicide program when first spots appear — don't wait."],
    },

    "Tomato___Late_blight": {
        "common_name": "Tomato Late Blight",
        "pathogen": "Phytophthora infestans (Oomycete)",
        "severity_indicators": {
            "early":    "Water-soaked pale green patches on leaf edges",
            "moderate": "Dark brown lesions with white mold on undersides",
            "severe":   "Rapid collapse of entire plant in 3-7 days if untreated",
        },
        "progression_days": {"early_to_moderate": 3, "moderate_to_severe": 4},
        "treatment": {
            "organic":   ["Copper fungicide spray immediately on detection",
                          "Remove and destroy all infected plant parts"],
            "chemical":  ["Metalaxyl + Mancozeb (Ridomil Gold MZ)",
                          "Cymoxanil-based fungicides — systemic action"],
            "preventive":["Plant blight-resistant varieties",
                          "Avoid cool + wet conditions for planting",
                          "Never compost infected material"],
        },
        "farming_tips": ["⚠️ Act within 24 hours — late blight is extremely aggressive!"],
    },

    "Tomato___Leaf_Mold": {
        "common_name": "Tomato Leaf Mold",
        "pathogen": "Passalora fulva (Fungus)",
        "severity_indicators": {
            "early":    "Pale yellow spots on upper leaf surface",
            "moderate": "Olive-green velvety mold on underside of leaves",
            "severe":   "Leaves curl, yellow completely, and drop",
        },
        "progression_days": {"early_to_moderate": 10, "moderate_to_severe": 10},
        "treatment": {
            "organic":   ["Increase ventilation in greenhouse", "Reduce humidity <85%"],
            "chemical":  ["Mancozeb or Chlorothalonil sprays"],
            "preventive":["Resistant varieties (Jumbo, Cobra)", "Space plants for air flow"],
        },
        "farming_tips": ["Primarily a greenhouse disease — control humidity above all else."],
    },

    "Tomato___Septoria_leaf_spot": {
        "common_name": "Septoria Leaf Spot",
        "pathogen": "Septoria lycopersici (Fungus)",
        "severity_indicators": {
            "early":    "Small circular spots with dark border on lower leaves",
            "moderate": "Spots with white centers, many per leaf",
            "severe":   "Leaves yellow and drop, moves up entire plant",
        },
        "progression_days": {"early_to_moderate": 7, "moderate_to_severe": 10},
        "treatment": {
            "organic":   ["Copper spray", "Remove infected leaves immediately"],
            "chemical":  ["Chlorothalonil 75WP or Mancozeb"],
            "preventive":["Crop rotation (3+ years)", "Drip irrigation only"],
        },
        "farming_tips": ["Most common tomato disease globally — preventive sprays are key."],
    },

    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "common_name": "Tomato Spider Mites",
        "pathogen": "Tetranychus urticae (Mite — not a fungus!)",
        "severity_indicators": {
            "early":    "Fine stippling/bronze speckling on upper leaf surface",
            "moderate": "Webbing visible on leaf undersides, leaf bronzing",
            "severe":   "Leaves dry, curl and drop; entire plant defoliated",
        },
        "progression_days": {"early_to_moderate": 5, "moderate_to_severe": 7},
        "treatment": {
            "organic":   ["Spray strong water jet to dislodge mites",
                          "Neem oil spray", "Release predatory mites (Phytoseiulus)"],
            "chemical":  ["Abamectin 1.8 EC @ 1ml/L", "Spiromesifen (Oberon)"],
            "preventive":["Avoid drought stress (mites love dry conditions)",
                          "Avoid excessive nitrogen"],
        },
        "farming_tips": ["Mites reproduce very fast in hot, dry weather — act quickly."],
    },

    "Tomato___Target_Spot": {
        "common_name": "Tomato Target Spot",
        "pathogen": "Corynespora cassiicola (Fungus)",
        "severity_indicators": {
            "early":    "Small brown spots with yellow halos",
            "moderate": "Concentric ring pattern (target) on leaves and fruit",
            "severe":   "Large necrotic lesions, defoliation",
        },
        "progression_days": {"early_to_moderate": 8, "moderate_to_severe": 10},
        "treatment": {
            "organic":   ["Copper-based fungicide"],
            "chemical":  ["Azoxystrobin + Difenoconazole (Amistar Top)"],
            "preventive":["Improve air circulation", "Avoid prolonged leaf wetness"],
        },
        "farming_tips": ["Common in warm, humid tropical regions."],
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "common_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "pathogen": "Tomato yellow leaf curl virus — Begomovirus (Virus, spread by whitefly)",
        "severity_indicators": {
            "early":    "Young leaves curl upward with slight yellowing at edges",
            "moderate": "Severe leaf curling, stunted growth, flowers drop",
            "severe":   "Plant fully stunted, no fruit set possible",
        },
        "progression_days": {"early_to_moderate": 10, "moderate_to_severe": 14},
        "treatment": {
            "organic":   ["Yellow sticky traps for whitefly monitoring",
                          "Reflective silver mulch to repel whiteflies",
                          "Neem oil spray for whitefly control"],
            "chemical":  ["Imidacloprid drench (whitefly control)",
                          "Thiamethoxam 25 WG spray — NO cure for virus itself"],
            "preventive":["Plant TYLCV-resistant varieties",
                          "Install insect-proof netting",
                          "Remove infected plants immediately — no recovery possible"],
        },
        "farming_tips": ["⚠️ No chemical cures the virus. Focus 100% on whitefly control."],
    },

    "Tomato___Tomato_mosaic_virus": {
        "common_name": "Tomato Mosaic Virus (ToMV)",
        "pathogen": "Tobamovirus (Virus — mechanical transmission)",
        "severity_indicators": {
            "early":    "Light-dark green mosaic pattern on young leaves",
            "moderate": "Leaf distortion, curling, fern-like appearance",
            "severe":   "Stunted plant, necrotic streaks on stems, fruit malformation",
        },
        "progression_days": {"early_to_moderate": 7, "moderate_to_severe": 14},
        "treatment": {
            "organic":   ["Remove and burn infected plants",
                          "Wash hands/tools with soap before handling plants"],
            "chemical":  ["No chemical cure — focus on vector and hygiene control"],
            "preventive":["Use virus-indexed seed", "Disinfect tools with 10% bleach",
                          "Control aphids (virus vectors)"],
        },
        "farming_tips": ["Virus spreads via touch — never smoke near tomato plants (tobacco mosaic)."],
    },

    "Tomato___healthy": {
        "common_name": "Healthy Tomato",
        "pathogen": None,
        "severity_indicators": {"early": "N/A", "moderate": "N/A", "severe": "N/A"},
        "progression_days": {},
        "treatment": {"organic": [], "chemical": [], "preventive": ["Weekly scouting recommended"]},
        "farming_tips": ["Calcium sprays prevent blossom end rot in hot weather."],
    },

    # ── POTATO ───────────────────────────────────────────────────────────────
    "Potato___Early_blight": {
        "common_name": "Potato Early Blight",
        "pathogen": "Alternaria solani (Fungus)",
        "severity_indicators": {
            "early":    "Dark brown target-ring spots on older lower leaves",
            "moderate": "Multiple lesions, yellowing spreads upward",
            "severe":   "Severe defoliation, tuber surface lesions",
        },
        "progression_days": {"early_to_moderate": 7, "moderate_to_severe": 10},
        "treatment": {
            "organic":   ["Neem oil", "Remove infected foliage"],
            "chemical":  ["Mancozeb 75WP @ 2.5g/L every 7-10 days"],
            "preventive":["Crop rotation (3 years)", "Avoid nitrogen excess"],
        },
        "farming_tips": ["Hilling soil around base reduces tuber infection risk."],
    },

    "Potato___Late_blight": {
        "common_name": "Potato Late Blight",
        "pathogen": "Phytophthora infestans (Oomycete)",
        "severity_indicators": {
            "early":    "Water-soaked lesions on leaf tips/margins",
            "moderate": "White mold on leaf undersides, lesions turn brown",
            "severe":   "Entire foliage collapses within days, tuber rot",
        },
        "progression_days": {"early_to_moderate": 3, "moderate_to_severe": 3},
        "treatment": {
            "organic":   ["Copper hydroxide spray immediately"],
            "chemical":  ["Metalaxyl-M + Mancozeb (Ridomil Gold)", "Cymoxanil"],
            "preventive":["Certified disease-free seed tubers",
                          "Destroy cull piles", "Haulm destruction before harvest"],
        },
        "farming_tips": ["⚠️ Late blight can destroy an entire crop in 7-10 days. Preventive sprays are critical."],
    },

    "Potato___healthy": {
        "common_name": "Healthy Potato",
        "pathogen": None,
        "severity_indicators": {"early": "N/A", "moderate": "N/A", "severe": "N/A"},
        "progression_days": {},
        "treatment": {"organic": [], "chemical": [], "preventive": ["Monitor tubers at harvest"]},
        "farming_tips": ["Store harvested tubers in cool, dark, well-ventilated conditions."],
    },

    # ── GRAPE ────────────────────────────────────────────────────────────────
    "Grape___Black_rot": {
        "common_name": "Grape Black Rot",
        "pathogen": "Guignardia bidwellii (Fungus)",
        "severity_indicators": {
            "early":    "Reddish-brown circular spots on leaves",
            "moderate": "Spots enlarge with black pycnidia (dots) in center",
            "severe":   "Berries shrivel into hard black mummies",
        },
        "progression_days": {"early_to_moderate": 10, "moderate_to_severe": 14},
        "treatment": {
            "organic":   ["Sulfur spray 7 days after bud break"],
            "chemical":  ["Myclobutanil or Captan — begin at bud break"],
            "preventive":["Remove and destroy mummified berries",
                          "Canopy management for air flow"],
        },
        "farming_tips": ["Critical spray windows: bud break through 4 weeks post-bloom."],
    },

    "Grape___Esca_(Black_Measles)": {
        "common_name": "Grape Esca / Black Measles",
        "pathogen": "Phaeomoniella chlamydospora and others (Wood fungi complex)",
        "severity_indicators": {
            "early":    "Interveinal chlorosis/reddish discoloration between leaf veins",
            "moderate": "Tiger-stripe pattern on leaves, berry spotting",
            "severe":   "Sudden wilting (apoplexy), vine death possible",
        },
        "progression_days": {"early_to_moderate": 21, "moderate_to_severe": 30},
        "treatment": {
            "organic":   ["Wound protectants (natural latex) after pruning"],
            "chemical":  ["Arsenite of sodium (restricted)", "Trichoderma-based bioagent"],
            "preventive":["Protect pruning wounds with fungicide paste",
                          "Prune in dry weather", "Use clean, disinfected tools"],
        },
        "farming_tips": ["Esca is a wood disease — prevention at pruning is the ONLY effective control."],
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "common_name": "Grape Leaf Blight",
        "pathogen": "Isariopsis clavispora / Pseudocercospora vitis (Fungus)",
        "severity_indicators": {
            "early":    "Irregular brown spots on upper leaf surface",
            "moderate": "Spots enlarge, grayish lesions on underside",
            "severe":   "Premature defoliation, berry sunscald from exposed clusters",
        },
        "progression_days": {"early_to_moderate": 10, "moderate_to_severe": 10},
        "treatment": {
            "organic":   ["Bordeaux mixture (copper sulfate + lime)"],
            "chemical":  ["Mancozeb or Captan-based fungicides"],
            "preventive":["Canopy thinning", "Avoid excessive irrigation"],
        },
        "farming_tips": ["Common in late season; maintain leaf removal in bunch zone."],
    },

    "Grape___healthy": {
        "common_name": "Healthy Grape",
        "pathogen": None,
        "severity_indicators": {"early": "N/A", "moderate": "N/A", "severe": "N/A"},
        "progression_days": {},
        "treatment": {"organic": [], "chemical": [], "preventive": ["Dormant copper sprays preventively"]},
        "farming_tips": ["Balanced canopy management is key to grape health."],
    },

    # ── PEPPER ───────────────────────────────────────────────────────────────
    "Pepper,_bell___Bacterial_spot": {
        "common_name": "Pepper Bacterial Spot",
        "pathogen": "Xanthomonas campestris pv. vesicatoria (Bacteria)",
        "severity_indicators": {
            "early":    "Small water-soaked spots on leaves",
            "moderate": "Brown necrotic lesions with yellow halo",
            "severe":   "Defoliation, scabby fruit lesions",
        },
        "progression_days": {"early_to_moderate": 5, "moderate_to_severe": 7},
        "treatment": {
            "organic":   ["Copper hydroxide spray", "Use disease-free seed"],
            "chemical":  ["Copper + Mancozeb combination sprays"],
            "preventive":["Avoid overhead irrigation", "Crop rotation 2-3 years"],
        },
        "farming_tips": ["Rain and wind are primary spread mechanisms — protect during storms."],
    },

    "Pepper,_bell___healthy": {
        "common_name": "Healthy Bell Pepper",
        "pathogen": None,
        "severity_indicators": {"early": "N/A", "moderate": "N/A", "severe": "N/A"},
        "progression_days": {},
        "treatment": {"organic": [], "chemical": [], "preventive": ["Consistent watering prevents stress"]},
        "farming_tips": ["Calcium foliar spray prevents blossom end rot."],
    },

    # ── OTHER CROPS (abbreviated entries) ────────────────────────────────────
    "Blueberry___healthy": {
        "common_name": "Healthy Blueberry", "pathogen": None,
        "severity_indicators": {"early": "N/A", "moderate": "N/A", "severe": "N/A"},
        "progression_days": {},
        "treatment": {"organic": [], "chemical": [], "preventive": ["Maintain soil pH 4.5-5.5"]},
        "farming_tips": ["Blueberries thrive in acidic soil — test pH annually."],
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "common_name": "Cherry Powdery Mildew", "pathogen": "Podosphaera clandestina (Fungus)",
        "severity_indicators": {
            "early": "White powdery patches on young leaves",
            "moderate": "Coating on 20-40% leaf surface, leaf curl",
            "severe": "Defoliation, fruit russet",
        },
        "progression_days": {"early_to_moderate": 7, "moderate_to_severe": 10},
        "treatment": {
            "organic": ["Potassium bicarbonate spray", "Sulfur dust"],
            "chemical": ["Myclobutanil or Trifloxystrobin"],
            "preventive": ["Plant in full sun", "Avoid high nitrogen"],
        },
        "farming_tips": ["Powdery mildew thrives in dry weather with humid nights."],
    },
    "Cherry_(including_sour)___healthy": {
        "common_name": "Healthy Cherry", "pathogen": None,
        "severity_indicators": {"early": "N/A", "moderate": "N/A", "severe": "N/A"},
        "progression_days": {},
        "treatment": {"organic": [], "chemical": [], "preventive": []},
        "farming_tips": ["Dormant oil spray prevents scale insects."],
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "common_name": "Citrus Greening (HLB)", "pathogen": "Candidatus Liberibacter asiaticus (Bacteria — spread by psyllid)",
        "severity_indicators": {
            "early": "Blotchy mottle on one branch, asymmetric yellowing",
            "moderate": "Multiple branches affected, small misshapen fruit",
            "severe": "Tree decline, bitter pithy fruit, no economic yield",
        },
        "progression_days": {"early_to_moderate": 60, "moderate_to_severe": 180},
        "treatment": {
            "organic": ["Remove and destroy infected trees immediately"],
            "chemical": ["Imidacloprid for psyllid vector control",
                         "Foliar nutrition (micronutrients) to slow decline"],
            "preventive": ["Certified disease-free nursery stock", "Psyllid monitoring",
                           "Quarantine infected orchards"],
        },
        "farming_tips": ["⚠️ HLB has NO cure. Infected trees must be removed to protect neighbors."],
    },
    "Peach___Bacterial_spot": {
        "common_name": "Peach Bacterial Spot", "pathogen": "Xanthomonas arboricola pv. pruni (Bacteria)",
        "severity_indicators": {
            "early": "Small water-soaked spots on leaves",
            "moderate": "Purple-brown lesions, shot-hole appearance",
            "severe": "Heavy defoliation, fruit pitting and cracking",
        },
        "progression_days": {"early_to_moderate": 7, "moderate_to_severe": 10},
        "treatment": {
            "organic": ["Copper hydroxide at petal fall"],
            "chemical": ["Oxytetracycline during bloom (where permitted)"],
            "preventive": ["Plant resistant varieties", "Windbreaks reduce spread"],
        },
        "farming_tips": ["Warm, wet weather at bloom = highest infection risk."],
    },
    "Peach___healthy": {
        "common_name": "Healthy Peach", "pathogen": None,
        "severity_indicators": {"early": "N/A", "moderate": "N/A", "severe": "N/A"},
        "progression_days": {},
        "treatment": {"organic": [], "chemical": [], "preventive": []},
        "farming_tips": ["Thin fruit early for larger, quality peaches."],
    },
    "Raspberry___healthy": {
        "common_name": "Healthy Raspberry", "pathogen": None,
        "severity_indicators": {"early": "N/A", "moderate": "N/A", "severe": "N/A"},
        "progression_days": {},
        "treatment": {"organic": [], "chemical": [], "preventive": []},
        "farming_tips": ["Remove old canes after harvest to prevent disease buildup."],
    },
    "Soybean___healthy": {
        "common_name": "Healthy Soybean", "pathogen": None,
        "severity_indicators": {"early": "N/A", "moderate": "N/A", "severe": "N/A"},
        "progression_days": {},
        "treatment": {"organic": [], "chemical": [], "preventive": []},
        "farming_tips": ["Inoculate seed with Bradyrhizobium for nitrogen fixation."],
    },
    "Squash___Powdery_mildew": {
        "common_name": "Squash Powdery Mildew", "pathogen": "Podosphaera xanthii (Fungus)",
        "severity_indicators": {
            "early": "White powdery spots on upper leaf surface",
            "moderate": "Spots coalesce, entire leaf covered",
            "severe": "Leaves yellow and die, reduced fruit quality",
        },
        "progression_days": {"early_to_moderate": 7, "moderate_to_severe": 7},
        "treatment": {
            "organic": ["Potassium bicarbonate 5g/L spray", "Neem oil"],
            "chemical": ["Myclobutanil or Trifloxystrobin"],
            "preventive": ["Plant resistant varieties", "Adequate plant spacing"],
        },
        "farming_tips": ["Avoid late-evening irrigation which promotes humid conditions."],
    },
    "Strawberry___Leaf_scorch": {
        "common_name": "Strawberry Leaf Scorch", "pathogen": "Diplocarpon earliana (Fungus)",
        "severity_indicators": {
            "early": "Small purple-red circular spots on leaves",
            "moderate": "Spots enlarge, centers turn gray-brown",
            "severe": "Leaves appear scorched/burned, plant vigor reduced",
        },
        "progression_days": {"early_to_moderate": 10, "moderate_to_severe": 14},
        "treatment": {
            "organic": ["Remove and destroy infected leaves after harvest"],
            "chemical": ["Captan or Thiram fungicide"],
            "preventive": ["Plant resistant varieties", "Good air circulation"],
        },
        "farming_tips": ["Renovate bed after harvest — mow leaves and apply fertilizer."],
    },
    "Strawberry___healthy": {
        "common_name": "Healthy Strawberry", "pathogen": None,
        "severity_indicators": {"early": "N/A", "moderate": "N/A", "severe": "N/A"},
        "progression_days": {},
        "treatment": {"organic": [], "chemical": [], "preventive": []},
        "farming_tips": ["Mulch with straw to keep fruit clean and retain moisture."],
    },
}


def get_disease_info(class_name: str) -> dict:
    """Return the knowledge base entry for a class name (with fallback)."""
    return DISEASE_KB.get(class_name, {
        "common_name": class_name.replace("___", " — ").replace("_", " "),
        "pathogen": "Unknown",
        "severity_indicators": {
            "early": "Minimal lesions detected",
            "moderate": "Moderate lesion coverage",
            "severe": "Extensive damage visible",
        },
        "progression_days": {"early_to_moderate": 7, "moderate_to_severe": 10},
        "treatment": {
            "organic": ["Consult local agricultural extension officer"],
            "chemical": ["Consult local agricultural extension officer"],
            "preventive": ["Regular scouting and early detection"],
        },
        "farming_tips": ["Consult a plant pathologist for accurate diagnosis."],
    })
