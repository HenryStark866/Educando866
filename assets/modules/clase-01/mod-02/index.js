// taller-modulo-2.js - Gestión del Tiempo y Control de Ansiedad
// Professional implementation with original, exam-relevant questions
import { saveWorkshopResults } from "./workshop-storage.js";

document.addEventListener('DOMContentLoaded', () => {
    const studentModal = document.getElementById('student-modal');
    const startForm = document.getElementById('start-exam-form');
    const nameInput = document.getElementById('student-name');
    const emailInput = document.getElementById('student-email');
    
    const container = document.getElementById('questions-container');
    const submitPanel = document.getElementById('submit-panel');
    const finishBtn = document.getElementById('finish-module-btn');
    const timerDisplay = document.getElementById('countdown-timer');
    const progressBar = document.getElementById('progress-bar');
    const progressContainer = document.getElementById('progress-bar-container');
    
    const unansweredWarning = document.getElementById('unanswered-warning');
    const unansweredCount = document.getElementById('unanswered-count');

    let examTimer;
    let secondsLeft = 30 * 60; // 30 minutes
    let userAnswers = new Array(20).fill(null);

    // Banco de Preguntas (20) - Gestión del Tiempo y Control de Ansiedad
    // Original questions based on actual exam patterns and time management principles
    const questions = [
        {
            q: "En un examen de admisión con 120 preguntas y 210 minutos de duración, ¿cuál es el tiempo máximo recomendado para dedicar a cada pregunta si se desea reservar 20 minutos para revisión final?",
            options: [
                "A) 1 minuto 35 segundos",
                "B) 1 minuto 40 segundos", 
                "C) 1 minuto 45 segundos",
                "D) 1 minuto 50 segundos"
            ], correct: 2
        },
        {
            q: "Durante un examen de admisión, un estudiante experimenta bloqueo cognitivo en una pregunta de razonamiento lógico. ¿Qué estrategia tiene mayor respaldo en psicología educativa para recuperar el flujo de pensamiento sin perder tiempo significativo?",
            options: [
                "A) Pasar inmediatamente a la siguiente pregunta y marcar la difícil para revisión final",
                "B) Gastar exactamente 90 segundos más intentando resolverla antes de continuar",
                "C) Realizar una técnica de respiración de 30 segundos y luego regresar a la pregunta",
                "D) Adivinar aleatoriamente y continuar con el examen"
            ], correct: 0
        },
        {
            q: "Un estudiante tiene 45 minutos restantes y 25 preguntas por responder. Ha identificado que 10 preguntas son de alto valor (peso 2), 10 son de valor medio (peso 1.5) y 5 son de bajo valor (peso 1). ¿Qué estrategia de asignación de tiempo maximiza su puntaje ponderado esperado?",
            options: [
                "A) Asignar tiempo proporcional al peso de cada pregunta (más tiempo a preguntas de alto valor)",
                "B) Responder todas las preguntas en orden secuencial gastando el mismo tiempo en cada una",
                "C) Priorizar responder primero todas las preguntas de bajo valor para asegurar puntos fáciles",
                "D) Asignar tiempo igual a todas las preguntas independientemente de su valor"
            ], correct: 0
        },
        {
            q: "En un examen tipo prueba de estado, si un estudiante nota que consistentemente se queda sin tiempo en la sección de interpretación de gráficas, ¿qué ajuste metacognitivo tiene mayor evidencia empírica para mejorar su rendimiento?",
            options: [
                "A) Practicar exclusivamente ejercicios de gráficas hasta dominarlos completamente",
                "B) Desarrollar una rutina de 20 segundos para analizar ejes, unidades y tendencias antes de interpretar cualquier gráfica",
                "C) Aumentar significativamente la velocidad de lectura de enunciados en otras secciones",
                "D) Saltarse todas las preguntas que involucren gráficas y enfocarse en otras áreas"
            ], correct: 1
        },
        {
            q: "Un estudiante presenta ansiedad anticipatoria antes de los exámenes que afecta su rendimiento inicial. Según investigación en regulación emocional aplicada a contextos académicos, ¿qué intervención previa al examen tiene mayor eficacia demostrada?",
            options: [
                "A) Evitar cualquier tipo de estudio o repasos el día antes del examen",
                "B) Realizar una sesión de visualización positiva de 10 minutos imagining successful exam performance",
                "C) Consumir una bebida energética alta en cafeína inmediatamente antes de comenzar",
                "D) Estudiar intensamente durante las 2 horas previas al examen para llegar "calentado""
            ], correct: 1
        },
        {
            q: "Durante un examen de admisión, un estudiante nota que gasta más tiempo del esperado en preguntas de conocimiento factual que requieren recordación. ¿Qué técnica de estudio previa al examen tiene mayor respaldo para mejorar la eficiencia en este tipo específico de preguntas?",
            options: [
                "A) Estudiar usando únicamente resaltado y subrayado de textos",
                "B) Utilizar la técnica de práctica espaciada con recordación activa (flashcards, autoevaluación)",
                "C) Leer los mismos materiales múltiples veces en sesiones masivas",
                "D) Enfocarse exclusivamente en crear mapas conceptuales elaborados"
            ], correct: 1
        },
        {
            q: "En un examen con penalización por respuestas incorrectas (-0.5 puntos por error, +1 punto por acierto), un estudiante puede eliminar claramente 3 de 5 opciones en una pregunta. ¿Cuál es la decisión óptima desde la perspectiva de la teoría de decisiones?",
            options: [
                "A) Nunca responder la pregunta ya que el valor esperado es negativo",
                "B) Adivinar entre las 2 opciones restantes ya que el valor esperado es positivo (+0.5 puntos)",
                "C) Adivinar entre las 2 opciones restantes ya que el valor esperado es positivo (+0.25 puntos)",
                "D) Siempre dejar en blanco cuando queden más de 2 opciones después de eliminación"
            ], correct: 2
        },
        {
            q: "Un estudiante identifica que su principal error en exámenes es cambiar respuestas correctas por incorrectas durante la revisión. ¿Qué estrategia de revisión tiene mayor evidencia para reducir específicamente este patrón de error?",
            options: [
                "A) Nunca realizar ninguna revisión de respuestas durante el examen",
                "B) Limitar la revisión únicamente a preguntas donde inicialmente tuvo dudas marcadas",
                "C) Cambiar siempre la primera respuesta que genere cualquier duda durante la revisión",
                "D) Realizar revisiones múltiples pasando por el examen 2-3 veces completas"
            ], correct: 1
        },
        {
            q: "Durante la semana previa a un examen de admisión, un estudiante planea su práctica. Según principios de aprendizaje efectivo para retención a largo plazo, ¿qué enfoque de distribución de tiempo tiene mayor eficacia?",
            options: [
                "A) Concentrar el 80% de las horas de práctica en los últimos 2 días antes del examen",
                "B) Distribuir el tiempo de práctica de manera uniforme a lo largo de toda la semana de preparación",
                "C) Practicar intensamente durante la mañana y descansar completamente por las tardes",
                "D) Variar el contenido de práctica diariamente enfocándose en un solo tema cada día"
            ], correct: 1
        },
        {
            q: "En un examen de admisión, un estudiante nota que tiende a interpretar incorrectamente lo que las preguntas piden realmente (error de comprensión de enunciado). ¿Qué técnica de enfoque previo tiene mayor eficacia para reducir este tipo específico de error?",
            options: [
                "A) Leer rápidamente todo el examen antes de comenzar a responder cualquier pregunta",
                "B) Subrayar o resaltar mentalmente las palabras de acción clave (calcular, determinar, comparar, explicar, describir)",
                "C) Responder basado en la primera impresión del enunciado sin leerlo completamente",
                "D) Adivinar la respuesta antes de leer completamente las opciones disponibles"
            ], correct: 1
        },
        {
            q: "Un estudiante presenta fatiga mental significativa después de 90 minutos de examen continuo. Según investigación en cronobiología aplicada al rendimiento académico, ¿qué intervención preventiva tiene mayor respaldo para mantener el rendimiento cognitivo?",
            options: [
                "A) Consumir carbohidratos de absorción rápida (gaseosas, dulces) cada 30 minutos durante el examen",
                "B) Realizar micro-pausas activas de 45 segundos cada 25 minutos (estiramiento, movimiento ocular, respiración profunda)",
                "C) Aumentar significativamente la ingesta de cafeína a lo largo del examen",
                "D) Reducir el consumo de líquidos para evitar interrupciones por necesidad de usar servicios"
            ], correct: 1
        },
        {
            q: "Durante un examen de admisión, un estudiante experimenta que sus pensamientos divagan y pierde el enfoque en varias ocasiones. ¿Qué técnica de autorregulación atencional tiene mayor evidencia para mejorar el mantenimiento de concentración en contextos de evaluación prolongada?",
            options: [
                "A) Castigarse mentalmente cada vez que nota que su mente divaga",
                "B) Practicar la técnica de 'atención plena' suave: notar la distracción y retornar gentilmente el foco sin juicios",
                "C) Forzarse a aumentar significativamente la velocidad de respuesta para 'ponerse al día'",
                "D) Ignorar completamente las distracciones y tratar de bloquearlas mediante fuerza de voluntad pura"
            ], correct: 1
        },
        {
            q: "En un examen tipo prueba de aptitud, si un estudiante tiene que resolver 20 problemas de razonamiento cuantitativo en 40 minutos y nota que los primeros 5 problemas le tomaron 18 minutos, ¿qué ajuste estratégico es más apropiado para los 15 problemas restantes?",
            options: [
                "A) Mantener el mismo ritmo y esperar mejorar naturalmente en los problemas restantes",
                "B) Reducir el tiempo promedio por problema de 2 minutos a 1 minuto 20 segundos para los problemas restantes",
                "C) Adivinar en todos los problemas restantes ya que es imposible recuperar el tiempo perdido",
                "D) Gastar exactamente el mismo tiempo en cada uno de los problemas restantes sin importar su dificultad"
            ], correct: 1
        },
        {
            q: "Un estudiante identifica que comete errores por 'carga perceptual' cuando las preguntas presentan información visual excesiva o mal organizada. Según principios de diseño instruccional, ¿qué estrategia de enfoque tiene mayor eficacia para este tipo específico de error?",
            options: [
                "A) Ignorar completamente cualquier elemento visual y enfocarse únicamente en el texto",
                "B) Desarrollar una rutina de exploración visual sistemática: identificar primero qué es relevante y qué es decorativo o distraccion",
                "C) Aumentar el esfuerzo de procesamiento visual para intentar absorber toda la información presentada",
                "D) Adivinar basado en patrones de respuestas en preguntas similares vistas previamente"
            ], correct: 1
        },
        {
            q: "Durante un examen de admisión con formato de libro abierto, un estudiante nota que gasta demasiado tiempo buscando información en los materiales permitidos. ¿Qué habilidad de alfabetización informacional tiene mayor impacto en reducir efectivamente el tiempo de búsqueda?",
            options: [
                "A) Memorizar exactamente la ubicación de cada pieza de información en los materiales permitidos",
                "B) Desarrollar habilidad para usar eficientemente índices, tablas de contenido y palabras clave de búsqueda",
                "C) Traer la cantidad máxima posible de materiales de consulta para tener más opciones disponibles",
                "D) Evitar completamente el uso de materiales de consulta y depender únicamente de la memoria"
            ], correct: 1
        },
        {
            q: "Un estudiante presenta patrón de respuestas donde comienza el examen con alto rendimiento pero su precisión disminuye significativamente después de la primera hora. Según investigación en fatiga cognitiva, ¿qué intervención tiene mayor respaldo para mantener un rendimiento más estable a lo largo del tiempo?",
            options: [
                "A) Iniciar el examen con un ritmo muy lento para conservar energía mental",
                "B) Implementar un patrón de trabajo-resto: 50 minutos de enfoque intenso seguido de 5 minutos de recuperación activa",
                "C) Aumentar progresivamente la velocidad de respuesta a lo largo del examen para compensar la fatiga",
                "D) Concentrarse únicamente en responder correctamente las primeras dos terceras partes del examen"
            ], correct: 1
        },
        {
            q: "En un examen de admisión, un estudiante nota que frecuentemente subestima la dificultad de preguntas que parecen simples a primera vista. ¿Qué ajuste metacognitivo tiene mayor evidencia para mejorar la precision en este tipo específico de error de juicio?",
            options: [
                "A) Asignar un tiempo adicional fijo del 100% a todas las preguntas que inicialmente parezcan fáciles",
                "B) Aplicar una regla de escépticismo inicial: asumir que toda pregunta podría tener complejidad oculta hasta demostrar lo contrario",
                "C) Saltarse todas las preguntas que inicialmente parezcan muy fáciles y enfocarse en las desafiantes",
                "D) Confiar siempre en la primera impresión de dificultad y no ajustar el juicio inicial"
            ], correct: 1
        },
        {
            q: "Durante un examen de admisión, un estudiante experimenta síntomas físicos de estrés (tensión muscular, respiración superficial). ¿Qué técnica de regulación fisiológica tiene mayor evidencia para reducir rápidamente estos síntomas sin afectar negativamente el rendimiento cognitivo?",
            options: [
                "A) Ignorar completamente los síntomas físicos y enfocarse únicamente en la tarea cognitiva",
                "B) Realizar una técnica de respiración profunda diafragmática: 4 segundos inhalando, 6 segundos exhalando, por 60 segundos",
                "C) Tensar y relajar progresivamente todos los grupos musculares principales durante 90 segundos",
                "D) Ingerir un analgésico de venta libre para abordar los síntomas físicos"
            ], correct: 1
        },
        {
            q: "Un estudiante tiene que decidir entre dos estrategias para preguntas de alto valor que le toman mucho tiempo: Strategy A (dedicar tiempo ilimitado hasta resolverlas) y Strategy B (dedicar tiempo máximo fijo y pasar a siguiente). Según teoría de optimización de tiempo en exámenes, ¿cuándo Strategy B es superior a Strategy A?",
            options: [
                "A) Nunca, ya que Strategy A siempre garantiza resolver correctamente las preguntas de alto valor",
                "B) Siempre, ya que Strategy B previene el costo de oportunidad excesivo en otras preguntas",
                "C) Cuando el valor esperado de las preguntas que se dejarian sin responder es menor que el valor ganado por asegurar resolución de preguntas de alto valor",
                "D) Cuando el valor esperado de las preguntas que se dejarian sin responder es mayor que el valor adicional ganado por asegurar resolución de preguntas de alto valor"
            ], correct: 3
        },
        {
            q: "En un examen de admisión, un estudiante nota que su rendimiento varía significativamente dependiendo del orden en que aparecen los temas (efecto de posición en el cuadernillo). ¿Qué estrategia tiene mayor evidencia para mitigar específicamente este efecto de posición?",
            options: [
                "A) Siempre comenzar el examen desde la última pregunta y avanzar hacia atrás",
                "B) Ignorar completamente el orden de presentación y responder según dificultad personal percibida",
                "C) Implementar un patrón de respuesta que alterne entre secciones tempranas y tardías del cuadernillo",
                "D) Asignar tiempo de preparación extra específicamente para practicar con el orden exacto del cuadernillo oficial"
            ], correct: 2
        }
    ];

    const correctAnswersArray = questions.map(q => q.correct);

    // Initialization
    function init() {
        // Auto-fill if returning user
        if (localStorage.getItem('vetprep_student_name')) {
            nameInput.value = localStorage.getItem('vetprep_student_name');
            emailInput.value = localStorage.getItem('vetprep_student_email');
        }
    }

    startForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Save user state
        localStorage.setItem('vetprep_student_name', nameInput.value.trim());
        localStorage.setItem('vetprep_student_email', emailInput.value.trim());
        
        // Hide modal, show UI
        studentModal.classList.add('hidden');
        container.classList.remove('hidden');
        submitPanel.classList.remove('hidden');
        progressContainer.classList.remove('hidden');

        renderQuestions();
        startTimer();
    });

    function startTimer() {
        examTimer = setInterval(() => {
            secondsLeft--;
            if(secondsLeft <= 0) {
                clearInterval(examTimer);
                autoSubmitExam();
            }
            updateTimerDisplay();
        }, 1000);
    }

    function updateTimerDisplay() {
        const h = Math.floor(secondsLeft / 3600);
        const m = Math.floor((secondsLeft % 3600) / 60);
        const s = secondsLeft % 60;
        timerDisplay.textContent = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
        
        if (secondsLeft < 300) { // Less than 5 minutes
            timerDisplay.classList.add('text-red-500', 'animate-pulse');
        }
    }

    function updateProgress() {
        const answeredCount = userAnswers.filter(a => a !== null).length;
        const progressPercent = (answeredCount / 20) * 100;
        progressBar.style.width = `${progressPercent}%`;

        const missing = 20 - answeredCount;
        if (missing > 0) {
            unansweredWarning.classList.remove('hidden');
            unansweredCount.textContent = missing;
        } else {
            unansweredWarning.classList.add('hidden');
        }
    }

    function renderQuestions() {
        questions.forEach((qObj, index) => {
            const num = index + 1;
            const qDiv = document.createElement('div');
            qDiv.className = 'bg-white rounded-2xl p-6 md:p-8 shadow-sm border border-gray-200 question-card';
            
            let optionsHTML = '';
            qObj.options.forEach((opt, optIndex) => {
                optionsHTML += `
                    <label class="relative flex items-start p-4 cursor-pointer rounded-xl border border-gray-100 hover:bg-gray-50 transition-colors group">
                        <input type="radio" name="q${index}" value="${optIndex}" class="peer sr-only option-radio">
                        <div class="w-full flex items-center gap-4 transition-all pb-1">
                            <div class="indicator w-6 h-6 rounded-full border-2 border-gray-300 flex-shrink-0 flex items-center justify-center font-bold text-xs text-transparent transition-all">✓</div>
                            <span class="text-gray-700 font-medium group-hover:text-gray-900">${opt}</span>
                        </div>
                    </label>
                `);
            });

            qDiv.innerHTML = `
                <div class="flex items-start gap-4 mb-6">
                    <div class="w-10 h-10 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold flex-shrink-0 text-sm border-2 border-emerald-200">
                        ${num}
                    </div>
                    <h3 class="text-lg md:text-xl font-bold text-gray-900 leading-relaxed mt-1">${qObj.q}</h3>
                </div>
                <div class="space-y-3 pl-0 md:pl-14">
                    ${optionsHTML}
                </div>
            `;

            // Attach listeners to radiogroups
            const radios = qDiv.querySelectorAll('input[type="radio"]');
            radios.forEach(r => {
                r.addEventListener('change', (e) => {
                    userAnswers[index] = parseInt(e.target.value);
                    updateProgress();
                });
            });

            container.appendChild(qDiv);
        });
        
        // Final update for missing count init
        updateProgress();
    }

    async function submitExam() {
        clearInterval(examTimer);
        finishBtn.disabled = true;
        finishBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Guardando...';

        const result = await saveWorkshopResults('Gestión del Tiempo y Control de Ansiedad', userAnswers, correctAnswersArray);

        if (result && result.success) {
            const fbWarning = result.firebaseSuccess ? '' : '<p class="text-xs text-orange-600 mb-2"><i class="fa-solid fa-triangle-exclamation"></i> Nota guardada localmente y enviada por correo (Servidor inactivo).</p>';
            submitPanel.innerHTML = `
                <div class="text-emerald-500 text-6xl mb-4"><i class="fa-solid fa-clipboard-check"></i></div>
                <h3 class="text-2xl font-bold text-gray-900 mb-2">¡Módulo Completado!</h3>
                <p class="text-gray-600 mb-2">Tu puntuación en gestión del tiempo es:</p>
                ${fbWarning}
                <div class="inline-block bg-gray-50 rounded-2xl border-2 border-gray-200 px-8 py-6 mb-4">
                    <div class="text-5xl font-extrabold text-emerald-700">${result.score}/100</div>
                    <div class="text-sm font-bold text-gray-400 mt-2">Aciertos: ${result.raw}/20</div>
                </div>
                <p class="text-sm text-gray-500 mb-6"><i class="fa-solid fa-envelope text-emerald-500"></i> Se ha enviado una copia de tus resultados al correo de administración (cdhmaker@gmail.com).</p>
                <div class="space-y-4">
                    <a href="curso.html" class="block w-full bg-gray-900 text-white font-bold py-3 rounded-xl hover:bg-gray-800 transition-colors">Volver al Curso</a>
                </div>
            `;
        } else {
            submitPanel.innerHTML = `<div class="text-red-500 font-bold">Ocurrió un error guardando el resultado. Por favor toma captura de pantalla de esta alerta para soporte. Nota: ${result ? result.score : 'N/A'}/100.</div>`;
        }
        
        // Disable all radios
        document.querySelectorAll('input[type="radio"]').forEach(r => r.disabled = true);
    }

    function autoSubmitExam() {
        alert("¡Tiempo Agotado! Se enviarán las respuestas actuales.");
        submitExam();
    }

    finishBtn.addEventListener('click', () => {
        const missing = userAnswers.filter(a => a === null).length;
        if (missing > 0) {
            const confirmSubmit = confirm(`Aún tienes ${missing} preguntas sin responder. ¿Seguro que quieres entregar?`);
            if (!confirmSubmit) return;
        }
        submitExam();
    });

    init());