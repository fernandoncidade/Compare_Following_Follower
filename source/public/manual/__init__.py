try:
    from . import DOC_PT_BR
    from . import DOC_EN_US

except Exception:
    DOC_PT_BR = None
    DOC_EN_US = None

__all__ = ["DOC_PT_BR", "DOC_EN_US"]
