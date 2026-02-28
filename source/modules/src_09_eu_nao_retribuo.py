from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def eu_nao_retribuo(followers: set[str], following: set[str]) -> list[str]:
    try:
        normalized_followers = {item.strip().lower() for item in followers if isinstance(item, str) and item.strip()}
        normalized_following = {item.strip().lower() for item in following if isinstance(item, str) and item.strip()}
        return sorted(normalized_followers - normalized_following)

    except Exception as exc:
        logger.error(f"Erro ao calcular usuários que eu não retribuo: {exc}")
