from datetime import datetime, timedelta, timezone

from app.core.config.settings import settings
from app.core.security.JwtManager import JwtManager


def test_create_token_inlinea_iat_y_orig_iat():
    token = JwtManager.create_token({"sub": "7"})
    payload = JwtManager.decode_token(token)

    assert payload["iat"] == payload["orig_iat"]
    assert (
        payload["exp"] - payload["iat"]
        == settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


def test_needs_renewal_solo_dentro_de_la_ventana():
    ahora = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

    fresco = {
        "exp": int((ahora + timedelta(minutes=60)).timestamp()),
        "orig_iat": int(ahora.timestamp()),
    }
    en_ventana = {
        "exp": int((ahora + timedelta(minutes=14)).timestamp()),
        "orig_iat": int((ahora - timedelta(minutes=46)).timestamp()),
    }
    vencido = {
        "exp": int((ahora - timedelta(minutes=1)).timestamp()),
        "orig_iat": int((ahora - timedelta(minutes=61)).timestamp()),
    }
    cerca_del_tope = {
        "exp": int((ahora + timedelta(minutes=14)).timestamp()),
        "orig_iat": int(
            (ahora - timedelta(hours=7, minutes=46)).timestamp()
        ),
    }

    assert JwtManager.needs_renewal(fresco, ahora) is False
    assert JwtManager.needs_renewal(en_ventana, ahora) is True
    assert JwtManager.needs_renewal(vencido, ahora) is False
    assert JwtManager.needs_renewal(cerca_del_tope, ahora) is False


def test_renew_token_devuelve_una_hora_desde_ahora():
    ahora = datetime.now(timezone.utc)
    payload = {
        "sub": "7",
        "orig_iat": int(
            (ahora - timedelta(minutes=46)).timestamp()
        ),
        "exp": int((ahora + timedelta(minutes=14)).timestamp()),
    }

    resultado = JwtManager.decode_token(
        JwtManager.renew_token(payload)
    )
    nuevo_exp = datetime.fromtimestamp(
        resultado["exp"], tz=timezone.utc
    )

    assert timedelta(minutes=59) < nuevo_exp - ahora < timedelta(minutes=61)
    assert resultado["orig_iat"] == payload["orig_iat"]


def test_renew_token_respeta_tope_absoluto_y_conserva_claims():
    ahora = datetime.now(timezone.utc)
    inicio = ahora - timedelta(hours=7, minutes=50)
    payload = {
        "sub": "7",
        "correo": "ana@example.com",
        "id_rol": 2,
        "orig_iat": int(inicio.timestamp()),
        "exp": int((ahora + timedelta(minutes=10)).timestamp()),
    }

    resultado = JwtManager.decode_token(
        JwtManager.renew_token(payload)
    )
    nuevo_exp = datetime.fromtimestamp(
        resultado["exp"], tz=timezone.utc
    )

    assert resultado["sub"] == "7"
    assert resultado["correo"] == "ana@example.com"
    assert resultado["id_rol"] == 2
    assert resultado["orig_iat"] == payload["orig_iat"]
    assert nuevo_exp <= inicio + timedelta(
        hours=settings.TOKEN_ABSOLUTE_MAX_HOURS
    )
    assert nuevo_exp > ahora
