from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

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
