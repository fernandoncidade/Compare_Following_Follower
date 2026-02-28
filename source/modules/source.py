from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
import requests
from source.modules.RateLimitInfo import RateLimitInfo
from .src_01_get_persistent_base_dir import _get_persistent_base_dir as _get_persistent_base_dir_impl
from .src_02_resolve_persistent_file_path import _resolve_persistent_file_path as _resolve_persistent_file_path_impl
from .src_03_read_windows_light_theme_flag import _read_windows_light_theme_flag as _read_windows_light_theme_flag_impl
from .src_04_resolve_exact_icon_path import _resolve_exact_icon_path as _resolve_exact_icon_path_impl
from .src_05_resolve_app_icon_path_for_theme import _resolve_app_icon_path_for_theme as _resolve_app_icon_path_for_theme_impl
from .src_06_resolve_app_icon_path import _resolve_app_icon_path as _resolve_app_icon_path_impl
from .src_07_set_windows_app_user_model_id import _set_windows_app_user_model_id as _set_windows_app_user_model_id_impl
from .src_08_nao_retribuem import nao_retribuem as _nao_retribuem_impl
from .src_09_eu_nao_retribuo import eu_nao_retribuo as _eu_nao_retribuo_impl
from .src_10_mutuos import mutuos as _mutuos_impl
from .src_11_format_rate_limit_reset import _format_rate_limit_reset as _format_rate_limit_reset_impl
from .src_12_get_token import get_token as _get_token_impl
from .src_13_build_headers import build_headers as _build_headers_impl
from .src_14_build_session import build_session as _build_session_impl
from .src_15_unfollow_user import unfollow_user as _unfollow_user_impl
from .src_16_extract_connection import _extract_connection as _extract_connection_impl
from .src_17_fetch_graphql_page import GraphPage, fetch_graphql_page as _fetch_graphql_page_impl
from .src_18_fetch_relationships_graphql import CompareData, fetch_relationships_graphql as _fetch_relationships_graphql_impl
from .src_19_load_cache_file import _load_cache_file as _load_cache_file_impl
from .src_20_load_non_followers_state_file import _load_non_followers_state_file as _load_non_followers_state_file_impl
from .src_21_load_previous_non_followers import load_previous_non_followers as _load_previous_non_followers_impl
from .src_22_save_non_followers_state import save_non_followers_state as _save_non_followers_state_impl
from .src_23_load_cached_data import load_cached_data as _load_cached_data_impl
from .src_24_save_cached_data import save_cached_data as _save_cached_data_impl
from .src_25_get_compare_data import get_compare_data as _get_compare_data_impl
from .src_26_format_rate_limit import format_rate_limit as _format_rate_limit_impl
from .src_27_format_cache_status import format_cache_status as _format_cache_status_impl
from .src_28_print_cli_report import print_cli_report as _print_cli_report_impl
from .src_29_format_exception import format_exception as _format_exception_impl
from .src_30_run_gui import run_gui as _run_gui_impl
from .src_31_qt_excepthook import _qt_excepthook as _qt_excepthook_impl
from .src_32_persist_github_token import (
    PersistTokenResult,
    ResetTokenResult,
    persist_github_token as _persist_github_token_impl,
    reset_github_token as _reset_github_token_impl,
)
from .src_33_load_last_user import load_last_user as _load_last_user_impl
from .src_34_save_last_user import save_last_user as _save_last_user_impl

DEFAULT_USER = ""
VERIFY_SSL = os.getenv("GITHUB_INSECURE", "").strip().lower() not in {"1", "true", "yes"}
CONNECT_TIMEOUT = float(os.getenv("GITHUB_CONNECT_TIMEOUT", "10"))
READ_TIMEOUT = float(os.getenv("GITHUB_READ_TIMEOUT", "30"))
CACHE_TTL_SECONDS = int(os.getenv("FOLLOW_COMPARE_CACHE_TTL", "900"))
APP_ICON_FILENAME_DARK = "FollowingFollower_256-256.ico"
APP_ICON_FILENAME_CLEAR = "GitHubFollowersVazado_256-256.ico"
WINDOWS_APP_USER_MODEL_ID = "FollowingFollower.GitHubFollowCompare"


class ConfigError(RuntimeError):
    pass


class GraphQLError(RuntimeError):
    pass


@dataclass
class UnfollowResult:
    succeeded: list[str]
    failed: dict[str, str]


CACHE_FILE = _resolve_persistent_file_path_impl("FOLLOW_COMPARE_CACHE_FILE", ".github_follow_compare_atual.json")
NON_FOLLOWERS_STATE_FILE = _resolve_persistent_file_path_impl("FOLLOW_COMPARE_STATE_FILE", ".github_follow_compare_antigo.json")
LAST_USER_FILE = _resolve_persistent_file_path_impl("FOLLOW_COMPARE_LAST_USER_FILE", ".github_follow_compare_last_user.json")
GRAPHQL_URL = "https://api.github.com/graphql"
REST_API_URL = "https://api.github.com"

