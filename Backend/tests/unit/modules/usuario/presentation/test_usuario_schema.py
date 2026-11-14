import pytest
from pydantic import ValidationError

from app.modules.usuario.presentation.schema.usuario_schema import (
    BloqueoUsuarioRequest,
)
from app.shared.constants.motivo_bloqueo import DESCRIPCION_MOTIVO_BLOQUEO


def test_bloqueo_request_recorta_los_espacios_del_motivo():
    assert BloqueoUsuarioRequest(motivo="  Fraude  ").motivo == "Fraude"


def test_bloqueo_request_permite_el_motivo_ausente():
    assert BloqueoUsuarioRequest().motivo is None


def test_bloqueo_request_acepta_255_caracteres():
    assert len(BloqueoUsuarioRequest(motivo="x" * 255).motivo) == 255


def test_bloqueo_request_rechaza_256_caracteres():
    with pytest.raises(ValidationError):
        BloqueoUsuarioRequest(motivo="x" * 256)


def test_bloqueo_request_documenta_la_restriccion_del_motivo():
    descripcion = BloqueoUsuarioRequest.model_fields["motivo"].description

    assert descripcion == DESCRIPCION_MOTIVO_BLOQUEO
    assert "Obligatorio" in descripcion
    assert "Mínimo 5 caracteres" in descripcion
    assert "máximo 255" in descripcion
