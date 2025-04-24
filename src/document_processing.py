import os
import PyPDF2
import docx

def load_document_from_path(file_path: str) -> str:
    """Carga el contenido de un archivo de texto o PDF desde disco."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo no existe: {file_path}")

    _, ext = os.path.splitext(file_path)
    if ext.lower() == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext.lower() == ".pdf":
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join(
                page.extract_text() or "" for page in reader.pages
            )
    else:
        raise ValueError(f"Formato no soportado: {ext}")

def extract_text_from_pdf(pdf_file) -> str:
    """Extrae texto de un objeto file-like PDF cargado por Streamlit."""
    reader = PyPDF2.PdfReader(pdf_file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(docx_file) -> str:
    """Extrae texto de un objeto file-like DOCX cargado por Streamlit."""
    doc = docx.Document(docx_file)
    return "\n".join(para.text for para in doc.paragraphs)

def extract_text_from_txt(txt_file) -> str:
    """Extrae texto de un objeto file-like TXT cargado por Streamlit."""
    return txt_file.read().decode("utf-8")

def process_uploaded_file(uploaded_file) -> str:
    """
    Procesa un archivo subido por el usuario (pdf, docx o txt)
    y devuelve todo su texto.
    """
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    if name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    if name.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    raise ValueError(f"Formato no compatible: {uploaded_file.name}")
