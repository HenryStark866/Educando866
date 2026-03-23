// simulacro-global.js

// Generador de 80 preguntas (Mock para demostración de alto nivel)
const generateQuestions = () => {
    const questions = [];
    
    // 40 Competencia Lectora
    for (let i = 1; i <= 40; i++) {
        let text = i <= 20 ? "TEXTO 1: Inteligencia Artificial" : "TEXTO 2: Filosofía Griega";
        questions.push({
            id: i,
            area: 'lectura',
            textTitle: text,
            statement: `Pregunta de Competencia Lectora #${i}. Según el autor en el párrafo anterior, ¿cuál es la inferencia más válida?`,
            options: [
                { id: 'a', text: 'La afirmación principal no tiene sustento en los hechos mencionados.' },
                { id: 'b', text: 'El desarrollo tecnológico es un peligro inherente e ineludible.' },
                { id: 'c', text: 'La optimización algorítmica carece de moralidad intrínseca.' },
                { id: 'd', text: 'La inteligencia biológica superará siempre a la artificial por su adaptabilidad.' }
            ],
            correct: 'c'
        });
    }

    // 40 Razonamiento Lógico
    for (let i = 41; i <= 80; i++) {
        let diff = i > 70 ? 'Avanzado' : 'Medio';
        questions.push({
            id: i,
            area: 'logica',
            textTitle: `Razonamiento Matemático - Nivel ${diff}`,
            statement: `Pregunta de Lógica #${i}. Si 5 máquinas idénticas tardan 12 horas en ensamblar 300 piezas, ¿cuántas horas tardarían 8 máquinas del doble de eficiencia en ensamblar 900 piezas? (Aplica proporciones compuestas).`,
            options: [
                { id: 'a', text: '9 horas' },
                { id: 'b', text: '11.25 horas' },
                { id: 'c', text: '18 horas' },
                { id: 'd', text: '22.5 horas' }
            ],
            correct: 'b' // (300/60 = 5p/h per mach -> 10p/h eff -> 8 mach = 80p/h -> 900/80 = 11.25)
        });
    }
    return questions;
};

const questionsData = generateQuestions();
let timerInterval;

document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-exam-btn');
    const modal = document.getElementById('student-modal');
    const mainUI = document.getElementById('main-ui');
    const container = document.getElementById('questions-container');
    const answeredCountEL = document.getElementById('answered-count');
    
    // Render Questions
    questionsData.forEach((q, index) => {
        const div = document.createElement('div');
        div.className = "bg-white border text-sm border-gray-100 rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group";
        
        let areaColor = q.area === 'lectura' ? 'sky' : 'emerald';
        
        div.innerHTML = `
            <div class="absolute left-0 top-0 h-full w-1 bg-${areaColor}-500 opacity-50"></div>
            <div class="flex items-center gap-2 mb-3">
                <span class="text-xs font-bold text-gray-400 bg-gray-100 px-2 py-1 rounded">Pregunta ${q.id}</span>
                <span class="text-[10px] font-bold text-${areaColor}-600 bg-${areaColor}-50 px-2 py-1 rounded uppercase tracking-wider">${q.textTitle}</span>
            </div>
            <p class="font-bold text-gray-800 mb-5 text-[15px] leading-snug">${q.statement}</p>
            <div class="space-y-3">
                ${q.options.map(opt => `
                    <label class="flex items-start p-3 border border-gray-200 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors relative">
                        <input type="radio" name="q${q.id}" value="${opt.id}" class="sr-only option-radio" onchange="updateCounter()">
                        <div class="w-full flex">
                            <div class="w-5 h-5 rounded-full border-2 border-gray-300 mr-3 flex-shrink-0 flex items-center justify-center indicator mt-0.5">
                                <i class="fa-solid fa-check text-[10px] opacity-0"></i>
                            </div>
                            <span class="text-gray-700 select-none">${opt.text}</span>
                        </div>
                    </label>
                `).join('')}
            </div>
        `;
        container.appendChild(div);
    });

    // Start Logic
    startBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
        mainUI.classList.remove('hidden');
        document.body.classList.remove('overflow-hidden');
        
        // 3 Hours Timer
        startTimer(3 * 60 * 60, document.getElementById('countdown-timer'));
    });

    // Counter Update attached to global scope
    window.updateCounter = () => {
        const answered = document.querySelectorAll('.option-radio:checked').length;
        answeredCountEL.textContent = answered;
    };

    // Finish Exam
    document.getElementById('finish-exam-btn').addEventListener('click', () => {
        gradeExam();
    });
});

