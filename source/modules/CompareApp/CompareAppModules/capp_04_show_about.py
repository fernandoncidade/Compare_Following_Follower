from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _show_about(self) -> None:
    try:
        from source.ui.ui_03_exibir_sobre import exibir_sobre

        exibir_sobre(self)

    except Exception as exc:
        logger.error(f"Erro ao abrir Sobre: {exc}")
