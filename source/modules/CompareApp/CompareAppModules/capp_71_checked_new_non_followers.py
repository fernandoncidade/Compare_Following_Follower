from __future__ import annotations
from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _checked_new_non_followers(self) -> list[str]:
    try:
        checked: list[str] = []

        for idx in range(self.novos_nao_seguidores_list.count()):
            item = self.novos_nao_seguidores_list.item(idx)

            if item.checkState() == Qt.Checked:
                checked.append(item.text())

        return checked

    except Exception as exc:
        logger.error(f"Erro ao obter itens selecionados de novos não seguidores: {exc}")
        return []
