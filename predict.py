from pathlib import Path

import joblib
import pandas as pd


# =========================================================
# MediAI 2.0 — Disease Prediction Service
# =========================================================

# Project root
BASE_DIR = Path(__file__).resolve().parent

# Model paths
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "model.pkl"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"

# Dataset path
DATASET_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "disease_sympts_prec_full.csv"
)


# =========================================================
# Load Model Resources
# =========================================================

model = joblib.load(MODEL_PATH)

vectorizer = joblib.load(VECTORIZER_PATH)

df = pd.read_csv(DATASET_PATH)


# =========================================================
# Prediction
# =========================================================

def predict_disease(symptoms):
    """
    Predict the most likely disease from the
    provided symptoms.

    Returns:
        disease
        confidence
        precaution
        top_predictions
    """

    # -----------------------------------------------------
    # Convert symptoms into model-compatible vector
    # -----------------------------------------------------

    symptom_vector = vectorizer.transform(
        [symptoms]
    )


    # -----------------------------------------------------
    # Calculate probability for every disease
    # -----------------------------------------------------

    probabilities = model.predict_proba(
        symptom_vector
    )[0]

    classes = model.classes_


    # -----------------------------------------------------
    # Combine disease names with probabilities
    # -----------------------------------------------------

    predictions = list(
        zip(
            classes,
            probabilities
        )
    )


    # -----------------------------------------------------
    # Sort from highest to lowest probability
    # -----------------------------------------------------

    predictions.sort(
        key=lambda item: item[1],
        reverse=True
    )


    # -----------------------------------------------------
    # Keep top 3 predictions
    # -----------------------------------------------------

    top_predictions = predictions[:3]


    # -----------------------------------------------------
    # Best prediction
    # -----------------------------------------------------

    disease = top_predictions[0][0]

    confidence = round(
        float(top_predictions[0][1]) * 100,
        2
    )


    # -----------------------------------------------------
    # Get precautions from dataset
    # -----------------------------------------------------

    row = df[
        df["disease"] == disease
    ]


    if not row.empty:

        precaution = row.iloc[0][
            "precautions"
        ]

    else:

        precaution = (
            "Consult a healthcare professional."
        )


    # -----------------------------------------------------
    # Return result
    # -----------------------------------------------------

    return (
        disease,
        confidence,
        precaution,
        top_predictions
    )