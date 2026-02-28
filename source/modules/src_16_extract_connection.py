from __future__ import annotations
from typing import Any
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _extract_connection(user_data: dict[str, Any], field_name: str, enabled: bool) -> tuple[list[str], bool, str | None]:
    try:
        from source.modules import source as core

        if not enabled:
            return [], False, None

        connection = user_data.get(field_name)

        if not isinstance(connection, dict):
            raise core.GraphQLError(f"Resposta GraphQL inválida para '{field_name}'.")

        nodes = connection.get("nodes")
        page_info = connection.get("pageInfo")

        if not isinstance(nodes, list) or not isinstance(page_info, dict):
            raise core.GraphQLError(f"Estrutura inválida para '{field_name}'.")

        logins: list[str] = []

        for node in nodes:
            if not isinstance(node, dict):
                continue

            raw_login = node.get("login")

            if not isinstance(raw_login, str):
                continue

            normalized_login = raw_login.strip().lower()

            if normalized_login:
                logins.append(normalized_login)

        has_next = bool(page_info.get("hasNextPage"))
        raw_end_cursor = page_info.get("endCursor")
        end_cursor = raw_end_cursor if isinstance(raw_end_cursor, str) else None
        return logins, has_next, end_cursor

    except Exception as exc:
        logger.error(f"Erro ao extrair conexão '{field_name}': {exc}")
