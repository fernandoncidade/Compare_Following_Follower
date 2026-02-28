from source import main, format_exception
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


if __name__ == "__main__":
    try:
        exit_code = main()

        if exit_code is None:
            exit_code = 0

        raise SystemExit(int(exit_code))

    except KeyboardInterrupt:
        logger.error("Execução interrompida pelo usuário.")
        raise SystemExit(130)

    except Exception as exc:
        logger.error(format_exception(exc))
        raise SystemExit(1)
