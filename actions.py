#!/usr/bin/python3
from luppo.actionsapi import luppotools
from luppo.actionsapi import shelltools
import os

WorkDir = "."

def build():
    pass

def install():
    src_dir = os.environ.get("LDI_SRC_DIR", os.getcwd())

    # Copy application main entry and package directory
    main_py = os.path.join(src_dir, "main.py")
    if not os.path.isfile(main_py):
        main_py = "main.py"
    if os.path.isfile(main_py):
        luppotools.insinto("/usr/share/luppo-driver-installer", main_py)

    ldi_dir = os.path.join(src_dir, "src")
    if not os.path.isdir(ldi_dir):
        ldi_dir = "src"
    if os.path.isdir(ldi_dir):
        luppotools.insinto("/usr/share/luppo-driver-installer", ldi_dir)

    # Launcher script (/usr/bin/luppo-driver-installer)
    launcher_path = os.path.join(src_dir, "luppo-driver-installer")
    if not os.path.isfile(launcher_path):
        launcher_path = "luppo-driver-installer"
    
    if not os.path.isfile(launcher_path):
        with open("luppo-driver-installer", "w") as f:
            f.write("#!/bin/bash\nexec python3 /usr/share/luppo-driver-installer/main.py \"$@\"\n")
        os.chmod("luppo-driver-installer", 0o755)
        launcher_path = "luppo-driver-installer"

    luppotools.dobin(launcher_path)

    # Desktop entry
    desktop_path = os.path.join(src_dir, "luppo-driver-installer.desktop")
    if not os.path.isfile(desktop_path):
        desktop_path = "luppo-driver-installer.desktop"
    if os.path.isfile(desktop_path):
        luppotools.insinto("/usr/share/applications", desktop_path)

    # App icon
    icon_path = os.path.join(src_dir, "src", "assets", "favicon.png")
    if not os.path.isfile(icon_path):
        icon_path = os.path.join("src", "assets", "favicon.png")
    if os.path.isfile(icon_path):
        luppotools.insinto("/usr/share/icons/hicolor/128x128/apps", icon_path, "luppo-driver-installer.png")

    # Documentation & License
    readme_path = os.path.join(src_dir, "README.md")
    if not os.path.isfile(readme_path):
        readme_path = "README.md"
    if os.path.isfile(readme_path):
        luppotools.dodoc(readme_path)

    license_path = os.path.join(src_dir, "LICENSE")
    if not os.path.isfile(license_path):
        license_path = "LICENSE"
    if os.path.isfile(license_path):
        luppotools.dodoc(license_path)
