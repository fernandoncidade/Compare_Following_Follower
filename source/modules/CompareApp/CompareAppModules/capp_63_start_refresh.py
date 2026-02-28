from __future__ import annotations
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _start_refresh(self, force_network_refresh: bool) -> None:
    try:
        if self._is_loading:
            return

        user = self.user_input.text().strip()

        if not user:
            QMessageBox.critical(self, self._tr("Entrada inválida"), self._tr("Informe um usuário GitHub."))
            return

        if not self._ensure_token_available_for_refresh(user):
            return

        self._set_loading(True)
        self._set_cache_status("updating")
        self._thread = QThread(self)
        self._worker = self._fetch_worker_cls(user=user, force_network_refresh=force_network_refresh, build_session_fn=self._build_session_fn, get_compare_data_fn=self._get_compare_data_fn, config_error_cls=self._config_error_cls,)
        self._active_worker_mode = "fetch"
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.success.connect(self._on_fetch_success)
        self._worker.error.connect(self._on_fetch_error)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.finished.connect(self._on_worker_finished)
        self._thread.start()

    except Exception as exc:
        logger.error(f"Erro ao iniciar processo de atualização: {exc}")
