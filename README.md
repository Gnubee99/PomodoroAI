# PomodoroAI

What will AI come up with for a Pomodoro timer to keep me focused on distractions?

A command-line Pomodoro timer application with time tracking and statistics.

## Features

- 🍅 **Default 25-minute work timer** - Classic Pomodoro technique
- ⏰ **5-minute break timer** - Take regular breaks
- ⚙️ **Custom timer durations** - Set your own work and break times
- 📊 **Daily time tracking** - Keep a running tally of your focused time
- 📈 **Visual statistics** - See your productivity with charts
- 💾 **Persistent data** - Track your progress across sessions

## Installation

This application requires Python 3.6 or higher and uses only standard library modules.

```bash
# Clone the repository
git clone https://github.com/Gnubee99/PomodoroAI.git
cd PomodoroAI

# Make the script executable (optional)
chmod +x pomodoro.py
```

## Usage

Run the Pomodoro timer:

```bash
python3 pomodoro.py
```

### Menu Options

1. **Start work session (25 minutes)** - Begin a standard Pomodoro work session
2. **Start break (5 minutes)** - Take a 5-minute break
3. **Custom work timer** - Set a custom duration for work
4. **Custom break timer** - Set a custom duration for break
5. **View statistics** - See your productivity stats and charts
6. **Exit** - Close the application

### Features in Detail

#### Timer Controls
- The timer displays a live countdown
- Press `Ctrl+C` to stop the timer early
- Sessions longer than 1 minute can be optionally recorded when stopped early
- Completed sessions are automatically recorded

#### Statistics
- View daily breakdown of work and break time
- Visual bar charts showing productivity
- Track sessions over multiple days
- See today's progress and weekly summaries

#### Data Storage
- All session data is stored in `~/.pomodoro_data.json`
- Data persists across application restarts
- Privacy-focused: all data stays on your local machine

## Example Session

```
🍅 Welcome to PomodoroAI Timer!

==================================================
POMODORO TIMER
==================================================
1. Start work session (25 minutes)
2. Start break (5 minutes)
3. Custom work timer
4. Custom break timer
5. View statistics
6. Exit
==================================================

Select an option (1-6): 1

==================================================
Starting work timer: 25:00
==================================================
Press Ctrl+C to stop the timer
⏱  Time remaining: 24:32
```

## Tips for Maximum Productivity

1. **Eliminate distractions** before starting a session
2. **Use breaks wisely** - stand up, stretch, hydrate
3. **Review statistics** regularly to understand your patterns
4. **Adjust custom times** to find what works best for you
5. **Celebrate consistency** - building the habit is key!

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
