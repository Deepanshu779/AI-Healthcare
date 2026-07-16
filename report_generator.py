import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


def generate_report(
    name,
    age,
    gender,
    bmi,
    risk,
    symptoms,
    disease,
    confidence,
    precaution,
    ai_response
):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    pdf_path = os.path.join(BASE_DIR, "static", "report.pdf")

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    doc = SimpleDocTemplate(
        pdf_path,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER
    title.textColor = colors.HexColor("#0D47A1")

    heading = styles["Heading2"]
    heading.textColor = colors.HexColor("#1565C0")

    normal = styles["BodyText"]

    story = []

    # ===================================
    # HEADER
    # ===================================

    story.append(
        Paragraph(
            "🩺 <b>MediAI Healthcare Diagnosis Assistant</b>",
            title
        )
    )

    story.append(
        Paragraph(
            "Machine Learning + Generative AI",
            normal
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # ===================================
    # PATIENT INFORMATION
    # ===================================

    story.append(Paragraph("<b>Patient Information</b>", heading))

    patient = [

        ["Patient Name", name],

        ["Age", str(age)],

        ["Gender", gender],

        ["BMI", str(bmi)],

        ["Risk Level", risk]

    ]

    table = Table(patient, colWidths=[170, 300])

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565C0")),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),

        ])

    )

    story.append(table)

    story.append(Spacer(1, 0.25 * inch))

    # ===================================
    # SYMPTOMS
    # ===================================

    story.append(Paragraph("<b>Symptoms</b>", heading))

    story.append(
        Paragraph(symptoms, normal)
    )

    story.append(Spacer(1, 0.2 * inch))

    # ===================================
    # AI ASSESSMENT
    # ===================================

    story.append(
        Paragraph("<b>Possible Health Assessment</b>", heading)
    )

    assessment = [

        ["Most Likely Condition", disease],

        ["Confidence", f"{confidence:.2f}%"]

    ]

    t2 = Table(assessment, colWidths=[180, 290])

    t2.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E3F2FD")),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),

        ])

    )

    story.append(t2)

    story.append(Spacer(1, 0.25 * inch))

    # ===================================
    # PRECAUTIONS
    # ===================================

    story.append(
        Paragraph("<b>Recommended Precautions</b>", heading)
    )

    story.append(
        Paragraph(precaution, normal)
    )

    story.append(Spacer(1, 0.25 * inch))

    # ===================================
    # AI RECOMMENDATION
    # ===================================

    story.append(
        Paragraph("<b>AI Medical Recommendation</b>", heading)
    )

    story.append(
        Paragraph(ai_response.replace("\n", "<br/>"), normal)
    )

    story.append(Spacer(1, 0.3 * inch))

    # ===================================
    # DISCLAIMER
    # ===================================

    story.append(
        Paragraph(
            "<b>Disclaimer</b>",
            heading
        )
    )

    story.append(

        Paragraph(

            "This report was generated using Artificial Intelligence "
            "and Machine Learning for educational purposes only. "
            "It is not a medical diagnosis and should not replace "
            "consultation with a qualified healthcare professional.",

            normal

        )

    )

    doc.build(story)