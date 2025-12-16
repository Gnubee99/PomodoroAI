#!/usr/bin/env python3
"""
Pomodoro Timer Application
A web-based GUI Pomodoro timer with time tracking and statistics.
"""

from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime, date, timezone
from pathlib import Path
import threading
import time

app = Flask(__name__)

class PomodoroTimer:
    """Main Pomodoro Timer class with tracking capabilities."""
    
    DEFAULT_WORK_TIME = 25 * 60  # 25 minutes in seconds
    DEFAULT_BREAK_TIME = 5 * 60  # 5 minutes in seconds
    DATA_FILE = Path.home() / ".pomodoro_data.json"
    
    def __init__(self):
        """Initialize the Pomodoro timer."""
        self.data = self.load_data()
        self.timer_running = False
        self.remaining_seconds = 0
        self.session_type = None
        self.start_time = None
        self.duration = 0
        self.lock = threading.RLock()  # Use RLock to allow reentrant locking
    
    def load_data(self):
        """Load tracking data from file."""
        if self.DATA_FILE.exists():
            try:
                with open(self.DATA_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def save_data(self):
        """Save tracking data to file."""
        try:
            with open(self.DATA_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save data: {e}")
    
    def record_session(self, duration_seconds, session_type="work"):
        """Record a completed session."""
        if session_type not in ("work", "break"):
            raise ValueError(f"Invalid session_type: {session_type}. Must be 'work' or 'break'.")

        # Use UTC for consistent date storage across timezones
        today = datetime.now(timezone.utc).date().isoformat()

        if today not in self.data:
            self.data[today] = {
                "work_time": 0,
                "break_time": 0,
                "sessions": []
            }

        self.data[today][f"{session_type}_time"] += duration_seconds
        self.data[today]["sessions"].append({
            "type": session_type,
            "duration": duration_seconds,
            "completed_at": datetime.now(timezone.utc).isoformat()
        })

        self.save_data()
    
    def start_timer(self, duration_seconds, session_type="work"):
        """Start a new timer."""
        with self.lock:
            self.timer_running = True
            self.remaining_seconds = duration_seconds
            self.session_type = session_type
            self.start_time = time.time()
            self.duration = duration_seconds
    
    def stop_timer(self):
        """Stop the current timer."""
        with self.lock:
            if self.timer_running:
                elapsed = self.duration - self.remaining_seconds
                if elapsed >= 60:  # Record if at least 1 minute
                    self.record_session(elapsed, self.session_type)
            self.timer_running = False
            self.remaining_seconds = 0
            self.session_type = None
    
    def complete_timer(self):
        """Complete the current timer and record session."""
        with self.lock:
            if self.timer_running:
                self.record_session(self.duration, self.session_type)
                self.timer_running = False
                self.remaining_seconds = 0
                self.session_type = None
    
    def tick(self):
        """Update timer (call this periodically)."""
        with self.lock:
            if self.timer_running:
                elapsed = time.time() - self.start_time
                self.remaining_seconds = max(0, self.duration - int(elapsed))
                if self.remaining_seconds <= 0:
                    self.complete_timer()
                    return True  # Timer completed
        return False
    
    def get_status(self):
        """Get current timer status."""
        with self.lock:
            return {
                "running": self.timer_running,
                "remaining": self.remaining_seconds,
                "session_type": self.session_type,
                "duration": self.duration
            }
    
    def get_statistics(self, days=7):
        """Get statistics for recent days."""
        if not self.data:
            return []
        
        dates = sorted(self.data.keys(), reverse=True)[:days]
        stats = []
        
        for date_str in dates:
            day_data = self.data[date_str]
            stats.append({
                "date": date_str,
                "work_time": day_data["work_time"] // 60,
                "break_time": day_data["break_time"] // 60,
                "sessions": len(day_data["sessions"])
            })
        
        return stats
    
    def get_today_stats(self):
        """Get today's statistics."""
        # Use UTC for consistent date retrieval across timezones
        today = datetime.now(timezone.utc).date().isoformat()
        if today in self.data:
            day_data = self.data[today]
            return {
                "work_time": day_data["work_time"] // 60,
                "break_time": day_data["break_time"] // 60,
                "sessions": len(day_data["sessions"])
            }
        return {"work_time": 0, "break_time": 0, "sessions": 0}


# Global timer instance
timer = PomodoroTimer()

# Background thread to update timer
def timer_thread():
    """Background thread that updates the timer."""
    while True:
        timer.tick()
        time.sleep(1)

# Start background thread
thread = threading.Thread(target=timer_thread, daemon=True)
thread.start()


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/api/start', methods=['POST'])
def start():
    """Start a timer."""
    data = request.json
    duration = data.get('duration', timer.DEFAULT_WORK_TIME)
    session_type = data.get('type', 'work')
    timer.start_timer(duration, session_type)
    return jsonify({"success": True})


@app.route('/api/stop', methods=['POST'])
def stop():
    """Stop the timer."""
    timer.stop_timer()
    return jsonify({"success": True})


@app.route('/api/status')
def status():
    """Get timer status."""
    return jsonify(timer.get_status())


@app.route('/api/stats')
def stats():
    """Get statistics."""
    return jsonify({
        "today": timer.get_today_stats(),
        "history": timer.get_statistics()
    })


if __name__ == '__main__':
    print("\n🍅 PomodoroAI Timer - Web GUI")
    print("=" * 50)
    print("Opening browser at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50 + "\n")
    app.run(debug=False, host='0.0.0.0', port=5000)
