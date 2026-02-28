from .ApplicationPathUtils import get_app_base_path, get_text_file_path, load_text_file
from .CaminhoPersistenteUtils import obter_caminho_persistente
from .IconUtils import get_icon_path
from .LogManager import LogManager

__all__ = [
    "GerenciadorBotoesUI",
    "LogManager",
    "get_app_base_path",
    "get_icon_path",
    "get_text_file_path",
    "load_text_file",
    "obter_caminho_persistente",
]


def __getattr__(name: str):
    if name == "GerenciadorBotoesUI":
        from .GerenciadorBotoesUI import GerenciadorBotoesUI
        return GerenciadorBotoesUI

    raise AttributeError(f"module 'source.utils' has no attribute '{name}'")
