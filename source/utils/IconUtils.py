import os
import sys
from functools import lru_cache
import unicodedata
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

@lru_cache(maxsize=1)
def get_app_base_path():
    try:
        if getattr(sys, 'frozen', False):
            if hasattr(sys, '_MEIPASS'):
                base = sys._MEIPASS
                logger.debug(f"Executando como PyInstaller: {base}")
                return base

            else:
                exe_dir = os.path.dirname(sys.executable)
                logger.debug(f"Executando como executável: {exe_dir}")
                return exe_dir

        else:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            logger.debug(f"Executando em modo desenvolvimento: {base}")
            return base

    except Exception as e:
        logger.error(f"Erro ao obter caminho base do app: {e}", exc_info=True)
        return None

@lru_cache(maxsize=512)
def get_icon_path(icon_name):
    try:
        base_path = get_app_base_path()
        if not base_path:
            logger.error("Caminho base não encontrado")
            return None

        if not os.path.splitext(icon_name)[1]:
            extensions = ['.png', '.ico', '.svg', '.jpg']

        else:
            extensions = ['']

        possible_paths = []
        for ext in extensions:
            icon_with_ext = icon_name + ext if ext else icon_name
            possible_paths.extend([
                os.path.join(base_path, "assets", "icons", icon_with_ext),
                os.path.join(base_path, "source", "assets", "icons", icon_with_ext),
                os.path.join(base_path, "icons", icon_with_ext),
                os.path.join(base_path, "_internal", "icons", icon_with_ext),
                os.path.join(os.path.dirname(__file__), "..", "assets", "icons", icon_with_ext)
            ])

        for icon_path in possible_paths:
            icon_path = os.path.abspath(icon_path)
            if os.path.exists(icon_path):
                file_size = os.path.getsize(icon_path)
                logger.debug(f"✓ Ícone encontrado: {icon_path} ({file_size} bytes)")
                return icon_path

        try:
            def _normalize(s: str) -> str:
                if s is None:
                    return ''

                s = s.lower()
                s = unicodedata.normalize('NFKD', s)
                return ''.join(ch for ch in s if not unicodedata.combining(ch))

            search_dirs = list({
                os.path.join(base_path, "assets", "icons"),
                os.path.join(base_path, "source", "assets", "icons"),
                os.path.join(base_path, "icons"),
                os.path.join(base_path, "_internal", "icons"),
                os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "icons"))
            })

            norm_name = _normalize(icon_name)
            logger.debug(f"Procurando fallback para ícone '{icon_name}' nos diretórios: {search_dirs}")

            for d in search_dirs:
                try:
                    if not os.path.isdir(d):
                        continue

                    for root, _, files in os.walk(d):
                        for f in files:
                            stem, _ = os.path.splitext(f)
                            if norm_name in _normalize(stem) or _normalize(stem) in norm_name:
                                candidate = os.path.abspath(os.path.join(root, f))
                                file_size = os.path.getsize(candidate)
                                logger.warning(f"¡ Ícone aproximado encontrado para '{icon_name}': {candidate} ({file_size} bytes)")
                                return candidate

                except Exception:
                    continue

        except Exception as e:
            logger.error(f"Erro no fallback de busca de ícone '{icon_name}': {e}", exc_info=True)

        logger.error(f"✗ Ícone '{icon_name}' NÃO encontrado em nenhum dos {len(possible_paths)} caminhos e no fallback")

        try:
            placeholder_dir = os.path.join(base_path, "assets", "icons")
            os.makedirs(placeholder_dir, exist_ok=True)
            placeholder_file = os.path.join(placeholder_dir, f"missing_icon_{norm_name}.svg")
            if not os.path.exists(placeholder_file):
                svg_content = (
                    '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64">'
                    '<rect width="100%" height="100%" fill="transparent"/>'
                    f'<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" '
                    'font-size="10" fill="#888">' + str(icon_name) + '</text></svg>'
                )
                with open(placeholder_file, 'w', encoding='utf-8') as fh:
                    fh.write(svg_content)

            logger.warning(f"Retornando placeholder para ícone '{icon_name}': {placeholder_file}")
            return os.path.abspath(placeholder_file)

        except Exception as e:
            logger.error(f"Falha ao criar placeholder para ícone '{icon_name}': {e}", exc_info=True)
            return None

    except Exception as e:
        logger.error(f"Erro ao obter caminho do ícone '{icon_name}': {e}", exc_info=True)
        return None
