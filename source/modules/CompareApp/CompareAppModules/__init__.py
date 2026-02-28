from __future__ import annotations

from typing import Type

from .capp_01_connect_translation_manager import _connect_translation_manager
from .capp_02_get_current_language_code import _get_current_language_code
from .capp_03_on_language_selected import _on_language_selected
from .capp_04_show_about import _show_about
from .capp_05_show_manual import _show_manual
from .capp_06_file_actions_locked import _file_actions_locked
from .capp_07_on_new_selected import _on_new_selected
from .capp_08_on_open_selected import _on_open_selected
from .capp_09_on_save_selected import _on_save_selected
from .capp_10_on_help_selected import _on_help_selected
from .capp_11_on_close_selected import _on_close_selected
from .capp_12_on_set_github_token_selected import _on_set_github_token_selected
from .capp_13_resolve_database_file_paths import _resolve_database_file_paths
from .capp_14_on_delete_selected import _on_delete_selected
from .capp_15_remove_file_for_token_reset import _remove_file_for_token_reset
from .capp_16_restart_application import _restart_application
from .capp_17_on_reset_github_token_selected import _on_reset_github_token_selected
from .capp_18_clear_reported_data import _clear_reported_data
from .capp_19_clear_persistent_data_files import _clear_persistent_data_files
from .capp_20_ensure_json_path import _ensure_json_path
from .capp_21_read_json_dict import _read_json_dict
from .capp_22_write_json_atomic import _write_json_atomic
from .capp_23_to_int_or_none import _to_int_or_none
from .capp_24_normalize_cache_payload import _normalize_cache_payload
from .capp_25_normalize_state_payload import _normalize_state_payload
from .capp_26_parse_import_payload import _parse_import_payload
from .capp_27_create_compare_data_from_cache_payload import _create_compare_data_from_cache_payload
from .capp_28_apply_state_payload_only import _apply_state_payload_only
from .capp_29_build_cache_payload_from_ui import _build_cache_payload_from_ui
from .capp_30_build_state_payload import _build_state_payload
from .capp_31_on_language_changed import _on_language_changed
from .capp_32_changeEvent import changeEvent
from .capp_33_stop_theme_icon_watcher import _stop_theme_icon_watcher
from .capp_34_disconnect_active_worker_ui_signals import _disconnect_active_worker_ui_signals
from .capp_35_shutdown_active_worker import _shutdown_active_worker
from .capp_36_closeEvent import closeEvent
from .capp_37_apply_translations import _apply_translations
from .capp_38_configure_tab import _configure_tab
from .capp_39_configure_new_non_followers_tab import _configure_new_non_followers_tab
from .capp_40_format_tab_title import _format_tab_title
from .capp_41_set_tab_count import _set_tab_count
from .capp_42_refresh_tab_titles import _refresh_tab_titles
from .capp_43_update_relationship_tab_counts import _update_relationship_tab_counts
from .capp_44_update_primary_tab_counts import _update_primary_tab_counts
from .capp_45_update_new_non_followers_count import _update_new_non_followers_count
from .capp_46_set_counts_values import _set_counts_values
from .capp_47_render_counts_label import _render_counts_label
from .capp_48_set_cache_status import _set_cache_status
from .capp_49_set_cache_status_from_data import _set_cache_status_from_data
from .capp_50_render_cache_status import _render_cache_status
from .capp_51_set_rate_status_info import _set_rate_status_info
from .capp_52_set_rate_status_unavailable import _set_rate_status_unavailable
from .capp_53_set_rate_status_updating import _set_rate_status_updating
from .capp_54_render_rate_status import _render_rate_status
from .capp_55_set_requests_used import _set_requests_used
from .capp_56_render_requests_status import _render_requests_status
from .capp_57_load_startup_cache import _load_startup_cache
from .capp_58_load_cached_data_for_user import _load_cached_data_for_user
from .capp_59_is_missing_token_error import _is_missing_token_error
from .capp_60_request_and_persist_github_token import _request_and_persist_github_token
from .capp_61_ensure_token_available_for_refresh import _ensure_token_available_for_refresh
from .capp_62_refresh import refresh
from .capp_63_start_refresh import _start_refresh
from .capp_64_set_loading import _set_loading
from .capp_65_on_worker_finished import _on_worker_finished
from .capp_66_is_refresh_thread_running import _is_refresh_thread_running
from .capp_67_calculate_new_non_followers import _calculate_new_non_followers
from .capp_68_on_fetch_success import _on_fetch_success
from .capp_69_on_fetch_error import _on_fetch_error
from .capp_70_fill_new_non_followers import _fill_new_non_followers
from .capp_71_checked_new_non_followers import _checked_new_non_followers
from .capp_72_update_unfollow_button_state import _update_unfollow_button_state
from .capp_73_unfollow_selected import _unfollow_selected
from .capp_74_on_unfollow_success import _on_unfollow_success
from .capp_75_on_unfollow_error import _on_unfollow_error
from .capp_76_fill_text import _fill_text
from .capp_77_start_theme_icon_watcher import _start_theme_icon_watcher
from .capp_78_refresh_theme_icon_if_needed import _refresh_theme_icon_if_needed

