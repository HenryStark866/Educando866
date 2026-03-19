#!/usr/bin/env python3
"""
Generates modulo-03.html through modulo-10.html with rich, full interactive content.
Run from the project root: python scripts/generate_modules.py
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
        .acc-open .acc-content{{max-height:600px;opacity:1;}}
        .acc-open .fa-chevron-down{{transform:rotate(180deg);}}
        .flashcard{{perspective:1000px;cursor:pointer;}}
        .fc-inner{{position:relative;width:100%;height:100%;text-align:center;transition:transform .6s cubic-bezier(.4,0,.2,1);transform-style:preserve-3d;border-radius:1rem;}}
        .flashcard:hover .fc-inner{{transform:rotateY(180deg);}}
        .fc-front,.fc-back{{position:absolute;width:100%;height:100%;-webkit-backface-visibility:hidden;backface-visibility:hidden;display:flex;align-items:center;justify-content:center;padding:1.25rem;border-radius:1rem;border:1px solid #e5e7eb;}}
        .fc-front{{background:#f8fafc;color:#1e293b;}}
        .fc-back{{background:#059669;color:white;transform:rotateY(180deg);border:none;}}
    </style>
</head>
<body class="p-4 md:p-8 selection:bg-emerald-500 selection:text-white">
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
                        else if(userVal===correct) fb.innerHTML='<i class="fa-solid fa-check-circle mr-2"></i> ¡Correcto!';
                        else fb.innerHTML='<i class="fa-solid fa-circle-xmark mr-2"></i> Incorrecto. Revisa el acordeón correspondiente.';
                    }}
                }});
                if(window.parent&&window.parent.progressManager){{
                    const pct=Math.round((score/total)*100);
                    window.parent.progressManager.saveQuizScore('modulo-{num_padded}',pct);
                    btn.textContent=`Guardado (${{pct}}%)`;
                    btn.className='flex items-center justify-center gap-2 w-full sm:w-auto px-8 py-3.5 bg-gray-800 text-white font-bold rounded-xl cursor-default';
                }}
            }});
        }});
    </script>
</body></html>
"""

