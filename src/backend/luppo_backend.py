"""
Luppo Package Manager Backend Interface.
Handles checking package status, querying repository metadata, and running
install/remove operations with elevated permissions (pkexec / sudo).
"""

import os
import sys
import time
import re
import subprocess
from typing import Tuple, Optional, Dict, Any, Generator
from src.models.gpu_device import DriverOption, DriverStatus
from src.config.i18n import tr

# Try importing native luppo module if available
NATIVE_LUPPO_AVAILABLE = False
try:
    import luppo.db.installdb
    import luppo.db.packagedb
    NATIVE_LUPPO_AVAILABLE = True
except ImportError:
    NATIVE_LUPPO_AVAILABLE = False


class LuppoBackend:
    """Interface to Luppo Package Manager."""

    def __init__(self, demo_mode: bool = False):
        self.demo_mode = demo_mode
        self._installdb = None
        self._packagedb = None
        
        if NATIVE_LUPPO_AVAILABLE:
            try:
                self._installdb = luppo.db.installdb.InstallDB()
                self._packagedb = luppo.db.packagedb.PackageDB()
            except Exception:
                pass

    def check_package_status(self, driver: DriverOption) -> DriverOption:
        """Check if driver package and its extra packages are installed."""
        if self.demo_mode:
            # In demo mode, simulate driver status
            if driver.id in ["nvidia-driver", "intel-mesa", "amdgpu-mesa"]:
                driver.status = DriverStatus.INSTALLED
                driver.installed_version = "550.54.14-1"
                driver.available_version = "550.54.14-1"
            else:
                driver.status = DriverStatus.NOT_INSTALLED
                driver.installed_version = None
                driver.available_version = "550.54.14-1"
            return driver

        # 1. Try Python API first
        is_installed, version = self._check_installed_native(driver.package_name)
        if not is_installed:
            # 2. Fallback to CLI search
            is_installed, version = self._check_installed_cli(driver.package_name)

        if is_installed:
            driver.status = DriverStatus.INSTALLED
            driver.installed_version = version
        else:
            driver.status = DriverStatus.NOT_INSTALLED
            driver.installed_version = None

        # Fetch available version if possible
        avail_ver = self._check_available_native(driver.package_name)
        if not avail_ver:
            avail_ver = self._check_available_cli(driver.package_name)
        driver.available_version = avail_ver or "1.0.0"

        return driver

    def _check_installed_native(self, pkg_name: str) -> Tuple[bool, Optional[str]]:
        if self._installdb:
            try:
                if self._installdb.has_package(pkg_name):
                    pkg = self._installdb.get_package(pkg_name)
                    ver = f"{pkg.version}-{pkg.release}"
                    return True, ver
            except Exception:
                pass
        return False, None

    def _check_installed_cli(self, pkg_name: str) -> Tuple[bool, Optional[str]]:
        try:
            res = subprocess.run(["luppo", "info", pkg_name], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and ("Kurulu paket:" in res.stdout or "Installed package:" in res.stdout):
                ver_match = re.search(r"(?:Sürüm|Version):\s*([^\s,]+)", res.stdout)
                rel_match = re.search(r"(?:Salım|Release):\s*([^\s,]+)", res.stdout)
                ver = ver_match.group(1) if ver_match else tr("status_installed")
                if rel_match:
                    ver += f"-{rel_match.group(1)}"
                return True, ver
        except Exception:
            pass
        return False, None

    def _check_available_native(self, pkg_name: str) -> Optional[str]:
        if self._packagedb:
            try:
                pkg, repo = self._packagedb.get_package_repo(pkg_name)
                if pkg:
                    return f"{pkg.version}-{pkg.release}"
            except Exception:
                pass
        return None

    def _check_available_cli(self, pkg_name: str) -> Optional[str]:
        try:
            res = subprocess.run(["luppo", "info", pkg_name], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                ver_match = re.search(r"(?:Sürüm|Version):\s*([^\s,]+)", res.stdout)
                if ver_match:
                    return ver_match.group(1)
        except Exception:
            pass
        return None

    def install_package(self, pkg_name: str, extra_pkgs: list = None) -> Generator[Dict[str, Any], None, bool]:
        """
        Executes package installation yielding progress updates.
        Yields dicts with {"percent": int, "message": str, "log": str}
        Returns True on success, False on failure.
        """
        pkgs_to_install = [pkg_name] + (extra_pkgs or [])
        cmd_str = " ".join(pkgs_to_install)

        yield {
            "percent": 5,
            "message": tr("luppo_install_start", pkg_name=pkg_name),
            "log": tr("luppo_cmd_install", cmd=cmd_str)
        }

        if self.demo_mode:
            # Simulated installation steps
            steps = [
                (15, tr("luppo_verifying_repos"), 0.5),
                (30, tr("luppo_downloading", pkg=pkg_name, size="48.2 MB"), 1.0),
                (55, tr("luppo_unpacking"), 0.8),
                (75, tr("luppo_copying_files"), 1.2),
                (90, tr("luppo_updating_xorg"), 0.7),
                (100, tr("luppo_install_done", pkg=pkg_name), 0.3)
            ]
            for pct, msg, sleep_t in steps:
                time.sleep(sleep_t)
                yield {"percent": pct, "message": msg, "log": msg}
            return True

        # Real Execution using pkexec or sudo
        exec_cmd = ["pkexec", "luppo", "install", "--yes"] + pkgs_to_install
        
        try:
            process = subprocess.Popen(
                exec_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            progress = 10
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break

                if line:
                    clean_line = line.strip()
                    if "%" in clean_line:
                        pct_match = re.search(r"(\d+)%", clean_line)
                        if pct_match:
                            progress = min(95, max(progress, int(pct_match.group(1))))
                    else:
                        progress = min(90, progress + 2)

                    yield {
                        "percent": progress,
                        "message": clean_line[:80],
                        "log": f"[LUPPO] {clean_line}"
                    }

            return_code = process.poll()
            if return_code == 0:
                yield {
                    "percent": 100,
                    "message": tr("luppo_install_comp_msg"),
                    "log": tr("luppo_install_comp_log")
                }
                return True
            else:
                yield {
                    "percent": 0,
                    "message": tr("luppo_err_exit_code", code=return_code),
                    "log": tr("luppo_err_install_fail", code=return_code)
                }
                return False

        except Exception as e:
            yield {
                "percent": 0,
                "message": tr("luppo_err_exit_code", code=str(e)),
                "log": tr("luppo_exception", msg=str(e))
            }
            return False

    def remove_package(self, pkg_name: str) -> Generator[Dict[str, Any], None, bool]:
        """
        Executes package removal yielding progress updates.
        """
        yield {
            "percent": 5,
            "message": tr("luppo_remove_start", pkg=pkg_name),
            "log": tr("luppo_cmd_remove", pkg=pkg_name)
        }

        if self.demo_mode:
            steps = [
                (30, tr("luppo_checking_deps"), 0.5),
                (60, tr("luppo_deleting_files"), 0.8),
                (90, tr("luppo_refreshing_mods"), 0.5),
                (100, tr("luppo_remove_done", pkg=pkg_name), 0.3)
            ]
            for pct, msg, sleep_t in steps:
                time.sleep(sleep_t)
                yield {"percent": pct, "message": msg, "log": msg}
            return True

        exec_cmd = ["pkexec", "luppo", "remove", "--yes", pkg_name]
        try:
            process = subprocess.Popen(
                exec_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            progress = 10
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    clean_line = line.strip()
                    progress = min(90, progress + 5)
                    yield {"percent": progress, "message": clean_line[:80], "log": f"[LUPPO] {clean_line}"}

            return_code = process.poll()
            if return_code == 0:
                yield {
                    "percent": 100,
                    "message": tr("luppo_remove_comp_msg"),
                    "log": tr("luppo_remove_comp_log")
                }
                return True
            else:
                yield {
                    "percent": 0,
                    "message": tr("luppo_err_exit_code", code=return_code),
                    "log": tr("luppo_err_remove_fail", code=return_code)
                }
                return False
        except Exception as e:
            yield {
                "percent": 0,
                "message": tr("luppo_err_exit_code", code=str(e)),
                "log": tr("luppo_exception", msg=str(e))
            }
            return False

    def update_repositories(self) -> Generator[Dict[str, Any], None, bool]:
        """Update Luppo package repositories."""
        yield {
            "percent": 10,
            "message": tr("luppo_update_repos_start"),
            "log": tr("luppo_cmd_update_repo")
        }

        if self.demo_mode:
            time.sleep(1.0)
            yield {
                "percent": 50,
                "message": tr("luppo_downloading_repos"),
                "log": tr("luppo_updating_repos_log")
            }
            time.sleep(1.0)
            yield {
                "percent": 100,
                "message": tr("luppo_repos_updated_msg"),
                "log": tr("luppo_repos_updated_log")
            }
            return True

        exec_cmd = ["pkexec", "luppo", "update-repo"]
        try:
            process = subprocess.Popen(exec_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                yield {"percent": 50, "message": line.strip()[:80], "log": f"[LUPPO] {line.strip()}"}
            process.wait()
            return process.returncode == 0
        except Exception as e:
            yield {
                "percent": 0,
                "message": tr("luppo_err_exit_code", code=str(e)),
                "log": tr("luppo_exception", msg=str(e))
            }
            return False
