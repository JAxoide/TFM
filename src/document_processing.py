import PyPDF2
import docx
import os

def load_document(file_path):
    """Carga el contenido de un archivo de texto o PDF."""
    _, ext = os.path.splitext(file_path)
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    elif ext == ".pdf":
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    else:
        raise ValueError("Formato de archivo no compatible.")

# Cargar el documento del AI Act
document_text = load_document("data/ai_act_summary.pdf")

def extract_text_from_pdf(pdf_file):
    """Extrae texto de un archivo PDF."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    return text

def extract_text_from_docx(docx_file):
    """Extrae texto de un archivo DOCX."""
    doc = docx.Document(docx_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_txt(txt_file):
    """Extrae texto de un archivo TXT."""
    return txt_file.read().decode("utf-8")

def process_uploaded_file(uploaded_file):  
    """Procesa un archivo subido por el usuario."""
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    else:
        return "Formato no compatible"

def process_document(document_text):
    """
    Procesa el documento y evalúa los riesgos.
    """
    from src.risk_analysis import evaluate_risks  # ✅ Importación dentro de la función para evitar errores
    risks = evaluate_risks(document_text)
    return risks



