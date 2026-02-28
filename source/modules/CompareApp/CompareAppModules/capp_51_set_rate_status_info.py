from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _set_rate_status_info(self, info: Any) -> None:
    try:
        self._rate_status_mode = "info"
        self._rate_status_info = info
        self.rate_label.setText(self._render_rate_status())

    except Exception as exc:
        logger.error(f"Erro ao atualizar status do rate limit: {exc}")
