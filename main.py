#!/usr/bin/env python3
"""
Main Entry Point for Luppo Driver Installer.
"""

import sys
import os
import argparse

# Ensure application working directory is set to project root
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, SCRIPT_DIR)
os.chdir(SCRIPT_DIR)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from src.config.config import APP_NAME, APP_ORGANIZATION, APP_VERSION
from src.ui.main_window import MainWindow

from src.config.i18n import tr


def parse_args():
    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run application in Demo / Simulation mode without modifying system packages."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    app = QApplication(sys.argv)
    app.setApplicationName(tr("app_name"))
    app.setOrganizationName(APP_ORGANIZATION)
    app.setApplicationVersion(APP_VERSION)

    # Load application logo icon
    icon_path = os.path.join(SCRIPT_DIR, "src", "assets", "favicon.png")
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)

    window = MainWindow(demo_mode=args.demo)
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
