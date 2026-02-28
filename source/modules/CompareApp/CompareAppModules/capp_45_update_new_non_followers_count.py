from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _update_new_non_followers_count(self, new_non_followers: int) -> None:
    try:
        self._tab_new_non_followers_count = max(new_non_followers, 0)
        self._refresh_tab_titles()

    except Exception as exc:
        logger.error(f"Erro ao atualizar contagem da aba de novos não seguidores: {exc}")
