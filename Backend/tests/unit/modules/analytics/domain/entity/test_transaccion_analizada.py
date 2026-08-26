from datetime import date, datetime

from app.modules.analytics.domain.entity.transaccion_analizada import (
    TransaccionAnalizada
)


def construir_entidad():
    return TransaccionAnalizada(
        id_transaccion=7,
        id_usuario=6,
        monto=50000.50,
        tipo_transaccion="GASTO",
        fecha=datetime(2026, 8, 24, 12, 30),
        descripcion=(
            "Almuerzo con amigos en el centro comercial y de postre "
            "fuimos por un helado"
        ),
        nombre_categoria="Restaurantes",
    )


def test_fecha_relativa_devuelve_hoy_cuando_es_el_mismo_dia():
    entidad = construir_entidad()

    assert entidad.fecha_relativa(hoy=date(2026, 8, 24)) == "hoy"


def test_fecha_relativa_devuelve_ayer_y_hace_n_dias():
    entidad = construir_entidad()

    assert entidad.fecha_relativa(hoy=date(2026, 8, 25)) == "ayer"
    assert entidad.fecha_relativa(hoy=date(2026, 8, 31)) == "hace 7 días"


def test_descripcion_resumida_trunca_cuando_supera_el_limite():
    entidad = construir_entidad()

    resumida = entidad.descripcion_resumida(20)

    assert resumida.endswith("...")
    assert len(resumida) <= 23
    assert resumida.startswith("Almuerzo")


def test_descripcion_resumida_no_cambia_cuando_es_corta():
    entidad = construir_entidad()
    entidad.descripcion = "Mercado"

    assert entidad.descripcion_resumida() == "Mercado"


def test_armar_contexto_sin_datos_personales():
    entidad = construir_entidad()
    stats_top = [
        {"nombre_categoria": "Restaurantes", "total": 150000.40},
    ]

    contexto = entidad.armar_contexto(
        total_gastado_mes=320000.75,
        top_categorias=stats_top,
        saldo_cuenta=1000000.89,
        hoy=date(2026, 8, 24),
    )

    assert contexto["monto"] == 50000
    assert contexto["categoria"] == "Restaurantes"
    assert contexto["fecha_relativa"] == "hoy"
    assert contexto["saldo_cuenta"] == 1000001
    assert contexto["total_gastado_mes"] == 320001
    assert contexto["top_categorias"] == [
        {"categoria": "Restaurantes", "total": 150000}
    ]
    assert len(contexto["descripcion"]) <= TransaccionAnalizada.MAX_DESCRIPCION + 3

    for dato_prohibido in ("id_usuario", "id_cuenta", "id_transaccion", "email", "nombres"):
        assert dato_prohibido not in contexto


def test_es_de_usuario_valida_pertenencia():
    entidad = construir_entidad()

    assert entidad.es_de_usuario(6) is True
    assert entidad.es_de_usuario(99) is False
