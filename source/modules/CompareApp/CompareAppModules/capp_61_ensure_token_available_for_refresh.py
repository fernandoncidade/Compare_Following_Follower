from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _ensure_token_available_for_refresh(self, user: str) -> bool:
    try:
        if self._get_token_fn():
            return True

        cached = self._load_cached_data_for_user(user, include_expired=True)

        if cached is not None:
            return True

        return self._request_and_persist_github_token()

    except Exception as exc:
        logger.error(f"Erro ao validar token para atualização: {exc}")
        return False
