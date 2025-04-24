import streamlit as st
from document_processing import process_uploaded_file
from risk_analysis import evaluate_risks
import json

st.set_page_config(page_title="DeepEval – Evaluación de Riesgos en IA", layout="wide")

st.title("🤖 DeepEval: Evaluación Ética y Regulatoria de Proyectos de IA")

# 1. Subida del documento
uploaded_file = st.file_uploader("📄 Sube un documento del proyecto (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])

if uploaded_file:
    # 2. Extracción de texto
    with st.spinner("🔍 Analizando el contenido del documento..."):
        document_text = process_uploaded_file(uploaded_file)

    st.subheader("📘 Vista previa del documento:")
    st.text_area("Texto extraído", document_text, height=300)

    # 3. Evaluación de riesgos
    if st.button("🚨 Evaluar riesgos"):
        with st.spinner("🤖 Generando evaluación de riesgos..."):
            raw_response = evaluate_risks(document_text)

            try:
                response = json.loads(raw_response)
                if "questions" in response:
                    st.subheader("❓ Preguntas para profundizar:")
                    for i, q in enumerate(response["questions"], 1):
                        st.markdown(f"**{i}.** {q}")
                else:
                    st.error("No se encontraron preguntas en la respuesta del modelo.")
            except json.JSONDecodeError:
                st.error("❌ Error al interpretar la respuesta del modelo.")
                st.text(raw_response)
