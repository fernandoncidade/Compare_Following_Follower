from __future__ import annotations
import sys
from .src_31_qt_excepthook import _qt_excepthook
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def run_gui(initial_user: str, force_refresh: bool = False) -> int:
    try:
        from source.modules import source as core

        try:
            from PySide6.QtCore import QCoreApplication
            from PySide6.QtGui import QIcon
            from PySide6.QtWidgets import QApplication
            from source.language.tr_01_gerenciadorTraducao import GerenciadorTraducao
            from source.modules.CompareApp import CompareApp
            from source.modules.FetchWorker import FetchWorker
            from source.modules.UnfollowWorker import UnfollowWorker

        except Exception as exc:
            raise core.ConfigError("PySide6 não está disponível neste ambiente. Rode com --cli.") from exc

        core._set_windows_app_user_model_id()
        current_theme_is_light = core._read_windows_light_theme_flag()
        icon_path = core._resolve_app_icon_path_for_theme(current_theme_is_light)

        app = QApplication.instance()
        owns_app = app is None

        if app is None:
            app = QApplication(sys.argv)

        try:
            app.setProperty("_compare_follow_close_requested", False)

        except Exception:
            pass

        translation_manager = GerenciadorTraducao()
        translation_manager.aplicar_traducao()

        app_icon = None

        if icon_path:
            candidate_icon = QIcon(icon_path)

            if not candidate_icon.isNull():
                app_icon = candidate_icon
                app.setWindowIcon(app_icon)

        window = CompareApp(
            start_user=initial_user,
            force_network_refresh=force_refresh,
            app_instance=app,
            theme_is_light=current_theme_is_light,
            initial_icon_path=icon_path,
            fetch_worker_cls=FetchWorker,
            unfollow_worker_cls=UnfollowWorker,
            build_session_fn=core.build_session,
            get_compare_data_fn=core.get_compare_data,
            get_token_fn=core.get_token,
            unfollow_user_fn=core.unfollow_user,
            unfollow_result_cls=core.UnfollowResult,
            load_cached_data_fn=core.load_cached_data,
            load_previous_non_followers_fn=core.load_previous_non_followers,
            save_non_followers_state_fn=core.save_non_followers_state,
            format_cache_status_fn=core.format_cache_status,
            format_rate_limit_fn=core.format_rate_limit,
            format_exception_fn=core.format_exception,
            resolve_theme_flag_fn=core._read_windows_light_theme_flag,
            resolve_icon_for_theme_fn=core._resolve_app_icon_path_for_theme,
            config_error_cls=core.ConfigError,
            translation_manager=translation_manager,
        )

        if app_icon is not None and not app_icon.isNull():
            window.setWindowIcon(app_icon)

        window.setWindowTitle(QCoreApplication.translate("App", "GitHub Follow Compare"))
        window.resize(980, 650)
        window.show()

        if owns_app:
            previous_excepthook = sys.excepthook
            sys.excepthook = _qt_excepthook(previous_excepthook)

            try:
                exit_code = app.exec()

                if exit_code != 0:
                    try:
                        close_requested = bool(app.property("_compare_follow_close_requested"))

                    except Exception:
                        close_requested = False

                    if close_requested:
                        return 0

                return exit_code

            except KeyboardInterrupt:
                return 130

            finally:
                sys.excepthook = previous_excepthook

        return 0

    except Exception as exc:
        logger.error(f"Erro durante execução GUI: {exc}")
        return 1
