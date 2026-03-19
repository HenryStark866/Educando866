// examen-parcial.js - Examen Parcial de Estrategias de Lectura Crítica Avanzada
import { saveWorkshopResults } from "./workshop-storage.js";

document.addEventListener('DOMContentLoaded', () => {
    const studentModal = document.getElementById('student-modal');
    const startForm = document.getElementById('start-exam-form');
    const nameInput = document.getElementById('student-name');
    const emailInput = document.getElementById('student-email');
    
    const container = document.getElementById('questions-container');
    const submitPanel = document.getElementById('submit-panel');
    const finishBtn = document.getElementById('finish-exam-btn');
    const timerDisplay = document.getElementById('countdown-timer');
    const progressBar = document.getElementById('progress-bar');
    const progressContainer = document.getElementById('progress-bar-container');
    
    const unansweredWarning = document.getElementById('unanswered-warning');
    const unansweredCount = document.getElementById('unanswered-count');

    let examTimer;
    let secondsLeft = 20 * 60; // 20 minutes
    let userAnswers = new Array(10).fill(null);

    // Banco de Preguntas (10) - Examen Parcial de Estrategias de Lectura Crítica Avanzada
    const questions = [
        {
            q: "Al evaluar la credibilidad de una fuente en un texto académico, ¿cuál de los siguientes factores contribuye MÁS a su autoridad?",
            options: [
                "A) La antigüedad de la publicación",
                "B) El número de páginas del documento",
                "C) La revisión por pares y la afiliación institucional del autor",
                "D) El tamaño de la fuente utilizada"
            ], correct: 2
        },
        {
            q: "En un texto que presenta una postura controvertida, el autor utiliza principalmente datos de estudios financiados por una organización que se beneficiaría económicamente de que se aceptara dicha postura. ¿Qué riesgo analítico está presente?",
            options: [
                "A) Sesgo de confirmación",
                "B) Confusión de causalidad",
                "C) Conflicto de intereses potencial",
                "D) Error de muestreo"
            ], correct: 2
        },
        {
            q: "Al identificar la idea central de un párrafo complejo, ¿qué elemento debes buscar PRIMERO?",
            options: [
                "A) El ejemplo más detallado",
                "B) La primera oración del párrafo",
                "C) La afirmación que resume o generaliza el contenido",
                "D) La palabra más repetida"
            ], correct: 2
        },
        {
            q: "¿Cuál de las siguientes afirmaciones sobre las inferencias válidas es CORRECTA?",
            options: [
                "A) Una inferencia puede ser válida incluso si contradice información explícita del texto",
                "B) Una inferencia válida debe estar completamente explícita en el texto",
                "C) Una inferencia válida se deriva logicamente de la información proporcionada en el texto",
                "D) Las inferencias siempre son subjetivas y dependen del lector"
            ], correct: 2
        },
        {
            q: "En un texto expositivo sobre el cambio climático, el autor presenta un gráfico que muestra aumento de temperatura seguido de la afirmación 'Este patrón demuestra que las actividades humanas son la causa principal'. ¿Qué tipo de salto lógico podría estar presente?",
            options: [
                "A) Generalización apresurada",
                "B) Confusión entre correlación y causalidad",
                "C) Falacia de autoridad",
                "D) Dilema falso"
            ], correct: 1
        }
    ];

    // Fill the rest with placeholders to reach 10 questions
    const placeholderQuestions = Array.from({length: 5}, (_, i) => ({
        q: `Pregunta de Examen Parcial #${i+6}: [Simulación] Evaluación integral de competencias en lectura crítica avanzada, análisis de argumentos y evaluación de evidencia en textos complejos.`,
        options: [
            `A) Enfoque literal: centrarse solo en lo que dice explícitamente el texto.`,
            `B) Enfoque crítico: analizar argumentos, identificar sesgos y evaluar la validez de inferencias.`,
            `C) Enfoque superficial: buscar solo palabras clave sin entender el contexto.`,
            `D) Enfoque memorístico: tratar de recordar tanto como sea posible del texto.`
        ], correct: 1
    }));

    questions.push(...placeholderQuestions);

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
        const progressPercent = (answeredCount / 10) * 100;
        progressBar.style.width = `${progressPercent}%`;

        const missing = 10 - answeredCount;
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

        const result = await saveWorkshopResults('Examen Parcial - Lectura Crítica Avanzada', userAnswers, correctAnswersArray);

        if (result && result.success) {
            const fbWarning = result.firebaseSuccess ? '' : '<p class="text-xs text-orange-600 mb-2"><i class="fa-solid fa-triangle-exclamation"></i> Nota guardada localmente y enviada por correo (Servidor inactivo).</p>';
            submitPanel.innerHTML = `
                <div class="text-emerald-500 text-6xl mb-4"><i class="fa-solid fa-clipboard-check"></i></div>
                <h3 class="text-2xl font-bold text-gray-900 mb-2">¡Examen Parcial Completado!</h3>
                <p class="text-gray-600 mb-2">Tu puntuación en el examen parcial es:</p>
                ${fbWarning}
                <div class="inline-block bg-gray-50 rounded-2xl border-2 border-gray-200 px-8 py-6 mb-4">
                    <div class="text-5xl font-extrabold text-emerald-700">${result.score}/100</div>
                    <div class="text-sm font-bold text-gray-400 mt-2">Aciertos: ${result.raw}/10</div>
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

    init();
});