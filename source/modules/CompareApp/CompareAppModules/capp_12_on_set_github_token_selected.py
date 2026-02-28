from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_set_github_token_selected(self) -> None:
    try:
        if self._file_actions_locked():
            return

        self._request_and_persist_github_token()

    except Exception as exc:
        logger.error(f"Erro ao executar ação de definir token GitHub: {exc}")
