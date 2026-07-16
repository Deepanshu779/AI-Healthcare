from flask import Flask, render_template, request
from predict import predict_disease
from groq_helper import get_ai_advice
from report_generator import generate_report

from utils import (
    calculate_bmi,
    bmi_status,
    calculate_risk,
    temperature_status,
    spo2_status,
    emergency_check,
    health_score,
    health_summary
)

app = Flask(__name__)


def parse_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # ===========================
    # Personal Information
    # ===========================

    name = request.form.get("name", "")

    age = parse_int(request.form.get("age"))

    gender = request.form.get("gender", "")

    # ===========================
    # Physical Information
    # ===========================

    height = parse_float(request.form.get("height"))

    weight = parse_float(request.form.get("weight"))

    temperature = request.form.get("temperature")

    spo2 = request.form.get("spo2")

    # ===========================
    # Symptoms
    # ===========================

    selected_symptoms = request.form.getlist("symptoms")

    other_symptoms = request.form.get(
        "other_symptoms",
        ""
    ).strip()

    if other_symptoms:
        selected_symptoms.append(other_symptoms)

    if not selected_symptoms:

        return render_template(
            "index.html",
            error="Please select at least one symptom."
        )

    symptoms = ", ".join(selected_symptoms)

    # ===========================
    # Medical Information
    # ===========================

    duration = request.form.get("duration") or "Not Provided"

    severity = request.form.get("severity") or "Mild"

    progress = request.form.get("progress") or "Not Provided"

    contact = request.form.get("contact") or "Not Provided"

    history_list = request.form.getlist("history")

    history = ", ".join(history_list) if history_list else "None"

    emergency = request.form.getlist("emergency")

    # ===========================
    # Health Calculations
    # ===========================

    bmi = calculate_bmi(height, weight)

    bmi_result = bmi_status(bmi)

    risk = calculate_risk(
        age,
        severity,
        temperature,
        spo2
    )

    temp_status = temperature_status(temperature)

    oxygen_status = spo2_status(spo2)

    emergency_detected = emergency_check(emergency)

    score = health_score(risk, bmi)

    summary = health_summary(score)

    # ===========================
    # Machine Learning Prediction
    # ===========================

    disease, confidence, precaution, predictions = predict_disease(symptoms)

    # Optional: avoid strong claims when confidence is low

    if confidence < 70:

        disease = "No single condition can be predicted confidently."

    # ===========================
    # AI Recommendation
    # ===========================

    try:

        ai_response = get_ai_advice(

            age=age,

            gender=gender,

            symptoms=symptoms,

            disease=disease,

            duration=duration,

            severity=severity,

            history=history,

            bmi=bmi,

            risk=risk,

            temperature=temperature,

            spo2=spo2,

            progress=progress,

            contact=contact,

            emergency=emergency

        )

    except Exception as e:

        ai_response = f"AI Error: {str(e)}"

    # ===========================
    # Generate PDF
    # ===========================

    try:
        generate_report(
            name=name,
            age=age,
            gender=gender,
            bmi=bmi,
            risk=risk,
            symptoms=symptoms,
            disease=disease,
            confidence=confidence,
            precaution=precaution,
            ai_response=ai_response
        )

        print("PDF generated successfully")

    except Exception as e:
        print("PDF error:", e)

    # ===========================
    # Result Page
    # ===========================

    return render_template(

        "result.html",

        name=name,

        age=age,

        gender=gender,

        height=height,

        weight=weight,

        bmi=bmi,

        bmi_status=bmi_result,

        risk=risk,

        temperature=temperature,

        temperature_status=temp_status,

        spo2=spo2,

        spo2_status=oxygen_status,

        health_score=score,

        health_summary=summary,

        emergency=emergency_detected,

        symptoms=symptoms,

        duration=duration,

        severity=severity,

        progress=progress,

        contact=contact,

        history=history,

        disease=disease,

        confidence=round(confidence, 2),

        precaution=precaution,

        ai_response=ai_response,

        predictions=predictions
    )


if __name__ == "__main__":
    app.run(debug=True)
