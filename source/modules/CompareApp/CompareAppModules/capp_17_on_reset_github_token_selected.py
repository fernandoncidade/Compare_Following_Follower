from __future__ import annotations
import os
from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_reset_github_token_selected(self) -> None:
    try:
        if self._file_actions_locked():
            return

        state_file, cache_file = self._resolve_database_file_paths()
        title = self._resolve_label("Resetar token GitHub", "Reset GitHub token")
        answer = QMessageBox.question(
            self,
            title,
            self._resolve_label(
                "Esta ação irá:\n"
                "1) Remover variável persistente do usuário atual;\n"
                "2) Remover variável persistente do sistema (Machine);\n"
                "3) Remover da sessão atual;\n"
                "4) Remover do Registro - Escopo Usuário;\n"
                "5) Remover do Registro - Escopo Sistema.\n\n"
                "Também irá excluir os arquivos abaixo e reiniciar o aplicativo:\n"
                "{state_file}\n"
                "{cache_file}\n\n"
                "Deseja continuar?",
                "This action will:\n"
                "1) Remove the current user's persistent variable;\n"
                "2) Remove the system persistent variable (Machine);\n"
                "3) Remove it from the current session;\n"
                "4) Remove it from the Registry - User scope;\n"
                "5) Remove it from the Registry - System scope.\n\n"
                "It will also delete the files below and restart the application:\n"
                "{state_file}\n"
                "{cache_file}\n\n"
                "Do you want to continue?",
            ).format(
                state_file=str(state_file),
                cache_file=str(cache_file),
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if answer != QMessageBox.Yes:
            return

        result = self._reset_github_token_fn()
        os.environ.pop("GITHUB_TOKEN", None)
        token_process_ok = "GITHUB_TOKEN" not in os.environ

        state_ok, state_msg = self._remove_file_for_token_reset(state_file)
        cache_ok, cache_msg = self._remove_file_for_token_reset(cache_file)
        files_ok = state_ok and cache_ok

        user_ok = bool(getattr(result, "user_scope_removed", False))
        system_ok = bool(getattr(result, "system_scope_removed", False))
        user_msg = str(getattr(result, "user_scope_message", "") or "-")
        system_msg = str(getattr(result, "system_scope_message", "") or "-")
        details_lines = [
            f"{self._resolve_label('Usuário', 'User')}: {user_msg}",
            f"{self._resolve_label('Sistema', 'System')}: {system_msg}",
            f"{self._resolve_label('Sessão atual', 'Current session')}: "
            f"{self._resolve_label('removida', 'removed') if token_process_ok else self._resolve_label('não removida', 'not removed')}",
            f"{str(state_file)}: {state_msg}",
            f"{str(cache_file)}: {cache_msg}",
        ]
        details = "\n".join(details_lines)

        full_success = user_ok and system_ok and token_process_ok and files_ok
        partial_success = any([user_ok, system_ok, token_process_ok, state_ok, cache_ok])

        if full_success:
            QMessageBox.information(
                self,
                title,
                self._resolve_label(
                    "Token, variáveis de ambiente e arquivos locais removidos com sucesso.\n"
                    "O aplicativo será reiniciado.\n\nDetalhes:\n",
                    "Token, environment variables, and local files were removed successfully.\n"
                    "The application will now restart.\n\nDetails:\n",
                )
                + details,
            )

        elif partial_success:
            QMessageBox.warning(
                self,
                title,
                self._resolve_label(
                    "A ação foi concluída parcialmente.\n"
                    "O aplicativo será reiniciado.\n\nDetalhes:\n",
                    "The action completed partially.\n"
                    "The application will now restart.\n\nDetails:\n",
                )
                + details,
            )

        else:
            QMessageBox.critical(
                self,
                title,
                self._resolve_label(
                    "Não foi possível concluir o reset.\n"
                    "O aplicativo tentará reiniciar mesmo assim.\n\nDetalhes:\n",
                    "Could not complete the reset.\n"
                    "The application will still attempt to restart.\n\nDetails:\n",
                )
                + details,
            )

        if not self._restart_application():
            QMessageBox.critical(
                self,
                title,
                self._resolve_label(
                    "Falha ao reiniciar automaticamente. Reinicie o aplicativo manualmente.",
                    "Failed to restart automatically. Restart the application manually.",
                ),
            )

    except Exception as exc:
        logger.error(f"Erro ao executar ação de resetar token GitHub: {exc}")
        QMessageBox.critical(
            self,
            self._resolve_label("Resetar token GitHub", "Reset GitHub token"),
            self._resolve_label(
                "Falha ao resetar o token automaticamente.",
                "Failed to reset the token automatically.",
            ),
        )
