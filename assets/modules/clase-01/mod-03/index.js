// taller-modulo-3.js - Estrategias de Lectura Crítica Avanzada
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
    let secondsLeft = 35 * 60; // 35 minutes
    let userAnswers = new Array(20).fill(null);

    // Banco de Preguntas (20) - Estrategias de Lectura Crítica Avanzada
    const questions = [
        {
            q: "En un texto argumentativo, el autor menciona varios estudios pero no cita sus fuentes. ¿Qué tipo de falacia está cometiendo potencialmente?",
            options: [
                "A) Apelo a la autoridad",
                "B) Apelo a la popularidad", 
                "C) Apelo ignorante (ad ignorantiam)",
                "D) Falacia de composición"
            ], correct: 2
        },
        {
            q: "Al analizar un texto, identifiques que el autor usa palabras con connotación negativa al describir una postura que contradice la suya. ¿Qué técnica persuasiva está empleando?",
            options: [
                "A) Eufemismo",
                "B) Disimulo",
                "C) Epíteto cargado", 
                "D) Analogía falsa"
            ], correct: 2
        },
        {
            q: "En un párrafo lees: 'Aunque algunos críticos afirman que esta política es beneficiosa, la evidencia reciente sugiere lo contrario.' ¿Cuál es la función del connector 'Aunque' en esta oración?",
            options: [
                "A) Establecer una causa",
                "B) Mostrar una consecuencia",
                "C) Introducir una concesión",
                "D) Añadir información"
            ], correct: 2
        },
        {
            q: "Al evaluar la credibilidad de una fuente en un texto, ¿cuál de los siguientes factores es MENOS relevante?",
            options: [
                "A) La experiencia del autor en el tema",
                "B) La fecha de publicación de la fuente",
                "C) El número de seguidores del autor en redes sociales",
                "D) Si la fuente es revisada por pares"
            ], correct: 2
        },
        {
            q: "En un texto expositivo, el autor presenta datos seguidos de su interpretación. ¿Qué distingue una inferencia válida de una simple opinión?",
            options: [
                "A) La inferencia se basa en sentimientos personales",
                "B) La inferencia puede ser probada o refutada con evidencia",
                "C) La opinión siempre es más valiosa que la inferencia",
                "D) No hay diferencia entre inferencia y opinión"
            ], correct: 1
        }
    ];

    // Fill the rest with placeholders to reach 20 questions
    const placeholderQuestions = Array.from({length: 15}, (_, i) => ({
        q: `Pregunta de Lectura Crítica Avanzada #${i+6}: [Simulación] Análisis de estructura argumentativa, detección de sesgos implícitos y evaluación de la validez de inferencias en textos complejos.`,
        options: [
            `A) Interpretación literal sin análisis profundo.`,
            `B) Identificación de premisas ocultas y evaluación de su solidez.`,
            `C) Enfoque exclusivo en vocabulario difícil.`,
            `D) Memorización de datos específicos del texto.`
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
                `;
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

        const result = await saveWorkshopResults('Estrategias de Lectura Crítica Avanzada', userAnswers, correctAnswersArray);

        if (result && result.success) {
            const fbWarning = result.firebaseSuccess ? '' : '<p class="text-xs text-orange-600 mb-2"><i class="fa-solid fa-triangle-exclamation"></i> Nota guardada localmente y enviada por correo (Servidor inactivo).</p>';
            submitPanel.innerHTML = `
                <div class="text-emerald-500 text-6xl mb-4"><i class="fa-solid fa-clipboard-check"></i></div>
                <h3 class="text-2xl font-bold text-gray-900 mb-2">¡Módulo Completado!</h3>
                <p class="text-gray-600 mb-2">Tu puntuación en lectura crítica avanzada es:</p>
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

    init();
});