// ai-professor.js

document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('ai-toggle-btn');
    const closeBtn = document.getElementById('ai-close-btn');
    const chatWindow = document.getElementById('ai-chat-window');
    const chatMessages = document.getElementById('ai-chat-messages');
    
    // New Text Input Elements
    const chatInput = document.getElementById('ai-chat-input');
    const sendBtn = document.getElementById('ai-send-btn');

    // Advanced Keyword Knowledge Base
    const knowledgeBase = [
        {
            keywords: ['regla de tres', 'proporciones', 'proporcionalidad', 'directa', 'inversa', 'obreros', 'dias'],
            area: 'Lógica',
            response: "Para problemas de proporcionalidad en la UdeA, recuerda la regla de oro: **Si una variable sube y la otra baja, es Inversa (se multiplica recto). Si ambas suben, es Directa (se multiplica en cruz)**. Por ejemplo, a más obreros, *menos* días (Inversa)."
        },
        {
            keywords: ['mitosis', 'meiosis', 'celula', 'biologia', 'genetica', 'ADN', 'ARN'],
            area: 'Biología',
            response: "Biología UdeA evalúa fuertemente Genética. Recuerda que la **Mitosis** crea 2 células diploides (idénticas, para crecimiento), mientras que la **Meiosis** crea 4 células haploides (espermatozoides/óvulos) y tiene **entrecruzamiento** para variabilidad genética."
        },
        {
            keywords: ['quimica', 'estequiometria', 'moles', 'soluciones', 'ph', 'acido', 'base'],
            area: 'Química',
            response: "En Química, el cálculo de Molaridad (M = moles soluto / Litros de solución) es vital. Recuerda también que un pH menor a 7 es Ácido. ¡El examen evalúa más el análisis que la memoria de la tabla periódica!"
        },
        {
            keywords: ['fisica', 'cinematica', 'newton', 'energia', 'trabajo', 'velocidad', 'aceleracion'],
            area: 'Física',
            response: "Sobre Física: F = m*a (Segunda Ley de Newton). Ten clarísimo que si no hay fuerza neta, la aceleración es CERO (pero puede haber velocidad constante MRU). Además, el Trabajo (W) = Fuerza x Distancia."
        },
        {
            keywords: ['lectura', 'critica', 'texto', 'autor', 'inferir', 'inferencia', 'principal', 'idea'],
            area: 'Competencia Lectora',
            response: "En Competencia Lectora UdeA, el 60% son inferencias. **Nunca marques una respuesta literal del texto como una inferencia**. La inferencia es una conclusión lógica oculta que extraes de las premisas del autor."
        },
        {
            keywords: ['geometria', 'area', 'volumen', 'triangulo', 'pitagoras', 'circulo'],
            area: 'Lógica',
            response: "Área de triángulos y el Teorema de Pitágoras (a² + b² = c²) salen SIEMPRE en Lógica Matemática de Unal y UdeA. Memoriza los triángulos rectángulos notables (3-4-5 y 5-12-13) para ahorrar tiempo."
        },
        {
            keywords: ['hol', 'ola', 'buen', 'dia', 'tarde', 'noche', 'hey', 'profe'],
            area: 'General',
            response: "¡Hola! Soy tu Profe IA de Educando866. ¿En qué tema tienes dudas hoy? Pregúntame sobre regla de tres, biología celular, leyes de Newton, trucos de lectura crítica, etc."
        }
    ];

    const fallbackResponse = "Interesante pregunta. En el examen de la Universidad, ese es un nivel avanzado que tocamos a profundidad en los Talleres Oficiales. **Te recomiendo repasar tus Guías en PDF**. ¿Tienes dudas sobre alguna rama específica como Lógica o Competencia Lectora?";

    // Toggle Chat visibility
    if(toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            chatWindow.classList.remove('hidden');
            toggleBtn.classList.add('hidden');
            const pulse = toggleBtn.querySelector('.animate-pulse');
            if(pulse) pulse.remove();
            scrollToBottom();
        });
    }

    if(closeBtn) {
        closeBtn.addEventListener('click', () => {
            chatWindow.classList.add('hidden');
            toggleBtn.classList.remove('hidden');
        });
    }

    // Initialize Default Welcome
    if(chatMessages && chatMessages.children.length === 0) {
        chatMessages.innerHTML = `
            <div class="self-start max-w-[85%] bg-white p-3.5 rounded-2xl rounded-tl-sm shadow-sm border border-gray-200 text-sm text-gray-700 slide-up leading-relaxed relative">
                ¡Hola futuro universitario! <i class="fa-solid fa-graduation-cap text-emerald-500"></i><br>Soy tu <b>Profe IA Especializado</b>. Dime tu duda concreta, analiza un concepto o ponme a prueba sobre temas de admisión. <br><br>Escribe tu duda abajo.
            </div>
        `;
    }

    function scrollToBottom() {
        setTimeout(() => {
            if(chatMessages) chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 50);
    }

    function appendMessage(sender, text) {
        const div = document.createElement('div');
        div.className = \`max-w-[85%] p-3.5 rounded-2xl shadow-sm text-sm slide-up leading-relaxed relative \${
            sender === 'user' 
            ? 'self-end bg-emerald-600 text-white rounded-tr-sm border border-emerald-700' 
            : 'self-start bg-white text-gray-700 rounded-tl-sm border border-gray-200'
        }\`;
        div.innerHTML = text;
        chatMessages.appendChild(div);
        scrollToBottom();
    }

    function appendTypingIndicator() {
        const div = document.createElement('div');
        div.id = 'typing-indicator';
        div.className = 'self-start bg-white px-4 py-3.5 rounded-2xl rounded-tl-sm shadow-sm border border-gray-200 flex items-center gap-1.5 slide-up w-16 my-1';
        div.innerHTML = \`
            <div class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-duration: 1s; animation-delay: 0ms;"></div>
            <div class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-duration: 1s; animation-delay: 200ms;"></div>
            <div class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-duration: 1s; animation-delay: 400ms;"></div>
        \`;
        chatMessages.appendChild(div);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }

    function findResponse(query) {
        const lowerQuery = query.toLowerCase();
        
        let bestMatch = null;
        let maxHits = 0;

        for (const kb of knowledgeBase) {
            let hits = 0;
            for (const key of kb.keywords) {
                if (lowerQuery.includes(key)) hits++;
            }
            if (hits > maxHits) {
                maxHits = hits;
                bestMatch = kb;
            }
        }

        if (bestMatch && maxHits > 0) {
            return \`
                <div class="flex items-center gap-2 mb-2 pb-2 border-b border-gray-100">
                    <span class="text-xs font-bold text-emerald-600 uppercase tracking-wider">\${bestMatch.area} ACADÉMICA</span>
                </div>
                \${bestMatch.response.replace(/\\*\\*(.*?)\\*\\*/g, '<strong class="text-emerald-800">$1</strong>')}
            \`;
        }
        
        return fallbackResponse.replace(/\\*\\*(.*?)\\*\\*/g, '<strong class="text-emerald-800">$1</strong>');
    }

    function handleUserInput() {
        const text = chatInput.value.trim();
        if (!text) return;

        // Limpiar input y agregar mensaje user
        chatInput.value = '';
        appendMessage('user', text);

        appendTypingIndicator();

        // Simular pensamiento 1s a 3s según longitud de la pregunta
        const thinkTime = Math.min(3000, 1000 + (text.length * 15));
        
        setTimeout(() => {
            removeTypingIndicator();
            const responseText = findResponse(text);
            appendMessage('bot', responseText);
        }, thinkTime);
    }

    // Attach listeners
    if(sendBtn) {
        sendBtn.addEventListener('click', handleUserInput);
    }
    
    if(chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleUserInput();
        });
    }
});