# 🩺 MediAI 2.0

<p align="center">
  <strong>AI-Powered Healthcare Assessment & Clinical Decision-Support Demo</strong><br/>
  A Flask + Machine Learning web application for symptom-based health assessment, vitals analysis, AI-assisted guidance, and report generation.
</p>

<p align="center">
  <a href="https://github.com/Deepanshu779/MediAI2.0">
    <img src="https://img.shields.io/badge/GitHub-MediAI%202.0-181717?style=for-the-badge&logo=github" alt="GitHub"/>
  </a>
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-Web%20App-000000?style=for-the-badge&logo=flask" alt="Flask"/>
  <img src="https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn"/>
  <img src="https://img.shields.io/badge/Groq-Optional%20LLM-111111?style=for-the-badge" alt="Groq"/>
</p>

> **⚠️ Medical & Educational Disclaimer:** MediAI 2.0 is a student/educational demonstration project. It does **not** provide a medical diagnosis, prescription, or substitute for a qualified healthcare professional. For urgent or emergency symptoms, seek professional medical care immediately.

---

## 📌 Overview

**MediAI 2.0** is a healthcare-focused web application that combines a locally hosted machine-learning prediction pipeline with rule-based health calculations and an optional Groq-powered language model.

The application is designed to demonstrate how multiple components can work together in a single healthcare experience:

- 🧠 **Symptom-based ML prediction**
- ❤️ **Vitals and biometric calculations**
- 🚨 **Emergency / red-flag screening**
- 🤖 **AI-assisted clinical guidance**
- 💬 **Conversational health assistant**
- 📄 **Downloadable PDF assessment reports**
- 🌐 **Flask-based web interface and JSON APIs**
- 🔒 **Offline-first prediction path** with no LLM key required

---

## ✨ Key Features

### 🧠 Machine Learning Health Assessment
Users enter symptoms and receive a ranked differential-style prediction from a locally stored scikit-learn model.

The prediction pipeline:

1. Converts the entered symptoms into a vector representation.
2. Uses the trained classifier to calculate probabilities.
3. Returns the most likely condition plus top predictions.
4. Applies an uncertainty guard for low-confidence results.

### 📊 Health & Vitals Analysis
MediAI calculates several useful health metrics from user inputs, including:

- BMI and BMI status
- Estimated risk level
- Temperature status
- SpO₂ status
- Health score and summary
- Basal Metabolic Rate (BMR)
- Estimated hydration requirement
- Target heart rate
- Mean Arterial Pressure (MAP), when blood-pressure values are supplied

### 🚨 Emergency Screening
The assessment includes a dedicated red-flag section intended to surface potentially urgent symptoms and direct users toward immediate medical attention.

### 🤖 AI Clinical Guidance
MediAI supports two modes:

**Offline mode**
- Uses the local clinical intelligence engine.
- Works without an API key.
- Provides structured care guidance based on the predicted condition and assessment data.

**Optional Groq mode**
- Uses Groq's LLM API for richer natural-language guidance.
- Falls back to the local engine when the API key is missing or the request fails.

### 💬 AI Health Assistant
The application includes a conversational assistant endpoint that can:

- Explain common symptoms
- Discuss basic health concepts
- Highlight emergency warning signs
- Suggest when to seek professional care
- Direct users to the full health assessment

### 📄 PDF Health Reports
After an assessment, the application generates a structured PDF report containing:

- Patient snapshot
- Vitals and health metrics
- Symptoms and clinical context
- Model suggestion and confidence
- Precautions
- AI-generated / offline care guidance
- Safety disclaimer

---

## 🏗️ How MediAI Works

