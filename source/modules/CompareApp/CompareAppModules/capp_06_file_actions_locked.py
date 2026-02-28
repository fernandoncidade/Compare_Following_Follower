from __future__ import annotations
from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _file_actions_locked(self) -> bool:
    try:
        if not self._is_loading:
            return False

        QMessageBox.warning(
            self,
            self._resolve_label("Ação indisponível", "Action unavailable"),
            self._resolve_label(
                "Aguarde o término da atualização para usar este comando.",
                "Wait for the refresh to finish before using this command.",
            ),
        )
        return True

    except Exception as exc:
        logger.error(f"Erro ao validar bloqueio de ação de arquivo: {exc}")
        return False
