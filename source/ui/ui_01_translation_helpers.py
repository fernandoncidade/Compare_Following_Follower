from __future__ import annotations
from PySide6.QtCore import QCoreApplication


def tr(text: str) -> str:
    try:
        return QCoreApplication.translate("App", text)

    except Exception:
        return text
