from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _set_loading(self, value: bool) -> None:
    try:
        self._is_loading = value
        self.refresh_button.setDisabled(value)
        self.user_input.setDisabled(value)
        self.force_refresh_checkbox.setDisabled(value)
        self.novos_nao_seguidores_list.setDisabled(value)
        self._update_unfollow_button_state()

    except Exception as exc:
        logger.error(f"Erro ao atualizar estado de carregamento: {exc}")
