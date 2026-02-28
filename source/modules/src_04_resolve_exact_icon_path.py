from __future__ import annotations
import os
from source.utils import get_icon_path, get_text_file_path
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _resolve_exact_icon_path(icon_filename: str) -> str | None:
    try:
        icon_path = get_icon_path(icon_filename)

        if icon_path and os.path.exists(icon_path):
            return icon_path

        fallback = get_text_file_path(icon_filename, folder="icons")

        if fallback and os.path.exists(fallback):
            return fallback

        return None

    except Exception as exc:
        logger.error(f"Erro ao resolver caminho do ícone {icon_filename}: {exc}")
