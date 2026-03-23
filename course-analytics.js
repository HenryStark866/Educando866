// course-analytics.js

document.addEventListener('DOMContentLoaded', () => {
    // Read from localStorage (saved by simulacro-global.js)
    const lecScore = parseInt(localStorage.getItem('educando866_simulacro_lectura')) || 0;
    const logScore = parseInt(localStorage.getItem('educando866_simulacro_logica')) || 0;
    const totalScore = parseInt(localStorage.getItem('educando866_simulacro_total')) || 0;

    const elStatLec = document.getElementById('stat-lectura');
    const elBarLec = document.getElementById('bar-lectura');
    const elStatLog = document.getElementById('stat-logica');
    const elBarLog = document.getElementById('bar-logica');
    const recText = document.getElementById('ia-recommendation');

    if (lecScore > 0 || logScore > 0) {
        // Update bars
        setTimeout(() => {
            elStatLec.textContent = lecScore + '%';
            elBarLec.style.width = lecScore + '%';
            
            elStatLog.textContent = logScore + '%';
            elBarLog.style.width = logScore + '%';
        }, 500);

        // Simple IA recommendation logic based on difference
        if (lecScore < 50 && logScore < 50) {
            recText.innerHTML = "Prioridad Crítica: Fundamentos.<br><span class='font-normal text-xs text-gray-300'>Vuelve a los módulos 1 al 4 inmediatamente.</span>";
            recText.className = "text-sm font-bold text-red-400 mt-1 leading-tight";
        } else if (lecScore >= 80 && logScore >= 80) {
            recText.innerHTML = "¡Nivel de Admisión Alcanzado!<br><span class='font-normal text-xs text-emerald-200'>Mantén la práctica constante de simulacros.</span>";
            recText.className = "text-sm font-bold text-emerald-400 mt-1 leading-tight";
        } else if (lecScore > logScore + 20) {
            recText.innerHTML = "Alerta: Desbalance Lógico.<br><span class='font-normal text-xs text-sky-200'>Tu lectura nos salvará, pero necesitas fortalecer 'Proporcionalidad Inversa'.</span>";
            recText.className = "text-sm font-bold text-sky-400 mt-1 leading-tight";
        } else if (logScore > lecScore + 20) {
            recText.innerHTML = "Alerta: Desbalance Lector.<br><span class='font-normal text-xs text-emerald-200'>Cálculo excelente, pero las inferencias de texto te están costando puntos.</span>";
            recText.className = "text-sm font-bold text-emerald-400 mt-1 leading-tight";
        } else {
            recText.innerHTML = "Rendimiento Equilibrado.<br><span class='font-normal text-xs text-gray-300'>Trata de aumentar un 10% en ambas áreas la próxima semana.</span>";
            recText.className = "text-sm font-bold text-yellow-400 mt-1 leading-tight";
        }
    }
});