def bind_compare_app_methods(cls: Type[object]) -> Type[object]:
    cls._connect_translation_manager = _connect_translation_manager
    cls._get_current_language_code = _get_current_language_code
    cls._on_language_selected = _on_language_selected
    cls._show_about = _show_about
    cls._show_manual = _show_manual
    cls._file_actions_locked = _file_actions_locked
    cls._on_new_selected = _on_new_selected
    cls._on_open_selected = _on_open_selected
    cls._on_save_selected = _on_save_selected
    cls._on_help_selected = _on_help_selected
    cls._on_close_selected = _on_close_selected
    cls._on_set_github_token_selected = _on_set_github_token_selected
    cls._resolve_database_file_paths = _resolve_database_file_paths
    cls._on_delete_selected = _on_delete_selected
    cls._remove_file_for_token_reset = _remove_file_for_token_reset
    cls._restart_application = _restart_application
    cls._on_reset_github_token_selected = _on_reset_github_token_selected
    cls._clear_reported_data = _clear_reported_data
    cls._clear_persistent_data_files = _clear_persistent_data_files
    cls._ensure_json_path = staticmethod(_ensure_json_path)
    cls._read_json_dict = staticmethod(_read_json_dict)
    cls._write_json_atomic = staticmethod(_write_json_atomic)
    cls._to_int_or_none = staticmethod(_to_int_or_none)
    cls._normalize_cache_payload = _normalize_cache_payload
    cls._normalize_state_payload = _normalize_state_payload
    cls._parse_import_payload = _parse_import_payload
    cls._create_compare_data_from_cache_payload = _create_compare_data_from_cache_payload
    cls._apply_state_payload_only = _apply_state_payload_only
    cls._build_cache_payload_from_ui = _build_cache_payload_from_ui
    cls._build_state_payload = _build_state_payload
    cls._on_language_changed = _on_language_changed
    cls.changeEvent = changeEvent
    cls._stop_theme_icon_watcher = _stop_theme_icon_watcher
    cls._disconnect_active_worker_ui_signals = _disconnect_active_worker_ui_signals
    cls._shutdown_active_worker = _shutdown_active_worker
    cls.closeEvent = closeEvent
    cls._apply_translations = _apply_translations
    cls._configure_tab = _configure_tab
    cls._configure_new_non_followers_tab = _configure_new_non_followers_tab
    cls._format_tab_title = staticmethod(_format_tab_title)
    cls._set_tab_count = _set_tab_count
    cls._refresh_tab_titles = _refresh_tab_titles
    cls._update_relationship_tab_counts = _update_relationship_tab_counts
    cls._update_primary_tab_counts = _update_primary_tab_counts
    cls._update_new_non_followers_count = _update_new_non_followers_count
    cls._set_counts_values = _set_counts_values
    cls._render_counts_label = _render_counts_label
    cls._set_cache_status = _set_cache_status
    cls._set_cache_status_from_data = _set_cache_status_from_data
    cls._render_cache_status = _render_cache_status
    cls._set_rate_status_info = _set_rate_status_info
    cls._set_rate_status_unavailable = _set_rate_status_unavailable
    cls._set_rate_status_updating = _set_rate_status_updating
    cls._render_rate_status = _render_rate_status
    cls._set_requests_used = _set_requests_used
    cls._render_requests_status = _render_requests_status
    cls._load_startup_cache = _load_startup_cache
    cls._load_cached_data_for_user = _load_cached_data_for_user
    cls._is_missing_token_error = _is_missing_token_error
    cls._request_and_persist_github_token = _request_and_persist_github_token
    cls._ensure_token_available_for_refresh = _ensure_token_available_for_refresh
    cls.refresh = refresh
    cls._start_refresh = _start_refresh
    cls._set_loading = _set_loading
    cls._on_worker_finished = _on_worker_finished
    cls._is_refresh_thread_running = _is_refresh_thread_running
    cls._calculate_new_non_followers = _calculate_new_non_followers
    cls._on_fetch_success = _on_fetch_success
    cls._on_fetch_error = _on_fetch_error
    cls._fill_new_non_followers = _fill_new_non_followers
    cls._checked_new_non_followers = _checked_new_non_followers
    cls._update_unfollow_button_state = _update_unfollow_button_state
    cls._unfollow_selected = _unfollow_selected
    cls._on_unfollow_success = _on_unfollow_success
    cls._on_unfollow_error = _on_unfollow_error
    cls._fill_text = _fill_text
    cls._start_theme_icon_watcher = _start_theme_icon_watcher
    cls._refresh_theme_icon_if_needed = _refresh_theme_icon_if_needed
    return cls

