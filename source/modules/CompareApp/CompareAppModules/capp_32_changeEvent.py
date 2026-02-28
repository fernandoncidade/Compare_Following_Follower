from __future__ import annotations
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QWidget
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def changeEvent(self, event: QEvent) -> None:
    try:
        if event.type() == QEvent.LanguageChange:
            self._apply_translations()

    except Exception as exc:
        logger.error(f"Erro ao processar evento de mudança de idioma: {exc}")

    QWidget.changeEvent(self, event)
