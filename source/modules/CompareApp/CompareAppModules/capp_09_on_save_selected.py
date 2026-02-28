from __future__ import annotations
import time
from pathlib import Path
from PySide6.QtWidgets import QFileDialog, QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_save_selected(self) -> None:
    try:
        if self._file_actions_locked():
            return

        selected_path, _ = QFileDialog.getSaveFileName(
            self,
            self._resolve_label("Salvar arquivo JSON", "Save JSON file"),
            "",
            "JSON (*.json)",
        )

        if not selected_path:
            return

        target_path = self._ensure_json_path(Path(selected_path))
        saved_at_epoch = time.time()
        user = self.user_input.text().strip()
        no_longer_follow_me_values: list[str] = []

        for idx in range(self.novos_nao_seguidores_list.count()):
            item = self.novos_nao_seguidores_list.item(idx)

            if item is None:
                continue

            text = item.text()

            if isinstance(text, str):
                no_longer_follow_me_values.append(text)

        payload = {
            "atual": self._build_cache_payload_from_ui(user=user, saved_at_epoch=saved_at_epoch),
            "antigo": self._build_state_payload(
                user=user,
                saved_at_epoch=saved_at_epoch,
                values=no_longer_follow_me_values,
            ),
        }

        if self._write_json_atomic(target_path, payload):
            QMessageBox.information(
                self,
                self._resolve_label("Salvar", "Save"),
                self._resolve_label(
                    "Dados exportados com sucesso.",
                    "Data exported successfully.",
                ),
            )

        else:
            QMessageBox.warning(
                self,
                self._resolve_label("Salvar", "Save"),
                self._resolve_label(
                    "Não foi possível salvar o arquivo.",
                    "Could not save the file.",
                ),
            )

    except Exception as exc:
        logger.error(f"Erro ao executar ação Salvar: {exc}")
