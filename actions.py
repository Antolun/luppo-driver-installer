#!/usr/bin/python3
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
import os

WorkDir = "."

def build():
    pass

def install():
    src_dir = os.environ.get("PISIDI_SRC_DIR", os.getcwd())

    # Copy application main entry and package directory
    main_py = os.path.join(src_dir, "main.py")
    if not os.path.isfile(main_py):
        main_py = "main.py"
    if os.path.isfile(main_py):
        pisitools.insinto("/usr/share/pisidi", main_py)

    pisidi_dir = os.path.join(src_dir, "pisidi")
    if not os.path.isdir(pisidi_dir):
        pisidi_dir = "pisidi"
    if os.path.isdir(pisidi_dir):
        pisitools.insinto("/usr/share/pisidi", pisidi_dir)

    # Launcher script (/usr/bin/pisidi)
    launcher_path = os.path.join(src_dir, "pisidi")
    if not os.path.isfile(launcher_path):
        launcher_path = "pisidi"
    
    if not os.path.isfile(launcher_path):
        with open("pisidi", "w") as f:
            f.write("#!/bin/bash\nexec python3 /usr/share/pisidi/main.py \"$@\"\n")
        os.chmod("pisidi", 0o755)
        launcher_path = "pisidi"

    pisitools.dobin(launcher_path)

    # Desktop entry
    desktop_path = os.path.join(src_dir, "com.antolun.pisidi.desktop")
    if not os.path.isfile(desktop_path):
        desktop_path = "com.antolun.pisidi.desktop"
    if os.path.isfile(desktop_path):
        pisitools.insinto("/usr/share/applications", desktop_path)

    # App icon
    icon_path = os.path.join(src_dir, "pisidi", "assets", "pisidi.png")
    if not os.path.isfile(icon_path):
        icon_path = os.path.join("pisidi", "assets", "pisidi.png")
    if os.path.isfile(icon_path):
        pisitools.insinto("/usr/share/icons/hicolor/128x128/apps", icon_path, "pisidi.png")

    # Documentation & License
    readme_path = os.path.join(src_dir, "README.md")
    if not os.path.isfile(readme_path):
        readme_path = "README.md"
    if os.path.isfile(readme_path):
        pisitools.dodoc(readme_path)

    license_path = os.path.join(src_dir, "LICENSE")
    if not os.path.isfile(license_path):
        license_path = "LICENSE"
    if os.path.isfile(license_path):
        pisitools.dodoc(license_path)
