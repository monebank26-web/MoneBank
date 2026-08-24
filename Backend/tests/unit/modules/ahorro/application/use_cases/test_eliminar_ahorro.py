from unittest.mock import Mock

import pytest

from app.modules.ahorro.application.use_cases.eliminar_ahorro import (
    EliminarAhorroUseCase
)
from app.shared.exceptions.business_exceptions import (
    AhorroNoEncontrado,
    CuentaNoEncontrada,
)


def repository_mock():
    repository = Mock()

    cuenta = Mock()
    cuenta.id_cuenta = 1
    repository.get_cuenta_por_usuario.return_value = cuenta

    ahorro = Mock()
    ahorro.id_cuenta = 1
    repository.get_by_id.return_value = ahorro

    repository.delete.return_value = {"mensaje": "Ahorro eliminado"}

    return repository


def test_debe_eliminar_un_ahorro_propio():

    repository = repository_mock()

    resultado = EliminarAhorroUseCase(repository).execute(5, 12)

    repository.delete.assert_called_once_with(5)
    assert resultado == {"mensaje": "Ahorro eliminado"}


def test_sin_cuenta_lanza_cuenta_no_encontrada():

    repository = repository_mock()
    repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        EliminarAhorroUseCase(repository).execute(5, 12)

    repository.delete.assert_not_called()


def test_ahorro_ajeno_lanza_ahorro_no_encontrado():

    repository = repository_mock()
    repository.get_by_id.return_value.id_cuenta = 2

    with pytest.raises(AhorroNoEncontrado):
        EliminarAhorroUseCase(repository).execute(5, 12)

    repository.delete.assert_not_called()


def test_ahorro_inexistente_lanza_ahorro_no_encontrado():

    repository = repository_mock()
    repository.get_by_id.return_value = None

    with pytest.raises(AhorroNoEncontrado):
        EliminarAhorroUseCase(repository).execute(999, 12)

    repository.delete.assert_not_called()
