"""Safety-first triage layer for MediAI.

This module is deliberately conservative. It does not diagnose or prescribe;
it only flags user-selected emergency symptoms and abnormal vital readings so
that routine ML output cannot distract from urgent care guidance.
"""
from __future__ import annotations


def assess_safety(emergency_symptoms=None, temperature=None, spo2=None, severity=None) -> dict:
    emergency_symptoms = [str(x).strip() for x in (emergency_symptoms or []) if str(x).strip()]
    try:
        temp = float(temperature) if temperature not in (None, "") else None
    except (TypeError, ValueError):
        temp = None
    try:
        oxygen = float(spo2) if spo2 not in (None, "") else None
    except (TypeError, ValueError):
        oxygen = None

    alerts = []
    if emergency_symptoms:
        alerts.append("User-selected emergency warning symptom(s) require prompt professional evaluation.")
    if oxygen is not None and oxygen < 92:
        alerts.append("Recorded SpO₂ is below 92%; urgent medical assessment is appropriate.")
    if temp is not None and temp >= 40:
        alerts.append("Recorded temperature is very high; urgent medical assessment is appropriate.")
    if str(severity or "").strip().lower() == "critical":
        alerts.append("Critical symptom severity was reported.")

    if emergency_symptoms or (oxygen is not None and oxygen < 92) or (temp is not None and temp >= 40) or str(severity or "").lower() == "critical":
        level = "Emergency"
        action = "Seek immediate professional/emergency medical care. Do not rely on the AI assessment as a substitute for clinical evaluation."
    elif (oxygen is not None and oxygen < 95) or (temp is not None and temp >= 38.5) or str(severity or "").lower() == "severe":
        level = "Urgent"
        action = "Arrange prompt medical evaluation, especially if symptoms are worsening or persistent."
    else:
        level = "Routine"
        action = "Continue with the educational assessment while monitoring symptoms and seeking care if they worsen."

    return {"level": level, "alerts": alerts, "action": action}
