"""
Console Log Viewer Component with QSvgRenderer icons.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QCheckBox, QLabel, QFileDialog, QSizePolicy
from PyQt6.QtCore import Qt, QDateTime, QSize
from ui.icon_helper import get_icon, create_icon_label
from i18n import tr


class LogViewer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Toolbar
        tool_layout = QHBoxLayout()
        tool_layout.setSpacing(8)

        tool_layout.addWidget(create_icon_label("terminal.svg", 18))
        
        lbl_title = QLabel(tr("log_title"))
        lbl_title.setStyleSheet("font-weight: 700; font-size: 12px; color: #f8fafc;")

        tool_layout.addWidget(lbl_title)
        tool_layout.addStretch()

        self.cb_autoscroll = QCheckBox(tr("log_autoscroll"))
        self.cb_autoscroll.setChecked(True)
        tool_layout.addWidget(self.cb_autoscroll)

        btn_clear = QPushButton(tr("log_clear"))
        btn_clear.setIcon(get_icon("trash.svg", 16, 16))
        btn_clear.setIconSize(QSize(16, 16))
        btn_clear.setObjectName("btn_secondary")
        btn_clear.clicked.connect(self.clear_logs)
        tool_layout.addWidget(btn_clear)

        btn_save = QPushButton(tr("log_save"))
        btn_save.setIcon(get_icon("save.svg", 16, 16))
        btn_save.setIconSize(QSize(16, 16))
        btn_save.setObjectName("btn_secondary")
        btn_save.clicked.connect(self.save_logs)
        tool_layout.addWidget(btn_save)

        layout.addLayout(tool_layout)

        # Text Console
        self.console = QTextEdit()
        self.console.setObjectName("log_console")
        self.console.setReadOnly(True)
        self.console.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.console, stretch=1)

    def append_log(self, text: str):
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        
        formatted = text
        if "[HATA]" in text or "Hata" in text or "[ERROR]" in text or "FAIL" in text:
            formatted = f"<span style='color:#ef4444;'>[{timestamp}] {text}</span>"
        elif "[PISI]" in text:
            formatted = f"<span style='color:#38bdf8;'>[{timestamp}] {text}</span>"
        elif "[DONANIM]" in text or "[HARDWARE]" in text:
            formatted = f"<span style='color:#10b981;'>[{timestamp}] {text}</span>"
        elif "[SİSTEM]" in text or "[SYSTEM]" in text:
            formatted = f"<span style='color:#a855f7;'>[{timestamp}] {text}</span>"
        else:
            formatted = f"<span style='color:#94a3b8;'>[{timestamp}] {text}</span>"

        self.console.append(formatted)

        if self.cb_autoscroll.isChecked():
            sb = self.console.verticalScrollBar()
            sb.setValue(sb.maximum())

    def clear_logs(self):
        self.console.clear()

    def save_logs(self):
        file_path, _ = QFileDialog.getSaveFileName(self, tr("log_save_dialog_title"), "pisi_graphics_installer.log", "Log Files (*.log);;All Files (*)")
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.console.toPlainText())
            except Exception as e:
                self.append_log(tr("log_save_error", error=str(e)))
