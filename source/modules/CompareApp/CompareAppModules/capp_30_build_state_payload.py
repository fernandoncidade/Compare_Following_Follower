from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _build_state_payload(self, user: str, saved_at_epoch: float, values: list[str]) -> dict[str, Any]:
    try:
        followers = sorted({item.strip().lower() for item in self._followers_values if isinstance(item, str) and item.strip()})
        following = sorted({item.strip().lower() for item in self._following_values if isinstance(item, str) and item.strip()})

        if not followers:
            followers = sorted({item.strip().lower() for item in set(self._non_following_values).union(self._mutual_values) if isinstance(item, str) and item.strip()})

        if not following:
            following = sorted({item.strip().lower() for item in set(self._non_followers_values).union(self._mutual_values) if isinstance(item, str) and item.strip()})

        return {
            "user": user,
            "saved_at_epoch": float(saved_at_epoch),
            "followers": followers,
            "following": following,
            "nao_retribuem": sorted({item.strip().lower() for item in self._non_followers_values if isinstance(item, str) and item.strip()}),
            "eu_nao_retribuo": sorted({item.strip().lower() for item in self._non_following_values if isinstance(item, str) and item.strip()}),
            "mutuos": sorted({item.strip().lower() for item in self._mutual_values if isinstance(item, str) and item.strip()}),
            "nao_me_seguem_mais": sorted({item.strip().lower() for item in values if isinstance(item, str) and item.strip()}),
        }

    except Exception as exc:
        logger.error(f"Erro ao construir payload de estado para exportação: {exc}")
        return {
            "user": user,
            "saved_at_epoch": float(saved_at_epoch),
            "followers": [],
            "following": [],
            "nao_retribuem": [],
            "eu_nao_retribuo": [],
            "mutuos": [],
            "nao_me_seguem_mais": [],
        }
