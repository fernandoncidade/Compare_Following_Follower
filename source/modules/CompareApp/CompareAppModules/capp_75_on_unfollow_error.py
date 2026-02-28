from __future__ import annotations
from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_unfollow_error(self, exc: Exception) -> None:
    try:
        self._set_loading(False)
        raw_error_message = self._format_exception_fn(exc)

        if self._is_missing_token_error(raw_error_message):
            if self._request_and_persist_github_token():
                self._unfollow_selected()
                return

        error_message = self._translate_runtime_message(raw_error_message)
        self._set_cache_status("unfollow_failed")
        QMessageBox.critical(self, self._tr("Erro ao executar unfollow"), error_message)

    except Exception as log_exc:
        logger.error(f"Erro ao processar erro de unfollow: {log_exc}")
