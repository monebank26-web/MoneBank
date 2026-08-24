from unittest.mock import Mock
from app.modules.usuario.application.use_cases.obtener_usuario import ObtenerUsuariosUseCase


def test_debe_obtener_todos_los_usuarios():

    repository = Mock()

    usuarios = [
        {"id": 1, "nombre": "Juan"},
        {"id": 2, "nombre": "Ana"}
    ]

    repository.get_all.return_value = usuarios

    use_case = ObtenerUsuariosUseCase(repository)

    resultado = use_case.execute()

    repository.get_all.assert_called_once_with()

    assert resultado == usuarios


def test_debe_retornar_lista_vacia_si_no_hay_usuarios():

    repository = Mock()

    repository.get_all.return_value = []

    use_case = ObtenerUsuariosUseCase(repository)

    resultado = use_case.execute()

    repository.get_all.assert_called_once_with()

    assert resultado == []
