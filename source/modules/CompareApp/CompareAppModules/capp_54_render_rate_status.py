from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _render_rate_status(self) -> str:
    try:
        if self._rate_status_mode == "updating":
            return self._tr("Rate limit restante: atualizando...")

        if self._rate_status_mode != "info":
            return self._tr("Rate limit restante: indisponível")

        info = self._rate_status_info
        if info is None or info.remaining is None or info.limit is None:
            return self._tr("Rate limit restante: indisponível")

        extras: list[str] = []

        if info.cost is not None:
            extras.append(self._tr("custo {value}").format(value=info.cost))

        if info.reset_at:
            extras.append(self._tr("reset {value}").format(value=info.reset_at))

        suffix = f" ({' | '.join(extras)})" if extras else ""
        return self._tr("Rate limit restante: {remaining}/{limit}{suffix}").format(remaining=info.remaining, limit=info.limit, suffix=suffix,)

    except Exception as exc:
        logger.error(f"Erro ao renderizar status de rate limit: {exc}")
        return self._tr("Rate limit restante: indisponível")
