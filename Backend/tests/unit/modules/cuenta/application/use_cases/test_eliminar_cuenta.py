from unittest.mock import Mock

import pytest

from app.modules.cuenta.application.use_cases.eliminar_cuenta import (
    EliminarCuentaUseCase
)
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


def test_debe_eliminar_la_cuenta():

    repository = Mock()
    repository.get_cuenta_por_id.return_value = Mock()
    repository.delete.return_value = {"mensaje": "Cuenta eliminada"}

    resultado = EliminarCuentaUseCase(repository).execute(1)

    repository.delete.assert_called_once_with(1)
    assert resultado == {"mensaje": "Cuenta eliminada"}


def test_cuenta_inexistente_lanza_cuenta_no_encontrada():

    repository = Mock()
    repository.get_cuenta_por_id.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        EliminarCuentaUseCase(repository).execute(999)

    repository.delete.assert_not_called()