#!/usr/bin/env python3
"""
Pomodoro Timer Application
A command-line Pomodoro timer with time tracking and statistics.
"""

import time
import sys
import json
from datetime import datetime, date
from pathlib import Path


class PomodoroTimer:
    """Main Pomodoro Timer class with tracking capabilities."""
    
    DEFAULT_WORK_TIME = 25 * 60  # 25 minutes in seconds
    DEFAULT_BREAK_TIME = 5 * 60  # 5 minutes in seconds
    DATA_FILE = Path.home() / ".pomodoro_data.json"
    
    def __init__(self):
        """Initialize the Pomodoro timer."""
        self.data = self.load_data()
    
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
            print(f"Warning: Could not save data: {e}", file=sys.stderr)
    
    def record_session(self, duration_seconds, session_type="work"):
        """Record a completed session."""
        # Validate session type
        if session_type not in ("work", "break"):
            raise ValueError(f"Invalid session_type: {session_type}. Must be 'work' or 'break'.")
        
        today = date.today().isoformat()
        
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
            "completed_at": datetime.now().isoformat()
        })
        
        self.save_data()
    
    def format_time(self, seconds):
        """Format seconds as MM:SS."""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
    
    def run_timer(self, duration_seconds, session_type="work"):
        """Run a countdown timer."""
        print(f"\n{'='*50}")
        print(f"Starting {session_type} timer: {self.format_time(duration_seconds)}")
        print(f"{'='*50}")
        print("Press Ctrl+C to stop the timer")
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        try:
            while True:
                current_time = time.time()
                remaining = int(end_time - current_time)
                
                if remaining <= 0:
                    break
                
                # Display timer
                sys.stdout.write(f"\r⏱  Time remaining: {self.format_time(remaining)} ")
                sys.stdout.flush()
                time.sleep(0.5)
            
            # Timer completed
            elapsed = int(time.time() - start_time)
            print(f"\n\n✓ {session_type.capitalize()} session completed!")
            print(f"Duration: {self.format_time(elapsed)}")
            self.record_session(elapsed, session_type)
            
            # Play a bell sound (using system bell)
            print("\a" * 3)
            
            return True
            
        except KeyboardInterrupt:
            elapsed = int(time.time() - start_time)
            print(f"\n\n⚠ Timer stopped early")
            print(f"Time elapsed: {self.format_time(elapsed)}")
            
            if elapsed >= 60:  # Only record if at least 1 minute
                response = input("Record this session? (y/n): ").strip().lower()
                if response == 'y':
                    self.record_session(elapsed, session_type)
                    print("✓ Session recorded")
            
            return False
    
    def show_stats(self, days=7):
        """Display statistics for recent days."""
        print(f"\n{'='*50}")
        print("POMODORO STATISTICS")
        print(f"{'='*50}\n")
        
        if not self.data:
            print("No sessions recorded yet.")
            return
        
        # Get dates sorted in reverse order
        dates = sorted(self.data.keys(), reverse=True)[:days]
        
        total_work = 0
        total_break = 0
        
        for date_str in dates:
            day_data = self.data[date_str]
            work_mins = day_data["work_time"] // 60
            break_mins = day_data["break_time"] // 60
            session_count = len(day_data["sessions"])
            
            total_work += day_data["work_time"]
            total_break += day_data["break_time"]
            
            # Create visual bar chart
            work_blocks = "█" * (work_mins // 25)
            
            print(f"{date_str}")
            print(f"  Work:  {work_mins:3d} min {work_blocks}")
            print(f"  Break: {break_mins:3d} min")
            print(f"  Sessions: {session_count}")
            print()
        
        # Today's stats
        today = date.today().isoformat()
        if today in self.data:
            print(f"{'='*50}")
            print(f"TODAY'S PROGRESS")
            print(f"{'='*50}")
            today_work = self.data[today]["work_time"] // 60
            today_break = self.data[today]["break_time"] // 60
            print(f"Work time:  {today_work} minutes")
            print(f"Break time: {today_break} minutes")
            print(f"Sessions:   {len(self.data[today]['sessions'])}")
        
        # Overall stats
        print(f"\n{'='*50}")
        print(f"SUMMARY (Last {len(dates)} days)")
        print(f"{'='*50}")
        print(f"Total work time:  {total_work // 60} minutes ({total_work // 3600:.1f} hours)")
        print(f"Total break time: {total_break // 60} minutes")
        print()


def print_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("POMODORO TIMER")
    print("="*50)
    print("1. Start work session (25 minutes)")
    print("2. Start break (5 minutes)")
    print("3. Custom work timer")
    print("4. Custom break timer")
    print("5. View statistics")
    print("6. Exit")
    print("="*50)


def get_custom_time():
    """Get custom time from user."""
    while True:
        try:
            minutes = int(input("Enter duration in minutes: "))
            if minutes > 0:
                return minutes * 60
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")


def main():
    """Main application entry point."""
    timer = PomodoroTimer()
    
    print("\n🍅 Welcome to PomodoroAI Timer!")
    
    while True:
        print_menu()
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == '1':
            timer.run_timer(timer.DEFAULT_WORK_TIME, "work")
        
        elif choice == '2':
            timer.run_timer(timer.DEFAULT_BREAK_TIME, "break")
        
        elif choice == '3':
            duration = get_custom_time()
            timer.run_timer(duration, "work")
        
        elif choice == '4':
            duration = get_custom_time()
            timer.run_timer(duration, "break")
        
        elif choice == '5':
            timer.show_stats()
        
        elif choice == '6':
            print("\n👋 Thanks for using PomodoroAI Timer!")
            print("Stay focused and productive!\n")
            sys.exit(0)
        
        else:
            print("\n⚠ Invalid option. Please select 1-6.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
