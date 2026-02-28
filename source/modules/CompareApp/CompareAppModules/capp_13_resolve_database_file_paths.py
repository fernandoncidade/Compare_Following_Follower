from __future__ import annotations
from pathlib import Path
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _resolve_database_file_paths(self) -> tuple[Path, Path]:
    try:
        from source.modules import source as core

        state_file = Path(core.NON_FOLLOWERS_STATE_FILE)
        cache_file = Path(core.CACHE_FILE)
        return state_file, cache_file

    except Exception as exc:
        logger.error(f"Erro ao resolver caminhos de cache/estado para reset de token: {exc}")
        base = Path.home() / "AppData" / "Local" / "FollowingFollower"
        return (
            base / ".github_follow_compare_antigo.json",
            base / ".github_follow_compare_atual.json",
        )
