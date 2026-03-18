from pathlib import Path

from fpdf import FPDF


ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "assets" / "pdfs"


COURSE_CLASSES = [
    {
        "number": 1,
        "title": "Fundamentos de estrategia para examen UdeA",
        "module": "Estrategia",
        "objectives": [
            "Entender la estructura del examen y su logica de evaluacion.",
            "Construir un plan de estudio semanal medible.",
            "Aplicar tecnica de control de tiempo por bloque.",
        ],
        "concepts": [
            "Mapa del examen por competencias.",
            "Metodo 70-20-10: practica, analisis, retroalimentacion.",
            "Matriz de errores para priorizar estudio.",
        ],
        "guided_practice": [
            "Define meta de puntaje por competencia.",
            "Calcula tiempo por pregunta con margen de revision.",
            "Construye cronograma de 14 dias con bloques de 60 min.",
        ],
        "bank": {
            "basico": [
                "Que evalua principalmente el examen de admision?",
                "Cuantos minutos se recomiendan para revisar respuestas al final?",
                "Que variable debes medir cada semana para ver avance?",
            ],
            "intermedio": [
                "Como ajustas el plan si fallas en lectura critica y matematicas?",
                "Que criterio usas para priorizar temas de alto impacto?",
                "Describe una rutina de simulacro de 90 minutos.",
            ],
            "avanzado": [
                "Disena un plan de rescate para subir 15 puntos en 21 dias.",
                "Explica como reducir errores por ansiedad durante el examen.",
                "Plantea indicadores para decidir si repetir un modulo.",
            ],
        },
    },
    {
        "number": 2,
        "title": "Razonamiento numerico y proporcionalidad",
        "module": "Matematicas",
        "objectives": [
            "Resolver ejercicios de proporcion y regla de tres.",
            "Dominar porcentajes en contextos reales.",
            "Reducir errores de calculo rapido.",
        ],
        "concepts": [
            "Tasa unitaria.",
            "Cambio porcentual directo e inverso.",
            "Comparacion de razones.",
        ],
        "guided_practice": [
            "Convierte problemas verbales a expresiones numericas.",
            "Resuelve 10 ejercicios de porcentaje con verificacion inversa.",
            "Practica equivalencias de fraccion-decimal-porcentaje.",
        ],
        "bank": {
            "basico": [
                "Calcula 15% de 320.",
                "Si 4 cuadernos cuestan 20000 COP, cuanto valen 7?",
                "Transforma 0.375 a porcentaje.",
            ],
            "intermedio": [
                "Un precio sube 10% y luego baja 10%. El resultado final es mayor o menor?",
                "Si 6 personas hacen una tarea en 8 horas, cuantas horas tardan 4 personas?",
                "Compara las razones 18/24 y 21/28.",
            ],
            "avanzado": [
                "Disena un atajo mental para calcular 7.5% de cualquier numero.",
                "Resuelve un problema mixto de descuento + impuesto.",
                "Explica por que dos porcentajes opuestos no se anulan siempre.",
            ],
        },
    },
    {
        "number": 3,
        "title": "Secuencias, patrones y logica formal",
        "module": "Logica",
        "objectives": [
            "Identificar patrones aditivos y multiplicativos.",
            "Aplicar proposiciones logicas basicas.",
            "Justificar respuestas con pasos claros.",
        ],
        "concepts": [
            "Diferencias y segundas diferencias.",
            "Conectores logicos: Y, O, NO, SI...ENTONCES.",
            "Tablas de verdad simplificadas.",
        ],
        "guided_practice": [
            "Completa 12 secuencias numericas de dificultad creciente.",
            "Evalua 8 proposiciones compuestas.",
            "Detecta distractores por sobre-generalizacion.",
        ],
        "bank": {
            "basico": [
                "Completa: 3, 6, 12, 24, __.",
                "Evalua la negacion de la frase: hoy estudie.",
                "Completa: 5, 8, 11, 14, __.",
            ],
            "intermedio": [
                "Determina el valor faltante: 2, 5, 11, 23, __.",
                "Cuando es verdadera la expresion p AND q?",
                "Analiza patron en 1, 4, 9, 16, __.",
            ],
            "avanzado": [
                "Construye una tabla de verdad para (p OR q) AND (NOT p).",
                "Crea una secuencia propia y explica su regla en dos pasos.",
                "Resuelve una serie con patron alternado y justifica.",
            ],
        },
    },
    {
        "number": 4,
        "title": "Lectura critica I: idea central e inferencias",
        "module": "Lectura critica",
        "objectives": [
            "Identificar tesis y argumentos de apoyo.",
            "Distinguir informacion explicita e inferida.",
            "Responder con evidencia textual concreta.",
        ],
        "concepts": [
            "Tema vs idea principal.",
            "Inferencia valida.",
            "Tono y proposito del autor.",
        ],
        "guided_practice": [
            "Resume un texto argumentativo en 4 lineas.",
            "Separa hechos, opiniones e inferencias.",
            "Relaciona conectores con funcion discursiva.",
        ],
        "bank": {
            "basico": [
                "Que expresa la idea principal de un parrafo?",
                "Que diferencia hay entre dato e interpretacion?",
                "Que busca una pregunta inferencial?",
            ],
            "intermedio": [
                "Selecciona la mejor inferencia a partir de dos premisas.",
                "Identifica el tono del autor en un fragmento breve.",
                "Define la funcion del conector sin embargo.",
            ],
            "avanzado": [
                "Refuta una inferencia debil usando evidencia textual.",
                "Reescribe una conclusion para que sea logicamente valida.",
                "Analiza sesgo del narrador en un texto corto.",
            ],
        },
    },
    {
        "number": 5,
        "title": "Lectura critica II: vocabulario y estructura",
        "module": "Lectura critica",
        "objectives": [
            "Interpretar vocabulario por contexto.",
            "Reconocer estructura textual y jerarquia de ideas.",
            "Mejorar velocidad de comprension sin perder precision.",
        ],
        "concepts": [
            "Campo semantico.",
            "Coherencia y cohesion.",
            "Macroestructura textual.",
        ],
        "guided_practice": [
            "Marca terminos clave y define significado probable.",
            "Crea mapa conceptual de un texto de 3 parrafos.",
            "Identifica conectores de causa, contraste y conclusion.",
        ],
        "bank": {
            "basico": [
                "Que pista del contexto ayuda a definir una palabra?",
                "Que es cohesion textual?",
                "Que relacion expresa por lo tanto?",
            ],
            "intermedio": [
                "Sustituye un termino por sinonimo sin perder sentido.",
                "Ordena ideas secundarias segun prioridad.",
                "Detecta una ruptura de coherencia en un parrafo.",
            ],
            "avanzado": [
                "Reconstruye un texto desordenado justificando el orden.",
                "Identifica ambiguedad y propone version precisa.",
                "Evalua si la conclusion se deriva de las premisas.",
            ],
        },
    },
    {
        "number": 6,
        "title": "Biologia aplicada para admision",
        "module": "Biologia",
        "objectives": [
            "Dominar conceptos basicos de celula y genetica.",
            "Relacionar sistemas biologicos con funciones.",
            "Resolver preguntas de biologia contextualizadas.",
        ],
        "concepts": [
            "Organelos celulares y funcion.",
            "Mitosis y meiosis.",
            "Sistemas: respiratorio, circulatorio y digestivo.",
        ],
        "guided_practice": [
            "Completa cuadro comparativo mitosis vs meiosis.",
            "Relaciona organelo con funcion en 12 pares.",
            "Explica cadena de transporte de oxigeno en 5 pasos.",
        ],
        "bank": {
            "basico": [
                "Que organelo produce ATP?",
                "Que contiene el nucleo celular?",
                "Que sistema transporta nutrientes?",
            ],
            "intermedio": [
                "Diferencia genotipo y fenotipo con ejemplo.",
                "Explica intercambio gaseoso en alveolos.",
                "Identifica fase celular en una descripcion.",
            ],
            "avanzado": [
                "Analiza un caso de herencia mendeliana simple.",
                "Predice efecto de falla mitocondrial en tejido activo.",
                "Integra dos sistemas corporales en un escenario clinico.",
            ],
        },
    },
    {
        "number": 7,
        "title": "Quimica esencial: atomo, enlace y reaccion",
        "module": "Quimica",
        "objectives": [
            "Comprender estructura atomica y tabla periodica.",
            "Clasificar tipos de enlace quimico.",
            "Balancear reacciones sencillas.",
        ],
        "concepts": [
            "Numero atomico y masa atomica.",
            "Electronegatividad y polaridad.",
            "Ley de conservacion de la masa.",
        ],
        "guided_practice": [
            "Clasifica 15 compuestos por tipo de enlace.",
            "Balancea 8 ecuaciones basicas.",
            "Predice producto de una reaccion simple.",
        ],
        "bank": {
            "basico": [
                "Que representa el numero atomico?",
                "Que enlace predomina en NaCl?",
                "Que particula tiene carga negativa?",
            ],
            "intermedio": [
                "Compara enlace covalente polar vs no polar.",
                "Balancea: H2 + O2 -> H2O.",
                "Identifica agente oxidante en una reaccion simple.",
            ],
            "avanzado": [
                "Interpreta tendencia periodica en un grupo.",
                "Explica por que una molecula es polar con su geometria.",
                "Resuelve problema de estequiometria basica.",
            ],
        },
    },
    {
        "number": 8,
        "title": "Fisica base: movimiento y fuerza",
        "module": "Fisica",
        "objectives": [
            "Aplicar formulas de movimiento rectilineo.",
            "Resolver problemas con leyes de Newton.",
            "Interpretar graficas posicion-tiempo y velocidad-tiempo.",
        ],
        "concepts": [
            "Velocidad media y aceleracion.",
            "Fuerza neta.",
            "Trabajo y energia.",
        ],
        "guided_practice": [
            "Resuelve 10 ejercicios de MRU y MRUA.",
            "Calcula fuerza neta en sistemas de una dimension.",
            "Analiza pendiente en graficas cinemáticas.",
        ],
        "bank": {
            "basico": [
                "Formula de velocidad media.",
                "Unidad SI de fuerza.",
                "Que mide la aceleracion?",
            ],
            "intermedio": [
                "Calcula F para m=3 kg y a=2 m/s2.",
                "Un movil recorre 120 m en 15 s: velocidad?",
                "Relacion entre trabajo y energia.",
            ],
            "avanzado": [
                "Interpreta una grafica v-t con cambio de pendiente.",
                "Resuelve problema con dos fuerzas opuestas.",
                "Explica conservacion de energia en una caida libre ideal.",
            ],
        },
    },
    {
        "number": 9,
        "title": "Matematica avanzada: algebra y funciones",
        "module": "Matematicas",
        "objectives": [
            "Resolver ecuaciones lineales y cuadraticas.",
            "Interpretar funciones y sus graficas.",
            "Aplicar factorizacion en ejercicios de examen.",
        ],
        "concepts": [
            "Productos notables.",
            "Funcion lineal y cuadratica.",
            "Dominio e imagen.",
        ],
        "guided_practice": [
            "Factoriza 12 expresiones algebraicas.",
            "Resuelve 10 ecuaciones con verificacion.",
            "Traza grafica de funcion lineal y cuadratica.",
        ],
        "bank": {
            "basico": [
                "Resuelve: 2x + 7 = 19.",
                "Expande: (a+b)^2.",
                "Que representa la pendiente en una recta?",
            ],
            "intermedio": [
                "Resuelve: x^2 - 5x + 6 = 0.",
                "Determina interseccion con eje y para y=3x-4.",
                "Factoriza: x^2 + 7x + 12.",
            ],
            "avanzado": [
                "Analiza comportamiento de una funcion cuadratica por su discriminante.",
                "Modela un problema verbal con ecuacion cuadratica.",
                "Compara crecimiento lineal y cuadratico en contexto real.",
            ],
        },
    },
    {
        "number": 10,
        "title": "Simulacro final integrador y plan de cierre",
        "module": "Cierre",
        "objectives": [
            "Integrar competencias vistas en 10 clases.",
            "Medir rendimiento final y brechas pendientes.",
            "Definir plan de mantenimiento previo al examen.",
        ],
        "concepts": [
            "Gestion de tiempo en simulacro completo.",
            "Priorizacion de preguntas por dificultad.",
            "Revision final basada en evidencia.",
        ],
        "guided_practice": [
            "Ejecuta simulacro de 40 preguntas en 90 minutos.",
            "Clasifica errores en conceptual, proceso y distraccion.",
            "Cierra con plan de repaso de 7 dias.",
        ],
        "bank": {
            "basico": [
                "Cuanto tiempo asignar por pregunta en promedio?",
                "Que haces si una pregunta toma mas de 2 minutos?",
                "Que informacion no puede faltar en tu matriz de errores?",
            ],
            "intermedio": [
                "Define regla para decidir cuando adivinar de forma estrategica.",
                "Construye esquema de repaso para 3 dias finales.",
                "Como equilibrar precision y velocidad?",
            ],
            "avanzado": [
                "Diseña un informe final de rendimiento por competencia.",
                "Propone estrategia anti-fatiga para examen largo.",
                "Define indicadores minimos para presentarte con confianza.",
            ],
        },
    },
]


