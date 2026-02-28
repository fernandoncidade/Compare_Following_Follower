from __future__ import annotations
from PySide6.QtWidgets import QPlainTextEdit
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _fill_text(self, widget: QPlainTextEdit, values: list[str]) -> None:
    try:
        widget.setPlainText("\n".join(values) if values else self._tr("(ninguém)"))

    except Exception as exc:
        logger.error(f"Erro ao preencher texto do widget: {exc}")
