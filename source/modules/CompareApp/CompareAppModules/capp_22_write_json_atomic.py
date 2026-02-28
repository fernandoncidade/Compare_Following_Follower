from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _write_json_atomic(path: Path, payload: dict[str, Any]) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_file = path.with_suffix(path.suffix + ".tmp")
        temp_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        temp_file.replace(path)
        return True

    except OSError:
        return False
