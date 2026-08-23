"""Backward-compatible MediAI prediction interface.

MediAI 2.0 uses the structured symptom model when its trained artifacts are
available. The original TF-IDF model remains as a safe fallback so existing
deployments continue to start before the new model is trained.
"""
from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

MODEL_V2 = Path("model/model_v2.pkl")
VOCAB_V2 = Path("model/symptom_vocabulary_v2.pkl")

if MODEL_V2.exists() and VOCAB_V2.exists():
    from predict_v2 import predict_disease_v2

    def predict_disease(symptoms):
        symptom_list = [s.strip() for s in str(symptoms).split(",") if s.strip()]
        result = predict_disease_v2(symptom_list, top_k=5)
        predictions = [
            (item["disease"], item["model_probability"] / 100.0)
            for item in result["predictions"]
        ]
        return (
            result["disease"],
            result["model_probability"],
            result["precaution"],
            predictions,
        )
else:
    # Legacy compatibility until the MediAI 2.0 model is trained.
    model = joblib.load("model/model.pkl")
    vectorizer = joblib.load("model/vectorizer.pkl")
    df = pd.read_csv("dataset/disease_sympts_prec_full.csv")

    def predict_disease(symptoms):
        symptom_vector = vectorizer.transform([symptoms])
        probabilities = model.predict_proba(symptom_vector)[0]
        classes = model.classes_
        predictions = list(zip(classes, probabilities))
        predictions.sort(key=lambda x: x[1], reverse=True)
        top_predictions = predictions[:3]
        disease = top_predictions[0][0]
        probability = round(top_predictions[0][1] * 100, 2)
        row = df[df["disease"] == disease]
        precaution = row.iloc[0]["precautions"] if not row.empty else "Consult a healthcare professional."
        return disease, probability, precaution, top_predictions
