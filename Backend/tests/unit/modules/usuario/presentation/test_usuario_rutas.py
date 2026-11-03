from datetime import datetime, timedelta
from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.database.connection import get_db
from app.core.security.auth import get_current_user
from app.core.security.roles import ROL_ADMIN, ROL_USUARIO
from app.modules.admin.infrastructure.model.registro_accion_admin_model import (
    RegistroAccionAdminModel,
)
from app.modules.usuario.presentation.router.router import router
from app.shared.constants.acciones import ACCION_DESBLOQUEAR_USUARIO
from app.shared.constants.codigos_error import (
    CODIGO_CUENTA_INACTIVA_NO_BLOQUEABLE,
    CODIGO_CUENTA_NO_BLOQUEADA,
    CODIGO_CUENTA_YA_BLOQUEADA,
    CODIGO_CUENTA_YA_INACTIVA,
    CODIGO_NO_PUEDE_DESACTIVARSE,
)
from app.shared.exceptions.handlers.common_handlers import (
    register_common_exception_handlers,
)
from app.shared.exceptions.handlers.global_handlers import (
    register_global_exception_handlers,
)
from app.shared.exceptions.handlers.usuario_handlers import (
    register_usuario_exception_handlers,
)


ADMIN_ID = 1
USUARIO_ACTIVO_ID = 2
USUARIO_INACTIVO_ID = 3
USUARIO_BLOQUEADO_ID = 4
OTRO_ACTIVO_ID = 5
USUARIO_ACTIVO_TEMPORAL_ID = 6
USUARIO_INEXISTENTE_ID = 999


def crear_tablas(engine):
    with engine.begin() as conexion:
        conexion.execute(text("""
            CREATE TABLE usuario (
                id_usuario INTEGER PRIMARY KEY,
                nombres VARCHAR(80) NOT NULL,
                apellidos VARCHAR(100) NOT NULL,
                correo VARCHAR(150) NOT NULL UNIQUE,
                contrasena VARCHAR(100) NOT NULL,
                fecha_creacion DATE,
                estado VARCHAR(20) NOT NULL,
                id_rol INTEGER,
                id_tipo_usuario INTEGER,
                intentos_fallidos INTEGER NOT NULL DEFAULT 0,
                bloqueado_hasta DATETIME,
                motivo_bloqueo VARCHAR(255),
                fecha_bloqueo DATETIME,
                fecha_desbloqueo DATETIME,
                CONSTRAINT usuario_estado_check CHECK (
                    estado IN ('ACTIVO', 'INACTIVO', 'BLOQUEADO')
                )
            )
        """))
        conexion.execute(text("""
            CREATE TABLE registro_accion_admin (
                id_registro_accion INTEGER PRIMARY KEY AUTOINCREMENT,
                id_admin INTEGER NOT NULL,
                accion VARCHAR(60) NOT NULL,
                id_usuario_afectado INTEGER,
                detalle TEXT,
                fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """))


def insertar_usuario(conexion, id_usuario, correo, estado, id_rol, **extra):
    datos = {
        "id_usuario": id_usuario,
        "nombres": f"Usuario {id_usuario}",
        "apellidos": "Prueba",
        "correo": correo,
        "contrasena": f"hash-{id_usuario}",
        "fecha_creacion": "2026-01-01",
        "estado": estado,
        "id_rol": id_rol,
        "id_tipo_usuario": 3,
        "intentos_fallidos": 0,
        "bloqueado_hasta": None,
        "motivo_bloqueo": None,
        "fecha_bloqueo": None,
        "fecha_desbloqueo": None,
    }
    datos.update(extra)

    conexion.execute(text("""
        INSERT INTO usuario (
            id_usuario,
            nombres,
            apellidos,
            correo,
            contrasena,
            fecha_creacion,
            estado,
            id_rol,
            id_tipo_usuario,
            intentos_fallidos,
            bloqueado_hasta,
            motivo_bloqueo,
            fecha_bloqueo,
            fecha_desbloqueo
        ) VALUES (
            :id_usuario,
            :nombres,
            :apellidos,
            :correo,
            :contrasena,
            :fecha_creacion,
            :estado,
            :id_rol,
            :id_tipo_usuario,
            :intentos_fallidos,
            :bloqueado_hasta,
            :motivo_bloqueo,
            :fecha_bloqueo,
            :fecha_desbloqueo
        )
    """), datos)


