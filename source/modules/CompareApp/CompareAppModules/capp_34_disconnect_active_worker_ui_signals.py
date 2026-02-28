from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _disconnect_active_worker_ui_signals(self) -> None:
    try:
        if self._worker is None:
            return

        if self._active_worker_mode == "fetch":
            signal_slot_pairs = [
                ("success", self._on_fetch_success),
                ("error", self._on_fetch_error),
            ]

        elif self._active_worker_mode == "unfollow":
            signal_slot_pairs = [
                ("success", self._on_unfollow_success),
                ("error", self._on_unfollow_error),
            ]

        else:
            return

        for signal_name, slot in signal_slot_pairs:
            signal = getattr(self._worker, signal_name, None)

            if signal is None:
                continue

            try:
                signal.disconnect(slot)

            except (RuntimeError, TypeError):
                pass

            except Exception as exc:
                logger.error(f"Erro ao desconectar sinal '{signal_name}' durante fechamento: {exc}")

    except Exception as exc:
        logger.error(f"Erro ao desconectar sinais da thread ativa: {exc}")
