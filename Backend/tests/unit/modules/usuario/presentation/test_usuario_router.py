from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from fastapi.routing import APIRoute
from sqlalchemy.exc import IntegrityError

from app.core.security.auth import get_current_user
from app.core.security.roles import ROL_ADMIN, ROL_USUARIO
from app.modules.usuario.presentation.router.router import (
    actualizar_usuario,
    obtener_usuario_por_id,
    router,
)
from app.modules.usuario.presentation.schema.usuario_schema import UsuarioUpdate
from app.shared.constants.acciones import ACCION_MODIFICAR_USUARIO
from app.shared.exceptions.auth_errors import EmailAlreadyExistsException
from app.shared.exceptions.common import UsuarioNotFoundException


class ErrorDelMotor(Exception):
    """Simula el error del motor: en Postgres el nombre va en `diag`."""

    def __init__(self, restriccion=None, mensaje="error de integridad"):
        super().__init__(mensaje)

        if restriccion:
            self.diag = SimpleNamespace(constraint_name=restriccion)


def error_de_integridad(restriccion=None, mensaje="error de integridad"):
    return IntegrityError("UPDATE usuario", {}, ErrorDelMotor(restriccion, mensaje))


def buscar_ruta(metodo, path):
    for ruta in router.routes:
        if (
            isinstance(ruta, APIRoute)
            and ruta.path == path
            and metodo in ruta.methods
        ):
            return ruta

    raise AssertionError(f"No existe la ruta {metodo} {path}")


def usuario_actual(id_usuario, id_rol):
    return Mock(id_usuario=id_usuario, id_rol=id_rol)


def test_listar_usuarios_sigue_exigiendo_rol_admin():
    ruta = buscar_ruta("GET", "/usuarios/")

    dependencia_rol = None

    for dependencia in ruta.dependant.dependencies:
        if any(sub.call is get_current_user for sub in dependencia.dependencies):
            dependencia_rol = dependencia.call

    assert dependencia_rol is not None

    with pytest.raises(HTTPException) as exc:
        dependencia_rol(usuario_actual(5, ROL_USUARIO))

    assert exc.value.status_code == 403

    assert dependencia_rol(usuario_actual(6, ROL_ADMIN)).id_usuario == 6


def test_obtener_usuario_por_id_bloquea_a_otro_usuario():
    repository = Mock()

    with pytest.raises(HTTPException) as exc:
        obtener_usuario_por_id(
            9,
            repository=repository,
            current_user=usuario_actual(5, ROL_USUARIO),
        )

    assert exc.value.status_code == 403
    repository.get_by_id.assert_not_called()


def test_obtener_usuario_por_id_permite_al_admin_y_al_propio_usuario():
    for current_user in (
        usuario_actual(6, ROL_ADMIN),
        usuario_actual(9, ROL_USUARIO),
    ):
        repository = Mock()
        repository.get_by_id.return_value = Mock(id_usuario=9)

        resultado = obtener_usuario_por_id(
            9,
            repository=repository,
            current_user=current_user,
        )

        assert resultado.id_usuario == 9


def test_obtener_usuario_por_id_lanza_404_si_no_existe():
    repository = Mock()
    repository.get_by_id.return_value = None

    with pytest.raises(UsuarioNotFoundException):
        obtener_usuario_por_id(
            99,
            repository=repository,
            current_user=usuario_actual(6, ROL_ADMIN),
        )


def test_actualizar_usuario_bloquea_a_otro_usuario():
    unit_of_work = Mock()

    with pytest.raises(HTTPException) as exc:
        actualizar_usuario(
            9,
            UsuarioUpdate(nombres="Ana"),
            repository=Mock(),
            unit_of_work=unit_of_work,
            current_user=usuario_actual(5, ROL_USUARIO),
        )

    assert exc.value.status_code == 403
    unit_of_work.commit.assert_not_called()


def test_actualizar_usuario_confirma_una_sola_vez_y_audita():
    repository = Mock()
    repository.get_by_id.return_value = Mock(id_usuario=9)
    repository.exists_by_email.return_value = False

    usuario_actualizado = Mock(id_usuario=9, nombres="Ana")
    repository.update.return_value = usuario_actualizado

    unit_of_work = Mock()

    resultado = actualizar_usuario(
        9,
        UsuarioUpdate(nombres="Ana", correo="ana@test.com"),
        repository=repository,
        unit_of_work=unit_of_work,
        current_user=usuario_actual(6, ROL_ADMIN),
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
    repository = Mock()
    repository.get_by_id.return_value = Mock(id_usuario=9)
    repository.exists_by_email.return_value = True
    unit_of_work = Mock()

    with pytest.raises(EmailAlreadyExistsException):
        actualizar_usuario(
            9,
            UsuarioUpdate(correo="David@gmail.com"),
            repository=repository,
            unit_of_work=unit_of_work,
            current_user=usuario_actual(6, ROL_ADMIN),
        )

    unit_of_work.rollback.assert_called_once()
    unit_of_work.commit.assert_not_called()
    repository.update.assert_not_called()
    unit_of_work.registros_accion_admin.registrar.assert_not_called()


def test_actualizar_usuario_propaga_el_error_de_correo_del_repositorio_con_rollback():
    repository = Mock()
    repository.get_by_id.return_value = Mock(id_usuario=9)
    repository.exists_by_email.return_value = False
    repository.update.side_effect = EmailAlreadyExistsException()
    unit_of_work = Mock()

    with pytest.raises(EmailAlreadyExistsException):
        actualizar_usuario(
            9,
            UsuarioUpdate(correo="david@gmail.com"),
            repository=repository,
            unit_of_work=unit_of_work,
            current_user=usuario_actual(6, ROL_ADMIN),
        )

    unit_of_work.rollback.assert_called_once()
    unit_of_work.commit.assert_not_called()


def test_actualizar_usuario_deja_subir_los_errores_de_integridad_ajenos_al_correo():
    repository = Mock()
    repository.get_by_id.return_value = Mock(id_usuario=9)
    repository.exists_by_email.return_value = False
    repository.update.side_effect = error_de_integridad(
        mensaje="viola la restricción usuario_estado_check"
    )
    unit_of_work = Mock()

    with pytest.raises(IntegrityError):
        actualizar_usuario(
            9,
            UsuarioUpdate(nombres="Ana"),
            repository=repository,
            unit_of_work=unit_of_work,
            current_user=usuario_actual(6, ROL_ADMIN),
        )

    unit_of_work.rollback.assert_called_once()
    unit_of_work.commit.assert_not_called()
