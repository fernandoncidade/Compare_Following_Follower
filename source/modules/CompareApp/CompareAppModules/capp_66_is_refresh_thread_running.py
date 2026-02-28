from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _is_refresh_thread_running(self) -> bool:
    try:
        if self._thread is None:
            return False

        try:
            return self._thread.isRunning()

        except RuntimeError:
            return False

    except Exception as exc:
        logger.error(f"Erro ao verificar estado da thread de atualização: {exc}")
        return False
