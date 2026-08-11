"""
Logs View: Full page log console container.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from pisidi.ui.components.log_viewer import LogViewer


class LogsView(QWidget):

    def __init__(self, log_viewer: LogViewer, parent=None):
        super().__init__(parent)
        self.log_viewer = log_viewer
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.log_viewer, stretch=1)
