from __future__ import annotations
import os
from PySide6.QtCore import QTimer
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _start_theme_icon_watcher(self) -> None:
    try:
        if os.name != "nt":
            return

        self._theme_icon_timer = QTimer(self)
        self._theme_icon_timer.setInterval(1200)
        self._theme_icon_timer.timeout.connect(self._refresh_theme_icon_if_needed)
        self._theme_icon_timer.start()

    except Exception as exc:
        logger.error(f"Erro ao iniciar verificador de tema para ícone: {exc}")
