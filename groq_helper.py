import os
import re
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
            "overview": "Gastrointestinal tract irritation or acid reflux may cause epigastric pain, nausea, heartburn, and burning sensations.",
            "home_care": "Eat smaller, more frequent meals. Avoid lying down for at least 2-3 hours after meals. Elevate the head of your bed slightly.",
            "diet": "Opt for non-citrus fruits (bananas, melons), oatmeal, lean poultry, boiled vegetables, and ginger infusion. Avoid spicy, fried, caffeinated, and acidic foods.",
            "specialist": "Gastroenterologist or Internal Medicine Physician if discomfort is severe, accompanied by black stools or difficulty swallowing."
        }
    elif any(k in d_lower for k in ["pneumonia", "bronchial asthma", "bronchitis", "tuberculosis", "chronic"]):
        return {
            "overview": "Lower respiratory tract condition impacting airway ventilation, oxygenation, and pulmonary capacity.",
            "home_care": "Use warm steam inhalation, stay in clean well-ventilated spaces, rest in an elevated upright position, and continuously track SpO2 levels.",
            "diet": "Warm broths, herbal infusions with honey, antioxidant-rich berries, citrus bioflavonoids, and ample warm hydration to thin bronchial secretions.",
            "specialist": "Pulmonologist or Emergency Care immediately if blood oxygen drops below 94% or breathing becomes labored."
        }
    elif any(k in d_lower for k in ["common cold", "allergy", "allergic rhinitis", "sinusitis"]):
        return {
            "overview": "Upper respiratory tract viral infection or allergic response affecting nasal passages, sinuses, and pharynx.",
            "home_care": "Saline nasal irrigation, steam inhalation, warm salt water gargling, ample rest, and allergen avoidance.",
            "diet": "Warm liquids, ginger-turmeric tea, chicken/vegetable soup, citrus fruits, and zinc-rich foods.",
            "specialist": "General Physician or ENT Specialist if symptoms persist beyond 7–10 days or facial sinus pressure worsens."
        }
    elif any(k in d_lower for k in ["malaria", "dengue", "typhoid", "viral fever"]):
        return {
            "overview": "Systemic febrile illness often transmitted through vectors or waterborne pathogens requiring clinical confirmation via laboratory testing.",
            "home_care": "Strict bed rest, cold sponge baths for temperature reduction, mosquito netting, and daily platelet or fever pattern monitoring.",
            "diet": "Intensive hydration with ORS (Oral Rehydration Salts), tender coconut water, pomegranate juice, and easily digestible porridge.",
            "specialist": "Infectious Disease Specialist or General Physician for diagnostic blood panels (CBC, Widal, NS1 antigen, Dengue IgM/IgG, MP smear)."
        }
    elif any(k in d_lower for k in ["fungal infection", "jaundice", "hepatitis", "skin rash", "acne", "psoriasis"]):
        return {
            "overview": "Dermatological or hepatic condition affecting skin barrier integrity, fungal proliferation, or bilirubin clearance.",
            "home_care": "Keep affected skin clean and completely dry. Wear loose, breathable cotton clothing. Avoid sharing towels or linens.",
            "diet": "Low-fat, easily digestible diet. Drink abundant clean water. Strictly avoid alcohol, refined sugars, and greasy fried foods.",
            "specialist": "Dermatologist for cutaneous symptoms, or Hepatologist / Gastroenterologist for jaundice / elevated liver enzymes."
        }
    elif any(k in d_lower for k in ["arthritis", "osteoarthritis", "cervical spondylosis"]):
        return {
            "overview": "Musculoskeletal or joint inflammatory condition causing stiffness, discomfort, and restricted range of motion.",
            "home_care": "Apply warm compresses for stiffness and cold packs for acute swelling. Practice gentle low-impact range-of-motion stretching.",
            "diet": "Anti-inflammatory foods: omega-3 fatty acids (flaxseeds, walnuts, chia seeds), turmeric, dark leafy greens, and calcium-rich foods.",
            "specialist": "Rheumatologist or Orthopedic Specialist for targeted physical therapy and joint imaging."
        }
    elif any(k in d_lower for k in ["diabetes", "hypoglycemia", "hypertension", "hypothyroidism", "hyperthyroidism"]):
        return {
            "overview": "Endocrine or metabolic regulation imbalance requiring periodic biometric monitoring and lifestyle calibration.",
            "home_care": "Monitor blood glucose and blood pressure regularly. Maintain consistent sleep and low-impact daily exercise schedules.",
            "diet": "Complex carbohydrates with low glycemic index, high-fiber legumes, whole grains, and minimal refined sugars or excess sodium.",
            "specialist": "Endocrinologist or Cardiologist for comprehensive metabolic panel and prescription management."
        }
    elif any(k in d_lower for k in ["migraine", "headache", "paralysis", "vertigo"]):
        return {
            "overview": "Neurological or vascular episode affecting cranial nerves, cerebral circulation, or vestibular balance.",
            "home_care": "Rest in a quiet, dark, well-ventilated room. Apply cold compresses across forehead or temples. Avoid screen glare and loud sounds.",
            "diet": "Maintain regular meal schedules. Stay hydrated with electrolytes. Avoid aged cheeses, MSG, artificial sweeteners, and excess caffeine.",
            "specialist": "Neurologist if headaches are sudden/severe ('thunderclap'), accompanied by visual loss, motor weakness, or numbness."
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
    guidance = get_disease_category_guidance(disease)

    vitals_summary = []
    if temperature:
        vitals_summary.append(f"Temperature: {temperature}°C")
    if spo2:
        vitals_summary.append(f"Blood Oxygen (SpO2): {spo2}%")
    vitals_str = ", ".join(vitals_summary) if vitals_summary else "Vitals within standard ranges or not recorded"

    emergency_warning = ""
    if emergency and len(emergency) > 0:
        emergency_warning = f"""
## Urgent Clinical Warning
> **CRITICAL RED-FLAG ALERT**: High-risk emergency symptoms were reported ({', '.join(emergency)}). 
> **Immediate Action Required**: Do not wait for routine appointments. Please proceed to the nearest Emergency Department or call emergency medical services immediately.
"""

    return f"""## Diagnostic Differential Assessment
Based on the symptom profile presented ({symptoms}) and demographic indicators (Age: {age}, Gender: {gender}, BMI: {bmi}), the machine learning pattern analysis indicates **{disease}** as the primary differential consideration.
{guidance['overview']}

## Clinical Pattern Correlation
- **Reported Duration**: {duration} with {severity.lower()} intensity ({progress or 'stable course'}).
- **Observed Vitals**: {vitals_str}.
- **Reported Exposure**: {contact or 'No known pathogen contact'}.
- **Medical Background**: {history}.
- **Calculated Risk Level**: **{risk} Risk** stratification.
{emergency_warning}
## Recommended Home Care & Supportive Protocol
- {guidance['home_care']}
- Ensure uninterrupted restorative rest and isolate if infectious symptoms are suspected.
- Track temperature, pulse, and oxygen saturation every 4-6 hours.

## Evidence-Based Nutrition & Hydration
- {guidance['diet']}
- Maintain electrolyte balance with coconut water, light broths, or oral rehydration solutions.
- Avoid heavy, greasy, or ultra-processed meals until gastrointestinal and systemic equilibrium is restored.

## Critical Red Flags Requiring Immediate Emergency Care
- Sudden severe chest pain, radiating left arm pain, or severe shortness of breath.
- SpO2 dropping below 93% on room air.
- Persistent high fever (>39.5°C / 103°F) unresponsive to antipyretics.
- Sudden onset confusion, slurred speech, facial drooping, or limb weakness.
- Inability to retain fluids for >24 hours with signs of severe dehydration.

## Specialist & Next Steps
- **Primary Recommendation**: Schedule a clinical consultation with a **{guidance['specialist']}**.
- Bring this generated diagnostic summary report and a log of vital signs to your doctor for precision evaluation.

## Educational Disclaimer
*MediAI 2.0 provides clinical intelligence for educational and triage triage assistance only. It is not an automated medical prescription or formal clinical diagnosis. Always seek direct medical guidance from qualified physicians.*"""


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
    Calls Groq LLM if API key is provided; otherwise seamlessly returns high-grade offline clinical advice.
    """
    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if not api_key or Groq is None:
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

        prompt = f"""You are MediAI Clinical Intelligence Assistant. Provide a thorough, professional clinical assessment based on the patient's intake data below.

PATIENT PROFILE:
- Age: {age} | Gender: {gender} | BMI: {bmi}
- Primary ML Differential Disease Prediction: {disease}
- Active Symptoms: {symptoms}
- Duration: {duration} | Severity: {severity} | Progression: {progress or 'Stable'}
- Body Temperature: {temperature or 'Not provided'} °C | SpO2: {spo2 or 'Not provided'} %
- Known Exposure / Contact: {contact or 'None reported'}
- Medical History: {history}
- Emergency Symptoms: {', '.join(emergency) if emergency else 'None reported'}
- Risk Level: {risk}

FORMAT YOUR RESPONSE EXACTLY USING THESE HEADINGS:
## Diagnostic Differential Assessment
## Clinical Pattern Correlation
## Recommended Home Care & Supportive Protocol
## Evidence-Based Nutrition & Hydration
## Critical Red Flags Requiring Immediate Emergency Care
## Specialist & Next Steps
## Educational Disclaimer

Maintain an empathetic, authoritative, clinical, and safety-first medical tone."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a world-class AI clinical healthcare decision-support system. Provide evidence-based medical triage guidance and structured patient recommendations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Groq API call fallback triggered ({e}). Using local Clinical Intelligence engine.")
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


