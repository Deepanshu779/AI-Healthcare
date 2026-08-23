"""Create a reproducible audit of the benchmark symptom dataset."""
from __future__ import annotations

import json
from pathlib import Path

from ml.preprocess import build_feature_matrix, dataset_summary, load_dataset


def main() -> None:
    df = load_dataset()
    X, y, vocabulary = build_feature_matrix(df)
    summary = dataset_summary(df, X)
    summary["disease_examples"] = sorted(y.unique().tolist())[:20]
    summary["symptom_examples"] = vocabulary[:30]
    Path("results").mkdir(exist_ok=True)
    Path("results/dataset_audit.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
