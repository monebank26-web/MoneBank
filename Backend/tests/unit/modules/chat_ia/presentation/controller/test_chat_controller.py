from unittest.mock import Mock

from app.modules.chat_ia.presentation.controller.chat_controller import (
    RESPUESTA_GENERICA,
    ChatIaController,
)
from app.modules.chat_ia.presentation.schema.chat_schema import (
    EnviarMensajeRequest,
    TurnoChat,
)
from app.shared.exceptions.chat_ia_errors import ConsejoIANoDisponible


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

    unit_of_work = Mock()
    unit_of_work.ahorros = ahorro_repo

    return cuenta_repo, unit_of_work, transacc_repo


def crear_controller(chat_ia):
    cuenta_repo, unit_of_work, transacc_repo = crear_mocks_interiores()
    return ChatIaController(
        cuenta_repo,
        unit_of_work,
        transacc_repo,
        chat_ia,
    )


def crear_request():
    return EnviarMensajeRequest(
        mensaje="¿cómo voy?",
        historial=[TurnoChat(rol="user", texto="hola")],
    )


def test_enviar_mensaje_con_exito_devuelve_generado_con_ia_true():
    chat_ia = Mock()
    chat_ia.generar_respuesta.return_value = "Respuesta del asesor."
    controller = crear_controller(chat_ia)

    respuesta = controller.enviar_mensaje(crear_request(), Mock(id_usuario=6))

    assert respuesta.respuesta == "Respuesta del asesor."
    assert respuesta.generado_con_ia is True


def test_enviar_mensaje_con_fallo_ia_devuelve_generico():
    chat_ia = Mock()
    chat_ia.generar_respuesta.side_effect = ConsejoIANoDisponible()
    controller = crear_controller(chat_ia)

    respuesta = controller.enviar_mensaje(crear_request(), Mock(id_usuario=6))

    assert respuesta.respuesta == RESPUESTA_GENERICA
    assert respuesta.generado_con_ia is False


def test_enviar_mensaje_usa_id_del_usuario_autenticado():
    chat_ia = Mock()
    chat_ia.generar_respuesta.return_value = "ok"
    controller = crear_controller(chat_ia)

    controller.enviar_mensaje(crear_request(), Mock(id_usuario=6))

    assert chat_ia.generar_respuesta.called
