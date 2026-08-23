"""Dataset preparation for MediAI 2.0.

Converts the symptom-list column into a binary symptom feature matrix.
The original dataset is retained as the source benchmark; no clinical claims
are made about its suitability for diagnosis.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pandas as pd


DATASET_PATH = Path("dataset/disease_sympts_prec_full.csv")


def normalize_symptom(value: object) -> str:
    """Normalize one symptom token while preserving its meaning."""
    text = str(value or "").strip().lower()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_,")


def parse_symptoms(value: object) -> list[str]:
    """Parse the comma-separated symptom field into normalized tokens."""
    if pd.isna(value):
        return []
    return [s for s in (normalize_symptom(x) for x in str(value).split(",")) if s]


def load_dataset(path: str | Path = DATASET_PATH) -> pd.DataFrame:
    """Load and minimally validate the benchmark dataset."""
    df = pd.read_csv(path)
    required = {"disease", "symptoms"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    df = df.copy()
    df["disease"] = df["disease"].astype(str).str.strip()
    df["symptom_list"] = df["symptoms"].apply(parse_symptoms)
    df = df[df["disease"].ne("") & df["symptom_list"].map(bool)].copy()
    return df


def build_feature_matrix(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """Build one binary feature per unique symptom."""
    vocabulary = sorted({symptom for row in df["symptom_list"] for symptom in row})
    X = pd.DataFrame(0, index=df.index, columns=vocabulary, dtype="int8")
    for idx, symptoms in df["symptom_list"].items():
        X.loc[idx, list(set(symptoms))] = 1
    y = df["disease"].copy()
    return X, y, vocabulary


def dataset_summary(df: pd.DataFrame, X: pd.DataFrame) -> dict:
    """Return reproducible dataset-quality statistics for the model card."""
    symptom_signatures = df["symptom_list"].map(lambda x: "|".join(sorted(set(x))))
    duplicate_rows = int(df.duplicated(subset=["disease", "symptoms"]).sum())
    duplicate_signatures = int(pd.DataFrame({"disease": df["disease"], "signature": symptom_signatures}).duplicated().sum())
    return {
        "rows_after_cleaning": int(len(df)),
        "disease_count": int(df["disease"].nunique()),
        "symptom_count": int(X.shape[1]),
        "duplicate_raw_rows": duplicate_rows,
        "duplicate_disease_symptom_signatures": duplicate_signatures,
        "missing_symptom_rows": int(df["symptom_list"].map(len).eq(0).sum()),
        "class_distribution": {str(k): int(v) for k, v in df["disease"].value_counts().to_dict().items()},
    }