def sembrar_usuarios(engine):
    with engine.begin() as conexion:
        insertar_usuario(
            conexion,
            ADMIN_ID,
            "admin@example.com",
            "ACTIVO",
            ROL_ADMIN,
        )
        insertar_usuario(
            conexion,
            USUARIO_ACTIVO_ID,
            "activo@example.com",
            "ACTIVO",
            ROL_USUARIO,
        )
        insertar_usuario(
            conexion,
            USUARIO_INACTIVO_ID,
            "inactivo@example.com",
            "INACTIVO",
            ROL_USUARIO,
        )
        insertar_usuario(
            conexion,
            USUARIO_BLOQUEADO_ID,
            "bloqueado@example.com",
            "BLOQUEADO",
            ROL_USUARIO,
            motivo_bloqueo="Fraude",
            fecha_bloqueo="2026-01-02 10:30:00",
            intentos_fallidos=5,
            bloqueado_hasta=(
                datetime.now() + timedelta(minutes=30)
            ).strftime("%Y-%m-%d %H:%M:%S"),
        )
        insertar_usuario(
            conexion,
            OTRO_ACTIVO_ID,
            "otro@example.com",
            "ACTIVO",
            ROL_USUARIO,
        )
        insertar_usuario(
            conexion,
            USUARIO_ACTIVO_TEMPORAL_ID,
            "temporal@example.com",
            "ACTIVO",
            ROL_USUARIO,
            intentos_fallidos=5,
            bloqueado_hasta=(
                datetime.now() + timedelta(minutes=30)
            ).strftime("%Y-%m-%d %H:%M:%S"),
        )


@pytest.fixture
def entorno(tmp_path):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'usuarios.db'}",
        connect_args={"check_same_thread": False},
    )
    crear_tablas(engine)
    sembrar_usuarios(engine)

    session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    app = FastAPI()
    app.include_router(router)
    register_usuario_exception_handlers(app)
    register_common_exception_handlers(app)
    register_global_exception_handlers(app)

    def override_get_db():
        sesion = session_factory()
        try:
            yield sesion
        finally:
            sesion.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as cliente:
        yield cliente, app, session_factory

    app.dependency_overrides.clear()
    engine.dispose()


def autenticar_admin(app):
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id_usuario=ADMIN_ID,
        id_rol=ROL_ADMIN,
    )


def autenticar_usuario(app):
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id_usuario=USUARIO_ACTIVO_ID,
        id_rol=ROL_USUARIO,
    )


def contar_auditorias(session_factory):
    with session_factory() as sesion:
        return sesion.query(RegistroAccionAdminModel).count()


def obtener_usuario(session_factory, id_usuario):
    with session_factory() as sesion:
        return sesion.execute(text("""
            SELECT
                estado,
                motivo_bloqueo,
                fecha_bloqueo,
                fecha_desbloqueo,
                intentos_fallidos,
                bloqueado_hasta
            FROM usuario
            WHERE id_usuario = :id_usuario
        """), {"id_usuario": id_usuario}).mappings().one()


def obtener_ultima_auditoria(session_factory):
    with session_factory() as sesion:
        auditoria = (
            sesion.query(RegistroAccionAdminModel)
            .order_by(RegistroAccionAdminModel.id_registro_accion.desc())
            .first()
        )

        return {
            "id_admin": auditoria.id_admin,
            "accion": auditoria.accion,
            "id_usuario_afectado": auditoria.id_usuario_afectado,
            "detalle": auditoria.detalle,
        }


def assert_sin_contrasena(payload):
    if isinstance(payload, dict):
        assert "contrasena" not in payload
        for valor in payload.values():
            assert_sin_contrasena(valor)
    elif isinstance(payload, list):
        for item in payload:
            assert_sin_contrasena(item)


def test_sin_token_devuelve_401(entorno):
    cliente, _, _ = entorno

    respuesta = cliente.delete(f"/usuarios/{USUARIO_INACTIVO_ID}")

    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "Token no proporcionado"


def test_usuario_no_admin_devuelve_403(entorno):
    cliente, app, _ = entorno
    autenticar_usuario(app)

    respuesta = cliente.delete(f"/usuarios/{USUARIO_INACTIVO_ID}")

    assert respuesta.status_code == 403


def test_usuario_inexistente_devuelve_404(entorno):
    cliente, app, _ = entorno
    autenticar_admin(app)

    respuesta = cliente.delete(f"/usuarios/{USUARIO_INEXISTENTE_ID}")

    assert respuesta.status_code == 404
    assert respuesta.json()["message"] == "Usuario no encontrado"
    assert_sin_contrasena(respuesta.json())


