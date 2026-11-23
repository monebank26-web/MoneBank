from unittest.mock import Mock

import pytest

from app.modules.usuario.application.use_cases.actualizar_usuarios import (
    ActualizarUsuarioUseCase,
)
from app.shared.constants.acciones import ACCION_MODIFICAR_USUARIO
from app.shared.exceptions.auth_errors import EmailAlreadyExistsException
from app.shared.exceptions.common import UsuarioNotFoundException


def crear_caso_uso(repository=None, registro_repository=None):
    return ActualizarUsuarioUseCase(
        repository if repository is not None else Mock(),
        registro_repository if registro_repository is not None else Mock(),
    )


def crear_repository(usuario_existe=True):
    repository = Mock()
    repository.get_by_id.return_value = Mock(id_usuario=7) if usuario_existe else None
    repository.exists_by_email.return_value = False
    repository.update.return_value = Mock(id_usuario=7)
    return repository


def test_execute_actualiza_y_registra_la_auditoria():

    repository = crear_repository()
    usuario_actualizado = Mock(id_usuario=7, nombres="Ana")
    repository.update.return_value = usuario_actualizado
    registro_repository = Mock()

    caso_uso = crear_caso_uso(repository, registro_repository)

    resultado = caso_uso.execute(
        7,
        {"nombres": "Ana", "correo": " Ana@Test.com "},
        6,
    )

    assert resultado is usuario_actualizado

    repository.exists_by_email.assert_called_once_with(
        "Ana@Test.com",
        excluir_id_usuario=7,
    )

    repository.update.assert_called_once_with(
        7,
        {"nombres": "Ana", "correo": "Ana@Test.com"},
    )

    registro_repository.registrar.assert_called_once_with(
        id_admin=6,
        accion=ACCION_MODIFICAR_USUARIO,
        id_usuario_afectado=7,
        detalle="Campos modificados: correo, nombres",
    )


def test_execute_rechaza_el_correo_de_otro_usuario():

    repository = crear_repository()
    repository.exists_by_email.return_value = True
    registro_repository = Mock()

    caso_uso = crear_caso_uso(repository, registro_repository)

    with pytest.raises(EmailAlreadyExistsException):
        caso_uso.execute(7, {"correo": "david@gmail.com"}, 6)

    repository.exists_by_email.assert_called_once_with(
        "david@gmail.com",
        excluir_id_usuario=7,
    )

    repository.update.assert_not_called()
    registro_repository.registrar.assert_not_called()


def test_execute_no_consulta_el_correo_si_no_se_envia():

    repository = crear_repository()

    caso_uso = crear_caso_uso(repository)

    caso_uso.execute(7, {"nombres": "Ana"}, 6)

    repository.exists_by_email.assert_not_called()
    repository.update.assert_called_once_with(7, {"nombres": "Ana"})


def test_execute_descarta_los_campos_no_enviados_o_nulos():

    repository = crear_repository()

    caso_uso = crear_caso_uso(repository)

    caso_uso.execute(7, {"nombres": "Ana", "correo": None, "apellidos": None}, 6)

    repository.update.assert_called_once_with(7, {"nombres": "Ana"})


def test_execute_lanza_usuario_no_encontrado_si_no_existe():

    repository = crear_repository(usuario_existe=False)
    registro_repository = Mock()

    caso_uso = crear_caso_uso(repository, registro_repository)

    with pytest.raises(UsuarioNotFoundException):
        caso_uso.execute(99, {"nombres": "Ana"}, 6)

    repository.update.assert_not_called()
    registro_repository.registrar.assert_not_called()


def test_execute_lanza_usuario_no_encontrado_si_el_update_no_devuelve_nada():

    repository = crear_repository()
    repository.update.return_value = None
    registro_repository = Mock()

    caso_uso = crear_caso_uso(repository, registro_repository)

    with pytest.raises(UsuarioNotFoundException):
        caso_uso.execute(7, {"nombres": "Ana"}, 6)

    registro_repository.registrar.assert_not_called()


def test_execute_propaga_el_error_del_repositorio():

    repository = crear_repository()
    repository.update.side_effect = RuntimeError("Error al actualizar")
    registro_repository = Mock()

    caso_uso = crear_caso_uso(repository, registro_repository)

    with pytest.raises(RuntimeError, match="Error al actualizar"):
        caso_uso.execute(7, {"nombres": "Ana"}, 6)

    registro_repository.registrar.assert_not_called()


def test_execute_sin_cambios_registra_la_auditoria():

    repository = crear_repository()
    registro_repository = Mock()

    caso_uso = crear_caso_uso(repository, registro_repository)

    caso_uso.execute(7, {}, 6)

    registro_repository.registrar.assert_called_once_with(
        id_admin=6,
        accion=ACCION_MODIFICAR_USUARIO,
        id_usuario_afectado=7,
        detalle="Sin cambios",
    )
