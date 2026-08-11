"""
System & Graphics Diagnostics View with responsive auto-sizing to fit window.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QFrame, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt
from pisidi.backend.hardware_detector import HardwareDetector
from pisidi.ui.icon_helper import create_icon_label
from pisidi.config.i18n import tr


class SysInfoView(QWidget):

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
        head_box.addWidget(create_icon_label("chart.svg", 18))
        
        lbl_head = QLabel(tr("sysinfo_title"))
        lbl_head.setStyleSheet("font-size: 14px; font-weight: 800; color: #ffffff;")
        head_box.addWidget(lbl_head)
        head_box.addStretch()

        layout.addLayout(head_box)

        # Scroll Area
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

        # 1. Environment & Display Card
        env_card = QFrame()
        env_card.setProperty("class", "GPUCard")
        ec_layout = QVBoxLayout(env_card)
        ec_layout.setSpacing(6)
        
        env_header = QHBoxLayout()
        env_header.setSpacing(6)
        env_header.addWidget(create_icon_label("monitor.svg", 16))
        lbl_env_title = QLabel(tr("sysinfo_env_title"))
        lbl_env_title.setStyleSheet("font-weight: 700; font-size: 12px; color: #6366f1;")
        env_header.addWidget(lbl_env_title)
        env_header.addStretch()
        ec_layout.addLayout(env_header)

        sys_summary = HardwareDetector.get_system_summary()
        env_text = (
            f"<b>{tr('sysinfo_desktop')}</b> {sys_summary['desktop']}<br>"
            f"<b>{tr('sysinfo_session')}</b> {sys_summary['session_type']}<br>"
            f"<b>{tr('sysinfo_kernel')}</b> {sys_summary['kernel']} ({sys_summary['arch']})<br>"
        )
        lbl_env_content = QLabel(env_text)
        lbl_env_content.setStyleSheet("color: #cbd5e1; font-size: 12px; line-height: 1.4;")
        ec_layout.addWidget(lbl_env_content)

        c_layout.addWidget(env_card)

        # 2. OpenGL Diagnostics Card
        gl_card = QFrame()
        gl_card.setProperty("class", "GPUCard")
        gl_layout = QVBoxLayout(gl_card)
        gl_layout.setSpacing(6)

        gl_header = QHBoxLayout()
        gl_header.setSpacing(6)
        gl_header.addWidget(create_icon_label("opengl.svg", 16))
        lbl_gl_title = QLabel(tr("sysinfo_gl_title"))
        lbl_gl_title.setStyleSheet("font-weight: 700; font-size: 12px; color: #10b981;")
        gl_header.addWidget(lbl_gl_title)
        gl_header.addStretch()
        gl_layout.addLayout(gl_header)

        self.txt_gl_info = QTextEdit()
        self.txt_gl_info.setReadOnly(True)
        self.txt_gl_info.setObjectName("log_console")
        self.txt_gl_info.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.txt_gl_info.setMinimumHeight(60)
        self.txt_gl_info.setMaximumHeight(110)
        gl_layout.addWidget(self.txt_gl_info)

        c_layout.addWidget(gl_card)

        # 3. Vulkan Diagnostics Card
        vk_card = QFrame()
        vk_card.setProperty("class", "GPUCard")
        vk_layout = QVBoxLayout(vk_card)
        vk_layout.setSpacing(6)

        vk_header = QHBoxLayout()
        vk_header.setSpacing(6)
        vk_header.addWidget(create_icon_label("vulkan.svg", 16))
        lbl_vk_title = QLabel(tr("sysinfo_vk_title"))
        lbl_vk_title.setStyleSheet("font-weight: 700; font-size: 12px; color: #f43f5e;")
        vk_header.addWidget(lbl_vk_title)
        vk_header.addStretch()
        vk_layout.addLayout(vk_header)

        self.txt_vk_info = QTextEdit()
        self.txt_vk_info.setReadOnly(True)
        self.txt_vk_info.setObjectName("log_console")
        self.txt_vk_info.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.txt_vk_info.setMinimumHeight(50)
        self.txt_vk_info.setMaximumHeight(100)
        vk_layout.addWidget(self.txt_vk_info)

        c_layout.addWidget(vk_card)

        # 4. Raw PCI Hardware Output
        pci_card = QFrame()
        pci_card.setProperty("class", "GPUCard")
        pci_layout = QVBoxLayout(pci_card)
        pci_layout.setSpacing(6)

        pci_header = QHBoxLayout()
        pci_header.setSpacing(6)
        pci_header.addWidget(create_icon_label("search.svg", 16))
        lbl_pci_title = QLabel(tr("sysinfo_pci_title"))
        lbl_pci_title.setStyleSheet("font-weight: 700; font-size: 12px; color: #3b82f6;")
        pci_header.addWidget(lbl_pci_title)
        pci_header.addStretch()
        pci_layout.addLayout(pci_header)

        self.txt_pci_info = QTextEdit()
        self.txt_pci_info.setReadOnly(True)
        self.txt_pci_info.setObjectName("log_console")
        self.txt_pci_info.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.txt_pci_info.setMinimumHeight(70)
        self.txt_pci_info.setMaximumHeight(120)
        pci_layout.addWidget(self.txt_pci_info)

        c_layout.addWidget(pci_card)
        c_layout.addStretch()

        scroll.setWidget(container)
        layout.addWidget(scroll, stretch=1)

        self.refresh_diagnostics()

    def refresh_diagnostics(self):
        gl_out = HardwareDetector._run_cmd(["glxinfo", "-B"]) or tr("sysinfo_gl_failed")
        self.txt_gl_info.setPlainText(gl_out)

        vk_out = HardwareDetector._run_cmd(["vulkaninfo", "--summary"]) or tr("sysinfo_vk_failed")
        self.txt_vk_info.setPlainText(vk_out)

        pci_out = HardwareDetector._run_cmd(["lspci", "-vnn"]) or tr("sysinfo_pci_failed")
        filtered_pci = []
        for block in pci_out.split("\n\n"):
            if any(term in block for term in ["VGA", "3D", "Display"]):
                filtered_pci.append(block)
        
        self.txt_pci_info.setPlainText("\n\n".join(filtered_pci) if filtered_pci else pci_out)
