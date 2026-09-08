from unittest.mock import Mock

import pytest

from app.modules.chat_ia.presentation.router.router import (
    RESPUESTA_GENERICA,
    _armar_respuesta,
)
from app.modules.chat_ia.presentation.schema.chat_schema import TurnoChat
from app.shared.exceptions.business_exceptions import ConsejoIANoDisponible


def crear_mocks_interiores():
    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta.saldo = 1000000.50
    cuenta_repo = Mock()
    cuenta_repo.get_cuenta_por_usuario.return_value = cuenta

    ahorro_repo = Mock()
    ahorro_repo.get_metas_activas.return_value = []
    ahorro_repo.get_by_cuenta_y_tipo.return_value = []

    transacc_repo = Mock()
    transacc_repo.sumar_ingresos.return_value = 100000
    transacc_repo.sumar_gastos.return_value = 40000
    transacc_repo.top_categorias.return_value = []

    return cuenta_repo, ahorro_repo, transacc_repo


def test_armar_respuesta_con_exito_devuelve_generado_con_ia_true():
    cuenta_repo, ahorro_repo, transacc_repo = crear_mocks_interiores()
    chat_ia = Mock()
    chat_ia.generar_respuesta.return_value = "Respuesta del asesor."

    respuesta = _armar_respuesta(
        mensaje="¿cómo voy?",
        historial=[TurnoChat(rol="user", texto="hola")],
        id_usuario=6,
        cuenta_repo=cuenta_repo,
        ahorro_repo=ahorro_repo,
        transacc_repo=transacc_repo,
        chat_ia=chat_ia,
    )

    assert respuesta.respuesta == "Respuesta del asesor."
    assert respuesta.generado_con_ia is True


def test_armar_respuesta_con_fallo_ia_devuelve_generico():
    cuenta_repo, ahorro_repo, transacc_repo = crear_mocks_interiores()
    chat_ia = Mock()
    chat_ia.generar_respuesta.side_effect = ConsejoIANoDisponible()

    respuesta = _armar_respuesta(
        mensaje="¿cómo voy?",
        historial=[TurnoChat(rol="user", texto="hola")],
        id_usuario=6,
        cuenta_repo=cuenta_repo,
        ahorro_repo=ahorro_repo,
        transacc_repo=transacc_repo,
        chat_ia=chat_ia,
    )

    assert respuesta.respuesta == RESPUESTA_GENERICA
    assert respuesta.generado_con_ia is False
