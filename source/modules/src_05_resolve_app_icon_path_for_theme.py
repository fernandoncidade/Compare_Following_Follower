from __future__ import annotations
from .src_04_resolve_exact_icon_path import _resolve_exact_icon_path
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _resolve_app_icon_path_for_theme(is_light_theme: bool | None) -> str | None:
    try:
        from source.modules import source as core

        if is_light_theme is True:
            preferred = core.APP_ICON_FILENAME_CLEAR
            secondary = core.APP_ICON_FILENAME_DARK

        elif is_light_theme is False:
            preferred = core.APP_ICON_FILENAME_DARK
            secondary = core.APP_ICON_FILENAME_CLEAR

        else:
            preferred = core.APP_ICON_FILENAME_CLEAR
            secondary = core.APP_ICON_FILENAME_DARK

        return _resolve_exact_icon_path(preferred) or _resolve_exact_icon_path(secondary)

    except Exception as exc:
        logger.error(f"Erro ao resolver caminho do ícone do aplicativo para o tema: {exc}")
