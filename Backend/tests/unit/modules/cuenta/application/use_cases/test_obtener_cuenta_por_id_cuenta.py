from unittest.mock import Mock

import pytest

from app.modules.cuenta.application.use_cases.obtener_cuenta_por_id_cuenta import (
    ObtenerCuentaPorIdUseCase
)
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


def test_debe_obtener_cuenta_por_id_cuenta():

    repository = Mock()

    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta.saldo = 150000
    cuenta.id_usuario = 3

    repository.get_cuenta_por_id.return_value = cuenta

    resultado = ObtenerCuentaPorIdUseCase(repository).execute(1)

    repository.get_cuenta_por_id.assert_called_once_with(1)
    assert resultado == cuenta


def test_cuenta_inexistente_lanza_cuenta_no_encontrada():

    repository = Mock()
    repository.get_cuenta_por_id.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        ObtenerCuentaPorIdUseCase(repository).execute(999)