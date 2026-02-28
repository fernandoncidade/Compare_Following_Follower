from __future__ import annotations
import json
import time
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def save_last_user(user: str) -> None:
    try:
        from source.modules import source as core

        normalized_user = str(user).strip()

        if not normalized_user:
            return

        payload = {
            "user": normalized_user,
            "saved_at_epoch": time.time(),
        }
        temp_file = core.LAST_USER_FILE.with_suffix(core.LAST_USER_FILE.suffix + ".tmp")

        try:
            core.LAST_USER_FILE.parent.mkdir(parents=True, exist_ok=True)
            temp_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            temp_file.replace(core.LAST_USER_FILE)

        except OSError:
            pass

    except Exception as exc:
        logger.error(f"Erro ao salvar último usuário '{user}': {exc}")
