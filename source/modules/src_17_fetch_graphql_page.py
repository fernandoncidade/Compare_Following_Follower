from __future__ import annotations
from typing import Any
import requests
from dataclasses import dataclass
from source.modules.RateLimitInfo import RateLimitInfo
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


@dataclass
class GraphPage:
    followers: list[str]
    following: list[str]
    followers_has_next: bool
    following_has_next: bool
    followers_end_cursor: str | None
    following_end_cursor: str | None
    rate_limit: RateLimitInfo | None

def fetch_graphql_page(session: requests.Session, user: str, after_followers: str | None, after_following: str | None, include_followers: bool, include_following: bool,) -> "GraphPage":
    try:
        from source.modules import source as core

        variables = {
            "login": user,
            "afterFollowers": after_followers,
            "afterFollowing": after_following,
            "includeFollowers": include_followers,
            "includeFollowing": include_following,
        }

        response = session.post(core.GRAPHQL_URL, json={"query": core.GRAPHQL_QUERY, "variables": variables}, timeout=(core.CONNECT_TIMEOUT, core.READ_TIMEOUT),)
        response.raise_for_status()

        payload: Any = response.json()

        if not isinstance(payload, dict):
            raise core.GraphQLError("Resposta inesperada da API GraphQL.")

        errors = payload.get("errors")

        if errors:
            messages: list[str] = []

            if isinstance(errors, list):
                for item in errors:
                    if isinstance(item, dict) and isinstance(item.get("message"), str):
                        messages.append(item["message"])

            detail = "; ".join(messages) if messages else str(errors)
            rate_info = RateLimitInfo.from_headers(response.headers)

            if rate_info and rate_info.remaining == 0:
                reset_msg = f" Próximo reset: {rate_info.reset_at}." if rate_info.reset_at else ""
                raise core.GraphQLError(f"Rate limit excedido.{reset_msg}")

            raise core.GraphQLError(f"Erro GraphQL: {detail}")

        data = payload.get("data")

        if not isinstance(data, dict):
            raise core.GraphQLError("Resposta GraphQL sem campo 'data'.")

        user_data = data.get("user")

        if user_data is None:
            raise core.GraphQLError(f"Usuário '{user}' não encontrado.")

        if not isinstance(user_data, dict):
            raise core.GraphQLError("Campo 'user' inválido na resposta GraphQL.")

        followers, followers_has_next, followers_end_cursor = core._extract_connection(user_data, "followers", include_followers)
        following, following_has_next, following_end_cursor = core._extract_connection(user_data, "following", include_following)
        rate_limit = RateLimitInfo.from_payload(data.get("rateLimit")) or RateLimitInfo.from_headers(response.headers)

        return core.GraphPage(
            followers=followers,
            following=following,
            followers_has_next=followers_has_next,
            following_has_next=following_has_next,
            followers_end_cursor=followers_end_cursor,
            following_end_cursor=following_end_cursor,
            rate_limit=rate_limit,
        )

    except Exception as exc:
        logger.error(f"Erro ao buscar página GraphQL para o usuário '{user}': {exc}")
        raise
