from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def load_previous_non_followers(user: str) -> set[str] | None:
    try:
        from source.modules import source as core

        payload = core._load_non_followers_state_file()

        if payload is None:
            return None

        if payload.get("user") != user:
            return None

        values = payload.get("followers")

        if not isinstance(values, list):
            return None

        return {item.strip().lower() for item in values if isinstance(item, str) and item.strip()}

    except Exception as exc:
        logger.error(f"Erro ao carregar seguidores anteriores para o usuário '{user}': {exc}")
