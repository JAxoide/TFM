import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import streamlit as st
from document_processing import process_document
from llm import ask_question


st.title("Evaluación de Riesgos en IA Generativa")

# Subida de archivo
uploaded_file = st.file_uploader("Sube un documento (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    text = process_document(uploaded_file)
    st.session_state["document_text"] = text
    st.success("Documento cargado correctamente.")
    st.write("### Resumen inicial:")
    st.write(text[:1000] + "...")  # Muestra los primeros 1000 caracteres

pregunta = "¿Cuáles son los principales riesgos del AI Act?"
respuesta = ask_question(pregunta)
print(respuesta)