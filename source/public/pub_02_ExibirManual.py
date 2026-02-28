from PySide6.QtCore import QCoreApplication, Qt, QEvent
from PySide6.QtGui import QTextCharFormat, QFont, QTextCursor, QFontMetrics
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QTextBrowser
from source.utils.LogManager import LogManager
from source.utils.MessageBox import MessageBox
logger = LogManager.get_logger()

def _tr_multi(key: str) -> str:
    val = QCoreApplication.translate("App", key)

    if val and val != key:
        return val

    val = QCoreApplication.translate("InterfaceGrafica", key)
    return val if val and val != key else key

def exibir_manual(app):
    try:
        existing = getattr(app, "_manual_dialog", None)
        if existing is not None:
            try:
                if existing.isVisible():
                    existing.raise_()
                    existing.activateWindow()
                    return

            except Exception:
                pass

        def _get_idioma_atual() -> str:
            idioma_local = "pt_BR"
            try:
                if hasattr(app, "gerenciador_traducao") and app.gerenciador_traducao:
                    idioma_local = app.gerenciador_traducao.obter_idioma_atual() or "pt_BR"

            except Exception:
                pass

            return idioma_local

        from source.public.pub_05_Manual import (get_manual_blocks, get_manual_document, get_manual_title,)

        idioma = _get_idioma_atual()
        window_title = get_manual_title(idioma)
        blocks, order = get_manual_blocks(idioma)
        sections = get_manual_document(idioma)


        class ManualDialog(QDialog):
            def changeEvent(self, event) -> None:
                super().changeEvent(event)

                if event.type() == QEvent.Type.LanguageChange:
                    try:
                        refresh_manual()

                    except Exception:
                        logger.debug("Falha ao atualizar tradução do Manual em runtime", exc_info=True)

        dlg = ManualDialog(None)
        dlg.setWindowTitle(window_title)

        dlg.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowSystemMenuHint
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
            | Qt.WindowType.WindowCloseButtonHint
        )

        dlg.setWindowModality(Qt.WindowModality.NonModal)
        dlg.setModal(False)
        dlg.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

        setattr(app, "_manual_dialog", dlg)

        def _clear_manual_dialog(*_args) -> None:
            if getattr(app, "_manual_dialog", None) is dlg:
                setattr(app, "_manual_dialog", None)

        dlg.destroyed.connect(_clear_manual_dialog)

        qt_app = QCoreApplication.instance()

        if qt_app is not None:
            qt_app.aboutToQuit.connect(dlg.close)

        try:
            app.destroyed.connect(dlg.close)

        except Exception:
            pass

        dlg.setMinimumSize(900, 650)

        root = QVBoxLayout(dlg)

        body = QHBoxLayout()
        root.addLayout(body)

        lst = QListWidget()
        lst.setMinimumWidth(300)

        viewer = QTextBrowser()
        viewer.setReadOnly(True)
        viewer.setOpenLinks(False)

        body.addWidget(lst, 0)
        body.addWidget(viewer, 1)

        btn_close = QPushButton()
        btn_close.clicked.connect(dlg.close)
        footer = QHBoxLayout()
        footer.addStretch(1)
        footer.addWidget(btn_close)
        root.addLayout(footer)

        dlg._manual_positions = {}
        dlg._manual_row_to_id = []
        dlg._manual_id_to_title = {}

        def _apply_close_label() -> None:
            close_text = _tr_multi("Fechar")

            if close_text == "Fechar":
                close_text = "Fechar" if _get_idioma_atual() == "pt_BR" else "Close"

            btn_close.setText(close_text)
            fm = QFontMetrics(btn_close.font())
            text_w = fm.horizontalAdvance(btn_close.text())
            btn_close.setFixedWidth(text_w + 24)

        def _render_manual(lang: str) -> None:
            nonlocal blocks, order, sections

            blocks, order = get_manual_blocks(lang)
            sections = get_manual_document(lang)

            dlg._manual_id_to_title = {s.id: s.title for s in sections}
            dlg._manual_row_to_id = list(order)

            lst.blockSignals(True)
            lst.clear()

            for sid in dlg._manual_row_to_id:
                lst.addItem(dlg._manual_id_to_title.get(sid, sid))

            lst.blockSignals(False)
            viewer.clear()

            base_font = viewer.font()
            base_size = base_font.pointSize()

            if base_size is None or base_size <= 0:
                base_size = 10

            fmt_normal = QTextCharFormat()
            fmt_normal.setFont(base_font)

            fmt_main_title = QTextCharFormat(fmt_normal)
            fmt_main_title.setFontWeight(QFont.Weight.Bold)
            fmt_main_title.setFontPointSize(base_size + 8)

            fmt_toc_title = QTextCharFormat(fmt_normal)
            fmt_toc_title.setFontWeight(QFont.Weight.Bold)

            fmt_toc_item = QTextCharFormat(fmt_normal)
            fmt_toc_item.setFontWeight(QFont.Weight.Bold)

            fmt_body_title = QTextCharFormat(fmt_normal)
            fmt_body_title.setFontWeight(QFont.Weight.Bold)
            fmt_body_title.setFontPointSize(base_size + 2)

            cursor = viewer.textCursor()
            cursor.beginEditBlock()

            dlg._manual_positions = {}

            def insert_line(text: str, fmt: QTextCharFormat | None = None) -> None:
                cursor.insertText(text, fmt or fmt_normal)
                cursor.insertBlock()

            def insert_blank() -> None:
                cursor.insertBlock()

            manual_title = get_manual_title(lang)
            title_line_used = False

            for blk in blocks:
                if blk.kind == "blank":
                    insert_blank()
                    continue

                if blk.kind == "divider":
                    insert_line(blk.text, fmt_normal)
                    continue

                if blk.kind == "toc_title":
                    insert_line(blk.text, fmt_toc_title)
                    continue

                if blk.kind == "toc_item":
                    fmt_link = QTextCharFormat(fmt_toc_item)
                    fmt_link.setAnchor(True)
                    fmt_link.setAnchorHref(blk.section_id or "")
                    insert_line(blk.text, fmt_link)
                    continue

                if blk.kind in ("section_title", "detail_title"):
                    if blk.section_id:
                        dlg._manual_positions[blk.section_id] = cursor.position()

                    insert_line(blk.text, fmt_body_title)
                    continue

                if blk.kind == "bullet":
                    insert_line(f"    - {blk.text}", fmt_normal)
                    continue

                if blk.kind == "line":
                    if (not title_line_used) and (blk.text == manual_title):
                        insert_line(blk.text, fmt_main_title)
                        title_line_used = True

                    else:
                        insert_line(blk.text, fmt_normal)

                    continue

                insert_line(blk.text, fmt_normal)

            cursor.endEditBlock()
            viewer.moveCursor(QTextCursor.Start)

        def scroll_cursor_to_top() -> None:
            viewer.ensureCursorVisible()
            sb = viewer.verticalScrollBar()
            y = viewer.cursorRect().top()
            sb.setValue(sb.value() + y)

        def go_to_section_id(section_id: str) -> None:
            try:
                pos = getattr(dlg, "_manual_positions", {}).get(section_id)

                if pos is None:
                    return

                c = viewer.textCursor()
                c.setPosition(pos)
                viewer.setTextCursor(c)
                scroll_cursor_to_top()

            except Exception:
                logger.debug("Falha ao navegar para seção do manual", exc_info=True)

        def go_to_section(row: int) -> None:
            ids = getattr(dlg, "_manual_row_to_id", [])

            if row < 0 or row >= len(ids):
                return

            go_to_section_id(ids[row])

        def on_anchor_clicked(url) -> None:
            sid = url.toString().strip()

            if not sid:
                return

            go_to_section_id(sid)

        def refresh_manual() -> None:
            ids = getattr(dlg, "_manual_row_to_id", [])
            current_row = lst.currentRow()
            current_sid = ids[current_row] if 0 <= current_row < len(ids) else None

            lang = _get_idioma_atual()
            dlg.setWindowTitle(get_manual_title(lang))
            _apply_close_label()
            _render_manual(lang)

            if current_sid and current_sid in dlg._manual_row_to_id:
                lst.setCurrentRow(dlg._manual_row_to_id.index(current_sid))

            else:
                lst.setCurrentRow(0)

        viewer.anchorClicked.connect(on_anchor_clicked)
        lst.currentRowChanged.connect(go_to_section)

        _apply_close_label()
        _render_manual(idioma)
        lst.setCurrentRow(0)

        dlg.show()
        dlg.raise_()
        dlg.activateWindow()

    except Exception as e:
        logger.error(f"Erro ao abrir Manual: {e}", exc_info=True)
        MessageBox.critical_error_exception(app, e, tr_func=_tr_multi)