```text
┌───────────────────────────────┐
│        User Assessment        │
│ Symptoms • Demographics       │
│ Vitals • History • Severity   │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Health Calculations       │
│ BMI • Risk • SpO₂ • Temperature│
│ BMR • Hydration • Target HR   │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       ML Prediction Engine     │
│ TF-IDF Vectorizer + Classifier│
│ Probability / Ranking         │
└───────────────┬───────────────┘
                │
                ├───────────────┐
                │               │
                ▼               ▼
┌───────────────────────┐  ┌───────────────────────┐
│ Offline Clinical      │  │ Optional Groq LLM     │
│ Intelligence Engine   │  │ Enhanced Guidance      │
└────────────┬──────────┘  └────────────┬──────────┘
             │                          │
             └─────────────┬────────────┘
                           ▼
                ┌────────────────────────┐
                │ Results Dashboard      │
                │ Assessment + Guidance  │
                └───────────┬────────────┘
                            ▼
                ┌────────────────────────┐
                │ PDF Clinical Report    │
                └────────────────────────┘
```

---

## 🧰 Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Machine Learning | scikit-learn |
| Data Processing | Pandas, NumPy |
| Model Serialization | Joblib |
| Optional LLM | Groq API |
| Environment Variables | python-dotenv |
| PDF Generation | ReportLab |
| Web Server | Gunicorn |
| Frontend | HTML, CSS, JavaScript, Jinja templates |
| Runtime | Python 3.11 |

---

## 📂 Project Structure

```text
MediAI2.0/
├── app.py                    # Flask application, routes and JSON APIs
├── predict.py                # Loads model/vectorizer and performs predictions
├── train_model.py            # Model training pipeline
├── utils.py                  # BMI, risk, vitals and helper utilities
├── groq_helper.py            # Groq integration + offline AI fallback
├── report_generator.py       # PDF report generation
├── requirements.txt          # Python dependencies
├── Procfile                  # Gunicorn deployment command
├── runtime.txt               # Python runtime version
├── .gitignore
│
├── data/
│   └── raw/
│       └── disease_sympts_prec_full.csv
│
├── models/
│   ├── model.pkl             # Trained classifier
│   └── vectorizer.pkl        # Fitted feature vectorizer
│
├── static/
│   ├── css/                  # Stylesheets
│   ├── js/                   # Client-side scripts
│   ├── images/               # Project assets
│   └── report.pdf            # Generated/sample report
│
└── templates/
    ├── base.html
    ├── components/
    └── pages/
        ├── home.html
        ├── assessment.html
        ├── assistant.html
        └── result.html
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Deepanshu779/MediAI2.0.git
cd MediAI2.0
```

### 2. Create a virtual environment

#### Windows — PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Windows — Command Prompt

```cmd
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The repository already includes **ReportLab** in `requirements.txt`, so no separate installation step is required.

### 4. Optional: Configure Groq

MediAI works without Groq. To enable the optional LLM-powered guidance and chat features, create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Do **not** commit your API key to GitHub.

### 5. Start the application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## 🌐 Application Routes

| Route | Method | Purpose |
|---|---:|---|
| `/` | GET | MediAI landing page |
| `/assessment` | GET | Guided health assessment |
| `/assistant` | GET | AI health assistant |
| `/predict` | POST | Process assessment and render results |
| `/api/chat` | POST | Conversational assistant JSON API |
| `/api/symptoms` | GET | Return the symptom catalogue |
| `/api/calculate-vitals` | POST | Calculate BMI, BMR, MAP, hydration, target HR and statuses |
| `/report/download` | GET | Download generated PDF report |

---

## 🧪 Model Pipeline

The prediction service loads its resources from:

```text
models/model.pkl
models/vectorizer.pkl
```

and reads the symptom/disease dataset from:

```text
data/raw/disease_sympts_prec_full.csv
```

At runtime, `predict.py`:

1. Loads the trained model and vectorizer with Joblib.
2. Loads the reference dataset with Pandas.
3. Vectorizes the submitted symptom text.
4. Calls `predict_proba()` on the trained classifier.
5. Produces a primary disease suggestion and ranked predictions.

The web application then combines the model output with vitals, risk scoring, emergency screening, and care guidance.

---

## 🔌 API Examples

### Calculate Vitals

**POST** `/api/calculate-vitals`

Example request:

```json
{
  "height": 170,
  "weight": 65,
  "age": 21,
  "gender": "Male",
  "temperature": 37.2,
  "spo2": 98,
  "systolic": 120,
  "diastolic": 80
}
```

Example response:

```json
{
  "bmi": 22.49,
  "bmi_status": "Normal",
  "temperature_status": "...",
  "spo2_status": "...",
  "bmr": 1617,
  "hydration_liters": 2.6,
  "target_heart_rate": "...",
  "map": 93.33
}
```

### Chat Assistant

**POST** `/api/chat`

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What should I know about a fever?"
    }
  ]
}
```

