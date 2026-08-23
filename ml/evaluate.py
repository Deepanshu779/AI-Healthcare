"""Generate a detailed classification report and confusion matrix."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

from ml.preprocess import build_feature_matrix, load_dataset


def main() -> None:
    df = load_dataset()
    X, y, _ = build_feature_matrix(df)
    model = joblib.load("model/model_v2.pkl")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    Path("results").mkdir(exist_ok=True)
    report = classification_report(y_test, pred, zero_division=0, output_dict=True)
    Path("results/classification_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    labels = sorted(y.unique())
    cm = confusion_matrix(y_test, pred, labels=labels)
    pd.DataFrame(cm, index=labels, columns=labels).to_csv("results/confusion_matrix.csv")

    fig, ax = plt.subplots(figsize=(16, 14))
    ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels).plot(
        ax=ax, xticks_rotation=90, colorbar=False
    )
    fig.tight_layout()
    fig.savefig("results/confusion_matrix.png", dpi=180)
    plt.close(fig)

    print("Evaluation artifacts written to results/.")


if __name__ == "__main__":
    main()
