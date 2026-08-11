"""
UI Stylesheet (QSS) and Theme constants for PyQt6 modern dark design with auto-sizing support.
"""

MAIN_STYLE = """
/* Global Window & Font Settings */
QWidget {
    background-color: #0f172a;
    color: #f8fafc;
    font-family: 'Segoe UI', 'Ubuntu', 'Inter', sans-serif;
    font-size: 12px;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #1e293b;
    width: 6px;
    margin: 0px;
    border-radius: 3px;
}

QScrollBar::handle:vertical {
    background: #475569;
    min-height: 20px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: #6366f1;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Sidebar Navigation */
#sidebar {
    background-color: #1e293b;
    border-right: 1px solid #334155;
    min-width: 200px;
    max-width: 200px;
}

#nav_btn {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 6px;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    font-size: 12px;
}

#nav_btn:hover {
    background-color: #334155;
    color: #f8fafc;
}

#nav_btn:checked {
    background-color: #4f46e5;
    color: #ffffff;
    font-weight: 700;
}

/* Header Bar */
#header_bar {
    background-color: #1e293b;
    border-bottom: 1px solid #334155;
    padding: 8px 16px;
}

#app_title {
    font-size: 15px;
    font-weight: 800;
    color: #ffffff;
}

#app_subtitle {
    font-size: 11px;
    color: #94a3b8;
}

/* Cards & Containers - Compact Auto-Sizing */
.GPUCard {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 10px;
}

.GPUCard:hover {
    border: 1px solid #6366f1;
}

.DriverRow {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px 10px;
    margin-top: 6px;
}

.DriverRow:hover {
    border: 1px solid #475569;
}

/* Buttons */
QPushButton {
    background-color: #4f46e5;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    padding: 6px 12px;
    font-weight: 600;
    font-size: 12px;
}

QPushButton:hover {
    background-color: #6366f1;
}

QPushButton:pressed {
    background-color: #3730a3;
}

QPushButton:disabled {
    background-color: #334155;
    color: #64748b;
}

QPushButton#btn_danger {
    background-color: #dc2626;
}

QPushButton#btn_danger:hover {
    background-color: #ef4444;
}

QPushButton#btn_secondary {
    background-color: #334155;
    color: #f8fafc;
}

QPushButton#btn_secondary:hover {
    background-color: #475569;
}

QPushButton#btn_demo {
    background-color: #334155;
    color: #f8fafc;
}

QPushButton#btn_demo:hover {
    background-color: blue;
}

/* Badges */
.Badge {
    border-radius: 4px;
    padding: 3px 6px;
    font-size: 10px;
    font-weight: 700;
}

.BadgeNvidia {
    background-color: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid #10b981;
}

.BadgeAmd {
    background-color: rgba(244, 63, 94, 0.15);
    color: #f43f5e;
    border: 1px solid #f43f5e;
}

.BadgeIntel {
    background-color: rgba(59, 130, 246, 0.15);
    color: #3b82f6;
    border: 1px solid #3b82f6;
}

.BadgeRecommended {
    background-color: rgba(99, 102, 241, 0.15);
    color: #818cf8;
    border: 1px solid #6366f1;
}

/* Progress Bar */
QProgressBar {
    background-color: #0f172a;
    border: 1px solid transparent;
    border-radius: 4px;
    height: 8px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #818cf8);
    border-radius: 3px;
    border: 1px solid transparent;
}

/* Terminal Console Log Viewer */
#log_console {
    background-color: #020617;
    color: #38bdf8;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 11px;
    border: 1px solid #1e293b;
    border-radius: 6px;
    padding: 8px;
}

/* Combo Box & Inputs */
QComboBox {
    background-color: #0f172a;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 5px;
    padding: 5px 10px;
    font-size: 12px;
}

QComboBox::drop-down {
    border: none;
}
"""