class StudyPDF(FPDF):
    def header(self):
        self.set_fill_color(6, 78, 59)
        self.rect(0, 0, 210, 18, style="F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 12)
        self.set_xy(10, 5)
        self.cell(0, 6, "VetPrep UdeA - Curso Premium", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        self.set_text_color(33, 37, 41)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(108, 117, 125)
        self.cell(0, 6, f"Pagina {self.page_no()}", align="C")


def write_title(pdf: StudyPDF, class_data: dict):
    pdf.set_fill_color(220, 252, 231)
    pdf.set_draw_color(16, 185, 129)
    pdf.rect(10, 24, 190, 26, style="DF")
    pdf.set_xy(14, 29)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(5, 150, 105)
    pdf.multi_cell(182, 8, f"Clase {class_data['number']}: {class_data['title']}")
    pdf.set_text_color(33, 37, 41)
    pdf.set_y(56)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, f"Modulo: {class_data['module']} | Nivel: Curso completo de 10 clases")
    pdf.ln(2)


def write_section(pdf: StudyPDF, heading: str, lines: list[str]):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(4, 120, 87)
    pdf.multi_cell(0, 8, heading)
    pdf.set_text_color(33, 37, 41)
    pdf.set_font("Helvetica", "", 11)
    for item in lines:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 6, f"- {item}")
    pdf.ln(1)


