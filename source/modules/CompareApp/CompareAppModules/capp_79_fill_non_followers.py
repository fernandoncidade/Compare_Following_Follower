from __future__ import annotations
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _fill_non_followers(self, values: list[str]) -> None:
    try:
        self._non_followers_values = list(values)
        self.nao_seguidores_list.blockSignals(True)
        self.nao_seguidores_list.clear()

        for login in values:
            item = QListWidgetItem(login)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.Unchecked)
            self.nao_seguidores_list.addItem(item)

        self.nao_seguidores_list.blockSignals(False)
        self._update_unfollow_button_state()
        self._update_primary_tab_counts(
            non_followers=len(values),
            non_following=self._tab_non_following_count,
            mutuals=self._tab_mutuals_count,
        )

    except Exception as exc:
        logger.error(f"Erro ao preencher lista de não seguidores: {exc}")
