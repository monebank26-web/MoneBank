from unittest.mock import Mock

from app.modules.ahorro.application.use_cases.eliminar_ahorro import (
    EliminarAhorroUseCase
)


def test_debe_lanzar_error_si_el_id_usuario_es_none():

    repository = Mock()

    resultado_eliminacion = True

    repository.delete.return_value = resultado_eliminacion

    use_case = EliminarAhorroUseCase(repository)

    resultado = use_case.execute(1)

    repository.delete.assert_called_once_with(1)

    assert resultado == resultado_eliminacion
