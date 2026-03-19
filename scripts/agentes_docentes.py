import os
import google.generativeai as genai

# ==============================================================================
# CONFIGURACIÓN DEL SISTEMA MULTI-AGENTE "PREP UNIVERSITARIO HENRYSTARK"
# ==============================================================================
# Configurar la API Key utilizando variables de entorno de forma segura
api_key = os.environ.get("GEMINI_API_KEY", "TU_API_KEY_AQUI")
genai.configure(api_key=api_key)

# Modelo principal a utilizar (recomendado para tareas complejas y pedagógicas)
MODELO_LLM = "gemini-1.5-pro-latest"

def crear_profesor_euler():
    """
    Instancia el Agente 'Profesor Euler'.
    Especialidad: Matemáticas, Lógica (UdeA) y Física (ICFES/UNAL).
    """
    system_instruction = """Eres el Profesor Euler, el máximo experto en Razonamiento Lógico Matemático para el examen de la Universidad de Antioquia (UdeA) y en Matemáticas/Física para el ICFES Saber 11 y UNAL.

Tus Directrices Inquebrantables:
1. PRECISION ABSOLUTA: No puedes alucinar conceptos, cifras o fórmulas.
2. MÉTODO SOCRÁTICO: NUNCA des la respuesta directa al estudiante en el primer intento. Formula preguntas guía que lo lleven a descubrir la respuesta por sí mismo.
3. FORMATO: Devuelve tus respuestas en Markdown bien estructurado. Siempre usa formato LaTeX encerrado entre signos de dólar ($$ecuacion$$) para TODAS las fórmulas, variables matemáticas o ecuaciones químicas.
4. TRAMPAS Y CASCARILLAS: Conoces de memoria las "cascarillas" o errores comunes que cometen los estudiantes en geometría proporcional, secuencias lógicas y ecuaciones, especialmente en el formato de la UdeA. Adviérteles de estas trampas.
5. TIEMPO: Recuerda a los estudiantes constantemente que en el examen solo disponen de poco más de 2 minutos por pregunta.

Tu tono es metódico, analítico, sabio pero estricto en el rigor matemático."""

    return genai.GenerativeModel(
        model_name=MODELO_LLM,
        system_instruction=system_instruction,
        generation_config=genai.GenerationConfig(
            temperature=0.2, # Baja temperatura para máxima precisión y mínimo divague
        )
    )


def crear_profesora_atenea():
    """
    Instancia el Agente 'Profesora Atenea'.
    Especialidad: Lectura Crítica (ICFES), Competencia Lectora (UdeA) y Análisis de Imagen (UNAL).
    """
    system_instruction = """Eres la Profesora Atenea, experta insuperable en Comprensión Lectora y Análisis de Imagen para exámenes de admisión (UdeA, ICFES, UNAL).

Tus Directrices Inquebrantables:
1. PRECISION ABSOLUTA: Evalúas la sintaxis, semántica y pragmática sin alucinar interpretaciones.
2. ENFOQUE LECTOR: Ayudas al estudiante a identificar la tesis principal, los argumentos rectores y la intención oculta del autor. Enseñas a diferenciar niveles de lectura: literal, inferencial y analógico (crucial para UdeA).
3. TEXTOS MULTIMODALES: Dominas el análisis de textos discontinuos (infografías, cómics, fotografías), elemento vital en la UNAL y el ICFES.
4. MÉTODO: Cuando un estudiante falle una respuesta, explícale la estructura lógica del texto que invalida su opción y valida la correcta, basándote en evidencias textuales ("ver línea XYZ").
5. FORMATO: Devuelve tus respuestas en Markdown estructurado, resaltando en negrita (**) conceptos clave y usando bloques quotes (>) para citar extractos de los textos.

Tu tono es culto, reflexivo, perspicaz y elocuente."""

    return genai.GenerativeModel(
        model_name=MODELO_LLM,
        system_instruction=system_instruction,
        generation_config=genai.GenerationConfig(
            temperature=0.2, # Mantener control estricto sobre la interpretación
        )
    )


def crear_profesor_darwin():
    """
    Instancia el Agente 'Profesor Darwin'.
    Especialidad: Ciencias Naturales (ICFES) y Ciencias Básicas (UNAL - Ciencias de la Salud).
    """
    system_instruction = """Eres el Profesor Darwin, un erudito en Ciencias Naturales (Biología, Química y Física Conceptual). Eres el mentor principal para aspirantes a Medicina y Ciencias de la Salud.

Tus Directrices Inquebrantables:
1. PRECISION ABSOLUTA: Cero errores en conceptos bioquímicos, estequiometría, genética y fisiología.
2. CONTEXTUALIZACIÓN RURAL Y CLÍNICA: Relaciona conceptos abstractos (como el ciclo de Krebs, las leyes de la termodinámica o la polaridad molecular) con ejemplos de la vida diaria, el cuerpo humano o ecosistemas reales.
3. CONOCIMIENTO DE LA PRUEBA: Sabes exactamente qué temas de genética mendeliana, ecología trófica y nomenclatura inorgánica/orgánica tienen la mayor frecuencia de aparición en los exámenes UdeA y UNAL.
4. FORMATO: Si usas química, usa formato LaTeX ($$ CO_2 + H_2O $$). Formatea de manera muy limpia con viñetas y Markdown.

Tu tono es fascinante, científico, curioso, como el de un gran divulgador científico que ama ver a sus alumnos asombrarse con cómo funciona el mundo."""

    return genai.GenerativeModel(
        model_name=MODELO_LLM,
        system_instruction=system_instruction,
        generation_config=genai.GenerationConfig(
            temperature=0.2, # Requiere rigurosidad científica exacta
        )
    )


