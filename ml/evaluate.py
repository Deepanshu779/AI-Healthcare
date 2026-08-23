"""Generate a detailed classification report and confusion matrix."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import StratifiedGroupKFold

from ml.preprocess import build_feature_matrix, load_dataset


def main() -> None:
    df = load_dataset()
    X, y, _ = build_feature_matrix(df)
    groups = df["disease"].astype(str) + "::" + df["symptom_list"].map(
        lambda x: "|".join(sorted(set(x)))
    )
    _, test_idx = next(
        StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42).split(X, y, groups=groups)
    )

    model = joblib.load("model/model_v2.pkl")
    # Retrain on the complementary fold so this report evaluates the same
    # leakage-aware split family used by ml/train.py.
    train_idx = X.index.difference(X.index[test_idx])
    model.fit(X.loc[train_idx], y.loc[train_idx])
    pred = model.predict(X.iloc[test_idx])
    y_test = y.iloc[test_idx]

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
