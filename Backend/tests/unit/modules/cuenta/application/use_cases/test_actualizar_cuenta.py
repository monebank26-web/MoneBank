from unittest.mock import Mock

import pytest

from app.modules.cuenta.application.use_cases.actualizar_cuenta import (
    ActualizarCuentaUseCase
)
from app.shared.exceptions.ahorro_errors import EstadoInvalido
from app.shared.exceptions.transaccion_errors import (
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
)


def test_debe_actualizar_estado_de_la_cuenta():

    repository = Mock()

    cuenta = Mock()
    cuenta.id_usuario = 3
    repository.get_cuenta_por_id.return_value = cuenta

    actualizada = Mock()
    repository.update.return_value = actualizada

    resultado = ActualizarCuentaUseCase(repository).execute(
        1, {"estado": "INACTIVA"}, 3, False
    )

    repository.update.assert_called_once_with(1, {"estado": "INACTIVA"})
    assert resultado == actualizada


def test_estado_invalido_lanza_estado_invalido():

    repository = Mock()

    cuenta = Mock()
    cuenta.id_usuario = 3
    repository.get_cuenta_por_id.return_value = cuenta

    with pytest.raises(EstadoInvalido):
        ActualizarCuentaUseCase(repository).execute(
            1, {"estado": "BLOQUEADA"}, 3, False
        )

    repository.update.assert_not_called()


def test_cuenta_inexistente_lanza_cuenta_no_encontrada():

    repository = Mock()
    repository.get_cuenta_por_id.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        ActualizarCuentaUseCase(repository).execute(
            999, {"estado": "INACTIVA"}, 3, False
        )

    repository.update.assert_not_called()


def test_cuenta_de_otro_usuario_lanza_no_pertenece():

    repository = Mock()

    cuenta = Mock()
    cuenta.id_usuario = 3
    repository.get_cuenta_por_id.return_value = cuenta

    with pytest.raises(CuentaNoPerteneceAlUsuario):
        ActualizarCuentaUseCase(repository).execute(
            1, {"estado": "INACTIVA"}, 99, False
        )

    repository.update.assert_not_called()


def test_admin_puede_actualizar_cuenta_de_otro_usuario():

    repository = Mock()

    cuenta = Mock()
    cuenta.id_usuario = 3
    repository.get_cuenta_por_id.return_value = cuenta

    actualizada = Mock()
    repository.update.return_value = actualizada

    resultado = ActualizarCuentaUseCase(repository).execute(
        1, {"estado": "INACTIVA"}, 99, True
    )

    repository.update.assert_called_once_with(1, {"estado": "INACTIVA"})
    assert resultado == actualizada
