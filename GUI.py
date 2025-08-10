import sys

from enum import Enum
from itertools import accumulate
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QRadioButton,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QFile, QTextStream

import resources  # do not remove this


class TimerState(Enum):
    """Enum for timer states to improve code clarity."""

    INITIAL = "initial"
    RUNNING = "running"
    PAUSED = "paused"
    FINISHED = "finished"


class WritingPhase:
    """Data class to encapsulate phase information."""

    def __init__(self, name: str, duration_minutes: int):
        self.name = name
        self.duration_minutes = duration_minutes


class IELTSTimer(QWidget):
    """
    Enhanced IELTS Writing timer with better structure and features.
    """

    # Signals for better decoupling
    phase_changed = pyqtSignal(int)
    timer_finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Configuration
        self.tasks = {
            "Task 1": [
                WritingPhase("Read the question and analyse charts", 3),
                WritingPhase("Write introduction and overview", 5),
                WritingPhase("Write body 1", 5),
                WritingPhase("Write body 2", 5),
                WritingPhase("Edit & Review", 2),
            ],
            "Task 2": [
                WritingPhase("Read the question and understand the task", 3),
                WritingPhase("Brainstorm Ideas", 4),
                WritingPhase("Plan Structure", 3),
                WritingPhase("Write Essay", 27),
                WritingPhase("Edit & Review", 3),
            ],
        }

        # Initialize these attributes first
        self.phases = None
        self.phase_end_times = []
        self.total_time = 0

        # State variables
        self.elapsed_seconds = 0
        self.current_phase = 0
        self.state = TimerState.INITIAL
        self.timer = QTimer(self)

        self._setup_ui()
        self._connect_signals()
        self._load_styles()

        # Initialize with default task (Task 1)
        self._on_mode_change()
        self._reset_to_initial_state()

    def _setup_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("IELTS Writing timer")
        self.setFixedSize(450, 450)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Mode selection
        mode_frame = QFrame()
        mode_layout = QHBoxLayout(mode_frame)

        self.mode_label = QLabel("Choose task:")
        self.mode_label.setObjectName("modeLabel")
        mode_layout.addWidget(self.mode_label)

        task_layout = QHBoxLayout()

        self.task1_button = QRadioButton("Task 1", mode_frame)
        self.task1_button.setAutoExclusive(True)
        self.task1_button.setChecked(True)
        self.task1_button.toggled.connect(self._on_mode_change)
        task_layout.addWidget(self.task1_button)

        self.task2_button = QRadioButton("Task 2", mode_frame)
        self.task2_button.setAutoExclusive(True)
        self.task2_button.toggled.connect(self._on_mode_change)
        task_layout.addWidget(self.task2_button)

        mode_layout.addLayout(task_layout)

        main_layout.addWidget(mode_frame)

        # Phase section
        phase_frame = QFrame()
        phase_layout = QVBoxLayout(phase_frame)

        self.phase_label = QLabel("Ready to Start!")
        self.phase_label.setObjectName("phaseLabel")
        self.phase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        phase_layout.addWidget(self.phase_label)

        self.duration_label = QLabel()
        self.duration_label.setObjectName("durationLabel")
        self.duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        phase_layout.addWidget(self.duration_label)

        main_layout.addWidget(phase_frame)

        # Time display
        self.time_label = QLabel("00:00")
        self.time_label.setObjectName("timeLabel")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.time_label)

        # Phase info
        self.phase_info_label = QLabel("")
        self.phase_info_label.setObjectName("phaseInfoLabel")
        self.phase_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.phase_info_label)

        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.start_pause_button = QPushButton("Start")
        self.start_pause_button.setObjectName("startButton")
        button_layout.addWidget(self.start_pause_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("resetButton")
        button_layout.addWidget(self.reset_button)

        main_layout.addLayout(button_layout)

        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 0)
        main_layout.setStretch(2, 1)
        main_layout.setStretch(3, 0)
        main_layout.setStretch(4, 0)

        self.setLayout(main_layout)

    def _connect_signals(self):
        """Connect signals to slots."""
        self.start_pause_button.clicked.connect(self._on_start_pause_clicked)
        self.reset_button.clicked.connect(self._reset_to_initial_state)
        self.timer.timeout.connect(self._on_timer_tick)
        self.phase_changed.connect(self._on_phase_changed)
        self.timer_finished.connect(self._on_timer_finished)

    def _load_styles(self):
        """Load styles from QSS resource file."""
        style_file = QFile(":/styles.qss")
        if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(style_file)
            self.setStyleSheet(stream.readAll())
            style_file.close()
        else:
            print("Warning: Could not open styles.qss")

    def _reset_to_initial_state(self):
        """Reset the timer to initial state."""
        self.timer.stop()
        self.elapsed_seconds = 0
        self.current_phase = 0
        self.state = TimerState.INITIAL

        self._update_display()
        self._update_ui_state()

    def _on_mode_change(self):
        """Handle mode change and calculate cumulative times."""
        mode = "Task 1" if self.task1_button.isChecked() else "Task 2"
        if mode in self.tasks:
            self.phases = self.tasks[mode]
            self.phase_end_times = list(
                accumulate(phase.duration_minutes for phase in self.phases)
            )
            self.total_time = self.phase_end_times[-1] if self.phase_end_times else 0

            # Reset to initial state when mode changes
            if hasattr(self, "state"):  # Check if object is fully initialized
                self._reset_to_initial_state()

    def _on_start_pause_clicked(self):
        """Handle start/pause button clicks."""
        if self.state == TimerState.INITIAL:
            self._start_timer()
        elif self.state == TimerState.RUNNING:
            self._pause_timer()
        elif self.state == TimerState.PAUSED:
            self._resume_timer()
        elif self.state == TimerState.FINISHED:
            self._reset_to_initial_state()

    def _start_timer(self):
        """Start the timer."""
        self.state = TimerState.RUNNING
        self.timer.start(1000)  # Update every second
        self._update_ui_state()

    def _pause_timer(self):
        """Pause the timer."""
        self.state = TimerState.PAUSED
        self.timer.stop()
        self._update_ui_state()

    def _resume_timer(self):
        """Resume the timer."""
        self.state = TimerState.RUNNING
        self.timer.start(1000)
        self._update_ui_state()

    def _on_timer_tick(self):
        """Handle timer tick (every second)."""
        self.elapsed_seconds += 1
        self._update_display()
        self._check_phase_transition()

        # Check if timer is finished
        if self.total_time > 0 and self.elapsed_seconds >= self.total_time * 60:
            self.timer_finished.emit()

    def _check_phase_transition(self):
        """Check if we should transition to the next phase."""
        if not self.phases or not self.phase_end_times:
            return

        elapsed_minutes = self.elapsed_seconds // 60

        # Find current phase based on elapsed time
        new_phase = 0
        for i, end_time in enumerate(self.phase_end_times):
            if elapsed_minutes < end_time:
                new_phase = i
                break
        else:
            new_phase = len(self.phases) - 1  # Last phase

        if new_phase != self.current_phase:
            self.current_phase = new_phase
            self.phase_changed.emit(self.current_phase)

    def _on_phase_changed(self, phase_index):
        """Handle phase change."""
        if self.phases and 0 <= phase_index < len(self.phases):
            self._update_display()

    def _on_timer_finished(self):
        """Handle timer completion."""
        QApplication.beep()
        self.state = TimerState.FINISHED
        self.timer.stop()
        self._update_display()
        self._update_ui_state()

    def _update_display(self):
        """Update all display elements."""
        # Update time display
        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

        # Update phase information
        if self.state == TimerState.FINISHED:
            self.phase_label.setText("🎉 Time Complete!")
            self.duration_label.setText(None)
            self.phase_info_label.setText("Great job! Review your work.")
        elif self.state == TimerState.INITIAL:
            self.phase_label.setText("Ready to Start!")
            self.duration_label.setText(None)
            self.phase_info_label.setText(f"Total time: {self.total_time} minutes")
        else:
            if self.phases and 0 <= self.current_phase < len(self.phases):
                current_phase = self.phases[self.current_phase]
                self.phase_label.setText(
                    f"Phase {self.current_phase + 1}: {current_phase.name}"
                )
                self.duration_label.setText(f"{current_phase.duration_minutes} minutes")

                # Calculate remaining time
                if self.total_time > 0:
                    remaining = self.total_time * 60 - self.elapsed_seconds
                    remaining_minutes = max(0, remaining) // 60
                    remaining_seconds = max(0, remaining) % 60

                    self.phase_info_label.setText(
                        f"Time remaining: {remaining_minutes:02d}:{remaining_seconds:02d}"
                    )
                else:
                    self.phase_info_label.setText("Time remaining: 00:00")

    def _update_ui_state(self):
        """Update button states based on current timer state."""
        state_config = {
            TimerState.INITIAL: {
                "mode_selection_enabled": True,
                "start_button_text": "Start",
                "start_button_enabled": True,
                "reset_button_enabled": False,
            },
            TimerState.RUNNING: {
                "mode_selection_enabled": False,
                "start_button_text": "Pause",
                "start_button_enabled": True,
                "reset_button_enabled": True,
            },
            TimerState.PAUSED: {
                "mode_selection_enabled": False,
                "start_button_text": "Resume",
                "start_button_enabled": True,
                "reset_button_enabled": True,
            },
            TimerState.FINISHED: {
                "mode_selection_enabled": True,
                "start_button_text": "Restart",
                "start_button_enabled": True,
                "reset_button_enabled": True,
            },
        }

        config = state_config[self.state]

        self.task1_button.setEnabled(config["mode_selection_enabled"])
        self.task2_button.setEnabled(config["mode_selection_enabled"])

        self.start_pause_button.setText(config["start_button_text"])
        self.start_pause_button.setEnabled(config["start_button_enabled"])
        self.reset_button.setEnabled(config["reset_button_enabled"])

        # Update button styling based on state
        if self.state == TimerState.RUNNING:
            self.start_pause_button.setObjectName("pauseButton")
        else:
            self.start_pause_button.setObjectName("startButton")

        # Refresh stylesheet to apply new object name
        style = self.start_pause_button.style()
        if style:
            style.unpolish(self.start_pause_button)
            style.polish(self.start_pause_button)

    def get_progress_percentage(self):
        """Get current progress as percentage."""
        return (
            (self.elapsed_seconds / (self.total_time * 60)) * 100
            if self.total_time > 0
            else 0
        )


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("IELTS Writing Timer")
    app.setWindowIcon(QIcon(":/icon.ico"))

    window = IELTSTimer()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
