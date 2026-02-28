from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _apply_translations(self) -> None:
    try:
        self.setWindowTitle(self._tr("Comparar - Seguindo e Seguido"))

        if self._menu_bar_ui is not None:
            self._menu_bar_ui.set_checked_language(self._get_current_language_code())
            self._menu_bar_ui.retranslate()

        self.user_label.setText(self._tr("Usuário GitHub:"))
        self.force_refresh_checkbox.setText(self._tr("Forçar atualização da API (ignorar cache por 15 min)"))
        self.force_refresh_checkbox.setToolTip(self._tr("Mais lento e usa rate limit."))
        self.button_manager.set_button_text(self.refresh_button, self._tr("▶️ Executar"))
        self.button_manager.set_button_text(self.unfollow_button, self._tr("🗑️ Unfollow"))
        self._tab_title_followers = self._tr("🔵 Seguidores")
        self._tab_title_following = self._tr("🟣 Sigo")
        self._tab_title_non_followers = self._tr("🔴 Não seguidores")
        self._tab_title_non_following = self._tr("🟡 Não sigo")
        self._tab_title_mutuals = self._tr("🟢 Mútuos")
        self._tab_title_new_non_followers = self._tr("🟠 Não me seguem mais")
        self._render_counts_label()
        self.cache_label.setText(self._render_cache_status())
        self.rate_label.setText(self._render_rate_status())
        self.requests_label.setText(self._render_requests_status())
        self._refresh_tab_titles()
        self._fill_text(self.followers_text, self._followers_values)
        self._fill_text(self.following_text, self._following_values)
        self._fill_text(self.nao_retribuem_text, self._non_followers_values)
        self._fill_text(self.eu_nao_retribuo_text, self._non_following_values)
        self._fill_text(self.mutuos_text, self._mutual_values)
        self.button_manager.update_all_button_sizes()

    except Exception as exc:
        logger.error(f"Erro ao aplicar traduções da interface: {exc}")
