from __future__ import annotations
import json
import time
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def save_non_followers_state(user: str, nao_retribuem: set[str] | list[str]) -> None:
    try:
        from source.modules import source as core

        payload = {
            "user": user,
            "saved_at_epoch": time.time(),
            "nao_retribuem": sorted({item for item in nao_retribuem if isinstance(item, str)}),
        }
        temp_file = core.NON_FOLLOWERS_STATE_FILE.with_suffix(core.NON_FOLLOWERS_STATE_FILE.suffix + ".tmp")

        try:
            core.NON_FOLLOWERS_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            temp_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            temp_file.replace(core.NON_FOLLOWERS_STATE_FILE)

        except OSError:
            pass

    except Exception as exc:
        logger.error(f"Erro ao salvar estado de não seguidores para o usuário '{user}': {exc}")
