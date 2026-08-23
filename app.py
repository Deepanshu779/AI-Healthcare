import os
from flask import Flask, jsonify, render_template, request
from predict import predict_disease
from groq_helper import get_ai_advice
from chat_service import chat_response
from report_generator import generate_report
from safety_engine import assess_safety

from utils import (calculate_bmi, bmi_status, calculate_risk, temperature_status,
                   spo2_status, emergency_check, health_score, health_summary,
                   parse_precautions_list, parse_ai_sections)

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
    return render_template("index.html", has_api_key=bool(os.getenv("GROQ_API_KEY", "").strip()))


@app.route("/assistant")
def assistant():
    return render_template("assistant.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"reply": "Please describe what you are experiencing or ask a health question."}), 400
    if len(message) > 3000:
        return jsonify({"reply": "Please keep your message under 3000 characters."}), 400
    history = payload.get("history", [])
    if not isinstance(history, list):
        history = []
    return jsonify({"reply": chat_response(message, history)})


@app.route("/predict", methods=["POST"])
def predict():
    name = request.form.get("name", "Patient").strip()
    age = parse_int(request.form.get("age"), 30)
    gender = request.form.get("gender", "Not Specified")
    height = parse_float(request.form.get("height"), 170.0)
    weight = parse_float(request.form.get("weight"), 65.0)
    temperature = request.form.get("temperature", "").strip()
    spo2 = request.form.get("spo2", "").strip()

    selected_symptoms = request.form.getlist("symptoms")
    other_symptoms = request.form.get("other_symptoms", "").strip()
    if other_symptoms:
        existing = {x.lower() for x in selected_symptoms}
        for value in other_symptoms.split(","):
            clean = value.strip().lower()
            if clean and clean not in existing:
                selected_symptoms.append(clean)
                existing.add(clean)
    if not selected_symptoms:
        return render_template("index.html", error="Please select at least one symptom or describe your symptoms.", has_api_key=bool(os.getenv("GROQ_API_KEY", "").strip()))

    symptoms_str = ", ".join(selected_symptoms)
    duration = request.form.get("duration") or "1-3 Days"
    severity = request.form.get("severity") or "Mild"
    progress = request.form.get("progress") or "Stable"
    contact = request.form.get("contact") or "No known exposure"
    history_values = request.form.getlist("history")
    history = ", ".join(history_values) if history_values else "None reported"
    emergency = request.form.getlist("emergency")

    bmi = calculate_bmi(height, weight)
    bmi_result = bmi_status(bmi)
    risk = calculate_risk(age, severity, temperature, spo2)
    temp_status = temperature_status(temperature)
    oxygen_status = spo2_status(spo2)
    safety = assess_safety(emergency_symptoms=emergency, symptoms=selected_symptoms, temperature=temperature, spo2=spo2, severity=severity, age=age)
    emergency_detected = safety["level"] == "Emergency" or emergency_check(emergency)
    score = health_score(risk, bmi)
    summary = health_summary(score)

    disease, confidence, precaution, predictions = predict_disease(symptoms_str)
    disease_display = "Inconclusive / Overlapping Condition" if confidence < 35 else disease

    if safety["level"] in {"Emergency", "Urgent"}:
        ai_response = (
            "## Safety / Triage Alert\n"
            f"**Level: {safety['level']}**\n\n"
            + "\n".join(f"- {alert}" for alert in safety["alerts"])
            + f"\n\n**Recommended action:** {safety['action']}\n\n"
            "## Important Clinical Note\nThis is an educational screening system, not a diagnosis. Professional evaluation should take priority."
        )
    else:
        try:
            ai_response = get_ai_advice(age=age, gender=gender, symptoms=symptoms_str, disease=disease_display,
                                        duration=duration, severity=severity, history=history, bmi=bmi, risk=risk,
                                        temperature=temperature, spo2=spo2, progress=progress, contact=contact,
                                        emergency=emergency)
        except Exception as exc:
            ai_response = f"Clinical Assessment: {exc}"

    precautions_list = parse_precautions_list(precaution)
    ai_sections = parse_ai_sections(ai_response)
    has_api_key = bool(os.getenv("GROQ_API_KEY", "").strip())

    try:
        generate_report(name=name, age=age, gender=gender, height=height, weight=weight, bmi=bmi, risk=risk,
                        temperature=temperature, temperature_status=temp_status, spo2=spo2, spo2_status=oxygen_status,
                        health_score=score, health_summary=summary, symptoms=symptoms_str, duration=duration,
                        severity=severity, progress=progress, contact=contact, history=history, emergency=emergency,
                        disease=disease_display, confidence=confidence, precaution=precaution, ai_response=ai_response)
    except Exception as exc:
        print("PDF generation error:", exc)

    return render_template("result.html", name=name, age=age, gender=gender, height=height, weight=weight,
                           bmi=bmi, bmi_status=bmi_result, risk=risk, temperature=temperature or "Not Provided",
                           temperature_status=temp_status, spo2=spo2 or "Not Provided", spo2_status=oxygen_status,
                           health_score=score, health_summary=summary, emergency_detected=emergency_detected,
                           emergency_list=emergency, safety_level=safety["level"], safety_alerts=safety["alerts"],
                           safety_action=safety["action"], symptoms=symptoms_str, selected_symptoms=selected_symptoms,
                           duration=duration, severity=severity, progress=progress, contact=contact, history=history,
                           disease=disease_display, confidence=round(confidence, 1), precaution=precaution,
                           precautions_list=precautions_list, ai_response=ai_response, ai_sections=ai_sections,
                           predictions=predictions, has_api_key=has_api_key)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
