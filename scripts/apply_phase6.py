import os
import re

workspace = r"c:\Users\Admin Mantenimiento\OneDrive - Antioqueña de Incubacion\Escritorio\Educando866-main"

# 1. Update index.html
index_file = os.path.join(workspace, "index.html")
with open(index_file, "r", encoding="utf-8") as f:
    idx_content = f.read()

idx_content = idx_content.replace('Entrar al curso', 'Acceder al Aula')
idx_content = idx_content.replace('alt="Estudiante de Veterinaria"', 'alt="Estudiante Universitario"')

with open(index_file, "w", encoding="utf-8") as f:
    f.write(idx_content)

# 2. Update ai-professor.js
aiprof_file = os.path.join(workspace, "ai-professor.js")
with open(aiprof_file, "r", encoding="utf-8") as f:
    ai_content = f.read()

ai_content = ai_content.replace('Para el componente de Biología en Veterinaria UdeA, enfócate en **biología celular (mitosis, meiosis)** y los **sistemas del cuerpo animal**.', 'Para el componente de Biología UdeA, enfócate en **biología celular (mitosis, meiosis)** y los **sistemas metabólicos celulares**.')
ai_content = ai_content.replace('¡Hola futuro veterinario!', '¡Hola futuro universitario!')
ai_content = ai_content.replace('VetPrep UdeA', 'PrepUdeA')

with open(aiprof_file, "w", encoding="utf-8") as f:
    f.write(ai_content)

# 3. Inject Pomodoro into curso.html
curso_file = os.path.join(workspace, "curso.html")
with open(curso_file, "r", encoding="utf-8") as f:
    crso_content = f.read()

pomodoro_html = """                <!-- Pomodoro Widget -->
                <div class="bg-white rounded-2xl p-5 border border-gray-200 shadow-sm mb-6 flex flex-col items-center transform hover:scale-[1.02] transition-transform">
                    <div class="flex items-center gap-2 mb-2 w-full justify-center text-gray-400">
                        <i class="fa-solid fa-stopwatch text-emerald-500 animate-pulse"></i>
                        <span class="text-xs font-bold uppercase tracking-widest text-gray-500">Pomodoro Focus</span>
                    </div>
                    <div id="pomodoro-display" class="text-4xl font-extrabold text-gray-900 mb-4 tracking-tighter" style="font-family: monospace;">25:00</div>
                    <div class="flex gap-2 w-full">
                        <button id="pomodoro-start" class="flex-1 bg-emerald-100 text-emerald-700 hover:bg-emerald-200 py-2 rounded-xl text-sm font-bold transition-all shadow-sm">Iniciar</button>
                        <button id="pomodoro-reset" class="flex-1 bg-gray-50 text-gray-500 hover:bg-gray-100 hover:text-gray-700 py-2 rounded-xl text-sm font-bold transition-colors">Reiniciar</button>
                    </div>
                </div>

"""
# Find target string for injection
target_tips = '                <!-- Formation Tips Widget -->'
if pomodoro_html not in crso_content and target_tips in crso_content:
    crso_content = crso_content.replace(target_tips, pomodoro_html + target_tips)

pomodoro_js = """
        // Pomodoro Timer Logic
        let pomoInterval;
        let pomoTime = 25 * 60;
        let isPomoRunning = false;
        const pomoDisplay = document.getElementById('pomodoro-display');
        const pomoStartBtn = document.getElementById('pomodoro-start');
        
        function formatPomoTime(seconds) {
            const m = Math.floor(seconds / 60).toString().padStart(2, '0');
            const s = (seconds % 60).toString().padStart(2, '0');
            return `${m}:${s}`;
        }
        
        if (pomoStartBtn) {
            pomoStartBtn.addEventListener('click', () => {
                if (isPomoRunning) {
                    clearInterval(pomoInterval);
                    isPomoRunning = false;
                    pomoStartBtn.textContent = 'Reanudar';
                    pomoStartBtn.className = 'flex-1 bg-emerald-100 text-emerald-700 hover:bg-emerald-200 py-2 rounded-xl text-sm font-bold transition-all shadow-sm';
                } else {
                    isPomoRunning = true;
                    pomoStartBtn.textContent = 'Pausar';
                    pomoStartBtn.className = 'flex-1 bg-yellow-100 text-yellow-700 hover:bg-yellow-200 py-2 rounded-xl text-sm font-bold transition-all shadow-sm';
                    pomoInterval = setInterval(() => {
                        if (pomoTime > 0) {
                            pomoTime--;
                            pomoDisplay.textContent = formatPomoTime(pomoTime);
                        } else {
                            clearInterval(pomoInterval);
                            isPomoRunning = false;
                            pomoStartBtn.textContent = 'Iniciar';
                            pomoStartBtn.className = 'flex-1 bg-emerald-100 text-emerald-700 hover:bg-emerald-200 py-2 rounded-xl text-sm font-bold transition-all shadow-sm';
                            alert('¡Pomodoro de 25 minutos terminado! El cerebro necesita descansar. Tómate 5 minutos.');
                            pomoTime = 5 * 60; // 5 min break
                            pomoDisplay.textContent = formatPomoTime(pomoTime);
                        }
                    }, 1000);
                }
            });
            
            document.getElementById('pomodoro-reset').addEventListener('click', () => {
                clearInterval(pomoInterval);
                isPomoRunning = false;
                pomoTime = 25 * 60;
                pomoDisplay.textContent = formatPomoTime(pomoTime);
                pomoStartBtn.textContent = 'Iniciar';
                pomoStartBtn.className = 'flex-1 bg-emerald-100 text-emerald-700 hover:bg-emerald-200 py-2 rounded-xl text-sm font-bold transition-all shadow-sm';
            });
        }
"""
target_end_script = "        setInterval(rotateTips, 8000);"
if "Pomodoro Timer Logic" not in crso_content and target_end_script in crso_content:
    crso_content = crso_content.replace(target_end_script, target_end_script + pomodoro_js)

with open(curso_file, "w", encoding="utf-8") as f:
    f.write(crso_content)

print("Text replacements and Pomodoro injection completed.")
