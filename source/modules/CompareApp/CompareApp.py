from __future__ import annotations
from typing import Any, Callable
from PySide6.QtCore import QObject, QThread, QTimer
from PySide6.QtWidgets import QApplication, QCheckBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPlainTextEdit, QTabWidget, QVBoxLayout, QWidget
from source.ui import CompareMenuBar, build_compare_menu_bar, tr
from source.utils.GerenciadorBotoesUI import GerenciadorBotoesUI
from source.utils.LogManager import LogManager
from .CompareAppModules import bind_compare_app_methods
logger = LogManager.get_logger()


class CompareApp(QWidget):
    def __init__(
        self,
        start_user: str,
        force_network_refresh: bool,
        app_instance: QApplication,
        theme_is_light: bool | None,
        initial_icon_path: str | None,
        fetch_worker_cls: type[QObject],
        unfollow_worker_cls: type[QObject],
        build_session_fn: Callable[[], Any],
        get_compare_data_fn: Callable[..., Any],
        get_token_fn: Callable[[], str | None],
        persist_github_token_fn: Callable[[str], Any],
        reset_github_token_fn: Callable[[], Any],
        unfollow_user_fn: Callable[[Any, str], None],
        unfollow_result_cls: type[Any],
        load_cached_data_fn: Callable[..., Any],
        load_previous_non_followers_fn: Callable[[str], set[str] | None],
        save_non_followers_state_fn: Callable[[str, set[str] | list[str]], None],
        format_cache_status_fn: Callable[[Any], str],
        format_rate_limit_fn: Callable[[Any], str],
        format_exception_fn: Callable[[Exception], str],
        resolve_theme_flag_fn: Callable[[], bool | None],
        resolve_icon_for_theme_fn: Callable[[bool | None], str | None],
        config_error_cls: type[Exception],
        translation_manager: Any | None = None,
    ) -> None:
        super().__init__()
        try:
            self._app_instance = app_instance
            self._theme_is_light = theme_is_light
            self._current_icon_path = initial_icon_path
            self._theme_icon_timer: QTimer | None = None
            self._translation_manager = translation_manager
            self.gerenciador_traducao = translation_manager
            self._fetch_worker_cls = fetch_worker_cls
            self._unfollow_worker_cls = unfollow_worker_cls
            self._build_session_fn = build_session_fn
            self._get_compare_data_fn = get_compare_data_fn
            self._get_token_fn = get_token_fn
            self._persist_github_token_fn = persist_github_token_fn
            self._reset_github_token_fn = reset_github_token_fn
            self._unfollow_user_fn = unfollow_user_fn
            self._unfollow_result_cls = unfollow_result_cls
            self._load_cached_data_fn = load_cached_data_fn
            self._load_previous_non_followers_fn = load_previous_non_followers_fn
            self._save_non_followers_state_fn = save_non_followers_state_fn
            self._format_cache_status_fn = format_cache_status_fn
            self._format_rate_limit_fn = format_rate_limit_fn
            self._format_exception_fn = format_exception_fn
            self._resolve_theme_flag_fn = resolve_theme_flag_fn
            self._resolve_icon_for_theme_fn = resolve_icon_for_theme_fn
            self._config_error_cls = config_error_cls

            self.button_manager = GerenciadorBotoesUI(self)
            self.user_input = QLineEdit(start_user)
            self.user_label = QLabel()
            self.force_refresh_checkbox = QCheckBox()
            self.force_refresh_checkbox.setChecked(force_network_refresh)
            self.refresh_button = self.button_manager.create_button_with_auto_resize(min_padding=28)
            self.unfollow_button = self.button_manager.create_button_with_auto_resize(min_padding=28)
            self.counts_label = QLabel()
            self.cache_label = QLabel()
            self.rate_label = QLabel()
            self.requests_label = QLabel()
            self.followers_text = QPlainTextEdit()
            self.following_text = QPlainTextEdit()
            self.nao_retribuem_text = QPlainTextEdit()
            self.eu_nao_retribuo_text = QPlainTextEdit()
            self.mutuos_text = QPlainTextEdit()
            self.novos_nao_seguidores_list = QListWidget()
            self.tabs: QTabWidget | None = None
            self._menu_bar_ui: CompareMenuBar | None = None

            self._counts_following: int | None = None
            self._counts_followers: int | None = None
            self._counts_non_following: int | None = None
            self._counts_mutuals: int | None = None
            self._counts_no_longer_follow_me: int | None = None
            self._cache_status_mode = "none"
            self._cache_status_payload: dict[str, Any] = {}
            self._rate_status_mode = "unavailable"
            self._rate_status_info: Any = None
            self._requests_used_count: int | None = None
            self._followers_values: list[str] = []
            self._following_values: list[str] = []
            self._non_followers_values: list[str] = []
            self._non_following_values: list[str] = []
            self._mutual_values: list[str] = []

            self._tab_title_followers = ""
            self._tab_title_following = ""
            self._tab_title_non_followers = ""
            self._tab_title_non_following = ""
            self._tab_title_mutuals = ""
            self._tab_title_new_non_followers = ""
            self._tab_followers_count = 0
            self._tab_following_count = 0
            self._tab_non_followers_count = 0
            self._tab_non_following_count = 0
            self._tab_mutuals_count = 0
            self._tab_new_non_followers_count = 0
            self._tab_followers_index = -1
            self._tab_following_index = -1
            self._tab_non_followers_index = -1
            self._tab_non_following_index = -1
            self._tab_mutuals_index = -1
            self._tab_new_non_followers_index = -1

            self._thread: QThread | None = None
            self._worker: QObject | None = None
            self._active_worker_mode: str | None = None
            self._is_loading = False
            self._build_ui()
            self._connect_translation_manager()
            self._apply_translations()
            self._load_startup_cache(start_user)
            self._start_theme_icon_watcher()

        except Exception as exc:
            logger.error(f"Erro ao inicializar CompareApp: {exc}")

    @staticmethod
    def _tr(text: str) -> str:
        try:
            return tr(text)

        except Exception as exc:
            logger.error(f"Erro ao traduzir texto '{text}': {exc}")
            return text

    def _translate_runtime_message(self, message: str) -> str:
        try:
            if not isinstance(message, str) or not message:
                return message

            translated_lines = [self._tr(line) if line else line for line in message.splitlines()]
            return "\n".join(translated_lines)

        except Exception as exc:
            logger.error(f"Erro ao traduzir mensagem dinâmica '{message}': {exc}")
            return message

    def _resolve_label(self, pt_br: str, en_us: str) -> str:
        try:
            translated = self._tr(pt_br)

            if translated and translated != pt_br:
                return translated

            if self._get_current_language_code() == "en_US":
                return en_us

            return pt_br

        except Exception as exc:
            logger.error(f"Erro ao resolver rótulo '{pt_br}/{en_us}': {exc}")
            return pt_br

    def _build_ui(self) -> None:
        try:
            self.setMinimumSize(980, 650)
            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(12, 12, 12, 12)
            main_layout.setSpacing(8)

            self._menu_bar_ui = build_compare_menu_bar(
                parent=self,
                on_language_selected=self._on_language_selected,
                on_new_selected=self._on_new_selected,
                on_open_selected=self._on_open_selected,
                on_save_selected=self._on_save_selected,
                on_delete_selected=self._on_delete_selected,
                on_help_selected=self._on_help_selected,
                on_close_selected=self._on_close_selected,
                on_set_github_token_selected=self._on_set_github_token_selected,
                on_reset_github_token_selected=self._on_reset_github_token_selected,
                on_manual_selected=self._show_manual,
                on_about_selected=self._show_about,
                current_language=self._get_current_language_code(),
            )
            main_layout.setMenuBar(self._menu_bar_ui.menu_bar)

            top_layout = QHBoxLayout()
            top_layout.addWidget(self.user_label)
            top_layout.addWidget(self.user_input, stretch=1)
            top_layout.addWidget(self.refresh_button)
            main_layout.addLayout(top_layout)
            main_layout.addWidget(self.force_refresh_checkbox)

            status_layout = QVBoxLayout()
            status_layout.setSpacing(4)
            status_layout.addWidget(self.counts_label)
            status_layout.addWidget(self.cache_label)
            status_layout.addWidget(self.rate_label)
            status_layout.addWidget(self.requests_label)
            main_layout.addLayout(status_layout)

            self.tabs = QTabWidget()
            self._tab_followers_index = self._configure_tab(self.tabs, self._tab_title_followers, self.followers_text)
            self._tab_following_index = self._configure_tab(self.tabs, self._tab_title_following, self.following_text)
            self._tab_mutuals_index = self._configure_tab(self.tabs, self._tab_title_mutuals, self.mutuos_text)
            self._tab_non_followers_index = self._configure_tab(self.tabs, self._tab_title_non_followers, self.nao_retribuem_text)
            self._tab_non_following_index = self._configure_tab(self.tabs, self._tab_title_non_following, self.eu_nao_retribuo_text)
            self._tab_new_non_followers_index = self._configure_new_non_followers_tab(self.tabs)
            main_layout.addWidget(self.tabs, stretch=1)

            self.refresh_button.clicked.connect(self.refresh)
            self.unfollow_button.clicked.connect(self._unfollow_selected)
            self.novos_nao_seguidores_list.itemChanged.connect(self._update_unfollow_button_state)
            self._update_unfollow_button_state()
            self.button_manager.update_all_button_sizes()

        except Exception as exc:
            logger.error(f"Erro ao construir UI do CompareApp: {exc}")

bind_compare_app_methods(CompareApp)
