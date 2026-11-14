from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.programacion_ahorro.application.modificar_programacion import ModificarProgramacion
from app.shared.exceptions.ahorro_errors import (
    FrecuenciaInvalida,
    ProgramacionFinalizada,
    ProgramacionNoEncontrada,
)
from app.shared.exceptions.common import CuentaNoEncontrada, MontoInvalido


def mocks_con_programacion():
    repository = Mock()
    cuenta_repository = Mock()
    ahorro_repository = Mock()

    cuenta_repository.get_cuenta_por_usuario.return_value = Mock(id_cuenta=1)

    programacion = Mock()
    programacion.id_programacion_ahorro = 10
    programacion.id_ahorro = 5
    programacion.estado = "ACTIVA"
    repository.get_by_id.return_value = programacion

    ahorro_repository.get_by_id.return_value = Mock(id_cuenta=1)

    return repository, cuenta_repository, ahorro_repository, programacion


def test_debe_modificar_monto_y_frecuencia():

    repository, cuenta_repository, ahorro_repository, _ = mocks_con_programacion()
    actualizada = Mock()
    repository.update_periodicidad.return_value = actualizada

    resultado = ModificarProgramacion(
        repository,
        cuenta_repository,
        ahorro_repository,
    ).execute(6, 10, Decimal("75000"), "SEMANAL")

    repository.get_by_id.assert_called_once_with(10)
    ahorro_repository.get_by_id.assert_called_once_with(5)
    repository.update_periodicidad.assert_called_once_with(
        10,
        Decimal("75000"),
        "SEMANAL",
    )
    assert resultado == actualizada


def test_sin_cuenta_lanza_cuenta_no_encontrada():

    repository, cuenta_repository, ahorro_repository, _ = mocks_con_programacion()
    cuenta_repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        ModificarProgramacion(
            repository,
            cuenta_repository,
            ahorro_repository,
        ).execute(6, 10, Decimal("1000"), "MENSUAL")

    repository.update_periodicidad.assert_not_called()


def test_programacion_inexistente_lanza_programacion_no_encontrada():

    repository, cuenta_repository, ahorro_repository, _ = mocks_con_programacion()
    repository.get_by_id.return_value = None

    with pytest.raises(ProgramacionNoEncontrada):
        ModificarProgramacion(
            repository,
            cuenta_repository,
            ahorro_repository,
        ).execute(6, 10, Decimal("1000"), "MENSUAL")

    repository.update_periodicidad.assert_not_called()


def test_programacion_de_otro_usuario_lanza_programacion_no_encontrada():

    repository, cuenta_repository, ahorro_repository, _ = mocks_con_programacion()
    ahorro_repository.get_by_id.return_value = Mock(id_cuenta=99)

    with pytest.raises(ProgramacionNoEncontrada):
        ModificarProgramacion(
            repository,
            cuenta_repository,
            ahorro_repository,
        ).execute(6, 10, Decimal("1000"), "MENSUAL")

    repository.update_periodicidad.assert_not_called()


def test_programacion_finalizada_no_se_puede_modificar():

    repository, cuenta_repository, ahorro_repository, programacion = mocks_con_programacion()
    programacion.estado = "FINALIZADA"

    with pytest.raises(ProgramacionFinalizada):
        ModificarProgramacion(
            repository,
            cuenta_repository,
            ahorro_repository,
        ).execute(6, 10, Decimal("1000"), "MENSUAL")

    repository.update_periodicidad.assert_not_called()


def test_frecuencia_invalida_lanza_frecuencia_invalida():

    repository, cuenta_repository, ahorro_repository, _ = mocks_con_programacion()

    with pytest.raises(FrecuenciaInvalida):
        ModificarProgramacion(
            repository,
            cuenta_repository,
            ahorro_repository,
        ).execute(6, 10, Decimal("1000"), "CADA_RATO")

    repository.update_periodicidad.assert_not_called()


def test_monto_invalido_lanza_monto_invalido():

    repository, cuenta_repository, ahorro_repository, _ = mocks_con_programacion()

    with pytest.raises(MontoInvalido):
        ModificarProgramacion(
            repository,
            cuenta_repository,
            ahorro_repository,
        ).execute(6, 10, Decimal("0"), "MENSUAL")

    repository.update_periodicidad.assert_not_called()


def test_update_devuelve_none_lanza_programacion_no_encontrada():

    repository, cuenta_repository, ahorro_repository, _ = mocks_con_programacion()
    repository.update_periodicidad.return_value = None

    with pytest.raises(ProgramacionNoEncontrada):
        ModificarProgramacion(
            repository,
            cuenta_repository,
            ahorro_repository,
        ).execute(6, 10, Decimal("1000"), "MENSUAL")
