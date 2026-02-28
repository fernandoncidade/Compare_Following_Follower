from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _show_manual(self) -> None:
    try:
        from source.public.pub_01_ExibirPublic import exibir_manual

        exibir_manual(self)

    except Exception as exc:
        logger.error(f"Erro ao abrir Manual: {exc}")
