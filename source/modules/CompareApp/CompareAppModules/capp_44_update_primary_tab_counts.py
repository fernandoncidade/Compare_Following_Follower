from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _update_primary_tab_counts(self, non_followers: int, non_following: int, mutuals: int) -> None:
    try:
        self._tab_non_followers_count = max(non_followers, 0)
        self._tab_non_following_count = max(non_following, 0)
        self._tab_mutuals_count = max(mutuals, 0)
        self._refresh_tab_titles()

    except Exception as exc:
        logger.error(f"Erro ao atualizar contagens das abas principais: {exc}")
