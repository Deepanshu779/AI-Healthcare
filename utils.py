import re
import math

def calculate_bmi(height, weight):
    """
    Calculate BMI using height (cm) and weight (kg)
    """
    try:
        height = float(height)
        weight = float(weight)

        if height <= 0 or weight <= 0:
            return 0.0

        height_m = height / 100.0
        bmi = weight / (height_m * height_m)

        return round(bmi, 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0


def bmi_status(bmi):
    """
    Return BMI category
    """
    if bmi <= 0:
        return "Invalid"
    elif bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal (Healthy)"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"


def calculate_risk(age, severity, temperature=None, spo2=None):
    """
    Calculate patient's overall risk level (Low, Medium, High, Critical)
    """
    try:
        age = int(age)
    except Exception:
        age = 30

    severity = str(severity or "").lower()

    try:
        temperature = float(temperature) if temperature else None
    except Exception:
        temperature = None

    try:
        spo2 = int(spo2) if spo2 else None
    except Exception:
        spo2 = None

    # Critical / High Risk
    if (
        (spo2 is not None and spo2 < 90)
        or (temperature is not None and temperature >= 40.0)
    ):
        return "Critical"
    elif (
        age >= 60
        or severity in ["severe", "critical"]
        or (temperature is not None and temperature >= 39.0)
        or (spo2 is not None and spo2 < 93)
    ):
        return "High"
    elif (
        age >= 45
        or severity == "moderate"
        or (temperature is not None and temperature >= 38.0)
        or (spo2 is not None and spo2 < 96)
    ):
        return "Medium"

    return "Low"


def emergency_check(emergency_list):
    """
    Returns True if emergency symptoms are selected
    """
    if not emergency_list:
        return False
    return len(emergency_list) > 0


def temperature_status(temperature):
    """
    Return temperature status
    """
    try:
        temperature = float(temperature)
    except Exception:
        return "Not Provided"

    if temperature < 35.0:
        return "Hypothermia"
    elif temperature < 37.3:
        return "Normal"
    elif temperature < 38.5:
        return "Mild Fever"
    elif temperature < 40.0:
        return "High Fever"
    else:
        return "Hyperpyrexia (Critical)"


def spo2_status(spo2):
    """
    Return oxygen saturation status
    """
    try:
        spo2 = int(spo2)
    except Exception:
        return "Not Provided"

    if spo2 >= 95:
        return "Optimal (Normal)"
    elif spo2 >= 92:
        return "Low (Caution)"
    else:
        return "Critical (Hypoxia)"


def health_score(risk, bmi):
    """
    Calculate overall health score (0–100)
    """
    score = 100

    if risk == "Critical":
        score -= 60
    elif risk == "High":
        score -= 40
    elif risk == "Medium":
        score -= 20

    if bmi < 18.5:
        score -= 10
    elif bmi >= 30:
        score -= 15
    elif bmi >= 25:
        score -= 5

    return max(score, 10)


def health_summary(score):
    """
    Return health summary based on score
    """
    if score >= 85:
        return "Optimal Condition"
    elif score >= 70:
        return "Mild Caution"
    elif score >= 50:
        return "Moderate Risk"
    else:
        return "Needs Clinical Attention"


def calculate_bmr(weight, height, age, gender="Male"):
    """
    Basal Metabolic Rate via Mifflin-St Jeor formula
    """
    try:
        w = float(weight)
        h = float(height)
        a = int(age)
        base = (10 * w) + (6.25 * h) - (5 * a)
        if str(gender).lower().startswith("f"):
            return round(base - 161, 0)
        return round(base + 5, 0)
    except Exception:
        return 1600.0


def calculate_hydration(weight):
    """
    Recommended daily water intake in liters (35ml per kg)
    """
    try:
        w = float(weight)
        return round((w * 0.035), 1)
    except Exception:
        return 2.5


def calculate_target_heart_rate(age):
    """
    Cardiovascular heart rate zones based on age (Max HR = 220 - age)
    """
    try:
        a = int(age)
        max_hr = 220 - a
        return {
            "max": max_hr,
            "moderate": f"{int(max_hr * 0.5)} - {int(max_hr * 0.7)} bpm",
            "vigorous": f"{int(max_hr * 0.7)} - {int(max_hr * 0.85)} bpm"
        }
    except Exception:
        return {"max": 190, "moderate": "95 - 133 bpm", "vigorous": "133 - 161 bpm"}


def calculate_map(systolic, diastolic):
    """
    Mean Arterial Pressure (MAP = (2*Diastolic + Systolic) / 3)
    """
    try:
        sys = float(systolic)
        dia = float(diastolic)
        map_val = (2 * dia + sys) / 3.0
        return round(map_val, 1)
    except Exception:
        return None


def parse_precautions_list(precaution_text):
    """
    Splits precautions string into a clean list of individual action items.
    """
    if not precaution_text or precaution_text == "Consult a healthcare professional.":
        return [
            "Consult a licensed healthcare professional for tailored medical guidance.",
            "Continuously monitor your vital signs and symptom changes.",
            "Maintain optimal hydration, gentle rest, and record symptom onset times."
        ]

    # Split by comma or semicolons
    items = [p.strip().capitalize() for p in re.split(r'[,;]\s*', str(precaution_text)) if p.strip()]
    return items if items else [precaution_text]


def parse_ai_sections(ai_text):
    """
    Parses markdown response with ## headings into structured sections for clean UI rendering.
    """
    sections = {}
    current_key = "general"
    sections[current_key] = []

    for line in str(ai_text or "").splitlines():
        trimmed = line.strip()
        if trimmed.startswith("## "):
            heading = trimmed[3:].strip().lower()
            if "assessment" in heading or "possible" in heading:
                current_key = "assessment"
            elif "why" in heading or "fit" in heading:
                current_key = "why_fit"
            elif "home" in heading or "protocol" in heading or "care" in heading:
                current_key = "home_care"
            elif "diet" in heading or "nutrition" in heading:
                current_key = "diet"
            elif "warning" in heading or "red flag" in heading or "urgent" in heading:
                current_key = "warnings"
            elif "consult" in heading or "specialist" in heading or "doctor" in heading:
                current_key = "specialist"
            elif "note" in heading or "disclaimer" in heading:
                current_key = "note"
            else:
                current_key = heading.replace(" ", "_")
            sections[current_key] = []
        else:
            if trimmed:
                sections[current_key].append(trimmed)

    # Convert list of lines to joined text
    return {k: "\n".join(v) for k, v in sections.items()}


def get_all_symptoms_catalog():
    """
    Returns full categorized symptom catalog for UI mapping, search, and 3D anatomy explorer.
    """
    return {
        "general": {
            "name": "Systemic & General",
            "icon": "activity",
            "color": "#38bdf8",
            "description": "Fever, fatigue, chills, body weight and systemic discomfort",
            "symptoms": [
                "high_fever", "mild_fever", "chills", "shivering", "fatigue", "lethargy",
                "malaise", "sweating", "weight_loss", "weight_gain", "increased_appetite",
                "loss_of_appetite", "dehydration", "restlessness", "sunken_eyes", "muscle_weakness",
                "swelled_lymph_nodes"
            ]
        },
        "respiratory": {
            "name": "Respiratory & Pulmonary",
            "icon": "wind",
            "color": "#34d399",
            "description": "Lungs, airways, breathing difficulty, throat and nasal passages",
            "symptoms": [
                "cough", "breathlessness", "phlegm", "chest_pain", "throat_irritation",
                "continuous_sneezing", "sinus_pressure", "runny_nose", "congestion",
                "patches_in_throat", "mucoid_sputum", "rusty_sputum", "blood_in_sputum"
            ]
        },
        "digestive": {
            "name": "Digestive & Gastrointestinal",
            "icon": "disc",
            "color": "#fbbf24",
            "description": "Stomach, liver, bowel, digestion and abdominal discomfort",
            "symptoms": [
                "vomiting", "nausea", "acidity", "indigestion", "stomach_pain", "abdominal_pain",
                "diarrhoea", "constipation", "passage_of_gases", "belly_pain", "distention_of_abdomen",
                "ulcers_on_tongue", "stomach_bleeding", "yellowish_skin", "yellowing_of_eyes"
            ]
        },
        "neurological": {
            "name": "Neurological & Sensory",
            "icon": "cpu",
            "color": "#a855f7",
            "description": "Brain, cranial nerves, vision, balance and cognitive sensation",
            "symptoms": [
                "headache", "dizziness", "loss_of_balance", "unsteadiness", "altered_sensorium",
                "visual_disturbances", "blurred_and_distorted_vision", "spinning_movements",
                "lack_of_concentration", "slurred_speech", "depression", "irritability", "anxiety"
            ]
        },
        "cardiovascular": {
            "name": "Cardiovascular & Circulatory",
            "icon": "heart",
            "color": "#f43f5e",
            "description": "Heart, blood vessels, circulation, palpitations and pressure",
            "symptoms": [
                "chest_pain", "fast_heart_rate", "palpitations", "swollen_legs",
                "swollen_blood_vessels", "prominent_veins_on_calf", "cold_hands_and_feets"
            ]
        },
        "musculoskeletal": {
            "name": "Musculoskeletal & Joints",
            "icon": "shield",
            "color": "#f97316",
            "description": "Bones, joints, muscles, spine and physical mobility",
            "symptoms": [
                "joint_pain", "muscle_pain", "back_pain", "neck_pain", "knee_pain", "hip_joint_pain",
                "muscle_wasting", "movement_stiffness", "swelling_joints", "stiff_neck", "cramps"
            ]
        },
        "dermatology": {
            "name": "Dermatology & Skin",
            "icon": "layers",
            "color": "#ec4899",
            "description": "Skin surface, rashes, lesions, itching and allergies",
            "symptoms": [
                "itching", "skin_rash", "nodal_skin_eruptions", "dischromic _patches", "skin_peeling",
                "blister", "red_sore_around_nose", "yellow_crust_ooze", "pus_filled_pimples",
                "blackheads", "scurring", "red_spots_over_body", "bruising"
            ]
        },
        "urinary": {
            "name": "Urinary & Renal",
            "icon": "droplet",
            "color": "#06b6d4",
            "description": "Kidneys, bladder, urinary tract and fluid clearance",
            "symptoms": [
                "burning_micturition", "spotting_ urination", "dark_urine", "yellow_urine",
                "polyuria", "continuous_feel_of_urine", "foul_smell_of urine", "bladder_discomfort"
            ]
        }
    }