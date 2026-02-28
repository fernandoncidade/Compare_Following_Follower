from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _render_cache_status(self) -> str:
    try:
        mode = self._cache_status_mode
        payload = self._cache_status_payload

        if mode == "updating":
            return self._tr("Atualizando dados...")

        if mode == "interrupted":
            return self._tr("Atualização interrompida pelo usuário.")

        if mode == "start_failed":
            return self._tr("Falha ao iniciar atualização.")

        if mode == "fetch_failed":
            return self._tr("Falha ao atualizar.")

        if mode == "from_cache":
            return self._tr("Origem: cache local (idade {age}s)").format(age=payload.get("age", 0))

        if mode == "from_graphql":
            return self._tr("Origem: GraphQL (requisições nesta atualização: {requests})").format(requests=payload.get("requests", 0))

        if mode == "unfollowing":
            return self._tr("Executando unfollow em {count} perfil(is)...").format(count=payload.get("count", 0))

        if mode == "unfollow_failed":
            return self._tr("Falha ao executar unfollow.")

        return self._tr("Origem: -")

    except Exception as exc:
        logger.error(f"Erro ao renderizar status de cache: {exc}")
        return self._tr("Origem: -")
