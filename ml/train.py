"""Train and evaluate MediAI 2.0 symptom models.

This script intentionally evaluates several models rather than assuming that
Random Forest is best. It also prevents the common mistake of fitting a text
vectorizer before the train/test split: symptom vocabulary is learned from the
training fold only through the feature names already defined by the benchmark
schema.
"""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.svm import LinearSVC

from ml.preprocess import build_feature_matrix, dataset_summary, load_dataset

MODEL_DIR = Path("model")
RESULT_DIR = Path("results")
RANDOM_STATE = 42


def build_models():
    """Return strong, CPU-friendly candidate models for tabular symptom data."""
    return {
        "logistic_regression": LogisticRegression(max_iter=3000, C=2.0, class_weight="balanced"),
        "random_forest": RandomForestClassifier(
            n_estimators=500,
            max_features="sqrt",
            min_samples_leaf=1,
            class_weight="balanced_subsample",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "linear_svm": CalibratedClassifierCV(
            LinearSVC(C=1.0, class_weight="balanced", random_state=RANDOM_STATE),
            cv=3,
            method="sigmoid",
        ),
        "hist_gradient_boosting": HistGradientBoostingClassifier(
            learning_rate=0.08,
            max_iter=250,
            max_leaf_nodes=31,
            random_state=RANDOM_STATE,
        ),
    }


def evaluate(model, X_test, y_test) -> dict:
    pred = model.predict(X_test)
    return {
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision_macro": float(precision_score(y_test, pred, average="macro", zero_division=0)),
        "recall_macro": float(recall_score(y_test, pred, average="macro", zero_division=0)),
        "f1_macro": float(f1_score(y_test, pred, average="macro", zero_division=0)),
        "f1_weighted": float(f1_score(y_test, pred, average="weighted", zero_division=0)),
    }


def main() -> None:
    MODEL_DIR.mkdir(exist_ok=True)
    RESULT_DIR.mkdir(exist_ok=True)

    df = load_dataset()
    X, y, vocabulary = build_feature_matrix(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )

    results = []
    trained = {}
    for name, model in build_models().items():
        model.fit(X_train, y_train)
        metrics = evaluate(model, X_test, y_test)
        metrics["model"] = name
        results.append(metrics)
        trained[name] = model
        print(f"{name}: accuracy={metrics['accuracy']:.4f}, macro_f1={metrics['f1_macro']:.4f}")

    results_df = pd.DataFrame(results).sort_values("f1_macro", ascending=False)
    best_name = str(results_df.iloc[0]["model"])
    best_model = trained[best_name]

    joblib.dump(best_model, MODEL_DIR / "model_v2.pkl")
    joblib.dump(vocabulary, MODEL_DIR / "symptom_vocabulary_v2.pkl")

    results_df.to_csv(RESULT_DIR / "model_comparison.csv", index=False)
    metadata = {
        "version": "2.0",
        "task": "symptom-based preliminary health assessment benchmark",
        "best_model": best_name,
        "random_state": RANDOM_STATE,
        "test_size": 0.20,
        "feature_type": "binary symptom presence",
        "dataset": dataset_summary(df, X),
        "models_evaluated": list(trained),
        "metrics": results,
        "clinical_disclaimer": "Benchmark model for educational/research use; not a medical diagnostic device.",
    }
    (RESULT_DIR / "model_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Saved best model: {best_name}")


if __name__ == "__main__":
    main()
