#!/usr/bin/env python3
"""
BindCraft GUI - Main Application (Demo Version)
A mock desktop application demonstrating the BindCraft interface without actual structure generation.
"""

import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow


def main():
    """Entry point for the BindCraft GUI application."""
    app = QApplication(sys.argv)
    app.setApplicationName("BindCraft Demo")
    app.setOrganizationName("BindCraft")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