function startTimer(duration, display) {
    let timer = duration, hours, minutes, seconds;
    timerInterval = setInterval(() => {
        hours = parseInt(timer / 3600, 10);
        minutes = parseInt((timer % 3600) / 60, 10);
        seconds = parseInt(timer % 60, 10);

        hours = hours < 10 ? "0" + hours : hours;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = `${hours}:${minutes}:${seconds}`;

        if (timer < 300) { display.classList.add('text-red-500'); } // Last 5 mins
        if (--timer < 0) {
            clearInterval(timerInterval);
            display.textContent = "00:00:00";
            gradeExam(true); // Forced submission
        }
    }, 1000);
}

function gradeExam(forced = false) {
    clearInterval(timerInterval);
    
    let lecturaScore = 0;
    let logicaScore = 0;
    
    questionsData.forEach(q => {
        const selected = document.querySelector(`input[name="q${q.id}"]:checked`);
        if (selected && selected.value === q.correct) {
            if (q.area === 'lectura') lecturaScore++;
            else logicaScore++;
        }
    });

    // Calc %
    const lecPerc = Math.round((lecturaScore / 40) * 100);
    const logPerc = Math.round((logicaScore / 40) * 100);
    const totalPerc = Math.round(((lecturaScore + logicaScore) / 80) * 100);

    // Salvar resultados globalmente si existe window.parent o localStorage (simulando Base de Datos/Firebase)
    localStorage.setItem('educando866_simulacro_lectura', lecPerc);
    localStorage.setItem('educando866_simulacro_logica', logPerc);
    localStorage.setItem('educando866_simulacro_total', totalPerc);

    // Custom stylized alert instead of standard alert
    document.body.insertAdjacentHTML('beforeend', `
        <div class="fixed inset-0 z-[100] bg-gray-900/95 backdrop-blur-xl flex items-center justify-center p-4">
            <div class="bg-gray-900 border border-gray-800 rounded-3xl p-10 shadow-[0_0_100px_rgba(16,185,129,0.3)] max-w-lg w-full text-center">
                <i class="fa-solid fa-flag-checkered text-6xl text-emerald-500 mb-6 drop-shadow-[0_0_15px_rgba(16,185,129,0.8)]"></i>
                <h2 class="text-4xl font-extrabold text-white mb-2">Prueba Finalizada</h2>
                <p class="text-gray-400 mb-10 text-sm">${forced ? 'El tiempo límite expiró.' : 'Has entregado el simulacro.'}</p>
                
                <div class="grid grid-cols-2 gap-4 mb-8">
                    <div class="bg-sky-900/30 border border-sky-800/50 rounded-2xl p-4">
                        <p class="text-sky-400 text-xs font-bold tracking-widest uppercase mb-1">Competencia Lectora</p>
                        <p class="text-3xl font-bold text-white">${lecPerc}%</p>
                    </div>
                    <div class="bg-emerald-900/30 border border-emerald-800/50 rounded-2xl p-4">
                        <p class="text-emerald-400 text-xs font-bold tracking-widest uppercase mb-1">Lógica Matemática</p>
                        <p class="text-3xl font-bold text-white">${logPerc}%</p>
                    </div>
                </div>

                <p class="text-gray-300 text-sm mb-8 bg-white/5 py-3 rounded-lg border border-white/10">Estos resultados se han guardado en tu <b class="text-emerald-400">Dashboard de Analíticas</b>.</p>

                <a href="curso.html" class="inline-block w-full bg-white text-gray-900 font-extrabold py-4 px-8 rounded-xl hover:bg-emerald-400 transition-colors cursor-pointer">
                    Volver al Dashboard
                </a>
            </div>
        </div>
    `);
}
