"""Safety-first triage rules for MediAI.

This module is deliberately deterministic. It does not diagnose disease; it
flags combinations of user-entered red-flag symptoms and vital measurements
that warrant urgent human assessment.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class SafetyAssessment:
    level: str
    score: int
    alerts: list[str]
    actions: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


EMERGENCY_TERMS = {
    "chest pain", "chest pressure", "severe breathing difficulty",
    "difficulty breathing", "blue lips", "loss of consciousness",
    "fainting", "seizure", "severe bleeding", "suicidal thoughts",
}

URGENT_TERMS = {
    "persistent vomiting", "confusion", "severe dehydration",
    "severe abdominal pain", "new weakness", "difficulty speaking",
}


def _contains_any(values: list[str], terms: set[str]) -> list[str]:
    text = " ".join(str(v).lower().replace("_", " ") for v in values)
    return sorted(term for term in terms if term in text)


def assess_safety(*, symptoms=None, emergency=None, temperature=None, spo2=None, age=0) -> SafetyAssessment:
    values = list(symptoms or []) + list(emergency or [])
    alerts: list[str] = []
    score = 0

    emergency_hits = _contains_any(values, EMERGENCY_TERMS)
    urgent_hits = _contains_any(values, URGENT_TERMS)

    if emergency_hits:
        score += 80
        alerts.append("Red-flag symptom(s): " + ", ".join(emergency_hits) + ".")
    if urgent_hits:
        score += 35
        alerts.append("Urgent symptom(s): " + ", ".join(urgent_hits) + ".")

    try:
        if spo2 is not None and float(spo2) < 92:
            score += 90
            alerts.append(f"SpO2 {spo2}% is critically low and needs urgent medical assessment.")
        elif spo2 is not None and float(spo2) < 95:
            score += 25
            alerts.append(f"SpO2 {spo2}% is below the usual healthy range; repeat and monitor carefully.")
    except (TypeError, ValueError):
        pass

    try:
        if temperature is not None and float(temperature) >= 40:
            score += 60
            alerts.append(f"Temperature {temperature}°C is very high.")
        elif temperature is not None and float(temperature) >= 39:
            score += 25
            alerts.append(f"Temperature {temperature}°C indicates high fever.")
    except (TypeError, ValueError):
        pass

    try:
        if int(age) >= 65:
            score += 10
    except (TypeError, ValueError):
        pass

    if score >= 70:
        level = "Emergency"
        actions = [
            "Seek emergency medical care now.",
            "Do not rely on the predicted condition as a diagnosis.",
            "If symptoms are rapidly worsening, contact local emergency services.",
        ]
    elif score >= 25:
        level = "Urgent"
        actions = [
            "Arrange prompt assessment by a qualified healthcare professional.",
            "Repeat abnormal vitals when possible and record the trend.",
        ]
    else:
        level = "Routine"
        actions = [
            "Continue symptom and vital monitoring.",
            "Seek clinical advice if symptoms persist, worsen, or new red flags appear.",
        ]

    return SafetyAssessment(level, min(score, 100), alerts, actions)
