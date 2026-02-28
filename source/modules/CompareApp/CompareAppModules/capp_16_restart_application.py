from __future__ import annotations
import os
import subprocess
import sys
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _restart_application(self) -> bool:
    try:
        if getattr(sys, "frozen", False):
            command = [sys.executable, *sys.argv[1:]]

        else:
            command = [sys.executable, *sys.argv]

        subprocess.Popen(command, cwd=os.getcwd())

        try:
            if self._app_instance is not None:
                self._app_instance.setProperty("_compare_follow_close_requested", True)

        except Exception:
            pass

        self.close()

        if self._app_instance is not None:
            self._app_instance.quit()

        return True

    except Exception as exc:
        logger.error(f"Erro ao reiniciar aplicativo: {exc}")
        return False
