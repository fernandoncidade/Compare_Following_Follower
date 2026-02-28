from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
from PySide6.QtGui import QAction, QActionGroup, QKeySequence
from PySide6.QtWidgets import QMenu, QMenuBar, QWidget
from source.ui.ui_01_translation_helpers import tr


@dataclass
class CompareMenuBar:
    menu_bar: QMenuBar
    file_menu: QMenu
    settings_menu: QMenu
    options_menu: QMenu
    language_menu: QMenu
    action_set_github_token: QAction
    action_reset_github_token: QAction
    action_new: QAction
    action_open: QAction
    action_save: QAction
    action_delete: QAction
    action_help: QAction
    action_close: QAction
    action_manual: QAction
    action_about: QAction
    action_pt_br: QAction
    action_en_us: QAction

    def retranslate(self) -> None:
        self.file_menu.setTitle(self._resolve_label("Arquivo", "File"))
        self.action_new.setText(self._resolve_label("Novo", "New"))
        self.action_open.setText(self._resolve_label("Abrir", "Open"))
        self.action_save.setText(self._resolve_label("Salvar", "Save"))
        self.action_delete.setText(self._resolve_label("Excluir", "Delete"))
        self.action_help.setText(self._resolve_label("Ajuda", "Help"))
        self.action_close.setText(self._resolve_label("Fechar", "Close"))
        self.settings_menu.setTitle(self._resolve_label("Configurações", "Settings"))
        self.action_set_github_token.setText(self._resolve_label("Definir token GitHub", "Set GitHub token"))
        self.action_reset_github_token.setText(self._resolve_label("Resetar Token/Variáveis de Ambiente", "Reset Token/Environment Variables"))
        self.options_menu.setTitle(self._resolve_label("Opções", "Options"))
        self.action_manual.setText(self._resolve_label("Manual", "Manual"))
        self.action_about.setText(self._resolve_label("Sobre", "About"))
        self.language_menu.setTitle(tr("Idioma"))
        self.action_pt_br.setText(tr("Português (Brasil)"))
        self.action_en_us.setText(tr("Inglês (Estados Unidos)"))

    def _resolve_label(self, pt_br: str, en_us: str) -> str:
        translated = tr(pt_br)

        if translated and translated != pt_br:
            return translated

        if self.action_en_us.isChecked():
            return en_us

        return pt_br

    def set_checked_language(self, language_code: str | None) -> None:
        if language_code == "en_US":
            self.action_en_us.setChecked(True)

        else:
            self.action_pt_br.setChecked(True)


