/**
 * Educando866 / PrepUdeA - Firebase Configuration
 * Proyecto: prepudea-platform
 * Provee: db (Firestore), auth (Firebase Authentication), app
 */

import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-app.js";
import { getFirestore, doc, getDoc, setDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-firestore.js";
import {
    getAuth,
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    onAuthStateChanged,
    signOut
} from "https://www.gstatic.com/firebasejs/11.0.0/firebase-auth.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-analytics.js";

const firebaseConfig = {
    apiKey: "AIzaSyBOLlMtZB9vfdbWo3PlABfTru19A2Id2I4",
    authDomain: "prepudea-platform.firebaseapp.com",
    databaseURL: "https://prepudea-platform-default-rtdb.firebaseio.com",
    projectId: "prepudea-platform",
    storageBucket: "prepudea-platform.firebasestorage.app",
    messagingSenderId: "30596061507",
    appId: "1:30596061507:web:7dd5dbbad3ededc5f6f7f6",
    measurementId: "G-Y19TSL20GR"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app, "prep-curso-uni");
const auth = getAuth(app);
const analytics = getAnalytics(app);

/**
 * Crear perfil del estudiante en Firestore al registrarse.
 * @param {string} uid - UID de Firebase Auth
 * @param {string} nombre - Nombre completo
 * @param {string} email - Correo electrónico
 * @param {string} plan - Plan de acceso (ej. 'general')
 */
async function crearPerfilEstudiante(uid, nombre, email, plan = 'general') {
    const ref = doc(db, 'estudiantes', uid);
    const snap = await getDoc(ref);
    if (!snap.exists()) {
        await setDoc(ref, {
            nombre,
            email,
            plan,
            pago_verificado: false,   // El admin lo activa manualmente en Firestore Console
            curso_completado: false,
            clases_vistas: [],
            quiz_scores: {},
            fecha_registro: serverTimestamp()
        });
    }
}

/**
 * Verifica si el usuario tiene pago verificado.
 * @param {string} uid
 * @returns {Promise<boolean>}
 */
async function verificarPago(uid) {
    const ref = doc(db, 'estudiantes', uid);
    const snap = await getDoc(ref);
    if (snap.exists()) {
        return snap.data().pago_verificado === true;
    }
    return false;
}

export { app, db, auth, analytics, crearPerfilEstudiante, verificarPago, onAuthStateChanged, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, doc, getDoc, setDoc, serverTimestamp };
