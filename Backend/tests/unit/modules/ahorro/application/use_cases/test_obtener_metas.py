from unittest.mock import Mock

import pytest

from app.modules.ahorro.application.use_cases.obtener_metas import ObtenerMetas
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


def test_debe_retornar_las_metas_activas_de_la_cuenta():

    repository = Mock()
    cuenta_repository = Mock()

    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta_repository.get_cuenta_por_usuario.return_value = cuenta

    metas = [
        {"id_ahorro": 46, "nombre": "Viaje", "porcentaje_completado": 50},
        {"id_ahorro": 47, "nombre": "Emergencia", "porcentaje_completado": 10},
    ]
    repository.get_metas_activas.return_value = metas

    resultado = ObtenerMetas(repository, cuenta_repository).execute(6)

    repository.get_metas_activas.assert_called_once_with(1)
    assert resultado == metas


def test_sin_metas_retorna_lista_vacia():

    repository = Mock()
    cuenta_repository = Mock()

    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta_repository.get_cuenta_por_usuario.return_value = cuenta
    repository.get_metas_activas.return_value = []

    resultado = ObtenerMetas(repository, cuenta_repository).execute(6)

    assert resultado == []


def test_sin_cuenta_lanza_cuenta_no_encontrada():

    repository = Mock()
    cuenta_repository = Mock()
    cuenta_repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        ObtenerMetas(repository, cuenta_repository).execute(6)