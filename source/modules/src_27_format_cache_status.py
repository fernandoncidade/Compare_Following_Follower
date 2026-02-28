from __future__ import annotations
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

def format_cache_status(data: "CompareData") -> str:
    try:
        if data.from_cache:
            age = int(data.cache_age_seconds or 0)
            return f"Origem: cache local (idade {age}s)"

        return f"Origem: GraphQL (requisições nesta atualização: {data.requests_made})"

    except Exception as exc:
        logger.error(f"Erro ao formatar status do cache para o usuário '{data.user}': {exc}")
