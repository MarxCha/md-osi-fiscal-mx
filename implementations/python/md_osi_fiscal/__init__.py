"""md-osi-fiscal — implementación Python de referencia."""
from .definitions import (
    BaseLegal,
    Domain,
    Regla,
    Termino,
    list_reglas,
    load_domain,
    load_regla,
)

__version__ = "1.0.0rc1"

__all__ = [
    "BaseLegal",
    "Domain",
    "Regla",
    "Termino",
    "list_reglas",
    "load_domain",
    "load_regla",
]
