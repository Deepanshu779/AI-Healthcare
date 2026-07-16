import joblib
import pandas as pd

# Load trained model
model = joblib.load("model/model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

# Load dataset
df = pd.read_csv("dataset/disease_sympts_prec_full.csv")


def predict_disease(symptoms):

    # Convert symptoms to vector
    symptom_vector = vectorizer.transform([symptoms])

    # Get probability for every disease
    probabilities = model.predict_proba(symptom_vector)[0]

    classes = model.classes_

    # Combine disease names with probabilities
    predictions = list(zip(classes, probabilities))

    # Sort by highest probability
    predictions.sort(key=lambda x: x[1], reverse=True)

    # Top 3 predictions
    top_predictions = predictions[:3]

    # Best prediction
    disease = top_predictions[0][0]

    confidence = round(top_predictions[0][1] * 100, 2)

    # Get precautions
    row = df[df["disease"] == disease]

    if not row.empty:
        precaution = row.iloc[0]["precautions"]
    else:
        precaution = "Consult a healthcare professional."

    return disease, confidence, precaution, top_predictions