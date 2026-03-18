from pathlib import Path

from fpdf import FPDF


ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "assets" / "pdfs"


class StudyPDF(FPDF):
    def header(self):
        self.set_fill_color(6, 78, 59)
        self.rect(0, 0, 210, 18, style="F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 12)
        self.set_xy(10, 5)
        self.cell(0, 6, "VetPrep UdeA - Material de estudio", ln=1)
        self.ln(8)
        self.set_x(self.l_margin)
        self.set_text_color(33, 37, 41)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(108, 117, 125)
        self.cell(0, 6, f"Pagina {self.page_no()}", align="C")


def title(pdf: StudyPDF, text: str):
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(5, 150, 105)
    pdf.cell(0, 12, text, ln=1)
    pdf.set_text_color(33, 37, 41)
    pdf.set_x(pdf.l_margin)
    pdf.ln(1)


def section(pdf: StudyPDF, heading: str, body_lines: list[str]):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(4, 120, 87)
    pdf.multi_cell(0, 8, heading)
    pdf.set_text_color(33, 37, 41)
    pdf.set_font("Helvetica", "", 11)
    for line in body_lines:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 6, line)
    pdf.ln(2)


def generate_pdf_1(output_path: Path):
    pdf = StudyPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    title(pdf, "Guia de estudio 1 - Estrategia y Logica Matematica")
    section(
        pdf,
        "Como usar esta guia",
        [
            "Objetivo: mejorar puntaje en razonamiento logico para examen de admision.",
            "Metodo sugerido: 60 minutos diarios durante 10 dias.",
            "Bloque sugerido: 20 min teoria, 30 min ejercicios, 10 min revision de errores.",
        ],
    )

    section(
        pdf,
        "Modulo 1 - Pensamiento proporcional",
        [
            "1) Si una maquina produce 48 piezas en 6 horas, en 9 horas produce: (a) 60 (b) 72 (c) 81.",
            "2) En una receta para 4 personas se usan 300 g de arroz. Para 10 personas se necesitan: (a) 600 g (b) 650 g (c) 750 g.",
            "Estrategia: convierta a tasa por unidad y luego escale.",
        ],
    )

    section(
        pdf,
        "Modulo 2 - Regla de tres y porcentajes",
        [
            "1) Un articulo sube 20% y luego baja 20%. El precio final es igual, mayor o menor al inicial?",
            "2) Si una beca cubre 35% y el curso vale 50000 COP, cuanto paga el estudiante?",
            "Tip UdeA: evite intuicion, haga cuentas cortas con 100 como base.",
        ],
    )

    section(
        pdf,
        "Modulo 3 - Secuencias numericas",
        [
            "1) 2, 6, 12, 20, 30, __",
            "2) 81, 27, 9, 3, __",
            "3) 5, 9, 17, 33, __",
            "Revise diferencias, razones y combinaciones de patrones.",
        ],
    )

    section(
        pdf,
        "Modulo 4 - Tablas de verdad basicas",
        [
            "Proposiciones: p = llueve, q = llevo paraguas.",
            "Construya y evalua: p AND q, p OR q, NOT p.",
            "Ejercicio: indique cuando la expresion (p OR q) AND (NOT p) es verdadera.",
        ],
    )

    pdf.add_page()
    section(
        pdf,
        "Modulo 5 - Problemas de conteo",
        [
            "1) Cuantos numeros de 3 cifras se pueden formar con 1,2,3,4 sin repetir?",
            "2) En un grupo de 8 estudiantes, de cuantas formas se eligen 2 representantes?",
            "Clave: diferencie permutacion (importa orden) y combinacion (no importa orden).",
        ],
    )

    section(
        pdf,
        "Modulo 6 - Geometria util",
        [
            "Area triangulo = base x altura / 2",
            "Area circulo = pi x r^2",
            "Perimetro circulo = 2 x pi x r",
            "Ejercicio: radio 7 cm, calcule area y perimetro usando pi=3.14",
        ],
    )

    section(
        pdf,
        "Simulacro corto (10 preguntas)",
        [
            "Responda en maximo 15 minutos.",
            "1) 15% de 240 = ?",
            "2) Siguiente termino: 4, 7, 13, 25, ?",
            "3) Si 5 obreros terminan en 12 dias, 10 obreros en cuantos dias?",
            "4) Cuantos diagonales tiene un pentagono?",
            "5) Valor de x: 3x + 5 = 29",
            "6) Probabilidad de sacar cara en una moneda equilibrada.",
            "7) Si A implica B y A es verdadero, B es?",
            "8) 0.25 equivale a que porcentaje?",
            "9) Si un numero aumenta de 80 a 92, aumento porcentual?",
            "10) En un aula hay 12 mujeres y 18 hombres. Proporcion mujeres:hombres?",
        ],
    )

    section(
        pdf,
        "Clave de respuestas simulacro",
        [
            "1) 36",
            "2) 49",
            "3) 6 dias",
            "4) 5",
            "5) 8",
            "6) 1/2",
            "7) Verdadero",
            "8) 25%",
            "9) 15%",
            "10) 2:3",
        ],
    )

    section(
        pdf,
        "Checklist de calidad",
        [
            "- Tiempo por pregunta menor a 90 segundos.",
            "- Error por calculo menor a 10%.",
            "- Dominio de porcentajes y proporcionalidad mayor a 80%.",
            "- Revision final de errores al terminar cada sesion.",
        ],
    )

    pdf.output(str(output_path))


