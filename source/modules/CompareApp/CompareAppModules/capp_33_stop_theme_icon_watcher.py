from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _stop_theme_icon_watcher(self) -> None:
    try:
        if self._theme_icon_timer is None:
            return

        try:
            self._theme_icon_timer.stop()

        except RuntimeError:
            pass

        except Exception as exc:
            logger.error(f"Erro ao interromper timer de tema: {exc}")

        self._theme_icon_timer = None

    except Exception as exc:
        logger.error(f"Erro ao finalizar verificador de tema: {exc}")
