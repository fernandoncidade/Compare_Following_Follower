from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _read_json_dict(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else None

    except (OSError, json.JSONDecodeError):
        return None
