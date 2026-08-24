from unittest.mock import Mock

from app.modules.transaccion.application.use_cases.obtener_transacciones_historial import (
    ObtenerHistorialUseCase
)


FILTROS = {"pagina": 1, "por_pagina": 10}


def test_debe_retornar_historial_paginado():

    repository = Mock()

    repository.find_historial.return_value = (
        [{"id_transaccion": 1}, {"id_transaccion": 2}],
        25
    )

    resultado = ObtenerHistorialUseCase(repository).execute(6, dict(FILTROS))

    repository.find_historial.assert_called_once_with(6, dict(FILTROS))

    assert resultado["total"] == 25
    assert resultado["pagina"] == 1
    assert resultado["por_pagina"] == 10
    assert resultado["total_paginas"] == 3
    assert len(resultado["items"]) == 2


def test_pagina_exacta_no_genera_pagina_extra():

    repository = Mock()

    repository.find_historial.return_value = ([], 20)

    resultado = ObtenerHistorialUseCase(repository).execute(6, dict(FILTROS))

    assert resultado["total_paginas"] == 2


def test_historial_vacio_retorna_cero_paginas():

    repository = Mock()

    repository.find_historial.return_value = ([], 0)

    resultado = ObtenerHistorialUseCase(repository).execute(6, dict(FILTROS))

    assert resultado == {
        "items": [],
        "total": 0,
        "pagina": 1,
        "por_pagina": 10,
        "total_paginas": 0
    }
