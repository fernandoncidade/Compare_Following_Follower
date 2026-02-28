from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _load_startup_cache(self, user: str) -> None:
    try:
        normalized_user = user.strip()

        if not normalized_user:
            self._fill_new_non_followers([])
            return

        try:
            cached = self._load_cached_data_fn(normalized_user, include_expired=True)

        except TypeError:
            cached = self._load_cached_data_fn(normalized_user)

        if cached is None:
            self._fill_new_non_followers([])
            return

        self._on_fetch_success(cached)

    except Exception as exc:
        logger.error(f"Erro ao carregar cache de inicialização para o usuário '{user}': {exc}")
