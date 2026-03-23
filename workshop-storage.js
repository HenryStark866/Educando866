// workshop-storage.js
import { db, auth } from "./firebase-config.js";
import { collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-firestore.js";

const ADMIN_NOTIFICATION_EMAIL = "henrytaborda866@pascualbravo.edu.co";

function withTimeout(promise, ms, label) {
    return Promise.race([
        promise,
        new Promise((_, reject) => setTimeout(() => reject(new Error(`timeout:${label}`)), ms))
    ]);
}

/**
 * Guarda los resultados del taller en Firestore de forma automática.
 * @param {string} workshopType - 'Logica' o 'Lectura'
 * @param {Array} userAnswers - Array con las respuestas seleccionadas por el usuario.
 * @param {Array} correctAnswers - Array base con las respuestas correctas.
 */
export async function saveWorkshopResults(workshopType, userAnswers, correctAnswers) {
    if (!userAnswers || !correctAnswers || userAnswers.length !== correctAnswers.length) {
        console.error("Error: Arrays de respuestas no coinciden o están incompletos.");
        return null;
    }

    let rawScore = 0;
    const totalQuestions = correctAnswers.length;

    // Calculamos el puntaje
    for (let i = 0; i < totalQuestions; i++) {
        if (userAnswers[i] === correctAnswers[i]) {
            rawScore++;
        }
    }

    // Puntaje simulado sobre 100
    const finalScore = parseFloat(((rawScore / totalQuestions) * 100).toFixed(2));

    // Obtener datos del estudiante (Prioridad Auth -> LocalStorage)
    const currentUser = auth ? auth.currentUser : null;
    const studentName = currentUser?.displayName || localStorage.getItem('educando866_student_name') || 'Anónimo';
    const studentEmail = currentUser?.email || localStorage.getItem('educando866_student_email') || 'anonimo@anonimo.com';
    const uid = currentUser?.uid || 'guest';
    
    // Almacenamiento del documento
    const workshopData = {
        student: {
            uid: uid,
            name: studentName,
            email: studentEmail
        },
        workshopType: workshopType,
        score: {
            raw: rawScore,
            totalQuestions: totalQuestions,
            final: finalScore
        },
        createdAt: serverTimestamp(),
        deviceUserAgent: navigator.userAgent
    };

    let docId = 'N/A';
    let firebaseSuccess = false;

    // Firebase addDoc con timeout de 8 segundos
    try {
        const docRef = await withTimeout(addDoc(collection(db, "talleres_resultados"), workshopData), 8000, "Firebase AddDoc");
        console.log(`[Firebase] Resultado de ${workshopType} guardado con éxito. ID: ${docRef.id}`);
        docId = docRef.id;
        firebaseSuccess = true;
    } catch (e) {
        console.error("Error guardando el resultado del taller en Firebase: ", e);
        // Fallback a localStorage
        const backupKey = `backup_score_${workshopType}_${Date.now()}`;
        localStorage.setItem(backupKey, JSON.stringify(workshopData));
    }

    // Enviar correo automáticamente al administrador usando FormSubmit
    try {
        const emailMessage = `
Estudiante: ${studentName} (${uid})
Correo: ${studentEmail}
Examen: ${workshopType}
Puntaje: ${finalScore}/100
Aciertos: ${rawScore}/${totalQuestions}
Firebase ID: ${docId}
        `.trim();

        // Notificar en la mini-db de notificaciones
        try {
            await withTimeout(addDoc(collection(db, "mail_notifications"), {
                channel: "formsubmit",
                to: ADMIN_NOTIFICATION_EMAIL,
                subject: `Resultado: ${workshopType} - ${studentName}`,
                student: { name: studentName, email: studentEmail },
                createdAt: serverTimestamp(),
                status: "attempted"
            }), 3000, "mail_notifications");
        } catch (mErr) { console.warn("No se pudo registrar la notificación de mail en Firestore", mErr); }

        await withTimeout(fetch(`https://formsubmit.co/ajax/${ADMIN_NOTIFICATION_EMAIL}`, {
            method: "POST",
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: JSON.stringify({
                _subject: `Nuevo Resultado: ${workshopType} - ${studentName}`,
                _replyto: studentEmail,
                _captcha: 'false',
                mensaje: emailMessage,
                estudiante: studentName,
                puntaje: `${finalScore}/100`,
                aciertos: `${rawScore}/${totalQuestions}`,
                examen: workshopType
            })
        }), 5000, "FormSubmit Fetch");
        
        console.log("[Email] Correo enviado exitosamente.");
    } catch (emailError) {
        console.error("Error enviando el correo:", emailError);
    }

    return { success: true, score: finalScore, raw: rawScore, firebaseSuccess };
}
