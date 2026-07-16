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
        return "Healthy"

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
    except:
        age = 0

    severity = severity.lower()

    try:
        temperature = float(temperature) if temperature else None
    except:
        temperature = None

    try:
        spo2 = int(spo2) if spo2 else None
    except:
        spo2 = None

    # High Risk
    if (
        age >= 60
        or severity == "severe"
        or (temperature is not None and temperature >= 39)
        or (spo2 is not None and spo2 < 92)
    ):
        return "High"

    # Medium Risk
    elif (
        age >= 40
        or severity == "moderate"
        or (temperature is not None and temperature >= 38)
        or (spo2 is not None and spo2 < 95)
    ):
        return "Medium"

    return "Low"


def emergency_check(emergency_list):
    """
    Returns True if emergency symptoms are selected
    """

    if emergency_list is None:
        return False

    return len(emergency_list) > 0


def temperature_status(temperature):
    """
    Return temperature status
    """

    try:
        temperature = float(temperature)
    except:
        return "Not Provided"

    if temperature < 37.5:
        return "Normal"

    elif temperature < 39:
        return "Fever"

    else:
        return "High Fever"


def spo2_status(spo2):
    """
    Return oxygen saturation status
    """

    try:
        spo2 = int(spo2)
    except:
        return "Not Provided"

    if spo2 >= 95:
        return "Normal"

    elif spo2 >= 92:
        return "Low"

    else:
        return "Critical"


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

    return max(score, 0)


def health_summary(score):
    """
    Return health summary based on score
    """

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Good"

    elif score >= 60:
        return "Fair"

    else:
        return "Needs Medical Attention"