from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_worker_finished(self) -> None:
    try:
        if self.sender() is self._thread:
            self._worker = None
            self._thread = None
            self._active_worker_mode = None

        if self._is_loading and not self._is_refresh_thread_running():
            self._set_loading(False)

    except Exception as exc:
        logger.error(f"Erro ao finalizar thread de trabalho: {exc}")
