from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def refresh(self, _checked: bool = False) -> None:
    try:
        if self._is_loading and not self._is_refresh_thread_running():
            self._set_loading(False)

        try:
            self._start_refresh(force_network_refresh=self.force_refresh_checkbox.isChecked())

        except KeyboardInterrupt:
            self._set_loading(False)
            self._set_cache_status("interrupted")
            self._set_rate_status_unavailable()
            self._set_requests_used(0)

        except BaseException:
            self._set_loading(False)
            self._set_cache_status("start_failed")
            self._set_rate_status_unavailable()
            self._set_requests_used(0)
            raise

    except Exception as exc:
        logger.error(f"Erro ao iniciar atualização: {exc}")
