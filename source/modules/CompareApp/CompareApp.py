from __future__ import annotations
import json
import os
from pathlib import Path
import time
from typing import Any, Callable
from PySide6.QtCore import QEvent, QObject, QThread, QTimer, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPlainTextEdit,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from source.ui import CompareMenuBar, build_compare_menu_bar, tr
from source.utils.GerenciadorBotoesUI import GerenciadorBotoesUI
from source.utils.LogManager import LogManager
from source.utils.MessageBox import MessageBox
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
                on_help_selected=self._on_help_selected,
                on_close_selected=self._on_close_selected,
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

    def _connect_translation_manager(self) -> None:
        try:
            if self._translation_manager is None:
                return

            self._translation_manager.idioma_alterado.connect(self._on_language_changed)

        except Exception as exc:
            logger.error(f"Erro ao conectar gerenciador de tradução: {exc}")

    def _get_current_language_code(self) -> str:
        try:
            if self._translation_manager is None:
                return "pt_BR"

            current_language = self._translation_manager.obter_idioma_atual()

            if isinstance(current_language, str) and current_language in {"pt_BR", "en_US"}:
                return current_language

            return "pt_BR"

        except Exception as exc:
            logger.error(f"Erro ao obter idioma atual: {exc}")
            return "pt_BR"

    def _on_language_selected(self, language_code: str) -> None:
        try:
            if self._translation_manager is None:
                return

            if language_code == self._get_current_language_code():
                return

            self._translation_manager.definir_idioma(language_code)

        except Exception as exc:
            logger.error(f"Erro ao alterar idioma para '{language_code}': {exc}")

    def _show_about(self) -> None:
        try:
            from source.ui.ui_03_exibir_sobre import exibir_sobre

            exibir_sobre(self)

        except Exception as exc:
            logger.error(f"Erro ao abrir Sobre: {exc}")

    def _show_manual(self) -> None:
        try:
            from source.public.pub_01_ExibirPublic import exibir_manual

            exibir_manual(self)

        except Exception as exc:
            logger.error(f"Erro ao abrir Manual: {exc}")

    def _file_actions_locked(self) -> bool:
        try:
            if not self._is_loading:
                return False

            QMessageBox.warning(
                self,
                self._resolve_label("Ação indisponível", "Action unavailable"),
                self._resolve_label(
                    "Aguarde o término da atualização para usar este comando.",
                    "Wait for the refresh to finish before using this command.",
                ),
            )
            return True

        except Exception as exc:
            logger.error(f"Erro ao validar bloqueio de ação de arquivo: {exc}")
            return False

    def _on_new_selected(self) -> None:
        try:
            if self._file_actions_locked():
                return

            answer = QMessageBox.question(
                self,
                self._resolve_label("Novo", "New"),
                self._resolve_label(
                    "Deseja limpar os dados das abas e resetar os arquivos locais de cache/estado?",
                    "Do you want to clear tab data and reset local cache/state files?",
                ),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if answer != QMessageBox.Yes:
                return

            self._clear_reported_data()
            files_cleared = self._clear_persistent_data_files()

            if files_cleared:
                QMessageBox.information(
                    self,
                    self._resolve_label("Novo", "New"),
                    self._resolve_label(
                        "Dados da interface e arquivos locais foram limpos.",
                        "UI data and local files were cleared.",
                    ),
                )

            else:
                QMessageBox.warning(
                    self,
                    self._resolve_label("Novo", "New"),
                    self._resolve_label(
                        "Dados da interface foram limpos, mas houve falha ao limpar arquivos locais.",
                        "UI data was cleared, but local files could not be fully cleared.",
                    ),
                )

        except Exception as exc:
            logger.error(f"Erro ao executar ação Novo: {exc}")

    def _on_open_selected(self) -> None:
        try:
            if self._file_actions_locked():
                return

            selected_path, _ = QFileDialog.getOpenFileName(
                self,
                self._resolve_label("Abrir arquivo JSON", "Open JSON file"),
                "",
                "JSON (*.json)",
            )

            if not selected_path:
                return

            payload = self._read_json_dict(Path(selected_path))

            if payload is None:
                QMessageBox.warning(
                    self,
                    self._resolve_label("Abrir", "Open"),
                    self._resolve_label(
                        "Não foi possível ler o arquivo JSON selecionado.",
                        "Could not read the selected JSON file.",
                    ),
                )
                return

            cache_payload, state_payload = self._parse_import_payload(payload)

            if cache_payload is None and state_payload is None:
                QMessageBox.warning(
                    self,
                    self._resolve_label("Abrir", "Open"),
                    self._resolve_label(
                        "Formato inválido. Use JSON no padrão de cache, estado ou pacote contendo ambos.",
                        "Invalid format. Use JSON in cache, state, or combined package format.",
                    ),
                )
                return

            if (
                cache_payload is not None
                and state_payload is not None
                and cache_payload.get("user") != state_payload.get("user")
            ):
                QMessageBox.warning(
                    self,
                    self._resolve_label("Abrir", "Open"),
                    self._resolve_label(
                        "Arquivo inválido: 'cache.user' e 'state.user' precisam ser iguais.",
                        "Invalid file: 'cache.user' and 'state.user' must match.",
                    ),
                )
                return

            from source.modules import source as core

            persisted_ok = True

            if state_payload is not None:
                persisted_ok = self._write_json_atomic(core.NON_FOLLOWERS_STATE_FILE, state_payload) and persisted_ok

            if cache_payload is not None:
                persisted_ok = self._write_json_atomic(core.CACHE_FILE, cache_payload) and persisted_ok
                self.user_input.setText(cache_payload["user"])
                self._on_fetch_success(self._create_compare_data_from_cache_payload(cache_payload))

            elif state_payload is not None:
                self.user_input.setText(state_payload["user"])
                self._apply_state_payload_only(state_payload)

            if persisted_ok:
                QMessageBox.information(
                    self,
                    self._resolve_label("Abrir", "Open"),
                    self._resolve_label(
                        "Arquivo carregado com sucesso.",
                        "File loaded successfully.",
                    ),
                )

            else:
                QMessageBox.warning(
                    self,
                    self._resolve_label("Abrir", "Open"),
                    self._resolve_label(
                        "Arquivo carregado na interface, mas houve falha ao persistir os dados locais.",
                        "File loaded in the UI, but local persistence failed.",
                    ),
                )

        except Exception as exc:
            logger.error(f"Erro ao executar ação Abrir: {exc}")

    def _on_save_selected(self) -> None:
        try:
            if self._file_actions_locked():
                return

            selected_path, _ = QFileDialog.getSaveFileName(
                self,
                self._resolve_label("Salvar arquivo JSON", "Save JSON file"),
                "",
                "JSON (*.json)",
            )

            if not selected_path:
                return

            target_path = self._ensure_json_path(Path(selected_path))
            saved_at_epoch = time.time()
            user = self.user_input.text().strip()
            no_longer_follow_me_values: list[str] = []

            for idx in range(self.novos_nao_seguidores_list.count()):
                item = self.novos_nao_seguidores_list.item(idx)

                if item is None:
                    continue

                text = item.text()

                if isinstance(text, str):
                    no_longer_follow_me_values.append(text)

            payload = {
                "atual": self._build_cache_payload_from_ui(user=user, saved_at_epoch=saved_at_epoch),
                "antigo": self._build_state_payload(
                    user=user,
                    saved_at_epoch=saved_at_epoch,
                    values=no_longer_follow_me_values,
                ),
            }

            if self._write_json_atomic(target_path, payload):
                QMessageBox.information(
                    self,
                    self._resolve_label("Salvar", "Save"),
                    self._resolve_label(
                        "Dados exportados com sucesso.",
                        "Data exported successfully.",
                    ),
                )

            else:
                QMessageBox.warning(
                    self,
                    self._resolve_label("Salvar", "Save"),
                    self._resolve_label(
                        "Não foi possível salvar o arquivo.",
                        "Could not save the file.",
                    ),
                )

        except Exception as exc:
            logger.error(f"Erro ao executar ação Salvar: {exc}")

    def _on_help_selected(self) -> None:
        try:
            actions: list[tuple[str, str]]

            if self._menu_bar_ui is not None:
                actions = [
                    (self._menu_bar_ui.action_new.text(), self._menu_bar_ui.action_new.shortcut().toString()),
                    (self._menu_bar_ui.action_open.text(), self._menu_bar_ui.action_open.shortcut().toString()),
                    (self._menu_bar_ui.action_save.text(), self._menu_bar_ui.action_save.shortcut().toString()),
                    (self._menu_bar_ui.action_help.text(), self._menu_bar_ui.action_help.shortcut().toString()),
                    (self._menu_bar_ui.action_close.text(), self._menu_bar_ui.action_close.shortcut().toString()),
                    (self._menu_bar_ui.language_menu.title(), self._menu_bar_ui.language_menu.menuAction().shortcut().toString(),),
                    (self._menu_bar_ui.action_manual.text(), self._menu_bar_ui.action_manual.shortcut().toString()),
                    (self._menu_bar_ui.action_about.text(), self._menu_bar_ui.action_about.shortcut().toString()),
                ]

            else:
                actions = [
                    (self._resolve_label("Novo", "New"), "Ctrl+N"),
                    (self._resolve_label("Abrir", "Open"), "Ctrl+O"),
                    (self._resolve_label("Salvar", "Save"), "Ctrl+S"),
                    (self._resolve_label("Ajuda", "Help"), "F1"),
                    (self._resolve_label("Fechar", "Close"), "Ctrl+Q"),
                    (self._resolve_label("Idioma", "Language"), "Alt+I"),
                    (self._resolve_label("Manual", "Manual"), "Ctrl+Shift+M"),
                    (self._resolve_label("Sobre", "About"), "Ctrl+Shift+A"),
                ]

            lines = "".join([f"<li><b>{label}</b>: <code>{shortcut or '-'}</code></li>" for label, shortcut in actions])
            help_html = (
                f"<b>{self._resolve_label('Atalhos do menu Arquivo', 'File menu shortcuts')}</b><br><br>"
                f"<ul>{lines}</ul>"
            )
            MessageBox.app_help_shortcuts(self, help_html)

        except Exception as exc:
            logger.error(f"Erro ao executar ação Ajuda: {exc}")

    def _on_close_selected(self) -> None:
        try:
            self.close()

        except Exception as exc:
            logger.error(f"Erro ao executar ação Fechar: {exc}")

    def _clear_reported_data(self) -> None:
        try:
            self._set_counts_values(None, None, None, None, None)
            self._set_cache_status("none")
            self._set_rate_status_unavailable()
            self._set_requests_used(None)
            self._followers_values = []
            self._following_values = []
            self._non_followers_values = []
            self._non_following_values = []
            self._mutual_values = []
            self._update_relationship_tab_counts(followers=0, following=0)
            self._update_primary_tab_counts(non_followers=0, non_following=0, mutuals=0)
            self._fill_text(self.followers_text, self._followers_values)
            self._fill_text(self.following_text, self._following_values)
            self._fill_text(self.nao_retribuem_text, self._non_followers_values)
            self._fill_text(self.eu_nao_retribuo_text, self._non_following_values)
            self._fill_text(self.mutuos_text, self._mutual_values)
            self._fill_new_non_followers([])

        except Exception as exc:
            logger.error(f"Erro ao limpar dados reportados: {exc}")

    def _clear_persistent_data_files(self) -> bool:
        try:
            from source.modules import source as core

            saved_at_epoch = time.time()
            empty_cache_payload = {
                "user": "",
                "saved_at_epoch": saved_at_epoch,
                "followers": [],
                "following": [],
                "nao_retribuem": [],
                "eu_nao_retribuo": [],
                "mutuos": [],
                "nao_me_seguem_mais": [],
                "rate_limit": {
                    "remaining": None,
                    "limit": None,
                    "cost": None,
                    "resetAt": None,
                },
            }
            empty_state_payload = {
                "user": "",
                "saved_at_epoch": saved_at_epoch,
                "followers": [],
                "following": [],
                "nao_retribuem": [],
                "eu_nao_retribuo": [],
                "mutuos": [],
                "nao_me_seguem_mais": [],
            }

            cache_ok = self._write_json_atomic(core.CACHE_FILE, empty_cache_payload)
            state_ok = self._write_json_atomic(core.NON_FOLLOWERS_STATE_FILE, empty_state_payload)
            return cache_ok and state_ok

        except Exception as exc:
            logger.error(f"Erro ao limpar arquivos persistentes: {exc}")
            return False

    @staticmethod
    def _ensure_json_path(path: Path) -> Path:
        try:
            if path.suffix.lower() == ".json":
                return path

            return path.with_suffix(".json")

        except Exception:
            return path

    @staticmethod
    def _read_json_dict(path: Path) -> dict[str, Any] | None:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            return payload if isinstance(payload, dict) else None

        except (OSError, json.JSONDecodeError):
            return None

    @staticmethod
    def _write_json_atomic(path: Path, payload: dict[str, Any]) -> bool:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            temp_file = path.with_suffix(path.suffix + ".tmp")
            temp_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            temp_file.replace(path)
            return True

        except OSError:
            return False

    @staticmethod
    def _to_int_or_none(value: Any) -> int | None:
        try:
            if isinstance(value, bool):
                return None

            if isinstance(value, int):
                return value

            if isinstance(value, float):
                return int(value)

            if isinstance(value, str):
                try:
                    return int(value.strip())

                except ValueError:
                    return None

            return None

        except Exception:
            return None

    def _normalize_cache_payload(self, payload: Any) -> dict[str, Any] | None:
        try:
            if not isinstance(payload, dict):
                return None

            user = payload.get("user")
            saved_at_epoch = payload.get("saved_at_epoch")
            followers = payload.get("followers")
            following = payload.get("following")
            rate_limit = payload.get("rate_limit")
            nao_me_seguem_mais = payload.get("nao_me_seguem_mais")

            if not isinstance(user, str):
                return None

            if not isinstance(saved_at_epoch, (int, float)) or isinstance(saved_at_epoch, bool):
                return None

            if not isinstance(followers, list) or not isinstance(following, list):
                return None

            if rate_limit is not None and not isinstance(rate_limit, dict):
                return None

            if nao_me_seguem_mais is not None and not isinstance(nao_me_seguem_mais, list):
                return None

            normalized_rate_limit = {
                "remaining": None,
                "limit": None,
                "cost": None,
                "resetAt": None,
            }

            if isinstance(rate_limit, dict):
                reset_at = rate_limit.get("resetAt")
                normalized_rate_limit = {
                    "remaining": self._to_int_or_none(rate_limit.get("remaining")),
                    "limit": self._to_int_or_none(rate_limit.get("limit")),
                    "cost": self._to_int_or_none(rate_limit.get("cost")),
                    "resetAt": reset_at if isinstance(reset_at, str) else None,
                }

            normalized_followers = sorted({item.strip().lower() for item in followers if isinstance(item, str) and item.strip()})
            normalized_following = sorted({item.strip().lower() for item in following if isinstance(item, str) and item.strip()})
            normalized_nao_me_seguem_mais = []

            if isinstance(nao_me_seguem_mais, list):
                normalized_nao_me_seguem_mais = sorted({item.strip().lower() for item in nao_me_seguem_mais if isinstance(item, str) and item.strip()})

            normalized_nao_retribuem = sorted(set(normalized_following) - set(normalized_followers))
            normalized_eu_nao_retribuo = sorted(set(normalized_followers) - set(normalized_following))
            normalized_mutuos = sorted(set(normalized_following) & set(normalized_followers))

            return {
                "user": user.strip(),
                "saved_at_epoch": float(saved_at_epoch),
                "followers": normalized_followers,
                "following": normalized_following,
                "nao_retribuem": normalized_nao_retribuem,
                "eu_nao_retribuo": normalized_eu_nao_retribuo,
                "mutuos": normalized_mutuos,
                "nao_me_seguem_mais": normalized_nao_me_seguem_mais,
                "rate_limit": normalized_rate_limit,
            }

        except Exception as exc:
            logger.error(f"Erro ao normalizar payload de cache: {exc}")
            return None

    def _normalize_state_payload(self, payload: Any) -> dict[str, Any] | None:
        try:
            if not isinstance(payload, dict):
                return None

            user = payload.get("user")
            saved_at_epoch = payload.get("saved_at_epoch")
            followers = payload.get("followers")
            following = payload.get("following")
            non_followers = payload.get("nao_retribuem")
            nao_me_seguem_mais = payload.get("nao_me_seguem_mais")

            if not isinstance(user, str):
                return None

            if not isinstance(saved_at_epoch, (int, float)) or isinstance(saved_at_epoch, bool):
                return None

            if followers is not None and not isinstance(followers, list):
                return None

            if following is not None and not isinstance(following, list):
                return None

            if non_followers is not None and not isinstance(non_followers, list):
                return None

            if nao_me_seguem_mais is not None and not isinstance(nao_me_seguem_mais, list):
                return None

            normalized_followers = (sorted({item.strip().lower() for item in followers if isinstance(item, str) and item.strip()}) if isinstance(followers, list) else [])
            normalized_following = (sorted({item.strip().lower() for item in following if isinstance(item, str) and item.strip()}) if isinstance(following, list) else [])
            normalized_no_longer_follow_me = []

            if isinstance(nao_me_seguem_mais, list):
                normalized_no_longer_follow_me = sorted({item.strip().lower() for item in nao_me_seguem_mais if isinstance(item, str) and item.strip()})

            if not normalized_followers and not normalized_following:
                normalized_nao_retribuem = sorted({item for item in (non_followers or []) if isinstance(item, str)})
                normalized_eu_nao_retribuo: list[str] = []
                normalized_mutuos: list[str] = []

            else:
                normalized_nao_retribuem = sorted(set(normalized_following) - set(normalized_followers))
                normalized_eu_nao_retribuo = sorted(set(normalized_followers) - set(normalized_following))
                normalized_mutuos = sorted(set(normalized_following) & set(normalized_followers))

            return {
                "user": user.strip(),
                "saved_at_epoch": float(saved_at_epoch),
                "followers": normalized_followers,
                "following": normalized_following,
                "nao_retribuem": normalized_nao_retribuem,
                "eu_nao_retribuo": normalized_eu_nao_retribuo,
                "mutuos": normalized_mutuos,
                "nao_me_seguem_mais": normalized_no_longer_follow_me,
            }

        except Exception as exc:
            logger.error(f"Erro ao normalizar payload de estado: {exc}")
            return None

    def _parse_import_payload(self, payload: Any) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        try:
            if not isinstance(payload, dict):
                return None, None

            bundle_cache = self._normalize_cache_payload(payload.get("cache"))
            bundle_state = self._normalize_state_payload(payload.get("state"))

            if bundle_cache is None:
                bundle_cache = self._normalize_cache_payload(payload.get("atual"))

            if bundle_state is None:
                bundle_state = self._normalize_state_payload(payload.get("antigo"))

            if bundle_cache is not None or bundle_state is not None:
                return bundle_cache, bundle_state

            cache_payload = self._normalize_cache_payload(payload)
            if cache_payload is not None:
                return cache_payload, None

            state_payload = self._normalize_state_payload(payload)
            if state_payload is not None:
                return None, state_payload

            return None, None

        except Exception as exc:
            logger.error(f"Erro ao interpretar payload importado: {exc}")
            return None, None

    def _create_compare_data_from_cache_payload(self, payload: dict[str, Any]) -> Any:
        try:
            from source.modules import source as core

            saved_at_epoch = float(payload.get("saved_at_epoch", 0.0))
            age_seconds = max(time.time() - saved_at_epoch, 0.0)

            return core.CompareData(
                user=payload.get("user", ""),
                followers={item.strip().lower() for item in payload.get("followers", []) if isinstance(item, str) and item.strip()},
                following={item.strip().lower() for item in payload.get("following", []) if isinstance(item, str) and item.strip()},
                rate_limit=core.RateLimitInfo.from_payload(payload.get("rate_limit")),
                requests_made=0,
                from_cache=True,
                cache_age_seconds=age_seconds,
                nao_me_seguem_mais=sorted({item.strip().lower() for item in payload.get("nao_me_seguem_mais", []) if isinstance(item, str) and item.strip()}),
            )

        except Exception as exc:
            logger.error(f"Erro ao criar CompareData a partir do cache importado: {exc}")
            raise

    def _apply_state_payload_only(self, payload: dict[str, Any]) -> None:
        try:
            followers = {item.strip().lower() for item in payload.get("followers", []) if isinstance(item, str) and item.strip()}
            following = {item.strip().lower() for item in payload.get("following", []) if isinstance(item, str) and item.strip()}
            values = [item.strip().lower() for item in payload.get("nao_retribuem", []) if isinstance(item, str) and item.strip()]
            no_longer_follow_me = sorted({item.strip().lower() for item in payload.get("nao_me_seguem_mais", []) if isinstance(item, str) and item.strip()})

            self._followers_values = sorted(followers)
            self._following_values = sorted(following)

            if followers or following:
                self._non_followers_values = sorted(following - followers)
                self._non_following_values = sorted(followers - following)
                self._mutual_values = sorted(following & followers)

            else:
                self._non_followers_values = values
                self._non_following_values = []
                self._mutual_values = []
                self._followers_values = sorted({item.strip().lower() for item in set(self._non_following_values).union(self._mutual_values) if isinstance(item, str) and item.strip()})
                self._following_values = sorted({item.strip().lower() for item in set(self._non_followers_values).union(self._mutual_values) if isinstance(item, str) and item.strip()})

            self._set_counts_values(None, None, None, None, None)
            self._set_cache_status("none")
            self._set_rate_status_unavailable()
            self._set_requests_used(None)
            self._update_relationship_tab_counts(followers=len(self._followers_values), following=len(self._following_values),)
            self._update_primary_tab_counts(non_followers=len(self._non_followers_values), non_following=len(self._non_following_values), mutuals=len(self._mutual_values),)
            self._fill_text(self.followers_text, self._followers_values)
            self._fill_text(self.following_text, self._following_values)
            self._fill_text(self.nao_retribuem_text, self._non_followers_values)
            self._fill_text(self.eu_nao_retribuo_text, self._non_following_values)
            self._fill_text(self.mutuos_text, self._mutual_values)
            self._fill_new_non_followers(no_longer_follow_me or values)

        except Exception as exc:
            logger.error(f"Erro ao aplicar payload de estado: {exc}")

    def _build_cache_payload_from_ui(self, user: str, saved_at_epoch: float) -> dict[str, Any]:
        try:
            followers = sorted({item.strip().lower() for item in self._followers_values if isinstance(item, str) and item.strip()})
            following = sorted({item.strip().lower() for item in self._following_values if isinstance(item, str) and item.strip()})

            if not followers:
                followers = sorted({item.strip().lower() for item in set(self._non_following_values).union(self._mutual_values) if isinstance(item, str) and item.strip()})

            if not following:
                following = sorted({item.strip().lower() for item in set(self._non_followers_values).union(self._mutual_values) if isinstance(item, str) and item.strip()})

            nao_me_seguem_mais: list[str] = []

            for idx in range(self.novos_nao_seguidores_list.count()):
                item = self.novos_nao_seguidores_list.item(idx)

                if item is None:
                    continue

                text = item.text()

                if isinstance(text, str):
                    normalized_text = text.strip().lower()

                    if normalized_text:
                        nao_me_seguem_mais.append(normalized_text)

            rate_info = self._rate_status_info
            reset_at = getattr(rate_info, "reset_at", None)

            return {
                "user": user,
                "saved_at_epoch": float(saved_at_epoch),
                "followers": followers,
                "following": following,
                "nao_retribuem": sorted({item.strip().lower() for item in self._non_followers_values if isinstance(item, str) and item.strip()}),
                "eu_nao_retribuo": sorted({item.strip().lower() for item in self._non_following_values if isinstance(item, str) and item.strip()}),
                "mutuos": sorted({item.strip().lower() for item in self._mutual_values if isinstance(item, str) and item.strip()}),
                "nao_me_seguem_mais": sorted({item.strip().lower() for item in nao_me_seguem_mais if isinstance(item, str) and item.strip()}),
                "rate_limit": {
                    "remaining": self._to_int_or_none(getattr(rate_info, "remaining", None)),
                    "limit": self._to_int_or_none(getattr(rate_info, "limit", None)),
                    "cost": self._to_int_or_none(getattr(rate_info, "cost", None)),
                    "resetAt": reset_at if isinstance(reset_at, str) else None,
                },
            }

        except Exception as exc:
            logger.error(f"Erro ao construir payload de cache para exportação: {exc}")
            return {
                "user": user,
                "saved_at_epoch": float(saved_at_epoch),
                "followers": [],
                "following": [],
                "nao_retribuem": [],
                "eu_nao_retribuo": [],
                "mutuos": [],
                "nao_me_seguem_mais": [],
                "rate_limit": {
                    "remaining": None,
                    "limit": None,
                    "cost": None,
                    "resetAt": None,
                },
            }

    def _build_state_payload(self, user: str, saved_at_epoch: float, values: list[str]) -> dict[str, Any]:
        try:
            followers = sorted({item.strip().lower() for item in self._followers_values if isinstance(item, str) and item.strip()})
            following = sorted({item.strip().lower() for item in self._following_values if isinstance(item, str) and item.strip()})

            if not followers:
                followers = sorted({item.strip().lower() for item in set(self._non_following_values).union(self._mutual_values) if isinstance(item, str) and item.strip()})

            if not following:
                following = sorted({item.strip().lower() for item in set(self._non_followers_values).union(self._mutual_values) if isinstance(item, str) and item.strip()})

            return {
                "user": user,
                "saved_at_epoch": float(saved_at_epoch),
                "followers": followers,
                "following": following,
                "nao_retribuem": sorted({item.strip().lower() for item in self._non_followers_values if isinstance(item, str) and item.strip()}),
                "eu_nao_retribuo": sorted({item.strip().lower() for item in self._non_following_values if isinstance(item, str) and item.strip()}),
                "mutuos": sorted({item.strip().lower() for item in self._mutual_values if isinstance(item, str) and item.strip()}),
                "nao_me_seguem_mais": sorted({item.strip().lower() for item in values if isinstance(item, str) and item.strip()}),
            }

        except Exception as exc:
            logger.error(f"Erro ao construir payload de estado para exportação: {exc}")
            return {
                "user": user,
                "saved_at_epoch": float(saved_at_epoch),
                "followers": [],
                "following": [],
                "nao_retribuem": [],
                "eu_nao_retribuo": [],
                "mutuos": [],
                "nao_me_seguem_mais": [],
            }

    def _on_language_changed(self, language_code: str) -> None:
        try:
            if self._menu_bar_ui is not None:
                self._menu_bar_ui.set_checked_language(language_code)

            self._apply_translations()

        except Exception as exc:
            logger.error(f"Erro ao processar mudança de idioma: {exc}")

    def changeEvent(self, event: QEvent) -> None:
        try:
            if event.type() == QEvent.LanguageChange:
                self._apply_translations()

        except Exception as exc:
            logger.error(f"Erro ao processar evento de mudança de idioma: {exc}")

        super().changeEvent(event)

    def _stop_theme_icon_watcher(self) -> None:
        try:
            if self._theme_icon_timer is None:
                return

            try:
                self._theme_icon_timer.stop()

            except RuntimeError:
                pass

            except Exception as exc:
                logger.error(f"Erro ao interromper timer de tema: {exc}")

            self._theme_icon_timer = None

        except Exception as exc:
            logger.error(f"Erro ao finalizar verificador de tema: {exc}")

    def _disconnect_active_worker_ui_signals(self) -> None:
        try:
            if self._worker is None:
                return

            if self._active_worker_mode == "fetch":
                signal_slot_pairs = [
                    ("success", self._on_fetch_success),
                    ("error", self._on_fetch_error),
                ]

            elif self._active_worker_mode == "unfollow":
                signal_slot_pairs = [
                    ("success", self._on_unfollow_success),
                    ("error", self._on_unfollow_error),
                ]

            else:
                return

            for signal_name, slot in signal_slot_pairs:
                signal = getattr(self._worker, signal_name, None)

                if signal is None:
                    continue

                try:
                    signal.disconnect(slot)

                except (RuntimeError, TypeError):
                    pass

                except Exception as exc:
                    logger.error(f"Erro ao desconectar sinal '{signal_name}' durante fechamento: {exc}")

        except Exception as exc:
            logger.error(f"Erro ao desconectar sinais da thread ativa: {exc}")

    def _shutdown_active_worker(self, wait_timeout_ms: int = 15000) -> None:
        try:
            thread = self._thread

            if thread is None:
                self._worker = None
                return

            try:
                is_running = thread.isRunning()

            except RuntimeError:
                is_running = False

            if is_running:
                try:
                    thread.requestInterruption()

                except Exception:
                    pass

                try:
                    thread.quit()

                except RuntimeError:
                    pass

                except Exception as exc:
                    logger.error(f"Erro ao solicitar encerramento da thread: {exc}")

                try:
                    finished = thread.wait(max(0, int(wait_timeout_ms)))

                except RuntimeError:
                    finished = True

                except Exception as exc:
                    logger.error(f"Erro ao aguardar finalização da thread: {exc}")
                    finished = False

                if not finished:
                    logger.error("Thread de trabalho não finalizou a tempo; forçando encerramento.")

                    try:
                        thread.terminate()

                    except RuntimeError:
                        pass

                    except Exception as exc:
                        logger.error(f"Erro ao forçar encerramento da thread: {exc}")

                    try:
                        thread.wait(2000)

                    except RuntimeError:
                        pass

                    except Exception as exc:
                        logger.error(f"Erro ao aguardar thread após encerramento forçado: {exc}")

            self._worker = None
            self._thread = None
            self._active_worker_mode = None

        except Exception as exc:
            logger.error(f"Erro ao finalizar thread ativa no fechamento da janela: {exc}")

    def closeEvent(self, event) -> None:
        try:
            try:
                if self._app_instance is not None:
                    self._app_instance.setProperty("_compare_follow_close_requested", True)

            except Exception:
                pass

            self._stop_theme_icon_watcher()
            self._disconnect_active_worker_ui_signals()
            self._shutdown_active_worker()

            for attr_name in ("_manual_dialog", "_sobre_dialog"):
                dialog = getattr(self, attr_name, None)

                if dialog is None:
                    continue

                try:
                    dialog.close()

                except RuntimeError:
                    pass

                except Exception as exc:
                    logger.error(f"Erro ao fechar diálogo '{attr_name}': {exc}")

                finally:
                    try:
                        setattr(self, attr_name, None)

                    except Exception:
                        pass

        except Exception as exc:
            logger.error(f"Erro ao processar fechamento da janela principal: {exc}")

        super().closeEvent(event)

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

    def _configure_tab(self, tabs: QTabWidget, title: str, widget: QPlainTextEdit) -> int:
        try:
            widget.setReadOnly(True)
            widget.setLineWrapMode(QPlainTextEdit.NoWrap)
            return tabs.addTab(widget, self._format_tab_title(title, 0))

        except Exception as exc:
            logger.error(f"Erro ao configurar aba '{title}': {exc}")
            return -1

    def _configure_new_non_followers_tab(self, tabs: QTabWidget) -> int:
        try:
            container = QWidget()
            layout = QVBoxLayout(container)
            layout.setContentsMargins(8, 8, 8, 8)
            layout.setSpacing(8)
            layout.addWidget(self.novos_nao_seguidores_list, stretch=1)
            layout.addWidget(self.unfollow_button)
            return tabs.addTab(container, self._format_tab_title(self._tab_title_new_non_followers, 0))

        except Exception as exc:
            logger.error(f"Erro ao configurar aba de novos não seguidores: {exc}")
            return -1

    @staticmethod
    def _format_tab_title(title: str, count: int) -> str:
        try:
            return f"{title} = {max(count, 0)}"

        except Exception as exc:
            logger.error(f"Erro ao formatar título da aba: {exc}")
            return title

    def _set_tab_count(self, tab_index: int, title: str, count: int) -> None:
        try:
            if self.tabs is None or tab_index < 0:
                return

            self.tabs.setTabText(tab_index, self._format_tab_title(title, count))

        except Exception as exc:
            logger.error(f"Erro ao atualizar contagem da aba '{title}': {exc}")

    def _refresh_tab_titles(self) -> None:
        try:
            self._set_tab_count(self._tab_followers_index, self._tab_title_followers, self._tab_followers_count)
            self._set_tab_count(self._tab_following_index, self._tab_title_following, self._tab_following_count)
            self._set_tab_count(self._tab_non_followers_index, self._tab_title_non_followers, self._tab_non_followers_count)
            self._set_tab_count(self._tab_non_following_index, self._tab_title_non_following, self._tab_non_following_count)
            self._set_tab_count(self._tab_mutuals_index, self._tab_title_mutuals, self._tab_mutuals_count)
            self._set_tab_count(self._tab_new_non_followers_index, self._tab_title_new_non_followers, self._tab_new_non_followers_count)

        except Exception as exc:
            logger.error(f"Erro ao atualizar títulos das abas: {exc}")

    def _update_relationship_tab_counts(self, followers: int, following: int) -> None:
        try:
            self._tab_followers_count = max(followers, 0)
            self._tab_following_count = max(following, 0)
            self._refresh_tab_titles()

        except Exception as exc:
            logger.error(f"Erro ao atualizar contagens das abas de seguidores/seguindo: {exc}")

    def _update_primary_tab_counts(self, non_followers: int, non_following: int, mutuals: int) -> None:
        try:
            self._tab_non_followers_count = max(non_followers, 0)
            self._tab_non_following_count = max(non_following, 0)
            self._tab_mutuals_count = max(mutuals, 0)
            self._refresh_tab_titles()

        except Exception as exc:
            logger.error(f"Erro ao atualizar contagens das abas principais: {exc}")

    def _update_new_non_followers_count(self, new_non_followers: int) -> None:
        try:
            self._tab_new_non_followers_count = max(new_non_followers, 0)
            self._refresh_tab_titles()

        except Exception as exc:
            logger.error(f"Erro ao atualizar contagem da aba de novos não seguidores: {exc}")

    def _set_counts_values(self, following: int | None, followers: int | None, non_following: int | None, mutuals: int | None, no_longer_follow_me: int | None,) -> None:
        try:
            self._counts_following = following
            self._counts_followers = followers
            self._counts_non_following = non_following
            self._counts_mutuals = mutuals
            self._counts_no_longer_follow_me = no_longer_follow_me
            self._render_counts_label()

        except Exception as exc:
            logger.error(f"Erro ao atualizar contagens do resumo: {exc}")

    def _render_counts_label(self) -> None:
        try:
            following_value = "-" if self._counts_following is None else str(self._counts_following)
            followers_value = "-" if self._counts_followers is None else str(self._counts_followers)
            non_following_value = "-" if self._counts_non_following is None else str(self._counts_non_following)
            mutuals_value = "-" if self._counts_mutuals is None else str(self._counts_mutuals)
            no_longer_follow_me_value = ("-" if self._counts_no_longer_follow_me is None else str(self._counts_no_longer_follow_me))
            self.counts_label.setText(self._tr("Seguidores = {followers}; Sigo = {following}; Não sigo = {non_following}; Mútuos = {mutuals}; Não me seguem mais = {no_longer_follow_me}").format(
                followers=followers_value, following=following_value, non_following=non_following_value, mutuals=mutuals_value, no_longer_follow_me=no_longer_follow_me_value,))

        except Exception as exc:
            logger.error(f"Erro ao renderizar rótulo de contagens: {exc}")

    def _set_cache_status(self, mode: str, **payload: Any) -> None:
        try:
            self._cache_status_mode = mode
            self._cache_status_payload = payload
            self.cache_label.setText(self._render_cache_status())

        except Exception as exc:
            logger.error(f"Erro ao atualizar status de cache: {exc}")

    def _set_cache_status_from_data(self, data: Any) -> None:
        try:
            if data.from_cache:
                age = int(data.cache_age_seconds or 0)
                self._set_cache_status("from_cache", age=age)
                return

            self._set_cache_status("from_graphql", requests=int(data.requests_made))

        except Exception as exc:
            logger.error(f"Erro ao atualizar status de cache com dados: {exc}")

    def _render_cache_status(self) -> str:
        try:
            mode = self._cache_status_mode
            payload = self._cache_status_payload

            if mode == "updating":
                return self._tr("Atualizando dados...")

            if mode == "interrupted":
                return self._tr("Atualização interrompida pelo usuário.")

            if mode == "start_failed":
                return self._tr("Falha ao iniciar atualização.")

            if mode == "fetch_failed":
                return self._tr("Falha ao atualizar.")

            if mode == "from_cache":
                return self._tr("Origem: cache local (idade {age}s)").format(age=payload.get("age", 0))

            if mode == "from_graphql":
                return self._tr("Origem: GraphQL (requisições nesta atualização: {requests})").format(requests=payload.get("requests", 0))

            if mode == "unfollowing":
                return self._tr("Executando unfollow em {count} perfil(is)...").format(count=payload.get("count", 0))

            if mode == "unfollow_failed":
                return self._tr("Falha ao executar unfollow.")

            return self._tr("Origem: -")

        except Exception as exc:
            logger.error(f"Erro ao renderizar status de cache: {exc}")
            return self._tr("Origem: -")

    def _set_rate_status_info(self, info: Any) -> None:
        try:
            self._rate_status_mode = "info"
            self._rate_status_info = info
            self.rate_label.setText(self._render_rate_status())

        except Exception as exc:
            logger.error(f"Erro ao atualizar status do rate limit: {exc}")

    def _set_rate_status_unavailable(self) -> None:
        try:
            self._rate_status_mode = "unavailable"
            self._rate_status_info = None
            self.rate_label.setText(self._render_rate_status())

        except Exception as exc:
            logger.error(f"Erro ao marcar rate limit como indisponível: {exc}")

    def _set_rate_status_updating(self) -> None:
        try:
            self._rate_status_mode = "updating"
            self.rate_label.setText(self._render_rate_status())

        except Exception as exc:
            logger.error(f"Erro ao marcar rate limit como atualizando: {exc}")

    def _render_rate_status(self) -> str:
        try:
            if self._rate_status_mode == "updating":
                return self._tr("Rate limit restante: atualizando...")

            if self._rate_status_mode != "info":
                return self._tr("Rate limit restante: indisponível")

            info = self._rate_status_info
            if info is None or info.remaining is None or info.limit is None:
                return self._tr("Rate limit restante: indisponível")

            extras: list[str] = []

            if info.cost is not None:
                extras.append(self._tr("custo {value}").format(value=info.cost))

            if info.reset_at:
                extras.append(self._tr("reset {value}").format(value=info.reset_at))

            suffix = f" ({' | '.join(extras)})" if extras else ""
            return self._tr("Rate limit restante: {remaining}/{limit}{suffix}").format(remaining=info.remaining, limit=info.limit, suffix=suffix,)

        except Exception as exc:
            logger.error(f"Erro ao renderizar status de rate limit: {exc}")
            return self._tr("Rate limit restante: indisponível")

    def _set_requests_used(self, count: int | None) -> None:
        try:
            self._requests_used_count = count
            self.requests_label.setText(self._render_requests_status())

        except Exception as exc:
            logger.error(f"Erro ao atualizar total de requisições: {exc}")

    def _render_requests_status(self) -> str:
        try:
            count_value = "-" if self._requests_used_count is None else str(self._requests_used_count)
            return self._tr("Requisições usadas nesta atualização: {count}").format(count=count_value)

        except Exception as exc:
            logger.error(f"Erro ao renderizar status de requisições: {exc}")
            return self._tr("Requisições usadas nesta atualização: -")

    def _load_startup_cache(self, user: str) -> None:
        try:
            try:
                cached = self._load_cached_data_fn(user.strip(), include_expired=True)

            except TypeError:
                cached = self._load_cached_data_fn(user.strip())

            if cached is None:
                self._fill_new_non_followers([])
                return

            self._on_fetch_success(cached)

        except Exception as exc:
            logger.error(f"Erro ao carregar cache de inicialização para o usuário '{user}': {exc}")

    def refresh(self, _checked: bool = False) -> None:
        try:
            if self._is_loading and not self._is_refresh_thread_running():
                self._set_loading(False)

            try:
                self._start_refresh(force_network_refresh=self.force_refresh_checkbox.isChecked())

            except KeyboardInterrupt:
                self._set_loading(False)
                self._set_cache_status("interrupted")
                self._set_rate_status_unavailable()
                self._set_requests_used(0)

            except BaseException:
                self._set_loading(False)
                self._set_cache_status("start_failed")
                self._set_rate_status_unavailable()
                self._set_requests_used(0)
                raise

        except Exception as exc:
            logger.error(f"Erro ao iniciar atualização: {exc}")

    def _start_refresh(self, force_network_refresh: bool) -> None:
        try:
            if self._is_loading:
                return

            user = self.user_input.text().strip()

            if not user:
                QMessageBox.critical(self, self._tr("Entrada inválida"), self._tr("Informe um usuário GitHub."))
                return

            self._set_loading(True)
            self._set_cache_status("updating")
            self._thread = QThread(self)
            self._worker = self._fetch_worker_cls(user=user, force_network_refresh=force_network_refresh, build_session_fn=self._build_session_fn, get_compare_data_fn=self._get_compare_data_fn, config_error_cls=self._config_error_cls,)
            self._active_worker_mode = "fetch"
            self._worker.moveToThread(self._thread)

            self._thread.started.connect(self._worker.run)
            self._worker.success.connect(self._on_fetch_success)
            self._worker.error.connect(self._on_fetch_error)
            self._worker.finished.connect(self._thread.quit)
            self._worker.finished.connect(self._worker.deleteLater)
            self._thread.finished.connect(self._thread.deleteLater)
            self._thread.finished.connect(self._on_worker_finished)
            self._thread.start()

        except Exception as exc:
            logger.error(f"Erro ao iniciar processo de atualização: {exc}")

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

    def _on_worker_finished(self) -> None:
        try:
            if self.sender() is self._thread:
                self._worker = None
                self._thread = None
                self._active_worker_mode = None

            if self._is_loading and not self._is_refresh_thread_running():
                self._set_loading(False)

        except Exception as exc:
            logger.error(f"Erro ao finalizar thread de trabalho: {exc}")

    def _is_refresh_thread_running(self) -> bool:
        try:
            if self._thread is None:
                return False

            try:
                return self._thread.isRunning()

            except RuntimeError:
                return False

        except Exception as exc:
            logger.error(f"Erro ao verificar estado da thread de atualização: {exc}")
            return False

    def _calculate_new_non_followers(self, data: Any) -> list[str]:
        try:
            values = getattr(data, "nao_me_seguem_mais", None)

            if isinstance(values, list):
                return sorted({item.strip().lower() for item in values if isinstance(item, str) and item.strip()})

            previous_followers = self._load_previous_non_followers_fn(data.user)

            if previous_followers is None:
                return []

            current_followers = {item.strip().lower() for item in getattr(data, "followers", []) if isinstance(item, str) and item.strip()}
            return sorted(previous_followers - current_followers)

        except Exception as exc:
            user_value = getattr(data, "user", self.user_input.text().strip() or "<desconhecido>")
            logger.error(f"Erro ao calcular usuários que não me seguem mais para o usuário '{user_value}': {exc}")
            return []

    def _on_fetch_success(self, data: Any) -> None:
        try:
            if data is None:
                raise self._config_error_cls("Dados de comparação vazios.")

            if not hasattr(data, "followers") or not hasattr(data, "following"):
                raise self._config_error_cls("Dados de comparação inválidos.")

            self._set_loading(False)
            no_longer_follow_me_values = self._calculate_new_non_followers(data)
            normalized_followers = sorted({item.strip().lower() for item in data.followers if isinstance(item, str) and item.strip()})
            normalized_following = sorted({item.strip().lower() for item in data.following if isinstance(item, str) and item.strip()})
            self._set_counts_values(following=len(normalized_following), followers=len(normalized_followers), non_following=len(data.eu_nao_retribuo), mutuals=len(data.mutuos), no_longer_follow_me=len(no_longer_follow_me_values),)
            self._set_cache_status_from_data(data)
            self._set_rate_status_info(data.rate_limit)
            self._set_requests_used(data.requests_made)
            self._update_relationship_tab_counts(followers=len(normalized_followers), following=len(normalized_following),)
            self._update_primary_tab_counts(non_followers=len(data.nao_retribuem), non_following=len(data.eu_nao_retribuo), mutuals=len(data.mutuos),)
            self._followers_values = list(normalized_followers)
            self._following_values = list(normalized_following)
            self._non_followers_values = list(data.nao_retribuem)
            self._non_following_values = list(data.eu_nao_retribuo)
            self._mutual_values = list(data.mutuos)
            self._fill_text(self.followers_text, self._followers_values)
            self._fill_text(self.following_text, self._following_values)
            self._fill_text(self.nao_retribuem_text, self._non_followers_values)
            self._fill_text(self.eu_nao_retribuo_text, self._non_following_values)
            self._fill_text(self.mutuos_text, self._mutual_values)
            self._fill_new_non_followers(no_longer_follow_me_values)

        except Exception as exc:
            user_value = getattr(data, "user", self.user_input.text().strip() or "<desconhecido>")
            logger.error(f"Erro ao processar dados de comparação para o usuário '{user_value}': {exc}")
            self._on_fetch_error(exc)

    def _on_fetch_error(self, exc: Exception) -> None:
        try:
            self._set_loading(False)
            error_message = self._format_exception_fn(exc)
            self._set_cache_status("fetch_failed")
            self._set_rate_status_unavailable()
            self._set_requests_used(0)
            self._set_counts_values(following=0, followers=0, non_following=0, mutuals=0, no_longer_follow_me=0)
            self._update_relationship_tab_counts(followers=0, following=0)
            self._update_primary_tab_counts(non_followers=0, non_following=0, mutuals=0)
            self._followers_values = []
            self._following_values = []
            self._non_followers_values = [self._tr("Erro: {message}").format(message=error_message)]
            self._non_following_values = []
            self._mutual_values = []
            self._fill_text(self.followers_text, self._followers_values)
            self._fill_text(self.following_text, self._following_values)
            self._fill_text(self.nao_retribuem_text, self._non_followers_values)
            self._fill_text(self.eu_nao_retribuo_text, self._non_following_values)
            self._fill_text(self.mutuos_text, self._mutual_values)
            self._fill_new_non_followers([])
            QMessageBox.critical(self, self._tr("Erro ao consultar GitHub"), error_message)

        except Exception as log_exc:
            logger.error(f"Erro ao processar erro de consulta para o usuário '{self.user_input.text()}': {log_exc}")

    def _fill_new_non_followers(self, values: list[str]) -> None:
        try:
            self.novos_nao_seguidores_list.blockSignals(True)
            self.novos_nao_seguidores_list.clear()

            for login in values:
                item = QListWidgetItem(login)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Unchecked)
                self.novos_nao_seguidores_list.addItem(item)

            self.novos_nao_seguidores_list.blockSignals(False)
            self._update_unfollow_button_state()
            self._update_new_non_followers_count(len(values))

        except Exception as exc:
            logger.error(f"Erro ao preencher lista de novos não seguidores: {exc}")

    def _checked_new_non_followers(self) -> list[str]:
        try:
            checked: list[str] = []

            for idx in range(self.novos_nao_seguidores_list.count()):
                item = self.novos_nao_seguidores_list.item(idx)

                if item.checkState() == Qt.Checked:
                    checked.append(item.text())

            return checked

        except Exception as exc:
            logger.error(f"Erro ao obter itens selecionados de novos não seguidores: {exc}")
            return []

    def _update_unfollow_button_state(self) -> None:
        try:
            has_checked_items = bool(self._checked_new_non_followers())
            self.unfollow_button.setEnabled((not self._is_loading) and has_checked_items)

        except Exception as exc:
            logger.error(f"Erro ao atualizar estado do botão de unfollow: {exc}")

    def _unfollow_selected(self) -> None:
        try:
            if self._is_loading:
                return

            selected_profiles = self._checked_new_non_followers()

            if not selected_profiles:
                QMessageBox.information(self, self._tr("Unfollow"), self._tr("Selecione ao menos um perfil na lista."))
                return

            preview = ", ".join(selected_profiles[:10])

            if len(selected_profiles) > 10:
                preview += ", ..."

            answer = QMessageBox.question(
                self,
                self._tr("Confirmar unfollow"),
                self._tr("Executar unfollow de {count} perfil(is)?\n\n{preview}").format(count=len(selected_profiles), preview=preview,),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if answer != QMessageBox.Yes:
                return

            self._set_loading(True)
            self._set_cache_status("unfollowing", count=len(selected_profiles))
            self._set_rate_status_updating()
            self._set_requests_used(None)
            self._thread = QThread(self)
            self._worker = self._unfollow_worker_cls(
                usernames=selected_profiles,
                build_session_fn=self._build_session_fn,
                get_token_fn=self._get_token_fn,
                unfollow_user_fn=self._unfollow_user_fn,
                format_exception_fn=self._format_exception_fn,
                config_error_cls=self._config_error_cls,
                unfollow_result_cls=self._unfollow_result_cls,
            )
            self._active_worker_mode = "unfollow"
            self._worker.moveToThread(self._thread)

            self._thread.started.connect(self._worker.run)
            self._worker.success.connect(self._on_unfollow_success)
            self._worker.error.connect(self._on_unfollow_error)
            self._worker.finished.connect(self._thread.quit)
            self._worker.finished.connect(self._worker.deleteLater)
            self._thread.finished.connect(self._thread.deleteLater)
            self._thread.finished.connect(self._on_worker_finished)
            self._thread.start()

        except Exception as exc:
            logger.error(f"Erro ao iniciar processo de unfollow: {exc}")

    def _on_unfollow_success(self, result: Any) -> None:
        try:
            self._set_loading(False)
            succeeded = len(result.succeeded)
            failed = len(result.failed)

            if succeeded == 0 and failed == 0:
                QMessageBox.information(self, self._tr("Unfollow"), self._tr("Nenhum perfil foi processado."))
                return

            summary = self._tr("Unfollow concluído.\nSucesso: {succeeded}\nFalhas: {failed}").format(succeeded=succeeded, failed=failed,)

            if failed:
                details = "\n".join([f"- {login}: {message}" for login, message in result.failed.items()])
                QMessageBox.warning(self, self._tr("Unfollow concluído com falhas"), f"{summary}\n\n{details}")

            else:
                QMessageBox.information(self, self._tr("Unfollow concluído"), summary)

            if succeeded > 0:
                self._start_refresh(force_network_refresh=True)

        except Exception as exc:
            logger.error(f"Erro ao processar resultado de unfollow: {exc}")

    def _on_unfollow_error(self, exc: Exception) -> None:
        try:
            self._set_loading(False)
            error_message = self._format_exception_fn(exc)
            self._set_cache_status("unfollow_failed")
            QMessageBox.critical(self, self._tr("Erro ao executar unfollow"), error_message)

        except Exception as log_exc:
            logger.error(f"Erro ao processar erro de unfollow: {log_exc}")

    def _fill_text(self, widget: QPlainTextEdit, values: list[str]) -> None:
        try:
            widget.setPlainText("\n".join(values) if values else self._tr("(ninguém)"))

        except Exception as exc:
            logger.error(f"Erro ao preencher texto do widget: {exc}")

    def _start_theme_icon_watcher(self) -> None:
        try:
            if os.name != "nt":
                return

            self._theme_icon_timer = QTimer(self)
            self._theme_icon_timer.setInterval(1200)
            self._theme_icon_timer.timeout.connect(self._refresh_theme_icon_if_needed)
            self._theme_icon_timer.start()

        except Exception as exc:
            logger.error(f"Erro ao iniciar verificador de tema para ícone: {exc}")

    def _refresh_theme_icon_if_needed(self) -> None:
        try:
            if os.name != "nt":
                return

            next_theme_value = self._resolve_theme_flag_fn()
            if next_theme_value == self._theme_is_light:
                return

            next_icon_path = self._resolve_icon_for_theme_fn(next_theme_value)
            if not next_icon_path or not os.path.exists(next_icon_path):
                return

            if next_icon_path == self._current_icon_path:
                self._theme_is_light = next_theme_value
                return

            next_icon = QIcon(next_icon_path)
            if next_icon.isNull():
                return

            self._theme_is_light = next_theme_value
            self._current_icon_path = next_icon_path
            self._app_instance.setWindowIcon(next_icon)
            self.setWindowIcon(next_icon)

        except Exception as exc:
            logger.error(f"Erro ao atualizar ícone para tema: {exc}")
