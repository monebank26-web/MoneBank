from app.core.dependencies.email_service import (
    EmailService,
    get_email_service as get_email_service_core,
)
from app.modules.auth.presentation.controller.auth_controller import (
    get_email_service as get_email_service_auth,
)


def test_auth_controller_reexporta_el_getter_compartido():
    assert get_email_service_auth is get_email_service_core


def test_get_email_service_crea_un_email_service():
    assert isinstance(get_email_service_core(), EmailService)
