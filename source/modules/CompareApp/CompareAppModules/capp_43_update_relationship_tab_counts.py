from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _update_relationship_tab_counts(self, followers: int, following: int) -> None:
    try:
        self._tab_followers_count = max(followers, 0)
        self._tab_following_count = max(following, 0)
        self._refresh_tab_titles()

    except Exception as exc:
        logger.error(f"Erro ao atualizar contagens das abas de seguidores/seguindo: {exc}")
