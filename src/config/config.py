"""
Luppo Driver Installer configuration, constants, and driver database for LupuS.
"""

from src.config.i18n import tr

APP_NAME = tr("app_name")
APP_SUBTITLE = tr("app_subtitle")
APP_VERSION = "2.0.0"
APP_ORGANIZATION = "Antolun"

# Color Palette (Modern Dark Theme)
COLOR_BG_DARK = "#0f172a"        # Main Background
COLOR_SURFACE = "#1e293b"        # Card / Container Surface
COLOR_SURFACE_HOVER = "#334155"  # Card Hover Surface
COLOR_SURFACE_LIGHT = "#475569"  # Lighter Surface / Borders
COLOR_BORDER = "#334155"         # Default Border
COLOR_BORDER_FOCUS = "#6366f1"   # Focused Border

# Text Colors
COLOR_TEXT_PRIMARY = "#f8fafc"
COLOR_TEXT_SECONDARY = "#94a3b8"
COLOR_TEXT_MUTED = "#64748b"

# Accent & Brand Colors
COLOR_PRIMARY = "#6366f1"        # Indigo Accent
COLOR_PRIMARY_HOVER = "#4f46e5"
COLOR_SUCCESS = "#10b981"        # Emerald Green
COLOR_WARNING = "#f59e0b"        # Amber Warning
COLOR_DANGER = "#ef4444"         # Red Danger
COLOR_INFO = "#06b6d4"           # Cyan Info

# Hardware Vendor Colors
COLOR_NVIDIA = "#10b981"         # NVIDIA Green
COLOR_AMD = "#f43f5e"            # AMD Red / Crimson
COLOR_INTEL = "#3b82f6"          # Intel Blue
COLOR_GENERIC = "#8b5cf6"        # Purple Generic


def get_driver_database():
    """Returns localized driver database per vendor."""
    return {
        "NVIDIA": [
            {
                "id": "nvidia-driver",
                "name": tr("driver_nvidia_prop_name"),
                "package_name": "nvidia-driver",
                "description": tr("driver_nvidia_prop_desc"),
                "recommended": False,
                "category": tr("cat_proprietary"),
                "extra_packages": ["nvidia-settings", "nvidia-prime"],
                "supported_series": ["RTX", "GTX 16xx", "GTX 10xx", "GTX 9xx", "GeForce 800M+"]
            },
            {
                "id": "nvidia-driver-open",
                "name": tr("driver_nvidia_open_name"),
                "package_name": "nvidia-driver-open",
                "description": tr("driver_nvidia_open_desc"),
                "recommended": True,
                "category": tr("cat_open_source_kernel"),
                "extra_packages": ["nvidia-settings"],
                "supported_series": ["Turing", "Ampere", "Ada Lovelace", "Hopper"]
            },
            {
                "id": "nvidia-390xx-driver",
                "name": tr("driver_nvidia_390_name"),
                "package_name": "nvidia-390xx-driver",
                "description": tr("driver_nvidia_390_desc"),
                "recommended": False,
                "category": tr("cat_legacy"),
                "extra_packages": ["nvidia-390xx-settings"],
                "supported_series": ["GeForce 400", "GeForce 500", "GeForce 600", "GeForce 700"]
            },
            {
                "id": "xf86-video-nouveau",
                "name": tr("driver_nouveau_name"),
                "package_name": "xf86-video-nouveau",
                "description": tr("driver_nouveau_desc"),
                "recommended": False,
                "category": tr("cat_open_source"),
                "extra_packages": ["mesa"],
                "supported_series": [tr("driver_all_nvidia")]
            }
        ],
        "AMD": [
            {
                "id": "amdgpu-mesa",
                "name": tr("driver_amd_mesa_name"),
                "package_name": "xf86-video-amdgpu",
                "description": tr("driver_amd_mesa_desc"),
                "recommended": True,
                "category": tr("cat_open_source"),
                "extra_packages": ["mesa", "mesa-vulkan-radeon", "lib32-mesa"],
                "supported_series": ["Radeon RX 7000", "RX 6000", "RX 5000", "RX 500/400", "Vega", "R9/R7"]
            },
            {
                "id": "ati-legacy",
                "name": tr("driver_amd_legacy_name"),
                "package_name": "xf86-video-ati",
                "description": tr("driver_amd_legacy_desc"),
                "recommended": False,
                "category": tr("cat_legacy_open_source"),
                "extra_packages": ["mesa"],
                "supported_series": [tr("driver_amd_legacy_series")]
            }
        ],
        "INTEL": [
            {
                "id": "intel-mesa",
                "name": tr("driver_intel_mesa_name"),
                "package_name": "mesa-vulkan-intel",
                "description": tr("driver_intel_mesa_desc"),
                "recommended": True,
                "category": tr("cat_open_source"),
                "extra_packages": ["xf86-video-intel", "intel-media-driver", "mesa"],
                "supported_series": ["Intel Arc", "Iris Xe", "UHD Graphics", "HD Graphics"]
            },
            {
                "id": "intel-media",
                "name": tr("driver_intel_media_name"),
                "package_name": "intel-media-driver",
                "description": tr("driver_intel_media_desc"),
                "recommended": False,
                "category": tr("cat_hw_acceleration"),
                "extra_packages": ["libva-utils"],
                "supported_series": [tr("driver_intel_broadwell_plus")]
            }
        ],
        "GENERIC": [
            {
                "id": "virtualbox-guest",
                "name": tr("driver_vbox_name"),
                "package_name": "virtualbox-guest-utils",
                "description": tr("driver_vbox_desc"),
                "recommended": False,
                "category": tr("cat_virtualization"),
                "extra_packages": [],
                "supported_series": ["VirtualBox VM"]
            },
            {
                "id": "vmware-video",
                "name": tr("driver_vmware_name"),
                "package_name": "xf86-video-vmware",
                "description": tr("driver_vmware_desc"),
                "recommended": False,
                "category": tr("cat_virtualization"),
                "extra_packages": [],
                "supported_series": ["VMware Workstation / ESXi"]
            }
        ]
    }


DRIVER_DATABASE = get_driver_database()
