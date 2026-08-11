"""
PyQt6 Worker threads for asynchronous hardware scanning and Pisi package manager tasks.
"""

from PyQt6.QtCore import QThread, pyqtSignal
from typing import List, Optional
from pisidi.models.gpu_device import GPUDevice, DriverOption
from pisidi.backend.hardware_detector import HardwareDetector
from pisidi.backend.pisi_backend import PisiBackend
from pisidi.config.i18n import tr


class HardwareScanWorker(QThread):
    """Worker thread to scan GPU devices and hardware info asynchronously."""
    
    scan_finished = pyqtSignal(list)   # List[GPUDevice]
    log_message = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.log_message.emit(tr("worker_scan_start"))
        gpus = HardwareDetector.detect_gpus()
        self.log_message.emit(tr("worker_scan_count", count=len(gpus)))
        for gpu in gpus:
            self.log_message.emit(tr("worker_scan_gpu_item", vendor=gpu.vendor_canonical, model=gpu.model_name, driver=gpu.active_kernel_driver))
        self.scan_finished.emit(gpus)


class PackageCheckWorker(QThread):
    """Worker thread to query Pisi package status for driver options."""

    status_updated = pyqtSignal(object)  # GPUDevice
    check_finished = pyqtSignal()
    log_message = pyqtSignal(str)

    def __init__(self, gpus: List[GPUDevice], demo_mode: bool = False, parent=None):
        super().__init__(parent)
        self.gpus = gpus
        self.pisi = PisiBackend(demo_mode=demo_mode)

    def run(self):
        self.log_message.emit(tr("worker_pisi_querying"))
        for gpu in self.gpus:
            for option in gpu.driver_options:
                self.pisi.check_package_status(option)
                self.log_message.emit(tr("worker_pisi_status", pkg=option.package_name, status=option.status.value, version=option.installed_version or tr("status_not_installed")))
            self.status_updated.emit(gpu)
        self.check_finished.emit()


class DriverActionWorker(QThread):
    """Worker thread for running package installation, removal, or repository update."""

    progress = pyqtSignal(int, str, str)  # percent, status message, log message
    action_finished = pyqtSignal(bool, str)

    def __init__(self, action_type: str, pkg_name: str, extra_pkgs: list = None, demo_mode: bool = False, parent=None):
        super().__init__(parent)
        self.action_type = action_type  # 'install', 'remove', 'update_repo'
        self.pkg_name = pkg_name
        self.extra_pkgs = extra_pkgs or []
        self.pisi = PisiBackend(demo_mode=demo_mode)

    def run(self):
        success = False
        final_msg = ""
        
        if self.action_type == "install":
            gen = self.pisi.install_package(self.pkg_name, self.extra_pkgs)
            try:
                while True:
                    update = next(gen)
                    self.progress.emit(update["percent"], update["message"], update["log"])
            except StopIteration as ret:
                success = bool(ret.value)
                final_msg = tr("worker_install_success", pkg=self.pkg_name) if success else tr("worker_install_fail", pkg=self.pkg_name)
        
        elif self.action_type == "remove":
            gen = self.pisi.remove_package(self.pkg_name)
            try:
                while True:
                    update = next(gen)
                    self.progress.emit(update["percent"], update["message"], update["log"])
            except StopIteration as ret:
                success = bool(ret.value)
                final_msg = tr("worker_remove_success", pkg=self.pkg_name) if success else tr("worker_remove_fail", pkg=self.pkg_name)

        elif self.action_type == "update_repo":
            gen = self.pisi.update_repositories()
            try:
                while True:
                    update = next(gen)
                    self.progress.emit(update["percent"], update["message"], update["log"])
            except StopIteration as ret:
                success = bool(ret.value)
                final_msg = tr("worker_repo_success") if success else tr("worker_repo_fail")

        self.action_finished.emit(success, final_msg)