def test_transiciones_invalidas_devuelven_409_con_codigo(entorno):
    cliente, app, session_factory = entorno
    autenticar_admin(app)
    auditorias_antes = contar_auditorias(session_factory)

    respuesta = cliente.delete(f"/usuarios/{USUARIO_INACTIVO_ID}")

    assert respuesta.status_code == 409
    assert respuesta.json()["code"] == CODIGO_CUENTA_YA_INACTIVA
    assert_sin_contrasena(respuesta.json())

    respuesta = cliente.put(
        f"/usuarios/{USUARIO_INACTIVO_ID}/bloquear",
        json={"motivo": "Motivo valido"},
    )

    assert respuesta.status_code == 409
    assert respuesta.json()["code"] == CODIGO_CUENTA_INACTIVA_NO_BLOQUEABLE
    assert_sin_contrasena(respuesta.json())

    respuesta = cliente.put(
        f"/usuarios/{USUARIO_BLOQUEADO_ID}/bloquear",
        json={"motivo": "Motivo valido"},
    )

    assert respuesta.status_code == 409
    assert respuesta.json()["code"] == CODIGO_CUENTA_YA_BLOQUEADA
    assert_sin_contrasena(respuesta.json())

    assert contar_auditorias(session_factory) == auditorias_antes


@pytest.mark.parametrize(
    "payload,mensaje",
    [
        ({}, "El motivo del bloqueo es obligatorio"),
        ({"motivo": None}, "El motivo del bloqueo es obligatorio"),
        ({"motivo": ""}, "El motivo del bloqueo es obligatorio"),
        ({"motivo": "   "}, "El motivo del bloqueo es obligatorio"),
        ({"motivo": "abcd"}, "El motivo del bloqueo es obligatorio"),
        ({"motivo": "x" * 256}, "Datos de entrada inválidos"),
    ],
)
def test_motivo_invalido_devuelve_422(entorno, payload, mensaje):
    cliente, app, _ = entorno
    autenticar_admin(app)

    respuesta = cliente.put(
        f"/usuarios/{USUARIO_ACTIVO_ID}/bloquear",
        json=payload,
    )

    assert respuesta.status_code == 422
    assert respuesta.json()["message"] == mensaje
    assert_sin_contrasena(respuesta.json())


def test_autodesactivacion_devuelve_400_con_codigo(entorno):
    cliente, app, _ = entorno
    autenticar_admin(app)

    respuesta = cliente.delete(f"/usuarios/{ADMIN_ID}")

    assert respuesta.status_code == 400
    assert respuesta.json()["code"] == CODIGO_NO_PUEDE_DESACTIVARSE
    assert_sin_contrasena(respuesta.json())


