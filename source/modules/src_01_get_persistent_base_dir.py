from __future__ import annotations
from pathlib import Path
from source.utils import obter_caminho_persistente
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _get_persistent_base_dir() -> Path:
    try:
        raw = obter_caminho_persistente()

        if isinstance(raw, str) and raw.strip():
            return Path(raw.strip()).expanduser()

    except Exception as exc:
        logger.warning(f"Erro ao obter diretório persistente: {exc}")

    return Path.cwd()
