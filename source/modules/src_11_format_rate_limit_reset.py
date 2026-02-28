from __future__ import annotations
from datetime import datetime
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _format_rate_limit_reset(reset_value: str | None) -> str | None:
    try:
        if not reset_value:
            return None

        try:
            ts = int(reset_value)

        except ValueError:
            return None

        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    except Exception as exc:
        logger.error(f"Erro ao formatar data de reset do rate limit: {exc}")
