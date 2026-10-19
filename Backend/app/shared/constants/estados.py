ESTADO_ACTIVO = "ACTIVO"
ESTADO_INACTIVO = "INACTIVO"
ESTADO_BLOQUEADO = "BLOQUEADO"

ESTADOS_USUARIO = (
    ESTADO_ACTIVO,
    ESTADO_INACTIVO,
    ESTADO_BLOQUEADO,
)

# Patrón para validar el estado que llega como filtro en la URL.
PATRON_ESTADO_USUARIO = "^(" + "|".join(ESTADOS_USUARIO) + ")$"


def normalizar_estado(estado) -> str:
    """Devuelve el estado en mayúsculas y sin espacios sobrantes."""
    return str(estado or "").strip().upper()


def es_bloqueado(estado) -> bool:
    return normalizar_estado(estado) == ESTADO_BLOQUEADO


def es_inactivo(estado) -> bool:
    return normalizar_estado(estado) == ESTADO_INACTIVO
