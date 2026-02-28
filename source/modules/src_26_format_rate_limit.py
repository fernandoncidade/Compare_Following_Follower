from __future__ import annotations
from source.modules.RateLimitInfo import RateLimitInfo
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def format_rate_limit(info: "RateLimitInfo | None") -> str:
    try:
        if info is None or info.remaining is None or info.limit is None:
            return "Rate limit restante: indisponível"

        extras: list[str] = []

        if info.cost is not None:
            extras.append(f"custo {info.cost}")

        if info.reset_at:
            extras.append(f"reset {info.reset_at}")

        suffix = f" ({' | '.join(extras)})" if extras else ""
        return f"Rate limit restante: {info.remaining}/{info.limit}{suffix}"

    except Exception as exc:
        logger.error(f"Erro ao formatar informações de rate limit: {exc}")
