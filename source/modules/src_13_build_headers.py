from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def build_headers() -> dict[str, str]:
    try:
        from source.modules import source as core

        headers = dict(core.HEADERS_BASE)
        token = core.get_token()

        if token:
            headers["Authorization"] = f"Bearer {token}"

        return headers

    except Exception as exc:
        logger.error(f"Erro ao construir headers para requisições: {exc}")
