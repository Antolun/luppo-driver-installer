"""
Drivers View: Displays GPU cards and driver options with responsive auto-sizing to fit window.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QProgressBar, QFrame, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from typing import List
from src.models.gpu_device import GPUDevice, DriverOption, DriverStatus
from src.ui.components.gpu_card import GPUCard
from src.ui.icon_helper import create_icon_label
from src.config.i18n import tr


class DriversView(QWidget):
    install_driver_requested = pyqtSignal(object, object)  # GPUDevice, DriverOption
    remove_driver_requested = pyqtSignal(object, object)   # GPUDevice, DriverOption
    update_repo_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.gpu_cards = []
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)

        # Progress / Status Header Bar (hidden by default until an action runs)
        self.progress_frame = QFrame()
        self.progress_frame.setStyleSheet("background-color: #1e293b; border: 1px solid #6366f1; border-radius: 8px; padding: 8px;")
        self.progress_frame.setVisible(False)

        pf_layout = QVBoxLayout(self.progress_frame)
        pf_layout.setSpacing(4)

        self.lbl_progress_status = QLabel(tr("view_executing_operation"))
        self.lbl_progress_status.setStyleSheet("font-weight: 700; color: #6366f1; font-size: 12px;border: none;background-color: transparent;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        pf_layout.addWidget(self.lbl_progress_status)
        pf_layout.addWidget(self.progress_bar)

        main_layout.addWidget(self.progress_frame)

        # Reboot Banner with SVG warning icon
        self.reboot_frame = QFrame()
        self.reboot_frame.setStyleSheet("background-color: rgba(16,185,129,0.15); border: 1px solid #10b981; border-radius: 8px; padding: 8px;")
        self.reboot_frame.setVisible(False)

        rf_layout = QHBoxLayout(self.reboot_frame)
        rf_layout.setSpacing(6)
        rf_layout.addWidget(create_icon_label("warning.svg", 16))

        lbl_reboot = QLabel(tr("reboot_warning"))
        lbl_reboot.setStyleSheet("color: #34d399; font-weight: 700; font-size: 12px;border: none;background-color: transparent;")
        
        rf_layout.addWidget(lbl_reboot)
        rf_layout.addStretch()

        main_layout.addWidget(self.reboot_frame)

        # Scrollable Area for GPU Cards with Auto-Fitting logic
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.cards_container = QWidget()
        self.cards_container.setStyleSheet("background-color: transparent;")
        self.cards_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(10)
        self.cards_layout.addStretch()

        scroll.setWidget(self.cards_container)
        main_layout.addWidget(scroll, stretch=1)

    def set_gpus(self, gpus: List[GPUDevice]):
        # Clear existing cards
        for card in self.gpu_cards:
            self.cards_layout.removeWidget(card)
            card.deleteLater()
        self.gpu_cards.clear()

        if not gpus:
            lbl_empty = QLabel(tr("no_gpus_found"))
            lbl_empty.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: 600; margin-top: 30px;")
            lbl_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.cards_layout.insertWidget(0, lbl_empty)
            return

        for gpu in gpus:
            card = GPUCard(gpu)
            card.install_driver_requested.connect(self.install_driver_requested.emit)
            card.remove_driver_requested.connect(self.remove_driver_requested.emit)
            self.gpu_cards.append(card)
            self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)

    def show_progress(self, title: str, percent: int):
        self.progress_frame.setVisible(True)
        self.lbl_progress_status.setText(title)
        self.progress_bar.setValue(percent)

    def hide_progress(self):
        self.progress_frame.setVisible(False)

    def show_reboot_warning(self):
        self.reboot_frame.setVisible(True)

    def refresh_cards(self):
        for card in self.gpu_cards:
            card.refresh_driver_statuses()