def generate_pdf_2(output_path: Path):
    pdf = StudyPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    title(pdf, "Guia de estudio 2 - Lectura critica y Ciencias base")
    section(
        pdf,
        "Plan de trabajo recomendado",
        [
            "Duracion: 2 semanas.",
            "Meta: subir precision en lectura critica y ciencias naturales.",
            "Sesion ideal: 70 min (30 lectura, 25 ciencias, 15 retroalimentacion).",
        ],
    )

    section(
        pdf,
        "Modulo 1 - Lectura critica",
        [
            "Identifique tesis central, tono del autor y proposito comunicativo.",
            "Pregunta tipo: cual es la idea principal del parrafo 2?",
            "Pregunta tipo: que inferencia es valida segun el texto?",
            "Regla: no responda por opinion personal, responda por evidencia textual.",
        ],
    )

    section(
        pdf,
        "Modulo 2 - Vocabulario en contexto",
        [
            "1) Determine significado por campo semantico del parrafo.",
            "2) Reemplace termino clave por sinonimo y verifique coherencia.",
            "3) Detecte conectores de contraste, causa y consecuencia.",
        ],
    )

    section(
        pdf,
        "Modulo 3 - Biologia esencial",
        [
            "Celula: membrana, nucleo, mitocondria, ribosoma.",
            "Genetica: ADN, gen, alelo, genotipo y fenotipo.",
            "Fisiologia: sistemas digestivo, respiratorio y circulatorio.",
            "Pregunta tipo: diferencia entre mitosis y meiosis.",
        ],
    )

    pdf.add_page()
    section(
        pdf,
        "Modulo 4 - Quimica base",
        [
            "Estructura atomica: proton, neutron, electron.",
            "Tabla periodica: tendencia de electronegatividad y radio atomico.",
            "Enlaces: ionico, covalente polar y no polar.",
            "Ejercicio: clasifique NaCl, H2O y O2 por tipo de enlace.",
        ],
    )

    section(
        pdf,
        "Modulo 5 - Fisica aplicada",
        [
            "Cinematica: velocidad = distancia / tiempo.",
            "Dinamica: F = m x a.",
            "Energia: potencial y cinetica.",
            "Ejercicio: masa 2 kg con aceleracion 3 m/s^2, fuerza resultante?",
        ],
    )

    section(
        pdf,
        "Simulacro integrado (10 preguntas)",
        [
            "1) Idea principal de un texto argumentativo.",
            "2) Funcion de un conector de contraste.",
            "3) Organelo responsable de energia celular.",
            "4) Diferencia clave entre mitosis y meiosis.",
            "5) Numero atomico representa que?",
            "6) Tipo de enlace en H2O.",
            "7) Formula de fuerza.",
            "8) Unidad SI de velocidad.",
            "9) Si un objeto recorre 100 m en 20 s, velocidad media?",
            "10) Inferencia valida frente a dato explicito.",
        ],
    )

    section(
        pdf,
        "Clave de respuestas simulacro",
        [
            "1) Tesis principal",
            "2) Oposicion entre ideas",
            "3) Mitocondria",
            "4) Mitosis mantiene cromosomas; meiosis reduce a la mitad",
            "5) Cantidad de protones",
            "6) Covalente polar",
            "7) F = m x a",
            "8) m/s",
            "9) 5 m/s",
            "10) La sustentada por evidencia del texto",
        ],
    )

    section(
        pdf,
        "Rubrica de avance",
        [
            "Nivel alto: 8 a 10 respuestas correctas por bloque.",
            "Nivel medio: 6 a 7 respuestas correctas por bloque.",
            "Nivel base: 0 a 5 respuestas correctas por bloque.",
            "Accion: repetir modulo con nivel base hasta subir a nivel medio.",
        ],
    )

    pdf.output(str(output_path))


def main():
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    generate_pdf_1(PDF_DIR / "guia-practica-1.pdf")
    generate_pdf_2(PDF_DIR / "guia-practica-2.pdf")
    print("PDF study materials generated successfully.")


if __name__ == "__main__":
    main()
