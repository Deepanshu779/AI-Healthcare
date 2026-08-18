# MediAI Healthcare Diagnosis Assistant

MediAI is a Flask-based healthcare assessment web application that uses machine learning to suggest possible health conditions from user-entered symptoms. It features a modern clinical UI, live real-time vitals and BMI calculators, searchable symptom selection across 130+ symptoms, and 100% offline standalone prediction without requiring an external API key (with optional Groq AI LLM enhancement).

> **Disclaimer**: This project is for educational and demonstration purposes only. It is not a medical diagnosis tool and must not replace consultation with a qualified healthcare professional.

---

## ✨ Features

- **100% Offline ML Disease Prediction**: Standalone Random Forest disease classifier (`scikit-learn`) running completely locally with zero API keys required.
- **Modern Clinical SaaS Interface**: Sleek dark-slate glassmorphism design system built with Plus Jakarta Sans typography.
- **Live Real-time Vitals & BMI Calculator**: Interactive client-side calculations that update dynamically as you type height, weight, temperature, and SpO2.
- **Smart Symptom Selector**: Live search filter and category pills (`Systemic & Fever`, `Respiratory`, `Digestive`, `Pain & Joints`, `Skin & Allergy`, `Neurological`) with 130+ supported symptoms.
- **Red Flag Emergency Screener**: High-visibility triage box for identifying acute warning signs.
- **Interactive Results Dashboard**:
  - Radial SVG animated confidence meter.
  - Differential diagnosis probability ranking bar chart.
  - Vitals & Health Score summary matrix.
  - Structured clinical care cards (Assessment & Etiology, Precautions, Nutrition & Diet, Specialist Referrals).
- **Official PDF & Print Reports**: Clean, downloadable clinical health assessment report.

---

## 🛠️ Technology Stack

<img width="1672" height="941" alt="Technology Stack" src="https://github.com/user-attachments/assets/a9b5185b-c3fa-4d0f-ba1c-a026bf29f022" />

---

## 📁 Project Structure

```text
Healthcare-AI/
├── app.py                                # Flask Application & Web Routes
├── predict.py                            # Machine Learning Prediction Module
├── train_model.py                        # Model Training Pipeline (Random Forest)
├── utils.py                              # Vitals, Risk, Score & Section Parsers
├── groq_helper.py                        # Offline Clinical Intelligence + Optional Groq LLM
├── report_generator.py                   # PDF Report Generator (ReportLab)
├── requirements.txt                      # Project Dependencies
├── dataset/
│   └── disease_sympts_prec_full.csv     # Disease, Symptoms & Precautions Dataset
├── model/
│   ├── model.pkl                         # Trained Scikit-Learn Model
│   └── vectorizer.pkl                    # TF-IDF Vectorizer
├── static/
│   ├── style.css                         # Clinical SaaS Design System CSS
│   ├── report.css                        # HTML Report Styling
│   └── report.pdf                        # Sample Generated PDF Report
└── templates/
    ├── index.html                        # Multi-Step Guided Assessment Form
    ├── result.html                       # Clinical Results Dashboard
    └── report.html                       # Web Report View
```

---

## 🏗️ System Architecture

![System Architecture](static/system-architecture.png)

---

## ⚙️ Setup & Installation

### 1. Create and activate a virtual environment

```bash
python -m venv venv
```

On Windows (PowerShell):
```powershell
.\venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install reportlab
```

### 3. (Optional) Configure Groq API Key
*Note: Prediction and clinical advice work 100% offline out-of-the-box! Adding a Groq key is optional.*

If desired, create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the Application

```bash
python app.py
```

Open your browser and navigate to:
```text
http://127.0.0.1:5000
```
