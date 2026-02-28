from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _format_rate_limit_reset(reset_value: str | None) -> str | None:
    try:
        if not reset_value:
            return None

        try:
            ts = int(reset_value)

        except ValueError:
            return None

        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    except Exception as exc:
        logger.error(f"Erro ao formatar reset do rate limit: {exc}")


@dataclass
class RateLimitInfo:
    remaining: int | None = None
    limit: int | None = None
    cost: int | None = None
    reset_at: str | None = None

    @staticmethod
    def _to_int(value: Any) -> int | None:
        try:
            if isinstance(value, int):
                return value

            if isinstance(value, str):
                try:
                    return int(value)

                except ValueError:
                    return None

            return None

        except Exception as exc:
            logger.error(f"Erro ao converter valor para int: {exc}")

    @classmethod
    def from_payload(cls, payload: Any) -> "RateLimitInfo | None":
        try:
            if not isinstance(payload, dict):
                return None

            info = cls(
                remaining=cls._to_int(payload.get("remaining")),
                limit=cls._to_int(payload.get("limit")),
                cost=cls._to_int(payload.get("cost")),
                reset_at=payload.get("resetAt") if isinstance(payload.get("resetAt"), str) else None,
            )

            if info.remaining is None and info.limit is None and info.cost is None and info.reset_at is None:
                return None

            return info

        except Exception as exc:
            logger.error(f"Erro ao criar RateLimitInfo a partir do payload: {exc}")

    @classmethod
    def from_headers(cls, headers: Mapping[str, str]) -> "RateLimitInfo | None":
        try:
            info = cls(
                remaining=cls._to_int(headers.get("X-RateLimit-Remaining")),
                limit=cls._to_int(headers.get("X-RateLimit-Limit")),
                reset_at=_format_rate_limit_reset(headers.get("X-RateLimit-Reset")),
            )

            if info.remaining is None and info.limit is None and info.reset_at is None:
                return None

            return info

        except Exception as exc:
            logger.error(f"Erro ao criar RateLimitInfo a partir dos headers: {exc}")
