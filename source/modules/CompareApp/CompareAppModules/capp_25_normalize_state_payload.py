from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _normalize_state_payload(self, payload: Any) -> dict[str, Any] | None:
    try:
        if not isinstance(payload, dict):
            return None

        user = payload.get("user")
        saved_at_epoch = payload.get("saved_at_epoch")
        followers = payload.get("followers")
        following = payload.get("following")
        non_followers = payload.get("nao_retribuem")
        nao_me_seguem_mais = payload.get("nao_me_seguem_mais")

        if not isinstance(user, str):
            return None

        if not isinstance(saved_at_epoch, (int, float)) or isinstance(saved_at_epoch, bool):
            return None

        if followers is not None and not isinstance(followers, list):
            return None

        if following is not None and not isinstance(following, list):
            return None

        if non_followers is not None and not isinstance(non_followers, list):
            return None

        if nao_me_seguem_mais is not None and not isinstance(nao_me_seguem_mais, list):
            return None

        normalized_followers = (sorted({item.strip().lower() for item in followers if isinstance(item, str) and item.strip()}) if isinstance(followers, list) else [])
        normalized_following = (sorted({item.strip().lower() for item in following if isinstance(item, str) and item.strip()}) if isinstance(following, list) else [])
        normalized_no_longer_follow_me = []

        if isinstance(nao_me_seguem_mais, list):
            normalized_no_longer_follow_me = sorted({item.strip().lower() for item in nao_me_seguem_mais if isinstance(item, str) and item.strip()})

        if not normalized_followers and not normalized_following:
            normalized_nao_retribuem = sorted({item for item in (non_followers or []) if isinstance(item, str)})
            normalized_eu_nao_retribuo: list[str] = []
            normalized_mutuos: list[str] = []

        else:
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
            "nao_me_seguem_mais": normalized_no_longer_follow_me,
        }

    except Exception as exc:
        logger.error(f"Erro ao normalizar payload de estado: {exc}")
        return None
