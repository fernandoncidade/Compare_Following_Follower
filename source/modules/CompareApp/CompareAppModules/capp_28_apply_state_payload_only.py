from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _apply_state_payload_only(self, payload: dict[str, Any]) -> None:
    try:
        followers = {item.strip().lower() for item in payload.get("followers", []) if isinstance(item, str) and item.strip()}
        following = {item.strip().lower() for item in payload.get("following", []) if isinstance(item, str) and item.strip()}
        values = [item.strip().lower() for item in payload.get("nao_retribuem", []) if isinstance(item, str) and item.strip()]
        no_longer_follow_me = sorted({item.strip().lower() for item in payload.get("nao_me_seguem_mais", []) if isinstance(item, str) and item.strip()})

        self._followers_values = sorted(followers)
        self._following_values = sorted(following)

        if followers or following:
            self._non_followers_values = sorted(following - followers)
            self._non_following_values = sorted(followers - following)
            self._mutual_values = sorted(following & followers)

        else:
            self._non_followers_values = values
            self._non_following_values = []
            self._mutual_values = []
            self._followers_values = sorted({item.strip().lower() for item in set(self._non_following_values).union(self._mutual_values) if isinstance(item, str) and item.strip()})
            self._following_values = sorted({item.strip().lower() for item in set(self._non_followers_values).union(self._mutual_values) if isinstance(item, str) and item.strip()})

        self._set_counts_values(None, None, None, None, None)
        self._set_cache_status("none")
        self._set_rate_status_unavailable()
        self._set_requests_used(None)
        self._update_relationship_tab_counts(followers=len(self._followers_values), following=len(self._following_values),)
        self._update_primary_tab_counts(non_followers=len(self._non_followers_values), non_following=len(self._non_following_values), mutuals=len(self._mutual_values),)
        self._fill_text(self.followers_text, self._followers_values)
        self._fill_text(self.following_text, self._following_values)
        self._fill_text(self.nao_retribuem_text, self._non_followers_values)
        self._fill_text(self.eu_nao_retribuo_text, self._non_following_values)
        self._fill_text(self.mutuos_text, self._mutual_values)
        self._fill_new_non_followers(no_longer_follow_me or values)

    except Exception as exc:
        logger.error(f"Erro ao aplicar payload de estado: {exc}")
