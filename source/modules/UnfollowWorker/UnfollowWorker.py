from __future__ import annotations
from typing import Any, Callable
from PySide6.QtCore import QObject, Signal, Slot
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class UnfollowWorker(QObject):
    success = Signal(object)
    error = Signal(object)
    finished = Signal()

    def __init__(self, usernames: list[str], build_session_fn: Callable[[], Any], get_token_fn: Callable[[], str | None], unfollow_user_fn: Callable[[Any, str], None], 
                 format_exception_fn: Callable[[Exception], str], config_error_cls: type[Exception], unfollow_result_cls: type[Any],) -> None:
        super().__init__()
        try:
            self.usernames = usernames
            self._build_session_fn = build_session_fn
            self._get_token_fn = get_token_fn
            self._unfollow_user_fn = unfollow_user_fn
            self._format_exception_fn = format_exception_fn
            self._config_error_cls = config_error_cls
            self._unfollow_result_cls = unfollow_result_cls

        except Exception as exc:
            logger.error(f"Erro ao inicializar UnfollowWorker: {exc}")

    @Slot()
    def run(self) -> None:
        try:
            session = self._build_session_fn()

            try:
                if not self._get_token_fn():
                    raise self._config_error_cls("Defina GITHUB_TOKEN para executar unfollow.")

                result = self._unfollow_result_cls(succeeded=[], failed={})

                for username in self.usernames:
                    try:
                        self._unfollow_user_fn(session, username)
                        result.succeeded.append(username)

                    except Exception as exc:
                        result.failed[username] = self._format_exception_fn(exc)

                self.success.emit(result)

            except BaseException as exc:
                if isinstance(exc, KeyboardInterrupt):
                    self.error.emit(self._config_error_cls("Execução interrompida pelo usuário."))

                else:
                    self.error.emit(exc)

            finally:
                session.close()
                self.finished.emit()

        except Exception as exc:
            logger.error(f"Erro durante execução do UnfollowWorker: {exc}")
