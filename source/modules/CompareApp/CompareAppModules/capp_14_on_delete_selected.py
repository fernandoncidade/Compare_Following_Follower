from __future__ import annotations
from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_delete_selected(self) -> None:
    try:
        if self._file_actions_locked():
            return

        state_file, cache_file = self._resolve_database_file_paths()
        existing_files = [path for path in (state_file, cache_file) if path.exists()]

        if not existing_files:
            QMessageBox.information(
                self,
                self._resolve_label("Excluir", "Delete"),
                self._resolve_label(
                    "Os arquivos do banco de dados não existem.\n\n"
                    "{state_file}\n"
                    "{cache_file}",
                    "Database files do not exist.\n\n"
                    "{state_file}\n"
                    "{cache_file}",
                ).format(state_file=str(state_file), cache_file=str(cache_file)),
            )
            return

        existing_paths_text = "\n".join(str(path) for path in existing_files)
        answer = QMessageBox.question(
            self,
            self._resolve_label("Excluir", "Delete"),
            self._resolve_label(
                "Deseja excluir o banco de dados?\n\n"
                "Arquivos existentes:\n"
                "{existing_paths}",
                "Do you want to delete the database?\n\n"
                "Existing files:\n"
                "{existing_paths}",
            ).format(existing_paths=existing_paths_text),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if answer != QMessageBox.Yes:
            return

        deletion_results = [self._remove_file_for_token_reset(path) for path in existing_files]
        deletion_ok = all(item[0] for item in deletion_results)

        if deletion_ok:
            self._clear_reported_data()
            QMessageBox.information(
                self,
                self._resolve_label("Sucesso", "Success"),
                self._resolve_label(
                    "Arquivos do banco de dados excluídos com sucesso!",
                    "Database files deleted successfully!",
                ),
            )
            return

        QMessageBox.critical(
            self,
            self._resolve_label("Erro", "Error"),
            self._resolve_label(
                "Falha ao excluir os arquivos do banco de dados!",
                "Failed to delete database files!",
            ),
        )

    except Exception as exc:
        logger.error(f"Erro ao executar ação de excluir banco de dados: {exc}")
        QMessageBox.critical(
            self,
            self._resolve_label("Erro", "Error"),
            self._resolve_label(
                "Falha ao excluir os arquivos do banco de dados!",
                "Failed to delete database files!",
            ),
        )
