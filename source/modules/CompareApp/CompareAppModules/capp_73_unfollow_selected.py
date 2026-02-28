from __future__ import annotations
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _unfollow_selected(self) -> None:
    try:
        if self._is_loading:
            return

        selected_profiles = self._checked_new_non_followers()

        if not selected_profiles:
            QMessageBox.information(self, self._tr("Unfollow"), self._tr("Selecione ao menos um perfil na lista."))
            return

        preview = ", ".join(selected_profiles[:10])

        if len(selected_profiles) > 10:
            preview += ", ..."

        answer = QMessageBox.question(
            self,
            self._tr("Confirmar unfollow"),
            self._tr("Executar unfollow de {count} perfil(is)?\n\n{preview}").format(count=len(selected_profiles), preview=preview,),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if answer != QMessageBox.Yes:
            return

        if not self._get_token_fn():
            if not self._request_and_persist_github_token():
                return

        self._set_loading(True)
        self._set_cache_status("unfollowing", count=len(selected_profiles))
        self._set_rate_status_updating()
        self._set_requests_used(None)
        self._thread = QThread(self)
        self._worker = self._unfollow_worker_cls(
            usernames=selected_profiles,
            build_session_fn=self._build_session_fn,
            get_token_fn=self._get_token_fn,
            unfollow_user_fn=self._unfollow_user_fn,
            format_exception_fn=self._format_exception_fn,
            config_error_cls=self._config_error_cls,
            unfollow_result_cls=self._unfollow_result_cls,
        )
        self._active_worker_mode = "unfollow"
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.success.connect(self._on_unfollow_success)
        self._worker.error.connect(self._on_unfollow_error)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.finished.connect(self._on_worker_finished)
        self._thread.start()

    except Exception as exc:
        logger.error(f"Erro ao iniciar processo de unfollow: {exc}")
