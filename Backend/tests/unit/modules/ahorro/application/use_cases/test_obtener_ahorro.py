from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.ahorro.application.use_cases.actualizar_ahorro import (
    ActualizarAhorroUseCase
)
from app.modules.ahorro.application.use_cases.eliminar_ahorro import (
    EliminarAhorroUseCase
)
from app.modules.ahorro.application.use_cases.obtener_ahorro import (
    ObtenerAhorrosUseCase
)
from app.modules.ahorro.application.use_cases.obtener_ahorro_por_id import (
    ObtenerAhorroPorIdUseCase
)
from app.shared.exceptions.business_exceptions import (
    AhorroNoEncontrado,
    EstadoInvalido,
    PresupuestoDuplicado,
)


def cuenta_repository_con(cuenta):
    cuenta_repository = Mock()
    cuenta_repository.get_cuenta_por_usuario.return_value = cuenta
    return cuenta_repository


def repository_actualizar_mock():
    repository = Mock()

    cuenta = Mock()
    cuenta.id_cuenta = 1

    ahorro = Mock()
    ahorro.id_ahorro = 5
    ahorro.id_cuenta = 1
    ahorro.id_categoria = 8
    ahorro.periodo = "SEMANAL"
    repository.get_by_id.return_value = ahorro

    tipo_limite = Mock()
    tipo_limite.id_tipo_ahorro = 3
    repository.get_tipo_ahorro.return_value = tipo_limite

    return repository, cuenta_repository_con(cuenta)


def test_listar_devuelve_solo_los_ahorros_de_la_cuenta_del_usuario():

    repository = Mock()
    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta_repository = cuenta_repository_con(cuenta)
    repository.get_by_cuenta.return_value = [Mock(), Mock()]

    resultado = ObtenerAhorrosUseCase(repository, cuenta_repository).execute(12)

    repository.get_by_cuenta.assert_called_once_with(1)
    assert len(resultado) == 2


def test_obtener_ahorro_ajeno_lanza_ahorro_no_encontrado():

    repository = Mock()
    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta_repository = cuenta_repository_con(cuenta)
    repository.get_by_id.return_value.id_cuenta = 2

    with pytest.raises(AhorroNoEncontrado):
        ObtenerAhorroPorIdUseCase(repository, cuenta_repository).execute(5, 12)


def test_actualizar_ignora_campos_fuera_de_la_whitelist():

    repository, cuenta_repository = repository_actualizar_mock()
    datos = {
        "nombre": "Presupuesto alimentacion",
        "estado": "PAUSADO",
        "id_cuenta": 99,
        "id_tipo_ahorro": 3,
        "id_categoria": 8,
        "saldo_actual": Decimal("999.99"),
        "saldo_inicial": Decimal("50.00"),
        "ahorro_automatico": True,
    }

    ActualizarAhorroUseCase(repository, cuenta_repository).execute(5, datos, 12)

    data_enviada = repository.update.call_args.args[1]
    assert set(data_enviada.keys()) == {"nombre", "estado"}


def test_actualizar_estado_invalido_lanza_estado_invalido():

    repository, cuenta_repository = repository_actualizar_mock()
    datos = {"nombre": "X", "estado": "CULMINADO"}

    with pytest.raises(EstadoInvalido):
        ActualizarAhorroUseCase(repository, cuenta_repository).execute(5, datos, 12)

    repository.update.assert_not_called()


def test_actualizar_limite_a_periodo_duplicado_lanza_presupuesto_duplicado():

    repository, cuenta_repository = repository_actualizar_mock()
    repository.get_by_id.return_value.id_tipo_ahorro = 3

    otro_limite = Mock()
    otro_limite.id_ahorro = 9
    otro_limite.id_categoria = 8
    otro_limite.periodo = "MENSUAL"
    otro_limite.estado = "ACTIVO"
    repository.get_by_cuenta_y_tipo.return_value = [otro_limite]

    with pytest.raises(PresupuestoDuplicado):
        ActualizarAhorroUseCase(repository, cuenta_repository).execute(
            5, {"periodo": "MENSUAL"}, 12
        )

    repository.update.assert_not_called()


def test_eliminar_ahorro_ajeno_lanza_ahorro_no_encontrado():

    repository = Mock()
    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta_repository = cuenta_repository_con(cuenta)
    repository.get_by_id.return_value.id_cuenta = 2

    with pytest.raises(AhorroNoEncontrado):
        EliminarAhorroUseCase(repository, cuenta_repository).execute(5, 12)

    repository.delete.assert_not_called()