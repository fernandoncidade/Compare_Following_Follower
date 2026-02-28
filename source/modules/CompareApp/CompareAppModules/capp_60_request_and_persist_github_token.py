from __future__ import annotations
import os
from PySide6.QtWidgets import QInputDialog, QLineEdit, QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _request_and_persist_github_token(self) -> bool:
    try:
        if os.name != "nt":
            QMessageBox.warning(
                self,
                self._resolve_label("Token GitHub", "GitHub token"),
                self._resolve_label(
                    "A configuração automática do token com setx está disponível apenas no Windows.",
                    "Automatic token setup with setx is available only on Windows.",
                ),
            )
            return False

        title = self._resolve_label("Token GitHub necessário", "GitHub token required")
        label = self._resolve_label(
            "Cole seu token GitHub e clique em OK.\n"
            "O aplicativo executará:\n"
            "setx GITHUB_TOKEN \"seu_token\" /M\n"
            "setx GITHUB_TOKEN \"seu_token\"\n"
            "Pode ser solicitada confirmação de administrador (UAC).",
            "Paste your GitHub token and click OK.\n"
            "The app will execute:\n"
            "setx GITHUB_TOKEN \"your_token\" /M\n"
            "setx GITHUB_TOKEN \"your_token\"\n"
            "An administrator confirmation (UAC) may be requested.",
        )

        while True:
            token, accepted = QInputDialog.getText(self, title, label, QLineEdit.Normal)

            if not accepted:
                return False

            normalized_token = token.strip().strip('"').strip("'")

            if normalized_token:
                break

            QMessageBox.warning(
                self,
                title,
                self._resolve_label(
                    "Token vazio. Informe um token válido para continuar.",
                    "Token is empty. Enter a valid token to continue.",
                ),
            )

        result = self._persist_github_token_fn(normalized_token)
        os.environ["GITHUB_TOKEN"] = normalized_token

        user_ok = bool(getattr(result, "user_scope_saved", False))
        system_ok = bool(getattr(result, "system_scope_saved", False))
        user_msg = str(getattr(result, "user_scope_message", "") or "-")
        system_msg = str(getattr(result, "system_scope_message", "") or "-")

        if user_ok and system_ok:
            QMessageBox.information(
                self,
                title,
                self._resolve_label(
                    "Token salvo com sucesso nas variáveis de usuário e de sistema.",
                    "Token saved successfully in user and system environment variables.",
                ),
            )
            return True

        details = (
            f"{self._resolve_label('Usuário', 'User')}: {user_msg}\n"
            f"{self._resolve_label('Sistema', 'System')}: {system_msg}"
        )

        if user_ok or system_ok:
            QMessageBox.warning(
                self,
                title,
                self._resolve_label(
                    "Token salvo parcialmente. A execução atual continuará usando o token informado.\n\n"
                    "Detalhes:\n",
                    "Token saved partially. The current execution will continue using the provided token.\n\n"
                    "Details:\n",
                )
                + details,
            )
            return True

        QMessageBox.critical(
            self,
            title,
            self._resolve_label(
                "Não foi possível salvar o token com setx.\n\nDetalhes:\n",
                "Could not save the token with setx.\n\nDetails:\n",
            )
            + details,
        )
        return False

    except Exception as exc:
        logger.error(f"Erro ao solicitar/persistir token GitHub: {exc}")
        QMessageBox.critical(
            self,
            self._resolve_label("Token GitHub", "GitHub token"),
            self._resolve_label(
                "Falha ao configurar o token automaticamente.",
                "Failed to configure the token automatically.",
            ),
        )
        return False
