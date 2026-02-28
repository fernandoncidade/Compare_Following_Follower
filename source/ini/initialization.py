import sys
from source.modules import ConfigError, DEFAULT_USER, VERIFY_SSL, build_session, get_compare_data, load_last_user, print_cli_report, run_gui
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def parse_args(argv: list[str]) -> tuple[str, bool, bool]:
    try:
        user = DEFAULT_USER
        cli_mode = False
        force_refresh = False
        idx = 0

        while idx < len(argv):
            arg = argv[idx]

            if arg == "--cli":
                cli_mode = True

            elif arg == "--no-cache":
                force_refresh = True

            elif arg in {"--user", "-u"}:
                idx += 1

                if idx >= len(argv):
                    raise ConfigError("Faltou valor para --user.")

                user = argv[idx].strip()

                if not user:
                    raise ConfigError("Usuário informado em --user está vazio.")

            else:
                raise ConfigError(f"Argumento não reconhecido: {arg}")

            idx += 1

        return user, cli_mode, force_refresh

    except Exception as exc:
        logger.error(f"Erro ao analisar argumentos: {exc}")

def run_cli(user: str, force_refresh: bool) -> int:
    try:
        session = build_session()

        try:
            data = get_compare_data(session, user, force_refresh=force_refresh)

        finally:
            session.close()

        print_cli_report(data)
        return 0

    except Exception as exc:
        logger.error(f"Erro durante execução CLI: {exc}")

def main(argv: list[str] | None = None) -> int:
    try:
        args = sys.argv[1:] if argv is None else argv
        user, cli_mode, force_refresh = parse_args(args)

        if not VERIFY_SSL:
            print("Aviso: SSL desativado por GITHUB_INSECURE. Use apenas para teste.", file=sys.stderr)

        if cli_mode:
            if not user.strip():
                raise ConfigError("No modo CLI, informe um usuário com --user.")

            return run_cli(user=user, force_refresh=force_refresh)

        if not user.strip():
            user = load_last_user()

        try:
            return run_gui(initial_user=user, force_refresh=force_refresh)

        except ConfigError:
            raise

        except Exception as exc:
            message = str(exc).lower()

            if "no display name" in message or "cannot open display" in message:
                return run_cli(user=user, force_refresh=force_refresh)

            raise

    except Exception as exc:
        logger.error(f"Erro na função main: {exc}")
