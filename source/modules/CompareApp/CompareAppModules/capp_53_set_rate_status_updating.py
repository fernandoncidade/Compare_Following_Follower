from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _set_rate_status_updating(self) -> None:
    try:
        self._rate_status_mode = "updating"
        self.rate_label.setText(self._render_rate_status())

    except Exception as exc:
        logger.error(f"Erro ao marcar rate limit como atualizando: {exc}")
