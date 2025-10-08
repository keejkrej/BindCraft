"""
Main Window for BindCraft GUI Demo
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTabWidget, QPushButton, QLabel, QTextEdit, QProgressBar
)
from PySide6.QtCore import Qt
from config_panel import ConfigPanel
from results_panel import ResultsPanel
from mock_worker import MockWorker


class MainWindow(QMainWindow):
    """Main application window for BindCraft GUI."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BindCraft - Binder Design Pipeline (Demo)")
        self.setGeometry(100, 100, 1400, 900)

        self.worker = None
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Main splitter
        splitter = QSplitter(Qt.Horizontal)

        # Left: Configuration Panel
        self.config_panel = ConfigPanel()
        splitter.addWidget(self.config_panel)

        # Right: Run Management and Results
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Run Management Section
        run_section = self.create_run_section()
        right_layout.addWidget(run_section, stretch=1)

        # Results Section
        self.results_panel = ResultsPanel()
        right_layout.addWidget(self.results_panel, stretch=2)

        splitter.addWidget(right_widget)

        # Set splitter proportions
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        main_layout.addWidget(splitter)

    def create_run_section(self):
        """Create the run management section."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Title
        title = QLabel("<h3>Run Management</h3>")
        layout.addWidget(title)

        # Run control button
        self.run_button = QPushButton("Start Run")
        self.run_button.setStyleSheet("QPushButton { font-size: 14px; padding: 10px; }")
        self.run_button.clicked.connect(self.toggle_run)
        layout.addWidget(self.run_button)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Log viewer
        log_label = QLabel("<b>Pipeline Log:</b>")
        layout.addWidget(log_label)

        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setStyleSheet("QTextEdit { font-family: monospace; font-size: 10px; }")
        layout.addWidget(self.log_viewer)

        return widget

    def toggle_run(self):
        """Start or stop the pipeline run."""
        if self.worker is None or not self.worker.isRunning():
            self.start_run()
        else:
            self.stop_run()

    def start_run(self):
        """Start the mock pipeline run."""
        # Update UI
        self.run_button.setText("Stop Run")
        self.run_button.setStyleSheet("QPushButton { font-size: 14px; padding: 10px; background-color: #d32f2f; color: white; }")
        self.progress_bar.setValue(0)
        self.log_viewer.clear()
        self.results_panel.clear_results()

        # Get configuration
        config = self.config_panel.get_config()

        # Create and start worker
        self.worker = MockWorker(config)
        self.worker.signal_log_message.connect(self.append_log)
        self.worker.signal_progress_update.connect(self.update_progress)
        self.worker.signal_design_accepted.connect(self.results_panel.add_design)
        self.worker.signal_run_finished.connect(self.run_finished)
        self.worker.start()

    def stop_run(self):
        """Stop the running pipeline."""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
            self.append_log("\n[STOPPED] Run stopped by user.\n")
            self.run_finished()

    def append_log(self, message):
        """Append a message to the log viewer."""
        self.log_viewer.append(message)

    def update_progress(self, value):
        """Update the progress bar."""
        self.progress_bar.setValue(value)

    def run_finished(self):
        """Handle run completion."""
        self.run_button.setText("Start Run")
        self.run_button.setStyleSheet("QPushButton { font-size: 14px; padding: 10px; }")
        self.worker = None