def build_compare_menu_bar(
    parent: QWidget,
    on_language_selected: Callable[[str], None],
    on_new_selected: Callable[[], None] | None = None,
    on_open_selected: Callable[[], None] | None = None,
    on_save_selected: Callable[[], None] | None = None,
    on_delete_selected: Callable[[], None] | None = None,
    on_help_selected: Callable[[], None] | None = None,
    on_close_selected: Callable[[], None] | None = None,
    on_set_github_token_selected: Callable[[], None] | None = None,
    on_reset_github_token_selected: Callable[[], None] | None = None,
    on_manual_selected: Callable[[], None] | None = None,
    on_about_selected: Callable[[], None] | None = None,
    current_language: str | None = None,
) -> CompareMenuBar:
    menu_bar = QMenuBar(parent)

    file_menu = QMenu(menu_bar)
    menu_bar.addMenu(file_menu)

    action_new = QAction(menu_bar)
    action_new.setShortcut(QKeySequence("Ctrl+N"))
    file_menu.addAction(action_new)

    action_open = QAction(menu_bar)
    action_open.setShortcut(QKeySequence("Ctrl+O"))
    file_menu.addAction(action_open)

    action_save = QAction(menu_bar)
    action_save.setShortcut(QKeySequence("Ctrl+S"))
    file_menu.addAction(action_save)

    action_delete = QAction(menu_bar)
    action_delete.setShortcut(QKeySequence("Ctrl+Shift+D"))
    file_menu.addAction(action_delete)

    action_help = QAction(menu_bar)
    action_help.setShortcut(QKeySequence("F1"))
    file_menu.addAction(action_help)

    file_menu.addSeparator()

    action_close = QAction(menu_bar)
    action_close.setShortcut(QKeySequence("Ctrl+Q"))
    file_menu.addAction(action_close)

    settings_menu = QMenu(menu_bar)
    menu_bar.addMenu(settings_menu)

    action_set_github_token = QAction(menu_bar)
    action_set_github_token.setShortcut(QKeySequence("Ctrl+Shift+T"))
    settings_menu.addAction(action_set_github_token)

    action_reset_github_token = QAction(menu_bar)
    action_reset_github_token.setShortcut(QKeySequence("Ctrl+Shift+R"))
    settings_menu.addAction(action_reset_github_token)

    settings_menu.addSeparator()

    language_menu = QMenu(settings_menu)
    language_menu.menuAction().setShortcut(QKeySequence("Alt+I"))
    settings_menu.addMenu(language_menu)

    actions_group = QActionGroup(menu_bar)
    actions_group.setExclusive(True)

    action_pt_br = QAction(menu_bar)
    action_pt_br.setCheckable(True)
    action_pt_br.setData("pt_BR")
    actions_group.addAction(action_pt_br)
    language_menu.addAction(action_pt_br)

    action_en_us = QAction(menu_bar)
    action_en_us.setCheckable(True)
    action_en_us.setData("en_US")
    actions_group.addAction(action_en_us)
    language_menu.addAction(action_en_us)

    options_menu = QMenu(menu_bar)
    menu_bar.addMenu(options_menu)

    action_manual = QAction(menu_bar)
    action_manual.setShortcut(QKeySequence("Ctrl+Shift+M"))
    options_menu.addAction(action_manual)

    action_about = QAction(menu_bar)
    action_about.setShortcut(QKeySequence("Ctrl+Shift+A"))
    options_menu.addAction(action_about)

    def _handle_language_selected(action: QAction) -> None:
        language_code = action.data()

        if isinstance(language_code, str):
            on_language_selected(language_code)

    if on_manual_selected is not None:
        action_manual.triggered.connect(lambda _checked=False: on_manual_selected())

    if on_about_selected is not None:
        action_about.triggered.connect(lambda _checked=False: on_about_selected())

    if on_new_selected is not None:
        action_new.triggered.connect(lambda _checked=False: on_new_selected())

    if on_open_selected is not None:
        action_open.triggered.connect(lambda _checked=False: on_open_selected())

    if on_save_selected is not None:
        action_save.triggered.connect(lambda _checked=False: on_save_selected())

    if on_delete_selected is not None:
        action_delete.triggered.connect(lambda _checked=False: on_delete_selected())

    if on_help_selected is not None:
        action_help.triggered.connect(lambda _checked=False: on_help_selected())

    if on_close_selected is not None:
        action_close.triggered.connect(lambda _checked=False: on_close_selected())

    if on_set_github_token_selected is not None:
        action_set_github_token.triggered.connect(lambda _checked=False: on_set_github_token_selected())

    if on_reset_github_token_selected is not None:
        action_reset_github_token.triggered.connect(lambda _checked=False: on_reset_github_token_selected())

    actions_group.triggered.connect(_handle_language_selected)

    menu_ui = CompareMenuBar(
        menu_bar=menu_bar,
        file_menu=file_menu,
        settings_menu=settings_menu,
        language_menu=language_menu,
        action_set_github_token=action_set_github_token,
        action_reset_github_token=action_reset_github_token,
        action_new=action_new,
        action_open=action_open,
        action_save=action_save,
        action_delete=action_delete,
        action_help=action_help,
        action_close=action_close,
        action_manual=action_manual,
        action_about=action_about,
        action_pt_br=action_pt_br,
        action_en_us=action_en_us,
        options_menu=options_menu,
    )
    menu_ui.set_checked_language(current_language)
    menu_ui.retranslate()
    return menu_ui
