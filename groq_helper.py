import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


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
    prompt = f"""
You are an experienced AI Healthcare Assistant.

IMPORTANT:
This is NOT a final medical diagnosis.
The machine learning model only suggests a possible health condition.
Do not claim with certainty that the patient has a disease.

=========================
PATIENT INFORMATION
=========================

Age: {age}
Gender: {gender}

BMI: {bmi}
Risk Level: {risk}

Temperature: {temperature if temperature else "Not Provided"} °C
SpO₂: {spo2 if spo2 else "Not Provided"} %

Symptoms:
{symptoms}

Duration:
{duration}

Severity:
{severity}

Symptoms Progress:
{progress if progress else "Not Provided"}

Recent Contact With Sick Person:
{contact if contact else "Not Provided"}

Medical History:
{history}

Emergency Symptoms:
{", ".join(emergency) if emergency else "None"}

=========================
MACHINE LEARNING RESULT
=========================

Possible Condition:
{disease}

=========================
YOUR TASK
=========================

Write the response using these headings:

## Possible Health Assessment

Briefly explain that this is only one possible condition based on the information provided.

## Why this Condition May Fit

Explain why the entered symptoms could match this condition.

## Other Possible Conditions

Mention 2 or 3 other possible illnesses that may have similar symptoms.

## Home Care Advice

Provide simple self-care tips such as hydration, rest, healthy food, and monitoring symptoms.

## Diet Recommendations

Recommend foods and fluids that may support recovery.

## Warning Signs

List symptoms that require urgent medical attention.

## When to Consult a Doctor

Explain when the user should seek professional medical advice.

## Important Note

Clearly state:

• Fever or headache alone cannot confirm a disease.
• Many illnesses share similar symptoms.
• More information or medical tests may be needed.

Finish with this disclaimer:

"This assessment is generated using Artificial Intelligence for educational purposes only. It is not a medical diagnosis and should not replace consultation with a qualified healthcare professional."

Keep the response below 300 words.
Use simple English.
Do not prescribe medicines.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI healthcare assistant that provides educational health information only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=700
    )

    return response.choices[0].message.content