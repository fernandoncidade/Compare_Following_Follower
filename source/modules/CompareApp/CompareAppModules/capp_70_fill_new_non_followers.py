from __future__ import annotations
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _fill_new_non_followers(self, values: list[str]) -> None:
    try:
        self.novos_nao_seguidores_list.blockSignals(True)
        self.novos_nao_seguidores_list.clear()

        for login in values:
            item = QListWidgetItem(login)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.Unchecked)
            self.novos_nao_seguidores_list.addItem(item)

        self.novos_nao_seguidores_list.blockSignals(False)
        self._update_unfollow_button_state()
        self._update_new_non_followers_count(len(values))

    except Exception as exc:
        logger.error(f"Erro ao preencher lista de novos não seguidores: {exc}")
