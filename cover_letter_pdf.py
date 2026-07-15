from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_cover_letter_pdf(content):
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(buffer)
    
    styles = getSampleStyleSheet()
    
    story = []
    
    story.append(Paragraph("<b>Cover Letter</b>", styles["Heading1"]))

    story.append(Paragraph(content.replace("\n", "<br/>"), styles["Normal"]))
    
    doc.build(story)
    buffer.seek(0)
    
    return buffer