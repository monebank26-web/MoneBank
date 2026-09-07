from unittest.mock import Mock

import pytest

from app.modules.cuenta.application.use_cases.actualizar_cuenta import (
    ActualizarCuentaUseCase
)
from app.shared.exceptions.business_exceptions import (
    CuentaNoEncontrada,
    EstadoInvalido,
)


def test_debe_actualizar_estado_de_la_cuenta():

    repository = Mock()
    repository.get_cuenta_por_id.return_value = Mock()

    actualizada = Mock()
    repository.update.return_value = actualizada

    resultado = ActualizarCuentaUseCase(repository).execute(1, {"estado": "INACTIVA"})

    repository.update.assert_called_once_with(1, {"estado": "INACTIVA"})
    assert resultado == actualizada


def test_estado_invalido_lanza_estado_invalido():

    repository = Mock()
    repository.get_cuenta_por_id.return_value = Mock()

    with pytest.raises(EstadoInvalido):
        ActualizarCuentaUseCase(repository).execute(1, {"estado": "BLOQUEADA"})

    repository.update.assert_not_called()


def test_cuenta_inexistente_lanza_cuenta_no_encontrada():

    repository = Mock()
    repository.get_cuenta_por_id.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        ActualizarCuentaUseCase(repository).execute(999, {"estado": "INACTIVA"})

    repository.update.assert_not_called()