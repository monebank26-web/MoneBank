from typing import get_args, get_origin

from fastapi.routing import APIRoute

from app.modules.usuario.presentation.router.router import router
from app.modules.usuario.presentation.schema.usuario_schema import (
    UsuarioAdminResponse,
    UsuarioDesactivadoResponse,
    UsuarioListResponse,
    UsuarioResponse,
)


CAMPOS_SENSIBLES_SIEMPRE = (
    "contrasena",
    "intentos_fallidos",
    "bloqueado_hasta",
)
CAMPOS_SOLO_ADMIN = (
    "motivo_bloqueo",
    "fecha_bloqueo",
)
CAMPOS_SENSIBLES = CAMPOS_SENSIBLES_SIEMPRE + CAMPOS_SOLO_ADMIN


def buscar_ruta(metodo, path):
    for ruta in router.routes:
        if (
            isinstance(ruta, APIRoute)
            and ruta.path == path
            and metodo in ruta.methods
        ):
            return ruta

    raise AssertionError(f"No existe la ruta {metodo} {path}")


def campos_del_response_model(response_model):
    """Devuelve los campos del usuario, desenvolviendo el sobre si lo trae."""
    modelo = response_model

    if get_origin(modelo) is list:
        modelo = get_args(modelo)[0]

    campos = getattr(modelo, "model_fields", {})

    if "items" in campos:
        modelo = get_args(campos["items"].annotation)[0]

    return set(modelo.model_fields)


def test_get_usuarios_declara_response_model_con_metadatos_de_bloqueo():
    ruta = buscar_ruta("GET", "/usuarios/")

    assert ruta.response_model is not None

    campos = campos_del_response_model(ruta.response_model)

    for campo in CAMPOS_SENSIBLES_SIEMPRE:
        assert campo not in campos

    for campo in CAMPOS_SOLO_ADMIN:
        assert campo in campos


def test_get_usuario_por_id_declara_response_model_sin_campos_sensibles():
    ruta = buscar_ruta("GET", "/usuarios/{id_usuario}")

    assert ruta.response_model is not None

    campos = campos_del_response_model(ruta.response_model)

    for campo in CAMPOS_SENSIBLES:
        assert campo not in campos


def test_delete_usuario_devuelve_solo_el_mensaje():
    ruta = buscar_ruta("DELETE", "/usuarios/{id_usuario}")

    assert ruta.response_model is UsuarioDesactivadoResponse
    assert set(ruta.response_model.model_fields) == {"mensaje"}


def test_usuario_admin_response_solo_agrega_los_metadatos_de_bloqueo():
    assert set(UsuarioAdminResponse.model_fields) == (
        set(UsuarioResponse.model_fields) | set(CAMPOS_SOLO_ADMIN)
    )


def test_usuario_response_conserva_los_campos_que_usa_el_panel():
    campos = set(UsuarioResponse.model_fields)

    assert {
        "id_usuario",
        "nombres",
        "apellidos",
        "correo",
        "estado",
        "id_rol",
        "fecha_creacion",
    } <= campos


def test_get_usuarios_devuelve_el_sobre_paginado():
    ruta = buscar_ruta("GET", "/usuarios/")

    assert ruta.response_model is UsuarioListResponse

    campos = set(ruta.response_model.model_fields)

    assert {"items", "total", "pagina", "por_pagina"} <= campos
