from __future__ import annotations
from source.utils.LogManager import LogManager
from source.utils.MessageBox import MessageBox
logger = LogManager.get_logger()

def _on_help_selected(self) -> None:
    try:
        actions: list[tuple[str, str]]

        if self._menu_bar_ui is not None:
            actions = [
                (self._menu_bar_ui.action_new.text(), self._menu_bar_ui.action_new.shortcut().toString()),
                (self._menu_bar_ui.action_open.text(), self._menu_bar_ui.action_open.shortcut().toString()),
                (self._menu_bar_ui.action_save.text(), self._menu_bar_ui.action_save.shortcut().toString()),
                (self._menu_bar_ui.action_delete.text(), self._menu_bar_ui.action_delete.shortcut().toString()),
                (self._menu_bar_ui.action_help.text(), self._menu_bar_ui.action_help.shortcut().toString()),
                (self._menu_bar_ui.action_close.text(), self._menu_bar_ui.action_close.shortcut().toString()),
                (self._menu_bar_ui.action_set_github_token.text(), self._menu_bar_ui.action_set_github_token.shortcut().toString(),),
                (self._menu_bar_ui.action_reset_github_token.text(), self._menu_bar_ui.action_reset_github_token.shortcut().toString(),),
                (self._menu_bar_ui.language_menu.title(), self._menu_bar_ui.language_menu.menuAction().shortcut().toString(),),
                (self._menu_bar_ui.action_manual.text(), self._menu_bar_ui.action_manual.shortcut().toString()),
                (self._menu_bar_ui.action_about.text(), self._menu_bar_ui.action_about.shortcut().toString()),
            ]

        else:
            actions = [
                (self._resolve_label("Novo", "New"), "Ctrl+N"),
                (self._resolve_label("Abrir", "Open"), "Ctrl+O"),
                (self._resolve_label("Salvar", "Save"), "Ctrl+S"),
                (self._resolve_label("Excluir", "Delete"), "Ctrl+Shift+D"),
                (self._resolve_label("Ajuda", "Help"), "F1"),
                (self._resolve_label("Fechar", "Close"), "Ctrl+Q"),
                (self._resolve_label("Definir token GitHub", "Set GitHub token"), "Ctrl+Shift+T"),
                (self._resolve_label("Resetar Token/Variáveis de Ambiente", "Reset Token/Environment Variables"), "Ctrl+Shift+R",),
                (self._resolve_label("Idioma", "Language"), "Alt+I"),
                (self._resolve_label("Manual", "Manual"), "Ctrl+Shift+M"),
                (self._resolve_label("Sobre", "About"), "Ctrl+Shift+A"),
            ]

        lines = "".join([f"<li><b>{label}</b>: <code>{shortcut or '-'}</code></li>" for label, shortcut in actions])
        help_html = (
            f"<b>{self._resolve_label('Atalhos do menu Arquivo', 'File menu shortcuts')}</b><br><br>"
            f"<ul>{lines}</ul>"
        )
        MessageBox.app_help_shortcuts(self, help_html)

    except Exception as exc:
        logger.error(f"Erro ao executar ação Ajuda: {exc}")
