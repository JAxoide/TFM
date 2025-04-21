from langchain_community.chat_models import ChatOpenAI
from document_processing import process_document  # ✅ Solo si es necesario
from document_processing import load_document

def evaluate_risks(document_text):
    """
    Evalúa los riesgos regulatorios y éticos del documento analizando su contenido.
    Retorna una evaluación categorizada de riesgos.
    """
    llm = ChatOpenAI(model_name="gpt-4-turbo")  # Usa GPT-4 Turbo

    prompt = f"""
   Eres un experto en regulación y ética de la IA. Tu tarea es analizar el siguiente documento y generar un informe detallado sobre los riesgos regulatorios y éticos que pueda presentar el proyecto descrito.

### **Fase 1: Identificación de Riesgos y Preguntas para el Usuario**
1. Analiza el documento y detecta riesgos en las siguientes categorías:
   - Cumplimiento normativo (GDPR, AI Act, etc.).
   - Fairness y sesgos (género, raza, socioeconómicos, etc.).
   - Transparencia y explicabilidad del sistema.
   - Privacidad y seguridad de los datos.
   - Impacto social y ético.

2. Para cada posible riesgo identificado, genera **preguntas para el usuario** que ayuden a confirmar o descartar el riesgo. 
   - Ejemplo: Si detectas que el modelo usa datos demográficos sin explicaciones claras, pregunta:  
     *"El modelo diferencia las respuestas según el género del usuario? ¿Cómo se garantiza que esto no genere sesgos?"*

3. Devuelve solo las preguntas en una lista JSON bajo la clave `"questions"`. Espera la respuesta del usuario antes de generar el informe.

### **Fase 2: Generación del Informe**
Tras recibir las respuestas del usuario, genera un informe con los siguientes apartados:

#### 📌 **1. Identificación de Riesgos**
- Enumera los riesgos confirmados tras la interacción con el usuario.
- Justifica cada riesgo con ejemplos específicos del documento.

#### 🛠 **2. Estrategias de Mitigación**
- Propón soluciones detalladas para cada riesgo detectado.
- Explica cómo estas estrategias ayudan a cumplir normativas y principios éticos.

#### 📝 **3. Conclusiones**
- Resumen de la evaluación realizada.
- Recomendaciones finales para reducir los riesgos del proyecto.

### **Datos del Documento:**
{document_text}

Responde en formato JSON con claves `"questions"` para la Fase 1 y `"report"` para la Fase 2.
"""

    response = llm.predict(prompt)
    return response  # Devuelve la evaluación en JSON

document_text = load_document("data/ai_act_summary.txt")
risks = evaluate_risks(document_text)

print("Evaluación de Riesgos:")
print(risks)