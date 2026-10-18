from app.modules.cuenta.domain.entity.cuenta import Cuenta


def construir_cuenta(**overrides):
    datos = {
        "id_cuenta": 1,
        "saldo": 100000,
        "estado": Cuenta.ESTADO_ACTIVA,
        "id_usuario": 7,
    }
    datos.update(overrides)
    return Cuenta(**datos)


def test_es_estado_valido():
    assert Cuenta.es_estado_valido(Cuenta.ESTADO_ACTIVA) is True
    assert Cuenta.es_estado_valido(Cuenta.ESTADO_INACTIVA) is True
    assert Cuenta.es_estado_valido("OTRO") is False


def test_esta_activa():
    assert construir_cuenta().esta_activa() is True
    assert construir_cuenta(estado=Cuenta.ESTADO_INACTIVA).esta_activa() is False


def test_tiene_saldo_suficiente():
    cuenta = construir_cuenta(saldo=50000)

    assert cuenta.tiene_saldo_suficiente(50000) is True
    assert cuenta.tiene_saldo_suficiente(50001) is False


def test_descontar_actualiza_saldo_cuando_alcanza():
    cuenta = construir_cuenta(saldo=100000)

    resultado = cuenta.descontar(30000)

    assert resultado is True
    assert cuenta.saldo == 70000


def test_descontar_no_modifica_saldo_si_no_alcanza():
    cuenta = construir_cuenta(saldo=1000)

    resultado = cuenta.descontar(5000)

    assert resultado is False
    assert cuenta.saldo == 1000


def test_acreditar_aumenta_saldo():
    cuenta = construir_cuenta(saldo=1000)

    cuenta.acreditar(2500)

    assert cuenta.saldo == 3500


def test_fecha_creacion_se_asigna_por_defecto():
    cuenta = construir_cuenta()

    assert cuenta.fecha_creacion is not None
