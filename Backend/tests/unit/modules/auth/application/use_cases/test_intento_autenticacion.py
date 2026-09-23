from datetime import datetime, timedelta, timezone

from app.modules.auth.domain.entity.intento_autenticacion import IntentoAutenticacion


def test_no_debe_bloquearse_con_menos_de_max_intentos():
    intento = IntentoAutenticacion(intentos_fallidos=2)

    assert intento.debe_bloquearse() is False


def test_debe_bloquearse_al_alcanzar_max_intentos():
    intento = IntentoAutenticacion(intentos_fallidos=3)

    assert intento.debe_bloquearse() is True


def test_no_esta_bloqueado_sin_fecha_bloqueo():
    intento = IntentoAutenticacion(intentos_fallidos=3, bloqueado_hasta=None)

    assert intento.esta_bloqueado() is False


def test_esta_bloqueado_con_fecha_futura():
    bloqueado_hasta = datetime.now(timezone.utc) + timedelta(minutes=15)
    intento = IntentoAutenticacion(intentos_fallidos=3, bloqueado_hasta=bloqueado_hasta)

    assert intento.esta_bloqueado() is True


def test_no_esta_bloqueado_con_fecha_pasada():
    bloqueado_hasta = datetime.now(timezone.utc) - timedelta(minutes=5)
    intento = IntentoAutenticacion(intentos_fallidos=3, bloqueado_hasta=bloqueado_hasta)

    assert intento.esta_bloqueado() is False