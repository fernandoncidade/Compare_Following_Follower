from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _shutdown_active_worker(self, wait_timeout_ms: int = 15000) -> None:
    try:
        thread = self._thread

        if thread is None:
            self._worker = None
            return

        try:
            is_running = thread.isRunning()

        except RuntimeError:
            is_running = False

        if is_running:
            try:
                thread.requestInterruption()

            except Exception:
                pass

            try:
                thread.quit()

            except RuntimeError:
                pass

            except Exception as exc:
                logger.error(f"Erro ao solicitar encerramento da thread: {exc}")

            try:
                finished = thread.wait(max(0, int(wait_timeout_ms)))

            except RuntimeError:
                finished = True

            except Exception as exc:
                logger.error(f"Erro ao aguardar finalização da thread: {exc}")
                finished = False

            if not finished:
                logger.error("Thread de trabalho não finalizou a tempo; forçando encerramento.")

                try:
                    thread.terminate()

                except RuntimeError:
                    pass

                except Exception as exc:
                    logger.error(f"Erro ao forçar encerramento da thread: {exc}")

                try:
                    thread.wait(2000)

                except RuntimeError:
                    pass

                except Exception as exc:
                    logger.error(f"Erro ao aguardar thread após encerramento forçado: {exc}")

        self._worker = None
        self._thread = None
        self._active_worker_mode = None

    except Exception as exc:
        logger.error(f"Erro ao finalizar thread ativa no fechamento da janela: {exc}")
