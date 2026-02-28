from __future__ import annotations
from PySide6.QtWidgets import QPlainTextEdit, QTabWidget
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _configure_tab(self, tabs: QTabWidget, title: str, widget: QPlainTextEdit) -> int:
    try:
        widget.setReadOnly(True)
        widget.setLineWrapMode(QPlainTextEdit.NoWrap)
        return tabs.addTab(widget, self._format_tab_title(title, 0))

    except Exception as exc:
        logger.error(f"Erro ao configurar aba '{title}': {exc}")
        return -1
