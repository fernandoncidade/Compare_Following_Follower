from __future__ import annotations
import time
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _create_compare_data_from_cache_payload(self, payload: dict[str, Any]) -> Any:
    try:
        from source.modules import source as core

        saved_at_epoch = float(payload.get("saved_at_epoch", 0.0))
        age_seconds = max(time.time() - saved_at_epoch, 0.0)

        return core.CompareData(
            user=payload.get("user", ""),
            followers={item.strip().lower() for item in payload.get("followers", []) if isinstance(item, str) and item.strip()},
            following={item.strip().lower() for item in payload.get("following", []) if isinstance(item, str) and item.strip()},
            rate_limit=core.RateLimitInfo.from_payload(payload.get("rate_limit")),
            requests_made=0,
            from_cache=True,
            cache_age_seconds=age_seconds,
            nao_me_seguem_mais=sorted({item.strip().lower() for item in payload.get("nao_me_seguem_mais", []) if isinstance(item, str) and item.strip()}),
        )

    except Exception as exc:
        logger.error(f"Erro ao criar CompareData a partir do cache importado: {exc}")
        raise
