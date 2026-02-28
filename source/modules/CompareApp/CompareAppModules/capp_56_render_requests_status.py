from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _render_requests_status(self) -> str:
    try:
        count_value = "-" if self._requests_used_count is None else str(self._requests_used_count)
        return self._tr("Requisições usadas nesta atualização: {count}").format(count=count_value)

    except Exception as exc:
        logger.error(f"Erro ao renderizar status de requisições: {exc}")
        return self._tr("Requisições usadas nesta atualização: -")
