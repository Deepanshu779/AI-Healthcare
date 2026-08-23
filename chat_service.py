from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

try:
    from groq import Groq
except ImportError:
    Groq = None

load_dotenv()

SYSTEM_PROMPT = """You are MediAI, an empathetic educational health assistant.

Safety rules:
- Never claim to diagnose a user or state that a disease is confirmed.
- Do not prescribe prescription medicines or tell users to change prescribed treatment.
- Help users organize symptoms, explain general health information, suggest appropriate next steps, and identify warning signs.
- If the user describes emergency warning signs such as severe difficulty breathing, severe chest pain/pressure, blue lips, loss of consciousness, seizure, severe bleeding, or severe confusion, prioritize urgent professional/emergency care before explanations.
- Do not invent test results, medical history, vital signs, or facts not provided by the user.
- Ask concise follow-up questions when important context is missing: age range, duration, severity, progression, temperature/SpO2 if relevant, and major medical history.
- Keep responses easy to scan: short paragraphs, bullets, and clear headings.
- Be calm and non-alarming. This is educational guidance and not a substitute for a clinician.
"""


def _offline_reply(message: str) -> str:
    text = message.lower()
    emergency_terms = ["can't breathe", "cannot breathe", "difficulty breathing", "severe chest pain", "chest pressure", "blue lips", "fainted", "unconscious", "seizure", "severe bleeding"]
    if any(term in text for term in emergency_terms):
        return ("### Please seek urgent medical care\n\n"
                "What you described can be a warning sign that needs prompt in-person assessment. "
                "Please contact local emergency medical services or go to the nearest emergency department, especially if symptoms are severe or worsening.\n\n"
                "I can help explain the symptoms afterward, but chat should not delay emergency care.")

    questions = []
    if not any(k in text for k in ["year", "age"]):
        questions.append("your age")
    if not any(k in text for k in ["day", "week", "hour", "month"]):
        questions.append("when it started")
    if not any(k in text for k in ["mild", "moderate", "severe"]):
        questions.append("how severe it is")
    suffix = "\n\nTo make the guidance more useful, tell me " + ", ".join(questions[:3]) + "." if questions else ""
    return ("### I can help you work through this\n\n"
            "I can help organize the symptoms you described, explain common possibilities in general terms, and point out warning signs to watch for. "
            "I cannot confirm a diagnosis from chat alone." + suffix +
            "\n\nIf symptoms are severe, rapidly worsening, or concerning, please seek professional medical evaluation.")


def chat_response(message: str, history: list[dict[str, Any]] | None = None) -> str:
    message = str(message or "").strip()
    if not message:
        return "Please describe what you are experiencing or ask a health question."

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or Groq is None:
        return _offline_reply(message)

    try:
        client = Groq(api_key=api_key)
        safe_history = []
        for item in (history or [])[-10:]:
            role = item.get("role")
            content = str(item.get("content", ""))[:3000]
            if role in {"user", "assistant"} and content:
                safe_history.append({"role": role, "content": content})
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *safe_history, {"role": "user", "content": message}],
            temperature=0.2,
            max_tokens=700,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return _offline_reply(message)
