import streamlit as st
from document_processing import process_uploaded_file
from risk_analysis import evaluate_risks
import json # Sigue siendo útil para depuración o si decides serializar algo.

st.set_page_config(page_title="DeepEval – Evaluación de Riesgos en IA", layout="wide")

st.title("ߤ֠Evaluación Ética y Regulatoria de Proyectos de IA")

# 1. Subida del documento
uploaded_file = st.file_uploader("ߓĠSube un documento del proyecto (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])

# Usar st.session_state para mantener el estado entre ejecuciones de Streamlit
if 'document_text' not in st.session_state:
    st.session_state.document_text = None
if 'questions' not in st.session_state:
    st.session_state.questions = None
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'final_report' not in st.session_state:
    st.session_state.final_report = None

if uploaded_file:
    # Si se sube un nuevo archivo o es el mismo, procesar
    if st.session_state.document_text is None or uploaded_file.name != st.session_state.last_uploaded_file_name:
        with st.spinner("ߔ͠Analizando el contenido del documento..."):
            document_text = process_uploaded_file(uploaded_file)
            st.session_state.document_text = document_text
            st.session_state.last_uploaded_file_name = uploaded_file.name # Guardar el nombre para saber si el archivo ha cambiado
            # Resetear estados al subir un nuevo archivo
            st.session_state.questions = None
            st.session_state.user_answers = {}
            st.session_state.final_report = None
            st.session_state.show_evaluate_button = True # Mostrar el botón de evaluar riesgos para la Fase 1
    
    st.subheader("ߓؠVista previa del documento:")
    st.text_area("Texto extraído", st.session_state.document_text, height=300, key="document_preview_text_area")

    # Botón para la FASE 1: Evaluar riesgos iniciales
    if st.session_state.show_evaluate_button:
        if st.button("ߚȠEvaluar riesgos iniciales"):
            with st.spinner("ߤ֠Generando evaluación de riesgos (Fase 1)..."):
                response_data = evaluate_risks(st.session_state.document_text)

                if "error" in response_data:
                    st.error(f"❌ Error en la evaluación de riesgos (Fase 1): {response_data['error']}")
                    if "details" in response_data:
                        st.exception(response_data['details'])
                    if "raw_response" in response_data:
                        st.text(f"Respuesta cruda del modelo (para depuración):\n{response_data['raw_response']}")
                elif "questions" in response_data and response_data["questions"]:
                    st.session_state.questions = response_data["questions"]
                    st.session_state.show_evaluate_button = False # Ocultar este botón una vez generadas las preguntas
                    st.session_state.user_answers = {q: "" for q in st.session_state.questions} # Inicializar respuestas vacías
                    st.session_state.final_report = None # Resetear el informe final
                else:
                    st.error("No se encontraron preguntas válidas en la respuesta del modelo. Asegúrate de que el modelo respondió en la Fase 1.")
                    st.json(response_data) # Muestra la respuesta para depuración

# Mostrar preguntas y permitir respuestas (Fase 1.5)
if st.session_state.questions:
    st.subheader("❓ Por favor, responde a las siguientes preguntas para profundizar:")
    # Usar un formulario para agrupar las entradas y un solo botón de envío
    with st.form("risk_questions_form"):
        for i, q in enumerate(st.session_state.questions, 1):
            st.session_state.user_answers[q] = st.text_area(f"**{i}.** {q}", value=st.session_state.user_answers.get(q, ""), key=f"q_{i}")
        
        # Botón para la FASE 2: Generar informe final
        submit_answers_button = st.form_submit_button("✅ Generar Informe Final")

        if submit_answers_button:
            with st.spinner("ߤ֠Generando el informe final de riesgos (Fase 2)..."):
                # Llamar a evaluate_risks con las respuestas del usuario
                response_data = evaluate_risks(st.session_state.document_text, user_responses=st.session_state.user_answers)

                if "error" in response_data:
                    st.error(f"❌ Error al generar el informe final (Fase 2): {response_data['error']}")
                    if "details" in response_data:
                        st.exception(response_data['details'])
                    if "raw_response" in response_data:
                        st.text(f"Respuesta cruda del modelo (para depuración):\n{response_data['raw_response']}")
                elif "identified_risks" in response_data and "mitigations" in response_data:
                    st.session_state.final_report = response_data
                    st.session_state.questions = None # Ocultar las preguntas una vez que el informe final esté listo
                    st.session_state.user_answers = {} # Limpiar las respuestas
                else:
                    st.error("El modelo no devolvió un informe final válido. Asegúrate de que el modelo respondió en la Fase 2.")
                    st.json(response_data) # Muestra la respuesta para depuración

# Mostrar el informe final (Fase 2)
if st.session_state.final_report:
    st.subheader("ߓʠInforme Final de Riesgos:")
    
    if st.session_state.final_report.get("identified_risks"):
        st.markdown("### Riesgos Identificados:")
        for risk in st.session_state.final_report["identified_risks"]:
            if isinstance(risk, dict) and "risk_name" in risk and "justification" in risk:
                st.markdown(f"#### **{risk['risk_name']}**")
                st.write(f"**Justificación:** {risk['justification']}")
            else:
                # Caso de fallback si el formato de los riesgos no es el esperado
                st.write(f"- {risk}")

    if st.session_state.final_report.get("mitigations"):
        st.markdown("### Estrategias de Mitigación:")
        for mitigation in st.session_state.final_report["mitigations"]:
            if isinstance(mitigation, dict) and "strategy" in mitigation and "details" in mitigation:
                st.markdown(f"#### **{mitigation['strategy']}**")
                st.write(f"**Detalles:** {mitigation['details']}")
            else:
                # Caso de fallback si el formato de las mitigaciones no es el esperado
                st.write(f"- {mitigation}")

    if not st.session_state.final_report.get("identified_risks") and not st.session_state.final_report.get("mitigations"):
        st.warning("El informe final no contiene riesgos identificados ni estrategias de mitigación.")
        st.json(st.session_state.final_report) # Muestra el contenido completo para depuración
