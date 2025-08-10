# IELTS Writing Timer

A PyQt6-based desktop application designed to help IELTS test takers manage their time effectively during writing tasks. The application provides structured timing phases for both Task 1 and Task 2, helping users practice proper time allocation for each section of the IELTS Writing test.

## Features

- **Dual Task Support**: Separate timing structures for IELTS Writing Task 1 (20 minutes) and Task 2 (40 minutes)
- **Phase-Based Timing**: Each task is broken down into specific phases with recommended time allocations
- **Visual Feedback**: Clear display of current phase, elapsed time, and remaining time
- **Timer Controls**: Start, pause, resume, and reset functionality
- **Audio Notification**: Sound alert when time is complete

## Task Structure

### Task 1 (20 minutes total)
1. **Read the question and analyse charts** - 3 minutes
2. **Write introduction and overview** - 5 minutes  
3. **Write body 1** - 5 minutes
4. **Write body 2** - 5 minutes
5. **Edit & Review** - 2 minutes

### Task 2 (40 minutes total)
1. **Read the question and understand the task** - 3 minutes
2. **Brainstorm Ideas** - 4 minutes
3. **Plan Structure** - 3 minutes
4. **Write Essay** - 27 minutes
5. **Edit & Review** - 3 minutes

## Requirements

- Python 3.7 or higher
- PyQt6
- Additional resource files:
  - `resources.qrc` (XML resource structure)
  - `resources.py` (compiled Qt resources)
  - `styles.qss` (stylesheet)
  - `icon.ico` (application icon)

## Installation

1. **Clone or download the application files**:
   ```bash
   git clone <repository-url>
   cd IELTS-Writing-Timer
   ```

2. **Install required dependencies**:
   ```bash
   pip install PyQt6
   ```

3. **Ensure resource files are present**:
   - Make sure `resources.py`, `styles.qss`, and `icon.ico` are in the same directory as `GUI.py`

## Usage

### Running the Application

```bash
python GUI.py
```

### Using the Timer

1. **Select Task Type**: Choose between Task 1 (20 min) or Task 2 (40 min) using the radio buttons
2. **Start Timer**: Click the "Start" button to begin timing
3. **Monitor Progress**: 
   - Current phase and its duration are displayed at the top
   - Elapsed time is shown in the center
   - Remaining time is displayed at the bottom
4. **Control Timer**:
   - **Pause**: Click "Pause" to temporarily stop the Timer
   - **Resume**: Click "Resume" to continue from where you paused
   - **Reset**: Click "Reset" to return to the initial state

### Timer States

- **Initial**: Ready to start, task selection available
- **Running**: Timer is active, shows current phase and remaining time
- **Paused**: Timer is temporarily stopped, can be resumed
- **Finished**: All phases completed, audio notification played

## File Structure

```
IELTS-Writing-Timer/
├── GUI.py              # Main application file
├── resources.py        # Compiled Qt resource file
├── resources.qrc       # XML file containing the resources (not used in the app, only for reference)
├── styles.qss          # Application stylesheet
├── icon.ico            # Application icon
└── README.md           # This file
```

## Features in Detail

### Phase Management
The application automatically transitions between phases based on the recommended time allocations. Each phase is clearly labeled with its purpose and duration.

### Time Tracking
- Real-time display of elapsed time in MM:SS format
- Calculation and display of remaining time for the entire task
- Progress tracking through all phases

### User Interface
- **Task Selection**: Radio buttons for easy switching between Task 1 and Task 2
- **Phase Information**: Clear display of current phase name and duration
- **Time Display**: Large, easy-to-read timer in the center
- **Control Buttons**: Intuitive start/pause/reset controls
- **Status Updates**: Dynamic button text and state management

### Accessibility
- Keyboard navigation support
- Clear visual hierarchy
- Audio notification for completion
- Responsive button states

## Customization

### Modifying Phase Durations
To adjust the time allocations for each phase, edit the `tasks` dictionary in the `__init__` method:

```python
self.tasks = {
    "Task 1": [
        WritingPhase("Read the question and analyse charts", 3),
        # Modify duration (in minutes) as needed
    ],
    "Task 2": [
        # Add, remove, or modify phases as desired
    ]
}
```

### Styling
The application uses Qt stylesheets loaded from `styles.qss`. You can customize the appearance by modifying this file.

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'PyQt6'**
   - Install PyQt6: `pip install PyQt6`

2. **Warning: Could not open styles.qss**
   - Ensure the `styles.qss` file is in the same directory as `GUI.py`
   - Check that the resource compilation was successful

3. **Application doesn't start**
   - Verify Python version (3.7+ required)
   - Check that all resource files are present

### Resource Files Missing
If resource files are missing, the application will still run but with reduced functionality:
- No custom styling (falls back to system default)
- No application icon
- Basic functionality remains intact

## Development

### Architecture
The application follows object-oriented principles with clear separation of concerns:

- **TimerState**: Enum for managing application states
- **WritingPhase**: Data class for phase information
- **IELTSTimer**: Main widget class with signal-slot architecture

### Key Components
- State management using enums
- Signal-slot pattern for decoupled communication
- Modular phase configuration
- Responsive UI updates


## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests to improve the application.

## Support

For questions or support, please open an issue in the project repository.