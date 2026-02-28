from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _set_cache_status_from_data(self, data: Any) -> None:
    try:
        if data.from_cache:
            age = int(data.cache_age_seconds or 0)
            self._set_cache_status("from_cache", age=age)
            return

        self._set_cache_status("from_graphql", requests=int(data.requests_made))

    except Exception as exc:
        logger.error(f"Erro ao atualizar status de cache com dados: {exc}")
