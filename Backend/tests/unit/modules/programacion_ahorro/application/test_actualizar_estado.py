from unittest.mock import Mock

import pytest

from app.modules.programacion_ahorro.application.actualizar_estado import ActualizarEstadoUseCase
from app.shared.exceptions.business_exceptions import (
    CuentaNoEncontrada,
    EstadoInvalido,
    ProgramacionNoEncontrada,
)


def mocks_con_cuenta():
    repository = Mock()
    cuenta_repository = Mock()

    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta_repository.get_cuenta_por_usuario.return_value = cuenta

    return repository, cuenta_repository


def test_debe_actualizar_estado_correctamente():

    repository, cuenta_repository = mocks_con_cuenta()

    actualizada = Mock()
    actualizada.id_programacion_ahorro = 10
    actualizada.estado = "PAUSADA"
    repository.update_estado.return_value = actualizada

    resultado = ActualizarEstadoUseCase(repository, cuenta_repository).execute(
        6, 10, "PAUSADA"
    )

    cuenta_repository.get_cuenta_por_usuario.assert_called_once_with(6)
    repository.update_estado.assert_called_once_with(10, "PAUSADA")
    assert resultado == actualizada


def test_sin_cuenta_lanza_cuenta_no_encontrada():

    repository, cuenta_repository = mocks_con_cuenta()
    cuenta_repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        ActualizarEstadoUseCase(repository, cuenta_repository).execute(
            6, 10, "PAUSADA"
        )

    repository.update_estado.assert_not_called()


def test_estado_invalido_lanza_estado_invalido():

    repository, cuenta_repository = mocks_con_cuenta()

    with pytest.raises(EstadoInvalido):
        ActualizarEstadoUseCase(repository, cuenta_repository).execute(
            6, 10, "INEXISTENTE"
        )

    repository.update_estado.assert_not_called()


def test_programacion_inexistente_lanza_programacion_no_encontrada():

    repository, cuenta_repository = mocks_con_cuenta()
    repository.update_estado.return_value = None

    with pytest.raises(ProgramacionNoEncontrada):
        ActualizarEstadoUseCase(repository, cuenta_repository).execute(
            6, 10, "PAUSADA"
        )