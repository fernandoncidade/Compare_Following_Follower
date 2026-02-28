from __future__ import annotations
import os
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _set_windows_app_user_model_id() -> None:
    try:
        if os.name != "nt":
            return

        from source.modules import source as core

        try:
            import ctypes

            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(core.WINDOWS_APP_USER_MODEL_ID)

        except Exception:
            pass

    except Exception as exc:
        logger.error(f"Erro ao definir AppUserModelID do Windows: {exc}")
