from __future__ import annotations
import os
from PySide6.QtGui import QIcon
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _refresh_theme_icon_if_needed(self) -> None:
    try:
        if os.name != "nt":
            return

        next_theme_value = self._resolve_theme_flag_fn()
        if next_theme_value == self._theme_is_light:
            return

        next_icon_path = self._resolve_icon_for_theme_fn(next_theme_value)
        if not next_icon_path or not os.path.exists(next_icon_path):
            return

        if next_icon_path == self._current_icon_path:
            self._theme_is_light = next_theme_value
            return

        next_icon = QIcon(next_icon_path)
        if next_icon.isNull():
            return

        self._theme_is_light = next_theme_value
        self._current_icon_path = next_icon_path
        self._app_instance.setWindowIcon(next_icon)
        self.setWindowIcon(next_icon)

    except Exception as exc:
        logger.error(f"Erro ao atualizar ícone para tema: {exc}")