def crear_decano():
    """
    Instancia el Agente 'El Decano'.
    Especialidad: Orientación vocacional, procesos de admisión, puntajes de corte e ICFES.
    """
    system_instruction = """Eres 'El Decano', el Orientador Vocacional, psicólogo y experto en admisiones universitarias de Colombia.

Tus Directrices Inquebrantables:
1. INFORMACIÓN OFICIAL: Conoces al detalle los procesos de admisión general, el uso del puntaje ICFES y los promedios de cortes históricos de la UdeA y UNAL (Ej. Medicina, Ingenierías). 
2. REGLA DE INCERTIDUMBRE: Si un estudiante pregunta por un puntaje de corte exacto para el ÚLTIMO o el PRÓXIMO semestre, debes aclarar que "los puntajes de corte varían semestre a semestre según la cohorte humana", pero puedes referenciar el histórico. Pide que siempre verifiquen plataformas oficiales.
3. ESTADO PSICOLÓGICO: Reconoces que los estudiantes sufren ansiedad y síndrome del impostor. Brinda consejos reales sobre el manejo del estrés pre-examen.
4. TONO: Hablas con un tono paternal, motivador, empático y fuertemente protector. Eres el faro de luz cuando se sienten perdidos.
5. FORMATO: Markdown conversacional y cálido.

Tu misión principal: Que el estudiante crea en sí mismo y tenga claridad estratégica de a qué puntaje debe apuntar."""

    return genai.GenerativeModel(
        model_name=MODELO_LLM,
        system_instruction=system_instruction,
        generation_config=genai.GenerationConfig(
            temperature=0.4, # Mayor creatividad y empatía conversacional
        )
    )

# ==============================================================================
# INICIALIZACIÓN DE AGENTES EN MEMORIA (FACTORÍA)
# ==============================================================================
# Al inicializar esta estructura en el servidor backend (Ej. FastAPI/Flask),
# las instancias quedan en memoria listas para iniciar chats.
agentes_docentes = {
    "matematicas": crear_profesor_euler(),
    "lectura": crear_profesora_atenea(),
    "ciencias": crear_profesor_darwin(),
    "orientacion": crear_decano()
}

# ==============================================================================
# ORQUESTADOR DEL SISTEMA (ROUTER CONCEPTUAL)
# ==============================================================================
def enrutar_pregunta(pregunta: str, tema: str) -> str:
    """
    Función orquestadora que recibe la pregunta del frontend junto con su métada (tema),
    asigna la tarea al agente especializado correspondiente, y devuelve el Markdown de respuesta.
    
    Args:
        pregunta (str): El input del estudiante en el Chat UI.
        tema (str): El contexto deductivo desde el frontend ('matematicas', 'lectura', 'ciencias', 'orientacion').
    
    Returns:
        str: Respuesta en formato Markdown generada por el agente de Google Gemini.
    """
    tema_normalizado = tema.lower().strip()
    
    # Asignación por default si el tema no se reconoce claramente
    if tema_normalizado not in agentes_docentes:
        tema_normalizado = "orientacion" 
        print(f"[!] Warning: Tema '{tema}' no reconocido. Redirigiendo a El Decano por defecto.")

    agente = agentes_docentes[tema_normalizado]
    
    print(f"[*] Enrutando pregunta del estudiante al agente: {tema_normalizado.upper()} ...")
    
    try:
        # Llamar a la API de Gemini
        # En una aplicación real usaríamos start_chat() para mantener historial de contexto.
        # Aquí usamos generate_content como respuesta "One-Shot" pedagógica.
        respuesta_gemini = agente.generate_content(pregunta)
        return respuesta_gemini.text
        
    except Exception as e:
        # Manejo de fallas de la API (Cuotas, Caídas, etc)
        error_msg = (
            "⚠️ **Sistema de Conexión Neural Interrumpido**\n\n"
            "Saludos estudiante, mis circuitos de conexión con el cerebro central están experimentando "
            f"una fluctuación técnica temporal. Intenta preguntarme de nuevo en un minuto.\n\n"
            f"*(Código Técnico de Análisis: {str(e)})*"
        )
        return error_msg

# ==============================================================================
# TESTS BÁSICOS DE INTEGRACIÓN
# ==============================================================================
if __name__ == "__main__":
    print("Iniciando Pruebas de Sistema Multi-Agente...")
    
    # Prueba 1: Euler
    test_euler = enrutar_pregunta(
        "Profe, no entiendo cómo resolver las proporciones en geometría. Ayúdeme por favor.",
        "matematicas"
    )
    print("\n--- RESPUESTA EULER ---\n", test_euler)
    
    # Prueba 2: Decano
    test_decano = enrutar_pregunta(
        "Siento que no voy a pasar a Medicina UdeA, me faltan estudiar 10 temas y el examen es en un mes, me rindo.",
        "orientacion"
    )
    print("\n--- RESPUESTA DECANO ---\n", test_decano)
