from datetime import datetime, timedelta, timezone

from app.core.constants import MAX_INTENTOS, MINUTOS_BLOQUEO
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


def test_registrar_intento_fallido_sin_bloqueo_bloquea_al_llegar_a_max(reloj_fijo):
    intento = IntentoAutenticacion(intentos_fallidos=2)

    intento.registrar_intento_fallido()

    assert intento.intentos_fallidos == MAX_INTENTOS
    assert intento.bloqueado_hasta == reloj_fijo + timedelta(
        minutes=MINUTOS_BLOQUEO
    )


def test_registrar_intento_fallido_tras_bloqueo_vencido_reinicia_el_contador(
    reloj_fijo,
):
    intento = IntentoAutenticacion(
        intentos_fallidos=3,
        bloqueado_hasta=reloj_fijo - timedelta(minutes=1),
    )

    intento.registrar_intento_fallido()

    assert intento.intentos_fallidos == 1
    assert intento.bloqueado_hasta is None