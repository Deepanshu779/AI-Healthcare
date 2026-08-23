"""Safety-first deterministic triage layer for MediAI.

This module does not diagnose or prescribe. It prioritizes urgent human-care
signals before routine ML/LLM guidance can be presented.
"""
from __future__ import annotations


def assess_safety(emergency_symptoms=None, symptoms=None, temperature=None, spo2=None, severity=None, age=None) -> dict:
    emergency_symptoms = [str(x).strip() for x in (emergency_symptoms or []) if str(x).strip()]
    symptoms = [str(x).strip().lower().replace("_", " ") for x in (symptoms or []) if str(x).strip()]
    all_symptoms = emergency_symptoms + symptoms

    try:
        temp = float(temperature) if temperature not in (None, "") else None
    except (TypeError, ValueError):
        temp = None
    try:
        oxygen = float(spo2) if spo2 not in (None, "") else None
    except (TypeError, ValueError):
        oxygen = None

    alerts = []
    red_flags = {"chest pain", "chest pressure", "difficulty breathing", "severe breathing difficulty",
                 "blue lips", "loss of consciousness", "fainting", "seizure", "severe bleeding",
                 "difficulty speaking", "new weakness"}
    matched = sorted(flag for flag in red_flags if any(flag in value for value in all_symptoms))
    if matched:
        alerts.append("Red-flag symptom(s): " + ", ".join(matched) + ".")
    if emergency_symptoms:
        alerts.append("User-selected emergency warning symptom(s) require prompt professional evaluation.")
    if oxygen is not None and oxygen < 92:
        alerts.append("Recorded SpO₂ is below 92%; urgent medical assessment is appropriate.")
    elif oxygen is not None and oxygen < 95:
        alerts.append("Recorded SpO₂ is below the usual healthy range; repeat and monitor carefully.")
    if temp is not None and temp >= 40:
        alerts.append("Recorded temperature is very high; urgent medical assessment is appropriate.")
    elif temp is not None and temp >= 39:
        alerts.append("Recorded temperature indicates high fever.")
    if str(severity or "").strip().lower() == "critical":
        alerts.append("Critical symptom severity was reported.")

    emergency = bool(matched or emergency_symptoms or (oxygen is not None and oxygen < 92) or
                     (temp is not None and temp >= 40) or str(severity or "").lower() == "critical")
    urgent = bool((oxygen is not None and oxygen < 95) or (temp is not None and temp >= 38.5) or
                  str(severity or "").lower() in {"severe", "moderate"})

    if emergency:
        level = "Emergency"
        action = "Seek immediate professional/emergency medical care. Do not rely on the AI assessment as a substitute for clinical evaluation."
    elif urgent:
        level = "Urgent"
        action = "Arrange prompt medical evaluation, especially if symptoms are worsening or persistent."
    else:
        level = "Routine"
        action = "Continue with the educational assessment while monitoring symptoms and seeking care if they worsen."

    return {"level": level, "alerts": alerts, "action": action}
