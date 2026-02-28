from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _clear_reported_data(self) -> None:
    try:
        self._set_counts_values(None, None, None, None, None)
        self._set_cache_status("none")
        self._set_rate_status_unavailable()
        self._set_requests_used(None)
        self._followers_values = []
        self._following_values = []
        self._non_followers_values = []
        self._non_following_values = []
        self._mutual_values = []
        self._update_relationship_tab_counts(followers=0, following=0)
        self._update_primary_tab_counts(non_followers=0, non_following=0, mutuals=0)
        self._fill_text(self.followers_text, self._followers_values)
        self._fill_text(self.following_text, self._following_values)
        self._fill_text(self.nao_retribuem_text, self._non_followers_values)
        self._fill_text(self.eu_nao_retribuo_text, self._non_following_values)
        self._fill_text(self.mutuos_text, self._mutual_values)
        self._fill_new_non_followers([])

    except Exception as exc:
        logger.error(f"Erro ao limpar dados reportados: {exc}")
