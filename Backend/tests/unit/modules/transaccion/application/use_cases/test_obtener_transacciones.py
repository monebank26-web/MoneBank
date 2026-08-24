from unittest.mock import Mock

import pytest

from app.modules.transaccion.application.use_cases.obtener_transacciones import (
    ObtenerTransaccionesUseCase
)
from app.shared.exceptions.business_exceptions import TransaccionesNoEncontrado


def test_debe_retornar_transacciones_del_usuario():

    repository = Mock()

    transacciones = [
        {'id': 1, 'monto': 50000, 'tipo': 'INGRESO'},
        {'id': 2, 'monto': 20000, 'tipo': 'GASTO'},
    ]

    repository.find_by_usuario.return_value = transacciones

    resultado = ObtenerTransaccionesUseCase(repository).execute(
        6
    )

    repository.find_by_usuario.assert_called_once_with(6)

    assert resultado == transacciones


def test_sin_transacciones_lanza_transacciones_no_encontrado():

    repository = Mock()

    repository.find_by_usuario.return_value = []

    with pytest.raises(TransaccionesNoEncontrado):
        ObtenerTransaccionesUseCase(repository).execute(
            6
        )
