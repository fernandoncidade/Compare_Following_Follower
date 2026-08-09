from __future__ import annotations
from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _configure_non_followers_tab(self, tabs: QTabWidget) -> int:
    try:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        layout.addWidget(self.nao_seguidores_list, stretch=1)
        layout.addWidget(self.unfollow_non_followers_button)
        return tabs.addTab(container, self._format_tab_title(self._tab_title_non_followers, 0))

    except Exception as exc:
        logger.error(f"Erro ao configurar aba de não seguidores: {exc}")
        return -1
