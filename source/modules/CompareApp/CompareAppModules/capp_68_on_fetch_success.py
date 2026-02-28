from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_fetch_success(self, data: Any) -> None:
    try:
        if data is None:
            raise self._config_error_cls("Dados de comparação vazios.")

        if not hasattr(data, "followers") or not hasattr(data, "following"):
            raise self._config_error_cls("Dados de comparação inválidos.")

        self._set_loading(False)
        no_longer_follow_me_values = self._calculate_new_non_followers(data)
        normalized_followers = sorted({item.strip().lower() for item in data.followers if isinstance(item, str) and item.strip()})
        normalized_following = sorted({item.strip().lower() for item in data.following if isinstance(item, str) and item.strip()})
        self._set_counts_values(following=len(normalized_following), followers=len(normalized_followers), non_following=len(data.eu_nao_retribuo), mutuals=len(data.mutuos), no_longer_follow_me=len(no_longer_follow_me_values),)
        self._set_cache_status_from_data(data)
        self._set_rate_status_info(data.rate_limit)
        self._set_requests_used(data.requests_made)
        self._update_relationship_tab_counts(followers=len(normalized_followers), following=len(normalized_following),)
        self._update_primary_tab_counts(non_followers=len(data.nao_retribuem), non_following=len(data.eu_nao_retribuo), mutuals=len(data.mutuos),)
        self._followers_values = list(normalized_followers)
        self._following_values = list(normalized_following)
        self._non_followers_values = list(data.nao_retribuem)
        self._non_following_values = list(data.eu_nao_retribuo)
        self._mutual_values = list(data.mutuos)
        self._fill_text(self.followers_text, self._followers_values)
        self._fill_text(self.following_text, self._following_values)
        self._fill_text(self.nao_retribuem_text, self._non_followers_values)
        self._fill_text(self.eu_nao_retribuo_text, self._non_following_values)
        self._fill_text(self.mutuos_text, self._mutual_values)
        self._fill_new_non_followers(no_longer_follow_me_values)

    except Exception as exc:
        user_value = getattr(data, "user", self.user_input.text().strip() or "<desconhecido>")
        logger.error(f"Erro ao processar dados de comparação para o usuário '{user_value}': {exc}")
        self._on_fetch_error(exc)
