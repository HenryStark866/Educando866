import { db } from "./firebase-config.js";
import { addDoc, collection, serverTimestamp } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-firestore.js";

const ADMIN_NOTIFICATION_EMAIL = "henrytaborda866@pascualbravo.edu.co";

const studentName = localStorage.getItem("vetprep_student_name") || "Estudiante";
const studentEmail = localStorage.getItem("vetprep_student_email") || "N/A";

async function sendAdminEmail(subject, lines) {
    try {
        await fetch(`https://formsubmit.co/ajax/${ADMIN_NOTIFICATION_EMAIL}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({
                _subject: subject,
                _replyto: studentEmail !== "N/A" ? studentEmail : undefined,
                estudiante: studentName,
                correo_estudiante: studentEmail,
                mensaje: lines.join("\n")
            })
        });
    } catch (error) {
        console.error("No se pudo enviar notificacion por correo:", error);
    }
}

async function logCourseEvent(eventType, details = {}) {
    const eventData = {
        eventType,
        student: {
            name: studentName,
            email: studentEmail
        },
        details,
        createdAt: serverTimestamp(),
        userAgent: navigator.userAgent,
        path: window.location.pathname
    };

    try {
        await addDoc(collection(db, "course_activity"), eventData);
    } catch (error) {
        console.error("No se pudo guardar evento en Firestore:", error);
    }
}

const sessionAccessKey = "vetprep_course_access_logged";
if (!sessionStorage.getItem(sessionAccessKey)) {
    sessionStorage.setItem(sessionAccessKey, "true");
    logCourseEvent("course_access", {
        message: "Ingreso al aula virtual"
    });
    sendAdminEmail("Nuevo ingreso al aula virtual", [
        `Estudiante: ${studentName}`,
        `Correo: ${studentEmail}`,
        "Evento: Ingreso al aula virtual"
    ]);
}

window.addEventListener("vetprep:pdf_open", (event) => {
    const title = event.detail?.title || "Material PDF";
    const href = event.detail?.href || "N/A";

    logCourseEvent("pdf_open", {
        title,
        href
    });

    sendAdminEmail("Apertura de PDF en aula virtual", [
        `Estudiante: ${studentName}`,
        `Correo: ${studentEmail}`,
        `Evento: Apertura de PDF`,
        `Material: ${title}`,
        `Archivo: ${href}`
    ]);
});

window.addEventListener("vetprep:class_change", (event) => {
    const classNumber = event.detail?.classNumber || "N/A";
    const title = event.detail?.title || "Clase";
    const module = event.detail?.module || "General";

    logCourseEvent("class_change", {
        classNumber,
        title,
        module
    });
});
