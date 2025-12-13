# PomodoroAI

A beautiful, web-based Pomodoro timer to help you stay focused and beat distractions.

## Features

- **Configurable Timers**: Customize work and break durations to fit your workflow
- **Default Settings**: 25-minute work sessions with 5-minute breaks
- **Visual Progress**: Real-time progress bar showing timer completion
- **Sound Notifications**: Pleasant 5-second audio notification when timers complete
- **Session Tracking**: Track the number of Pomodoros completed during your session
- **Browser Notifications**: Optional desktop notifications (requires permission)
- **Responsive Design**: Works on desktop and mobile devices
- **No Dependencies**: Pure HTML, CSS, and JavaScript

## Getting Started

### Quick Start

1. Open `index.html` in your web browser
2. Click the "Start" button to begin a work session
3. When the timer completes, you'll hear a notification sound
4. The timer automatically switches between work and break sessions

### Using a Local Server

For the best experience (especially for browser notifications), serve the files using a local web server:

```bash
# Using Python 3
python -m http.server 8000

# Using Python 2
python -m SimpleHTTPServer 8000

# Using Node.js (if you have npx)
npx http-server
```

Then open `http://localhost:8000` in your browser.

## How to Use

### Basic Controls

- **Start**: Begin the timer countdown
- **Pause**: Pause the current timer
- **Reset**: Reset the timer to the beginning of the current cycle

### Customizing Timer Durations

1. Scroll to the "Settings" section
2. Enter your desired work duration (1-60 minutes)
3. Enter your desired break duration (1-30 minutes)
4. Click "Apply Settings"

Your new settings will take effect immediately, and the timer will reset.

### Understanding the Display

- **Mode Indicator**: Shows whether you're in "Work Time" or "Break Time"
- **Timer Display**: Shows remaining time in MM:SS format
- **Progress Bar**: Visual indicator of timer completion
- **Pomodoros Today**: Number of work sessions completed
- **Current Cycle**: Shows if you're currently on work or break

## Features in Detail

### Sound Notifications

The timer plays a pleasant 5-second musical notification when each session completes. The sound uses Web Audio API to generate a chord progression without requiring external audio files.

### Session Tracking

The "Pomodoros Today" counter tracks how many work sessions you've completed while the application is open. This counter resets when you close the browser tab.

### Browser Notifications

The app can send desktop notifications when permitted. Click "Allow" when your browser asks for notification permissions to enable this feature.

## Technical Details

- **No Backend Required**: Everything runs in the browser
- **No External Dependencies**: Pure vanilla JavaScript
- **Modern Web APIs**: Uses Web Audio API for sound generation
- **Responsive Design**: CSS Grid and Flexbox for layout

## Browser Compatibility

Works in all modern browsers that support:
- ES6 JavaScript
- Web Audio API
- CSS Grid and Flexbox

Recommended browsers: Chrome, Firefox, Safari, Edge (latest versions)

## File Structure

```
PomodoroAI/
├── index.html    # Main HTML structure
├── style.css     # Styling and layout
├── app.js        # Timer logic and functionality
└── README.md     # This file
```

## Tips for Maximum Productivity

1. **Honor the Timer**: When the work timer is running, focus solely on your task
2. **Take Breaks**: Don't skip break periods - they help maintain focus
3. **Track Progress**: Use the Pomodoro counter to see your productivity
4. **Adjust as Needed**: Customize timer lengths to match your concentration span
5. **Minimize Distractions**: Close unnecessary tabs and apps during work sessions

## License

Open source - feel free to modify and use as you wish!

---

Built with focus 🎯
