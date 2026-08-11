"""
Data models for GPU Devices and Driver Options.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from pisidi.config.i18n import tr


class DriverStatus(Enum):
    NOT_INSTALLED = "not_installed"
    INSTALLED = "installed"
    RECOMMENDED = "recommended"
    INSTALLING = "installing"
    REMOVING = "removing"
    ERROR = "error"


@dataclass
class DriverOption:
    id: str
    name: str
    package_name: str
    description: str
    recommended: bool = False
    category: str = "General"
    extra_packages: List[str] = field(default_factory=list)
    supported_series: List[str] = field(default_factory=list)
    status: DriverStatus = DriverStatus.NOT_INSTALLED
    installed_version: Optional[str] = None
    available_version: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "package_name": self.package_name,
            "description": self.description,
            "recommended": self.recommended,
            "category": self.category,
            "status": self.status.value,
            "installed_version": self.installed_version,
            "available_version": self.available_version,
        }


@dataclass
class GPUDevice:
    pci_id: str                   # e.g., "01:00.0"
    vendor_raw: str               # e.g., "NVIDIA Corporation"
    vendor_canonical: str         # "NVIDIA", "AMD", "INTEL", "GENERIC"
    model_name: str               # e.g., "GA107M [GeForce RTX 3050 Ti Mobile]"
    device_code: str              # e.g., "10de:25a0"
    active_kernel_driver: str     # e.g., "nvidia", "i915", "amdgpu"
    kernel_modules: List[str] = field(default_factory=list)
    is_primary: bool = False
    is_hybrid: bool = False
    subsystem: str = ""
    opengl_vendor: str = ""
    opengl_renderer: str = ""
    opengl_version: str = ""
    vulkan_supported: bool = False
    vulkan_device_name: str = ""
    driver_options: List[DriverOption] = field(default_factory=list)

    @property
    def vendor_color(self) -> str:
        from pisidi.config.config import COLOR_NVIDIA, COLOR_AMD, COLOR_INTEL, COLOR_GENERIC
        if self.vendor_canonical == "NVIDIA":
            return COLOR_NVIDIA
        elif self.vendor_canonical == "AMD":
            return COLOR_AMD
        elif self.vendor_canonical == "INTEL":
            return COLOR_INTEL
        return COLOR_GENERIC

    @property
    def vendor_badge_text(self) -> str:
        if self.vendor_canonical == "NVIDIA":
            return tr("badge_nvidia")
        elif self.vendor_canonical == "AMD":
            return tr("badge_amd")
        elif self.vendor_canonical == "INTEL":
            return tr("badge_intel")
        return tr("badge_generic")

    @property
    def display_model_name(self) -> str:
        """Extracts and returns strictly the clean GPU model name."""
        import re
        name = self.model_name
        name = re.sub(r'\(prog-if.*?\)', '', name)
        name = re.sub(r'\(rev.*?\)', '', name)
        name = re.sub(r'^\[[0-9a-fA-F]{4}\]:?\s*', '', name)
        name = re.sub(r'^(NVIDIA Corporation|Advanced Micro Devices, Inc\. \[AMD/ATI\]|Intel Corporation)\s*', '', name, flags=re.IGNORECASE)
        
        matches = re.findall(r'\[([^\]]+)\]', name)
        for m in matches:
            m_strip = m.strip()
            if re.match(r'^[0-9a-fA-F]{4}:[0-9a-fA-F]{4}$', m_strip):
                continue
            if m_strip.lower() in ['vga controller', '3d controller', 'display controller', 'generic']:
                continue
            return m_strip

        name = re.sub(r'\[[0-9a-fA-F]{4}:[0-9a-fA-F]{4}\]', '', name)
        name = re.sub(r'\[[0-9a-fA-F]{4}\]', '', name)
        return name.strip()
