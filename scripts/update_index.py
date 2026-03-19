import os

path = r"c:\Users\Admin Mantenimiento\OneDrive - Antioqueña de Incubacion\Escritorio\Educando866-main\index.html"
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize line endings to avoid \r\n vs \n issues
text = text.replace('\r\n', '\n')

text = text.replace('                    <a href="curso.html" class="text-gray-600 hover:text-emerald-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">Entrar al curso</a>\n', '')
text = text.replace('                <a href="curso.html" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-emerald-600 hover:bg-emerald-50">Entrar al curso</a>\n', '')

form_target = """                <form id="student-login-form" autocomplete="on" class="space-y-5">
                    <div class="rounded-xl border border-emerald-200 bg-emerald-50 p-3">
                        <p class="text-xs font-semibold text-emerald-800">Becados Prep U: puedes ingresar con cédula + código de acceso.</p>
                    </div>
                    <div>
                        <label for="student-name" class="block text-sm font-semibold text-gray-700 mb-1.5">Nombre</label>
                        <input type="text" id="student-name" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 focus:bg-white transition-colors text-gray-800 font-medium placeholder-gray-400 outline-none" placeholder="Tu nombre completo" required>
                    </div>
                    <div>
                        <label for="student-email" class="block text-sm font-semibold text-gray-700 mb-1.5">Correo</label>
                        <input type="email" id="student-email" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 focus:bg-white transition-colors text-gray-800 font-medium placeholder-gray-400 outline-none" placeholder="tucorreo@ejemplo.com" required>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div>
                            <label for="student-id" class="block text-sm font-semibold text-gray-700 mb-1.5">Cédula (opcional)</label>
                            <input type="text" id="student-id" inputmode="numeric" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 focus:bg-white transition-colors text-gray-800 font-medium placeholder-gray-400 outline-none" placeholder="1032097855">
                        </div>
                        <div>
                            <label for="student-access-code" class="block text-sm font-semibold text-gray-700 mb-1.5">Código becado (opcional)</label>
                            <input type="text" id="student-access-code" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 focus:bg-white transition-colors text-gray-800 font-medium placeholder-gray-400 outline-none" placeholder="BEC-0001-NGA">
                        </div>
                    </div>
                    <p id="student-login-error" class="hidden text-sm text-red-600 font-medium">Credenciales de becado inválidas. Verifica cédula y código.</p>"""

form_replace = """                <form id="student-login-form" autocomplete="on" class="space-y-5">
                    <div>
                        <label for="student-email" class="block text-sm font-semibold text-gray-700 mb-1.5">Correo Electrónico</label>
                        <input type="email" id="student-email" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 focus:bg-white transition-colors text-gray-800 font-medium placeholder-gray-400 outline-none" placeholder="tucorreo@ejemplo.com" required>
                    </div>
                    <div>
                        <label for="student-password" class="block text-sm font-semibold text-gray-700 mb-1.5">Contraseña</label>
                        <input type="password" id="student-password" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 focus:bg-white transition-colors text-gray-800 font-medium placeholder-gray-400 outline-none" placeholder="••••••••" required>
                    </div>
                    <p id="student-login-error" class="hidden text-sm text-red-600 font-medium">Credenciales inválidas. Verifica tu correo y contraseña.</p>"""

text = text.replace(form_target, form_replace)

js_target = """        if (studentLoginForm) {
            studentLoginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                studentLoginError.classList.add('hidden');

                let name = document.getElementById('student-name').value.trim();
                let email = document.getElementById('student-email').value.trim();
                const idNumber = document.getElementById('student-id').value.trim();
                const accessCode = document.getElementById('student-access-code').value.trim().toUpperCase();

                const usingScholarshipLogin = idNumber !== '' || accessCode !== '';
                if (usingScholarshipLogin) {
                    const profile = scholarshipProfiles.find((item) => item.idNumber === idNumber && item.accessCode === accessCode);
                    if (!profile) {
                        studentLoginError.classList.remove('hidden');
                        return;
                    }

                    name = profile.fullName;
                    if (!email) email = profile.emailAlias;
                    localStorage.setItem('vetprep_student_id', profile.idNumber);
                    localStorage.setItem('vetprep_student_access_code', profile.accessCode);
                    localStorage.setItem('vetprep_student_role', 'becado');
                    localStorage.setItem('vetprep_student_plan', profile.plan);
                    localStorage.setItem('vetprep_student_status', profile.status);
                } else {
                    localStorage.setItem('vetprep_student_role', 'estudiante');
                }

                localStorage.setItem('vetprep_student_name', name);
                localStorage.setItem('vetprep_student_email', email);
                localStorage.setItem('vetprep_student_logged_in', 'true');
                window.location.href = 'curso.html';
            });
        }"""
        
js_replace = """        if (studentLoginForm) {
            studentLoginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                studentLoginError.classList.add('hidden');

                let email = document.getElementById('student-email').value.trim();
                let password = document.getElementById('student-password').value.trim();

                if (email && password) {
                    localStorage.setItem('vetprep_student_role', 'estudiante');
                    localStorage.setItem('vetprep_student_name', email.split('@')[0]);
                    localStorage.setItem('vetprep_student_email', email);
                    localStorage.setItem('vetprep_student_logged_in', 'true');
                    window.location.href = 'curso.html';
                } else {
                    studentLoginError.classList.remove('hidden');
                }
            });
        }"""

text = text.replace(js_target, js_replace)

# Write back with original \r\n
with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated index.html")
