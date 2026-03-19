// examen-parcial.js - Examen Parcial de Gestión del Tiempo y Control de Ansiedad
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

    // Banco de Preguntas (10) - Examen Parcial de Gestión del Tiempo y Control de Ansiedad
    const questions = [
        {
            q: "Si un estudiante tiene 120 minutos para un examen de 60 preguntas y ya ha usado 40 minutos para completar 20 preguntas, ¿a qué ritmo debería trabajar para terminar exactamente a tiempo?",
            options: [
                "A) 1 pregunta por minuto",
                "B) 1.5 preguntas por minuto", 
                "C) 2 preguntas por minuto",
                "D) 0.5 preguntas por minuto"
            ], correct: 0
        },
        {
            q: "Durante un examen de admisión, notas que tu mente divaga y pierdes concentración. ¿Cuál es la mejor estrategia inmediata para recuperar el foco?",
            options: [
                "A) Beber un trago de agua y continuar",
                "B) Hacer un estiramiento rápido de cuello y hombros",
                "C) Aumentar el ritmo de respuesta para 'ponerte al día'", 
                "D) Ignorar la distracción y forzar la concentración"
            ], correct: 1
        },
        {
            q: "Al practicar para un examen, aplicas la regla de que no debes pasar más de 2 minutos en ninguna pregunta. Si te encuentras con un problema complejo que claramente requerirá más tiempo, ¿qué deberías hacer?",
            options: [
                "A) Saltarte la pregunta y regresar si sobra tiempo",
                "B) Dedicar exactamente 2 minutos y luego avanzar",
                "C) Pedir ayuda al proctor", 
                "D) Adivinar aleatoriamente y continuar"
            ], correct: 0
        },
        {
            q: "Si en un examen de matemáticas tienes 30 minutos para resolver 15 problemas de cálculo y ya llevas 18 minutos habiendo resuelto 8 problemas, ¿cuál es tu situación actual?",
            options: [
                "A) Vas adelantado, tienes tiempo de sobra",
                "B) Vas exactamente según lo planeado",
                "C) Vas retrasado, necesitas acelerar", 
                "D) No se puede determinar con la información dada"
            ], correct: 2
        },
        {
            q: "¿Cuál de las siguientes técnicas es MENOS efectiva para controlar la ansiedad durante un examen de admisión?",
            options: [
                "A) Respiración diafragmática profunda",
                "B) Visualización positiva del resultado",
                "C) Comparar tu desempeño con el de otros estudiantes",
                "D) Uso de afirmaciones positivas personales"
            ], correct: 2
        }
    ];

    // Fill the rest with placeholders to reach 10 questions
    const placeholderQuestions = Array.from({length: 5}, (_, i) => ({
        q: `Pregunta de Examen Parcial #${i+6}: [Simulación] Evaluación integral de competencias en gestión del tiempo, control de ansiedad y toma de decisiones estratégicas bajo presión temporal.`,
        options: [
            `A) Enfoque reactivo: responder conforme surgen las preguntas sin planificación.`,
            `B) Enfoque estratégico: planificar asignación de tiempo según dificultad y ponderación.`,
            `C) Enfoque perfeccionista: dedicar tiempo excesivo a asegurar respuestas correctas.`,
            `D) Enfoque arriesgado: responder rápidamente para terminar antes de tiempo.`
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

        const result = await saveWorkshopResults('Examen Parcial - Gestión del Tiempo', userAnswers, correctAnswersArray);

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