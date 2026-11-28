from unittest.mock import Mock

import pytest

from app.modules.programacion_ahorro.application.actualizar_estado import ActualizarEstadoUseCase
from app.shared.exceptions.ahorro_errors import (
    EstadoInvalido,
    ProgramacionNoEncontrada,
)
from app.shared.exceptions.common import CuentaNoEncontrada


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


def test_debe_actualizar_estado_correctamente():

    repository, cuenta_repository, ahorro_repository, _ = mocks_con_programacion()

    actualizada = Mock()
    actualizada.id_programacion_ahorro = 10
    actualizada.estado = "PAUSADA"
    repository.update_estado.return_value = actualizada

    resultado = ActualizarEstadoUseCase(
        repository,
        cuenta_repository,
        ahorro_repository,
    ).execute(6, 10, "PAUSADA")

    cuenta_repository.get_cuenta_por_usuario.assert_called_once_with(6)
    repository.get_by_id.assert_called_once_with(10)
    ahorro_repository.get_by_id.assert_called_once_with(5)
    repository.update_estado.assert_called_once_with(10, "PAUSADA")
    assert resultado == actualizada


def test_sin_cuenta_lanza_cuenta_no_encontrada():

    repository, cuenta_repository, ahorro_repository, _ = mocks_con_programacion()
    cuenta_repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        ActualizarEstadoUseCase(
            repository,
            cuenta_repository,
            ahorro_repository,
        ).execute(6, 10, "PAUSADA")

    repository.update_estado.assert_not_called()


def test_estado_invalido_lanza_estado_invalido():

    repository, cuenta_repository, ahorro_repository, _ = mocks_con_programacion()

    with pytest.raises(EstadoInvalido):
        ActualizarEstadoUseCase(
            repository,
            cuenta_repository,
            ahorro_repository,
        ).execute(6, 10, "INEXISTENTE")

    repository.update_estado.assert_not_called()


def test_programacion_inexistente_lanza_programacion_no_encontrada():

    repository, cuenta_repository, ahorro_repository, _ = mocks_con_programacion()
    repository.get_by_id.return_value = None

    with pytest.raises(ProgramacionNoEncontrada):
        ActualizarEstadoUseCase(
            repository,
            cuenta_repository,
            ahorro_repository,
        ).execute(6, 10, "PAUSADA")

    repository.update_estado.assert_not_called()


def test_programacion_de_otro_usuario_lanza_programacion_no_encontrada():

    repository, cuenta_repository, ahorro_repository, _ = mocks_con_programacion()
    ahorro_repository.get_by_id.return_value = Mock(id_cuenta=99)

    with pytest.raises(ProgramacionNoEncontrada):
        ActualizarEstadoUseCase(
            repository,
            cuenta_repository,
            ahorro_repository,
        ).execute(6, 10, "PAUSADA")

    repository.update_estado.assert_not_called()


def test_update_devuelve_none_lanza_programacion_no_encontrada():

    repository, cuenta_repository, ahorro_repository, _ = mocks_con_programacion()
    repository.update_estado.return_value = None

    with pytest.raises(ProgramacionNoEncontrada):
        ActualizarEstadoUseCase(
            repository,
            cuenta_repository,
            ahorro_repository,
        ).execute(6, 10, "PAUSADA")