MODULES = [
    {
        "num": 3, "title": "Lógica Formal y Silogismos",
        "color": "indigo", "icon": "fa-diagram-project", "subject": "LÓGICA",
        "tagline": "Conectores lógicos, tablas de verdad y razonamiento deductivo para el examen de admisión.",
        "callout_title": "¿Qué evalúa la Sección de Lógica?",
        "callout_body": "El examen UdeA evalúa tu capacidad de inferir conclusiones válidas a partir de premisas. <strong>No necesitas saber matemáticas avanzadas</strong>: necesitas pensar con claridad bajo presión.",
        "callout_icon": "fa-puzzle-piece", "callout_color": "indigo",
        "accordions": [
            ("Conectores Lógicos (La Base de Todo)", "Los conectores son las palabras que unen proposiciones.<br><br><ul class='list-disc pl-5 space-y-2'><li><strong>Conjunción (P ∧ Q):</strong> 'P y Q'. Verdadera solo si AMBAS son verdaderas.</li><li><strong>Disyunción (P ∨ Q):</strong> 'P o Q'. Verdadera si AL MENOS UNA es verdadera.</li><li><strong>Negación (¬P):</strong> 'No P'. Invierte el valor de verdad.</li><li><strong>Condicional (P → Q):</strong> 'Si P, entonces Q'. Solo falsa si P es verdadera y Q es falsa.</li></ul>"),
            ("Silogismos: Deducción de Conclusiones", "Un silogismo válido mantiene la verdad de las premisas a la conclusión.<br><br><em>Ejemplo clásico:</em><br><ol class='list-decimal pl-5 space-y-2'><li>Todo animal es ser vivo. (Premisa 1)</li><li>El perro es un animal. (Premisa 2)</li><li><strong>Conclusión: El perro es un ser vivo.</strong></li></ol><br>El truco UdeA: te darán conclusiones incorrectas que <em>parecen</em> seguir de las premisas. Verifica la cadena de razonamiento paso a paso."),
            ("Tablas de Verdad Rápidas", "Para el examen, debes poder evaluar expresiones en segundos.<br><br><strong>Truco:</strong> El condicional (→) es el único conector que falla con un solo caso: <em>Premisa verdadera, conclusión falsa</em>. Aprende eso y tendrás el 80% de las preguntas de conectores resueltas."),
        ],
        "flashcards": [
            ("¿Cuándo es falso P → Q?", "Solo cuando P es <strong>Verdadera</strong> y Q es <strong>Falsa</strong>. En cualquier otro caso es verdadero."),
            ("¿Qué es el Modus Ponens?", "Si P → Q es verdadero, y P es verdadero, entonces Q debe ser verdadero. Es la inferencia más básica."),
            ("Negación de 'P y Q'", "No es 'no P y no Q'. La negación de una conjunción es: <strong>'¬P ∨ ¬Q'</strong> (Ley de De Morgan)."),
        ],
        "questions": [
            ("Si la afirmación 'Si llueve, el suelo está mojado' es verdadera, y el suelo NO está mojado, ¿qué podemos concluir?", [("a","No podemos sacar ninguna conclusión"),("b","Llovió de todas formas"),("c","No llovió")], "c", "Por el Modus Tollens: si P→Q es verdadero y Q es falso, entonces P debe ser falso."),
            ("¿Cuál es la negación correcta de 'Todos los estudiantes aprobaron'?", [("a","Ningún estudiante aprobó"),("b","Al menos un estudiante no aprobó"),("c","Casi todos aprobaron")], "b", "La negación de 'Todos X son Y' es 'Existe al menos un X que no es Y'.")
        ]
    },
    {
        "num": 4, "title": "Lectura Crítica I: Comprensión Profunda",
        "color": "purple", "icon": "fa-book-open", "subject": "LECTURA CRÍTICA",
        "tagline": "Identifica la tesis, los argumentos y la intención del autor en textos filosóficos y científicos.",
        "callout_title": "Niveles de Lectura que Evalúa la UdeA",
        "callout_body": "La UdeA evalúa tres niveles de comprensión: <strong>1) Literal</strong> (¿qué dice el texto?), <strong>2) Inferencial</strong> (¿qué implica?), y <strong>3) Analógico-crítico</strong> (¿con qué otra idea se relaciona?). La mayoría de preguntas son del nivel 2 y 3.",
        "callout_icon": "fa-magnifying-glass", "callout_color": "purple",
        "accordions": [
            ("Cómo Identificar la Tesis Central", "La tesis es la idea principal que el autor defiende. Para encontrarla:<br><ul class='list-disc pl-5 space-y-2'><li>Lee el primer y el último párrafo con máxima atención.</li><li>Busca la frase que el autor <em>repite o reformula</em> con diferentes palabras.</li><li>Pregúntate: ¿Qué está intentando demostrar el autor?</li><li>Las demás ideas son argumentos o ejemplos que <em>apoyan</em> esa tesis.</li></ul>"),
            ("Identificar Argumentos vs. Ejemplos", "Un argumento es una razón lógica que sostiene la tesis. Un ejemplo es solo una ilustración. En el examen UdeA, a menudo preguntan cuál de las siguientes opciones es un 'argumento que sustenta la posición del autor'. Identifica estructuras como: 'porque...', 'dado que...', 'puesto que...'."),
            ("Leer Entre Líneas: Inferencias", "Una inferencia es una conclusión que el texto permite sacar aunque no la diga explícitamente. <br><br><strong>Ejemplo:</strong> Si un texto dice 'El candidato no asistió a los debates', podríamos inferir que '<em>al candidato no le convenía debatir sus propuestas</em>'. Esta es una inferencia válida si el texto la sustenta."),
        ],
        "flashcards": [
            ("¿Cuál es la diferencia entre un tema y una tesis?", "El <strong>tema</strong> es el asunto que trata el texto. La <strong>tesis</strong> es la posición específica que el autor toma sobre ese tema."),
            ("'El autor implica que...'", "Una pregunta de este tipo busca una <strong>inferencia</strong>: algo que se deduce del texto pero que no está dicho explícitamente. Busca evidencia textual que la respalde."),
            ("Lectura Analógica", "Relaciona la idea del texto con otra situación similar. Pregunta tipo: '¿En qué otro contexto aplica la misma lógica del texto?'"),
        ],
        "questions": [
            ("En un texto donde el autor argumenta que 'la tecnología ha mejorado la productividad pero ha reducido la creatividad', ¿cuál es su tesis?", [("a","La tecnología es un invento moderno"),("b","La tecnología tiene efectos positivos y negativos en los seres humanos"),("c","La productividad es más importante que la creatividad")], "b", "La tesis resume la posición central. El autor reconoce dos efectos opuestos, lo que indica una postura balada y crítica."),
            ("Si un texto argumenta que 'la educación pública de calidad es la única forma real de reducir la desigualdad', ¿qué podemos inferir?", [("a","El autor es maestro de escuela"),("b","El autor considera que otros mecanismos como subsidios o empleos no son suficientes por sí solos"),("c","El autor quiere eliminar la educación privada")], "b", "La expresión 'única forma real' implica que el autor descarta o considera insuficientes las demás alternativas.")
        ]
    },
    {
        "num": 5, "title": "Lectura Crítica II: Vocabulario y Estructura",
        "color": "pink", "icon": "fa-language", "subject": "LECTURA CRÍTICA",
        "tagline": "Vocabulario contextual, tipos de texto y estructura argumentativa en el examen de admisión.",
        "callout_title": "El Vocabulario en el ICFES y la UdeA",
        "callout_body": "Nunca te pregunten el significado de una palabra de forma aislada. Siempre es en <strong>contexto</strong>. La pregunta es: ¿Qué quiso decir el autor con esta palabra en este párrafo específico? Aquí es donde el 70% de los estudiantes falla.",
        "callout_icon": "fa-spell-check", "callout_color": "pink",
        "accordions": [
            ("Cómo Resolver Vocabulario Contextual", "Estrategia de 3 pasos:<br><ol class='list-decimal pl-5 space-y-2'><li>Tacha la palabra en el texto y lee la oración sin ella.</li><li>Infiere un sinónimo o frase que encaje en ese contexto exacto.</li><li>Reemplaza cada opción de respuesta y lee la oración completa. La que mantenga el sentido del párrafo es la correcta.</li></ol>"),
            ("Tipos de Textos y Sus Intenciones", "Cada tipo de texto tiene una intención comunicativa:<br><ul class='list-disc pl-5 space-y-2'><li><strong>Expositivo:</strong> Informa o explica sin tomar partido.</li><li><strong>Argumentativo:</strong> Defiende una posición con razones.</li><li><strong>Narrativo:</strong> Cuenta eventos, puede tener intención literaria o didáctica.</li><li><strong>Descriptivo:</strong> Caracteriza detalladamente algo o alguien.</li></ul>La UdeA frecuentemente mezcla tipos en un solo texto."),
            ("Conectores Discursivos: Claves de Estructura", "Los conectores revelan la lógica interna del texto:<br><ul class='list-disc pl-5 space-y-2'><li><strong>Causales:</strong> 'porque', 'ya que', 'puesto que'.</li><li><strong>Adversativos:</strong> 'sin embargo', 'pero', 'no obstante'. (Señalan un giro en el argumento).</li><li><strong>Conclusivos:</strong> 'por lo tanto', 'en consecuencia', 'así pues'. (Aquí suele estar la tesis).</li></ul>"),
        ],
        "flashcards": [
            ("¿Qué busca la pregunta '¿A qué se refiere el autor con X?'", "A que identifiques el significado de X <strong>en ese contexto específico</strong>, no su definición del diccionario."),
            ("Un texto que empieza con 'Es falso que...'", "Es claramente <strong>argumentativo</strong>. El autor toma una posición en contra de una idea y probablemente presentará evidencia para refutarla."),
            ("'Sin embargo' en un párrafo", "Señala una <strong>concesión adversativa</strong>: el autor reconoce un punto válido del lado contrario, pero lo supera con un argumento más fuerte. Presta máxima atención a lo que viene DESPUÉS de 'sin embargo'."),
        ],
        "questions": [
            ("En el texto: 'La ciencia no es infalible, sin embargo, es el mejor sistema que hemos desarrollado para aproximarnos a la verdad.' La función del conector 'sin embargo' es:", [("a","Introducir una causa"),("b","Mostrar una contradicción que el autor resuelve a favor de la ciencia"),("c","Presentar una conclusión")], "b", "'Sin embargo' es un conector adversativo. El autor concede el punto negativo (no es infalible) pero lo contrapone con un argumento positivo más fuerte."),
            ("Si el autor usa la palabra 'voraz' para referirse al apetito del mercado global, en ese contexto significa:", [("a","Hambriento, insaciable en su consumo de recursos"),("b","Violento y agresivo físicamente"),("c","Lento y metódico")], "a", "Reemplaza 'voraz' por cada opción en la frase original. 'Un apetito insaciable del mercado global' mantiene perfectamente el sentido económico y crítico del texto.")
        ]
    },
    {
        "num": 6, "title": "Biología: Célula, Genética y Ecosistemas",
        "color": "green", "icon": "fa-dna", "subject": "BIOLOGÍA",
        "tagline": "Biología celular, herencia mendeliana y ecología enfocadas en las pruebas de Ciencias de la Salud.",
        "callout_title": "Biología para Aspirantes a Medicina",
        "callout_body": "Si aspiras a Medicina, Bacteriología o Enfermería, el componente de Biología de la UNAL es tu mayor aliado o tu mayor obstáculo. Los temas más frecuentes son: <strong>División celular (mitosis/meiosis), Expresión génica (transcripción/traducción) y Ecología de poblaciones.</strong>",
        "callout_icon": "fa-microscope", "callout_color": "green",
        "accordions": [
            ("La Célula: Mitosis vs. Meiosis", "Ambos son procesos de división celular, pero con propósitos opuestos:<br><ul class='list-disc pl-5 space-y-2'><li><strong>Mitosis:</strong> Crecimiento y reparación. Produce 2 células hijas IDÉNTICAS a la madre. Conserva el número cromosómico (2n → 2n).</li><li><strong>Meiosis:</strong> Reproducción sexual. Produce 4 células hijas con la MITAD de los cromosomas (2n → n). Genera variabilidad genética por entrecruzamiento.</li></ul><br><strong>Pregunta trampa UdeA:</strong> ¿Por qué los gemelos idénticos son clones? (Meiosis produce el óvulo fecundado, luego la mitosis duplica ese cigoto identicamente)."),
            ("Genética de Mendel: Las Leyes que Debes Dominar", "Mendel describió cómo se heredan los rasgos:<br><ul class='list-disc pl-5 space-y-2'><li><strong>Ley de Segregación:</strong> Cada individuo tiene dos alelos para cada gen; solo transmite uno a su descendencia (al azar).</li><li><strong>Ley de Distribución Independiente:</strong> Los genes de características diferentes se heredan de forma independiente.</li><li><strong>Cuadrado de Punnett:</strong> La herramienta esencial para calcular probabilidades de fenotipos en la descendencia. Practica cruces Aa × Aa y AaBb × AaBb.</li></ul>"),
            ("Ecología: Flujos y Niveles Tróficos", "La energía fluye en una sola dirección a través de la cadena alimentaria:<br><br><strong>Productor → Herbívoro → Carnívoro → Descomponedor</strong><br><br>Solo el <strong>10% de la energía</strong> se transfiere entre niveles. Esto explica por qué los carnívoros son menos abundantes que los productores. Las preguntas de ecología suelen preguntar qué ocurre con la cadena si un nivel poblacional colapsa."),
        ],
        "flashcards": [
            ("¿Qué es un fenotipo vs. un genotipo?", "El <strong>genotipo</strong> es la constitución genética (Aa, AA, aa). El <strong>fenotipo</strong> es la manifestación observable (color de ojos, altura). Un mismo fenotipo puede tener genotipos distintos (AA o Aa)."),
            ("Mutualismo vs. Parasitismo", "En el <strong>mutualismo</strong> ambas especies se benefician (abeja-flor). En el <strong>parasitismo</strong> una especie se beneficia a expensas de la otra (garrapata-perro)."),
            ("Organelo de la Respiración Celular", "La <strong>mitocondria</strong> es el organelo donde ocurre la respiración aeróbica y se produce la mayor parte del ATP. Por eso se llama 'la central energética de la célula'."),
        ],
        "questions": [
            ("Si dos individuos con genotipo Aa (pelo negro dominante sobre blanco recesivo) se cruzan, ¿qué proporción de descendencia tendrá pelo blanco?", [("a","0%"),("b","25%"),("c","50%")], "b", "El cruce Aa × Aa produce: AA (25%), Aa (50%), aa (25%). Solo el aa (homocigoto recesivo) expresa el rasgo blanco. Por eso 1 de cada 4 descendientes = 25%."),
            ("Una toxina destruye a todos los productores primarios de un ecosistema acuático. ¿Cuál es el efecto más inmediato?", [("a","Los descomponedores aumentan su población"),("b","Los herbívoros acuáticos pierden su fuente de alimento y su población colapsa"),("c","Los carnívoros toman el rol de productores")], "b", "Sin productores (algas, plantas acuáticas), los herbívoros no tienen qué comer. El colapso se propaga ascendiendo en la cadena trófica.")
        ]
    },
    {
        "num": 7, "title": "Química: Átomo, Enlace y Reacciones",
        "color": "orange", "icon": "fa-flask", "subject": "QUÍMICA",
        "tagline": "Estructura atómica, tabla periódica, tipos de enlace y estequiometría para el examen de admisión.",
        "callout_title": "Química en el ICFES: ¿Qué Entra?",
        "callout_body": "El ICFES Saber 11 no busca cálculos complejos. Evalúa si comprendes <strong>por qué</strong> ocurren las reacciones. La estequiometría (balanceo de ecuaciones y relaciones molares) representa hasta el 30% de las preguntas de ciencias.",
        "callout_icon": "fa-atom", "callout_color": "orange",
        "accordions": [
            ("Estructura del Átomo: Lo Que Todo Estudiante Debe Saber", "El átomo tiene tres partículas subatómicas:<ul class='list-disc pl-5 space-y-2 mt-2'><li><strong>Protones (+):</strong> En el núcleo. Su número define el elemento (número atómico Z).</li><li><strong>Neutrones (0):</strong> En el núcleo. Su número variable crea isótopos.</li><li><strong>Electrones (-):</strong> En orbitales alrededor del núcleo. Determinan las propiedades químicas y los enlaces.</li></ul><br><strong>Truco:</strong> En un átomo neutro, #protones = #electrones."),
            ("La Tabla Periódica Como Mapa de Propiedades", "La tabla periódica NO es solo una lista: es un mapa de propiedades:<ul class='list-disc pl-5 space-y-2 mt-2'><li><strong>De izquierda a derecha (período):</strong> Aumenta la electronegatividad, disminuye el radio atómico.</li><li><strong>De arriba a abajo (grupo):</strong> Aumenta el radio atómico, disminuye la electronegatividad.</li><li><strong>Gases nobles (col. 18):</strong> Extremadamente estables, no forman enlaces normalmente.</li></ul>"),
            ("Estequiometría: Balanceo de Ecuaciones", "Una ecuación química balanceada obedece la Ley de Conservación de la Masa (Lavoisier): los átomos no se crean ni destruyen.<br><br><strong>Estrategia para balancear:</strong><br><ol class='list-decimal pl-5 space-y-1 mt-2'><li>Escribe la ecuación sin balancear.</li><li>Cuenta los átomos de cada elemento en reactivos y productos.</li><li>Agrega coeficientes (sin cambiar subíndices) para igualar.</li><li>Verifica que ambos lados sean iguales.</li></ol>"),
        ],
        "flashcards": [
            ("¿Qué es un enlace covalente vs. iónico?", "En el <strong>enlace covalente</strong>, los átomos <em>comparten</em> electrones. En el <strong>enlace iónico</strong>, un átomo <em>transfiere</em> electrones al otro, creando iones con cargas opuestas que se atraen."),
            ("pH: Ácidos vs. Bases", "pH < 7 → ácido (más H⁺). pH > 7 → base (más OH⁻). pH = 7 → neutro (como el agua pura). El pH es una escala logarítmica, así que un pH de 3 es 10 veces más ácido que un pH de 4."),
            ("Ley de Conservación de la Masa", "La masa total de los reactivos siempre es igual a la masa total de los productos. Si 10g de A reacciona con 20g de B, los productos pesan 30g en total."),
        ],
        "questions": [
            ("En la ecuación sin balancear: Fe + O₂ → Fe₂O₃, ¿cuál es el coeficiente del O₂ en la ecuación balanceada?", [("a","1"),("b","3/2 (o 1.5)"),("c","2")], "b", "La ecuación balanceada es: 4Fe + 3O₂ → 2Fe₂O₃. El coeficiente del O₂ es 3. Si se pregunta en forma fraccionaria: 3/2 por mol de Fe₂O₃."),
            ("Un átomo de sodio (Na) tiene 11 protones y 11 electrones. Cuando forma el ion Na⁺, ¿cuántos electrones tiene?", [("a","12 electrones"),("b","10 electrones"),("c","11 electrones")], "b", "Al perder un electrón (carga +1), el Na pasa de 11 a 10 electrones. Los protones no cambian.")
        ]
    },
    {
        "num": 8, "title": "Física: Movimiento, Fuerza y Energía",
        "color": "cyan", "icon": "fa-rocket", "subject": "FÍSICA",
        "tagline": "Cinemática, las leyes de Newton y principios de energía para el examen ICFES y UNAL.",
        "callout_title": "Física Conceptual: El Enfoque del ICFES",
        "callout_body": "El ICFES rara vez pide cálculos puros. La mayoría de preguntas son de <strong>física conceptual</strong>: entiende las leyes y predice qué pasará en una situación dada. Dominar los conceptos te da una ventaja enorme sobre quienes solo memorizaron fórmulas.",
        "callout_icon": "fa-bolt", "callout_color": "cyan",
        "accordions": [
            ("Cinemática: Describiendo el Movimiento", "La cinemática estudia CÓMO se mueven los objetos (sin preguntar por qué).<ul class='list-disc pl-5 space-y-2 mt-2'><li><strong>Velocidad:</strong> \\(v = \\frac{\\Delta x}{\\Delta t}\\) — Desplazamiento por unidad de tiempo.</li><li><strong>Aceleración:</strong> \\(a = \\frac{\\Delta v}{\\Delta t}\\) — Cambio de velocidad por unidad de tiempo.</li><li><strong>Movimiento Uniforme (MU):</strong> Velocidad constante, aceleración = 0.</li><li><strong>Movimiento Uniformemente Acelerado (MUA):</strong> Aceleración constante (como la caída libre, \\(g ≈ 9.8 m/s^2\\)).</li></ul>"),
            ("Las 3 Leyes de Newton: El Core de la Física", "<ol class='list-decimal pl-5 space-y-2 mt-2'><li><strong>Ley de Inercia:</strong> Un objeto en reposo permanece en reposo y uno en movimiento permanece en movimiento a menos que una fuerza neta actúe sobre él.</li><li><strong>F = ma:</strong> La fuerza neta sobre un objeto es igual a su masa por su aceleración. \\(F = ma\\)</li><li><strong>Acción y Reacción:</strong> Por cada fuerza de acción, existe una fuerza de reacción igual en magnitud y opuesta en dirección.</li></ol>"),
            ("Energía y sus Transformaciones", "La Energía se conserva (No se crea ni se destruye, solo se transforma):<ul class='list-disc pl-5 space-y-2 mt-2'><li><strong>E. Cinética:</strong> \\(Ec = \\frac{1}{2}mv^2\\) — Energía del movimiento.</li><li><strong>E. Potencial Gravitacional:</strong> \\(Ep = mgh\\) — Energía almacenada por la altura.</li><li><strong>Principio de Conservación:</strong> Al caer desde una altura, la Ep se convierte en Ec. La suma total es siempre la misma (si ignoramos el aire).</li></ul>"),
        ],
        "flashcards": [
            ("¿Por qué la masa no cambia pero el peso sí?", "La <strong>masa</strong> es la cantidad de materia (constante). El <strong>peso</strong> es la fuerza gravitacional sobre esa masa (\\(P = mg\\)). En la Luna, g es menor, así que el peso es menor, pero la masa es la misma."),
            ("¿Qué sucede con la energía cinética si duplicas la velocidad?", "\\(Ec = \\frac{1}{2}mv^2\\). Si v se duplica, la energía cinética se <strong>cuadruplica</strong>. Por eso los accidentes a alta velocidad son exponencialmente más dañinos."),
            ("Movimiento Uniforme vs. MUA (gráficas)", "En un gráfico velocidad-tiempo: MU es una <strong>línea horizontal</strong> (velocidad constante). MUA es una <strong>línea diagonal</strong> (velocidad cambia linealmente con el tiempo)."),
        ],
        "questions": [
            ("Un objeto de 5 kg cae en caída libre. ¿Cuánto vale la fuerza neta sobre el objeto? (g = 10 m/s²)", [("a","0 N (la gravedad y la normal se cancelan)"),("b","50 N hacia abajo"),("c","5 N")], "b", "En caída libre no hay fuerza normal (no hay superficie de apoyo). Fuerza neta = F_gravedad = m × g = 5 kg × 10 m/s² = 50 N."),
            ("Un automóvil viaja a velocidad constante en una carretera. Según la Primera Ley de Newton, ¿qué se puede afirmar?", [("a","La fuerza del motor es cero"),("b","La fuerza neta sobre el auto es cero (el motor iguala la fricción y el aire)"),("c","Hay una aceleración positiva constante")], "b", "Velocidad constante implica aceleración cero. Por la 1era Ley, aceleración cero = Fuerza neta cero. El motor NO aplica fuerza neta; la fuerza del motor compensa exactamente las fuerzas de fricción.")
        ]
    },
    {
        "num": 9, "title": "Matemática Avanzada: Álgebra y Funciones",
        "color": "amber", "icon": "fa-square-root-variable", "subject": "MATEMÁTICAS",
        "tagline": "Ecuaciones, factorización, funciones lineales y cuadráticas para lograr el puntaje máximo.",
        "callout_title": "El 'Techo de Puntos' en Matemáticas",
        "callout_body": "Los estudiantes que dominan Álgebra y Funciones pueden resolver el 35–40% del componente de Lógica Matemática de la UdeA. Este módulo es la diferencia entre un puntaje competitivo y un puntaje de élite.",
        "callout_icon": "fa-chart-line", "callout_color": "amber",
        "accordions": [
            ("Factorización: El Arte de Simplificar", "Factorizar es expresar una expresión algebraica como producto de factores más simples. Tipos clave:<ul class='list-disc pl-5 space-y-2 mt-2'><li><strong>Factor común:</strong> \\(ax + ay = a(x+y)\\)</li><li><strong>Diferencia de cuadrados:</strong> \\(a^2 - b^2 = (a+b)(a-b)\\)</li><li><strong>Trinomio cuadrado perfecto:</strong> \\(a^2 + 2ab + b^2 = (a+b)^2\\)</li><li><strong>Trinomio general:</strong> \\(x^2 + bx + c = (x+r)(x+s)\\) donde \\(r+s=b\\) y \\(r \\cdot s = c\\)</li></ul>"),
            ("Funciones Lineales y Cuadráticas", "<strong>Función Lineal:</strong> \\(f(x) = mx + b\\)<ul class='list-disc pl-5 mt-2'><li>m = pendiente (inclinación de la recta)</li><li>b = intercepto en y (donde corta el eje Y)</li></ul><br><strong>Función Cuadrática (Parábola):</strong> \\(f(x) = ax^2 + bx + c\\)<ul class='list-disc pl-5 mt-2'><li>Si a > 0: abre hacia arriba (mínimo)</li><li>Si a < 0: abre hacia abajo (máximo)</li><li>Raíces: \\( x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\\)</li></ul>"),
            ("Sistemas de Ecuaciones: Método de Sustitución", "El método más limpio para el examen:<br><ol class='list-decimal pl-5 space-y-1 mt-2'><li>Despeja una variable en la ecuación más simple.</li><li>Sustituye esa expresión en la otra ecuación.</li><li>Resuelve la ecuación de una sola variable.</li><li>Reemplaza para encontrar la otra variable.</li></ol><br><em>Consejo:</em> Verifica siempre tu respuesta reemplazando en ambas ecuaciones originales."),
        ],
        "flashcards": [
            ("Fórmula cuadrática y discriminante", "El discriminante es \\(\\Delta = b^2 - 4ac\\). Si \\(\\Delta > 0\\): dos raíces reales. Si \\(\\Delta = 0\\): una raíz real. Si \\(\\Delta < 0\\): sin raíces reales."),
            ("Dominio de una función", "El <strong>dominio</strong> es el conjunto de todos los valores de x para los que la función está definida. Cuidado: no puedes dividir por cero ni tomar raíz cuadrada de un número negativo."),
            ("Diferencia de cuadrados rápida", "\\(x^2 - 25 = (x+5)(x-5)\\). El patrón \\(a^2 - b^2\\) siempre factoriza. Aprenderlo de memoria te ahorra 45 segundos por pregunta."),
        ],
        "questions": [
            ("¿Cuántas soluciones reales tiene la ecuación \\(x^2 - 6x + 9 = 0\\)?", [("a","Dos soluciones distintas"),("b","Una solución (doble)"),("c","Ninguna solución real")], "b", "El discriminante es \\(\\Delta = (-6)^2 - 4(1)(9) = 36 - 36 = 0\\). Discriminante = 0 significa una raíz real doble: x = 3."),
            ("La función \\(f(x) = 2x + 5\\). ¿Cuál es el valor de \\(f(3)\\)?", [("a","10"),("b","11"),("c","8")], "b", "\\(f(3) = 2(3) + 5 = 6 + 5 = 11\\). La evaluación de funciones es mecánica: reemplaza x por el valor dado.")
        ]
    },
    {
        "num": 10, "title": "Simulacro Final Integrador y Plan de Cierre",
        "color": "rose", "icon": "fa-flag-checkered", "subject": "SIMULACRO FINAL",
        "tagline": "Examen integrador de 20 preguntas tipo UdeA. Mide tu estado de preparación real antes del día del examen.",
        "callout_title": "Protocolo Pre-Examen (Últimas 72 horas)",
        "callout_body": "No estudies materia nueva en los últimos 3 días. Usa el tiempo para: 1) Repasar tarjetas de vocabulario y fórmulas clave. 2) Dormir 8 horas mínimo cada noche. 3) Hacer el simulacro a la misma hora que el examen real. 4) <strong>Confiar en el trabajo hecho.</strong>",
        "callout_icon": "fa-brain", "callout_color": "rose",
        "accordions": [
            ("Estrategia de 3 Pases: Protocolo del Día del Examen", "<strong>Pase 1 (40 min):</strong> Lee y responde SOLO las preguntas que sabes con seguridad (Verdes). Marca las dudosas y pasa.<br><br><strong>Pase 2 (60 min):</strong> Regresa a las preguntas Amarillas (complejas pero resolubles). Aplica eliminación de opciones.<br><br><strong>Pase 3 (20 min):</strong> Las Rojas. Si no sabes, nunca dejes en blanco: elimina 2 opciones y elige entre las 2 restantes. La probabilidad sube del 25% al 50%."),
            ("Manejo de la Ansiedad: Técnica 4-7-8", "Si durante el examen sientes que la ansiedad te bloquea:<ol class='list-decimal pl-5 space-y-1 mt-2'><li>Inhala por la nariz durante <strong>4 segundos</strong>.</li><li>Sostén el aire durante <strong>7 segundos</strong>.</li><li>Exhala por la boca durante <strong>8 segundos</strong>.</li></ol>Hazlo 2-3 veces. Activa el sistema nervioso parasimpático y reduce el cortisol en menos de 90 segundos."),
            ("Revisión de Conceptos Clave del Curso", "Antes de hacer el simulacro, repasa estas ideas en 5 minutos:<ul class='list-disc pl-5 space-y-2 mt-2'><li>Estrategia: Triage (Verde/Amarillo/Rojo) y 2.25 min por pregunta.</li><li>Lógica: El condicional (→) falla solo cuando P=V y Q=F.</li><li>Lectura: Busca la tesis en el primer y último párrafo.</li><li>Biología: Mitosis (2n→2n), Meiosis (2n→n).</li><li>Química: Balancear conservando masa y átomos.</li><li>Física: F=ma, Ec = ½mv².</li></ul>"),
        ],
        "flashcards": [
            ("El día del examen: ¿qué llevar?", "Documento de identidad original, lápiz o lapicero negro, borrador y mucha confianza. Llega 30 minutos antes del horario señalado."),
            ("Si terminas antes de tiempo...", "No entregues inmediatamente. Usa el tiempo restante para revisar el Pase 2 y 3. Un error de lectura rápida puede costarte una pregunta que sabías."),
            ("¿Vale la pena adivinar?", "En la UdeA <strong>NO hay puntos negativos</strong>. Nunca dejes preguntas en blanco. Siempre responde, aunque sea de forma educada entre 2 opciones eliminando las 2 más absurdas."),
        ],
        "questions": [
            ("Un estudiante entra al examen y ve una pregunta de química que no tiene idea de cómo resolver. Según el Método de Triage, ¿qué debe hacer?", [("a","Intentar resolverla con todo su tiempo para no perder los puntos"),("b","Marcarla como Roja, pasarla y volver al final si le sobra tiempo"),("c","Adivinar inmediatamente y borrar del cuadernillo")], "b", "El Triage dice: Las Rojas se pasan inmediatamente. Dedicar mucho tiempo a una pregunta que no sabes va en detrimento de las preguntas que sí puedes resolver correctamente."),
            ("En un examen de 80 preguntas en 3 horas (180 minutos), ¿cuánto tiempo tiene disponible en promedio por pregunta?", [("a","2 minutos y 45 segundos"),("b","2 minutos y 15 segundos"),("c","1 minuto y 30 segundos")], "b", "180 minutos ÷ 80 preguntas = 2.25 minutos = 2 minutos y 15 segundos por pregunta. Este número debe estar grabado en tu mente el día del examen.")
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
    
    fc_html = '<div class="grid grid-cols-1 sm:grid-cols-3 gap-6 h-44">'
    for (front, back) in m["flashcards"]:
        fc_html += f"""
                <div class="flashcard h-full">
                    <div class="fc-inner">
                        <div class="fc-front shadow-sm"><h4 class="font-bold text-base">{front}</h4></div>
                        <div class="fc-back shadow-lg"><p class="text-sm font-medium">{back}</p></div>
                    </div>
                </div>"""
    fc_html += "</div>"
    
    q_html = '<div id="quiz-container" class="space-y-8">'
    for qi, (qtext, options, correct, explanation) in enumerate(m["questions"]):
        q_html += f'<div class="q-item" data-correct="{correct}"><p class="font-semibold text-gray-800 mb-4">{qi+1}. {qtext}</p><div class="space-y-3">'
        for (val, lbl) in options:
            q_html += f'<label class="flex items-center p-4 border border-gray-200 rounded-xl cursor-pointer hover:bg-white transition-colors group"><input type="radio" name="q{qi+1}" value="{val}" class="w-4 h-4 text-emerald-600 border-gray-300"><span class="ml-3 text-sm text-gray-700">{lbl}</span></label>'
        q_html += f'<div class="q-feedback hidden mt-3 p-4 rounded-xl text-sm font-medium"></div></div></div>'
    q_html += '<button id="submit-quiz" class="flex items-center justify-center gap-2 w-full sm:w-auto px-8 py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl shadow-md transition-all"><i class="fa-solid fa-spell-check"></i> Verificar Respuestas</button></div>'

    callout_color_map = {
        "indigo": ("bg-indigo-50", "border-indigo-500", "text-indigo-500", "text-indigo-900", "text-indigo-800"),
        "purple": ("bg-purple-50", "border-purple-500", "text-purple-500", "text-purple-900", "text-purple-800"),
        "pink": ("bg-pink-50", "border-pink-500", "text-pink-500", "text-pink-900", "text-pink-800"),
        "green": ("bg-green-50", "border-green-500", "text-green-500", "text-green-900", "text-green-800"),
        "orange": ("bg-orange-50", "border-orange-500", "text-orange-500", "text-orange-900", "text-orange-800"),
        "cyan": ("bg-cyan-50", "border-cyan-500", "text-cyan-500", "text-cyan-900", "text-cyan-800"),
        "amber": ("bg-amber-50", "border-amber-500", "text-amber-500", "text-amber-900", "text-amber-800"),
        "rose": ("bg-rose-50", "border-rose-500", "text-rose-500", "text-rose-900", "text-rose-800"),
    }
    cc = callout_color_map.get(color, callout_color_map["green"])

    content = HEAD.format(num=num, title=m["title"]) + f"""
    <header class="mb-10 text-center">
        <span class="inline-block py-1 px-3 bg-emerald-100 text-emerald-700 text-xs font-bold uppercase tracking-widest rounded-md mb-4 border border-emerald-200">Módulo {num}</span>
        <h1 class="text-3xl md:text-4xl font-extrabold text-gray-900 mb-4 tracking-tight">{m["title"]}</h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto">{m["tagline"]}</p>
    </header>

    <section class="mb-12 max-w-4xl mx-auto">
        <div class="{cc[0]} border-l-4 {cc[1]} p-6 rounded-r-2xl shadow-sm">
            <div class="flex items-start gap-4">
                <div class="{cc[2]} text-2xl mt-1"><i class="fa-solid {m['callout_icon']}"></i></div>
                <div><h3 class="text-lg font-bold {cc[3]} mb-2">{m['callout_title']}</h3><p class="{cc[4]} text-sm leading-relaxed">{m['callout_body']}</p></div>
            </div>
        </div>
    </section>

    <section class="mb-12 max-w-4xl mx-auto">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3">
            <i class="fa-solid {m['icon']} text-emerald-500"></i> Conceptos Clave
        </h2>
        <div class="space-y-4">{acc_html}</div>
    </section>

    <section class="mb-16 max-w-4xl mx-auto">
        <h2 class="text-2xl font-bold text-gray-900 mb-2 flex items-center gap-3"><i class="fa-solid fa-layer-group text-emerald-500"></i> Repaso Rápido</h2>
        <p class="text-sm text-gray-500 mb-6">Pasa el cursor (o toca) las tarjetas para ver la respuesta.</p>
        {fc_html}
    </section>

    <section class="max-w-4xl mx-auto bg-gray-50 border border-gray-200 rounded-3xl p-6 sm:p-10 shadow-sm relative overflow-hidden">
        <div class="absolute top-0 left-0 w-2 h-full bg-emerald-500"></div>
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Comprobación de Lectura</h2>
        {q_html}
    </section>
""" + FOOT.format(num_padded=num_padded)
    return content

os.makedirs(BASE, exist_ok=True)
for m in MODULES:
    path = os.path.join(BASE, f"modulo-{m['num']:02d}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(gen_module(m))
    print(f"[OK] Generated {path}")

print("\nAll modules generated successfully!")
