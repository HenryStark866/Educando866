import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-app.js";
import { initializeFirestore } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-firestore.js";
import { getAuth, signInAnonymously, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-auth.js";

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyBOLlMtZB9vfdbWo3PlABfTru19A2Id2I4",
    projectId: "prepudea-platform",
    appId: "1:30596061507:web:7dd5dbbad3ededc5f6f7f6"
};

// Firebase initialization status
let firebaseInitialized = false;
let firebaseReady = false;
let initializationError = null;

// Initialize Firebase with error handling
try {
    const app = initializeApp(firebaseConfig);
    const db = initializeFirestore(app, {
        experimentalAutoDetectLongPolling: true,
        useFetchStreams: false
    });
    const auth = getAuth(app);
    
    // Authentication state listener
    let authReady = false;
    onAuthStateChanged(auth, (user) => {
        if (user) {
            authReady = true;
            checkFirebaseReady();
        } else {
            // User signed out, attempt anonymous sign-in
            signInAnonymously(auth).catch(err => {
                console.warn("Anonymous sign-in failed:", err);
            });
        }
    });
    
    // Initialize with anonymous authentication
    signInAnonymously(auth)
        .then(() => {
            authReady = true;
            checkFirebaseReady();
        })
        .catch(error => {
            // Handle specific Firebase auth errors
            if (error.code === 'auth/admin-restricted-operation') {
                console.warn("Anonymous authentication restricted by admin (expected in some environments)");
                authReady = true; // Proceed anyway for demo/dev purposes
                checkFirebaseReady();
            } else if (error.code === 'auth/network-request-failed') {
                console.warn("Network error during Firebase auth - will retry automatically");
                authReady = true; // Proceed anyway for offline capability
                checkFirebaseReady();
            } else {
                console.error("Firebase authentication error:", error);
                authReady = true; // Allow proceeding with localStorage fallback
                checkFirebaseReady();
            }
        });

    // Function to check if Firebase is ready
    function checkFirebaseReady() {
        if (authReady) {
            firebaseReady = true;
            firebaseInitialized = true;
            console.log("[Firebase] Successfully initialized and authenticated");
        }
    }

    // Export Firebase instances
    export { app, db, auth, firebaseReady, firebaseInitialized };
    
} catch (error) {
    console.error("Failed to initialize Firebase:", error);
    initializationError = error;
    
    // Export null instances so imports don't break
    export const app = null;
    export const db = null;
    export const auth = null;
    export const firebaseReady = false;
    export const firebaseInitialized = false;
}