from __future__ import annotations
from pathlib import Path
from PySide6.QtWidgets import QFileDialog, QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_open_selected(self) -> None:
    try:
        if self._file_actions_locked():
            return

        selected_path, _ = QFileDialog.getOpenFileName(
            self,
            self._resolve_label("Abrir arquivo JSON", "Open JSON file"),
            "",
            "JSON (*.json)",
        )

        if not selected_path:
            return

        payload = self._read_json_dict(Path(selected_path))

        if payload is None:
            QMessageBox.warning(
                self,
                self._resolve_label("Abrir", "Open"),
                self._resolve_label(
                    "Não foi possível ler o arquivo JSON selecionado.",
                    "Could not read the selected JSON file.",
                ),
            )
            return

        cache_payload, state_payload = self._parse_import_payload(payload)

        if cache_payload is None and state_payload is None:
            QMessageBox.warning(
                self,
                self._resolve_label("Abrir", "Open"),
                self._resolve_label(
                    "Formato inválido. Use JSON no padrão de cache, estado ou pacote contendo ambos.",
                    "Invalid format. Use JSON in cache, state, or combined package format.",
                ),
            )
            return

        if (
            cache_payload is not None
            and state_payload is not None
            and cache_payload.get("user") != state_payload.get("user")
        ):
            QMessageBox.warning(
                self,
                self._resolve_label("Abrir", "Open"),
                self._resolve_label(
                    "Arquivo inválido: 'cache.user' e 'state.user' precisam ser iguais.",
                    "Invalid file: 'cache.user' and 'state.user' must match.",
                ),
            )
            return

        from source.modules import source as core

        persisted_ok = True

        if state_payload is not None:
            persisted_ok = self._write_json_atomic(core.NON_FOLLOWERS_STATE_FILE, state_payload) and persisted_ok

        if cache_payload is not None:
            persisted_ok = self._write_json_atomic(core.CACHE_FILE, cache_payload) and persisted_ok
            self.user_input.setText(cache_payload["user"])
            self._on_fetch_success(self._create_compare_data_from_cache_payload(cache_payload))

        elif state_payload is not None:
            self.user_input.setText(state_payload["user"])
            self._apply_state_payload_only(state_payload)

        if persisted_ok:
            QMessageBox.information(
                self,
                self._resolve_label("Abrir", "Open"),
                self._resolve_label(
                    "Arquivo carregado com sucesso.",
                    "File loaded successfully.",
                ),
            )

        else:
            QMessageBox.warning(
                self,
                self._resolve_label("Abrir", "Open"),
                self._resolve_label(
                    "Arquivo carregado na interface, mas houve falha ao persistir os dados locais.",
                    "File loaded in the UI, but local persistence failed.",
                ),
            )

    except Exception as exc:
        logger.error(f"Erro ao executar ação Abrir: {exc}")
