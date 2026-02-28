from __future__ import annotations
from typing import Any
from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_unfollow_success(self, result: Any) -> None:
    try:
        self._set_loading(False)
        succeeded = len(result.succeeded)
        failed = len(result.failed)

        if succeeded == 0 and failed == 0:
            QMessageBox.information(self, self._tr("Unfollow"), self._tr("Nenhum perfil foi processado."))
            return

        summary = self._tr("Unfollow concluído.\nSucesso: {succeeded}\nFalhas: {failed}").format(succeeded=succeeded, failed=failed,)

        if failed:
            details = "\n".join([f"- {login}: {self._translate_runtime_message(message)}" for login, message in result.failed.items()])
            QMessageBox.warning(self, self._tr("Unfollow concluído com falhas"), f"{summary}\n\n{details}")

        else:
            QMessageBox.information(self, self._tr("Unfollow concluído"), summary)

        if succeeded > 0:
            self._start_refresh(force_network_refresh=True)

    except Exception as exc:
        logger.error(f"Erro ao processar resultado de unfollow: {exc}")
