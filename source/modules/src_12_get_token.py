from __future__ import annotations
import os
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_token() -> str | None:
    try:
        raw = os.getenv("GITHUB_TOKEN")

        if not raw:
            return None

        token = raw.strip().strip('"').strip("'")
        return token or None

    except Exception as exc:
        logger.error(f"Erro ao obter token do ambiente: {exc}")
