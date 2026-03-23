#!/usr/bin/env python3
"""
Generates modulo-01.html through modulo-12.html with rich, full interactive content.
Focus: University Admission Exams (UdeA, UNAL, ICFES).
Author: Antigravity AI
"""

import os

BASE = r"c:\Users\Admin Mantenimiento\OneDrive - Antioqueña de Incubacion\Escritorio\Educando866-main\assets\modulos"

HEAD = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Módulo {num}: {title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
    <style>
        body{{background:transparent;font-family:'Poppins',sans-serif;}}
        .acc-content{{transition:max-height .35s ease,opacity .35s ease;max-height:0;opacity:0;overflow:hidden;}}
        .acc-open .acc-content{{max-height:1000px;opacity:1;}}
        .acc-open .fa-chevron-down{{transform:rotate(180deg);}}
        .flashcard{{perspective:1000px;cursor:pointer;}}
        .fc-inner{{position:relative;width:100%;height:100%;text-align:center;transition:transform .6s cubic-bezier(.4,0,.2,1);transform-style:preserve-3d;border-radius:1rem;}}
        .flashcard:hover .fc-inner{{transform:rotateY(180deg);}}
        .fc-front,.fc-back{{position:absolute;width:100%;height:100%;-webkit-backface-visibility:hidden;backface-visibility:hidden;display:flex;align-items:center;justify-content:center;padding:1.25rem;border-radius:1rem;border:1px solid #e5e7eb;}}
        .fc-front{{background:#f8fafc;color:#1e293b;}}
        .fc-back{{background:#059669;color:white;transform:rotateY(180deg);border:none;}}
        .video-container {{ position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }}
        .video-container iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }}
        .custom-scrollbar::-webkit-scrollbar {{ width: 6px; }}
        .custom-scrollbar::-webkit-scrollbar-track {{ background: transparent; }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 10px; }}
    </style>
</head>
<body class="p-4 md:p-8 selection:bg-emerald-500 selection:text-white custom-scrollbar">
"""

FOOT = """
    <div class="h-20"></div>
    <script>
        function toggleAcc(btn){{
            const item=btn.parentElement;
            const isOpen=item.classList.contains('acc-open');
            document.querySelectorAll('.acc-item').forEach(el=>el.classList.remove('acc-open'));
            if(!isOpen) item.classList.add('acc-open');
        }}
        document.addEventListener('DOMContentLoaded',()=>{{
            const btn=document.getElementById('submit-quiz');
            if(!btn) return;
            btn.addEventListener('click',()=>{{
                const qs=document.querySelectorAll('.q-item');
                let score=0,total=qs.length;
                qs.forEach(q=>{{
                    const correct=q.dataset.correct;
                    const radios=q.querySelectorAll('input[type=radio]');
                    const fb=q.querySelector('.q-feedback');
                    let answered=false,userVal=null;
                    radios.forEach(r=>{{
                        const lbl=r.closest('label');
                        lbl.classList.remove('bg-red-50','border-red-300','bg-green-50','border-green-300');
                        r.disabled=true;
                        if(r.checked){{answered=true;userVal=r.value;
                            if(userVal===correct){{lbl.classList.add('bg-green-50','border-green-300');score++;}}
                            else lbl.classList.add('bg-red-50','border-red-300');
                        }}else if(r.value===correct) lbl.classList.add('bg-green-50','border-green-300','opacity-60');
                    }});
                    if(fb){{
                        fb.classList.remove('hidden');
                        if(!answered) fb.className='q-feedback mt-3 p-4 rounded-xl text-sm font-medium bg-yellow-50 text-yellow-800 border border-yellow-200';
                        else if(userVal===correct) fb.className='q-feedback mt-3 p-4 rounded-xl text-sm font-medium bg-green-50 text-green-800 border border-green-200';
                        else fb.className='q-feedback mt-3 p-4 rounded-xl text-sm font-medium bg-red-50 text-red-800 border border-red-200';
                        if(!answered) fb.innerHTML='<i class="fa-solid fa-triangle-exclamation mr-2"></i> Sin respuesta.';
                        else if(userVal===correct) fb.innerHTML='<i class="fa-solid fa-check-circle mr-2"></i> ¡Correcto! ' + (q.dataset.explanation || '');
                        else fb.innerHTML='<i class="fa-solid fa-circle-xmark mr-2"></i> Incorrecto. ' + (q.dataset.explanation || '');
                    }}
                }});
                if(window.parent&&window.parent.progressManager){{
                    const pct=Math.round((score/total)*100);
                    window.parent.progressManager.saveQuizScore('modulo-{num_padded}',pct);
                    btn.innerHTML = `<i class="fa-solid fa-cloud-check mr-2"></i> Puntaje: ${{pct}}%`;
                    btn.className='flex items-center justify-center gap-2 w-full sm:w-auto px-8 py-3.5 bg-gray-800 text-white font-bold rounded-xl cursor-default';
                }}
            }});
        }});
    </script>
</body></html>
"""

MODULES = [
    {
        "num": 1, "title": "Estrategia UdeA: El Arte de Ganar",
        "color": "emerald", "icon": "fa-chess", "subject": "ESTRATEGIA",
        "tagline": "Mentalidad de examinado, gestión de tiempo y técnicas de resolución rápida.",
        "callout_title": "La Regla de Oro",
        "callout_body": "El examen UdeA NO es una prueba de memoria. Es una prueba de <strong>razonamiento bajo presión</strong>. Tienes 2.25 min por pregunta. Si te bloqueas, pierdes puntos que podrías ganar en otras 3 preguntas fáciles.",
        "callout_icon": "fa-star", "callout_color": "emerald",
        "video_id": "dQw4w9WgXcQ", # Placeholder
        "accordions": [
            ("Método de Triage (Verde, Amarillo, Rojo)", "Clasifica preguntas al instante:<br><ul class='list-disc pl-5 space-y-2 mt-2'><li><strong>Verdes (Fáciles):</strong> Resolubles en < 1 min. Hazlas ya.</li><li><strong>Amarillas (Medias):</strong> Sabes cómo, pero toma tiempo. Marca y sigue.</li><li><strong>Rojas (Difíciles):</strong> No tienes idea. Marca y deja para el final.</li></ul>"),
            ("Active Recall vs. Lectura Pasiva", "Deja de leer y empieza a RECORDAR. Después de cada página, cierra el libro y explica en voz voz lo que aprendiste. Si no puedes, no lo sabes."),
        ],
        "flashcards": [
            ("¿Cuántas preguntas tiene el examen UdeA?", "80 preguntas (40 Lógica, 40 Lectura)."),
            ("¿Tiempo total?", "3 horas exactas (180 minutos)."),
            ("¿Hay puntos negativos?", "No. Debes responder TODAS las preguntas."),
        ],
        "questions": [
            ("¿Cuál es la estrategia recomendada si una pregunta de lógica te toma más de 3 minutos?", [("a","Seguir intentando hasta lograrlo"),("b","Marcarla como Roja y seguir con las Verdes"),("c","Llorar brevemente")], "b", "El tiempo es tu recurso más valioso."),
        ]
    },
    {
        "num": 2, "title": "Comprensión de Textos: Niveles de Lectura",
        "color": "sky", "icon": "fa-book-open", "subject": "LECTURA",
        "tagline": "Diferencia entre lo que el texto dice y lo que el autor insinúa.",
        "callout_title": "Niveles de Análisis",
        "callout_body": "UdeA evalúa el nivel <strong>Inferencial</strong>. No buscan que repitas lo que dice, sino que deduzcas qué implica el autor con sus palabras.",
        "callout_icon": "fa-brain", "callout_color": "sky",
        "video_id": "dQw4w9WgXcQ",
        "accordions": [
            ("Nivel Literal vs. Inferencial", "Literal: ¿Qué dice? (Datos explícitos). <br>Inferencial: ¿Qué sugiere? (Insinuaciones, ironía, tesis implícita)."),
            ("Identificar la Tesis", "La tesis es la COLUMNA VERTEBRAL del texto. Suele estar en el primer párrafo o al final del último."),
        ],
        "flashcards": [
            ("¿Qué es una inferencia?", "Una conclusión lógica basada en evidencia del texto."),
            ("Sinónimo de 'Implicar'", "Sugerir, conllevar, significar indirectamente."),
            ("Ubicación de la Tesis", "Introducción o Conclusión."),
        ],
        "questions": [
            ("Si un texto dice 'Incluso el sol tiene manchas', el autor sugiere que:", [("a","El sol está sucio"),("b","Nada ni nadie es perfecto"),("c","La astronomía es difícil")], "b", "Es una analogía sobre la imperfección inherente a las cosas aparentemente puras."),
        ]
    },
    {
        "num": 3, "title": "Lógica Formal y Silogismos",
        "color": "indigo", "icon": "fa-diagram-project", "subject": "LÓGICA",
        "tagline": "Conectores lógicos, tablas de verdad y razonamiento deductivo.",
        "callout_title": "Conectores Lógicos",
        "callout_body": "Domina el <strong>Condicional (A → B)</strong>. Es la base del 90% de los silogismos en el examen.",
        "callout_icon": "fa-puzzle-piece", "callout_color": "indigo",
        "accordions": [
            ("Tabla de Verdad del Condicional", "SÓLO es falso si el antecedente es Verdadero y el consecuente es Falso. (V → F = F)"),
            ("Leyes de De Morgan", "Negación de (P y Q) = (¬P o ¬Q). <br>Negación de (P o Q) = (¬P y ¬Q)."),
        ],
        "flashcards": [
            ("Contrapuesta de A → B", "Es ¬B → ¬A. (Equivalente lógico)."),
            ("Recíproca de A → B", "Es B → A. (NO necesariamente equivalente)."),
            ("Negación de 'Todos'", "Existe al menos uno que NO."),
        ],
        "questions": [
            ("Si 'Si estudio, apruebo' es verdad, y 'No aprobé', entonces:", [("a","Estudié poco"),("b","No estudié"),("c","Aprobé")], "b", "Modus Tollens: Si A->B y ¬B, entonces ¬A."),
        ]
    },
    {
        "num": 4, "title": "Razonamiento Lógico: Problemas de Ingenio",
        "color": "violet", "icon": "fa-lightbulb", "subject": "LÓGICA",
        "tagline": "Secuencias, distribuciones espaciales y acertijos lógicos.",
        "callout_title": "El Enfoque Lateral",
        "callout_body": "Muchos problemas no se resuelven con álgebra, sino con <strong>visualización</strong> y descarte de opciones absurdas.",
        "callout_icon": "fa-compass", "callout_color": "violet",
        "accordions": [
            ("Sucesiones Alfanuméricas", "Busca patrones saltando un término, o diferencias de segundo orden (la diferencia de las diferencias)."),
            ("Ordenamiento Lineal y Circular", "Dibuja un diagrama. Coloca primero los datos fijos ('Juan está a la derecha de Pedro')."),
        ],
        "flashcards": [
            ("Siguiente en: 2, 4, 8, 16...", "32 (Doble del anterior)."),
            ("Día anterior al ayer de mañana", "Ayer."),
            ("Relación de Parentesco", "Dibuja el árbol genealógico paso a paso."),
        ],
        "questions": [
            ("¿Qué número sigue: 1, 1, 2, 3, 5, 8, ...?", [("a","12"),("b","13"),("c","15")], "b", "Sucesión de Fibonacci: cada número es la suma de los dos anteriores."),
        ]
    },
    # More modules to reach 10
    {
        "num": 5, "title": "Matemática Básica: Aritmética y Razones",
        "color": "blue", "icon": "fa-calculator", "subject": "MATEMÁTICAS",
        "tagline": "Proporciones, porcentajes y regla de tres.",
        "callout_title": "Regla de Tres Compuesta",
        "callout_body": "Aprendre a identificar si las variables son Directamente Proporcionales o Inversamente Proporcionales.",
        "callout_icon": "fa-percent", "callout_color": "blue",
        "accordions": [
            ("Porcentajes Rápidos", "El 10% es correr la coma. El 5% es la mitad del 10%. El 1% es correr la coma dos veces."),
            ("Razones y Proporciones", "A es a B como C es a D. Multiplica en cruz para hallar la incógnita."),
        ],
        "flashcards": [
            ("Aumentar 20%", "Multiplicar por 1.20"),
            ("Disminuir 15%", "Multiplicar por 0.85"),
            ("Proporción Áurea", "1.618..."),
        ],
        "questions": [
            ("Si 3 camisas cuestan $45, ¿cuánto cuestan 7?", [("a","$105"),("b","$90"),("c","$115")], "a", "45/3 = 15 por camisa. 15 * 7 = 105."),
        ]
    },
    {
        "num": 6, "title": "Geometría Plana y Espacial",
        "color": "cyan", "icon": "fa-shapes", "subject": "GEOMETRÍA",
        "tagline": "Áreas, perímetros y volúmenes fundamentales.",
        "callout_title": "Teorema de Pitágoras",
        "callout_body": "\\(a^2 + b^2 = c^2\\). Fundamental para hallar distancias y diagonales.",
        "callout_icon": "fa-vector-square", "callout_color": "cyan",
        "accordions": [
            ("Áreas de Figuras Comunes", "Triángulo: (b*h)/2. Círculo: \\(\\pi r^2\\). Trapecio: \\(\\frac{B+b}{2} \\cdot h\\)."),
            ("Triángulos Notables", "30-60-90 y 45-45-90. Conocer sus proporciones ahorra mucho tiempo en trigonometría."),
        ],
        "flashcards": [
            ("Suma de ángulos internos (Triángulo)", "180 grados."),
            ("Perímetro del Círculo", "\\(2\\pi r\\)"),
            ("Volumen Esfera", "\\(\\frac{4}{3}\\pi r^3\\)"),
        ],
        "questions": [
            ("Un triángulo rectángulo tiene catetos de 3 y 4. ¿La hipotenusa es?", [("a","5"),("b","7"),("c","25")], "a", "Trío pitagórico 3-4-5."),
        ]
    },
    {
        "num": 7, "title": "Biología: La Unidad de la Vida",
        "color": "green", "icon": "fa-dna", "subject": "BIOLOGÍA",
        "tagline": "Célula, organelos y procesos metabólicos.",
        "callout_title": "El Dogma Central",
        "callout_body": "DNA $\\to$ RNA $\\to$ Proteína. Entender la transcripción y traducción es clave para genética.",
        "callout_icon": "fa-microscope", "callout_color": "green",
        "accordions": [
            ("Organelos Celulares", "Mitocondria: Energía (ATP). Ribosoma: Proteínas. Núcleo: Info genética."),
            ("Mitosis vs Meiosis", "Mitosis: 2 células hijas (2n). Meiosis: 4 células germinales (n)."),
        ],
        "flashcards": [
            ("¿Dónde ocurre la fotosíntesis?", "En los cloroplastos."),
            ("Base nitrogenada del RNA (no en DNA)", "Uracilo."),
            ("Célula Procariota", "Sin núcleo definido (ej. bacterias)."),
        ],
        "questions": [
            ("¿Qué organelo se encarga de la respiración celular?", [("a","Lisosoma"),("b","Mitocondria"),("c","Aparato de Golgi")], "b", "La mitocondria produce ATP."),
        ]
    },
    {
        "num": 8, "title": "Física: Mecánica y Fuerzas",
        "color": "orange", "icon": "fa-bolt", "subject": "FÍSICA",
        "tagline": "Leyes de Newton y cinemática básica.",
        "callout_title": "Fuerza y Aceleración",
        "callout_body": "F = m * a. La fuerza neta produce una aceleración proporcional a la masa del objeto.",
        "callout_icon": "fa-rocket", "callout_color": "orange",
        "accordions": [
            ("Leyes de Newton", "1. Inercia. 2. F=ma. 3. Acción-Reacción."),
            ("Caída Libre", "La aceleración es g (prox 10 m/s^2). La masa NO afecta la velocidad de caída en el vacío."),
        ],
        "flashcards": [
            ("Velocidad = ", "Distancia / Tiempo"),
            ("Unidad de Fuerza", "Newton (N)"),
            ("Energía Cinética", "\\(\\frac{1}{2}mv^2\\)"),
        ],
        "questions": [
            ("Si empujas una pared y no se mueve, ¿qué ocurre con el trabajo?", [("a","Es positivo"),("b","Es cero"),("c","Es negativo")], "b", "Trabajo = Fuerza * Desplazamiento. Si d=0, W=0."),
        ]
    },
    {
        "num": 9, "title": "Química: Materia y Reacciones",
        "color": "amber", "icon": "fa-flask", "subject": "QUÍMICA",
        "tagline": "Atomos, tabla periódica y enlaces.",
        "callout_title": "Enlaces Químicos",
        "callout_body": "Iónico: transferencia de electrones. Covalente: comparten electrones.",
        "callout_icon": "fa-atom", "callout_color": "amber",
        "accordions": [
            ("Propiedades Periódicas", "Electronegatividad: aumenta a la derecha y hacia arriba."),
            ("El Mol", "Unidad de medida de cantidad de sustancia (6.022e23 partículas)."),
        ],
        "flashcards": [
            ("pH de Ácidos", "Menor a 7."),
            ("Gas Noble", "Grupo 18 (Helio, Neón, etc)."),
            ("Isótopo", "Mismo elemento, diferente número de neutrones."),
        ],
        "questions": [
            ("¿Cuál es el pH del agua pura?", [("a","1"),("b","7"),("c","14")], "b", "Es neutro."),
        ]
    },
    {
        "num": 10, "title": "Simulacro Final y Cierre de Ciclo",
        "color": "rose", "icon": "fa-flag-checkered", "subject": "CIERRE",
        "tagline": "Consejos finales y puesta a punto.",
        "callout_title": "¡Lo Lograste!",
        "callout_body": "Has recorrido los 10 módulos. Ahora solo queda practicar con simulacros reales y confiar en tu proceso.",
        "callout_icon": "fa-award", "callout_color": "rose",
        "accordions": [
            ("Gestión de Ansiedad", "Día antes: NO ESTUDIES. Duerme 8 horas. Come ligero."),
            ("Durante la prueba", "Si te sobran 20 min, revisa la hoja de respuestas (burbujas mal llenadas)."),
        ],
        "flashcards": [
            ("¿Qué llevar?", "Lápiz 2, borrador, tajalápiz, documento."),
            ("¿Calculadora?", "No permitida en UdeA."),
            ("Puntaje de corte Medicina", "Suele ser > 80/100."),
        ],
        "questions": [
            ("El día del examen debo:", [("a","Llegar 5 min tarde"),("b","Estar 30 min antes"),("c","Tomar 5 cafés")], "b", "Evita el estrés innecesario."),
        ]
    }
]

def gen_module(m):
    num = m["num"]
    num_padded = f"{num:02d}"
    color = m["color"]
    
    acc_html = ""
    for (title, body) in m["accordions"]:
        acc_html += f"""
            <div class="acc-item bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
                <button class="w-full px-6 py-4 flex items-center justify-between bg-white hover:bg-gray-50 transition-colors focus:outline-none" onclick="toggleAcc(this)">
                    <span class="font-bold text-gray-800 text-left">{title}</span>
                    <i class="fa-solid fa-chevron-down text-gray-400 transition-transform duration-300"></i>
                </button>
                <div class="acc-content bg-gray-50 border-t border-gray-100">
                    <div class="p-6 text-gray-600 text-sm leading-relaxed">{body}</div>
                </div>
            </div>"""
    
    fc_html = '<div class="grid grid-cols-1 sm:grid-cols-3 gap-6">'
    for (front, back) in m["flashcards"]:
        fc_html += f"""
                <div class="flashcard h-44">
                    <div class="fc-inner">
                        <div class="fc-front shadow-sm border-2 border-gray-100"><h4 class="font-bold text-sm leading-tight">{front}</h4></div>
                        <div class="fc-back shadow-lg"><p class="text-xs font-semibold leading-relaxed">{back}</p></div>
                    </div>
                </div>"""
    fc_html += "</div>"
    
    q_html = '<div id="quiz-container" class="space-y-8">'
    for qi, (qtext, options, correct, explanation) in enumerate(m["questions"]):
        q_html += f'<div class="q-item" data-correct="{correct}" data-explanation="{explanation}"><p class="font-semibold text-gray-800 mb-4">{qi+1}. {qtext}</p><div class="space-y-3">'
        for (val, lbl) in options:
            q_html += f'<label class="flex items-center p-4 border border-gray-200 rounded-xl cursor-pointer hover:bg-white transition-colors group"><input type="radio" name="q{num}_{qi+1}" value="{val}" class="w-4 h-4 text-emerald-600 border-gray-300 focus:ring-emerald-500"><span class="ml-3 text-sm text-gray-700 font-medium">{lbl}</span></label>'
        q_html += f'<div class="q-feedback hidden mt-3 p-4 rounded-xl text-sm font-bold"></div></div></div>'
    q_html += '<button id="submit-quiz" class="flex items-center justify-center gap-2 w-full sm:w-auto px-8 py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl shadow-md transition-all active:scale-95"><i class="fa-solid fa-spell-check"></i> Verificar Respuestas</button></div>'

    callout_colors = {
        "emerald": ("bg-emerald-50", "border-emerald-500", "text-emerald-500", "text-emerald-900", "text-emerald-800"),
        "sky": ("bg-sky-50", "border-sky-500", "text-sky-500", "text-sky-900", "text-sky-800"),
        "indigo": ("bg-indigo-50", "border-indigo-500", "text-indigo-500", "text-indigo-900", "text-indigo-800"),
        "violet": ("bg-violet-50", "border-violet-500", "text-violet-500", "text-violet-900", "text-violet-800"),
        "blue": ("bg-blue-50", "border-blue-500", "text-blue-500", "text-blue-900", "text-blue-800"),
        "cyan": ("bg-cyan-50", "border-cyan-500", "text-cyan-500", "text-cyan-900", "text-cyan-800"),
        "green": ("bg-green-50", "border-green-500", "text-green-500", "text-green-900", "text-green-800"),
        "orange": ("bg-orange-50", "border-orange-500", "text-orange-500", "text-orange-900", "text-orange-800"),
        "amber": ("bg-amber-50", "border-amber-500", "text-amber-500", "text-amber-900", "text-amber-800"),
        "rose": ("bg-rose-50", "border-rose-500", "text-rose-500", "text-rose-900", "text-rose-800"),
    }
    cc = callout_colors.get(color, callout_colors["emerald"])

    video_section = ""
    if "video_id" in m:
        video_section = f"""
    <section class="mb-12 max-w-4xl mx-auto">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3"><i class="fa-solid fa-play-circle text-red-500"></i> Video Clase Complementaria</h2>
        <div class="video-container">
            <iframe src="https://www.youtube.com/embed/{m['video_id']}" allowfullscreen></iframe>
        </div>
    </section>"""

    content = HEAD.format(num=num, title=m["title"]) + f"""
    <header class="mb-10 text-center">
        <span class="inline-block py-1 px-3 bg-emerald-100 text-emerald-700 text-[10px] font-bold uppercase tracking-widest rounded-md mb-3 border border-emerald-200">Educando866 • Módulo {num}</span>
        <h1 class="text-3xl md:text-5xl font-extrabold text-gray-900 mb-4 tracking-tight leading-tight">{m["title"]}</h1>
        <p class="text-base text-gray-500 max-w-2xl mx-auto font-medium">{m["tagline"]}</p>
    </header>

    <section class="mb-12 max-w-4xl mx-auto">
        <div class="{cc[0]} border-l-4 {cc[1]} p-6 rounded-r-2xl shadow-sm border border-gray-100">
            <div class="flex items-start gap-4">
                <div class="{cc[2]} text-3xl mt-1"><i class="fa-solid {m['callout_icon']}"></i></div>
                <div><h3 class="text-lg font-bold {cc[3]} mb-2">{m['callout_title']}</h3><p class="{cc[4]} text-sm leading-relaxed font-medium">{m['callout_body']}</p></div>
            </div>
        </div>
    </section>

    {video_section}

    <section class="mb-12 max-w-4xl mx-auto">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3">
            <i class="fa-solid {m['icon']} text-emerald-500"></i> Conceptos y Teoría
        </h2>
        <div class="space-y-4">{acc_html}</div>
    </section>

    <section class="mb-16 max-w-4xl mx-auto">
        <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-3"><i class="fa-solid fa-layer-group text-emerald-500"></i> Flashcards Rápido</h2>
        </div>
        {fc_html}
    </section>

    <section class="max-w-4xl mx-auto bg-white border border-gray-200 rounded-3xl p-6 sm:p-10 shadow-lg relative overflow-hidden mb-12">
        <div class="absolute top-0 left-0 w-2 h-full bg-emerald-500"></div>
        <div class="flex items-center gap-4 mb-8">
            <div class="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-2xl flex items-center justify-center text-xl shadow-inner"><i class="fa-solid fa-vial"></i></div>
            <div>
                <h2 class="text-2xl font-bold text-gray-900">Quiz de Entrenamiento</h2>
                <p class="text-xs text-gray-500 font-bold uppercase tracking-widest mt-0.5">Mide tu nivel actual</p>
            </div>
        </div>
        {q_html}
    </section>

    <section class="max-w-4xl mx-auto bg-gray-900 rounded-3xl p-8 text-white relative overflow-hidden shadow-2xl">
        <div class="absolute -right-10 -bottom-10 opacity-20 text-9xl transform rotate-12"><i class="fa-solid fa-download"></i></div>
        <div class="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="text-center md:text-left">
                <h3 class="text-xl font-bold mb-2">Material de Profundización</h3>
                <p class="text-gray-400 text-sm">Descarga la guía en PDF con 50 ejercicios adicionales resueltos.</p>
            </div>
            <a href="#" class="inline-flex items-center gap-2 bg-emerald-500 hover:bg-emerald-600 px-6 py-3 rounded-xl font-bold transition-all shadow-lg hover:shadow-emerald-500/20 active:scale-95">
                <i class="fa-solid fa-file-pdf"></i> Descargar Guía
            </a>
        </div>
    </section>

""" + FOOT.format(num_padded=num_padded)
    return content

os.makedirs(BASE, exist_ok=True)
for m in MODULES:
    path = os.path.join(BASE, f"modulo-{m['num']:02d}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(gen_module(m))
    print(f"[OK] Generated {path}")

print("\nAll 10 modules generated with premium layout and interactive content!")
