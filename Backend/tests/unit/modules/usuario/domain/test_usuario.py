from datetime import datetime, timedelta, timezone

from app.modules.usuario.domain.entity.usuario import Usuario
from app.shared.constants.estados import ESTADO_ACTIVO


def crear_usuario(bloqueado_hasta=None):
    return Usuario(
        id_usuario=1,
        nombres="Ana",
        apellidos="Perez",
        correo="ana@example.com",
        contrasena="hash",
        estado=ESTADO_ACTIVO,
        id_rol=2,
        id_tipo_usuario=3,
        bloqueado_hasta=bloqueado_hasta,
    )


def test_bloqueo_temporal_es_falso_sin_fecha():
    usuario = crear_usuario()

    assert usuario.bloqueo_temporal is False


def test_bloqueo_temporal_es_verdadero_si_la_fecha_esta_vigente():
    usuario = crear_usuario(
        datetime.now(timezone.utc) + timedelta(minutes=5)
    )

    assert usuario.bloqueo_temporal is True


def test_bloqueo_temporal_es_falso_si_la_fecha_ya_paso():
    usuario = crear_usuario(
        datetime.now(timezone.utc) - timedelta(seconds=1)
    )

    assert usuario.bloqueo_temporal is False
