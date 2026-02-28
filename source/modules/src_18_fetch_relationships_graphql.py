from __future__ import annotations
import requests
from dataclasses import dataclass, field
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
    nao_me_seguem_mais: list[str] = field(default_factory=list)

    @property
    def nao_retribuem(self) -> list[str]:
        return _nao_retribuem(self.following, self.followers)

    @property
    def eu_nao_retribuo(self) -> list[str]:
        return _eu_nao_retribuo(self.followers, self.following)

    @property
    def mutuos(self) -> list[str]:
        return _mutuos(self.following, self.followers)

def fetch_relationships_graphql(session: requests.Session, user: str) -> "CompareData":
    try:
        from source.modules import source as core

        followers: set[str] = set()
        following: set[str] = set()
        requests_made = 0
        rate_limit: RateLimitInfo | None = None

        include_followers = True
        include_following = True
        after_followers: str | None = None
        after_following: str | None = None

        while include_followers or include_following:
            page = core.fetch_graphql_page(
                session=session,
                user=user,
                after_followers=after_followers,
                after_following=after_following,
                include_followers=include_followers,
                include_following=include_following,
            )
            requests_made += 1

            if include_followers:
                followers.update(page.followers)
                include_followers = page.followers_has_next
                after_followers = page.followers_end_cursor

            if include_following:
                following.update(page.following)
                include_following = page.following_has_next
                after_following = page.following_end_cursor

            rate_limit = page.rate_limit

        return core.CompareData(
            user=user,
            followers=followers,
            following=following,
            rate_limit=rate_limit,
            requests_made=requests_made,
            from_cache=False,
            nao_me_seguem_mais=[],
        )

    except Exception as exc:
        logger.error(f"Erro ao buscar relacionamentos via GraphQL para o usuário '{user}': {exc}")
        raise
