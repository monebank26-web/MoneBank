from unittest.mock import Mock

import pytest

from app.modules.cuenta.application.use_cases.eliminar_cuenta import (
    EliminarCuentaUseCase
)
from app.shared.exceptions.transaccion_errors import (
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
)


def test_debe_eliminar_la_cuenta():

    repository = Mock()

    cuenta = Mock()
    cuenta.id_usuario = 3
    repository.get_cuenta_por_id.return_value = cuenta

    repository.delete.return_value = {"mensaje": "Cuenta eliminada"}

    resultado = EliminarCuentaUseCase(repository).execute(1, 3, False)

    repository.delete.assert_called_once_with(1)
    assert resultado == {"mensaje": "Cuenta eliminada"}


def test_cuenta_inexistente_lanza_cuenta_no_encontrada():

    repository = Mock()
    repository.get_cuenta_por_id.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        EliminarCuentaUseCase(repository).execute(999, 3, False)

    repository.delete.assert_not_called()


def test_cuenta_de_otro_usuario_lanza_no_pertenece():

    repository = Mock()

    cuenta = Mock()
    cuenta.id_usuario = 3
    repository.get_cuenta_por_id.return_value = cuenta

    with pytest.raises(CuentaNoPerteneceAlUsuario):
        EliminarCuentaUseCase(repository).execute(1, 99, False)

    repository.delete.assert_not_called()


def test_admin_puede_eliminar_cuenta_de_otro_usuario():

    repository = Mock()

    cuenta = Mock()
    cuenta.id_usuario = 3
    repository.get_cuenta_por_id.return_value = cuenta

    repository.delete.return_value = {"mensaje": "Cuenta eliminada"}

    resultado = EliminarCuentaUseCase(repository).execute(1, 99, True)

    repository.delete.assert_called_once_with(1)
    assert resultado == {"mensaje": "Cuenta eliminada"}
