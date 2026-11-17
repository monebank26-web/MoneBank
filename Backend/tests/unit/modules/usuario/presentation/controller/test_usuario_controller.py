from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.core.security.roles import ROL_ADMIN, ROL_USUARIO
from app.modules.usuario.presentation.controller.usuario_controller import (
    UsuarioController,
)
from app.modules.usuario.presentation.schema.usuario_schema import (
    BloqueoUsuarioRequest,
    UsuarioUpdate,
)
from app.shared.constants.acciones import ACCION_MODIFICAR_USUARIO
from app.shared.constants.codigos_error import (
    CODIGO_CORREO_RESTABLECIMIENTO_NO_ENVIADO,
)
from app.shared.exceptions.auth_errors import EmailAlreadyExistsException
from app.shared.exceptions.common import UsuarioNotFoundException
from app.shared.exceptions.usuario_errors import (
    CorreoRestablecimientoNoEnviadoException,
    NoPuedeRestablecerPasswordPropiaException,
    SolicitudCodigoRecienteException,
)


def mocks():
    return Mock(), Mock()


def usuario_actual(id_usuario, id_rol):
    return Mock(id_usuario=id_usuario, id_rol=id_rol)


class ErrorDelMotor(Exception):
    """Simula el error del motor: en Postgres el nombre va en `diag`."""

    def __init__(self, restriccion=None, mensaje="error de integridad"):
        super().__init__(mensaje)

        if restriccion:
            self.diag = SimpleNamespace(constraint_name=restriccion)


def error_de_integridad(restriccion=None, mensaje="error de integridad"):
    return IntegrityError("UPDATE usuario", {}, ErrorDelMotor(restriccion, mensaje))


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.CrearUsuario"
)
def test_crear_usuario_usa_uow_y_commitea(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    usuario = Mock()
    usuario.model_dump.return_value = {"nombres": "Ana"}
    mock_use_case.return_value.execute.return_value = {"id_usuario": 1}

    resultado = controller.crear_usuario(usuario)

    mock_use_case.assert_called_once_with(repository, unit_of_work.cuentas)
    mock_use_case.return_value.execute.assert_called_once_with({"nombres": "Ana"})
    unit_of_work.commit.assert_called_once()
    assert resultado == {"id_usuario": 1}


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.CrearUsuario"
)
def test_crear_usuario_con_error_hace_rollback_sin_commit(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    usuario = Mock()
    usuario.model_dump.return_value = {"nombres": "Ana"}
    mock_use_case.return_value.execute.side_effect = RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        controller.crear_usuario(usuario)

    unit_of_work.rollback.assert_called_once()
    unit_of_work.commit.assert_not_called()


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.ObtenerUsuariosUseCase"
)
def test_obtener_usuarios_pasa_los_filtros_al_caso_de_uso(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    filtros = {
        "buscar": "ana",
        "estado": "ACTIVO",
        "id_rol": ROL_USUARIO,
        "pagina": 2,
        "por_pagina": 5,
    }
    mock_use_case.return_value.execute.return_value = {"items": [], "total": 0}

    resultado = controller.obtener_usuarios(
        usuario_actual(6, ROL_ADMIN),
        filtros,
    )

    mock_use_case.assert_called_once_with(repository)
    mock_use_case.return_value.execute.assert_called_once_with(filtros)
    unit_of_work.commit.assert_not_called()
    assert resultado == {"items": [], "total": 0}


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.ObtenerUsuariosUseCase"
)
def test_obtener_usuarios_sin_filtros_usa_el_paginado_por_defecto(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    mock_use_case.return_value.execute.return_value = {"items": [], "total": 0}

    controller.obtener_usuarios(usuario_actual(6, ROL_ADMIN))

    mock_use_case.return_value.execute.assert_called_once_with({})


def test_obtener_usuario_por_id_bloquea_a_otro_usuario():

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)

    with pytest.raises(HTTPException) as exc:
        controller.obtener_usuario_por_id(9, usuario_actual(5, ROL_USUARIO))

    assert exc.value.status_code == 403
    repository.get_by_id.assert_not_called()


def test_obtener_usuario_por_id_permite_al_admin_y_al_propio_usuario():

    for current_user in (
        usuario_actual(6, ROL_ADMIN),
        usuario_actual(9, ROL_USUARIO),
    ):
        repository, unit_of_work = mocks()
        repository.get_by_id.return_value = Mock(id_usuario=9)
        controller = UsuarioController(repository, unit_of_work)

        resultado = controller.obtener_usuario_por_id(9, current_user)

        assert resultado.id_usuario == 9


