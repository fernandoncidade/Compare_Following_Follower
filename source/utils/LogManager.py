import os
import logging
from datetime import datetime


class LogManager:
    _instance = None
    _logger = None
    _log_file = None
    _startup_log_file = None

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._configure_logging()

        return cls._logger

    @classmethod
    def get_log_file(cls):
        if cls._log_file is None:
            cls._configure_logging()

        return cls._log_file

    @classmethod
    def ensure_unicode(cls, message):
        if isinstance(message, bytes):
            return message.decode('utf-8', errors='replace')

        return str(message)

    @classmethod
    def _configure_logging(cls):
        try:
            log_dir = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'FollowersFollowingGitHub', 'logs')
            os.makedirs(log_dir, exist_ok=True)
            cls._log_file = os.path.join(log_dir, f'file_FollowersFollowingGitHub_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

            logging.basicConfig(
                level=logging.ERROR,
                format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                handlers=[
                    logging.FileHandler(cls._log_file, encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )

            cls._logger = logging.getLogger('File_FollowersFollowingGitHub')

            logging.getLogger('comtypes').setLevel(logging.CRITICAL)
            logging.getLogger('comtypes._comobject').setLevel(logging.CRITICAL)
            logging.getLogger('comtypes._vtbl').setLevel(logging.CRITICAL)
            logging.getLogger('comtypes._post_coinit.unknwn').setLevel(logging.CRITICAL)

            try:
                cls._cleanup_logs()

            except Exception:
                pass

        except Exception as e:
            try:
                user_data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'FollowersFollowingGitHub', 'logs')
                os.makedirs(user_data_dir, exist_ok=True)
                cls._log_file = os.path.join(user_data_dir, f'file_FollowersFollowingGitHub_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

                logging.basicConfig(
                    level=logging.ERROR,
                    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                    handlers=[
                        logging.FileHandler(cls._log_file, encoding='utf-8'),
                        logging.StreamHandler()
                    ]
                )

                cls._logger = logging.getLogger('File_FollowersFollowingGitHub')

                logging.getLogger('comtypes').setLevel(logging.CRITICAL)
                logging.getLogger('comtypes._comobject').setLevel(logging.CRITICAL)
                logging.getLogger('comtypes._vtbl').setLevel(logging.CRITICAL)
                logging.getLogger('comtypes._post_coinit.unknwn').setLevel(logging.CRITICAL)

                cls._logger.error(f"Erro ao configurar logging no diretório padrão: {e}")

                try:
                    cls._cleanup_logs()

                except Exception:
                    pass

            except Exception:
                logging.basicConfig(level=logging.CRITICAL)
                cls._logger = logging.getLogger('File_FollowersFollowingGitHub')

    @classmethod
    def debug(cls, message):
        cls.get_logger().debug(cls.ensure_unicode(message))

    @classmethod
    def info(cls, message):
        cls.get_logger().info(cls.ensure_unicode(message))

    @classmethod
    def warning(cls, message):
        cls.get_logger().warning(cls.ensure_unicode(message))

    @classmethod
    def error(cls, message, exc_info=False):
        cls.get_logger().error(cls.ensure_unicode(message), exc_info=exc_info)

    @classmethod
    def critical(cls, message, exc_info=True):
        cls.get_logger().critical(cls.ensure_unicode(message), exc_info=exc_info)

    @classmethod
    def _get_log_dir(cls) -> str:
        try:
            if cls._log_file:
                return os.path.dirname(cls._log_file)

            base = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~')
            return os.path.join(base, 'FollowersFollowingGitHub', 'logs')

        except Exception:
            return os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'FollowersFollowingGitHub', 'logs')

    @classmethod
    def _cleanup_logs(cls) -> None:
        try:
            log_dir = cls._get_log_dir()
            if not os.path.isdir(log_dir):
                return

            file_logs = [
                os.path.join(log_dir, name)
                for name in os.listdir(log_dir)
                if name.endswith(".log") and name.startswith("file_FollowersFollowingGitHub_")
            ]

            if len(file_logs) <= 10:
                return

            file_logs_sorted = sorted(file_logs, key=lambda p: os.path.getmtime(p))
            to_remove = len(file_logs_sorted) - 10
            removed = 0

            active_paths = set()
            if cls._log_file:
                active_paths.add(os.path.abspath(cls._log_file))

            if cls._startup_log_file:
                active_paths.add(os.path.abspath(cls._startup_log_file))

            for path in file_logs_sorted:
                if removed >= to_remove:
                    break

                try:
                    abs_path = os.path.abspath(path)
                    if abs_path in active_paths:
                        continue

                    os.remove(path)
                    removed += 1

                    try:
                        if cls._logger:
                            cls._logger.info(f"Removed old log file: {path}")

                    except Exception:
                        pass

                except Exception as e:
                    try:
                        if cls._logger:
                            cls._logger.warning(f"Failed to remove log file {path}: {e}")

                    except Exception:
                        pass

        except Exception:
            try:
                if cls._logger:
                    cls._logger.debug("Erro ao executar limpeza de logs")

            except Exception:
                pass
