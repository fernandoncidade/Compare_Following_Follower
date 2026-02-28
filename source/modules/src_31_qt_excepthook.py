from __future__ import annotations
from typing import Any, Callable
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _qt_excepthook(previous_excepthook: Callable[[type[BaseException], BaseException, Any], None],) -> Callable[[type[BaseException], BaseException, Any], None]:
    try:
        def _handler(exc_type: type[BaseException], exc_value: BaseException, traceback: Any) -> None:
            if issubclass(exc_type, KeyboardInterrupt):
                return

            previous_excepthook(exc_type, exc_value, traceback)

        return _handler

    except Exception as exc:
        logger.error(f"Erro ao criar excepthook para Qt: {exc}")
