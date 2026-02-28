from __future__ import annotations
import requests
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def unfollow_user(session: requests.Session, username: str) -> None:
    try:
        from source.modules import source as core

        login = username.strip()

        if not login:
            raise core.ConfigError("Perfil inválido para unfollow.")

        response = session.delete(f"{core.REST_API_URL}/user/following/{login}", timeout=(core.CONNECT_TIMEOUT, core.READ_TIMEOUT),)

        if response.status_code in {204, 404}:
            return

        response.raise_for_status()

    except Exception as exc:
        logger.error(f"Erro ao tentar deixar de seguir o usuário '{username}': {exc}")