def test_obtener_usuario_por_id_lanza_404_si_no_existe():

    repository, unit_of_work = mocks()
    repository.get_by_id.return_value = None
    controller = UsuarioController(repository, unit_of_work)

    with pytest.raises(UsuarioNotFoundException):
        controller.obtener_usuario_por_id(99, usuario_actual(6, ROL_ADMIN))


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.ActualizarUsuarioUseCase"
)
def test_actualizar_usuario_commitea(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    current_user = usuario_actual(1, ROL_USUARIO)
    usuario = Mock()
    usuario.model_dump.return_value = {"nombres": "Ana"}
    mock_use_case.return_value.execute.return_value = {"id_usuario": 1}

    resultado = controller.actualizar_usuario(1, usuario, current_user)

    mock_use_case.assert_called_once_with(
        repository,
        unit_of_work.registros_accion_admin,
    )
    mock_use_case.return_value.execute.assert_called_once_with(
        1,
        {"nombres": "Ana"},
        1,
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"id_usuario": 1}


def test_actualizar_usuario_de_otro_lanza_403():

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    current_user = usuario_actual(1, ROL_USUARIO)

    with pytest.raises(HTTPException) as exc:
        controller.actualizar_usuario(2, Mock(), current_user)

    assert exc.value.status_code == 403
    unit_of_work.commit.assert_not_called()
    unit_of_work.rollback.assert_not_called()


def test_actualizar_usuario_confirma_una_sola_vez_y_audita():

    repository, unit_of_work = mocks()
    repository.get_by_id.return_value = Mock(id_usuario=9)
    repository.exists_by_email.return_value = False

    usuario_actualizado = Mock(id_usuario=9, nombres="Ana")
    repository.update.return_value = usuario_actualizado

    controller = UsuarioController(repository, unit_of_work)

    resultado = controller.actualizar_usuario(
        9,
        UsuarioUpdate(nombres="Ana", correo="ana@test.com"),
        usuario_actual(6, ROL_ADMIN),
    )

    assert resultado is usuario_actualizado

    unit_of_work.commit.assert_called_once()
    unit_of_work.rollback.assert_not_called()

    auditoria = unit_of_work.registros_accion_admin.registrar

    assert auditoria.call_args.kwargs["id_admin"] == 6
    assert auditoria.call_args.kwargs["accion"] == ACCION_MODIFICAR_USUARIO
    assert auditoria.call_args.kwargs["id_usuario_afectado"] == 9
    auditoria.assert_called_once()


def test_actualizar_usuario_con_correo_duplicado_responde_409_sin_commit():

    repository, unit_of_work = mocks()
    repository.get_by_id.return_value = Mock(id_usuario=9)
    repository.exists_by_email.return_value = True

    controller = UsuarioController(repository, unit_of_work)

    with pytest.raises(EmailAlreadyExistsException):
        controller.actualizar_usuario(
            9,
            UsuarioUpdate(correo="David@gmail.com"),
            usuario_actual(6, ROL_ADMIN),
        )

    unit_of_work.rollback.assert_called_once()
    unit_of_work.commit.assert_not_called()
    repository.update.assert_not_called()
    unit_of_work.registros_accion_admin.registrar.assert_not_called()


def test_actualizar_usuario_propaga_el_error_de_correo_del_repositorio_con_rollback():

    repository, unit_of_work = mocks()
    repository.get_by_id.return_value = Mock(id_usuario=9)
    repository.exists_by_email.return_value = False
    repository.update.side_effect = EmailAlreadyExistsException()

    controller = UsuarioController(repository, unit_of_work)

    with pytest.raises(EmailAlreadyExistsException):
        controller.actualizar_usuario(
            9,
            UsuarioUpdate(correo="david@gmail.com"),
            usuario_actual(6, ROL_ADMIN),
        )

    unit_of_work.rollback.assert_called_once()
    unit_of_work.commit.assert_not_called()


def test_actualizar_usuario_deja_subir_los_errores_de_integridad_ajenos_al_correo():

    repository, unit_of_work = mocks()
    repository.get_by_id.return_value = Mock(id_usuario=9)
    repository.exists_by_email.return_value = False
    repository.update.side_effect = error_de_integridad(
        mensaje="viola la restricción usuario_estado_check"
    )

    controller = UsuarioController(repository, unit_of_work)

    with pytest.raises(IntegrityError):
        controller.actualizar_usuario(
            9,
            UsuarioUpdate(nombres="Ana"),
            usuario_actual(6, ROL_ADMIN),
        )

    unit_of_work.rollback.assert_called_once()
    unit_of_work.commit.assert_not_called()


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.InactivarUsuario"
)
def test_eliminar_usuario_commitea(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    current_user = usuario_actual(1, ROL_USUARIO)
    mock_use_case.return_value.execute.return_value = Mock(
        contrasena="hash-secreto"
    )

    resultado = controller.eliminar_usuario(1, current_user)

    mock_use_case.assert_called_once_with(
        repository,
        unit_of_work.registros_accion_admin,
    )
    mock_use_case.return_value.execute.assert_called_once_with(
        1,
        id_admin=current_user.id_usuario,
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"mensaje": "Usuario desactivado correctamente"}
    assert "contrasena" not in resultado


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.InactivarUsuario"
)
def test_eliminar_usuario_inexistente_propaga_el_404(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    current_user = usuario_actual(1, ROL_USUARIO)
    mock_use_case.return_value.execute.side_effect = UsuarioNotFoundException()

    with pytest.raises(UsuarioNotFoundException):
        controller.eliminar_usuario(99, current_user)

    unit_of_work.rollback.assert_called_once()
    unit_of_work.commit.assert_not_called()


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.BloquearUsuario"
)
def test_bloquear_usuario_envia_motivo(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    current_user = usuario_actual(1, ROL_USUARIO)
    datos = BloqueoUsuarioRequest(motivo="incumplimiento")
    mock_use_case.return_value.execute.return_value = {"estado": "BLOQUEADO"}

    resultado = controller.bloquear_usuario(5, datos, current_user)

    mock_use_case.assert_called_once_with(
        repository,
        unit_of_work.registros_accion_admin,
    )
    mock_use_case.return_value.execute.assert_called_once_with(
        5,
        "incumplimiento",
        id_admin=current_user.id_usuario,
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"estado": "BLOQUEADO"}


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.DesbloquearUsuario"
)
def test_desbloquear_usuario_commitea(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    current_user = usuario_actual(1, ROL_ADMIN)
    mock_use_case.return_value.execute.return_value = {"estado": "ACTIVO"}

    resultado = controller.desbloquear_usuario(5, current_user)

    mock_use_case.assert_called_once_with(
        repository,
        unit_of_work.registros_accion_admin,
    )
    mock_use_case.return_value.execute.assert_called_once_with(
        5,
        id_admin=current_user.id_usuario,
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"estado": "ACTIVO"}


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.DesbloquearUsuario"
)
def test_desbloquear_usuario_con_error_hace_rollback_sin_commit(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    current_user = usuario_actual(1, ROL_ADMIN)
    mock_use_case.return_value.execute.side_effect = RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        controller.desbloquear_usuario(5, current_user)

    unit_of_work.rollback.assert_called_once()
    unit_of_work.commit.assert_not_called()


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.RestablecerPasswordUsuario"
)
def test_restablecer_password_envia_correo_antes_de_commitear(mock_use_case):

    repository, unit_of_work = mocks()
    email_service = Mock()
    eventos = []

    def commit():
        eventos.append("commit")

    def enviar_correo(correo, codigo):
        eventos.append(("email", correo, codigo))
        return True

    unit_of_work.commit.side_effect = commit
    email_service.send_password_reset_by_admin.side_effect = enviar_correo

    resultado_caso_uso = {
        "id_usuario": 9,
        "correo": "usuario@test.com",
        "codigo": "123456",
    }
    mock_use_case.return_value.execute.return_value = resultado_caso_uso

    controller = UsuarioController(repository, unit_of_work, email_service)

    resultado = controller.restablecer_password_usuario(
        9,
        usuario_actual(6, ROL_ADMIN),
    )

    argumentos = mock_use_case.call_args.args
    assert argumentos[0] is repository
    assert argumentos[1] is unit_of_work.registros_accion_admin
    assert callable(argumentos[2]) is True
    mock_use_case.return_value.execute.assert_called_once_with(9, 6)
    assert eventos == [
        ("email", "usuario@test.com", "123456"),
        "commit",
    ]
    assert resultado == {
        "mensaje": (
            "Código de restablecimiento enviado al correo del usuario"
        )
    }
    assert "codigo" not in resultado
    assert "contrasena" not in resultado


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.RestablecerPasswordUsuario"
)
def test_restablecer_password_no_admin_devuelve_403(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)

    with pytest.raises(HTTPException) as exc:
        controller.restablecer_password_usuario(
            9,
            usuario_actual(6, ROL_USUARIO),
        )

    assert exc.value.status_code == 403
    mock_use_case.assert_not_called()
    unit_of_work.commit.assert_not_called()
    unit_of_work.rollback.assert_not_called()


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.RestablecerPasswordUsuario"
)
def test_restablecer_password_sin_email_service_falla_claro(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)

    with pytest.raises(
        RuntimeError,
        match="EmailService no inyectado en UsuarioController",
    ):
        controller.restablecer_password_usuario(
            9,
            usuario_actual(6, ROL_ADMIN),
        )

    mock_use_case.assert_not_called()
    unit_of_work.commit.assert_not_called()
    unit_of_work.rollback.assert_not_called()


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.RestablecerPasswordUsuario"
)
def test_restablecer_password_correo_no_enviado_responde_502_con_rollback(
    mock_use_case,
):

    repository, unit_of_work = mocks()
    email_service = Mock()
    email_service.send_password_reset_by_admin.return_value = False
    mock_use_case.return_value.execute.return_value = {
        "id_usuario": 9,
        "correo": "usuario@test.com",
        "codigo": "123456",
    }

    controller = UsuarioController(repository, unit_of_work, email_service)

    with pytest.raises(CorreoRestablecimientoNoEnviadoException) as exc:
        controller.restablecer_password_usuario(
            9,
            usuario_actual(6, ROL_ADMIN),
        )

    assert str(exc.value) == (
        "No se pudo enviar el código de restablecimiento. "
        "No se guardó ningún cambio. Intenta nuevamente."
    )
    assert exc.value.code == CODIGO_CORREO_RESTABLECIMIENTO_NO_ENVIADO
    unit_of_work.commit.assert_not_called()
    unit_of_work.rollback.assert_called_once()
    email_service.send_password_reset_by_admin.assert_called_once_with(
        "usuario@test.com",
        "123456",
    )


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.RestablecerPasswordUsuario"
)
def test_restablecer_password_excepcion_del_correo_responde_502_con_rollback(
    mock_use_case,
):

    repository, unit_of_work = mocks()
    email_service = Mock()
    email_service.send_password_reset_by_admin.side_effect = RuntimeError(
        "SMTP caído"
    )
    mock_use_case.return_value.execute.return_value = {
        "id_usuario": 9,
        "correo": "usuario@test.com",
        "codigo": "123456",
    }

    controller = UsuarioController(repository, unit_of_work, email_service)

    with pytest.raises(CorreoRestablecimientoNoEnviadoException):
        controller.restablecer_password_usuario(
            9,
            usuario_actual(6, ROL_ADMIN),
        )

    unit_of_work.commit.assert_not_called()
    unit_of_work.rollback.assert_called_once()


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.RestablecerPasswordUsuario"
)
def test_restablecer_password_error_del_caso_uso_hace_rollback(mock_use_case):

    repository, unit_of_work = mocks()
    email_service = Mock()
    mock_use_case.return_value.execute.side_effect = RuntimeError("boom")

    controller = UsuarioController(repository, unit_of_work, email_service)

    with pytest.raises(RuntimeError, match="boom"):
        controller.restablecer_password_usuario(
            9,
            usuario_actual(6, ROL_ADMIN),
        )

    unit_of_work.rollback.assert_called_once()
    unit_of_work.commit.assert_not_called()
    email_service.send_password_reset_by_admin.assert_not_called()


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.RestablecerPasswordUsuario"
)
def test_restablecer_password_en_enfriamiento_hace_rollback_y_no_envia(
    mock_use_case,
):
    repository, unit_of_work = mocks()
    email_service = Mock()
    mock_use_case.return_value.execute.side_effect = (
        SolicitudCodigoRecienteException()
    )

    controller = UsuarioController(repository, unit_of_work, email_service)

    with pytest.raises(SolicitudCodigoRecienteException):
        controller.restablecer_password_usuario(
            9,
            usuario_actual(6, ROL_ADMIN),
        )

    unit_of_work.rollback.assert_called_once()
    unit_of_work.commit.assert_not_called()
    email_service.send_password_reset_by_admin.assert_not_called()


def test_restablecer_password_propia_responde_400_sin_commit_ni_correo():

    repository, unit_of_work = mocks()
    email_service = Mock()
    controller = UsuarioController(repository, unit_of_work, email_service)

    with pytest.raises(NoPuedeRestablecerPasswordPropiaException):
        controller.restablecer_password_usuario(
            6,
            usuario_actual(6, ROL_ADMIN),
        )

    repository.get_by_id.assert_not_called()
    unit_of_work.rollback.assert_called_once()
    unit_of_work.commit.assert_not_called()
    email_service.send_password_reset_by_admin.assert_not_called()
