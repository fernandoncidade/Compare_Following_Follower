from __future__ import annotations
import json
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _load_non_followers_state_file() -> dict[str, Any] | None:
    try:
        from source.modules import source as core

        if not core.NON_FOLLOWERS_STATE_FILE.exists():
            return None

        try:
            content = json.loads(core.NON_FOLLOWERS_STATE_FILE.read_text(encoding="utf-8"))

        except (OSError, json.JSONDecodeError):
            return None

        return content if isinstance(content, dict) else None

    except Exception as exc:
        logger.error(f"Erro ao carregar arquivo de estado de não seguidores: {exc}")
