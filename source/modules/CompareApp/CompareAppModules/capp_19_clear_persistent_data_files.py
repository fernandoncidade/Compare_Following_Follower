from __future__ import annotations
import time
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _clear_persistent_data_files(self) -> bool:
    try:
        from source.modules import source as core

        saved_at_epoch = time.time()
        empty_cache_payload = {
            "user": "",
            "saved_at_epoch": saved_at_epoch,
            "followers": [],
            "following": [],
            "nao_retribuem": [],
            "eu_nao_retribuo": [],
            "mutuos": [],
            "nao_me_seguem_mais": [],
            "rate_limit": {
                "remaining": None,
                "limit": None,
                "cost": None,
                "resetAt": None,
            },
        }
        empty_state_payload = {
            "user": "",
            "saved_at_epoch": saved_at_epoch,
            "followers": [],
            "following": [],
            "nao_retribuem": [],
            "eu_nao_retribuo": [],
            "mutuos": [],
            "nao_me_seguem_mais": [],
        }

        cache_ok = self._write_json_atomic(core.CACHE_FILE, empty_cache_payload)
        state_ok = self._write_json_atomic(core.NON_FOLLOWERS_STATE_FILE, empty_state_payload)
        return cache_ok and state_ok

    except Exception as exc:
        logger.error(f"Erro ao limpar arquivos persistentes: {exc}")
        return False
