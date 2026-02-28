from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_language_changed(self, language_code: str) -> None:
    try:
        if self._menu_bar_ui is not None:
            self._menu_bar_ui.set_checked_language(language_code)

        self._apply_translations()

    except Exception as exc:
        logger.error(f"Erro ao processar mudança de idioma: {exc}")
