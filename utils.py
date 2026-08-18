import re

def calculate_bmi(height, weight):
    """
    Calculate BMI using height (cm) and weight (kg)
    """
    try:
        height = float(height)
        weight = float(weight)

        if height <= 0 or weight <= 0:
            return 0

        height = height / 100
        bmi = weight / (height * height)

        return round(bmi, 2)
    except (ValueError, TypeError):
        return 0


def bmi_status(bmi):
    """
    Return BMI category
    """
    if bmi == 0:
        return "Invalid"
    elif bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal (Healthy)"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calculate_risk(age, severity, temperature=None, spo2=None):
    """
    Calculate patient's overall risk level
    """
    try:
        age = int(age)
    except Exception:
        age = 0

    severity = str(severity or "").lower()

    try:
        temperature = float(temperature) if temperature else None
    except Exception:
        temperature = None

    try:
        spo2 = int(spo2) if spo2 else None
    except Exception:
        spo2 = None

    # High Risk
    if (
        age >= 60
        or severity in ["severe", "critical"]
        or (temperature is not None and temperature >= 39.0)
        or (spo2 is not None and spo2 < 92)
    ):
        return "High"

    # Medium Risk
    elif (
        age >= 40
        or severity == "moderate"
        or (temperature is not None and temperature >= 38.0)
        or (spo2 is not None and spo2 < 95)
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

    if temperature < 37.3:
        return "Normal"
    elif temperature < 38.5:
        return "Mild Fever"
    else:
        return "High Fever"


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

    if risk == "Medium":
        score -= 20
    elif risk == "High":
        score -= 40

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
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Moderate Risk"
    else:
        return "Needs Clinical Attention"


def parse_precautions_list(precaution_text):
    """
    Splits precautions string into a clean list of individual action items.
    """
    if not precaution_text or precaution_text == "Consult a healthcare professional.":
        return ["Consult a licensed healthcare professional for tailored medical advice.", "Monitor your vitals and symptom changes closely.", "Ensure adequate hydration and physical rest."]

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