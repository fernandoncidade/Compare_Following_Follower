from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _load_cached_data_for_user(self, user: str, include_expired: bool) -> Any | None:
    try:
        normalized_user = user.strip()

        if not normalized_user:
            return None

        try:
            return self._load_cached_data_fn(normalized_user, include_expired=include_expired)

        except TypeError:
            return self._load_cached_data_fn(normalized_user)

    except Exception as exc:
        logger.error(
            f"Erro ao verificar cache para o usuário '{user}' (include_expired={include_expired}): {exc}"
        )
        return None
