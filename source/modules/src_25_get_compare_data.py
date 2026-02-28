from __future__ import annotations
import requests
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

    @property
    def nao_retribuem(self) -> list[str]:
        return _nao_retribuem(self.following, self.followers)

    @property
    def eu_nao_retribuo(self) -> list[str]:
        return _eu_nao_retribuo(self.followers, self.following)

    @property
    def mutuos(self) -> list[str]:
        return _mutuos(self.following, self.followers)

def get_compare_data(session: requests.Session, user: str, force_refresh: bool = False) -> "CompareData":
    try:
        from source.modules import source as core

        stale_cache = core.load_cached_data(user, include_expired=True)

        if not force_refresh:
            cached = core.load_cached_data(user)

            if cached is not None:
                return cached

        if not core.get_token():
            if stale_cache is not None:
                return stale_cache

            raise core.ConfigError("Defina GITHUB_TOKEN para usar o GraphQL sem cache.")

        try:
            fresh_data = core.fetch_relationships_graphql(session, user)

        except Exception:
            if stale_cache is not None:
                return stale_cache

            raise

        core.save_cached_data(fresh_data)
        return fresh_data

    except Exception as exc:
        logger.error(f"Erro ao obter dados de comparação para o usuário '{user}': {exc}")
        raise
