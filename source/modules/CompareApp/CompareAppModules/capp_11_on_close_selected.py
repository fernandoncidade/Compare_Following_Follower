from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_close_selected(self) -> None:
    try:
        self.close()

    except Exception as exc:
        logger.error(f"Erro ao executar ação Fechar: {exc}")
