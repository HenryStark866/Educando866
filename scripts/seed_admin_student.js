/**
 * DB Seeder — Registra al director de la plataforma como primer estudiante aprobado.
 * Ejecutar una sola vez con: node scripts/seed_admin_student.js
 * Requiere firebase-admin instalado y un Service Account JSON.
 *
 * INSTRUCCIONES DE USO:
 * 1. Ve a Firebase Console > Configuración del proyecto > Cuentas de servicio.
 * 2. Haz clic en "Generar nueva clave privada" y guarda el JSON como `serviceAccount.json`
 *    en la raíz del proyecto (¡No subas este archivo a GitHub!).
 * 3. Instala Admin SDK: npm install firebase-admin
 * 4. Corre: node scripts/seed_admin_student.js
 */
const admin = require('firebase-admin');
const serviceAccount = require('../serviceAccount.json');

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://prepudea-platform-default-rtdb.firebaseio.com"
});

const db = admin.firestore();
const auth = admin.auth();

async function seedAdminStudent() {
    const email = 'henry.taborda866@pascualbravo.edu.co'; // Correo del admin/director
    const password = 'PrepUdeA2026!Admin';                // Contraseña segura provisional
    const nombre = 'Henry Stark - Director';
    const plan = 'admin';

    try {
        // 1. Create user in Firebase Auth
        let userRecord;
        try {
            userRecord = await auth.getUserByEmail(email);
            console.log(`[INFO] Usuario ya existe: ${userRecord.uid}`);
        } catch (e) {
            userRecord = await auth.createUser({ email, password, displayName: nombre });
            console.log(`[OK] Usuario creado con UID: ${userRecord.uid}`);
        }

        // 2. Seed Firestore profile with all flags enabled
        await db.collection('estudiantes').doc(userRecord.uid).set({
            nombre,
            email,
            plan,
            pago_verificado: true,
            curso_completado: true,
            es_admin: true,
            primer_estudiante: true,
            clases_vistas: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            quiz_scores: { 'modulo-01': 100, 'modulo-02': 100 },
            notas: { 1: 'Clase completada. Estrategia verificada.' },
            fecha_registro: admin.firestore.FieldValue.serverTimestamp(),
            historia: 'Primer estudiante en completar el curso PrepUdeA en Colombia.'
        }, { merge: true });

        console.log('[OK] Perfil de director guardado en Firestore con pago_verificado=true.');
        console.log(`\nCredenciales de acceso:\n  Email: ${email}\n  Password: ${password}`);
    } catch (err) {
        console.error('[ERROR]', err.message);
    } finally {
        process.exit(0);
    }
}

seedAdminStudent();
