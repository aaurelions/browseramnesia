import os
import sys
import subprocess
import time
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QGridLayout, QPushButton, QLabel, QWidget, QMessageBox, QProgressDialog
)

def resource_path(relative_path):
    """Get the absolute path to a resource bundled with PyInstaller."""
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

BROWSER_PATHS = {
    "Google Chrome": [
        "/Applications/Google Chrome.app/",
        "/Library/LaunchAgents/com.google.keystone*",
        "/Library/Application Support/Google/Chrome",
        "~/Library/Preferences/com.google.Chrome*",
        "~/Applications/Chrome Apps.localized/",
        "~/Library/Application Support/CrashReporter/Google Chrome",
        "~/Library/Caches/com.google.Chrome*",
        "~/Library/Saved Application State/com.google.Chrome.savedState/",
        "~/Library/Google/GoogleSoftwareUpdate/Actives/com.google.Chrome",
        "~/Library/Google/Google Chrome*",
    ],
    "Brave": [
        "/Applications/Brave Browser.app/",
        "~/Library/Application Support/BraveSoftware/",
        "~/Library/Caches/BraveSoftware/",
        "~/Library/Saved Application State/com.brave.Browser.savedState/",
    ],
    "Opera": [
        "/Applications/Opera.app/",
        "~/Library/Application Support/com.operasoftware.Opera/",
        "~/Library/Caches/com.operasoftware.Opera/",
        "~/Library/Saved Application State/com.operasoftware.Opera.savedState/",
    ],
    "Firefox": [
        "/Applications/Firefox.app/",
        "~/Library/Application Support/Firefox/",
        "~/Library/Caches/Firefox/",
        "~/Library/Saved Application State/org.mozilla.firefox.savedState/",
    ],
    "Puffin": [
        "/Applications/Puffin Secure Browser.app/",
        "~/Library/Application Support/Puffin Secure Browser/",
        "~/Library/Caches/Puffin Secure Browser/",
        "~/Library/Saved Application State/com.cloudmosa.puffin.savedState/",
    ],
    "Tor": [
        "/Applications/Tor Browser.app/",
        "~/Library/Application Support/TorBrowser-Data/",
        "~/Library/Caches/org.torproject.TorBrowser/",
        "~/Library/Saved Application State/org.torproject.TorBrowser.savedState/",
    ],
    "DuckDuckGo": [
        "/Applications/DuckDuckGo.app/",
        "~/Library/Application Support/DuckDuckGo/",
        "~/Library/Caches/DuckDuckGo/",
    ],
    "Mullvad": [
        "/Applications/Mullvad Browser.app/",
        "~/Library/Application Support/Mullvad/",
        "~/Library/Caches/Mullvad/",
    ],
    "Vivaldi": [
        "/Applications/Vivaldi.app/",
        "~/Library/Application Support/Vivaldi/",
        "~/Library/Caches/com.vivaldi.Vivaldi/",
        "~/Library/Saved Application State/com.vivaldi.Vivaldi.savedState/",
    ]
}

def is_browser_installed(browser_name):
    """Check if the browser is installed by verifying if any of its paths exist."""
    paths = BROWSER_PATHS.get(browser_name, [])
    for path in paths:
        resolved_path = os.path.expanduser(path)
        if os.path.exists(resolved_path):
            return True
    return False

class BrowserAmnesiaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser Amnesia")
        self.setFixedSize(600, 800)
        self.browser_buttons = {}
        self.init_ui()

    def init_ui(self):
        # Apply a dark gradient background
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2c3e50, stop: 1 #34495e
                );
            }
        """)

        layout = QVBoxLayout()

        # Logo at the top
        logo = QLabel()
        pixmap = QPixmap(resource_path("images/logo.png")).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("margin-top: 30px;")
        layout.addWidget(logo)

        # Title
        title = QLabel("Browser Amnesia")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: white; margin: 10px;")
        layout.addWidget(title)

        # Grid layout for buttons
        grid_layout = QGridLayout()

        row = 0
        col = 0
        for browser_name in BROWSER_PATHS.keys():
            # Create button
            button = QPushButton()
            button.setIcon(QIcon(resource_path(f"images/{browser_name.replace(' ', '').lower()}.png")))
            button.setIconSize(QSize(64, 64))
            button.setFixedSize(100, 100)

            if is_browser_installed(browser_name):
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #2c3e50;
                        border: 2px solid #34495e;
                        border-radius: 15px;
                    }
                    QPushButton:hover {
                        background-color: #770423;
                        border-color: #77045d;
                    }
                    QPushButton:pressed {
                        background-color: #16a085;
                        border-color: #1abc9c;
                    }
                """)
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                button.clicked.connect(lambda checked, b=browser_name: self.uninstall_browser(b))
            else:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: 2px dashed #7f8c8d;
                        border-radius: 15px;
                    }
                """)
                button.setEnabled(False)

            self.browser_buttons[browser_name] = button

            # Add button and browser name to grid
            browser_label = QLabel(browser_name)
            browser_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            browser_label.setStyleSheet("font-size: 14px; color: white; margin-top: 5px;")

            grid_layout.addWidget(button, row, col)
            grid_layout.addWidget(browser_label, row + 1, col)

            col += 1
            if col > 2:
                col = 0
                row += 2

        # Add grid layout to the main layout
        layout.addLayout(grid_layout)

        # Uninstall All Button
        uninstall_all_button = QPushButton("Uninstall All Browsers")
        uninstall_all_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        uninstall_all_button.setCursor(Qt.CursorShape.PointingHandCursor)
        uninstall_all_button.clicked.connect(self.uninstall_all_browsers)
        layout.addWidget(uninstall_all_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def uninstall_browser(self, browser_name):
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to uninstall {browser_name} and delete all related data?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            progress = QProgressDialog(f"Uninstalling {browser_name}...", "Cancel", 0, 100, self)
            progress.setWindowTitle("Please Wait")
            progress.setWindowModality(Qt.WindowModality.ApplicationModal)
            progress.setAutoClose(True)
            progress.setValue(0)

            for i in range(1, 11):
                time.sleep(0.1)
                progress.setValue(i * 10)
            progress.setValue(100)

            self.remove_browser_files(browser_name)
            QMessageBox.information(self, "Success", f"{browser_name} has been uninstalled.")

            # Update button style and disable it
            button = self.browser_buttons[browser_name]
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: 2px dashed #7f8c8d;
                    border-radius: 15px;
                }
            """)
            button.setEnabled(False)

    def uninstall_all_browsers(self):
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to uninstall ALL browsers and delete all related data?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            progress = QProgressDialog("Uninstalling all browsers...", "Cancel", 0, 100, self)
            progress.setWindowTitle("Please Wait")
            progress.setWindowModality(Qt.WindowModality.ApplicationModal)
            progress.setAutoClose(True)
            progress.setValue(0)

            for i in range(1, 11):
                time.sleep(0.2)
                progress.setValue(i * 10)
            progress.setValue(100)

            for browser_name in BROWSER_PATHS.keys():
                self.remove_browser_files(browser_name)
                # Update button style and disable it
                button = self.browser_buttons[browser_name]
                button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: 2px dashed #7f8c8d;
                        border-radius: 15px;
                    }
                """)
                button.setEnabled(False)

            QMessageBox.information(self, "Success", "All browsers have been uninstalled.")

    @staticmethod
    def remove_browser_files(browser_name):
        paths = BROWSER_PATHS.get(browser_name, [])
        for path in paths:
            try:
                resolved_path = os.path.expanduser(path)
                if os.path.exists(resolved_path):
                    subprocess.run(["rm", "-rf", resolved_path], check=True)
            except Exception as e:
                print(f"Error removing {resolved_path}: {e}")


if __name__ == "__main__":
    app = QApplication([])
    window = BrowserAmnesiaApp()
    window.show()
    app.exec()