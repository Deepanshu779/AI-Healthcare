# MediAI 2.0

MediAI 2.0 is an AI-assisted healthcare screening and health-companion web application built with Flask and machine learning. It combines structured symptom assessment, safety-first triage, vitals and BMI analysis, an AI health assistant, offline ML screening, and downloadable assessment reports.

> **Safety disclaimer:** MediAI 2.0 is an educational/research screening project. It is not a medical diagnosis tool, emergency service, or substitute for a qualified healthcare professional.

## Product identity

**Project name:** MediAI 2.0  
**Product type:** AI Health Companion + ML Screening Application  
**Current development branch:** `feature/mediai-2-0-ml-core`

## Core experience

- AI health assistant with conversational symptom guidance
- Focused follow-up questions and symptom organization
- Safety-first urgent/emergency escalation layer
- Structured symptom assessment
- Temperature and SpO₂ monitoring
- BMI calculation
- Offline machine-learning screening
- Differential model outputs for transparency
- Explainable assessment summary
- AI-generated educational guidance
- Printable/downloadable assessment report
- Mobile-responsive healthcare UI

## MediAI 2.0 ML foundation

The 2.0 ML pipeline upgrades the original classifier into a more rigorous, safety-aware framework.

- Structured binary symptom feature matrix
- Dataset-quality audit
- Multiple model benchmarking: Logistic Regression, Random Forest, calibrated Linear SVM, and HistGradientBoosting
- Leakage-aware StratifiedGroupKFold evaluation
- Accuracy, macro precision, macro recall, macro F1, and weighted F1
- Reproducible model metadata and model card
- Backward-compatible prediction interface
- Explicit distinction between **model probability** and clinical certainty

## Safety-first assessment

- Emergency/urgent triage runs before routine AI guidance
- Abnormal SpO₂, very high temperature, critical severity, and selected warning symptoms can trigger escalation
- Emergency/urgent results are not treated as routine self-care advice
- The safety engine is a project heuristic and is not a validated clinical triage protocol

## Project structure

```text
MediAI-2.0/
├── app.py
├── predict.py
├── chat_service.py
├── groq_helper.py
├── utils.py
├── safety_engine.py
├── report_generator.py
├── MODEL_CARD.md
├── ml/
│   ├── __init__.py
│   ├── preprocess.py
│   ├── audit_dataset.py
│   ├── train.py
│   └── evaluate.py
├── tests/
│   └── test_safety_engine.py
├── dataset/
│   └── disease_sympts_prec_full.csv
├── model/
│   ├── model.pkl
│   └── vectorizer.pkl
├── results/
│   └── generated ML audit/training/evaluation artifacts
├── static/
└── templates/
```

## Local setup

Create a virtual environment and install dependencies:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
```

Groq is optional. Keep API keys in your local environment; **never commit `.env` or API keys to GitHub**.

## Train MediAI 2.0

From the project root:

```bash
python -m ml.audit_dataset
python -m ml.train
python -m ml.evaluate
```

Training creates the 2.0 model artifacts under `model/`. Until those artifacts exist, `predict.py` keeps the existing model path available so the application remains functional.

## Run the application

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

### Main routes

- `/` — MediAI 2.0 full health assessment
- `/assistant` — MediAI 2.0 AI Health Assistant
- `/predict` — assessment submission endpoint
- `/api/chat` — AI assistant endpoint

## Run tests

```bash
pytest -q
```

## Technology stack

- Python / Flask
- Pandas / NumPy
- scikit-learn
- Joblib
- Groq (optional)
- ReportLab
- Matplotlib
- Pytest

## Responsible use

The benchmark dataset is not a substitute for clinically collected patient data. Model performance on this dataset does not establish clinical effectiveness. Do not use a MediAI 2.0 prediction as the sole basis for treatment or medication decisions. For severe, rapidly worsening, or emergency symptoms, seek professional medical care regardless of the model output.

## Review before main

This branch is intentionally being used as the **MediAI 2.0 review version**. Changes should be reviewed and tested here first. The `main` branch is not modified by this development work until the project owner explicitly approves the changes and merges them.
