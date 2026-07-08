from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_resume_pdf(data):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph(f"<b>{data['full_name']}</b>", styles["Title"]))
    elements.append(Paragraph(data["email"], styles["Normal"]))
    elements.append(Paragraph(data["phone"], styles["Normal"]))

    elements.append(Paragraph("<b>Professional Summary</b>", styles["Heading2"]))
    elements.append(Paragraph(data["summary"], styles["Normal"]))

    elements.append(Paragraph("<b>Education</b>", styles["Heading2"]))
    elements.append(Paragraph(data["education"], styles["Normal"]))

    elements.append(Paragraph("<b>Skills</b>", styles["Heading2"]))
    elements.append(Paragraph(data["skills"], styles["Normal"]))

    elements.append(Paragraph("<b>Work Experience</b>", styles["Heading2"]))
    elements.append(Paragraph(data["experience"], styles["Normal"]))

    doc.build(elements)

    buffer.seek(0)
    return buffer