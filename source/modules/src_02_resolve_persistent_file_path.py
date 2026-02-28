from __future__ import annotations
import os
from pathlib import Path
from .src_01_get_persistent_base_dir import _get_persistent_base_dir
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _resolve_persistent_file_path(env_var: str, default_filename: str) -> Path:
    try:
        raw_value = os.getenv(env_var)
        base_dir = _get_persistent_base_dir()

        if raw_value:
            cleaned_value = raw_value.strip().strip('"').strip("'")

            if cleaned_value:
                candidate = Path(cleaned_value).expanduser()

                if not candidate.is_absolute():
                    candidate = base_dir / candidate

                return candidate

        return base_dir / default_filename

    except Exception as exc:
        logger.error(f"Erro ao resolver caminho persistente para {env_var}: {exc}")
