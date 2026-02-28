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

def print_cli_report(data: "CompareData") -> None:
    try:
        from source.modules import source as core
        no_longer_follow_me = sorted({item for item in getattr(data, "nao_me_seguem_mais", []) if isinstance(item, str)})

        print(f"Usuário: {data.user}")
        print(
            f"Seguidores = {len(data.followers)}; "
            f"Sigo = {len(data.following)}; "
            f"Não sigo = {len(data.eu_nao_retribuo)}; "
            f"Mútuos = {len(data.mutuos)}; "
            f"Não me seguem mais = {len(no_longer_follow_me)}"
        )
        print(core.format_cache_status(data))
        print(core.format_rate_limit(data.rate_limit))

        print("\nSigo, mas não me segue de volta:")
        print("\n".join(data.nao_retribuem) or "(ninguém)")

        print("\nMe segue, mas eu não sigo de volta:")
        print("\n".join(data.eu_nao_retribuo) or "(ninguém)")

        print("\nMútuos:")
        print("\n".join(data.mutuos) or "(ninguém)")

        print("\nNão me seguem mais:")
        print("\n".join(no_longer_follow_me) or "(ninguém)")

    except Exception as exc:
        logger.error(f"Erro ao imprimir relatório CLI para o usuário '{data.user}': {exc}")
