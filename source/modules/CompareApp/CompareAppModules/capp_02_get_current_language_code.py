from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _get_current_language_code(self) -> str:
    try:
        if self._translation_manager is None:
            return "pt_BR"

        current_language = self._translation_manager.obter_idioma_atual()

        if isinstance(current_language, str) and current_language in {"pt_BR", "en_US"}:
            return current_language

        return "pt_BR"

    except Exception as exc:
        logger.error(f"Erro ao obter idioma atual: {exc}")
        return "pt_BR"
