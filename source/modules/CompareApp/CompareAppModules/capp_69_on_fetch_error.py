from __future__ import annotations
from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_fetch_error(self, exc: Exception) -> None:
    try:
        self._set_loading(False)
        raw_error_message = self._format_exception_fn(exc)

        if self._is_missing_token_error(raw_error_message):
            if self._request_and_persist_github_token():
                self._start_refresh(force_network_refresh=self.force_refresh_checkbox.isChecked())
                return

        error_message = self._translate_runtime_message(raw_error_message)
        self._set_cache_status("fetch_failed")
        self._set_rate_status_unavailable()
        self._set_requests_used(0)
        self._set_counts_values(following=0, followers=0, non_following=0, mutuals=0, no_longer_follow_me=0)
        self._update_relationship_tab_counts(followers=0, following=0)
        self._update_primary_tab_counts(non_followers=0, non_following=0, mutuals=0)
        self._followers_values = []
        self._following_values = []
        self._non_followers_values = [self._tr("Erro: {message}").format(message=error_message)]
        self._non_following_values = []
        self._mutual_values = []
        self._fill_text(self.followers_text, self._followers_values)
        self._fill_text(self.following_text, self._following_values)
        self._fill_text(self.nao_retribuem_text, self._non_followers_values)
        self._fill_text(self.eu_nao_retribuo_text, self._non_following_values)
        self._fill_text(self.mutuos_text, self._mutual_values)
        self._fill_new_non_followers([])
        QMessageBox.critical(self, self._tr("Erro ao consultar GitHub"), error_message)

    except Exception as log_exc:
        logger.error(f"Erro ao processar erro de consulta para o usuário '{self.user_input.text()}': {log_exc}")
