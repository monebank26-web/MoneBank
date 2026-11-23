from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.modules.auth.infrastructure.model.reset_token_model import (
    ResetTokenModel,
)
from app.modules.auth.infrastructure.repository.sql_auth_repository import (
    SqlAuthRepository,
)
from app.modules.usuario.infrastructure.model.usuario_model import UsuarioModel


def sesion_sqlite():
    engine = create_engine("sqlite://")
    UsuarioModel.__table__.create(engine)
    ResetTokenModel.__table__.create(engine)

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()


def agregar_usuarios(sesion):
    for id_usuario, correo in ((1, "uno@test.com"), (2, "dos@test.com")):
        sesion.add(
            UsuarioModel(
                id_usuario=id_usuario,
                nombres="Ana",
                apellidos="Perez",
                correo=correo,
                contrasena="hash",
                estado="ACTIVO",
                id_rol=2,
            )
        )

    sesion.commit()


def repositorio_con_usuarios():
    sesion = sesion_sqlite()
    agregar_usuarios(sesion)
    return SqlAuthRepository(sesion, None), sesion


def test_find_latest_recovery_token_devuelve_el_ultimo_del_usuario():
    repositorio, _ = repositorio_con_usuarios()
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=15)

    primero = repositorio.create_recovery_token(1, "hash-uno", expiracion)
    segundo = repositorio.create_recovery_token(1, "hash-dos", expiracion)
    repositorio.create_recovery_token(2, "hash-otro-usuario", expiracion)

    ultimo = repositorio.find_latest_recovery_token(1)

    assert ultimo is not None
    assert ultimo.id == segundo.id
    assert ultimo.id != primero.id
    assert ultimo.token_hash == "hash-dos"


def test_find_active_recovery_token_ignora_usados_y_expirados():
    repositorio, _ = repositorio_con_usuarios()
    ahora = datetime.now(timezone.utc)

    usado = repositorio.create_recovery_token(
        1, "hash-usado", ahora + timedelta(minutes=15)
    )
    repositorio.invalidate_token(usado.id)
    assert repositorio.find_active_recovery_token(1) is None

    repositorio.create_recovery_token(
        1, "hash-expirado", ahora - timedelta(minutes=1)
    )
    assert repositorio.find_active_recovery_token(1) is None

    activo = repositorio.create_recovery_token(
        1, "hash-activo", ahora + timedelta(minutes=15)
    )
    encontrado = repositorio.find_active_recovery_token(1)

    assert encontrado is not None
    assert encontrado.id == activo.id
    assert encontrado.token_hash == "hash-activo"


def test_find_valid_token_busca_por_usuario_y_hash():
    repositorio, _ = repositorio_con_usuarios()
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=15)
    repositorio.create_recovery_token(1, "hash-uno", expiracion)
    repositorio.create_recovery_token(2, "hash-dos", expiracion)

    encontrado = repositorio.find_valid_token(1, "hash-uno")

    assert encontrado is not None
    assert encontrado.usuario_id == 1
    assert repositorio.find_valid_token(2, "hash-uno") is None
    assert repositorio.find_valid_token(1, "hash-inexistente") is None


def test_find_valid_token_ignora_usados_y_expirados():
    repositorio, _ = repositorio_con_usuarios()
    ahora = datetime.now(timezone.utc)

    usado = repositorio.create_recovery_token(
        1, "hash-usado", ahora + timedelta(minutes=15)
    )
    repositorio.invalidate_token(usado.id)
    assert repositorio.find_valid_token(1, "hash-usado") is None

    repositorio.create_recovery_token(
        1, "hash-expirado", ahora - timedelta(minutes=1)
    )
    assert repositorio.find_valid_token(1, "hash-expirado") is None


def test_exists_recovery_token_hash_y_actualizacion_de_intentos():
    repositorio, _ = repositorio_con_usuarios()
    token = repositorio.create_recovery_token(
        1,
        "hash-activo",
        datetime.now(timezone.utc) + timedelta(minutes=15),
    )

    assert repositorio.exists_recovery_token_hash("hash-activo") is True
    assert repositorio.exists_recovery_token_hash("hash-inexistente") is False

    actualizado = repositorio.update_recovery_token_attempts(
        token.id, 4, False
    )

    assert actualizado.intentos_fallidos == 4
    assert actualizado.usado is False

    agotado = repositorio.update_recovery_token_attempts(token.id, 5, True)

    assert agotado.intentos_fallidos == 5
    assert agotado.usado is True
    assert repositorio.find_active_recovery_token(1) is None


def test_update_recovery_token_attempts_devuelve_none_si_no_existe():
    repositorio, _ = repositorio_con_usuarios()

    assert repositorio.update_recovery_token_attempts(999, 1, False) is None


def test_register_failed_attempt_tras_bloqueo_vencido_reinicia_el_contador(
    reloj_fijo,
):
    usuario = SimpleNamespace(
        intentos_fallidos=3,
        bloqueado_hasta=reloj_fijo - timedelta(minutes=1),
    )
    usuario_repository = Mock()
    usuario_repository.get_by_id.return_value = usuario
    repositorio = SqlAuthRepository(Mock(), usuario_repository)

    repositorio.register_failed_attempt(1)

    usuario_repository.update_auth_fields.assert_called_once_with(1, 1, None)
