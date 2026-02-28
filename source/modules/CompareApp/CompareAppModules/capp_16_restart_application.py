from __future__ import annotations
import os
import subprocess
import sys
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _as_existing_absolute_file_path(raw_path: str | None) -> str | None:
    if not raw_path:
        return None

    normalized = os.path.abspath(str(raw_path).strip().strip('"').strip("'"))

    if os.path.isfile(normalized):
        return normalized

    return None

def _resolve_qt_application_file_path() -> str | None:
    try:
        from PySide6.QtCore import QCoreApplication

        qt_app_path = QCoreApplication.applicationFilePath()
        return _as_existing_absolute_file_path(qt_app_path)

    except Exception:
        return None

def _resolve_restart_command() -> tuple[list[str], str | None]:
    restart_args = list(sys.argv[1:])
    argv0_path = _as_existing_absolute_file_path(sys.argv[0] if sys.argv else None)
    qt_app_path = _resolve_qt_application_file_path()
    sys_executable_path = _as_existing_absolute_file_path(sys.executable)

    for compiled_candidate in (qt_app_path, argv0_path, sys_executable_path):
        if not compiled_candidate:
            continue

        if compiled_candidate.lower().endswith(".exe") and os.path.basename(compiled_candidate).lower() != "python.exe":
            return [compiled_candidate, *restart_args], os.path.dirname(compiled_candidate)

    if getattr(sys, "frozen", False):
        if sys_executable_path:
            return [sys_executable_path, *restart_args], os.path.dirname(sys_executable_path)

        raise FileNotFoundError(
            "Executável de reinício não encontrado para app compilado "
            f"(argv0={sys.argv[0] if sys.argv else '<vazio>'}, executable={sys.executable})."
        )

    if argv0_path:
        return [sys.executable, argv0_path, *restart_args], os.getcwd()

    return [sys.executable, *restart_args], os.getcwd()

def _restart_application(self) -> bool:
    command: list[str] = []
    restart_cwd: str | None = None

    try:
        command, restart_cwd = _resolve_restart_command()

        popen_kwargs: dict[str, object] = {}

        if restart_cwd and os.path.isdir(restart_cwd):
            popen_kwargs["cwd"] = restart_cwd

        subprocess.Popen(command, **popen_kwargs)

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
        logger.error(
            "Erro ao reiniciar aplicativo: "
            f"{exc}. command={command!r}, cwd={restart_cwd!r}"
        )
        return False
