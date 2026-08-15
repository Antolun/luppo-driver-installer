"""
GPU Card Component with SVG logos and responsive window auto-sizing.
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from src.models.gpu_device import GPUDevice, DriverOption
from src.ui.components.driver_row import DriverRow
from src.ui.icon_helper import get_pixmap, create_icon_label
from src.config.i18n import tr


class GPUCard(QFrame):
    install_driver_requested = pyqtSignal(object, object)   # GPUDevice, DriverOption
    remove_driver_requested = pyqtSignal(object, object)    # GPUDevice, DriverOption

    def __init__(self, gpu: GPUDevice, parent=None):
        super().__init__(parent)
        self.gpu = gpu
        self.driver_rows = []
        self.setProperty("class", "GPUCard")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Header Row: Official SVG Provider Logo, Model Name, PCI Address
        header_row = QHBoxLayout()
        header_row.setSpacing(10)

        # Official Provider Logo (NVIDIA, AMD, Intel, Generic) - 28x28 clean brand icon
        lbl_logo = QLabel()
        logo_svg = "generic_gpu.svg"
        if self.gpu.vendor_canonical == "NVIDIA":
            logo_svg = "nvidia.svg"
        elif self.gpu.vendor_canonical == "AMD":
            logo_svg = "amd.svg"
        elif self.gpu.vendor_canonical == "INTEL":
            logo_svg = "intel.svg"
        
        lbl_logo.setPixmap(get_pixmap(logo_svg, 28, 28))
        lbl_logo.setFixedSize(28, 28)
        lbl_logo.setContentsMargins(0, 0, 0, 0)
        lbl_logo.setStyleSheet("padding: 0px; margin: 0px; border: none; background: transparent;")
        header_row.addWidget(lbl_logo)

        # GPU Model Title (Displays strictly the clean model name)
        lbl_model = QLabel(self.gpu.display_model_name)
        lbl_model.setStyleSheet("font-size: 14px; font-weight: 800; color: #ffffff;")
        lbl_model.setWordWrap(True)
        header_row.addWidget(lbl_model, stretch=1)

        # PCI Address Badge
        lbl_pci = QLabel(f"PCI: {self.gpu.pci_id}")
        lbl_pci.setStyleSheet("color: #94a3b8; font-size: 10px; font-weight: 600; background: #0f172a; padding: 0; border-radius: 4px;")
        header_row.addWidget(lbl_pci)

        if self.gpu.is_hybrid:
            hybrid_widget = QWidget()
            h_box = QHBoxLayout(hybrid_widget)
            h_box.setContentsMargins(6, 2, 6, 2)
            h_box.setSpacing(4)
            h_box.addWidget(create_icon_label("lightning.svg", 12))
            lbl_hybrid_text = QLabel(tr("badge_hybrid"))
            lbl_hybrid_text.setStyleSheet("color: #f59e0b; font-size: 10px; font-weight: 700;border: none;background: transparent;padding: 0px; margin: 0px;")
            h_box.addWidget(lbl_hybrid_text)
            hybrid_widget.setStyleSheet("background: rgba(245,158,11,0.15); border: 1px solid #f59e0b; border-radius: 4px;padding: 0px; margin: 0px;")
            header_row.addWidget(hybrid_widget)

        layout.addLayout(header_row)

        # Technical Details Specs Sub-bar with SVG icons
        specs_row = QHBoxLayout()
        specs_row.setSpacing(12)

        # Active Driver Box
        drv_box = QHBoxLayout()
        drv_box.setSpacing(4)
        drv_box.addWidget(create_icon_label("generic_gpu.svg", 13))
        lbl_active_drv = QLabel(tr("gpu_active_driver", driver=self.gpu.active_kernel_driver))
        lbl_active_drv.setStyleSheet("color: #94a3b8; font-size: 11px;")
        drv_box.addWidget(lbl_active_drv)

        # OpenGL Box
        gl_box = QHBoxLayout()
        gl_box.setSpacing(4)
        gl_box.addWidget(create_icon_label("opengl.svg", 13))
        gl_renderer = self.gpu.opengl_renderer or tr("spec_not_specified")
        lbl_gl = QLabel(tr("gpu_opengl", renderer=gl_renderer[:36]))
        lbl_gl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        gl_box.addWidget(lbl_gl)

        # Vulkan Box
        vk_box = QHBoxLayout()
        vk_box.setSpacing(4)
        vk_box.addWidget(create_icon_label("vulkan.svg", 13))
        vk_str = tr("gpu_vulkan_supported") if self.gpu.vulkan_supported else tr("gpu_vulkan_not_supported")
        lbl_vk = QLabel(vk_str)
        lbl_vk.setStyleSheet("color: #94a3b8; font-size: 11px;")
        vk_box.addWidget(lbl_vk)

        specs_row.addLayout(drv_box)
        specs_row.addLayout(gl_box)
        specs_row.addLayout(vk_box)
        specs_row.addStretch()

        layout.addLayout(specs_row)

        # Divider line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #334155; background-color: #334155; max-height: 1px; border: none;")
        layout.addWidget(line)

        # Drivers Title Section
        lbl_drivers_title = QLabel(tr("gpu_available_drivers"))
        lbl_drivers_title.setStyleSheet("font-size: 11px; font-weight: 700; color: #64748b; letter-spacing: 0.5px;")
        layout.addWidget(lbl_drivers_title)

        # Populate Driver Rows
        for driver in self.gpu.driver_options:
            row = DriverRow(driver)
            row.install_requested.connect(lambda d=driver: self.install_driver_requested.emit(self.gpu, d))
            row.remove_requested.connect(lambda d=driver: self.remove_driver_requested.emit(self.gpu, d))
            self.driver_rows.append(row)
            layout.addWidget(row)

    def refresh_driver_statuses(self):
        for row in self.driver_rows:
            row.update_status(row.driver.status)
