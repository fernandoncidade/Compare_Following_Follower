from __future__ import annotations
from pathlib import Path
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _remove_file_for_token_reset(self, path: Path) -> tuple[bool, str]:
    try:
        if path.exists():
            path.unlink()
            return True, self._resolve_label("Arquivo removido.", "File removed.")

        return True, self._resolve_label("Arquivo não encontrado (já removido).", "File not found (already removed).")

    except Exception as exc:
        logger.error(f"Erro ao remover arquivo '{path}' durante reset de token: {exc}")
        return False, str(exc)
