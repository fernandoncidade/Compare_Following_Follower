from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_language_selected(self, language_code: str) -> None:
    try:
        if self._translation_manager is None:
            return

        if language_code == self._get_current_language_code():
            return

        self._translation_manager.definir_idioma(language_code)

    except Exception as exc:
        logger.error(f"Erro ao alterar idioma para '{language_code}': {exc}")
