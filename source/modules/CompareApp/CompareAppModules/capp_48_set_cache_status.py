from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _set_cache_status(self, mode: str, **payload: Any) -> None:
    try:
        self._cache_status_mode = mode
        self._cache_status_payload = payload
        self.cache_label.setText(self._render_cache_status())

    except Exception as exc:
        logger.error(f"Erro ao atualizar status de cache: {exc}")
