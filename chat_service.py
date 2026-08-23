from __future__ import annotations

import os
from typing import Any
from dotenv import load_dotenv

try:
    from groq import Groq
except ImportError:
    Groq = None

load_dotenv()

SYSTEM_PROMPT = """You are MediAI 2.0, an empathetic, safety-first educational health assistant.

YOUR JOB
- Have a useful conversation, not a one-shot diagnosis.
- First understand the user's concern, then ask only the most useful 1–3 follow-up questions.
- When enough information is available, summarize the reported symptoms, explain reasonable possibilities in general educational terms, identify warning signs, and suggest an appropriate next step.
- Never state that a disease is confirmed and never present an ML prediction as a diagnosis.

SAFETY
- If the user describes severe difficulty breathing, severe chest pain/pressure, blue/grey lips, loss of consciousness, seizure, severe bleeding, severe confusion, or another obvious emergency, put urgent professional/emergency care first. Do not bury it in a long explanation.
- Do not prescribe prescription medicines, change prescribed treatment, or give dosing instructions.
- Do not invent tests, vitals, medical history, medications, allergies, or examination findings.
- Avoid false precision and avoid claiming clinical-grade accuracy.
- If information is insufficient, say what is missing rather than guessing.

CONVERSATION DESIGN
- Ask one focused question at a time when possible.
- Useful context can include age range, symptom onset/duration, severity, progression, location/character of symptoms, fever, SpO2 when respiratory symptoms are present, major medical history, medications/allergies, and relevant exposures.
- Do not interrogate the user with a long checklist.
- Mirror the user's language level. Keep technical terms explained simply.
- If the user asks a general health question without symptoms, answer directly and safely.

RESPONSE STYLE
- Use short sections and bullets.
- When asking questions, finish with the questions instead of overwhelming the user with advice.
- When giving an assessment, use these headings when useful:
  "What I understand", "What could be going on", "What to watch for", "What to do next".
- Make it clear that MediAI is educational and not a substitute for a clinician.
"""

EMERGENCY_TERMS = [
    "can't breathe", "cannot breathe", "difficulty breathing", "severe shortness of breath",
    "severe chest pain", "chest pressure", "blue lips", "blue face", "fainted", "unconscious",
    "seizure", "severe bleeding", "vomiting blood", "coughing blood", "stroke symptoms"
]


def _offline_reply(message: str) -> str:
    """Small deterministic fallback so the assistant remains useful without an API."""
    text = message.lower()
    if any(term in text for term in EMERGENCY_TERMS):
        return (
            "### Please seek urgent medical care\n\n"
            "What you described can be a warning sign that needs prompt in-person assessment. "
            "Please contact local emergency medical services or go to the nearest emergency department, "
            "especially if symptoms are severe or getting worse. Chat should not delay emergency care.\n\n"
            "If you are safe right now, I can help you organize the symptoms for a clinician afterward."
        )

    questions = []
    if not any(k in text for k in ["year", "years old", "age"]):
        questions.append("How old are you?")
    if not any(k in text for k in ["day", "days", "week", "weeks", "hour", "hours", "month", "months"]):
        questions.append("When did this start?")
    if not any(k in text for k in ["mild", "moderate", "severe", "1/10", "2/10", "3/10", "4/10", "5/10", "6/10", "7/10", "8/10", "9/10", "10/10"]):
        questions.append("How severe is it from 1–10?")

    first = questions[:2]
    question_text = "\n".join(f"- {q}" for q in first) if first else "- What has changed since the symptoms began?"
    return (
        "### Let's work through it\n\n"
        "I can help you organize the symptoms, explain general possibilities, and look for warning signs. "
        "I cannot confirm a diagnosis from chat alone.\n\n"
        "**A couple of things will help me understand the situation:**\n" + question_text +
        "\n\nIf symptoms are severe, rapidly worsening, or concerning, please seek professional medical evaluation."
    )


def _clean_history(history: list[dict[str, Any]] | None) -> list[dict[str, str]]:
    safe: list[dict[str, str]] = []
    for item in (history or [])[-10:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = str(item.get("content", "")).strip()[:3000]
        if role in {"user", "assistant"} and content:
            safe.append({"role": role, "content": content})
    return safe


def chat_response(message: str, history: list[dict[str, Any]] | None = None) -> str:
    message = str(message or "").strip()
    if not message:
        return "Please describe what you are experiencing or ask a health question."
    if len(message) > 3000:
        return "Please keep your message under 3000 characters."

    # Fast local safety gate before any external model call.
    if any(term in message.lower() for term in EMERGENCY_TERMS):
        return _offline_reply(message)

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or Groq is None:
        return _offline_reply(message)

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *_clean_history(history), {"role": "user", "content": message}],
            temperature=0.2,
            max_tokens=850,
        )
        reply = response.choices[0].message.content.strip()
        return reply or _offline_reply(message)
    except Exception as exc:
        print(f"MediAI chat fallback: {exc}")
        return _offline_reply(message)
