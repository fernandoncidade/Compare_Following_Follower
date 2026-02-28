from __future__ import annotations
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _render_counts_label(self) -> None:
    try:
        following_value = "-" if self._counts_following is None else str(self._counts_following)
        followers_value = "-" if self._counts_followers is None else str(self._counts_followers)
        non_following_value = "-" if self._counts_non_following is None else str(self._counts_non_following)
        mutuals_value = "-" if self._counts_mutuals is None else str(self._counts_mutuals)
        no_longer_follow_me_value = ("-" if self._counts_no_longer_follow_me is None else str(self._counts_no_longer_follow_me))
        self.counts_label.setText(self._tr("Seguidores = {followers}; Sigo = {following}; Não sigo = {non_following}; Mútuos = {mutuals}; Não me seguem mais = {no_longer_follow_me}").format(
            followers=followers_value, following=following_value, non_following=non_following_value, mutuals=mutuals_value, no_longer_follow_me=no_longer_follow_me_value,))

    except Exception as exc:
        logger.error(f"Erro ao renderizar rótulo de contagens: {exc}")
