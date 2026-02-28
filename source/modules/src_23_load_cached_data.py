from __future__ import annotations
import time
from dataclasses import dataclass
from source.modules.RateLimitInfo import RateLimitInfo
from .src_08_nao_retribuem import nao_retribuem as _nao_retribuem
from .src_09_eu_nao_retribuo import eu_nao_retribuo as _eu_nao_retribuo
from .src_10_mutuos import mutuos as _mutuos
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
        return _nao_retribuem(self.following, self.followers)

    @property
    def eu_nao_retribuo(self) -> list[str]:
        return _eu_nao_retribuo(self.followers, self.following)

    @property
    def mutuos(self) -> list[str]:
        return _mutuos(self.following, self.followers)

def load_cached_data(user: str, include_expired: bool = False) -> "CompareData | None":
    try:
        from source.modules import source as core

        payload = core._load_cache_file()

        if payload is None:
            return None

        if payload.get("user") != user:
            return None

        saved_at = payload.get("saved_at_epoch")

        if not isinstance(saved_at, (int, float)):
            return None

        age = time.time() - float(saved_at)

        if (not include_expired) and age > core.CACHE_TTL_SECONDS:
            return None

        raw_followers = payload.get("followers")
        raw_following = payload.get("following")
        raw_no_longer_follow_me = payload.get("nao_me_seguem_mais")

        if not isinstance(raw_followers, list) or not isinstance(raw_following, list):
            return None

        followers = {item.strip().lower() for item in raw_followers if isinstance(item, str) and item.strip()}
        following = {item.strip().lower() for item in raw_following if isinstance(item, str) and item.strip()}
        no_longer_follow_me: list[str] = []

        if isinstance(raw_no_longer_follow_me, list):
            no_longer_follow_me = sorted({item.strip().lower() for item in raw_no_longer_follow_me if isinstance(item, str) and item.strip()})

        rate_limit = RateLimitInfo.from_payload(payload.get("rate_limit"))

        return core.CompareData(
            user=user,
            followers=followers,
            following=following,
            rate_limit=rate_limit,
            requests_made=0,
            from_cache=True,
            cache_age_seconds=max(age, 0.0),
            nao_me_seguem_mais=no_longer_follow_me,
        )

    except Exception as exc:
        logger.error(f"Erro ao carregar dados em cache para o usuário '{user}': {exc}")
