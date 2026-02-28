from __future__ import annotations
import os
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _read_windows_light_theme_flag() -> bool | None:
    if os.name != "nt":
        return None

    try:
        import winreg
        personalize_key = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, personalize_key) as key:
            try:
                apps_use_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return bool(int(apps_use_light_theme))

            except OSError:
                system_use_light_theme, _ = winreg.QueryValueEx(key, "SystemUsesLightTheme")
                return bool(int(system_use_light_theme))

    except Exception:
        logger.warning("Erro ao ler tema claro do Windows")
        return None