def get_chat_response(messages):
    """
    Conversational AI Assistant endpoint. Handles natural language questions, symptom triage,
    and returns rich markdown responses with interactive suggestions.
    """
    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if api_key and Groq is not None:
        try:
            client = Groq(api_key=api_key)
            formatted_messages = [
                {
                    "role": "system",
                    "content": (
                        "You are MediAI Assistant, a world-class AI clinical health companion. "
                        "You help users understand their health symptoms, explain medical concepts in accessible terms, "
                        "advise when to see a physician, and suggest next steps. "
                        "Always prioritize safety, highlight red flags, and remind users that you are an AI health companion."
                    )
                }
            ]
            for m in messages:
                formatted_messages.append({"role": m.get("role", "user"), "content": m.get("content", "")})

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=formatted_messages,
                temperature=0.5,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq chat fallback: {e}")

    # OFFLINE INTELLIGENT CLINICAL CHATBOT FALLBACK
    last_msg = messages[-1].get("content", "").lower() if messages else ""

    # Check for emergency keywords
    if any(k in last_msg for k in ["chest pain", "difficulty breathing", "heart attack", "stroke", "paralysis", "unconscious", "bleeding profusely", "suicide"]):
        return (
            "🚨 **URGENT MEDICAL ALERT**: The symptoms you described could indicate a life-threatening medical emergency.\n\n"
            "**Immediate Steps**:\n"
            "1. Call emergency services immediately (**911** or your local emergency number).\n"
            "2. Do not attempt to drive yourself to the hospital.\n"
            "3. Rest in a safe, seated or supported position while emergency medical personnel arrive.\n\n"
            "If you are experiencing chest tightness, difficulty breathing, or sudden numbness, seek emergency medical attention without delay."
        )

    if any(k in last_msg for k in ["fever", "temperature", "chills"]):
        return (
            "🌡️ **Fever & Temperature Guidance**:\n\n"
            "A fever is your body's immune response to an infection. Here is what you should know:\n\n"
            "- **Temperature Classification**:\n"
            "  - *Normal*: 36.5°C – 37.5°C (97.7°F – 99.5°F)\n"
            "  - *Mild Fever*: 37.6°C – 38.4°C\n"
            "  - *High Fever*: ≥ 38.5°C (101.3°F)\n\n"
            "- **Home Management**:\n"
            "  - Drink plenty of hydrating fluids (water, ORS, herbal broths).\n"
            "  - Rest in a cool, ventilated room with light clothing.\n"
            "  - Take a lukewarm sponge bath if needed.\n\n"
            "- **When to see a doctor**:\n"
            "  - Fever lasts more than 3 consecutive days.\n"
            "  - Accompanied by stiff neck, shortness of breath, or confusion.\n\n"
            "👉 *Tip: You can launch our full [AI Health Assessment](/assessment) to analyze related symptoms.*"
        )

    if any(k in last_msg for k in ["headache", "migraine", "head pain"]):
        return (
            "🧠 **Headache & Migraine Assessment**:\n\n"
            "Headaches can range from tension and sinus pressure to migraines or vascular events.\n\n"
            "- **Common Types**:\n"
            "  - *Tension Headache*: Dull ache across both sides, band-like tightness.\n"
            "  - *Migraine*: Throbbing on one side, sensitivity to light/sound, possible nausea.\n"
            "  - *Sinus Headache*: Pressure behind eyes and forehead.\n\n"
            "- **Supportive Care**:\n"
            "  - Rest in a dark, quiet room with cold compress on forehead.\n"
            "  - Hydrate with water and electrolytes.\n"
            "  - Take a screen break and practice gentle neck stretches.\n\n"
            "⚠️ **Seek Immediate Care If**: The headache is sudden and excruciating ('thunderclap'), accompanied by speech difficulty, vision loss, or weakness."
        )

    if any(k in last_msg for k in ["cough", "throat", "cold", "flu", "sneeze"]):
        return (
            "🫁 **Respiratory Symptoms Care Guide**:\n\n"
            "- **Supportive Protocol**:\n"
            "  - Steam inhalation 2 times daily to loosen mucus.\n"
            "  - Warm salt-water gargle (1/2 tsp salt in warm water) for sore throat.\n"
            "  - Warm tea with honey and ginger for soothing cough reflex.\n"
            "  - Keep well-hydrated to help clear secretions.\n\n"
            "- **Monitor Your Blood Oxygen (SpO2)**:\n"
            "  - Normal SpO2 is **95% - 100%**.\n"
            "  - If SpO2 drops below **94%** or you experience breathing distress, consult a physician promptly."
        )

    if any(k in last_msg for k in ["stomach", "acidity", "nausea", "vomiting", "diarrhea", "gerd"]):
        return (
            "🥣 **Gastrointestinal Care & Triage**:\n\n"
            "- **Key Dietary Steps (BRAT Diet)**:\n"
            "  - Bananas, Rice, Applesauce, and Toast.\n"
            "  - Sip Oral Rehydration Solution (ORS) or electrolyte water.\n"
            "  - Avoid fried, oily, spicy, dairy, and caffeinated items.\n\n"
            "- **Acid Reflux / GERD Tips**:\n"
            "  - Eat smaller meals.\n"
            "  - Avoid lying flat for 2-3 hours after eating.\n"
            "  - Elevate your head slightly when sleeping."
        )

    # General Greeting / Default response
    return (
        "👋 **Hello! I am MediAI Clinical Assistant.**\n\n"
        "I can help you:\n"
        "- 🔍 Understand specific symptoms (e.g., fever, cough, joint pain, migraine)\n"
        "- 📊 Explain vitals and biometric targets (BMI, SpO2, Blood Pressure, Heart Rate)\n"
        "- 🛡️ Provide evidence-based home care, nutrition, and safety red flags\n"
        "- 🩺 Guide you to the right medical specialist\n\n"
        "**How can I assist you today?** Describe what you are experiencing, or click [Start Health Assessment](/assessment) for a full multi-parameter diagnostic screening."
    )
