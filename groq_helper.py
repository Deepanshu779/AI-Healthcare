import os
from dotenv import load_dotenv

try:
    from groq import Groq
except ImportError:
    Groq = None

load_dotenv()


def get_disease_category_guidance(disease_name):
    """
    Returns condition-specific educational guidance, home care, and dietary recommendations.
    """
    d_lower = str(disease_name).lower()

    if any(k in d_lower for k in ["gerd", "acidity", "peptic ulcer", "gastritis", "gastroenteritis"]):
        return {
            "overview": "Gastrointestinal tract irritation or acid reflux may cause epigastric pain, nausea, and burning sensation.",
            "home_care": "Eat smaller, more frequent meals. Avoid lying down for at least 2-3 hours after eating. Elevate the head of your bed slightly.",
            "diet": "Opt for non-citrus fruits (bananas, melons), oatmeal, lean proteins, boiled vegetables, and ginger tea. Avoid spicy, fried, caffeinated, and acidic foods.",
            "specialist": "Gastroenterologist or Internal Medicine Physician if pain is severe, accompanied by black stools or difficulty swallowing."
        }
    elif any(k in d_lower for k in ["pneumonia", "bronchial asthma", "bronchitis", "tuberculosis"]):
        return {
            "overview": "Lower respiratory involvement that can impact airway ventilation, oxygen exchange, and lung capacity.",
            "home_care": "Use warm steam inhalation, stay in well-ventilated areas, rest in an elevated seating position, and continuously monitor SpO2 levels.",
            "diet": "Warm soups, herbal teas with honey, antioxidant-rich fruits, vitamin C sources, and ample warm water to thin mucus.",
            "specialist": "Pulmonologist or Emergency Care immediately if oxygen drops below 94% or breathing becomes labored."
        }
    elif any(k in d_lower for k in ["common cold", "allergy", "allergic rhinitis", "sinusitis"]):
        return {
            "overview": "Upper respiratory tract viral infection or allergic response affecting nasal passages and sinuses.",
            "home_care": "Saline nasal rinse, steam inhalation, warm salt water gargling, ample rest, and staying away from known allergens and dust.",
            "diet": "Warm fluids, ginger-turmeric tea, chicken/vegetable broth, citrus fruits, and zinc-rich foods.",
            "specialist": "General Physician or ENT specialist if symptoms persist beyond 7–10 days or facial pain worsens."
        }
    elif any(k in d_lower for k in ["malaria", "dengue", "typhoid", "viral fever"]):
        return {
            "overview": "Systemic febrile illness often transmitted through vectors or waterborne pathogens requiring clinical confirmation through blood testing.",
            "home_care": "Strict bed rest, cold sponge baths for high fever, use mosquito netting, and monitor platelet count or fever pattern closely.",
            "diet": "High hydration with ORS (Oral Rehydration Salts), tender coconut water, pomegranate juice, papaya leaf extract (if advised), and easily digestible porridge.",
            "specialist": "Infectious Disease Specialist or General Physician for diagnostic blood panels (CBC, Widal, NS1 antigen, Dengue IgM/IgG, MP smear)."
        }
    elif any(k in d_lower for k in ["fungal infection", "jaundice", "hepatitis", "skin rash", "acne", "psoriasis"]):
        return {
            "overview": "Dermatological or hepatic condition affecting skin integrity, fungal proliferation, or bilirubin clearance.",
            "home_care": "Keep affected areas clean and completely dry. Wear loose, breathable cotton clothing. Avoid sharing towels or personal items.",
            "diet": "Low-fat, easily digestible diet. Drink abundant clean filtered water. For liver health, strictly avoid alcohol and processed greasy foods.",
            "specialist": "Dermatologist for cutaneous symptoms, or Hepatologist / Gastroenterologist for yellowing of eyes/skin (jaundice)."
        }
    elif any(k in d_lower for k in ["arthritis", "osteoarthritis", "cervical spondylosis"]):
        return {
            "overview": "Musculoskeletal or joint inflammatory condition causing stiffness, discomfort, and restricted range of motion.",
            "home_care": "Apply warm compresses for stiffness and cold packs for acute swelling. Practice gentle range-of-motion stretching.",
            "diet": "Anti-inflammatory foods: omega-3 fatty acids (flaxseeds, walnuts, fatty fish), turmeric, berries, leafy greens, and calcium-rich dairy or plant milks.",
            "specialist": "Rheumatologist or Orthopedic Specialist for targeted physical therapy and joint imaging."
        }
    elif any(k in d_lower for k in ["diabetes", "hypoglycemia", "hypertension", "hypothyroidism", "hyperthyroidism"]):
        return {
            "overview": "Endocrine or metabolic regulation imbalance requiring regular parameter monitoring and lifestyle adjustments.",
            "home_care": "Monitor blood glucose and blood pressure periodically. Maintain consistent sleep and low-impact daily exercise schedules.",
            "diet": "Complex carbohydrates with low glycemic index, high-fiber legumes, whole grains, and minimal refined sugars or excess sodium.",
            "specialist": "Endocrinologist or Cardiologist for comprehensive metabolic panel and prescription management."
        }
    elif any(k in d_lower for k in ["migraine", "headache", "paralysis", "vertigo"]):
        return {
            "overview": "Neurological or vascular episode affecting cranial nerves, cerebral blood flow, or vestibular balance.",
            "home_care": "Rest in a quiet, dark, well-ventilated room. Apply cold compresses across forehead or temples. Avoid screen time and bright lights.",
            "diet": "Maintain regular meal schedules. Stay hydrated with electrolytes. Avoid aged cheeses, MSG, artificial sweeteners, and excess caffeine.",
            "specialist": "Neurologist if headaches are sudden/severe ('thunderclap'), accompanied by visual loss, weakness, or numbness."
        }
    else:
        return {
            "overview": "Symptom complex aligned with general physiological imbalance or acute inflammatory response.",
            "home_care": "Get adequate physical rest (7-9 hours), drink at least 2.5-3 liters of fluids daily, and maintain a symptom log with timestamps.",
            "diet": "Balanced whole-food nutrition containing lean proteins, colorful vegetables, healthy fats, and adequate hydration.",
            "specialist": "Consult a registered General Physician for a formal physical examination and diagnostic evaluation."
        }


