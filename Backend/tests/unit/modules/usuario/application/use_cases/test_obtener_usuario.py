from unittest.mock import Mock

from app.modules.usuario.application.use_cases.obtener_usuario import (
    ObtenerUsuariosUseCase,
)


def test_debe_obtener_los_usuarios_con_el_sobre_paginado():

    repository = Mock()

    usuarios = [
        {"id_usuario": 1, "nombres": "Juan"},
        {"id_usuario": 2, "nombres": "Ana"},
    ]

    repository.listar.return_value = (usuarios, 42)

    use_case = ObtenerUsuariosUseCase(repository)

    resultado = use_case.execute({
        "buscar": "ju",
        "estado": "ACTIVO",
        "id_rol": 2,
        "pagina": 3,
        "por_pagina": 5,
    })

    repository.listar.assert_called_once_with({
        "buscar": "ju",
        "estado": "ACTIVO",
        "id_rol": 2,
        "pagina": 3,
        "por_pagina": 5,
    })

    assert resultado == {
        "items": usuarios,
        "total": 42,
        "pagina": 3,
        "por_pagina": 5,
    }


def test_debe_aplicar_el_paginado_por_defecto_sin_filtros():

    repository = Mock()
    repository.listar.return_value = ([], 0)

    use_case = ObtenerUsuariosUseCase(repository)

    resultado = use_case.execute()

    assert repository.listar.call_args.args[0] == {
        "pagina": 1,
        "por_pagina": 10,
    }

    assert resultado == {
        "items": [],
        "total": 0,
        "pagina": 1,
        "por_pagina": 10,
    }


def test_debe_ignorar_paginado_invalido_y_no_tocar_los_filtros_del_llamador():

    repository = Mock()
    repository.listar.return_value = ([], 0)

    filtros = {"buscar": "ana", "pagina": None, "por_pagina": 0}

    use_case = ObtenerUsuariosUseCase(repository)

    resultado = use_case.execute(filtros)

    assert resultado["pagina"] == 1
    assert resultado["por_pagina"] == 10
    assert filtros == {"buscar": "ana", "pagina": None, "por_pagina": 0}
