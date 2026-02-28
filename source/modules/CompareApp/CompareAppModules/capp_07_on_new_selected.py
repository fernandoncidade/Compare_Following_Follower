from __future__ import annotations
from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_new_selected(self) -> None:
    try:
        if self._file_actions_locked():
            return

        answer = QMessageBox.question(
            self,
            self._resolve_label("Novo", "New"),
            self._resolve_label(
                "Deseja limpar os dados das abas e resetar os arquivos locais de cache/estado?",
                "Do you want to clear tab data and reset local cache/state files?",
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if answer != QMessageBox.Yes:
            return

        self._clear_reported_data()
        files_cleared = self._clear_persistent_data_files()

        if files_cleared:
            QMessageBox.information(
                self,
                self._resolve_label("Novo", "New"),
                self._resolve_label(
                    "Dados da interface e arquivos locais foram limpos.",
                    "UI data and local files were cleared.",
                ),
            )

        else:
            QMessageBox.warning(
                self,
                self._resolve_label("Novo", "New"),
                self._resolve_label(
                    "Dados da interface foram limpos, mas houve falha ao limpar arquivos locais.",
                    "UI data was cleared, but local files could not be fully cleared.",
                ),
            )

    except Exception as exc:
        logger.error(f"Erro ao executar ação Novo: {exc}")
