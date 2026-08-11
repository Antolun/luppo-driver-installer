"""
Driver Row Component with SVG icons and auto-sizing.
"""

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QWidget, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from pisidi.models.gpu_device import DriverOption, DriverStatus
from pisidi.ui.icon_helper import get_icon, get_pixmap, create_icon_label
from pisidi.config.i18n import tr


class DriverRow(QFrame):
    install_requested = pyqtSignal(object)   # DriverOption
    remove_requested = pyqtSignal(object)    # DriverOption

    def __init__(self, driver: DriverOption, parent=None):
        super().__init__(parent)
        self.driver = driver
        self.setProperty("class", "DriverRow")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        # Left Info Box
        info_box = QVBoxLayout()
        info_box.setSpacing(3)

        # Title & Badges Row
        title_row = QHBoxLayout()
        title_row.setSpacing(6)

        lbl_name = QLabel(self.driver.name)
        lbl_name.setStyleSheet("font-weight: 700; font-size: 13px; color: #f8fafc;")

        title_row.addWidget(lbl_name)

        if self.driver.recommended:
            rec_widget = QWidget()
            rec_widget.setFixedHeight(16)
            rec_box = QHBoxLayout(rec_widget)
            rec_box.setContentsMargins(4, 0, 5, 0)
            rec_box.setSpacing(2)
            rec_box.addWidget(create_icon_label("star.svg", 9))
            lbl_rec_text = QLabel(tr("badge_recommended"))
            lbl_rec_text.setStyleSheet("color: #a5b4fc; font-size: 8.5px; font-weight: 700; border: none; background: transparent; padding: 0px; margin: 0px;")
            rec_box.addWidget(lbl_rec_text)
            rec_widget.setStyleSheet("background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 4px; margin: 0px;")
            title_row.addWidget(rec_widget)

        cat_widget = QWidget()
        cat_widget.setFixedHeight(16)
        cat_box = QHBoxLayout(cat_widget)
        cat_box.setContentsMargins(4, 0, 5, 0)
        cat_box.setSpacing(2)
        cat_box.addWidget(create_icon_label("package.svg", 9))
        lbl_cat_text = QLabel(self.driver.category)
        lbl_cat_text.setStyleSheet("color: #94a3b8; font-size: 8.5px; font-weight: 600; border: none; background: transparent; padding: 0px; margin: 0px;")
        cat_box.addWidget(lbl_cat_text)
        cat_widget.setStyleSheet("background: #1e293b; border: 1px solid #334155; border-radius: 4px; margin: 0px;")
        title_row.addWidget(cat_widget)

        title_row.addStretch()
        info_box.addLayout(title_row)

        # Description
        lbl_desc = QLabel(self.driver.description)
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("color: #94a3b8; font-size: 11px;")
        info_box.addWidget(lbl_desc)

        # Package Details line
        ver_text = tr("driver_row_package", pkg=self.driver.package_name)
        if self.driver.installed_version:
            ver_text += tr("driver_row_installed_ver", ver=self.driver.installed_version)
        elif self.driver.available_version:
            ver_text += tr("driver_row_repo_ver", ver=self.driver.available_version)

        lbl_ver = QLabel(ver_text)
        lbl_ver.setStyleSheet("color: #64748b; font-size: 10px;")
        info_box.addWidget(lbl_ver)

        layout.addLayout(info_box, stretch=1)

        # Right Action Column (Status & Button)
        action_box = QVBoxLayout()
        action_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        action_box.setSpacing(4)

        self.status_container = QWidget()
        self.status_box = QHBoxLayout(self.status_container)
        self.status_box.setContentsMargins(0, 0, 0, 0)
        self.status_box.setSpacing(4)

        self.lbl_status_icon = QLabel()
        self.lbl_status = QLabel()
        
        self.status_box.addWidget(self.lbl_status_icon)
        self.status_box.addWidget(self.lbl_status)

        self.btn_action = QPushButton()
        self.btn_action.setFixedWidth(110)

        self.update_status(self.driver.status)
        self.btn_action.clicked.connect(self._on_action_clicked)

        action_box.addWidget(self.status_container, alignment=Qt.AlignmentFlag.AlignCenter)
        action_box.addWidget(self.btn_action, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(action_box)

    def update_status(self, status: DriverStatus):
        self.driver.status = status
        if status == DriverStatus.INSTALLED:
            self.lbl_status_icon.setPixmap(get_pixmap("check.svg", 14, 14))
            self.lbl_status_icon.setVisible(True)
            self.lbl_status.setText(tr("status_installed"))
            self.lbl_status.setStyleSheet("color: #34d399; font-weight: 800; font-size: 11px;")
            self.btn_action.setText(tr("btn_remove"))
            self.btn_action.setObjectName("btn_danger")
            self.btn_action.setEnabled(True)
        elif status == DriverStatus.INSTALLING:
            self.lbl_status_icon.setVisible(False)
            self.lbl_status.setText(tr("status_installing"))
            self.lbl_status.setStyleSheet("color: #f59e0b; font-weight: 800; font-size: 11px;")
            self.btn_action.setText(tr("status_installing"))
            self.btn_action.setEnabled(False)
        elif status == DriverStatus.REMOVING:
            self.lbl_status_icon.setVisible(False)
            self.lbl_status.setText(tr("status_removing"))
            self.lbl_status.setStyleSheet("color: #f59e0b; font-weight: 800; font-size: 11px;")
            self.btn_action.setText(tr("status_removing"))
            self.btn_action.setEnabled(False)
        else:
            self.lbl_status_icon.setVisible(False)
            self.lbl_status.setText(tr("status_not_installed"))
            self.lbl_status.setStyleSheet("color: #64748b; font-size: 10px;")
            self.btn_action.setText(tr("btn_install"))
            self.btn_action.setObjectName("")
            self.btn_action.setEnabled(True)

        self.btn_action.style().unpolish(self.btn_action)
        self.btn_action.style().polish(self.btn_action)

    def _on_action_clicked(self):
        if self.driver.status == DriverStatus.INSTALLED:
            self.remove_requested.emit(self.driver)
        else:
            self.install_requested.emit(self.driver)
