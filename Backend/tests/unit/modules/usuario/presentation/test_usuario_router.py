from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from fastapi.routing import APIRoute

from app.core.security.auth import get_current_user
from app.core.security.roles import ROL_ADMIN, ROL_USUARIO
from app.modules.usuario.presentation.router.router import (
    actualizar_usuario,
    bloquear_usuario,
    crear_usuario,
    eliminar_usuario,
    obtener_usuario_por_id,
    obtener_usuarios,
    router,
)
from app.modules.usuario.presentation.schema.usuario_schema import (
    BloqueoUsuarioRequest,
    UsuarioUpdate,
)
from app.shared.constants.motivo_bloqueo import DESCRIPCION_MOTIVO_BLOQUEO


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


def test_listar_usuarios_conserva_los_filtros_de_la_url():
    ruta = buscar_ruta("GET", "/usuarios/")

    parametros = {parametro.name for parametro in ruta.dependant.query_params}

    assert {
        "buscar",
        "estado",
        "id_rol",
        "pagina",
        "por_pagina",
    } <= parametros


def test_crear_usuario_delega_en_el_controller():
    controller = Mock()
    controller.crear_usuario.return_value = {"id_usuario": 1}
    usuario = Mock()

    resultado = crear_usuario(usuario, controller)

    controller.crear_usuario.assert_called_once_with(usuario)
    assert resultado == {"id_usuario": 1}


def test_obtener_usuarios_delega_los_filtros_en_el_controller():
    controller = Mock()
    current_user = usuario_actual(6, ROL_ADMIN)

    obtener_usuarios(
        buscar="ana",
        estado="ACTIVO",
        id_rol=ROL_USUARIO,
        pagina=2,
        por_pagina=5,
        current_user=current_user,
        controller=controller,
    )

    controller.obtener_usuarios.assert_called_once_with(
        current_user,
        {
            "buscar": "ana",
            "estado": "ACTIVO",
            "id_rol": ROL_USUARIO,
            "pagina": 2,
            "por_pagina": 5,
        },
    )


def test_obtener_usuario_por_id_delega_en_el_controller():
    controller = Mock()
    current_user = usuario_actual(9, ROL_USUARIO)

    obtener_usuario_por_id(9, current_user=current_user, controller=controller)

    controller.obtener_usuario_por_id.assert_called_once_with(9, current_user)


def test_actualizar_usuario_delega_en_el_controller():
    controller = Mock()
    current_user = usuario_actual(6, ROL_ADMIN)
    usuario = UsuarioUpdate(nombres="Ana")

    actualizar_usuario(
        9,
        usuario,
        current_user=current_user,
        controller=controller,
    )

    controller.actualizar_usuario.assert_called_once_with(9, usuario, current_user)


def test_eliminar_usuario_delega_en_el_controller():
    controller = Mock()
    current_user = usuario_actual(6, ROL_ADMIN)

    eliminar_usuario(9, current_user=current_user, controller=controller)

    controller.eliminar_usuario.assert_called_once_with(9, current_user)


def test_bloquear_usuario_delega_en_el_controller():
    controller = Mock()
    current_user = usuario_actual(6, ROL_ADMIN)
    datos = BloqueoUsuarioRequest(motivo="incumplimiento")

    bloquear_usuario(
        9,
        datos,
        current_user=current_user,
        controller=controller,
    )

    controller.bloquear_usuario.assert_called_once_with(9, datos, current_user)


def test_bloquear_usuario_documenta_las_respuestas_de_error():
    ruta = buscar_ruta("PUT", "/usuarios/{id_usuario}/bloquear")

    assert {400, 401, 403, 404, 409, 422} <= set(ruta.responses)
    assert DESCRIPCION_MOTIVO_BLOQUEO in ruta.responses[422]["description"]


def test_eliminar_usuario_documenta_las_respuestas_de_error():
    ruta = buscar_ruta("DELETE", "/usuarios/{id_usuario}")

    assert {400, 401, 403, 404, 409, 422} <= set(ruta.responses)
