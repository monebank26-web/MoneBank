from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.ahorro.application.use_cases.actualizar_ahorro import (
    ActualizarAhorroUseCase,
)
from app.shared.exceptions.business_exceptions import PeriodoInvalido


def test_actualizar_limite_rechaza_periodo_fuera_del_catalogo():
    repository = Mock()

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    repository.get_cuenta_por_usuario.return_value = cuenta

    ahorro = Mock()
    ahorro.id_ahorro = 43
    ahorro.id_cuenta = 1
    ahorro.id_tipo_ahorro = 3
    ahorro.periodo = "MENSUAL"
    repository.get_by_id.return_value = ahorro

    tipo_limite = Mock()
    tipo_limite.id_tipo_ahorro = 3
    repository.get_tipo_ahorro.return_value = tipo_limite

    with pytest.raises(PeriodoInvalido):
        ActualizarAhorroUseCase(repository).execute(
            43, {"periodo": "ANUAL"}, 6
        )

    repository.update.assert_not_called()
