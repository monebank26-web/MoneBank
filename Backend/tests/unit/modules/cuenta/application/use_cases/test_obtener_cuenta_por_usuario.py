from unittest.mock import Mock

import pytest

from app.modules.cuenta.application.use_cases.obtener_cuenta_por_usuario import (
    ObtenerCuentaPorUsuarioUseCase
)
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


def test_debe_obtener_la_cuenta_del_usuario():

    repository = Mock()

    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta.saldo = 150000
    cuenta.id_usuario = 3

    repository.get_cuenta_por_usuario.return_value = cuenta

    use_case = ObtenerCuentaPorUsuarioUseCase(repository)

    resultado = use_case.execute(3)

    repository.get_cuenta_por_usuario.assert_called_once_with(3)

    assert resultado == cuenta


def test_sin_cuenta_lanza_cuenta_no_encontrada():

    repository = Mock()
    repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        ObtenerCuentaPorUsuarioUseCase(repository).execute(3)