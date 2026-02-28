from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _set_tab_count(self, tab_index: int, title: str, count: int) -> None:
    try:
        if self.tabs is None or tab_index < 0:
            return

        self.tabs.setTabText(tab_index, self._format_tab_title(title, count))

    except Exception as exc:
        logger.error(f"Erro ao atualizar contagem da aba '{title}': {exc}")
