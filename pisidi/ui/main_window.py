"""
Main Window for LupuS PiSiDi.
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QMessageBox, QSizePolicy
from PyQt6.QtCore import Qt

from pisidi.config.config import APP_NAME
from pisidi.models.gpu_device import GPUDevice, DriverOption, DriverStatus
from pisidi.backend.worker import HardwareScanWorker, PackageCheckWorker, DriverActionWorker
from pisidi.ui.style import MAIN_STYLE
from pisidi.ui.components.header_bar import HeaderBar
from pisidi.ui.components.sidebar import Sidebar
from pisidi.ui.components.log_viewer import LogViewer
from pisidi.ui.views.drivers_view import DriversView
from pisidi.ui.views.sysinfo_view import SysInfoView
from pisidi.ui.views.settings_view import SettingsView
from pisidi.ui.views.logs_view import LogsView
from pisidi.config.i18n import tr


class MainWindow(QMainWindow):

    def __init__(self, demo_mode: bool = False):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1280, 700)
        self.setMinimumSize(740, 480)
        
        self.demo_mode = demo_mode
        self.detected_gpus = []
        self.scan_worker = None
        self.pkg_check_worker = None
        self.action_worker = None

        self._apply_theme()
        self._init_ui()
        self.start_hardware_scan()

    def _apply_theme(self):
        self.setStyleSheet(MAIN_STYLE)

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 1. Header Bar
        self.header_bar = HeaderBar(demo_mode=self.demo_mode)
        self.header_bar.refresh_requested.connect(self.start_hardware_scan)
        self.header_bar.demo_toggled.connect(self._on_demo_toggled)
        root_layout.addWidget(self.header_bar)

        # 2. Main Content Splitter (Sidebar + Page Stack)
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Sidebar Navigation (Sidebar retained as requested)
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._on_page_changed)
        content_layout.addWidget(self.sidebar)

        # Shared Log Viewer Component
        self.log_viewer = LogViewer()

        # Stacked Pages Widget with Auto-Resizing Padding
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("padding: 12px;")
        self.stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Page Views
        self.drivers_view = DriversView()
        self.drivers_view.install_driver_requested.connect(self._on_install_requested)
        self.drivers_view.remove_driver_requested.connect(self._on_remove_requested)
        self.drivers_view.update_repo_requested.connect(self._on_update_repo_requested)

        self.sysinfo_view = SysInfoView()
        
        self.settings_view = SettingsView()
        self.settings_view.update_repo_requested.connect(self._on_update_repo_requested)

        self.logs_view = LogsView(self.log_viewer)

        self.stack.addWidget(self.drivers_view)   # Index 0
        self.stack.addWidget(self.sysinfo_view)   # Index 1
        self.stack.addWidget(self.settings_view)   # Index 2
        self.stack.addWidget(self.logs_view)       # Index 3

        content_layout.addWidget(self.stack, stretch=1)
        root_layout.addWidget(content_widget, stretch=1)

    def _on_page_changed(self, index: int):
        self.stack.setCurrentIndex(index)
        if index == 1:
            self.sysinfo_view.refresh_diagnostics()

    def _on_demo_toggled(self, enabled: bool):
        self.demo_mode = enabled
        self.log_viewer.append_log(tr("log_demo_enabled") if enabled else tr("log_demo_disabled"))
        self.start_hardware_scan()

    def start_hardware_scan(self):
        """Asynchronously scan GPU hardware devices."""
        self.log_viewer.append_log(tr("log_scan_start"))
        self.drivers_view.show_progress(tr("progress_scanning_gpus"), 20)

        self.scan_worker = HardwareScanWorker()
        self.scan_worker.log_message.connect(self.log_viewer.append_log)
        self.scan_worker.scan_finished.connect(self._on_hardware_scan_finished)
        self.scan_worker.start()

    def _on_hardware_scan_finished(self, gpus: list):
        self.detected_gpus = gpus
        self.drivers_view.set_gpus(gpus)
        self.drivers_view.show_progress(tr("progress_querying_pisi"), 60)

        # Check package statuses
        self.pkg_check_worker = PackageCheckWorker(gpus, demo_mode=self.demo_mode)
        self.pkg_check_worker.log_message.connect(self.log_viewer.append_log)
        self.pkg_check_worker.status_updated.connect(self._on_package_status_updated)
        self.pkg_check_worker.check_finished.connect(self._on_package_check_finished)
        self.pkg_check_worker.start()

    def _on_package_status_updated(self, gpu: GPUDevice):
        self.drivers_view.refresh_cards()

    def _on_package_check_finished(self):
        self.drivers_view.hide_progress()
        self.log_viewer.append_log(tr("log_scan_done"))

    def _on_install_requested(self, gpu: GPUDevice, driver: DriverOption):
        extra_str = ', '.join(driver.extra_packages) if driver.extra_packages else tr('none_str')
        reply = QMessageBox.question(
            self,
            tr("dialog_install_title"),
            tr("dialog_install_msg", driver_name=driver.name, package_name=driver.package_name, extra=extra_str),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        driver.status = DriverStatus.INSTALLING
        self.drivers_view.refresh_cards()
        self.log_viewer.append_log(tr("log_install_req", pkg=driver.package_name))

        self.action_worker = DriverActionWorker(
            action_type="install",
            pkg_name=driver.package_name,
            extra_pkgs=driver.extra_packages,
            demo_mode=self.demo_mode
        )
        self.action_worker.progress.connect(self._on_action_progress)
        self.action_worker.action_finished.connect(lambda success, msg: self._on_action_finished(success, msg, gpu, driver, DriverStatus.INSTALLED))
        self.action_worker.start()

    def _on_remove_requested(self, gpu: GPUDevice, driver: DriverOption):
        reply = QMessageBox.question(
            self,
            tr("dialog_remove_title"),
            tr("dialog_remove_msg", driver_name=driver.name, package_name=driver.package_name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        driver.status = DriverStatus.REMOVING
        self.drivers_view.refresh_cards()
        self.log_viewer.append_log(tr("log_remove_req", pkg=driver.package_name))

        self.action_worker = DriverActionWorker(
            action_type="remove",
            pkg_name=driver.package_name,
            demo_mode=self.demo_mode
        )
        self.action_worker.progress.connect(self._on_action_progress)
        self.action_worker.action_finished.connect(lambda success, msg: self._on_action_finished(success, msg, gpu, driver, DriverStatus.NOT_INSTALLED))
        self.action_worker.start()

    def _on_update_repo_requested(self):
        self.log_viewer.append_log(tr("log_repo_req"))
        self.action_worker = DriverActionWorker(
            action_type="update_repo",
            pkg_name="",
            demo_mode=self.demo_mode
        )
        self.action_worker.progress.connect(self._on_action_progress)
        self.action_worker.action_finished.connect(lambda success, msg: self._on_repo_update_finished(success, msg))
        self.action_worker.start()

    def _on_action_progress(self, percent: int, message: str, log_line: str):
        self.drivers_view.show_progress(message, percent)
        if log_line:
            self.log_viewer.append_log(log_line)

    def _on_action_finished(self, success: bool, msg: str, gpu: GPUDevice, driver: DriverOption, target_status: DriverStatus):
        self.drivers_view.hide_progress()
        
        if success:
            driver.status = target_status
            if target_status == DriverStatus.INSTALLED:
                driver.installed_version = driver.available_version or tr("version_updated")
            else:
                driver.installed_version = None

            self.drivers_view.refresh_cards()
            self.drivers_view.show_reboot_warning()
            self.log_viewer.append_log(tr("log_success", msg=msg))
            QMessageBox.information(self, tr("dialog_success_title"), msg)
        else:
            driver.status = DriverStatus.ERROR
            self.drivers_view.refresh_cards()
            self.log_viewer.append_log(tr("log_error", msg=msg))
            QMessageBox.critical(self, tr("dialog_error_title"), msg)

    def _on_repo_update_finished(self, success: bool, msg: str):
        self.drivers_view.hide_progress()
        if success:
            self.log_viewer.append_log(tr("log_success", msg=msg))
            QMessageBox.information(self, tr("dialog_repo_success_title"), msg)
            self.start_hardware_scan()
        else:
            self.log_viewer.append_log(tr("log_error", msg=msg))
            QMessageBox.critical(self, tr("dialog_repo_error_title"), msg)
