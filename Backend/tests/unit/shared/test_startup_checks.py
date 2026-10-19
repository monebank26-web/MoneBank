import logging
from unittest.mock import Mock, patch

from app.shared import startup_checks


TABLAS_BASE = list(startup_checks.TABLAS_REQUERIDAS) + ["usuario"]

COLUMNAS_BASE = {"usuario": ["fecha_desbloqueo", "estado"]}

CATEGORIAS_EXISTENTES = {
    ("mesada parental enviada", "GASTO"),
    ("mesada parental recibida", "INGRESO"),
}


class InspectorFalso:

    def __init__(self, tablas, columnas):
        self.tablas = list(tablas)
        self.columnas = columnas

    def get_table_names(self):
        return self.tablas

    def get_columns(self, tabla):
        return [{"name": nombre} for nombre in self.columnas.get(tabla, [])]


def motor_falso(categorias=CATEGORIAS_EXISTENTES):
    motor = Mock()
    conexion = Mock()
    conexion.__enter__ = Mock(return_value=conexion)
    conexion.__exit__ = Mock(return_value=False)
    motor.connect.return_value = conexion

    def ejecutar(sql, parametros=None):
        resultado = Mock()
        clave = (parametros["nombre"], parametros["tipo"])
        resultado.first.return_value = clave if clave in categorias else None
        return resultado

    conexion.execute.side_effect = ejecutar
    return motor


def verificar(tablas=None, columnas=None, categorias=CATEGORIAS_EXISTENTES):
    tablas = TABLAS_BASE if tablas is None else tablas
    columnas = COLUMNAS_BASE if columnas is None else columnas

    inspector = InspectorFalso(tablas, columnas)

    with patch.object(startup_checks, "inspect", return_value=inspector):
        return startup_checks.verificar_esquema(motor_falso(categorias))


def test_esquema_completo_no_genera_advertencias():
    assert verificar() == []


def test_detecta_una_tabla_faltante():
    tablas = [t for t in TABLAS_BASE if t != "registro_accion_admin"]

    advertencias = verificar(tablas=tablas)

    assert any("registro_accion_admin" in a for a in advertencias)


def test_detecta_la_columna_fecha_desbloqueo_faltante():
    advertencias = verificar(columnas={"usuario": ["estado"]})

    assert any("usuario.fecha_desbloqueo" in a for a in advertencias)


def test_detecta_una_categoria_de_sistema_faltante():
    advertencias = verificar(categorias={("mesada parental enviada", "GASTO")})

    assert any("Mesada parental recibida" in a for a in advertencias)
    assert not any("Mesada parental enviada" in a for a in advertencias)


def test_ejecutar_chequeo_de_arranque_loguea_las_advertencias(caplog):
    tablas = [t for t in TABLAS_BASE if t != "modulo_sistema"]
    inspector = InspectorFalso(tablas, COLUMNAS_BASE)

    with caplog.at_level(logging.WARNING, logger="app.shared.startup_checks"):
        with patch.object(startup_checks, "inspect", return_value=inspector):
            advertencias = startup_checks.ejecutar_chequeo_de_arranque(motor_falso())

    assert any("modulo_sistema" in a for a in advertencias)
    assert "Chequeo de arranque" in caplog.text


def test_ejecutar_chequeo_de_arranque_no_propaga_errores(caplog):
    with caplog.at_level(logging.WARNING, logger="app.shared.startup_checks"):
        with patch.object(
            startup_checks,
            "inspect",
            side_effect=RuntimeError("sin base de datos"),
        ):
            advertencias = startup_checks.ejecutar_chequeo_de_arranque(Mock())

    assert advertencias == []
    assert "Chequeo de arranque" in caplog.text
