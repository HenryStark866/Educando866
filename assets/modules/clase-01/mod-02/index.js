// taller-modulo-2.js - Gestión del Tiempo y Control de Ansiedad
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
    const questions = [
        {
            q: "Si tienes 90 minutos para resolver 40 preguntas y ya llevas 30 minutos resolviendo 10 preguntas, ¿cuánto tiempo deberías asignar aproximadamente a cada pregunta restante para terminar a tiempo?",
            options: [
                "A) 1.5 minutos por pregunta",
                "B) 2 minutos por pregunta", 
                "C) 2.5 minutos por pregunta",
                "D) 3 minutos por pregunta"
            ], correct: 2
        },
        {
            q: "Durante un examen, notas que te estás poniendo ansioso y tu corazón late rápido. ¿Cuál es la técnica más efectiva para reducir rápidamente la ansiedad en ese momento?",
            options: [
                "A) Tomar un vaso de agua y continuar",
                "B) Cerrar los ojos y hacer 3 respiraciones profundas",
                "C) Acelerar el ritmo para terminar antes",
                "D) Ignorar los síntomas y seguir trabajando"
            ], correct: 1
        },
        {
            q: "Al revisar tus respuestas faltan 5 minutos y tienes 8 preguntas sin responder. ¿Qué estrategia deberías seguir?",
            options: [
                "A) Responder las 8 preguntas más fáciles primero",
                "B) Responder las 8 preguntas en orden secuencial",
                "C) Adivinar en las 8 preguntas restantes",
                "D) Dejar las 8 preguntas en blanco y revisar las ya respondidas"
            ], correct: 0
        },
        {
            q: "Si en un examen de 120 preguntas tienes que responder en 210 minutos, ¿cuál es el tiempo promedio máximo que deberías dedicar a cada pregunta?",
            options: [
                "A) 1 minuto 30 segundos",
                "B) 1 minuto 45 segundos",
                "C) 1 minuto 50 segundos", 
                "D) 2 minutos"
            ], correct: 1
        },
        {
            q: "¿Cuál de las siguientes afirmaciones sobre la gestión del tiempo en exámenes es FALSA?",
            options: [
                "A) Es mejor responder primero las preguntas que sabes con certeza",
                "B) Deberías dedicar el mismo tiempo a todas las preguntas sin importar su dificultad",
                "C) Revisar tus respuestas al final puede mejorar tu puntaje",
                "D) Si te quedas atascado en una pregunta, es mejor pasar a la siguiente y regresar después"
            ], correct: 1
        }
    ];

    // Fill the rest with placeholders to reach 20 questions
    const placeholderQuestions = Array.from({length: 15}, (_, i) => ({
        q: `Pregunta de Gestión del Tiempo #${i+6}: [Simulación] Estrategia óptima para distribuir tiempo en secciones del examen según dificultad personal y ponderación de cada sección.`,
        options: [
            `A) Estrategia A: Enfocarse primero en las secciones de mayor ponderación.`,
            `B) Estrategia B: Distribuir tiempo equitativamente entre todas las secciones.`,
            `C) Estrategia C: Comenzar con las secciones donde tienes mayor habilidad.`,
            `D) Estrategia D: Alternar entre secciones para mantener la mente fresca.`
        ], correct: 2
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

    init();
});