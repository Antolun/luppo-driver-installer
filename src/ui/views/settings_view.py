"""
Settings & Hybrid Graphics Control View with QSvgRenderer icons and auto-sizing.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QComboBox, QScrollArea, QMessageBox, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from src.backend.hardware_detector import HardwareDetector
from src.ui.icon_helper import get_icon, create_icon_label
from src.config.i18n import tr


class SettingsView(QWidget):
    update_repo_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Header Title with SVG icon
        head_box = QHBoxLayout()
        head_box.setSpacing(6)
        head_box.addWidget(create_icon_label("settings.svg", 18))

        lbl_head = QLabel(tr("settings_title"))
        lbl_head.setStyleSheet("font-size: 14px; font-weight: 800; color: #ffffff;")
        head_box.addWidget(lbl_head)
        head_box.addStretch()

        layout.addLayout(head_box)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        container = QWidget()
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        c_layout = QVBoxLayout(container)
        c_layout.setContentsMargins(0, 0, 0, 0)
        c_layout.setSpacing(10)

        # 1. Hybrid Graphics Profile Switcher
        hybrid_card = QFrame()
        hybrid_card.setProperty("class", "GPUCard")
        hc_layout = QVBoxLayout(hybrid_card)
        hc_layout.setSpacing(6)

        hb_header = QHBoxLayout()
        hb_header.setSpacing(6)
        hb_header.addWidget(create_icon_label("lightning.svg", 16))
        lbl_hb_title = QLabel(tr("hybrid_profile_title"))
        lbl_hb_title.setStyleSheet("font-weight: 700; font-size: 12px; color: #f59e0b;")
        hb_header.addWidget(lbl_hb_title)
        hb_header.addStretch()
        hc_layout.addLayout(hb_header)

        lbl_hb_desc = QLabel(tr("hybrid_profile_desc"))
        lbl_hb_desc.setStyleSheet("color: #94a3b8; font-size: 11px;")
        hc_layout.addWidget(lbl_hb_desc)

        hb_row = QHBoxLayout()
        hb_row.setSpacing(8)

        lbl_mode = QLabel(tr("lbl_graphics_mode"))
        lbl_mode.setStyleSheet("font-weight: 600; color: #cbd5e1; font-size: 12px;")

        self.cmb_hybrid_mode = QComboBox()
        self.cmb_hybrid_mode.addItems([
            tr("hybrid_opt_prime"),
            tr("hybrid_opt_nv"),
            tr("hybrid_opt_integrated")
        ])

        btn_apply_hybrid = QPushButton(tr("btn_apply_profile"))
        btn_apply_hybrid.clicked.connect(self._apply_hybrid_profile)

        hb_row.addWidget(lbl_mode)
        hb_row.addWidget(self.cmb_hybrid_mode, stretch=1)
        hb_row.addWidget(btn_apply_hybrid)

        hc_layout.addLayout(hb_row)
        c_layout.addWidget(hybrid_card)

        # 2. Luppo Package Repository Management
        luppo_card = QFrame()
        luppo_card.setProperty("class", "GPUCard")
        pc_layout = QVBoxLayout(luppo_card)
        pc_layout.setSpacing(6)

        pc_header = QHBoxLayout()
        pc_header.setSpacing(6)
        pc_header.addWidget(create_icon_label("package.svg", 16))
        lbl_pc_title = QLabel(tr("luppo_mgmt_title"))
        lbl_pc_title.setStyleSheet("font-weight: 700; font-size: 12px; color: #6366f1;")
        pc_header.addWidget(lbl_pc_title)
        pc_header.addStretch()
        pc_layout.addLayout(pc_header)

        lbl_pc_desc = QLabel(tr("luppo_mgmt_desc"))
        lbl_pc_desc.setStyleSheet("color: #94a3b8; font-size: 11px;")
        pc_layout.addWidget(lbl_pc_desc)

        pc_btns = QHBoxLayout()
        pc_btns.setSpacing(8)

        btn_update_repo = QPushButton(tr("btn_update_repo"))
        btn_update_repo.setIcon(get_icon("refresh.svg", 16, 16))
        btn_update_repo.setIconSize(QSize(16, 16))
        btn_update_repo.setObjectName("btn_secondary")
        btn_update_repo.clicked.connect(self.update_repo_requested.emit)

        btn_clean_cache = QPushButton(tr("btn_clean_cache"))
        btn_clean_cache.setIcon(get_icon("trash.svg", 16, 16))
        btn_clean_cache.setIconSize(QSize(16, 16))
        btn_clean_cache.setObjectName("btn_secondary")
        btn_clean_cache.clicked.connect(self._clean_luppo_cache)

        pc_btns.addWidget(btn_update_repo)
        pc_btns.addWidget(btn_clean_cache)
        pc_btns.addStretch()

        pc_layout.addLayout(pc_btns)
        c_layout.addWidget(luppo_card)

        c_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll, stretch=1)

    def _apply_hybrid_profile(self):
        selected = self.cmb_hybrid_mode.currentText()
        QMessageBox.information(
            self,
            tr("msg_hybrid_title"),
            tr("msg_hybrid_text", mode=selected)
        )

    def _clean_luppo_cache(self):
        HardwareDetector._run_cmd(["luppo", "dc"])
        QMessageBox.information(self, tr("msg_luppo_cache_title"), tr("msg_luppo_cache_text"))
