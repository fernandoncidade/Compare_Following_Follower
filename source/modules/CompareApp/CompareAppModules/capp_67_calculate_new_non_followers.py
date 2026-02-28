from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _calculate_new_non_followers(self, data: Any) -> list[str]:
    try:
        values = getattr(data, "nao_me_seguem_mais", None)

        if isinstance(values, list):
            return sorted({item.strip().lower() for item in values if isinstance(item, str) and item.strip()})

        previous_followers = self._load_previous_non_followers_fn(data.user)

        if previous_followers is None:
            return []

        current_followers = {item.strip().lower() for item in getattr(data, "followers", []) if isinstance(item, str) and item.strip()}
        return sorted(previous_followers - current_followers)

    except Exception as exc:
        user_value = getattr(data, "user", self.user_input.text().strip() or "<desconhecido>")
        logger.error(f"Erro ao calcular usuários que não me seguem mais para o usuário '{user_value}': {exc}")
        return []
