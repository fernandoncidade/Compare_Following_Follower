from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _connect_translation_manager(self) -> None:
    try:
        if self._translation_manager is None:
            return

        self._translation_manager.idioma_alterado.connect(self._on_language_changed)

    except Exception as exc:
        logger.error(f"Erro ao conectar gerenciador de tradução: {exc}")
