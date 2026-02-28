from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def nao_retribuem(following: set[str], followers: set[str]) -> list[str]:
    try:
        normalized_following = {item.strip().lower() for item in following if isinstance(item, str) and item.strip()}
        normalized_followers = {item.strip().lower() for item in followers if isinstance(item, str) and item.strip()}
        return sorted(normalized_following - normalized_followers)

    except Exception as exc:
        logger.error(f"Erro ao calcular usuários que não retribuem: {exc}")
