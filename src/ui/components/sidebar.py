"""
Sidebar Navigation Component.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QButtonGroup
from PyQt6.QtCore import pyqtSignal, Qt
from src.config.config import APP_NAME, APP_VERSION
from src.config.i18n import tr


class Sidebar(QWidget):
    page_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(8)

        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        nav_items = [
            (0, tr("nav_gpus")),
            (1, tr("nav_diagnostics")),
            (2, tr("nav_settings")),
            (3, tr("nav_logs"))
        ]

        for index, text in nav_items:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setObjectName("nav_btn")
            if index == 0:
                btn.setChecked(True)
            
            self.btn_group.addButton(btn, index)
            layout.addWidget(btn)

        self.btn_group.idClicked.connect(self.page_changed.emit)

        layout.addStretch()

        # Footer Brand Label
        lbl_brand = QLabel(f"{APP_NAME} v{APP_VERSION}")
        lbl_brand.setStyleSheet("color: #475569; font-size: 11px; font-weight: 600; text-align: center; margin-left: 8px;")
        layout.addWidget(lbl_brand)
