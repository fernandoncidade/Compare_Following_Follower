from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _normalize_cache_payload(self, payload: Any) -> dict[str, Any] | None:
    try:
        if not isinstance(payload, dict):
            return None

        user = payload.get("user")
        saved_at_epoch = payload.get("saved_at_epoch")
        followers = payload.get("followers")
        following = payload.get("following")
        rate_limit = payload.get("rate_limit")
        nao_me_seguem_mais = payload.get("nao_me_seguem_mais")

        if not isinstance(user, str):
            return None

        if not isinstance(saved_at_epoch, (int, float)) or isinstance(saved_at_epoch, bool):
            return None

        if not isinstance(followers, list) or not isinstance(following, list):
            return None

        if rate_limit is not None and not isinstance(rate_limit, dict):
            return None

        if nao_me_seguem_mais is not None and not isinstance(nao_me_seguem_mais, list):
            return None

        normalized_rate_limit = {
            "remaining": None,
            "limit": None,
            "cost": None,
            "resetAt": None,
        }

        if isinstance(rate_limit, dict):
            reset_at = rate_limit.get("resetAt")
            normalized_rate_limit = {
                "remaining": self._to_int_or_none(rate_limit.get("remaining")),
                "limit": self._to_int_or_none(rate_limit.get("limit")),
                "cost": self._to_int_or_none(rate_limit.get("cost")),
                "resetAt": reset_at if isinstance(reset_at, str) else None,
            }

        normalized_followers = sorted({item.strip().lower() for item in followers if isinstance(item, str) and item.strip()})
        normalized_following = sorted({item.strip().lower() for item in following if isinstance(item, str) and item.strip()})
        normalized_nao_me_seguem_mais = []

        if isinstance(nao_me_seguem_mais, list):
            normalized_nao_me_seguem_mais = sorted({item.strip().lower() for item in nao_me_seguem_mais if isinstance(item, str) and item.strip()})

        normalized_nao_retribuem = sorted(set(normalized_following) - set(normalized_followers))
        normalized_eu_nao_retribuo = sorted(set(normalized_followers) - set(normalized_following))
        normalized_mutuos = sorted(set(normalized_following) & set(normalized_followers))

        return {
            "user": user.strip(),
            "saved_at_epoch": float(saved_at_epoch),
            "followers": normalized_followers,
            "following": normalized_following,
            "nao_retribuem": normalized_nao_retribuem,
            "eu_nao_retribuo": normalized_eu_nao_retribuo,
            "mutuos": normalized_mutuos,
            "nao_me_seguem_mais": normalized_nao_me_seguem_mais,
            "rate_limit": normalized_rate_limit,
        }

    except Exception as exc:
        logger.error(f"Erro ao normalizar payload de cache: {exc}")
        return None
