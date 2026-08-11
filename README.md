# PiSiDi (Pisi Linux / LupuS)

**PiSiDi** is a modern PyQt6 desktop application for Pisi Linux / LupuS designed to automatically detect NVIDIA, AMD, Intel, and Virtual Machine GPU hardware, and provide one-click driver installation, removal, and management through the PiSi package manager.

---

## Key Features

- **Automatic GPU Hardware Detection:**
  - Scans installed PCI display devices (`lspci`).
  - Detects hybrid dual-GPU setups (Optimus / PRIME) such as NVIDIA/Intel or AMD/Intel.
  - Reports active kernel drivers (`nvidia`, `i915`, `amdgpu`, `nouveau`), OpenGL renderer, and Vulkan API support.

- **Automatic Multi-Language Support (i18n):**
  - Native support for English and Turkish.
  - Automatically selects the interface language according to system locale settings (defaults to English).

- **PiSi Package Manager Integration:**
  - Queries driver package status via PiSi Python API and CLI.
  - Fetches currently installed system driver versions and new available versions from PiSi package repositories.
  - Performs package installation, removal, and repository updates using `pkexec` privilege elevation.
  - Non-blocking asynchronous UI powered by `QThread` workers.

- **Driver Database:**
  - **NVIDIA:** Official proprietary drivers (`nvidia-driver`, `nvidia-driver-open`), legacy drivers (`nvidia-390xx-driver`), and community open-source Nouveau driver (`xf86-video-nouveau`).
  - **AMD:** Mesa & AMDGPU open-source stack (`xf86-video-amdgpu`, `mesa-vulkan-radeon`) and legacy ATI driver (`xf86-video-ati`).
  - **Intel:** Intel graphics open-source stack (`mesa-vulkan-intel`, `intel-media-driver`).
  - **Virtual Devices:** VirtualBox Guest Additions and VMware SVGA drivers.

- **Modern PyQt6 Interface:**
  - **Graphics Cards View:** Interactive GPU cards, driver options, version badges, one-click install/remove actions, and reboot notification.
  - **System Diagnostics View:** Detailed system information including desktop environment (X11/Wayland), kernel release, `glxinfo`, `vulkaninfo`, and raw PCI device output.
  - **Settings & Hybrid Control:** Configure NVIDIA PRIME / Optimus profiles (Offload, High Performance, Integrated) and manage PiSi package repositories or cache.
  - **Live Console Log:** Real-time colored execution logging with auto-scroll and file export options.

- **Demo / Simulation Mode:**
  - Allows testing UI functionality and workflows without system modification using the `--demo` command-line flag or the toggle button in the header bar.

---

## Installation & Build
```bash
# 1. Clone Repository
git clone https://github.com/TeknoAnka/pisidi.git
cd pisidi

# 2. Start Build
chmod +x ./build-pisi.sh
sudo ./build-pisi.sh

# 3. Install Package
sudo pisi install ./pisidi-*-x86_64.pisi
```

---

## Requirements

- Python 3.8+
- PyQt6
- `pisi` package manager (on Pisi Linux / LupuS)
- System utilities: `lspci` (`pciutils`), `glxinfo` (`mesa-utils`), `vulkaninfo` (`vulkan-tools`)
