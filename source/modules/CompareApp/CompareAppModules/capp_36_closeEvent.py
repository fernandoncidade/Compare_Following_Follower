from __future__ import annotations
from PySide6.QtWidgets import QWidget
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def closeEvent(self, event) -> None:
    try:
        try:
            if self._app_instance is not None:
                self._app_instance.setProperty("_compare_follow_close_requested", True)

        except Exception:
            pass

        self._stop_theme_icon_watcher()
        self._disconnect_active_worker_ui_signals()
        self._shutdown_active_worker()

        for attr_name in ("_manual_dialog", "_sobre_dialog"):
            dialog = getattr(self, attr_name, None)

            if dialog is None:
                continue

            try:
                dialog.close()

            except RuntimeError:
                pass

            except Exception as exc:
                logger.error(f"Erro ao fechar diálogo '{attr_name}': {exc}")

            finally:
                try:
                    setattr(self, attr_name, None)

                except Exception:
                    pass

    except Exception as exc:
        logger.error(f"Erro ao processar fechamento da janela principal: {exc}")

    QWidget.closeEvent(self, event)
