from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _refresh_tab_titles(self) -> None:
    try:
        self._set_tab_count(self._tab_followers_index, self._tab_title_followers, self._tab_followers_count)
        self._set_tab_count(self._tab_following_index, self._tab_title_following, self._tab_following_count)
        self._set_tab_count(self._tab_non_followers_index, self._tab_title_non_followers, self._tab_non_followers_count)
        self._set_tab_count(self._tab_non_following_index, self._tab_title_non_following, self._tab_non_following_count)
        self._set_tab_count(self._tab_mutuals_index, self._tab_title_mutuals, self._tab_mutuals_count)
        self._set_tab_count(self._tab_new_non_followers_index, self._tab_title_new_non_followers, self._tab_new_non_followers_count)

    except Exception as exc:
        logger.error(f"Erro ao atualizar títulos das abas: {exc}")
