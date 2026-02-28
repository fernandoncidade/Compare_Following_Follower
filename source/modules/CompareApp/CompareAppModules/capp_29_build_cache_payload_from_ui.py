from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _build_cache_payload_from_ui(self, user: str, saved_at_epoch: float) -> dict[str, Any]:
    try:
        followers = sorted({item.strip().lower() for item in self._followers_values if isinstance(item, str) and item.strip()})
        following = sorted({item.strip().lower() for item in self._following_values if isinstance(item, str) and item.strip()})

        if not followers:
            followers = sorted({item.strip().lower() for item in set(self._non_following_values).union(self._mutual_values) if isinstance(item, str) and item.strip()})

        if not following:
            following = sorted({item.strip().lower() for item in set(self._non_followers_values).union(self._mutual_values) if isinstance(item, str) and item.strip()})

        nao_me_seguem_mais: list[str] = []

        for idx in range(self.novos_nao_seguidores_list.count()):
            item = self.novos_nao_seguidores_list.item(idx)

            if item is None:
                continue

            text = item.text()

            if isinstance(text, str):
                normalized_text = text.strip().lower()

                if normalized_text:
                    nao_me_seguem_mais.append(normalized_text)

        rate_info = self._rate_status_info
        reset_at = getattr(rate_info, "reset_at", None)

        return {
            "user": user,
            "saved_at_epoch": float(saved_at_epoch),
            "followers": followers,
            "following": following,
            "nao_retribuem": sorted({item.strip().lower() for item in self._non_followers_values if isinstance(item, str) and item.strip()}),
            "eu_nao_retribuo": sorted({item.strip().lower() for item in self._non_following_values if isinstance(item, str) and item.strip()}),
            "mutuos": sorted({item.strip().lower() for item in self._mutual_values if isinstance(item, str) and item.strip()}),
            "nao_me_seguem_mais": sorted({item.strip().lower() for item in nao_me_seguem_mais if isinstance(item, str) and item.strip()}),
            "rate_limit": {
                "remaining": self._to_int_or_none(getattr(rate_info, "remaining", None)),
                "limit": self._to_int_or_none(getattr(rate_info, "limit", None)),
                "cost": self._to_int_or_none(getattr(rate_info, "cost", None)),
                "resetAt": reset_at if isinstance(reset_at, str) else None,
            },
        }

    except Exception as exc:
        logger.error(f"Erro ao construir payload de cache para exportação: {exc}")
        return {
            "user": user,
            "saved_at_epoch": float(saved_at_epoch),
            "followers": [],
            "following": [],
            "nao_retribuem": [],
            "eu_nao_retribuo": [],
            "mutuos": [],
            "nao_me_seguem_mais": [],
            "rate_limit": {
                "remaining": None,
                "limit": None,
                "cost": None,
                "resetAt": None,
            },
        }