__all__ = [
    "_connect_translation_manager",
    "_get_current_language_code",
    "_on_language_selected",
    "_show_about",
    "_show_manual",
    "_file_actions_locked",
    "_on_new_selected",
    "_on_open_selected",
    "_on_save_selected",
    "_on_help_selected",
    "_on_close_selected",
    "_on_set_github_token_selected",
    "_resolve_database_file_paths",
    "_on_delete_selected",
    "_remove_file_for_token_reset",
    "_restart_application",
    "_on_reset_github_token_selected",
    "_clear_reported_data",
    "_clear_persistent_data_files",
    "_ensure_json_path",
    "_read_json_dict",
    "_write_json_atomic",
    "_to_int_or_none",
    "_normalize_cache_payload",
    "_normalize_state_payload",
    "_parse_import_payload",
    "_create_compare_data_from_cache_payload",
    "_apply_state_payload_only",
    "_build_cache_payload_from_ui",
    "_build_state_payload",
    "_on_language_changed",
    "changeEvent",
    "_stop_theme_icon_watcher",
    "_disconnect_active_worker_ui_signals",
    "_shutdown_active_worker",
    "closeEvent",
    "_apply_translations",
    "_configure_tab",
    "_configure_new_non_followers_tab",
    "_format_tab_title",
    "_set_tab_count",
    "_refresh_tab_titles",
    "_update_relationship_tab_counts",
    "_update_primary_tab_counts",
    "_update_new_non_followers_count",
    "_set_counts_values",
    "_render_counts_label",
    "_set_cache_status",
    "_set_cache_status_from_data",
    "_render_cache_status",
    "_set_rate_status_info",
    "_set_rate_status_unavailable",
    "_set_rate_status_updating",
    "_render_rate_status",
    "_set_requests_used",
    "_render_requests_status",
    "_load_startup_cache",
    "_load_cached_data_for_user",
    "_is_missing_token_error",
    "_request_and_persist_github_token",
    "_ensure_token_available_for_refresh",
    "refresh",
    "_start_refresh",
    "_set_loading",
    "_on_worker_finished",
    "_is_refresh_thread_running",
    "_calculate_new_non_followers",
    "_on_fetch_success",
    "_on_fetch_error",
    "_fill_new_non_followers",
    "_checked_new_non_followers",
    "_update_unfollow_button_state",
    "_unfollow_selected",
    "_on_unfollow_success",
    "_on_unfollow_error",
    "_fill_text",
    "_start_theme_icon_watcher",
    "_refresh_theme_icon_if_needed",
    "bind_compare_app_methods",
]
