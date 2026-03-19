/**
 * Educando866 Progress Manager
 * Tracks class and workshop completion.
 */

class ProgressManager {
    constructor() {
        this.storageKey = 'educando866_progress';
        this.progress = this.loadProgress();
    }

    loadProgress() {
        const saved = localStorage.getItem(this.storageKey);
        return saved ? JSON.parse(saved) : {
            completedClasses: [],
            completedWorkshops: [],
            lastUpdate: new Date().toISOString()
        };
    }

    saveProgress() {
        this.progress.lastUpdate = new Date().toISOString();
        localStorage.setItem(this.storageKey, JSON.stringify(this.progress));
        this.notifyUpdate();
    }

    markClassComplete(classNumber) {
        if (!this.progress.completedClasses.includes(classNumber)) {
            this.progress.completedClasses.push(classNumber);
            this.saveProgress();
        }
    }

    markClassIncomplete(classNumber) {
        this.progress.completedClasses = this.progress.completedClasses.filter(num => num !== classNumber);
        this.saveProgress();
    }

    isClassComplete(classNumber) {
        return this.progress.completedClasses.includes(classNumber);
    }

    markWorkshopComplete(workshopId) {
        if (!this.progress.completedWorkshops.includes(workshopId)) {
            this.progress.completedWorkshops.push(workshopId);
            this.saveProgress();
        }
    }

    isWorkshopComplete(workshopId) {
        return this.progress.completedWorkshops.includes(workshopId);
    }

    getCompletionPercentage() {
        const totalClasses = 10;
        const totalWorkshops = 2; // Logica and Lectura
        const completed = this.progress.completedClasses.length + this.progress.completedWorkshops.length;
        return Math.round((completed / (totalClasses + totalWorkshops)) * 100);
    }

    notifyUpdate() {
        window.dispatchEvent(new CustomEvent('educando866:progress_updated', {
            detail: this.progress
        }));
    }
}

export const progressManager = new ProgressManager();
window.progressManager = progressManager; // Global access for simple scripts
