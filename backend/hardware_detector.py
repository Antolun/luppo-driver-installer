"""
Hardware Detector module for graphics cards and display system environment.
"""

import os
import re
import subprocess
from typing import List, Dict, Any, Optional
from models.gpu_device import GPUDevice, DriverOption, DriverStatus
from config import get_driver_database
from i18n import tr


class HardwareDetector:
    """Detects GPU hardware via lspci, glxinfo, vulkaninfo, and sysfs."""

    @staticmethod
    def detect_gpus() -> List[GPUDevice]:
        """Detect all display devices installed on the system."""
        gpus: List[GPUDevice] = []
        lspci_output = HardwareDetector._run_cmd(["lspci", "-vnn"])
        
        if not lspci_output:
            # Fallback to simulated hardware if lspci is missing or empty
            return HardwareDetector._get_mock_gpus()

        gpus = HardwareDetector._parse_lspci(lspci_output)

        if not gpus:
            # Try lspci without flags or fallback
            lspci_basic = HardwareDetector._run_cmd(["lspci"])
            gpus = HardwareDetector._parse_lspci_basic(lspci_basic)

        if not gpus:
            gpus = HardwareDetector._get_mock_gpus()

        # Mark hybrid setup if multiple GPUs are found
        is_hybrid_system = len(gpus) > 1
        for gpu in gpus:
            gpu.is_hybrid = is_hybrid_system

        # Enrich with OpenGL & Vulkan info
        gl_info = HardwareDetector.get_opengl_info()
        vk_info = HardwareDetector.get_vulkan_info()

        for gpu in gpus:
            if gl_info.get("vendor"):
                gpu.opengl_vendor = gl_info.get("vendor", "")
                gpu.opengl_renderer = gl_info.get("renderer", "")
                gpu.opengl_version = gl_info.get("version", "")
            
            gpu.vulkan_supported = vk_info.get("supported", False)
            gpu.vulkan_device_name = vk_info.get("device_name", "")

            # Attach driver options from database
            gpu.driver_options = HardwareDetector._get_driver_options_for_vendor(gpu.vendor_canonical)

        return gpus

    @staticmethod
    def _parse_lspci(output: str) -> List[GPUDevice]:
        gpus: List[GPUDevice] = []
        # Split blocks by blank line or device header
        blocks = output.split("\n\n")
        
        for block in blocks:
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            if not lines:
                continue

            header = lines[0]
            # Check if PCI device is display class: 0300 (VGA), 0302 (3D), 0380 (Display)
            if not any(cls in header for cls in ["[0300]", "[0302]", "[0380]", "VGA compatible", "3D controller", "Display controller"]):
                continue

            # Extract PCI address (e.g. 01:00.0)
            pci_match = re.match(r"^([0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-9a-fA-F])", header)
            pci_id = pci_match.group(1) if pci_match else "00:00.0"

            # Extract device code [vendor:device] e.g. [10de:25a0]
            code_match = re.search(r"\[([0-9a-fA-F]{4}:[0-9a-fA-F]{4})\]", header)
            device_code = code_match.group(1) if code_match else "0000:0000"

            # Extract model name
            # Header typically: 01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA107M [GeForce RTX 3050 Ti Mobile] [10de:25a0]
            model_name = header
            if " controller" in header:
                model_name = header.split(" controller", 1)[-1]
                model_name = re.sub(r"^\[[0-9a-fA-F]{4}\]:\s*", "", model_name).strip()

            active_driver = tr("unknown_str")
            kernel_modules = []
            subsystem = ""

            for line in lines[1:]:
                if line.startswith("Kernel driver in use:"):
                    active_driver = line.split(":", 1)[1].strip()
                elif line.startswith("Kernel modules:"):
                    mods = line.split(":", 1)[1].strip()
                    kernel_modules = [m.strip() for m in mods.split(",") if m.strip()]
                elif line.startswith("Subsystem:"):
                    subsystem = line.split(":", 1)[1].strip()

            vendor_raw, vendor_canonical = HardwareDetector._determine_vendor(header, device_code)

            gpu = GPUDevice(
                pci_id=pci_id,
                vendor_raw=vendor_raw,
                vendor_canonical=vendor_canonical,
                model_name=model_name,
                device_code=device_code,
                active_kernel_driver=active_driver,
                kernel_modules=kernel_modules,
                subsystem=subsystem
            )
            gpus.append(gpu)

        return gpus

    @staticmethod
    def _parse_lspci_basic(output: str) -> List[GPUDevice]:
        gpus: List[GPUDevice] = []
        for line in output.splitlines():
            if any(term in line for term in ["VGA compatible", "3D controller", "Display controller"]):
                parts = line.split(" ", 1)
                pci_id = parts[0]
                model = parts[1] if len(parts) > 1 else line
                vendor_raw, vendor_canonical = HardwareDetector._determine_vendor(line, "")
                gpus.append(GPUDevice(
                    pci_id=pci_id,
                    vendor_raw=vendor_raw,
                    vendor_canonical=vendor_canonical,
                    model_name=model,
                    device_code="N/A",
                    active_kernel_driver=tr("default_str"),
                    kernel_modules=[]
                ))
        return gpus

    @staticmethod
    def _determine_vendor(text: str, device_code: str) -> tuple[str, str]:
        text_upper = text.upper()
        code_upper = device_code.upper()

        if "10DE:" in code_upper or "NVIDIA" in text_upper:
            return "NVIDIA Corporation", "NVIDIA"
        elif "8086:" in code_upper or "INTEL" in text_upper:
            return "Intel Corporation", "INTEL"
        elif "1002:" in code_upper or "AMD" in text_upper or "RADEON" in text_upper or re.search(r"\bATI\b", text_upper):
            return "Advanced Micro Devices, Inc. [AMD/ATI]", "AMD"
        elif "15AD:" in code_upper or "VMWARE" in text_upper:
            return "VMware, Inc.", "GENERIC"
        elif "80EE:" in code_upper or "VIRTUALBOX" in text_upper:
            return "InnoTek Systemberatung GmbH (VirtualBox)", "GENERIC"
        
        return tr("unknown_vendor"), "GENERIC"

    @staticmethod
    def _get_driver_options_for_vendor(vendor_canonical: str) -> List[DriverOption]:
        db = get_driver_database()
        options_data = db.get(vendor_canonical, db.get("GENERIC", []))
        driver_options = []
        for opt in options_data:
            driver_options.append(DriverOption(
                id=opt["id"],
                name=opt["name"],
                package_name=opt["package_name"],
                description=opt["description"],
                recommended=opt.get("recommended", False),
                category=opt.get("category", tr("cat_general")),
                extra_packages=opt.get("extra_packages", []),
                supported_series=opt.get("supported_series", []),
                status=DriverStatus.NOT_INSTALLED
            ))
        return driver_options

    @staticmethod
    def get_opengl_info() -> Dict[str, str]:
        info = {"vendor": "", "renderer": "", "version": ""}
        out = HardwareDetector._run_cmd(["glxinfo", "-B"])
        if not out:
            return info

        for line in out.splitlines():
            if "OpenGL vendor string:" in line:
                info["vendor"] = line.split(":", 1)[1].strip()
            elif "OpenGL renderer string:" in line:
                info["renderer"] = line.split(":", 1)[1].strip()
            elif "OpenGL core profile version string:" in line or "OpenGL version string:" in line:
                if not info["version"]:
                    info["version"] = line.split(":", 1)[1].strip()
        return info

    @staticmethod
    def get_vulkan_info() -> Dict[str, Any]:
        info = {"supported": False, "device_name": ""}
        out = HardwareDetector._run_cmd(["vulkaninfo", "--summary"])
        if out and "Vulkan Instance Version" in out:
            info["supported"] = True
            for line in out.splitlines():
                if "deviceName" in line:
                    info["device_name"] = line.split("=", 1)[-1].strip()
                    break
        return info

    @staticmethod
    def get_system_summary() -> Dict[str, str]:
        session_type = os.environ.get("XDG_SESSION_TYPE", tr("unknown_str")).capitalize()
        desktop = os.environ.get("XDG_CURRENT_DESKTOP", tr("unknown_str"))
        kernel = HardwareDetector._run_cmd(["uname", "-r"]).strip()
        arch = HardwareDetector._run_cmd(["uname", "-m"]).strip()
        
        return {
            "session_type": session_type,
            "desktop": desktop,
            "kernel": kernel,
            "arch": arch,
        }

    @staticmethod
    def _run_cmd(cmd: List[str]) -> str:
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                return res.stdout
        except Exception:
            pass
        return ""

    @staticmethod
    def _get_mock_gpus() -> List[GPUDevice]:
        """Provides realistic mock data for testing or fallback environments."""
        nvidia_gpu = GPUDevice(
            pci_id="01:00.0",
            vendor_raw="NVIDIA Corporation",
            vendor_canonical="NVIDIA",
            model_name="GA107M [GeForce RTX 3050 Ti Mobile]",
            device_code="10de:25a0",
            active_kernel_driver="nvidia",
            kernel_modules=["nvidia", "nouveau"],
            is_hybrid=True,
            opengl_vendor="NVIDIA Corporation",
            opengl_renderer="NVIDIA GeForce RTX 3050 Ti Laptop GPU/PCIe/SSE2",
            opengl_version="4.6.0 NVIDIA 550.54.14",
            vulkan_supported=True,
            vulkan_device_name="NVIDIA GeForce RTX 3050 Ti Mobile"
        )
        nvidia_gpu.driver_options = HardwareDetector._get_driver_options_for_vendor("NVIDIA")

        intel_gpu = GPUDevice(
            pci_id="00:02.0",
            vendor_raw="Intel Corporation",
            vendor_canonical="INTEL",
            model_name="TigerLake-H GT1 [UHD Graphics]",
            device_code="8086:9a60",
            active_kernel_driver="i915",
            kernel_modules=["i915"],
            is_hybrid=True,
            opengl_vendor="Intel",
            opengl_renderer="Mesa Intel(R) UHD Graphics (TGL GT1)",
            opengl_version="4.6 Mesa 24.0.5",
            vulkan_supported=True,
            vulkan_device_name="Intel(R) UHD Graphics (TGL GT1)"
        )
        intel_gpu.driver_options = HardwareDetector._get_driver_options_for_vendor("INTEL")

        return [intel_gpu, nvidia_gpu]
