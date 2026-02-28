from __future__ import annotations
import json
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def load_last_user() -> str:
    try:
        from source.modules import source as core

        if not core.LAST_USER_FILE.exists():
            return ""

        try:
            content = json.loads(core.LAST_USER_FILE.read_text(encoding="utf-8"))

        except (OSError, json.JSONDecodeError):
            return ""

        if not isinstance(content, dict):
            return ""

        raw_user = content.get("user")

        if not isinstance(raw_user, str):
            return ""

        return raw_user.strip()

    except Exception as exc:
        logger.error(f"Erro ao carregar último usuário: {exc}")
        return ""