Response:

```json
{
  "response": "..."
}
```

---

## ☁️ Deployment

The repository includes:

- `Procfile` → `web: gunicorn app:app`
- `runtime.txt` → Python 3.11.9

This makes the project suitable for platforms that support Gunicorn/Heroku-style Python deployments.

Before deploying:

1. Set `GROQ_API_KEY` as a platform environment variable when using Groq.
2. Ensure the model and dataset files are included in the deployed repository.
3. Keep secrets out of source control.
4. Verify PDF writing permissions for the `static/` directory on your hosting platform.

---

## 🔐 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | No | Enables Groq-powered AI responses and chat |

MediAI intentionally supports a local fallback, so the core assessment flow can operate without an external LLM API.

---

## 📸 Screenshots

Add screenshots here to make the repository more visually appealing:

```md
## 📸 Screenshots

### Home
<img width="1687" height="882" alt="Screenshot 2026-08-27 103408" src="https://github.com/user-attachments/assets/455b3987-c712-4a0f-8145-bdb4d24eeced" />

### Health Assessment
<img width="1575" height="888" alt="Screenshot 2026-08-27 103427" src="https://github.com/user-attachments/assets/4443f5d1-538b-4e30-8972-a90cb313fdcc" />

### Results Dashboard
<img width="1682" height="777" alt="Screenshot 2026-08-27 103453" src="https://github.com/user-attachments/assets/ddf1248e-c1e2-49ee-8df6-1d35b3a44df1" />

```

## 🎯 What This Project Demonstrates

MediAI 2.0 is a strong demonstration of combining:

- Full-stack Python web development
- Machine learning inference
- Data preprocessing and feature vectorization
- REST-style JSON endpoints
- Health/biometric calculations
- LLM integration with graceful offline fallback
- Dynamic server-rendered UI
- Automated PDF report generation
- Deployment-oriented Flask configuration

---

## 🔮 Future Improvements

Potential next steps for the project include:

- Add formal model evaluation metrics and validation reports
- Improve the training dataset and feature engineering
- Add authentication and user profiles
- Store assessment history securely
- Add unit/integration tests
- Add automated CI/CD checks
- Add containerized deployment with Docker
- Improve accessibility and mobile responsiveness
- Add multilingual health guidance
- Add clinician-reviewed content and stronger safety controls

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

A simple workflow:

```bash
git checkout -b feature/your-feature
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Then open a pull request on GitHub.

---

## ⭐ Support the Project

If you found MediAI 2.0 useful or interesting:

**⭐ Star the repository** on GitHub and share it with other developers or students interested in AI + healthcare.

Repository:  
https://github.com/Deepanshu779/MediAI2.0

---

## 👨‍💻 Developer

**Deepanshu Kumar Pandit**

GitHub: [@Deepanshu779](https://github.com/Deepanshu779)

---

## 📜 License

No explicit license file is currently included in the repository. Consider adding a `LICENSE` file before presenting this project as an open-source project.

---

<p align="center">
  <strong>Built with Python, Flask, Machine Learning & AI</strong><br/>
  <sub>Educational project • Safety-first • Offline-capable</sub>
</p>
