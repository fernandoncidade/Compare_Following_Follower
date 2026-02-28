from __future__ import annotations
from typing import Any, Callable
from PySide6.QtCore import QObject, Signal, Slot
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class FetchWorker(QObject):
    success = Signal(object)
    error = Signal(object)
    finished = Signal()

    def __init__(self, user: str, force_network_refresh: bool, build_session_fn: Callable[[], Any], get_compare_data_fn: Callable[..., Any], config_error_cls: type[Exception],) -> None:
        super().__init__()
        try:
            self.user = user
            self.force_network_refresh = force_network_refresh
            self._build_session_fn = build_session_fn
            self._get_compare_data_fn = get_compare_data_fn
            self._config_error_cls = config_error_cls

        except Exception as exc:
            logger.error(f"Erro ao inicializar FetchWorker: {exc}")

    @Slot()
    def run(self) -> None:
        session = None

        try:
            session = self._build_session_fn()

            if session is None:
                raise self._config_error_cls("Falha ao criar sessão de rede.")

            data = self._get_compare_data_fn(session, self.user, force_refresh=self.force_network_refresh)

            if data is None:
                raise self._config_error_cls("Não foi possível carregar os dados da comparação.")

            self.success.emit(data)

        except BaseException as exc:
            if isinstance(exc, KeyboardInterrupt):
                self.error.emit(self._config_error_cls("Execução interrompida pelo usuário."))

            elif isinstance(exc, Exception):
                self.error.emit(exc)

            else:
                self.error.emit(self._config_error_cls(str(exc)))

        finally:
            if session is not None:
                try:
                    session.close()

                except Exception as close_exc:
                    logger.error(f"Erro ao fechar sessão de atualização: {close_exc}")

            self.finished.emit()
