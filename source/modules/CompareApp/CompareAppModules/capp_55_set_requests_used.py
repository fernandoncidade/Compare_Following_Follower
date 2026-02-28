from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _set_requests_used(self, count: int | None) -> None:
    try:
        self._requests_used_count = count
        self.requests_label.setText(self._render_requests_status())

    except Exception as exc:
        logger.error(f"Erro ao atualizar total de requisições: {exc}")
