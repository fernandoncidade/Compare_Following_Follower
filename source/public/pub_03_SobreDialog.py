from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser, QSizePolicy, QHBoxLayout, QTabWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class SobreDialog(QDialog):
    def __init__(self, 
                parent, 
                titulo, 
                texto_fixo, 
                texto_history, 
                detalhes, 
                licencas, 
                sites_licencas, 
                show_history_text=None, 
                hide_history_text=None, 
                show_details_text=None, 
                hide_details_text=None, 
                show_licenses_text=None, 
                hide_licenses_text=None, 
                ok_text=None, 
                site_oficial_text=None, 
                avisos=None, 
                show_notices_text=None, 
                hide_notices_text=None, 
                privacy_policy=None, 
                show_privacy_policy_text=None, 
                hide_privacy_policy_text=None, 
                info_not_available_text="Information not available", 
                release_notes=None, 
                show_release_notes_text=None,
                hide_release_notes_text=None):
        super().__init__(parent)
        try:
            self.setWindowTitle(titulo)
            self.setWindowFlags(
            Qt.Window |
            Qt.WindowTitleHint |
            Qt.WindowSystemMenuHint |
            Qt.WindowMinMaxButtonsHint |
            Qt.WindowCloseButtonHint)
            self.setModal(False)

            layout = QVBoxLayout(self)
            layout.setSpacing(0)

            # Fixed Label
            self.fixed_label = QLabel(texto_fixo)
            self.fixed_label.setTextFormat(Qt.TextFormat.RichText)
            self.fixed_label.setWordWrap(True)
            self.fixed_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.fixed_label.setContentsMargins(0, 0, 0, 0)
            self.fixed_label.setIndent(0)
            self.fixed_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            try:
                self.fixed_label.adjustSize()
                h = self.fixed_label.height() or self.fixed_label.sizeHint().height()
                self.fixed_label.setMaximumHeight(h)

            except Exception:
                pass

            layout.addWidget(self.fixed_label)

            sh_history = show_history_text or "Histórico"
            hi_history = hide_history_text or "Ocultar histórico"
            sh_details = show_details_text or "Detalhes"
            hi_details = hide_details_text or "Ocultar detalhes"
            sh_licenses = show_licenses_text or "Licenças"
            hi_licenses = hide_licenses_text or "Ocultar licenças"
            sh_notices = show_notices_text or "Avisos"
            hi_notices = hide_notices_text or "Ocultar avisos"
            sh_privacy = show_privacy_policy_text or "Política de privacidade"
            hi_privacy = hide_privacy_policy_text or "Ocultar política de privacidade"
            sh_release = show_release_notes_text or "Notas de versão"
            hi_release = hide_release_notes_text or "Ocultar notas de versão"
            ok_text = ok_text or "OK"
            site_oficial_text = site_oficial_text or "Official site"

            # Tabs
            self.tabs = QTabWidget()
            self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Histórico Tab
            self.history_browser = QTextBrowser()
            self.history_browser.setReadOnly(True)
            self.history_browser.setOpenExternalLinks(True)

            if texto_history:
                self.history_browser.setPlainText(texto_history)

            else:
                self.history_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(self.history_browser, sh_history)

            # Detalhes Tab
            self.detalhes_browser = QTextBrowser()
            self.detalhes_browser.setReadOnly(True)
            self.detalhes_browser.setOpenExternalLinks(True)

            if detalhes:
                self.detalhes_browser.setPlainText(detalhes)

            else:
                self.detalhes_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(self.detalhes_browser, sh_details)

            # Licenças Tab
            self.licencas_browser = QTextBrowser()
            self.licencas_browser.setReadOnly(True)
            self.licencas_browser.setOpenExternalLinks(True)

            if licencas:
                texto_html = licencas.replace('\n', '<br>')
                texto_html += f"<br><br><h3>{site_oficial_text}</h3><ul>"
                for site in sites_licencas.strip().split('\n'):
                    if site.strip():
                        texto_html += f'<li><a href="{site.strip()}">{site.strip()}</a></li>'

                texto_html += "</ul>"
                self.licencas_browser.setHtml(texto_html)

            else:
                self.licencas_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(self.licencas_browser, sh_licenses)

            # Avisos Tab
            self.avisos_browser = QTextBrowser()
            self.avisos_browser.setReadOnly(True)
            self.avisos_browser.setOpenExternalLinks(True)

            if avisos:
                self.avisos_browser.setPlainText(avisos)

            else:
                self.avisos_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(self.avisos_browser, sh_notices)

            # Política de Privacidade Tab
            self.privacidade_browser = QTextBrowser()
            self.privacidade_browser.setReadOnly(True)
            self.privacidade_browser.setOpenExternalLinks(True)

            if privacy_policy:
                self.privacidade_browser.setPlainText(privacy_policy)

            else:
                self.privacidade_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(self.privacidade_browser, sh_privacy)

            # Notas de Versão Tab
            self.release_notes_browser = QTextBrowser()
            self.release_notes_browser.setReadOnly(True)
            self.release_notes_browser.setOpenExternalLinks(True)

            if release_notes:
                self.release_notes_browser.setPlainText(release_notes)

            else:
                self.release_notes_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(self.release_notes_browser, sh_release)

            self._tab_show_texts = [
                sh_history,
                sh_details,
                sh_licenses,
                sh_notices,
                sh_privacy,
                sh_release
            ]
            self._tab_hide_texts = [
                hi_history,
                hi_details,
                hi_licenses,
                hi_notices,
                hi_privacy,
                hi_release
            ]

            self.tabs.currentChanged.connect(self._on_tab_changed)
            self._update_tab_labels(self.tabs.currentIndex())

            layout.addWidget(self.tabs)

            button_layout = QHBoxLayout()
            button_layout.setContentsMargins(0, 9, 0, 0)
            button_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.ok_button = QPushButton(ok_text)
            self.ok_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.ok_button.clicked.connect(self.accept)
            button_layout.addStretch(1)
            button_layout.addWidget(self.ok_button, 0, Qt.AlignRight | Qt.AlignVCenter)
            layout.addLayout(button_layout)

            self.setMinimumSize(400, 200)

        except Exception as e:
            logger.error(f"Erro ao criar dialog sobre: {e}", exc_info=True)

    def _adjust_fixed_label_height(self):
        try:
            if not self.fixed_label:
                return

            doc = QTextDocument()
            doc.setDefaultFont(self.fixed_label.font())
            doc.setHtml(self.fixed_label.text())
            w = self.fixed_label.width()

            if not w or w <= 0:
                w = max(200, int(self.width() * 0.9))

            doc.setTextWidth(w)
            h = int(doc.size().height())

            if h > 0:
                self.fixed_label.setFixedHeight(h + 2)

        except Exception:
            pass

    def update_content(self,
                       titulo=None,
                       texto_fixo=None,
                       texto_history=None,
                       detalhes=None,
                       licencas=None,
                       sites_licencas=None,
                       ok_text=None,
                       site_oficial_text=None,
                       avisos=None,
                       privacy_policy=None,
                       release_notes=None,
                       show_history_text=None,
                       hide_history_text=None,
                       show_details_text=None,
                       hide_details_text=None,
                       show_licenses_text=None,
                       hide_licenses_text=None,
                       show_notices_text=None,
                       hide_notices_text=None,
                       show_privacy_policy_text=None,
                       hide_privacy_policy_text=None,
                       show_release_notes_text=None,
                       hide_release_notes_text=None,
                       info_not_available_text=None,
                       **kwargs):
        try:
            if titulo is not None:
                self.setWindowTitle(titulo)

            if texto_fixo is not None:
                self.fixed_label.setText(texto_fixo)
                try:
                    self._adjust_fixed_label_height()

                except Exception:
                    pass

            if texto_history is not None:
                if texto_history:
                    self.history_browser.setPlainText(texto_history)

                else:
                    self.history_browser.setHtml(f"<p>{info_not_available_text or 'Information not available'}.</p>")

            if detalhes is not None:
                if detalhes:
                    self.detalhes_browser.setPlainText(detalhes)

                else:
                    self.detalhes_browser.setHtml(f"<p>{info_not_available_text or 'Information not available'}.</p>")

            if licencas is not None or sites_licencas is not None or site_oficial_text is not None:
                lic = licencas or ''
                sites = sites_licencas or ''
                site_text = site_oficial_text or ''
                if lic:
                    texto_html = lic.replace('\n', '<br>')
                    texto_html += f"<br><br><h3>{site_text}</h3><ul>"
                    for site in sites.strip().split('\n'):
                        if site.strip():
                            texto_html += f'<li><a href="{site.strip()}">{site.strip()}</a></li>'

                    texto_html += "</ul>"
                    self.licencas_browser.setHtml(texto_html)

                else:
                    self.licencas_browser.setHtml(f"<p>{info_not_available_text or 'Information not available'}.</p>")

            if avisos is not None:
                if avisos:
                    self.avisos_browser.setPlainText(avisos)

                else:
                    self.avisos_browser.setHtml(f"<p>{info_not_available_text or 'Information not available'}.</p>")

            if privacy_policy is not None:
                if privacy_policy:
                    self.privacidade_browser.setPlainText(privacy_policy)

                else:
                    self.privacidade_browser.setHtml(f"<p>{info_not_available_text or 'Information not available'}.</p>")

            if release_notes is not None:
                if release_notes:
                    self.release_notes_browser.setPlainText(release_notes)

                else:
                    self.release_notes_browser.setHtml(f"<p>{info_not_available_text or 'Information not available'}.</p>")

            if ok_text is not None:
                try:
                    self.ok_button.setText(ok_text)

                except Exception:
                    pass

            show_texts = [show_history_text, show_details_text, show_licenses_text, show_notices_text, show_privacy_policy_text, show_release_notes_text]
            hide_texts = [hide_history_text, hide_details_text, hide_licenses_text, hide_notices_text, hide_privacy_policy_text, hide_release_notes_text]

            for i, v in enumerate(show_texts):
                if v is not None:
                    if len(self._tab_show_texts) > i:
                        self._tab_show_texts[i] = v

                    else:
                        self._tab_show_texts.append(v)

            for i, v in enumerate(hide_texts):
                if v is not None:
                    if len(self._tab_hide_texts) > i:
                        self._tab_hide_texts[i] = v

                    else:
                        self._tab_hide_texts.append(v)

            try:
                self._update_tab_labels(self.tabs.currentIndex())

            except Exception:
                pass

        except Exception as e:
            logger.error(f"Erro ao atualizar conteúdo do Sobre: {e}", exc_info=True)

    def resizeEvent(self, event):
        try:
            super().resizeEvent(event)

        except Exception:
            pass

        try:
            self._adjust_fixed_label_height()

        except Exception:
            pass

    def _on_tab_changed(self, index):
        try:
            self._update_tab_labels(index)

        except Exception as e:
            logger.error(f"Erro ao atualizar rótulos das abas: {e}", exc_info=True)

    def _update_tab_labels(self, current_index):
        count = self.tabs.count()
        while len(self._tab_show_texts) < count:
            self._tab_show_texts.append("")

        while len(self._tab_hide_texts) < count:
            self._tab_hide_texts.append("")

        for i in range(count):
            show = self._tab_show_texts[i] or ""
            hide = self._tab_hide_texts[i] or ""
            self.tabs.setTabText(i, hide if i == current_index else show)
