from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _parse_import_payload(self, payload: Any) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    try:
        if not isinstance(payload, dict):
            return None, None

        bundle_cache = self._normalize_cache_payload(payload.get("cache"))
        bundle_state = self._normalize_state_payload(payload.get("state"))

        if bundle_cache is None:
            bundle_cache = self._normalize_cache_payload(payload.get("atual"))

        if bundle_state is None:
            bundle_state = self._normalize_state_payload(payload.get("antigo"))

        if bundle_cache is not None or bundle_state is not None:
            return bundle_cache, bundle_state

        cache_payload = self._normalize_cache_payload(payload)
        if cache_payload is not None:
            return cache_payload, None

        state_payload = self._normalize_state_payload(payload)
        if state_payload is not None:
            return None, state_payload

        return None, None

    except Exception as exc:
        logger.error(f"Erro ao interpretar payload importado: {exc}")
        return None, None
