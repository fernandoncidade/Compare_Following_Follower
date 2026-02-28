from __future__ import annotations
from pathlib import Path
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _ensure_json_path(path: Path) -> Path:
    try:
        if path.suffix.lower() == ".json":
            return path

        return path.with_suffix(".json")

    except Exception:
        return path
