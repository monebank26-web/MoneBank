from unittest.mock import Mock
from app.modules.usuario.application.use_cases.eliminar_usuario import EliminarUsuarioUseCase

def test_debe_retornar_error_si_el_id_es_invalido():

    repository = Mock()
    db = Mock()

    use_case = EliminarUsuarioUseCase(repository)

    resultado = use_case.execute(db, -1)

    assert resultado == {
        "success": False,
        "message": "Id inválido"
    }

    repository.get_by_id.assert_not_called()
    repository.delete.assert_not_called()

def test_debe_retornar_error_si_el_usuario_no_existe():

    repository = Mock()
    db = Mock()

    repository.get_by_id.return_value = None

    use_case = EliminarUsuarioUseCase(repository)

    resultado = use_case.execute(db, 1)

    repository.get_by_id.assert_called_once_with(db, 1)
    repository.delete.assert_not_called()

    assert resultado == {
        "success": False,
        "message": "Usuario no encontrado"
    }

def test_debe_eliminar_usuario_correctamente():

    repository = Mock()
    db = Mock()

    repository.get_by_id.return_value = {
        "id": 1,
        "nombre": "Juan"
    }

    use_case = EliminarUsuarioUseCase(repository)

    resultado = use_case.execute(db, 1)

    repository.get_by_id.assert_called_once_with(db, 1)
    repository.delete.assert_called_once_with(db, 1)

    assert resultado == {
        "success": True,
        "message": "Usuario eliminado correctamente"
    }
