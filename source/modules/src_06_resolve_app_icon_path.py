from __future__ import annotations
from .src_03_read_windows_light_theme_flag import _read_windows_light_theme_flag
from .src_05_resolve_app_icon_path_for_theme import _resolve_app_icon_path_for_theme
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _resolve_app_icon_path() -> str | None:
    try:
        return _resolve_app_icon_path_for_theme(_read_windows_light_theme_flag())

    except Exception as exc:
        logger.error(f"Erro ao resolver caminho do ícone do aplicativo: {exc}")
