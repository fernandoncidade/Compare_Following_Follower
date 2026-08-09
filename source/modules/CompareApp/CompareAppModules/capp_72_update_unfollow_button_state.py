from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _update_unfollow_button_state(self) -> None:
    try:
        base_text = self._tr("🗑️ Unfollow")
        
        checked_new = self._checked_new_non_followers()
        has_checked_new = bool(checked_new)
        self.unfollow_button.setEnabled((not self._is_loading) and has_checked_new)
        
        count_new = len(checked_new)
        if count_new > 0:
            self.button_manager.set_button_text(self.unfollow_button, f"{base_text} ({count_new})")
        else:
            self.button_manager.set_button_text(self.unfollow_button, base_text)

        checked_non = self._checked_non_followers()
        has_checked_non = bool(checked_non)
        if hasattr(self, "unfollow_non_followers_button"):
            self.unfollow_non_followers_button.setEnabled((not self._is_loading) and has_checked_non)
            
            count_non = len(checked_non)
            if count_non > 0:
                self.button_manager.set_button_text(self.unfollow_non_followers_button, f"{base_text} ({count_non})")
            else:
                self.button_manager.set_button_text(self.unfollow_non_followers_button, base_text)

    except Exception as exc:
        logger.error(f"Erro ao atualizar estado do botão de unfollow: {exc}")