HEADERS_BASE = {
    "Accept": "application/vnd.github+json",
    "Content-Type": "application/json",
    "X-GitHub-Api-Version": "2022-11-28",
}

GRAPHQL_QUERY = """
query FollowCompare(
  $login: String!,
  $afterFollowers: String,
  $afterFollowing: String,
  $includeFollowers: Boolean!,
  $includeFollowing: Boolean!
) {
  user(login: $login) {
    followers(first: 100, after: $afterFollowers) @include(if: $includeFollowers) {
      nodes {
        login
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
    following(first: 100, after: $afterFollowing) @include(if: $includeFollowing) {
      nodes {
        login
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
  rateLimit {
    cost
    remaining
    limit
    resetAt
  }
}
""".strip()

def _get_persistent_base_dir() -> Path:
    return _get_persistent_base_dir_impl()

def _resolve_persistent_file_path(env_var: str, default_filename: str) -> Path:
    return _resolve_persistent_file_path_impl(env_var, default_filename)

def _read_windows_light_theme_flag() -> bool | None:
    return _read_windows_light_theme_flag_impl()

def _resolve_exact_icon_path(icon_filename: str) -> str | None:
    return _resolve_exact_icon_path_impl(icon_filename)

def _resolve_app_icon_path_for_theme(is_light_theme: bool | None) -> str | None:
    return _resolve_app_icon_path_for_theme_impl(is_light_theme)

def _resolve_app_icon_path() -> str | None:
    return _resolve_app_icon_path_impl()

def _set_windows_app_user_model_id() -> None:
    return _set_windows_app_user_model_id_impl()

def nao_retribuem(following: set[str], followers: set[str]) -> list[str]:
    return _nao_retribuem_impl(following, followers)

def eu_nao_retribuo(followers: set[str], following: set[str]) -> list[str]:
    return _eu_nao_retribuo_impl(followers, following)

def mutuos(following: set[str], followers: set[str]) -> list[str]:
    return _mutuos_impl(following, followers)

def _format_rate_limit_reset(reset_value: str | None) -> str | None:
    return _format_rate_limit_reset_impl(reset_value)

def get_token() -> str | None:
    return _get_token_impl()

def persist_github_token(token: str) -> PersistTokenResult:
    return _persist_github_token_impl(token)

def reset_github_token() -> ResetTokenResult:
    return _reset_github_token_impl()

def load_last_user() -> str:
    return _load_last_user_impl()

def save_last_user(user: str) -> None:
    return _save_last_user_impl(user)

def build_headers() -> dict[str, str]:
    return _build_headers_impl()

def build_session() -> requests.Session:
    return _build_session_impl()

def unfollow_user(session: requests.Session, username: str) -> None:
    return _unfollow_user_impl(session, username)

def _extract_connection(user_data: dict[str, Any], field_name: str, enabled: bool) -> tuple[list[str], bool, str | None]:
    return _extract_connection_impl(user_data, field_name, enabled)

def fetch_graphql_page(session: requests.Session, user: str, after_followers: str | None, after_following: str | None, include_followers: bool, include_following: bool,) -> GraphPage:
    return _fetch_graphql_page_impl(session=session, user=user, after_followers=after_followers, after_following=after_following, include_followers=include_followers, include_following=include_following,)

def fetch_relationships_graphql(session: requests.Session, user: str) -> CompareData:
    return _fetch_relationships_graphql_impl(session, user)

def _load_cache_file() -> dict[str, Any] | None:
    return _load_cache_file_impl()

def _load_non_followers_state_file() -> dict[str, Any] | None:
    return _load_non_followers_state_file_impl()

def load_previous_non_followers(user: str) -> set[str] | None:
    return _load_previous_non_followers_impl(user)

def save_non_followers_state(user: str, nao_retribuem: set[str] | list[str]) -> None:
    return _save_non_followers_state_impl(user, nao_retribuem)

def load_cached_data(user: str, include_expired: bool = False) -> CompareData | None:
    return _load_cached_data_impl(user, include_expired=include_expired)

def save_cached_data(data: CompareData) -> None:
    return _save_cached_data_impl(data)

def get_compare_data(session: requests.Session, user: str, force_refresh: bool = False) -> CompareData:
    return _get_compare_data_impl(session, user, force_refresh)

def format_rate_limit(info: RateLimitInfo | None) -> str:
    return _format_rate_limit_impl(info)

def format_cache_status(data: CompareData) -> str:
    return _format_cache_status_impl(data)

def print_cli_report(data: CompareData) -> None:
    return _print_cli_report_impl(data)

def format_exception(exc: Exception) -> str:
    return _format_exception_impl(exc)

def run_gui(initial_user: str, force_refresh: bool = False) -> int:
    return _run_gui_impl(initial_user, force_refresh)

def _qt_excepthook(previous_excepthook: Callable[[type[BaseException], BaseException, Any], None],) -> Callable[[type[BaseException], BaseException, Any], None]:
    return _qt_excepthook_impl(previous_excepthook)