def write_bank(pdf: StudyPDF, bank: dict):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(4, 120, 87)
    pdf.multi_cell(0, 8, "Banco de preguntas por nivel")
    pdf.set_text_color(33, 37, 41)
    for level in ("basico", "intermedio", "avanzado"):
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 7, f"Nivel {level}")
        pdf.set_font("Helvetica", "", 11)
        for idx, question in enumerate(bank[level], start=1):
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, 6, f"{idx}. {question}")
        pdf.ln(1)


def write_answer_guide(pdf: StudyPDF):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(4, 120, 87)
    pdf.multi_cell(0, 8, "Guia de autocorreccion")
    pdf.set_text_color(33, 37, 41)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 6, "Usa esta escala para calificar cada bloque de preguntas.")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 6, "- Alto: 80% a 100% de aciertos.")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 6, "- Medio: 60% a 79% de aciertos.")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 6, "- Base: menos de 60% de aciertos.")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 6, "Si quedas en nivel base, repite el modulo antes de avanzar.")


def generate_class_pdf(class_data: dict):
    pdf = StudyPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    write_title(pdf, class_data)
    write_section(pdf, "Objetivos de aprendizaje", class_data["objectives"])
    write_section(pdf, "Conceptos clave", class_data["concepts"])
    write_section(pdf, "Practica guiada", class_data["guided_practice"])

    pdf.add_page()
    write_bank(pdf, class_data["bank"])
    write_answer_guide(pdf)

    filename = f"clase-{class_data['number']:02d}.pdf"
    pdf.output(str(PDF_DIR / filename))


def write_manifest():
    manifest_path = PDF_DIR / "README.md"
    lines = [
        "# Material PDF del curso",
        "",
        "Este directorio contiene las 10 guias oficiales del curso VetPrep UdeA.",
        "Generacion automatica: `scripts/generate_study_pdfs.py`.",
        "",
    ]
    for class_data in COURSE_CLASSES:
        lines.append(f"- clase-{class_data['number']:02d}.pdf - Clase {class_data['number']}: {class_data['title']}")
    manifest_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    for class_data in COURSE_CLASSES:
        generate_class_pdf(class_data)
    write_manifest()
    print("10 PDF study materials generated successfully.")


if __name__ == "__main__":
    main()
