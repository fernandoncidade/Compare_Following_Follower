from __future__ import annotations
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def build_session() -> requests.Session:
    try:
        from source.modules import source as core

        retry = Retry(
            total=4,
            connect=4,
            read=4,
            status=4,
            backoff_factor=0.7,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=frozenset({"POST", "DELETE"}),
            raise_on_status=False,
        )

        adapter = HTTPAdapter(max_retries=retry)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update(core.build_headers())
        session.verify = core.VERIFY_SSL
        return session

    except Exception as exc:
        logger.error(f"Erro ao construir sessão para requisições: {exc}")
