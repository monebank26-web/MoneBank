import logging

from sqlalchemy import inspect, text

from app.core.database.connection import engine

logger = logging.getLogger(__name__)

TABLAS_REQUERIDAS = (
    "registro_accion_admin",
    "modulo_sistema",
    "limite_financiero_global",
    "registro_error",
    "mensaje_informativo",
)

COLUMNAS_REQUERIDAS = {
    "usuario": ("fecha_desbloqueo",),
}

CATEGORIAS_SISTEMA = (
    ("Mesada parental enviada", "GASTO"),
    ("Mesada parental recibida", "INGRESO"),
)


def verificar_esquema(motor=None) -> list:
    motor = motor or engine
    advertencias = []

    inspector = inspect(motor)
    tablas = set(inspector.get_table_names())

    for tabla in TABLAS_REQUERIDAS:
        if tabla not in tablas:
            advertencias.append(f"falta la tabla '{tabla}'")

    for tabla, columnas in COLUMNAS_REQUERIDAS.items():
        if tabla not in tablas:
            continue

        existentes = {
            columna["name"] for columna in inspector.get_columns(tabla)
        }

        for columna in columnas:
            if columna not in existentes:
                advertencias.append(f"falta la columna '{tabla}.{columna}'")

    advertencias.extend(_verificar_categorias_sistema(motor))

    return advertencias


def _verificar_categorias_sistema(motor) -> list:
    advertencias = []

    try:
        with motor.connect() as conexion:
            for nombre, tipo in CATEGORIAS_SISTEMA:
                existe = conexion.execute(
                    text(
                        "SELECT 1 FROM categoria "
                        "WHERE lower(trim(nombre_categoria)) = :nombre "
                        "AND upper(tipo_categoria) = :tipo "
                        "LIMIT 1"
                    ),
                    {"nombre": nombre.strip().lower(), "tipo": tipo.upper()},
                ).first()

                if not existe:
                    advertencias.append(
                        f"falta la categoría de sistema '{nombre}' ({tipo})"
                    )
    except Exception as error:
        advertencias.append(
            f"no se pudieron verificar las categorías de sistema: {error}"
        )

    return advertencias


def ejecutar_chequeo_de_arranque(motor=None) -> list:
    try:
        advertencias = verificar_esquema(motor)
    except Exception as error:
        logger.warning(
            "Chequeo de arranque: no se pudo completar: %s",
            error,
        )
        return []

    for advertencia in advertencias:
        logger.warning("Chequeo de arranque: %s", advertencia)

    return advertencias