def test_las_respuestas_no_exponen_contrasena(entorno):
    cliente, app, _ = entorno
    autenticar_admin(app)

    respuesta = cliente.get("/usuarios/")
    assert respuesta.status_code == 200
    assert_sin_contrasena(respuesta.json())

    bloqueado = next(
        item
        for item in respuesta.json()["items"]
        if item["id_usuario"] == USUARIO_BLOQUEADO_ID
    )
    assert bloqueado["motivo_bloqueo"] == "Fraude"
    assert bloqueado["fecha_bloqueo"] is not None
    assert "fecha_desbloqueo" in bloqueado

    respuesta = cliente.get(f"/usuarios/{USUARIO_BLOQUEADO_ID}")
    assert respuesta.status_code == 200
    assert_sin_contrasena(respuesta.json())

    detalle = respuesta.json()
    assert "motivo_bloqueo" not in detalle
    assert "fecha_bloqueo" not in detalle
    assert "fecha_desbloqueo" not in detalle

    respuesta = cliente.delete(f"/usuarios/{USUARIO_ACTIVO_ID}")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"mensaje": "Usuario desactivado correctamente"}
    assert_sin_contrasena(respuesta.json())

    respuesta = cliente.put(
        f"/usuarios/{OTRO_ACTIVO_ID}/bloquear",
        json={"motivo": "  Fraude  "},
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["motivo_bloqueo"] == "Fraude"
    assert_sin_contrasena(respuesta.json())


def test_desbloquear_sin_token_devuelve_401(entorno):
    cliente, _, _ = entorno

    respuesta = cliente.put(
        f"/usuarios/{USUARIO_BLOQUEADO_ID}/desbloquear"
    )

    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "Token no proporcionado"


def test_desbloquear_usuario_no_admin_devuelve_403(entorno):
    cliente, app, _ = entorno
    autenticar_usuario(app)

    respuesta = cliente.put(
        f"/usuarios/{USUARIO_BLOQUEADO_ID}/desbloquear"
    )

    assert respuesta.status_code == 403
    assert_sin_contrasena(respuesta.json())


def test_desbloquear_usuario_inexistente_devuelve_404(entorno):
    cliente, app, _ = entorno
    autenticar_admin(app)

    respuesta = cliente.put(
        f"/usuarios/{USUARIO_INEXISTENTE_ID}/desbloquear"
    )

    assert respuesta.status_code == 404
    assert respuesta.json()["message"] == "Usuario no encontrado"
    assert_sin_contrasena(respuesta.json())


def test_desbloquear_activo_sin_bloqueo_devuelve_409_con_codigo(entorno):
    cliente, app, session_factory = entorno
    autenticar_admin(app)
    auditorias_antes = contar_auditorias(session_factory)

    respuesta = cliente.put(
        f"/usuarios/{USUARIO_ACTIVO_ID}/desbloquear"
    )

    assert respuesta.status_code == 409
    assert respuesta.json()["code"] == CODIGO_CUENTA_NO_BLOQUEADA
    assert respuesta.json()["message"] == (
        "La cuenta no se encuentra bloqueada ni desactivada"
    )
    assert_sin_contrasena(respuesta.json())
    assert contar_auditorias(session_factory) == auditorias_antes


def test_desbloquear_bloqueado_actualiza_limpia_y_audita(entorno):
    cliente, app, session_factory = entorno
    autenticar_admin(app)
    auditorias_antes = contar_auditorias(session_factory)

    respuesta = cliente.put(
        f"/usuarios/{USUARIO_BLOQUEADO_ID}/desbloquear"
    )

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert set(cuerpo) == {
        "id_usuario",
        "estado",
        "fecha_desbloqueo",
    }
    assert cuerpo["id_usuario"] == USUARIO_BLOQUEADO_ID
    assert cuerpo["estado"] == "ACTIVO"
    assert cuerpo["fecha_desbloqueo"] is not None
    assert_sin_contrasena(cuerpo)

    usuario = obtener_usuario(session_factory, USUARIO_BLOQUEADO_ID)
    assert usuario["estado"] == "ACTIVO"
    assert usuario["motivo_bloqueo"] is None
    assert usuario["fecha_bloqueo"] is None
    assert usuario["fecha_desbloqueo"] is not None
    assert usuario["intentos_fallidos"] == 0
    assert usuario["bloqueado_hasta"] is None

    assert contar_auditorias(session_factory) == auditorias_antes + 1
    auditoria = obtener_ultima_auditoria(session_factory)
    assert auditoria["id_admin"] == ADMIN_ID
    assert auditoria["accion"] == ACCION_DESBLOQUEAR_USUARIO
    assert auditoria["id_usuario_afectado"] == USUARIO_BLOQUEADO_ID
    assert "BLOQUEADO" in auditoria["detalle"]
    assert "Fraude" in auditoria["detalle"]


def test_desbloquear_inactivo_actualiza_y_audita(entorno):
    cliente, app, session_factory = entorno
    autenticar_admin(app)

    respuesta = cliente.put(
        f"/usuarios/{USUARIO_INACTIVO_ID}/desbloquear"
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "ACTIVO"
    assert_sin_contrasena(respuesta.json())

    usuario = obtener_usuario(session_factory, USUARIO_INACTIVO_ID)
    assert usuario["estado"] == "ACTIVO"
    assert usuario["motivo_bloqueo"] is None
    assert usuario["fecha_bloqueo"] is None
    assert usuario["intentos_fallidos"] == 0
    assert usuario["bloqueado_hasta"] is None

    auditoria = obtener_ultima_auditoria(session_factory)
    assert auditoria["accion"] == ACCION_DESBLOQUEAR_USUARIO
    assert "INACTIVO" in auditoria["detalle"]
    assert "Sin motivo" in auditoria["detalle"]


def test_desbloquear_activo_con_bloqueo_temporal_vigente(entorno):
    cliente, app, session_factory = entorno
    autenticar_admin(app)

    respuesta = cliente.put(
        f"/usuarios/{USUARIO_ACTIVO_TEMPORAL_ID}/desbloquear"
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "ACTIVO"
    assert_sin_contrasena(respuesta.json())

    usuario = obtener_usuario(session_factory, USUARIO_ACTIVO_TEMPORAL_ID)
    assert usuario["estado"] == "ACTIVO"
    assert usuario["intentos_fallidos"] == 0
    assert usuario["bloqueado_hasta"] is None

    auditoria = obtener_ultima_auditoria(session_factory)
    assert auditoria["accion"] == ACCION_DESBLOQUEAR_USUARIO
    assert "ACTIVO" in auditoria["detalle"]
    assert "bloqueo temporal por intentos fallidos" in auditoria["detalle"]
