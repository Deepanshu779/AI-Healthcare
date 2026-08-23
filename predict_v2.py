"""MediAI 2.0 prediction engine.

Uses the structured symptom vocabulary created by ml.preprocess.py and the
best model trained by ml/train.py. The returned probability is explicitly
named model probability; it is not presented as a clinical diagnosis or a
validated medical confidence score.
"""
from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from ml.preprocess import normalize_symptom

MODEL_PATH = Path("model/model_v2.pkl")
VOCAB_PATH = Path("model/symptom_vocabulary_v2.pkl")
DATASET_PATH = Path("dataset/disease_sympts_prec_full.csv")

_model = None
_vocabulary = None
_dataset = None


def _load():
    global _model, _vocabulary, _dataset
    if _model is None:
        _model = joblib.load(MODEL_PATH)
        _vocabulary = joblib.load(VOCAB_PATH)
        _dataset = pd.read_csv(DATASET_PATH)


def _feature_frame(symptoms: list[str]) -> pd.DataFrame:
    _load()
    normalized = {normalize_symptom(s) for s in symptoms if normalize_symptom(s)}
    row = {feature: int(feature in normalized) for feature in _vocabulary}
    return pd.DataFrame([row], columns=_vocabulary)


def predict_disease_v2(symptoms: list[str], top_k: int = 5) -> dict:
    """Return ranked model results and contributing symptoms."""
    if not symptoms:
        raise ValueError("At least one symptom is required.")

    X = _feature_frame(symptoms)
    probabilities = _model.predict_proba(X)[0]
    classes = list(_model.classes_)
    ranked = sorted(zip(classes, probabilities), key=lambda item: item[1], reverse=True)
    top = ranked[: max(1, min(top_k, len(ranked)))]

    selected = {normalize_symptom(s) for s in symptoms}
    known = [s for s in selected if s in set(_vocabulary)]
    unknown = sorted(selected - set(_vocabulary))

    primary = top[0]
    rows = _dataset[_dataset["disease"] == primary[0]]
    precaution = rows.iloc[0].get("precautions", "") if not rows.empty else ""

    return {
        "disease": primary[0],
        "model_probability": round(float(primary[1]) * 100, 2),
        "predictions": [
            {"disease": disease, "model_probability": round(float(prob) * 100, 2)}
            for disease, prob in top
        ],
        "known_symptoms": sorted(known),
        "unrecognized_symptoms": unknown,
        "precaution": str(precaution) if pd.notna(precaution) else "",
        "model_note": "Model probability is an algorithmic estimate, not a clinical diagnosis or validated medical confidence score.",
    }
