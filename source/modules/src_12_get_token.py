from __future__ import annotations
import os
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _normalize_token(raw: Any) -> str | None:
    if raw is None:
        return None

    token = str(raw).strip().strip('"').strip("'")
    return token or None

def _read_windows_registry_token() -> str | None:
    if os.name != "nt":
        return None

    try:
        import winreg

    except Exception:
        return None

    key_candidates = [
        (winreg.HKEY_CURRENT_USER, r"Environment"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
    ]

    for root, sub_key in key_candidates:
        try:
            with winreg.OpenKey(root, sub_key, 0, winreg.KEY_READ) as key:
                value, _value_type = winreg.QueryValueEx(key, "GITHUB_TOKEN")
                token = _normalize_token(value)

                if token:
                    return token

        except Exception:
            continue

    return None

def get_token() -> str | None:
    try:
        token = _normalize_token(os.getenv("GITHUB_TOKEN"))

        if token:
            return token

        token = _read_windows_registry_token()

        if token:
            os.environ["GITHUB_TOKEN"] = token

        return token

    except Exception as exc:
        logger.error(f"Erro ao obter token do ambiente: {exc}")
