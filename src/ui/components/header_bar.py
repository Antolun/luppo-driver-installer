"""
Header Bar Component with high-contrast QSvgRenderer icons.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from src.config.config import APP_NAME
from src.backend.hardware_detector import HardwareDetector
from src.ui.icon_helper import get_icon, create_icon_label
from src.config.i18n import tr


class HeaderBar(QWidget):
    refresh_requested = pyqtSignal()
    demo_toggled = pyqtSignal(bool)

    def __init__(self, demo_mode: bool = False, parent=None):
        super().__init__(parent)
        self.setObjectName("header_bar")
        self.demo_mode = demo_mode
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(10)

        # Title & Subtitle Box
        title_box = QVBoxLayout()
        title_box.setSpacing(1)

        lbl_title = QLabel(APP_NAME)
        lbl_title.setObjectName("app_title")

        lbl_sub = QLabel(tr("app_subtitle"))
        lbl_sub.setObjectName("app_subtitle")

        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_sub)

        layout.addLayout(title_box)
        layout.addStretch()

        # System Status Badges with SVG icons
        sys_info = HardwareDetector.get_system_summary()

        # Session / Display Server Box
        session_box = QHBoxLayout()
        session_box.setSpacing(5)
        session_box.addWidget(create_icon_label("monitor.svg", 16))
        lbl_session_text = QLabel(f"{sys_info['desktop']}/{sys_info['session_type']}")
        lbl_session_text.setStyleSheet("color: #94a3b8; font-weight: 600; font-size: 11px;")
        session_box.addWidget(lbl_session_text)

        session_widget = QWidget()
        session_widget.setStyleSheet("background: #0f172a; border-radius: 5px; padding: 2px 8px;")
        session_widget.setLayout(session_box)

        # Kernel Box
        kernel_box = QHBoxLayout()
        kernel_box.setSpacing(5)
        kernel_box.addWidget(create_icon_label("kernel.svg", 16))
        lbl_kernel_text = QLabel(f"Kernel: {sys_info['kernel']}")
        lbl_kernel_text.setStyleSheet("color: #94a3b8; font-weight: 600; font-size: 11px;")
        kernel_box.addWidget(lbl_kernel_text)

        kernel_widget = QWidget()
        kernel_widget.setStyleSheet("background: #0f172a; border-radius: 5px; padding: 2px 8px;")
        kernel_widget.setLayout(kernel_box)

        layout.addWidget(session_widget)
        layout.addWidget(kernel_widget)

        # Demo Mode Toggle Button with explicit icon size
        self.btn_demo = QPushButton(tr("header_demo_inactive") if not self.demo_mode else tr("header_demo_active"))
        self.btn_demo.setIcon(get_icon("flask.svg", 18, 18))
        self.btn_demo.setIconSize(QSize(18, 18))
        self.btn_demo.setCheckable(True)
        self.btn_demo.setChecked(self.demo_mode)
        self.btn_demo.setObjectName("btn_secondary")
        self.btn_demo.clicked.connect(self._toggle_demo)

        # Refresh Hardware Button with explicit icon size
        btn_refresh = QPushButton(tr("header_refresh"))
        btn_refresh.setIcon(get_icon("refresh.svg", 18, 18))
        btn_refresh.setIconSize(QSize(18, 18))
        btn_refresh.setObjectName("btn_secondary")
        btn_refresh.clicked.connect(self.refresh_requested.emit)

        layout.addWidget(self.btn_demo)
        layout.addWidget(btn_refresh)

    def _toggle_demo(self, checked: bool):
        self.demo_mode = checked
        if checked:
            self.btn_demo.setText(tr("header_demo_active"))
            self.btn_demo.setStyleSheet("background-color: #f59e0b; color: #000000;")
        else:
            self.btn_demo.setText(tr("header_demo_inactive"))
            self.btn_demo.setStyleSheet("")
        self.demo_toggled.emit(checked)
