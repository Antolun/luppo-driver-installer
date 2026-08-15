"""
Icon helper using QSvgRenderer for high-precision vector SVG rendering in PyQt6.
"""

import os
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QSize, Qt, QRectF

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


def get_pixmap(name: str, width: int = 24, height: int = 24) -> QPixmap:
    """Renders SVG file at exact width and height using QSvgRenderer within target bounds."""
    path = os.path.join(ASSETS_DIR, name)
    if not os.path.exists(path):
        return QPixmap()

    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

    renderer = QSvgRenderer(path)
    if renderer.isValid():
        margin = max(0.5, min(width, height) * 0.04)
        target_rect = QRectF(margin, margin, float(width) - 2 * margin, float(height) - 2 * margin)
        renderer.render(painter, target_rect)
    painter.end()

    return pixmap


def get_icon(name: str, width: int = 20, height: int = 20) -> QIcon:
    """Returns a QIcon created from vector SVG at target dimensions."""
    pix = get_pixmap(name, width, height)
    return QIcon(pix)


def create_icon_label(icon_name: str, size: int = 18) -> QLabel:
    """Creates a QLabel displaying a high-resolution vector SVG icon with zero margin."""
    lbl = QLabel()
    pix = get_pixmap(icon_name, size, size)
    lbl.setPixmap(pix)
    lbl.setFixedSize(size, size)
    lbl.setContentsMargins(0, 0, 0, 0)
    lbl.setStyleSheet("padding: 0px; margin: 0px; border: none; background: transparent;")
    lbl.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    return lbl
