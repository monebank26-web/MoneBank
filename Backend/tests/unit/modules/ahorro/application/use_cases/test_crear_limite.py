from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.ahorro.application.use_cases.crear_limite import CrearLimite
from app.shared.exceptions.business_exceptions import (
    CategoriaNoCompatible,
    CategoriaNoExiste,
    CuentaNoEncontrada,
    MontoInvalido,
    PeriodoInvalido,
    PresupuestoDuplicado,
)


def datos_validos():
    return {
        "nombre": None,
        "monto_limite": Decimal("10000.00"),
        "periodo": "MENSUAL",
        "id_categoria": 8,
    }


def repository_base():
    repository = Mock()
    cuenta_repository = Mock()

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    cuenta_repository.get_cuenta_por_usuario.return_value = cuenta

    categoria = Mock()
    categoria.id_categoria = 8
    categoria.nombre_categoria = "Alimentación"
    categoria.tipo_categoria = "GASTO"
    repository.get_categoria.return_value = categoria

    tipo_limite = Mock()
    tipo_limite.id_tipo_ahorro = 3
    repository.get_tipo_ahorro.return_value = tipo_limite

    repository.get_by_cuenta_y_tipo.return_value = []

    creado = Mock()
    creado.id_ahorro = 99
    repository.create.return_value = creado

    return repository, cuenta_repository


def test_crea_limite_con_nombre_autogenerado():
    repository, cuenta_repository = repository_base()

    resultado = CrearLimite(repository, cuenta_repository).execute(datos_validos(), 6)

    assert resultado.id_ahorro == 99

    data_enviada = repository.create.call_args.args[0]
    assert data_enviada["nombre"] == "Límite Alimentación (MENSUAL)"
    assert data_enviada["monto_objetivo"] == Decimal("10000.00")
    assert data_enviada["saldo_inicial"] == 0
    assert data_enviada["estado"] == "ACTIVO"
    assert data_enviada["fecha_objetivo"] is None
    assert data_enviada["periodo"] == "MENSUAL"
    assert data_enviada["id_tipo_ahorro"] == 3
    assert data_enviada["id_categoria"] == 8
    assert data_enviada["id_cuenta"] == 1


def test_respeta_nombre_personalizado():
    repository, cuenta_repository = repository_base()
    datos = datos_validos()
    datos["nombre"] = "Presupuesto de mercado"

    CrearLimite(repository, cuenta_repository).execute(datos, 6)

    data_enviada = repository.create.call_args.args[0]
    assert data_enviada["nombre"] == "Presupuesto de mercado"


def test_cuenta_no_existe():
    repository, cuenta_repository = repository_base()
    cuenta_repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        CrearLimite(repository, cuenta_repository).execute(datos_validos(), 6)


def test_categoria_no_existe():
    repository, cuenta_repository = repository_base()
    repository.get_categoria.return_value = None

    with pytest.raises(CategoriaNoExiste):
        CrearLimite(repository, cuenta_repository).execute(datos_validos(), 6)


def test_categoria_debe_ser_de_gastos():
    repository, cuenta_repository = repository_base()
    repository.get_categoria.return_value.tipo_categoria = "AHORRO"

    with pytest.raises(CategoriaNoCompatible):
        CrearLimite(repository, cuenta_repository).execute(datos_validos(), 6)


def test_monto_debe_ser_positivo():
    repository, cuenta_repository = repository_base()
    datos = datos_validos()
    datos["monto_limite"] = Decimal("0")

    with pytest.raises(MontoInvalido):
        CrearLimite(repository, cuenta_repository).execute(datos, 6)


def test_periodo_invalido_fuera_del_catalogo():
    repository, cuenta_repository = repository_base()
    datos = datos_validos()
    datos["periodo"] = "ANUAL"

    with pytest.raises(PeriodoInvalido):
        CrearLimite(repository, cuenta_repository).execute(datos, 6)


def test_rechaza_duplicado_misma_categoria_y_periodo_activos():
    repository, cuenta_repository = repository_base()

    existente = Mock()
    existente.id_categoria = 8
    existente.periodo = "MENSUAL"
    existente.estado = "ACTIVO"
    repository.get_by_cuenta_y_tipo.return_value = [existente]

    with pytest.raises(PresupuestoDuplicado):
        CrearLimite(repository, cuenta_repository).execute(datos_validos(), 6)


def test_permite_mismo_periodo_en_distinta_categoria():
    repository, cuenta_repository = repository_base()

    existente = Mock()
    existente.id_categoria = 12
    existente.periodo = "MENSUAL"
    existente.estado = "ACTIVO"
    repository.get_by_cuenta_y_tipo.return_value = [existente]

    resultado = CrearLimite(repository, cuenta_repository).execute(datos_validos(), 6)

    assert resultado.id_ahorro == 99


def test_permite_duplicado_si_el_anterior_no_esta_activo():
    repository, cuenta_repository = repository_base()

    pausado = Mock()
    pausado.id_categoria = 8
    pausado.periodo = "MENSUAL"
    pausado.estado = "PAUSADO"
    repository.get_by_cuenta_y_tipo.return_value = [pausado]

    resultado = CrearLimite(repository, cuenta_repository).execute(datos_validos(), 6)

    assert resultado.id_ahorro == 99