def get_offline_advice(
    age,
    gender,
    symptoms,
    disease,
    duration,
    severity,
    history,
    bmi,
    risk,
    temperature=None,
    spo2=None,
    progress=None,
    contact=None,
    emergency=None
):
    """
    Generates rich, structured, condition-tailored clinical guidance completely offline without needing an API key.
    """
    category_info = get_disease_category_guidance(disease)
    emergency_text = ", ".join(emergency) if emergency else "None noted"
    
    # Vital alerts
    vital_warnings = []
    try:
        if temperature and float(temperature) >= 38.5:
            vital_warnings.append(f"Elevated body temperature ({temperature}°C) indicates active fever or systemic immune response.")
        if spo2 and int(spo2) < 95:
            vital_warnings.append(f"Borderline/Low Blood Oxygen Saturation ({spo2}%) requires close pulse oximetry monitoring.")
    except Exception:
        pass

    vital_warning_str = (" " + " ".join(vital_warnings)) if vital_warnings else ""

    return f"""## Possible Health Assessment
Based on the symptom profile and demographic indicators, the ML model identified **{disease}** as the primary potential condition.{vital_warning_str} Note that this is an educational screening assessment, not a confirmed clinical diagnosis.

## Why this Condition May Fit
The reported symptoms ({symptoms}) combined with a duration of {duration} and {severity.lower()} severity fit common presentation patterns for this condition. {category_info['overview']}

## Home Care & Recovery Protocol
- {category_info['home_care']}
- Ensure adequate physical rest and maintain continuous hydration (water, clear broths, oral electrolytes).
- Keep a daily log of vitals (temperature, blood oxygen, pulse) and symptom changes.

## Nutritional & Dietary Guidance
- {category_info['diet']}
- Avoid heavy, oily, overly processed foods, and refrain from alcohol or tobacco during recovery.

## Red Flag Warning Signs (Seek Urgent Care)
Seek immediate emergency medical attention if you experience:
- Sudden chest tightness, shortness of breath, or SpO2 dropping below 92%.
- High persistent fever unresponsive to antipyretics, severe confusion, or fainting.
- Blue-tinted lips/face, severe abdominal rigidity, or uncontrollable vomiting.
- *Emergency symptoms flagged:* {emergency_text}.

## When to Consult a Specialist
- Schedule a clinical appointment with a **{category_info['specialist']}**.
- Immediate in-person medical evaluation is advised if symptoms persist beyond 48–72 hours, worsen in intensity, or interact with known medical history ({history}).

## Important Clinical Note
Fever, body pain, or headaches alone cannot pinpoint a definitive diagnosis. Many conditions share overlapping symptom profiles. Comprehensive lab investigations (blood tests, imaging) conducted by a licensed healthcare provider are necessary for accurate treatment.

*Generated locally via MediAI Offline Clinical Intelligence Engine (No external API key required). For educational purposes only.*"""


