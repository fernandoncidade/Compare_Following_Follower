from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _is_missing_token_error(self, message: str) -> bool:
    try:
        normalized_message = (message or "").strip().lower()

        if "github_token" not in normalized_message:
            return False

        return (
            ("graphql sem cache" in normalized_message)
            or ("graphql without cache" in normalized_message)
            or ("executar unfollow" in normalized_message)
            or ("execute unfollow" in normalized_message)
        )

    except Exception as exc:
        logger.error(f"Erro ao validar mensagem de token ausente: {exc}")
        return False
