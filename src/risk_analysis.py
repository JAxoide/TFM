from langchain_community.chat_models import ChatOpenAI
import os
from config import OPENAI_API_KEY

# Opcional: si tienes configuración externa

MODEL_NAME = "gpt-4-turbo"
TEMPERATURE = 0.3

def evaluate_risks(document_text: str) -> str:
    """
    Analiza el texto del documento y devuelve un string JSON con:
      - "questions": lista de preguntas para profundizar
      - (o en segunda fase) "identified_risks" y "mitigations"
    """
    llm = ChatOpenAI(
        model_name=MODEL_NAME,
        openai_api_key=OPENAI_API_KEY,
        temperature=TEMPERATURE,
    )

    prompt = f"""
Eres un experto en regulación y ética de la IA. Tu tarea es evaluar el siguiente documento y generar un informe sobre riesgos regulatorios y éticos del proyecto descrito.

---

### 🧭 Fase 1: Identificación de Riesgos Potenciales

1. Analiza el texto y detecta riesgos en las siguientes categorías:
   - Cumplimiento normativo (GDPR, AI Act, etc.)
   - Fairness y sesgos (género, raza, socioeconómicos, etc.)
   - Transparencia y explicabilidad
   - Privacidad y seguridad de datos
   - Impacto social y ético

2. Para cada riesgo, genera una o más **preguntas para el usuario** que te permitan confirmarlo o descartarlo. Ejemplo:
   - "¿El sistema toma decisiones automatizadas sobre personas? ¿Cómo se justifica legalmente eso?"

3. Devuelve solo las preguntas en formato JSON bajo la clave `"questions"`.

---

### 🧪 Fase 2: Informe Final (si ya se han respondido preguntas)

Si se te proporcionan respuestas del usuario, evalúa cada riesgo de nuevo y genera un informe JSON con:

- `"identified_risks"`: lista de riesgos confirmados, con justificación breve.
- `"mitigations"`: estrategias detalladas para mitigar cada riesgo detectado.

---

Texto del Documento:
\"\"\"
{document_text}
\"\"\"

Responde solo en formato JSON.
"""

    return llm.predict(prompt)