def get_ai_advice(
    age,
    gender,
    symptoms,
    disease,
    duration,
    severity,
    history,
    bmi,
    risk,
    temperature=None,
    spo2=None,
    progress=None,
    contact=None,
    emergency=None
):
    """
    Returns AI clinical guidance. Uses Groq LLM if API key is provided, or seamlessly
    uses the enhanced Offline Clinical Intelligence Engine if no API key is set.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key or Groq is None or not str(api_key).strip():
        return get_offline_advice(
            age=age,
            gender=gender,
            symptoms=symptoms,
            disease=disease,
            duration=duration,
            severity=severity,
            history=history,
            bmi=bmi,
            risk=risk,
            temperature=temperature,
            spo2=spo2,
            progress=progress,
            contact=contact,
            emergency=emergency
        )

    try:
        client = Groq(api_key=api_key)

        prompt = f"""
You are an experienced, empathetic AI Clinical Assistant.

IMPORTANT:
This is an educational assessment, NOT a definitive medical diagnosis.
Do not prescribe prescription medicines or make absolute medical guarantees.

=========================
PATIENT DATA & CLINICAL PROFILE
=========================
- Age: {age} | Gender: {gender}
- BMI: {bmi} | Overall Risk Level: {risk}
- Temperature: {temperature if temperature else "Not Provided"} °C
- SpO2 Oxygen Saturation: {spo2 if spo2 else "Not Provided"} %
- Primary Symptoms: {symptoms}
- Symptom Duration: {duration}
- Severity: {severity}
- Progression: {progress if progress else "Not Provided"}
- Sick Contact Exposure: {contact if contact else "None"}
- Past Medical History: {history}
- Emergency Warning Symptoms: {", ".join(emergency) if emergency else "None"}
- ML Predicted Condition: {disease}

=========================
YOUR TASK
=========================
Generate a well-structured clinical advice response using these exact markdown headers:

## Possible Health Assessment
Explain why {disease} is suggested as a possibility and what it generally means.

## Why this Condition May Fit
Explain the relationship between the reported symptoms ({symptoms}) and this condition.

## Home Care & Recovery Protocol
Provide clear self-care advice (rest, hydration, temperature management, monitoring).

## Nutritional & Dietary Guidance
Provide specific foods, fluids, and dietary habits that support immune recovery or gut health for this type of condition.

## Red Flag Warning Signs (Seek Urgent Care)
List critical signs (low oxygen, chest pressure, severe dehydration, breathing difficulty) that warrant immediate emergency attention.

## When to Consult a Specialist
Suggest the appropriate medical specialist (e.g. Pulmonologist, Gastroenterologist, ENT, General Physician) and timeline for in-person consultation.

## Important Clinical Note
Conclude with a brief reminder that many illnesses have overlapping symptoms and an in-person physical exam/lab test is needed. Include the educational disclaimer.

Format cleanly with bullet points. Tone should be professional, empathetic, and objective.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional clinical healthcare assistant providing educational health guidance and triage recommendations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.25,
            max_tokens=800
        )

        return response.choices[0].message.content

    except Exception as e:
        # Graceful fallback to offline engine if API call fails (network issue, quota, expired key)
        print(f"Groq API call encountered: {e}. Falling back to offline clinical engine.")
        return get_offline_advice(
            age=age,
            gender=gender,
            symptoms=symptoms,
            disease=disease,
            duration=duration,
            severity=severity,
            history=history,
            bmi=bmi,
            risk=risk,
            temperature=temperature,
            spo2=spo2,
            progress=progress,
            contact=contact,
            emergency=emergency
        )
