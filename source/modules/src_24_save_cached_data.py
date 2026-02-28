from __future__ import annotations
import json
import time
from dataclasses import dataclass
from source.modules.RateLimitInfo import RateLimitInfo
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


@dataclass
class CompareData:
    user: str
    followers: set[str]
    following: set[str]
    rate_limit: RateLimitInfo | None
    requests_made: int
    from_cache: bool
    cache_age_seconds: float | None = None
    nao_me_seguem_mais: list[str] | None = None

    @property
    def nao_retribuem(self) -> list[str]:
        return sorted(self.following - self.followers)

    @property
    def eu_nao_retribuo(self) -> list[str]:
        return sorted(self.followers - self.following)

    @property
    def mutuos(self) -> list[str]:
        return sorted(self.following & self.followers)

def save_cached_data(data: "CompareData") -> None:
    try:
        from source.modules import source as core

        previous_payload = core._load_cache_file()
        previous_followers: set[str] = set()

        if isinstance(previous_payload, dict):
            raw_previous_followers = previous_payload.get("followers")

            if previous_payload.get("user") == data.user and isinstance(raw_previous_followers, list):
                previous_followers = {item.strip().lower() for item in raw_previous_followers if isinstance(item, str) and item.strip()}

            previous_temp_file = core.NON_FOLLOWERS_STATE_FILE.with_suffix(core.NON_FOLLOWERS_STATE_FILE.suffix + ".tmp")

            try:
                core.NON_FOLLOWERS_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
                previous_temp_file.write_text(json.dumps(previous_payload, ensure_ascii=False, indent=2), encoding="utf-8")
                previous_temp_file.replace(core.NON_FOLLOWERS_STATE_FILE)

            except OSError:
                pass

        followers = {item.strip().lower() for item in data.followers if isinstance(item, str) and item.strip()}
        following = {item.strip().lower() for item in data.following if isinstance(item, str) and item.strip()}
        nao_retribuem = sorted(following - followers)
        eu_nao_retribuo = sorted(followers - following)
        mutuos = sorted(following & followers)
        nao_me_seguem_mais = sorted(previous_followers - followers)

        try:
            data.nao_me_seguem_mais = list(nao_me_seguem_mais)

        except Exception:
            pass

        payload = {
            "user": data.user,
            "saved_at_epoch": time.time(),
            "followers": sorted(followers),
            "following": sorted(following),
            "nao_retribuem": nao_retribuem,
            "eu_nao_retribuo": eu_nao_retribuo,
            "mutuos": mutuos,
            "nao_me_seguem_mais": nao_me_seguem_mais,
            "rate_limit": {
                "remaining": data.rate_limit.remaining if data.rate_limit else None,
                "limit": data.rate_limit.limit if data.rate_limit else None,
                "cost": data.rate_limit.cost if data.rate_limit else None,
                "resetAt": data.rate_limit.reset_at if data.rate_limit else None,
            },
        }

        temp_file = core.CACHE_FILE.with_suffix(core.CACHE_FILE.suffix + ".tmp")

        try:
            core.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            temp_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            temp_file.replace(core.CACHE_FILE)

        except OSError:
            pass

    except Exception as exc:
        logger.error(f"Erro ao salvar dados em cache para o usuário '{data.user}': {exc}")
