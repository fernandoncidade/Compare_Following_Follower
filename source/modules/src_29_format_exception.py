from __future__ import annotations
from requests.exceptions import HTTPError, ProxyError, RequestException, SSLError
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def format_exception(exc: Exception) -> str:
    try:
        from source.modules import source as core

        if isinstance(exc, (core.ConfigError, core.GraphQLError)):
            return str(exc)

        if isinstance(exc, HTTPError):
            response = exc.response
            status = response.status_code if response is not None else "desconhecido"

            if response is not None and response.status_code == 403:
                remaining = response.headers.get("X-RateLimit-Remaining")
                reset_at = core._format_rate_limit_reset(response.headers.get("X-RateLimit-Reset"))

                if remaining == "0":
                    if reset_at:
                        return f"Erro HTTP 403 (rate limit excedido). Próximo reset: {reset_at}."

                    return "Erro HTTP 403 (rate limit excedido)."

            if response is not None:
                try:
                    payload = response.json()

                except ValueError:
                    payload = None

                if isinstance(payload, dict) and isinstance(payload.get("message"), str):
                    return f"Erro HTTP do GitHub: {status}. {payload['message']}"

            return f"Erro HTTP do GitHub: {status}."

        if isinstance(exc, SSLError):
            return (
                f"Erro SSL ao acessar api.github.com: {exc}\n"
                "Se estiver em rede corporativa/proxy, configure REQUESTS_CA_BUNDLE.\n"
                "Para teste temporário, use GITHUB_INSECURE=1."
            )

        if isinstance(exc, ProxyError):
            return f"Erro de proxy: {exc}\nRevise HTTPS_PROXY/HTTP_PROXY no ambiente."

        if isinstance(exc, RequestException):
            return f"Falha de rede ao consultar GitHub: {exc}"

        return str(exc)

    except Exception as log_exc:
        logger.error(f"Erro ao formatar exceção: {log_exc}")
