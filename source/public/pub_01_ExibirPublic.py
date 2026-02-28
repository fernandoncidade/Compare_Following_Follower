from PySide6.QtCore import QCoreApplication, Qt, QEvent
from source.public import (SobreDialog, SITE_LICENSES, 
    LICENSE_TEXT_PT_BR, LICENSE_TEXT_EN_US, 
    NOTICE_TEXT_PT_BR, NOTICE_TEXT_EN_US, 
    ABOUT_TEXT_PT_BR, ABOUT_TEXT_EN_US, 
    Privacy_Policy_pt_BR, Privacy_Policy_en_US, 
    History_APP_pt_BR, History_APP_en_US, 
    RELEASE_NOTES_pt_BR, RELEASE_NOTES_en_US,)
from source.utils.LogManager import LogManager
from source.utils.MessageBox import MessageBox
logger = LogManager.get_logger()

def _tr_multi(key: str) -> str:
    val = QCoreApplication.translate("App", key)

    if val and val != key:
        return val

    val = QCoreApplication.translate("InterfaceGrafica", key)
    return val if val and val != key else key

def exibir_sobre(app):
    try:
        existing = getattr(app, "_sobre_dialog", None)

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

        def _lbl(pt, en, idioma_local: str):
            return pt if idioma_local == "pt_BR" else en

        def _compute_payload(idioma_local: str) -> dict:
            textos_sobre = {"pt_BR": ABOUT_TEXT_PT_BR, "en_US": ABOUT_TEXT_EN_US}
            textos_licenca = {"pt_BR": LICENSE_TEXT_PT_BR, "en_US": LICENSE_TEXT_EN_US}
            textos_aviso = {"pt_BR": NOTICE_TEXT_PT_BR, "en_US": NOTICE_TEXT_EN_US}
            textos_privacidade = {"pt_BR": Privacy_Policy_pt_BR, "en_US": Privacy_Policy_en_US}
            history_texts = {"pt_BR": History_APP_pt_BR, "en_US": History_APP_en_US}
            release_notes_texts = {"pt_BR": RELEASE_NOTES_pt_BR, "en_US": RELEASE_NOTES_en_US}

            texto_sobre = textos_sobre.get(idioma_local, textos_sobre["en_US"])
            texto_licenca = textos_licenca.get(idioma_local, textos_licenca["en_US"])
            texto_aviso = textos_aviso.get(idioma_local, textos_aviso["en_US"])
            texto_privacidade = textos_privacidade.get(idioma_local, textos_privacidade["en_US"])
            texto_history = history_texts.get(idioma_local, history_texts["en_US"])
            texto_release_notes = release_notes_texts.get(idioma_local, release_notes_texts["en_US"])

            show_history = _tr_multi("show_history")

            if show_history == "show_history":
                show_history = _lbl("Histórico", "History", idioma_local)

            hide_history = _tr_multi("hide_history")

            if hide_history == "hide_history":
                hide_history = _lbl("Ocultar histórico", "Hide history", idioma_local)

            show_details = _tr_multi("show_details")

            if show_details == "show_details":
                show_details = _lbl("Detalhes", "Details", idioma_local)

            hide_details = _tr_multi("hide_details")

            if hide_details == "hide_details":
                hide_details = _lbl("Ocultar detalhes", "Hide details", idioma_local)

            show_licenses = _tr_multi("show_licenses")

            if show_licenses == "show_licenses":
                show_licenses = _lbl("Licenças", "Licenses", idioma_local)

            hide_licenses = _tr_multi("hide_licenses")

            if hide_licenses == "hide_licenses":
                hide_licenses = _lbl("Ocultar licenças", "Hide licenses", idioma_local)

            show_notices = _tr_multi("show_notices")

            if show_notices == "show_notices":
                show_notices = _lbl("Avisos", "Notices", idioma_local)

            hide_notices = _tr_multi("hide_notices")

            if hide_notices == "hide_notices":
                hide_notices = _lbl("Ocultar avisos", "Hide notices", idioma_local)

            show_privacy_policy = _tr_multi("show_privacy_policy")

            if show_privacy_policy == "show_privacy_policy":
                show_privacy_policy = _lbl("Política de privacidade", "Privacy Policy", idioma_local)

            hide_privacy_policy = _tr_multi("hide_privacy_policy")

            if hide_privacy_policy == "hide_privacy_policy":
                hide_privacy_policy = _lbl("Ocultar política de privacidade", "Hide privacy policy", idioma_local)

            show_release_notes = _tr_multi("show_release_notes")

            if show_release_notes == "show_release_notes":
                show_release_notes = _lbl("Notas de versão", "Release Notes", idioma_local)

            hide_release_notes = _tr_multi("hide_release_notes")

            if hide_release_notes == "hide_release_notes":
                hide_release_notes = _lbl("Ocultar notas de versão", "Hide release notes", idioma_local)

            titulo_tr = _tr_multi("Sobre — Compare - Following and Follower")

            if titulo_tr == "Sobre — Compare - Following and Follower":
                sobre_txt = _tr_multi("Sobre")

                if sobre_txt == "Sobre":
                    sobre_txt = _lbl("Sobre", "About", idioma_local)

                titulo_tr = f"{sobre_txt} — Compare - Following and Follower"

            version_label = _tr_multi("version")

            if version_label == "version":
                version_label = _lbl("Versão", "Version", idioma_local)

            authors_label = _tr_multi("authors:")

            if authors_label == "authors:":
                authors_label = _lbl("Autores:", "Authors:", idioma_local)

            description_label = _tr_multi("description:")

            if description_label == "description:":
                description_label = _lbl("Descrição:", "Description:", idioma_local)

            description_text = _tr_multi("description_text")

            if description_text == "description_text":
                description_text = _lbl("", "", idioma_local)

            app_title_key = "Compare - Following and Follower"
            app_title = _tr_multi(app_title_key)

            if app_title == app_title_key:
                app_title = "Compare - Following and Follower" if idioma_local == "en_US" else app_title_key

            texto_fixo = (
                f"<span style='font-size:16px;font-weight:bold'>{app_title}</span><br/><br/>"
                f"<span><b>{version_label}</b> 2026.2.29.0</span><br/><br/>"
                f"<span><b>{authors_label}</b> Fernando Nillsson Cidade</span><br/><br/>"
                f"<span><b>{description_label}</b> {description_text}</span><br/>"
            )

            ok_text = _tr_multi("OK")

            if ok_text == "OK":
                ok_text = _lbl("OK", "OK", idioma_local)

            site_oficial_text = _tr_multi("site_oficial")

            if site_oficial_text == "site_oficial":
                site_oficial_text = _lbl("Site oficial", "Official site", idioma_local)

            info_not_available_text = _tr_multi("information_not_available")

            if info_not_available_text == "information_not_available":
                info_not_available_text = _lbl("Informação não disponível", "Information not available", idioma_local)

            return {
                "titulo": titulo_tr,
                "texto_fixo": texto_fixo,
                "texto_history": texto_history,
                "detalhes": texto_sobre,
                "licencas": texto_licenca,
                "sites_licencas": SITE_LICENSES,
                "show_history_text": show_history,
                "hide_history_text": hide_history,
                "show_details_text": show_details,
                "hide_details_text": hide_details,
                "show_licenses_text": show_licenses,
                "hide_licenses_text": hide_licenses,
                "ok_text": ok_text,
                "site_oficial_text": site_oficial_text,
                "avisos": texto_aviso,
                "show_notices_text": show_notices,
                "hide_notices_text": hide_notices,
                "privacy_policy": texto_privacidade,
                "show_privacy_policy_text": show_privacy_policy,
                "hide_privacy_policy_text": hide_privacy_policy,
                "info_not_available_text": info_not_available_text,
                "release_notes": texto_release_notes,
                "show_release_notes_text": show_release_notes,
                "hide_release_notes_text": hide_release_notes,
            }

        def refresh_sobre() -> None:
            idioma_local = _get_idioma_atual()
            p = _compute_payload(idioma_local)
            dialog.update_content(
                titulo=p["titulo"],
                texto_fixo=p["texto_fixo"],
                texto_history=p["texto_history"],
                detalhes=p["detalhes"],
                licencas=p["licencas"],
                sites_licencas=p["sites_licencas"],
                ok_text=p["ok_text"],
                site_oficial_text=p["site_oficial_text"],
                avisos=p["avisos"],
                privacy_policy=p["privacy_policy"],
                release_notes=p["release_notes"],
                show_history_text=p["show_history_text"],
                hide_history_text=p["hide_history_text"],
                show_details_text=p["show_details_text"],
                hide_details_text=p["hide_details_text"],
                show_licenses_text=p["show_licenses_text"],
                hide_licenses_text=p["hide_licenses_text"],
                show_notices_text=p["show_notices_text"],
                hide_notices_text=p["hide_notices_text"],
                show_privacy_policy_text=p["show_privacy_policy_text"],
                hide_privacy_policy_text=p["hide_privacy_policy_text"],
                show_release_notes_text=p["show_release_notes_text"],
                hide_release_notes_text=p["hide_release_notes_text"],
                info_not_available_text=p["info_not_available_text"],
            )


        class SobreDialogRuntime(SobreDialog):
            def changeEvent(self, event) -> None:
                super().changeEvent(event)

                if event.type() == QEvent.Type.LanguageChange:
                    try:
                        refresh_sobre()

                    except Exception:
                        logger.debug("Falha ao atualizar tradução do Sobre em runtime", exc_info=True)

        idioma = _get_idioma_atual()
        p = _compute_payload(idioma)

        dialog = SobreDialogRuntime(
            None,
            titulo=p["titulo"],
            texto_fixo=p["texto_fixo"],
            texto_history=p["texto_history"],
            detalhes=p["detalhes"],
            licencas=p["licencas"],
            sites_licencas=p["sites_licencas"],
            show_history_text=p["show_history_text"],
            hide_history_text=p["hide_history_text"],
            show_details_text=p["show_details_text"],
            hide_details_text=p["hide_details_text"],
            show_licenses_text=p["show_licenses_text"],
            hide_licenses_text=p["hide_licenses_text"],
            ok_text=p["ok_text"],
            site_oficial_text=p["site_oficial_text"],
            avisos=p["avisos"],
            show_notices_text=p["show_notices_text"],
            hide_notices_text=p["hide_notices_text"],
            privacy_policy=p["privacy_policy"],
            show_privacy_policy_text=p["show_privacy_policy_text"],
            hide_privacy_policy_text=p["hide_privacy_policy_text"],
            info_not_available_text=p["info_not_available_text"],
            release_notes=p["release_notes"],
            show_release_notes_text=p["show_release_notes_text"],
            hide_release_notes_text=p["hide_release_notes_text"],
        )

        setattr(app, "_sobre_dialog", dialog)

        def _clear_sobre_dialog(*_args) -> None:
            if getattr(app, "_sobre_dialog", None) is dialog:
                setattr(app, "_sobre_dialog", None)

        dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        dialog.destroyed.connect(_clear_sobre_dialog)
        qt_app = QCoreApplication.instance()

        if qt_app is not None:
            qt_app.aboutToQuit.connect(dialog.close)

        try:
            app.destroyed.connect(dialog.close)

        except Exception:
            pass

        dialog.resize(900, int(500 * 1.2))

        try:
            if hasattr(dialog, '_adjust_fixed_label_height'):
                dialog._adjust_fixed_label_height()

        except Exception:
            pass

        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

    except Exception as e:
        logger.error(f"Erro ao exibir diálogo Sobre: {e}", exc_info=True)
        MessageBox.critical_error_exception(app, e, tr_func=_tr_multi)

def exibir_manual(app):
    try:
        from source.public.pub_02_ExibirManual import exibir_manual as exibir_manual_impl
        return exibir_manual_impl(app)

    except Exception as e:
        logger.error(f"Erro ao abrir Manual: {e}", exc_info=True)
        MessageBox.critical_error_exception(app, e, tr_func=_tr_multi)
