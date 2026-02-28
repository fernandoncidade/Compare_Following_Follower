from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _update_unfollow_button_state(self) -> None:
    try:
        has_checked_items = bool(self._checked_new_non_followers())
        self.unfollow_button.setEnabled((not self._is_loading) and has_checked_items)

    except Exception as exc:
        logger.error(f"Erro ao atualizar estado do botão de unfollow: {exc}")
