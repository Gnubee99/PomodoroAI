// PomodoroAI - Timer Application
class PomodoroTimer {
    constructor() {
        // DOM Elements
        this.timeDisplay = document.getElementById('timeDisplay');
        this.modeIndicator = document.getElementById('modeIndicator');
        this.startBtn = document.getElementById('startBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.pomodoroCount = document.getElementById('pomodoroCount');
        this.cycleType = document.getElementById('cycleType');
        this.workDurationInput = document.getElementById('workDuration');
        this.breakDurationInput = document.getElementById('breakDuration');
        this.applySettingsBtn = document.getElementById('applySettings');
        this.progressFill = document.getElementById('progressFill');

        // Timer state
        this.workDuration = 25 * 60; // 25 minutes in seconds
        this.breakDuration = 5 * 60; // 5 minutes in seconds
        this.timeRemaining = this.workDuration;
        this.totalTime = this.workDuration;
        this.isRunning = false;
        this.isWorkMode = true;
        this.timerInterval = null;
        this.completedPomodoros = 0;

        // Audio context for notifications
        this.audioContext = null;

        // Initialize
        this.init();
    }

    init() {
        // Event listeners
        this.startBtn.addEventListener('click', () => this.start());
        this.pauseBtn.addEventListener('click', () => this.pause());
        this.resetBtn.addEventListener('click', () => this.reset());
        this.applySettingsBtn.addEventListener('click', () => this.applySettings());

        // Initialize audio context on first user interaction
        document.addEventListener('click', () => {
            if (!this.audioContext) {
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }
        }, { once: true });

        this.updateDisplay();
        this.updateProgress();
    }

    start() {
        if (!this.isRunning) {
            this.isRunning = true;
            this.startBtn.disabled = true;
            this.pauseBtn.disabled = false;

            this.timerInterval = setInterval(() => {
                this.tick();
            }, 1000);
        }
    }

    pause() {
        if (this.isRunning) {
            this.isRunning = false;
            this.startBtn.disabled = false;
            this.pauseBtn.disabled = true;
            clearInterval(this.timerInterval);
        }
    }

    reset() {
        this.pause();
        this.timeRemaining = this.isWorkMode ? this.workDuration : this.breakDuration;
        this.totalTime = this.timeRemaining;
        this.updateDisplay();
        this.updateProgress();
    }

    tick() {
        this.timeRemaining--;
        this.updateDisplay();
        this.updateProgress();

        if (this.timeRemaining <= 0) {
            this.timerComplete();
        }
    }

    timerComplete() {
        this.pause();
        this.playNotification();

        // If work session completed, increment pomodoro count
        if (this.isWorkMode) {
            this.completedPomodoros++;
            this.pomodoroCount.textContent = this.completedPomodoros;
        }

        // Switch mode
        this.isWorkMode = !this.isWorkMode;
        this.timeRemaining = this.isWorkMode ? this.workDuration : this.breakDuration;
        this.totalTime = this.timeRemaining;

        // Update UI
        this.updateModeIndicator();
        this.updateDisplay();
        this.updateProgress();

        // Show notification
        this.showNotification();
    }

    updateDisplay() {
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        this.timeDisplay.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }

    updateProgress() {
        const progress = ((this.totalTime - this.timeRemaining) / this.totalTime) * 100;
        this.progressFill.style.width = `${progress}%`;
    }

    updateModeIndicator() {
        if (this.isWorkMode) {
            this.modeIndicator.textContent = 'Work Time';
            this.modeIndicator.style.color = '#667eea';
            this.cycleType.textContent = 'Work';
        } else {
            this.modeIndicator.textContent = 'Break Time';
            this.modeIndicator.style.color = '#48bb78';
            this.cycleType.textContent = 'Break';
        }
        this.modeIndicator.classList.add('mode-change');
        setTimeout(() => {
            this.modeIndicator.classList.remove('mode-change');
        }, 500);
    }

    applySettings() {
        const workMinutes = parseInt(this.workDurationInput.value);
        const breakMinutes = parseInt(this.breakDurationInput.value);

        if (workMinutes > 0 && breakMinutes > 0) {
            this.workDuration = workMinutes * 60;
            this.breakDuration = breakMinutes * 60;

            // Reset timer with new settings
            this.reset();

            // Show feedback
            this.applySettingsBtn.textContent = 'Applied! ✓';
            setTimeout(() => {
                this.applySettingsBtn.textContent = 'Apply Settings';
            }, 2000);
        }
    }

    playNotification() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }

        // Create a pleasant notification sound (about 5 seconds)
        const now = this.audioContext.currentTime;

        // Create oscillators for a chord progression
        const frequencies = [
            [523.25, 659.25, 783.99], // C major chord
            [587.33, 739.99, 880.00], // D major chord
            [659.25, 830.61, 987.77], // E major chord
        ];

        frequencies.forEach((chord, index) => {
            const startTime = now + (index * 1.5);

            chord.forEach((freq, i) => {
                const oscillator = this.audioContext.createOscillator();
                const gainNode = this.audioContext.createGain();

                oscillator.connect(gainNode);
                gainNode.connect(this.audioContext.destination);

                oscillator.frequency.value = freq;
                oscillator.type = 'sine';

                // Envelope
                const attackTime = 0.1;
                const decayTime = 0.3;
                const sustainLevel = 0.15;
                const releaseTime = 0.5;

                gainNode.gain.setValueAtTime(0, startTime);
                gainNode.gain.linearRampToValueAtTime(0.3, startTime + attackTime);
                gainNode.gain.linearRampToValueAtTime(sustainLevel, startTime + attackTime + decayTime);
                gainNode.gain.setValueAtTime(sustainLevel, startTime + 1.0);
                gainNode.gain.linearRampToValueAtTime(0, startTime + 1.0 + releaseTime);

                oscillator.start(startTime);
                oscillator.stop(startTime + 1.0 + releaseTime);
            });
        });
    }

    showNotification() {
        // Browser notification if permitted
        if ('Notification' in window && Notification.permission === 'granted') {
            const message = this.isWorkMode
                ? '🍅 Break time is over! Time to focus!'
                : '🎉 Great work! Time for a break!';

            new Notification('PomodoroAI', {
                body: message,
                icon: '🍅'
            });
        } else if ('Notification' in window && Notification.permission !== 'denied') {
            Notification.requestPermission();
        }
    }
}

// Initialize the timer when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const timer = new PomodoroTimer();

    // Request notification permission
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
});
