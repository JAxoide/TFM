# risk_analysis.py

from langchain_community.chat_models import ChatOpenAI
import os
import json # ¡IMPORTANTE! Asegúrate de importar json
from config import OPENAI_API_KEY, MODEL_NAME # Asegúrate de que MODEL_NAME también esté en config.py si lo usas

# Si MODEL_NAME y TEMPERATURE no están en config.py, defínelos aquí
# MODEL_NAME = "gpt-4-turbo" # O el modelo que estés usando
TEMPERATURE = 0.3

def evaluate_risks(document_text: str, user_responses: dict = None) -> dict:
    """
    Analiza el texto del documento y devuelve un diccionario con:
      - "questions": lista de preguntas para profundizar (Fase 1)
      - O "identified_risks" y "mitigations" (Fase 2)
    user_responses: Diccionario con las respuestas a las preguntas anteriores si estamos en Fase 2.
    
    Esta función ahora se encarga de parsear la respuesta del LLM a un diccionario
    Python y manejar errores de JSON.
    """
    llm = ChatOpenAI(
        model_name=MODEL_NAME, # Asegúrate de que MODEL_NAME esté definido o importado
        openai_api_key=OPENAI_API_KEY,
        temperature=TEMPERATURE,
    )

    # Construye el prompt según la fase
    if user_responses:
        # Estamos en Fase 2, incluir las respuestas del usuario
        response_text = "\n\nRespuestas del usuario:\n"
        for q, a in user_responses.items():
            response_text += f"- Pregunta: {q}\n  Respuesta: {a}\n"
        
        prompt_phase = f"""
### ߧʠFase 2: Informe Final (si ya se han respondido preguntas)

Se te han proporcionado respuestas del usuario a las preguntas de la Fase 1. Evalúa cada riesgo de nuevo, teniendo en cuenta estas respuestas y el documento original.

Genera un informe JSON con:

- `"identified_risks"`: lista de riesgos confirmados, con justificación breve.
- `"mitigations"`: estrategias detalladas para mitigar cada riesgo detectado.

---
{response_text}
"""
    else:
        # Estamos en Fase 1, solo preguntas
        prompt_phase = """
### ߧ͠Fase 1: Identificación de Riesgos Potenciales

1. Analiza el texto y detecta riesgos en las siguientes categorías:
    - Cumplimiento normativo (GDPR, AI Act, etc.)
    - Fairness y sesgos (género, raza, socioeconómicos, etc.)
    - Transparencia y explicabilidad
    - Privacidad y seguridad de datos
    - Impacto social y ético

2. Para cada riesgo, genera una o más **preguntas para el usuario** que te permitan confirmarlo o descartarlo. Ejemplo:
    - "¿El sistema toma decisiones automatizadas sobre personas? ¿Cómo se justifica legalmente eso?"

3. Devuelve solo las preguntas en formato JSON bajo la clave `"questions"`.
"""

    full_prompt = f"""
Eres un experto en regulación y ética de la IA. Tu tarea es evaluar el siguiente documento y generar un informe sobre riesgos regulatorios y éticos del proyecto descrito.

---
{prompt_phase}
---

Texto del Documento:
\"\"\"
{document_text}
\"\"\"

Responde solo en formato JSON.
"""

    raw_llm_response = llm.predict(full_prompt)
    
    # --- INICIO DEL MANEJO DE ERRORES Y LIMPIEZA DE JSON ---
    try:
        # Intenta encontrar el bloque de código JSON (```json...```)
        if "```json" in raw_llm_response:
            # Extrae solo el contenido dentro del bloque ```json
            json_str_start = raw_llm_response.find("```json") + len("```json")
            json_str_end = raw_llm_response.find("```", json_str_start)
            if json_str_end != -1:
                json_content = raw_llm_response[json_str_start:json_str_end].strip()
            else: # Si no encuentra la etiqueta de cierre, toma el resto
                json_content = raw_llm_response[json_str_start:].strip()
        else:
            # Si no hay bloque de código, asume que la respuesta completa es el JSON
            json_content = raw_llm_response.strip()

        # Intenta parsear el string JSON a un diccionario de Python
        parsed_json_data = json.loads(json_content)
        
        # Devuelve el diccionario de Python directamente.
        # Streamlit lo manejará mejor si recibe el dict, no un string JSON serializado de nuevo.
        return parsed_json_data 

    except json.JSONDecodeError as e:
        # Imprime el error y la respuesta cruda para depuración
        print(f"ERROR en risk_analysis.py: JSONDecodeError al parsear la respuesta del LLM: {e}")
        print(f"La respuesta cruda (sin limpiar) fue:\n{raw_llm_response}")
        print(f"El contenido intentado como JSON (limpio) fue:\n{json_content}")
        
        # Opcional: Podrías devolver un diccionario de error o levantar una excepción más amigable
        # Para que Streamlit no falle completamente, podrías devolver un diccionario con un mensaje de error
        return {"error": "El modelo no devolvió un JSON válido.", "details": str(e), "raw_response": raw_llm_response}
    except Exception as e:
        print(f"ERROR inesperado en risk_analysis.py al procesar la respuesta: {e}")
        return {"error": "Ocurrió un error inesperado al procesar la respuesta del modelo.", "details": str(e)}
