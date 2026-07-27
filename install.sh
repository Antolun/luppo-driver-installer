#!/bin/bash
# Graphics Driver Installer Installation & Uninstallation Script for Pisi Linux / LupuS

set -e

INSTALL_DIR="/usr/share/graphics-driver-installer"
BIN_PATH="/usr/bin/graphics-driver-installer"
DESKTOP_PATH="/usr/share/applications/graphics-driver-installer.desktop"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        echo "Error: This script must be run with root privileges."
        echo "Please run: sudo $0 $1"
        exit 1
    fi
}

do_install() {
    check_root "install"
    echo "Installing Graphics Driver Installer..."

    # 1. Create installation directory and copy application files
    echo " -> Copying application files to $INSTALL_DIR..."
    mkdir -p "$INSTALL_DIR"
    cp -r "$SCRIPT_DIR/main.py" \
          "$SCRIPT_DIR/config.py" \
          "$SCRIPT_DIR/i18n.py" \
          "$SCRIPT_DIR/models" \
          "$SCRIPT_DIR/backend" \
          "$SCRIPT_DIR/ui" \
          "$SCRIPT_DIR/assets" \
          "$INSTALL_DIR/"

    chmod -R 755 "$INSTALL_DIR"

    # 2. Create terminal launcher binary in /usr/bin/graphics-driver-installer
    echo " -> Creating terminal command ($BIN_PATH)..."
    cat << 'EOF' > "$BIN_PATH"
#!/bin/bash
exec python3 /usr/share/graphics-driver-installer/main.py "$@"
EOF
    chmod 755 "$BIN_PATH"

    # 4. Create desktop menu entry
    echo " -> Creating desktop menu entry ($DESKTOP_PATH)..."
    cat << 'EOF' > "$DESKTOP_PATH"
[Desktop Entry]
Type=Application
Name=Graphics Driver Installer
GenericName=GPU Driver Installer
Comment=Install and manage GPU drivers on Pisi Linux / LupuS
Exec=graphics-driver-installer %u
Icon=/usr/share/graphics-driver-installer/assets/graphics-driver-installer.png
Terminal=false
Categories=Settings;HardwareSettings;System;
StartupNotify=true
EOF
    chmod 644 "$DESKTOP_PATH"

    # 5. Update system icon & desktop database if available
    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
        gtk-update-icon-cache -f /usr/share/icons/hicolor 2>/dev/null || true
    fi
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database /usr/share/applications 2>/dev/null || true
    fi

    echo ""
    echo "Installation completed successfully!"
    echo "You can now run 'graphics-driver-installer' from terminal or application menu."
}

do_uninstall() {
    check_root "uninstall"
    echo "Uninstalling Graphics Driver Installer..."

    # 1. Remove installation directory
    if [ -d "$INSTALL_DIR" ]; then
        echo " -> Removing $INSTALL_DIR..."
        rm -rf "$INSTALL_DIR"
    fi

    # 2. Remove terminal launcher
    if [ -f "$BIN_PATH" ]; then
        echo " -> Removing $BIN_PATH..."
        rm -f "$BIN_PATH"
    fi

    # 3. Remove desktop entry
    if [ -f "$DESKTOP_PATH" ]; then
        echo " -> Removing $DESKTOP_PATH..."
        rm -f "$DESKTOP_PATH"
    fi

    # 4. Remove icons
    echo " -> Removing application icons..."
    rm -f "/usr/share/graphics-driver-installer/assets/graphics-driver-installer.png"

    # 5. Update system databases
    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
        gtk-update-icon-cache -f /usr/share/icons/hicolor 2>/dev/null || true
    fi
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database /usr/share/applications 2>/dev/null || true
    fi

    echo ""
    echo "Uninstallation completed successfully!"
}

case "$1" in
    install)
        do_install
        ;;
    uninstall)
        do_uninstall
        ;;
    reinstall)
        do_uninstall
        do_install
        ;;
    *)
        echo "Graphics Driver Installer Script"
        echo ""
        echo "Usage:"
        echo "  sudo ./install.sh install    - Install application to system"
        echo "  sudo ./install.sh uninstall  - Uninstall application from system"
        echo "  sudo ./install.sh reinstall  - Reinstall application"
        exit 1
        ;;
esac
