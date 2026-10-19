from unittest.mock import Mock

from app.modules.admin.infrastructure.model.registro_accion_admin_model import (
    RegistroAccionAdminModel,
)
from app.modules.admin.infrastructure.repository.sql_registro_accion_admin_repository import (
    SqlRegistroAccionAdminRepository,
)
from app.shared.constants.acciones import (
    ACCION_BLOQUEAR_USUARIO,
    ACCION_DESACTIVAR_USUARIO,
)


def test_registrar_crea_la_fila_y_hace_commit():
    db = Mock()
    repositorio = SqlRegistroAccionAdminRepository(db)

    registro = repositorio.registrar(
        id_admin=1,
        accion=ACCION_BLOQUEAR_USUARIO,
        id_usuario_afectado=7,
        detalle="Incumplimiento de normas",
    )

    assert isinstance(registro, RegistroAccionAdminModel)
    assert registro.id_admin == 1
    assert registro.accion == ACCION_BLOQUEAR_USUARIO
    assert registro.id_usuario_afectado == 7
    assert registro.detalle == "Incumplimiento de normas"

    db.add.assert_called_once_with(registro)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(registro)


def test_registrar_permite_accion_sin_usuario_afectado_ni_detalle():
    db = Mock()
    repositorio = SqlRegistroAccionAdminRepository(db)

    registro = repositorio.registrar(
        id_admin=1,
        accion=ACCION_DESACTIVAR_USUARIO,
    )

    assert registro.id_usuario_afectado is None
    assert registro.detalle is None
    assert registro.accion == ACCION_DESACTIVAR_USUARIO


def test_listar_consulta_el_modelo_y_limita_el_resultado():
    db = Mock()
    repositorio = SqlRegistroAccionAdminRepository(db)

    repositorio.listar(limite=10)

    db.query.assert_called_once_with(RegistroAccionAdminModel)

    consulta = db.query.return_value
    consulta.order_by.assert_called_once()
    consulta.order_by.return_value.limit.assert_called_once_with(10)
    consulta.order_by.return_value.limit.return_value.all.assert_called_once()
