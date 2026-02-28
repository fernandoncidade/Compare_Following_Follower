from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _format_tab_title(title: str, count: int) -> str:
    try:
        return f"{title} = {max(count, 0)}"

    except Exception as exc:
        logger.error(f"Erro ao formatar título da aba: {exc}")
        return title
