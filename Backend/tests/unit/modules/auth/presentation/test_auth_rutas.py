from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.auth.presentation.controller.auth_controller import (
    get_auth_controller,
)
from app.modules.auth.presentation.router.router import router
from app.shared.exceptions.handlers.auth_handlers import (
    register_auth_exception_handlers,
)


def crear_cliente():
    controller = Mock()
    controller.confirm_password_recovery.return_value = {"mensaje": "ok"}

    app = FastAPI()
    app.include_router(router)
    register_auth_exception_handlers(app)
    app.dependency_overrides[get_auth_controller] = lambda: controller

    return TestClient(app), controller


@pytest.mark.parametrize("codigo", ["12345", "1234567", "abcdef", ""])
def test_confirmar_recuperacion_codigo_con_formato_invalido_devuelve_422_sin_consumir_intentos(
    codigo,
):
    cliente, controller = crear_cliente()

    respuesta = cliente.post(
        "/auth/password-recovery/confirm",
        json={
            "correo": "usuario@test.com",
            "codigo": codigo,
            "nueva_contrasena": "ClaveNueva1!",
        },
    )

    assert respuesta.status_code == 422
    controller.confirm_password_recovery.assert_not_called()


def test_confirmar_recuperacion_acepta_codigo_de_seis_digitos():
    cliente, controller = crear_cliente()

    respuesta = cliente.post(
        "/auth/password-recovery/confirm",
        json={
            "correo": "usuario@test.com",
            "codigo": "000042",
            "nueva_contrasena": "ClaveNueva1!",
        },
    )

    assert respuesta.status_code == 200
    assert respuesta.json() == {"mensaje": "ok"}
    solicitud = controller.confirm_password_recovery.call_args.args[0]
    assert solicitud.codigo == "000042"
