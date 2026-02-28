from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _set_counts_values(self, following: int | None, followers: int | None, non_following: int | None, mutuals: int | None, no_longer_follow_me: int | None,) -> None:
    try:
        self._counts_following = following
        self._counts_followers = followers
        self._counts_non_following = non_following
        self._counts_mutuals = mutuals
        self._counts_no_longer_follow_me = no_longer_follow_me
        self._render_counts_label()

    except Exception as exc:
        logger.error(f"Erro ao atualizar contagens do resumo: {exc}")
