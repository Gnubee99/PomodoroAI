# PomodoroAI

What will AI come up with for a Pomodoro timer to keep me focused on distractions?

A beautiful web-based GUI Pomodoro timer with time tracking and statistics.

## Features

- 🍅 **Default 25-minute work timer** - Classic Pomodoro technique
- ⏰ **5-minute break timer** - Take regular breaks
- ⚙️ **Custom timer durations** - Set your own work and break times
- 📊 **Daily time tracking** - Keep a running tally of your focused time
- 📈 **Visual statistics** - See your productivity with beautiful charts
- 💾 **Persistent data** - Track your progress across sessions
- 🎨 **Modern GUI** - Beautiful, responsive web interface
- 🔔 **Audio notifications** - Get notified when sessions complete

## Installation

This application requires Python 3.6 or higher and Flask.

```bash
# Clone the repository
git clone https://github.com/Gnubee99/PomodoroAI.git
cd PomodoroAI

# Install dependencies
pip install -r requirements.txt
```

## Docker Installation (Alternative)

If you prefer using Docker, you can run PomodoroAI in a container:

### Option 1: Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/Gnubee99/PomodoroAI.git
cd PomodoroAI

# Start the container
docker-compose up -d

# View logs (optional)
docker-compose logs -f

# Stop the container
docker-compose down
```

### Option 2: Using Docker directly

```bash
# Build the image
docker build -t pomodoro-ai .

# Run the container with data persistence
docker run -d \
  --name pomodoro-ai \
  -p 5000:5000 \
  -v pomodoro-data:/data \
  -e HOME=/data \
  pomodoro-ai

# View logs
docker logs -f pomodoro-ai

# Stop and remove the container
docker stop pomodoro-ai
docker rm pomodoro-ai
```

### Docker Notes
- Data persists in a Docker volume named `pomodoro-data`
- The container automatically restarts unless stopped manually
- Access the app at **http://localhost:5000** just like the native installation
- To remove all data: `docker volume rm pomodoro-data`

## Usage

Start the Pomodoro timer web server:

```bash
python3 pomodoro.py
```

Then open your browser to: **http://localhost:5000**

### GUI Features

The web interface provides:

1. **Work Session Button** - Start a 25-minute work session with one click
2. **Break Button** - Start a 5-minute break session
3. **Custom Timers** - Set custom durations for work or breaks (1-120 minutes)
4. **Live Timer Display** - Large, easy-to-read countdown timer
5. **Stop Button** - Pause or stop the current session
6. **Today's Progress** - Real-time stats showing work time, break time, and session count
7. **Recent Activity** - Visual history of your sessions with bar charts

### Features in Detail

#### Timer Controls
- Click any button to start a timer instantly
- The timer updates in real-time with a smooth countdown
- Visual indicators show whether you're in a work or break session
- Stop button allows you to end sessions early (records if >1 minute)
- Audio notification plays when a session completes

#### Statistics
- Today's progress displayed prominently with three stat cards
- Work time, break time, and session counts updated live
- Recent activity shows up to 7 days of history
- Visual bar charts represent productivity (one bar per 25 minutes)
- All stats persist across browser sessions

#### Data Storage
- All session data is stored in `~/.pomodoro_data.json`
- Data persists across application restarts
- Privacy-focused: all data stays on your local machine
- Accessible from any browser on your network

## Tips for Maximum Productivity

1. **Eliminate distractions** before starting a session
2. **Use breaks wisely** - stand up, stretch, hydrate
3. **Review statistics** regularly to understand your patterns
4. **Adjust custom times** to find what works best for you
5. **Celebrate consistency** - building the habit is key!
6. **Keep the browser tab visible** - The timer updates in real-time

## Technical Details

- **Backend**: Flask web server (Python)
- **Frontend**: HTML5, CSS3, JavaScript (no frameworks needed)
- **Data**: JSON file storage
- **Port**: Runs on port 5000 by default
- **Network**: Accessible at http://localhost:5000 or http://[your-ip]:5000

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
