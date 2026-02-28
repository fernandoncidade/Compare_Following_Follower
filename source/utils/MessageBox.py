from __future__ import annotations
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QWidget
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class MessageBox:
    StandardButton = QMessageBox.StandardButton
    ButtonRole = QMessageBox.ButtonRole
    Icon = QMessageBox.Icon

    @staticmethod
    def create(parent=None):
        return QMessageBox(MessageBox._resolve_parent_widget(parent))

    @staticmethod
    def _is_qt_alive(obj) -> bool:
        if obj is None:
            return False

        try:
            from shiboken6 import isValid
            return bool(isValid(obj))

        except Exception:
            return True

    @staticmethod
    def _resolve_parent_widget(parent):
        if not MessageBox._is_qt_alive(parent):
            return None

        if isinstance(parent, QWidget):
            return parent

        try:
            scene = parent.scene() if hasattr(parent, "scene") else None

            if scene is not None and MessageBox._is_qt_alive(scene):
                views = scene.views()

                if views:
                    view = views[0]

                    if MessageBox._is_qt_alive(view):
                        return view

        except Exception:
            pass

        try:
            maybe_parent = parent.parentWidget() if hasattr(parent, "parentWidget") else None

            if isinstance(maybe_parent, QWidget) and MessageBox._is_qt_alive(maybe_parent):
                return maybe_parent

        except Exception:
            pass

        return None

    @staticmethod
    def tr(key: str) -> str:
        txt = QCoreApplication.translate("App", key)
        return txt if txt and txt != key else key

    @staticmethod
    def title_error() -> str:
        return MessageBox.tr("Erro")

    @staticmethod
    def title_warning() -> str:
        return MessageBox.tr("Aviso")

    @staticmethod
    def title_success() -> str:
        return MessageBox.tr("Sucesso")

    @staticmethod
    def title_saved() -> str:
        return MessageBox.tr("Salvo")

    @staticmethod
    def text_file_not_found() -> str:
        return MessageBox.tr("Arquivo não encontrado.")

    @staticmethod
    def warning_file_not_found(parent):
        return MessageBox.warning_error(parent, MessageBox.text_file_not_found())

    @staticmethod
    def warning_error(parent, text: str):
        return MessageBox.warning(parent, MessageBox.title_error(), text)

    @staticmethod
    def critical_error(parent, text: str):
        return MessageBox.critical(parent, MessageBox.title_error(), text)

    @staticmethod
    def critical_exception(parent, exc: Exception, prefix: str | None = None):
        label = prefix or MessageBox.title_error()
        return MessageBox.critical(parent, MessageBox.title_error(), f"{label}: {exc}")

    @staticmethod
    def critical_error_exception(parent, exc: Exception, tr_func=None):
        try:
            _tr = tr_func if callable(tr_func) else MessageBox.tr
            error_label = _tr("Erro")

            if not error_label:
                error_label = "Erro"

            return MessageBox.critical(parent, error_label, f"{error_label}: {exc}")

        except Exception:
            return MessageBox.critical_exception(parent, exc)

    @staticmethod
    def info_success(parent, text: str):
        return MessageBox.information(parent, MessageBox.title_success(), text)

    @staticmethod
    def info_saved(parent, text: str):
        return MessageBox.information(parent, MessageBox.title_saved(), text)

    @staticmethod
    def app_language_changed_success(parent):
        return MessageBox.information(
            parent,
            MessageBox.tr("✅ Idioma Alterado"),
            MessageBox.tr("O idioma foi alterado com sucesso!"),
        )

    @staticmethod
    def app_language_change_error(parent):
        return MessageBox.warning(
            parent,
            MessageBox.tr("⚠️ Erro"),
            MessageBox.tr("Não foi possível alterar o idioma."),
        )

    @staticmethod
    def app_help_shortcuts(parent, help_html: str):
        return MessageBox.information(
            parent,
            MessageBox.tr("Ajuda - Atalhos"),
            help_html,
        )

    @staticmethod
    def app_lazy_load_module_error(parent, erro: str):
        titulo = MessageBox.tr("Erro ao Carregar Módulo")
        msg_topo = MessageBox.tr("Ocorreu um erro ao carregar o módulo:")
        msg_rodape = MessageBox.tr("Verifique se todas as dependências estão instaladas.")
        return MessageBox.critical(parent, titulo, f"{msg_topo}\n\n{erro}\n\n{msg_rodape}")

    @staticmethod
    def trial_expired(parent, paid_version_url: str, icon_path: str | None = None):
        try:
            msg = MessageBox.create(parent)

            if icon_path:
                msg.setWindowIcon(QIcon(icon_path))

            msg.setIcon(MessageBox.Icon.Critical)
            msg.setWindowTitle(MessageBox.tr("trial_expired_title"))
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setText(
                f"{MessageBox.tr('trial_expired_message')}<br>"
                f"{MessageBox.tr('trial_buy_message')}<br><br>"
                f"{MessageBox.tr('trial_uninstall_message')}<br><br>"
                f'<a href="{paid_version_url}">{MessageBox.tr("trial_paid_link")}</a>'
            )
            msg.setStandardButtons(MessageBox.StandardButton.Ok)
            return msg.exec()

        except Exception as exc:
            logger.error(f"Erro ao exibir diálogo de trial expirado: {exc}", exc_info=True)
            return MessageBox.critical_error(parent, MessageBox.tr("trial_expired_message"))

    @staticmethod
    def _single_action(parent, title: str, text: str, icon, action_text: str):
        try:
            msg = MessageBox.create(parent)
            msg.setIcon(icon)
            msg.setWindowTitle(title)
            msg.setText(text)
            msg.addButton(action_text, MessageBox.ButtonRole.AcceptRole)
            msg.exec()

        except Exception as exc:
            logger.error(f"Erro ao exibir diálogo customizado: {exc}", exc_info=True)

    @staticmethod
    def _confirm(parent, title: str, text: str, ok_text: str | None = None, cancel_text: str | None = None) -> bool:
        try:
            msg = MessageBox.create(parent)
            msg.setIcon(MessageBox.Icon.Question)
            msg.setWindowTitle(title)
            msg.setText(text)
            ok_label = ok_text or MessageBox.tr("Ok")
            cancel_label = cancel_text or MessageBox.tr("Cancelar")
            btn_ok = msg.addButton(ok_label, MessageBox.ButtonRole.AcceptRole)
            msg.addButton(cancel_label, MessageBox.ButtonRole.RejectRole)
            msg.exec()
            return msg.clickedButton() == btn_ok

        except Exception as exc:
            logger.error(f"Erro ao exibir confirmação customizada: {exc}", exc_info=True)
            return False

    @staticmethod
    def feynman_delete_success(parent):
        MessageBox._single_action(
            parent,
            MessageBox.title_success(),
            MessageBox.tr("Conceito excluído com sucesso!"),
            MessageBox.Icon.Information,
            MessageBox.tr("Ok"),
        )

    @staticmethod
    def feynman_delete_error(parent):
        MessageBox._single_action(
            parent,
            MessageBox.title_error(),
            MessageBox.tr("Erro ao excluir conceito!"),
            MessageBox.Icon.Critical,
            MessageBox.tr("Fechar"),
        )

    @staticmethod
    def feynman_confirm_delete_concepts(parent, titulos: list[str]) -> bool:
        nomes = [t for t in (titulos or []) if t]

        if len(nomes) <= 1:
            alvo = nomes[0] if nomes else ""
            texto = MessageBox.tr("Deseja realmente deletar o conceito '{titulo}'?").format(titulo=alvo)

        else:
            texto = MessageBox.tr("Deseja realmente deletar os {n} conceitos selecionados?").format(n=len(nomes))

        return MessageBox._confirm(
            parent,
            MessageBox.tr("Confirmar Exclusão"),
            texto,
            ok_text=MessageBox.tr("Yes"),
            cancel_text=MessageBox.tr("No"),
        )

    @staticmethod
    def feynman_warn_missing_title(parent):
        return MessageBox.warning(
            parent,
            MessageBox.tr("Atenção"),
            MessageBox.tr("Por favor, digite o título do conceito!"),
        )

    @staticmethod
    def feynman_save_success(parent, titulo: str):
        return MessageBox.information(
            parent,
            MessageBox.tr("✅ Salvo"),
            MessageBox.tr("Conceito '{titulo}' salvo com sucesso!").format(titulo=titulo),
        )

    @staticmethod
    def feynman_unlinked_file_removed(parent):
        return MessageBox.information(
            parent,
            MessageBox.tr("Arquivo desvinculado"),
            MessageBox.tr("O arquivo vinculado foi removido do conceito."),
        )

    @staticmethod
    def feynman_linked_file_not_found(parent, caminho: str):
        return MessageBox.warning(
            parent,
            MessageBox.tr("Arquivo não encontrado"),
            MessageBox.tr("O arquivo vinculado não foi encontrado:\n{caminho}").format(caminho=caminho),
        )

    @staticmethod
    def feynman_linked_file_open_error(parent):
        return MessageBox.warning(
            parent,
            MessageBox.title_error(),
            MessageBox.tr("Não foi possível abrir o arquivo vinculado."),
        )

    @staticmethod
    def mapa_clear_success(parent):
        MessageBox._single_action(
            parent,
            MessageBox.title_success(),
            MessageBox.tr("Mapa Mental limpo com sucesso!"),
            MessageBox.Icon.Information,
            MessageBox.tr("Ok"),
        )

    @staticmethod
    def mapa_clear_error(parent):
        MessageBox._single_action(
            parent,
            MessageBox.title_error(),
            MessageBox.tr("Erro ao limpar Mapa Mental!"),
            MessageBox.Icon.Critical,
            MessageBox.tr("Fechar"),
        )

    @staticmethod
    def mapa_confirm_clear(parent) -> bool:
        return MessageBox._confirm(
            parent,
            MessageBox.title_warning(),
            MessageBox.tr("Deseja realmente limpar o Mapa Mental?"),
            ok_text=MessageBox.tr("Sim"),
            cancel_text=MessageBox.tr("Não"),
        )

    @staticmethod
    def mapa_confirm_delete_nodes(parent, nomes_nos: list[str]) -> bool:
        nomes = [n for n in (nomes_nos or []) if n]

        if len(nomes) <= 1:
            alvo = nomes[0] if nomes else ""
            texto = MessageBox.tr("Deseja realmente excluir '{no_conexao}'?").format(no_conexao=alvo)

        else:
            texto = MessageBox.tr("Deseja realmente excluir os '{no_conexao}' nós selecionados?").format(
                no_conexao=", ".join(nomes)
            )

        return MessageBox._confirm(
            parent,
            MessageBox.tr("Confirmar Exclusão"),
            texto,
            ok_text=MessageBox.tr("Ok"),
            cancel_text=MessageBox.tr("Cancelar"),
        )

    @staticmethod
    def mapa_delete_nodes_success(parent):
        MessageBox._single_action(
            parent,
            MessageBox.title_success(),
            MessageBox.tr("Nó(s) excluído(s) com sucesso!"),
            MessageBox.Icon.Information,
            MessageBox.tr("Ok"),
        )

    @staticmethod
    def mapa_delete_nodes_error(parent):
        MessageBox._single_action(
            parent,
            MessageBox.title_error(),
            MessageBox.tr("Erro ao excluir Nó(s)!"),
            MessageBox.Icon.Critical,
            MessageBox.tr("Fechar"),
        )

    @staticmethod
    def mapa_ai_alpha_notice(parent, notice_text: str):
        return MessageBox.warning(
            parent,
            MessageBox.tr("Lúmen"),
            notice_text,
            MessageBox.StandardButton.Ok,
        )

    @staticmethod
    def mapa_confirm_link_file_new_node(parent) -> bool:
        resp = MessageBox.question(
            parent,
            MessageBox.tr("Vincular arquivo"),
            MessageBox.tr("Deseja vincular este arquivo ao nó que será criado?"),
            MessageBox.StandardButton.Yes | MessageBox.StandardButton.No,
            MessageBox.StandardButton.Yes,
        )
        return resp == MessageBox.StandardButton.Yes

    @staticmethod
    def mapa_feynman_warn_missing_title(parent):
        return MessageBox.warning(
            parent,
            MessageBox.tr("Atenção"),
            MessageBox.tr("Por favor, digite o título do conceito!"),
        )

    @staticmethod
    def mapa_feynman_warn_missing_notes(parent):
        return MessageBox.warning(
            parent,
            MessageBox.tr("Atenção"),
            MessageBox.tr("Por favor, escreva suas notas antes de integrar ao Método Feynman!"),
        )

    @staticmethod
    def mapa_feynman_integrated_success(parent, titulo: str):
        return MessageBox.information(
            parent,
            MessageBox.tr("✅ Integrado"),
            MessageBox.tr("Conceito '{titulo}' integrado ao Método Feynman com sucesso!").format(titulo=titulo),
        )

    @staticmethod
    def mapa_feynman_integrate_error(parent, erro: str):
        return MessageBox.critical(
            parent,
            MessageBox.title_error(),
            MessageBox.tr("Erro ao integrar ao Método Feynman: {erro}").format(erro=erro),
        )

    @staticmethod
    def leitor_pause_requires_edge_tts(parent):
        return MessageBox.information(
            parent,
            MessageBox.tr("Pausar"),
            MessageBox.tr("Pausar/continuar está disponível apenas com as vozes neurais (Edge TTS)."),
        )

    @staticmethod
    def leitor_tts_error(parent, erro):
        return MessageBox.warning(
            parent,
            MessageBox.tr("TTS"),
            MessageBox.tr("Erro no TTS: {erro}").format(erro=erro),
        )

    @staticmethod
    def leitor_focus_ruler_activated(parent):
        return MessageBox.information(
            parent,
            MessageBox.tr("Régua de Foco Ativada"),
            MessageBox.tr(
                "✅ Régua de foco ativada!\n\n"
                "📌 Como usar:\n"
                "• Clique e arraste no centro para mover\n"
                "• Clique nas bordas/cantos para redimensionar\n"
                "• Use setas ↑↓←→ para ajuste fino\n"
                "• Pressione ESC para fechar"
            ),
        )

    @staticmethod
    def leitor_confirm_clear_panel(parent) -> bool:
        resp = MessageBox.warning(
            parent,
            MessageBox.tr("Limpar conteúdo"),
            MessageBox.tr('Esta ação irá limpar o conteúdo das abas "Texto" e "PDF".\n\nDeseja continuar?'),
            MessageBox.StandardButton.Yes | MessageBox.StandardButton.No,
            MessageBox.StandardButton.No,
        )
        return resp == MessageBox.StandardButton.Yes

    @staticmethod
    def leitor_confirm_create_new_text(parent) -> bool:
        return MessageBox._confirm(
            parent,
            MessageBox.tr("Criar Texto"),
            MessageBox.tr("Deseja criar um novo texto? O conteúdo atual será descartado."),
            ok_text=MessageBox.tr("Yes"),
            cancel_text=MessageBox.tr("No"),
        )

    @staticmethod
    def leitor_saved_txt(parent):
        return MessageBox.info_saved(parent, MessageBox.tr("Arquivo TXT salvo com sucesso."))

    @staticmethod
    def leitor_saved_docx(parent):
        return MessageBox.info_saved(parent, MessageBox.tr("Arquivo DOCX salvo com sucesso."))

    @staticmethod
    def leitor_saved_pdf(parent):
        return MessageBox.info_saved(parent, MessageBox.tr("Arquivo PDF salvo com sucesso."))

    @staticmethod
    def leitor_saved_txt_fallback(parent):
        return MessageBox.info_saved(parent, MessageBox.tr("Arquivo salvo (tratado como TXT)."))

    @staticmethod
    def leitor_warn_docx_dependency(parent):
        return MessageBox.warning(
            parent,
            MessageBox.title_warning(),
            MessageBox.tr("Não foi possível salvar DOCX. Verifique se 'python-docx' está instalado."),
        )

    @staticmethod
    def leitor_warn_pdf_dependencies(parent):
        return MessageBox.warning_error(
            parent,
            MessageBox.tr("Não foi possível gerar PDF. Instale 'reportlab' ou 'docx2pdf'."),
        )

    @staticmethod
    def leitor_warn_save_failed(parent):
        return MessageBox.warning_error(parent, MessageBox.tr("Não foi possível salvar o arquivo."))

    @staticmethod
    def eisen_warn_empty_task(parent):
        return MessageBox.warning_error(parent, MessageBox.tr("A tarefa não pode estar vazia."))

    @staticmethod
    def eisen_confirm_attach_file(parent) -> bool:
        resp = MessageBox.question(
            parent,
            MessageBox.tr("Vincular Arquivo"),
            MessageBox.tr("Deseja vincular o arquivo a esta tarefa?"),
            MessageBox.StandardButton.Yes | MessageBox.StandardButton.No,
            MessageBox.StandardButton.No,
        )
        return resp == MessageBox.StandardButton.Yes

    @staticmethod
    def eisen_confirm_remove_single_task(parent, item_text: str) -> bool:
        resp = MessageBox.question(
            parent,
            MessageBox.tr("Remover Tarefa"),
            MessageBox.tr("Deseja remover a tarefa '{item}'?").format(item=item_text),
            MessageBox.StandardButton.Yes | MessageBox.StandardButton.No,
            MessageBox.StandardButton.No,
        )
        return resp == MessageBox.StandardButton.Yes

    @staticmethod
    def eisen_confirm_remove_multiple_tasks(parent, total: int) -> bool:
        resp = MessageBox.question(
            parent,
            MessageBox.tr("Remover Tarefa"),
            MessageBox.tr("Deseja remover {n} tarefas selecionadas?").format(n=total),
            MessageBox.StandardButton.Yes | MessageBox.StandardButton.No,
            MessageBox.StandardButton.No,
        )
        return resp == MessageBox.StandardButton.Yes

    @staticmethod
    def eisen_remove_task_success(parent):
        return MessageBox.info_success(parent, MessageBox.tr("Tarefa removida com sucesso!"))

    @staticmethod
    def eisen_remove_tasks_success(parent, total: int):
        if int(total or 0) == 1:
            msg = MessageBox.tr("1 tarefa removida com sucesso!")

        else:
            msg = MessageBox.tr("{n} tarefas removidas com sucesso!").format(n=int(total or 0))

        return MessageBox.info_success(parent, msg)

    @staticmethod
    def eisen_confirm_remove_tasks_by_day(parent) -> bool:
        resp = MessageBox.question(
            parent,
            MessageBox.tr("Remover Tarefas"),
            MessageBox.tr("Deseja remover todas as tarefas do dia selecionado?"),
            MessageBox.StandardButton.Yes | MessageBox.StandardButton.No,
            MessageBox.StandardButton.No,
        )
        return resp == MessageBox.StandardButton.Yes

    @staticmethod
    def eisen_confirm_remove_tasks_by_month(parent) -> bool:
        resp = MessageBox.question(
            parent,
            MessageBox.tr("Remover Tarefas"),
            MessageBox.tr("Deseja remover todas as tarefas do mês selecionado?"),
            MessageBox.StandardButton.Yes | MessageBox.StandardButton.No,
            MessageBox.StandardButton.No,
        )
        return resp == MessageBox.StandardButton.Yes

    @staticmethod
    def eisen_share_pomodoro_success(parent, enviados: int):
        if enviados == 1:
            msg = MessageBox.tr("Tarefa enviada com sucesso para ⏱️ Gestão de Tempo - Pomodoro!⏱️")

        else:
            msg = MessageBox.tr("{n} tarefas enviadas com sucesso para ⏱️ Gestão de Tempo - Pomodoro!⏱️").replace("{n}", str(enviados))

        return MessageBox.info_success(parent, msg)

    @staticmethod
    def eisen_new_session_started(parent):
        return MessageBox.information(parent, MessageBox.tr("Novo"), MessageBox.tr("Nova sessão iniciada."))

    @staticmethod
    def eisen_all_data_removed(parent):
        return MessageBox.information(parent, MessageBox.tr("Limpar"), MessageBox.tr("Todos os dados foram removidos."))

    @staticmethod
    def eisen_open_dependency_missing_openpyxl(parent):
        return MessageBox.critical_error(parent, MessageBox.tr("openpyxl não está disponível."))

    @staticmethod
    def eisen_open_dependency_missing_pypdf2(parent):
        return MessageBox.critical_error(parent, MessageBox.tr("PyPDF2 não está disponível para ler PDF."))

    @staticmethod
    def eisen_open_import_success(parent):
        return MessageBox.information(parent, MessageBox.tr("Abrir"), MessageBox.tr("Arquivo importado com sucesso."))

    @staticmethod
    def eisen_open_pdf_import_success(parent):
        return MessageBox.information(parent, MessageBox.tr("Abrir"), MessageBox.tr("PDF importado com sucesso."))

    @staticmethod
    def eisen_open_pdf_incompatible(parent):
        return MessageBox.warning(parent, MessageBox.tr("Abrir"), MessageBox.tr("PDF não está no formato compatível."))

    @staticmethod
    def eisen_open_unsupported_format(parent):
        return MessageBox.warning(parent, MessageBox.tr("Abrir"), MessageBox.tr("Formato de arquivo não suportado."))

    @staticmethod
    def eisen_save_dependency_missing_openpyxl(parent):
        return MessageBox.critical_error(parent, MessageBox.tr("openpyxl não está disponível para salvar XLSX."))

    @staticmethod
    def eisen_save_dependency_missing_reportlab(parent):
        return MessageBox.critical_error(parent, MessageBox.tr("reportlab não está disponível para salvar PDF."))

    @staticmethod
    def eisen_save_success(parent):
        return MessageBox.information(parent, MessageBox.tr("Salvar"), MessageBox.tr("Arquivo salvo com sucesso."))

    @staticmethod
    def eisen_save_pdf_success(parent):
        return MessageBox.information(parent, MessageBox.tr("Salvar"), MessageBox.tr("PDF salvo com sucesso."))

    @staticmethod
    def eisen_save_unsupported_extension(parent):
        return MessageBox.warning(parent, MessageBox.tr("Salvar"), MessageBox.tr("Extensão não suportada."))

    @staticmethod
    def tempo_confirm_attach_file(parent, nome_arquivo: str):
        return MessageBox.question(
            parent,
            MessageBox.tr("Vincular arquivo"),
            MessageBox.tr("Deseja vincular o arquivo a esta tarefa?\n\n{nome}").format(nome=nome_arquivo),
            MessageBox.StandardButton.Yes | MessageBox.StandardButton.No,
            MessageBox.StandardButton.Yes,
        )

    @staticmethod
    def tempo_confirm_delete_task(parent, titulo: str) -> bool:
        resp = MessageBox.question(
            parent,
            MessageBox.tr("Confirmar Exclusão"),
            MessageBox.tr("Deseja remover a tarefa selecionada?\n\n{titulo}").format(titulo=titulo),
            MessageBox.StandardButton.Yes | MessageBox.StandardButton.No,
            MessageBox.StandardButton.No,
        )
        return resp == MessageBox.StandardButton.Yes

    @staticmethod
    def tempo_confirm_delete_tasks(parent, total: int) -> bool:
        resp = MessageBox.question(
            parent,
            MessageBox.tr("Confirmar Exclusão"),
            MessageBox.tr("Deseja remover {n} tarefa(s) selecionada(s)?").format(n=total),
            MessageBox.StandardButton.Yes | MessageBox.StandardButton.No,
            MessageBox.StandardButton.No,
        )
        return resp == MessageBox.StandardButton.Yes

    @staticmethod
    def tempo_delete_task_success(parent):
        return MessageBox.info_success(parent, MessageBox.tr("Tarefa removida com sucesso!"))

    @staticmethod
    def tempo_delete_tasks_success(parent, total_removidas: int):
        return MessageBox.info_success(
            parent,
            MessageBox.tr("{n} tarefa(s) removida(s) com sucesso!").format(n=total_removidas),
        )

    @staticmethod
    def tempo_delete_task_failure(parent):
        return MessageBox.warning(
            parent,
            MessageBox.tr("Falha"),
            MessageBox.tr("Não foi possível remover a tarefa selecionada."),
        )

    @staticmethod
    def tempo_delete_tasks_failure(parent):
        return MessageBox.warning(
            parent,
            MessageBox.tr("Falha"),
            MessageBox.tr("Não foi possível remover as tarefas selecionadas."),
        )

    @staticmethod
    def tempo_delete_task_error(parent):
        return MessageBox.warning(
            parent,
            MessageBox.tr("Falha"),
            MessageBox.tr("Ocorreu um erro ao remover a tarefa."),
        )

    @staticmethod
    def tempo_delete_tasks_error(parent):
        return MessageBox.warning(
            parent,
            MessageBox.tr("Falha"),
            MessageBox.tr("Ocorreu um erro ao remover as tarefas."),
        )

    @staticmethod
    def tempo_no_tasks_in_column(parent):
        return MessageBox.information(
            parent,
            MessageBox.tr("Nenhuma tarefa"),
            MessageBox.tr("Não há tarefas nesta coluna."),
        )

    @staticmethod
    def tempo_no_tasks_anywhere(parent):
        return MessageBox.information(
            parent,
            MessageBox.tr("Nenhuma tarefa"),
            MessageBox.tr("Não há tarefas em nenhuma coluna."),
        )

    @staticmethod
    def tempo_share_eisenhower_success(parent, enviados: int):
        if enviados > 1:
            msg = MessageBox.tr("{n} tarefas enviadas com sucesso para 🗂️ Matriz Eisenhower! 🗂️").format(n=enviados)

        else:
            msg = MessageBox.tr("Tarefa enviada com sucesso para 🗂️ Matriz Eisenhower! 🗂️")

        return MessageBox.info_success(parent, msg)

    @staticmethod
    def information(parent, title: str, text: str, buttons=QMessageBox.StandardButton.Ok, default_button=QMessageBox.StandardButton.NoButton):
        try:
            resolved_parent = MessageBox._resolve_parent_widget(parent)
            return QMessageBox.information(resolved_parent, title, text, buttons, default_button)

        except Exception as exc:
            logger.error(f"Erro ao exibir mensagem de informação: {exc}", exc_info=True)
            return QMessageBox.StandardButton.NoButton

    @staticmethod
    def warning(parent, title: str, text: str, buttons=QMessageBox.StandardButton.Ok, default_button=QMessageBox.StandardButton.NoButton):
        try:
            resolved_parent = MessageBox._resolve_parent_widget(parent)
            return QMessageBox.warning(resolved_parent, title, text, buttons, default_button)

        except Exception as exc:
            logger.error(f"Erro ao exibir mensagem de aviso: {exc}", exc_info=True)
            return QMessageBox.StandardButton.NoButton

    @staticmethod
    def critical(parent, title: str, text: str, buttons=QMessageBox.StandardButton.Ok, default_button=QMessageBox.StandardButton.NoButton):
        try:
            resolved_parent = MessageBox._resolve_parent_widget(parent)
            return QMessageBox.critical(resolved_parent, title, text, buttons, default_button)

        except Exception as exc:
            logger.error(f"Erro ao exibir mensagem crítica: {exc}", exc_info=True)
            return QMessageBox.StandardButton.NoButton

    @staticmethod
    def question(parent, title: str, text: str, buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, default_button=QMessageBox.StandardButton.No):
        try:
            resolved_parent = MessageBox._resolve_parent_widget(parent)
            return QMessageBox.question(resolved_parent, title, text, buttons, default_button)

        except Exception as exc:
            logger.error(f"Erro ao exibir mensagem de confirmação: {exc}", exc_info=True)
            return QMessageBox.StandardButton.No
