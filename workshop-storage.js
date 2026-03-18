// workshop-storage.js
import { db } from "./firebase-config.js";
import { collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-firestore.js";

const ADMIN_NOTIFICATION_EMAIL = "henrytaborda866@pascualbravo.edu.co";

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
    const finalScore = ((rawScore / totalQuestions) * 100).toFixed(2);

    // Obtener datos del estudiante almacenados localmente
    const studentName = localStorage.getItem('vetprep_student_name') || 'Anónimo';
    const studentEmail = localStorage.getItem('vetprep_student_email') || 'N/A';
    
    // Almacenamiento del documento
    const workshopData = {
        student: {
            name: studentName,
            email: studentEmail
        },
        workshopType: workshopType,
        score: {
            raw: rawScore,
            totalQuestions: totalQuestions,
            final: parseFloat(finalScore)
        },
        createdAt: serverTimestamp(),
        deviceUserAgent: navigator.userAgent
    };

    let docId = 'N/A';
    let firebaseSuccess = false;

    // Firebase addDoc con timeout de 8 segundos para evitar que se quede pegado ("Guardando...")
    try {
        const addDocPromise = addDoc(collection(db, "talleres_resultados"), workshopData);
        const timeoutPromise = new Promise((_, reject) => setTimeout(() => reject(new Error("Timeout de Firebase")), 8000));
        
        const docRef = await Promise.race([addDocPromise, timeoutPromise]);
        console.log(`[Firebase] Resultado de ${workshopType} guardado con éxito. ID: ${docRef.id}`);
        docId = docRef.id;
        firebaseSuccess = true;
    } catch (e) {
        console.error("Error guardando el resultado del taller en Firebase: ", e);
        // Fallback a localStorage
        localStorage.setItem(`backup_score_${workshopType}_${Date.now()}`, JSON.stringify(workshopData));
    }

    // Enviar correo automáticamente al administrador usando FormSubmit (Fetch API)
    try {
        const emailMessage = `
Estudiante: ${studentName}
Correo: ${studentEmail}
Examen: ${workshopType}
Puntaje: ${finalScore}/100
Aciertos: ${rawScore}/${totalQuestions}
Firebase ID: ${docId}
        `.trim();

        await fetch(`https://formsubmit.co/ajax/${ADMIN_NOTIFICATION_EMAIL}`, {
            method: "POST",
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                _subject: `Nuevo Resultado: ${workshopType} - ${studentName}`,
                _replyto: studentEmail,
                mensaje: emailMessage,
                estudiante: studentName,
                correo_estudiante: studentEmail,
                puntaje: `${finalScore}/100`,
                aciertos: `${rawScore}/${totalQuestions}`,
                examen: workshopType
            })
        });
        console.log("[Email] Correo enviado exitosamente con FormSubmit.");
    } catch (emailError) {
        console.error("Error enviando el correo con FormSubmit:", emailError);
    }

    // Devolvemos success basado en si pasamos la ejecución (incluso si firebase falló, intentamos enviar el correo)
    // Para que la UI avance y no se quede pegada, siempre devolvemos un objeto
    return { success: true, score: finalScore, raw: rawScore, firebaseSuccess };
}
