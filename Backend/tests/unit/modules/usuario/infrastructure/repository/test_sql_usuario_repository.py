from types import SimpleNamespace

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.modules.usuario.infrastructure.model.usuario_model import UsuarioModel
from app.modules.usuario.infrastructure.repository.sql_usuario_repository import (
    RESTRICCION_CORREO_USUARIO,
    SqlUsuarioRepository,
    es_conflicto_de_correo,
)


class ErrorDelMotor(Exception):
    """Simula el error del motor: en Postgres el nombre va en `diag`."""

    def __init__(self, restriccion=None, mensaje="error de integridad"):
        super().__init__(mensaje)

        if restriccion:
            self.diag = SimpleNamespace(constraint_name=restriccion)


def sesion_sqlite():
    engine = create_engine("sqlite://")
    UsuarioModel.__table__.create(engine)

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()


def agregar_usuario(
    sesion,
    id_usuario,
    correo,
    nombres="Ana",
    apellidos="Perez",
    estado="ACTIVO",
    id_rol=2,
):
    sesion.add(
        UsuarioModel(
            id_usuario=id_usuario,
            nombres=nombres,
            apellidos=apellidos,
            correo=correo,
            contrasena="hash",
            estado=estado,
            id_rol=id_rol,
        )
    )


def test_es_conflicto_de_correo_con_el_nombre_de_la_restriccion():
    error = IntegrityError(
        "INSERT",
        {},
        ErrorDelMotor(RESTRICCION_CORREO_USUARIO),
    )

    assert es_conflicto_de_correo(error) is True


def test_es_conflicto_de_correo_con_otra_restriccion():
    error = IntegrityError("INSERT", {}, ErrorDelMotor("usuario_pkey"))

    assert es_conflicto_de_correo(error) is False


def test_es_conflicto_de_correo_por_el_mensaje_cuando_no_hay_diagnostico():
    error = IntegrityError(
        "INSERT",
        {},
        ErrorDelMotor(mensaje=f"duplicate key value {RESTRICCION_CORREO_USUARIO}"),
    )

    assert es_conflicto_de_correo(error) is True


def test_es_conflicto_de_correo_con_otro_error_de_integridad():
    error = IntegrityError(
        "INSERT",
        {},
        ErrorDelMotor(mensaje="viola la restricción usuario_estado_check"),
    )

    assert es_conflicto_de_correo(error) is False


def test_exists_by_email_ignora_mayusculas_y_espacios():
    sesion = sesion_sqlite()
    agregar_usuario(sesion, 1, "David@gmail.com")
    sesion.commit()

    repositorio = SqlUsuarioRepository(sesion)

    assert repositorio.exists_by_email("  david@GMAIL.com ") is True
    assert repositorio.exists_by_email("otro@gmail.com") is False
    assert repositorio.exists_by_email("") is False
    assert repositorio.exists_by_email(None) is False


def test_exists_by_email_puede_excluir_al_propio_usuario():
    sesion = sesion_sqlite()
    agregar_usuario(sesion, 1, "david@gmail.com")
    agregar_usuario(sesion, 2, "ana@gmail.com")
    sesion.commit()

    repositorio = SqlUsuarioRepository(sesion)

    assert repositorio.exists_by_email("david@gmail.com") is True
    assert repositorio.exists_by_email("david@gmail.com", excluir_id_usuario=1) is False
    assert repositorio.exists_by_email("ana@gmail.com", excluir_id_usuario=1) is True


def test_update_deja_el_cambio_en_la_transaccion_sin_confirmarlo():
    sesion = sesion_sqlite()
    agregar_usuario(sesion, 1, "ana@test.com")
    sesion.commit()

    repositorio = SqlUsuarioRepository(sesion)

    resultado = repositorio.update(1, {"nombres": "Ana Maria"})

    assert resultado.nombres == "Ana Maria"

    sesion.rollback()
    sesion.expire_all()

    assert sesion.get(UsuarioModel, 1).nombres == "Ana"


def test_update_se_guarda_cuando_el_llamador_confirma():
    sesion = sesion_sqlite()
    agregar_usuario(sesion, 1, "ana@test.com")
    sesion.commit()

    repositorio = SqlUsuarioRepository(sesion)

    repositorio.update(1, {"nombres": "Ana Maria", "correo": "ana.maria@test.com"})
    sesion.commit()
    sesion.expire_all()

    guardado = sesion.get(UsuarioModel, 1)

    assert guardado.nombres == "Ana Maria"
    assert guardado.correo == "ana.maria@test.com"


def test_update_devuelve_none_si_el_usuario_no_existe():
    sesion = sesion_sqlite()

    repositorio = SqlUsuarioRepository(sesion)

    assert repositorio.update(99, {"nombres": "Ana"}) is None


def test_listar_filtra_por_busqueda_estado_y_rol():
    sesion = sesion_sqlite()
    agregar_usuario(sesion, 1, "ana@test.com", nombres="Ana", apellidos="Perez")
    agregar_usuario(sesion, 2, "bruno@test.com", nombres="Bruno", apellidos="Diaz")
    agregar_usuario(
        sesion,
        3,
        "carla@test.com",
        nombres="Carla",
        apellidos="Perez",
        estado="INACTIVO",
        id_rol=1,
    )
    sesion.commit()

    repositorio = SqlUsuarioRepository(sesion)

    def listar(**filtros):
        return repositorio.listar({
            "buscar": None,
            "estado": None,
            "id_rol": None,
            "pagina": 1,
            "por_pagina": 10,
            **filtros,
        })

    items, total = listar()
    assert total == 3
    assert [usuario.id_usuario for usuario in items] == [1, 2, 3]

    items, total = listar(buscar="perez")
    assert total == 2
    assert [usuario.id_usuario for usuario in items] == [1, 3]

    items, total = listar(estado="INACTIVO")
    assert total == 1
    assert items[0].id_usuario == 3

    items, total = listar(id_rol=2)
    assert total == 2

    items, total = listar(buscar="carla@test.com")
    assert total == 1
    assert items[0].id_usuario == 3

    items, total = listar(buscar="   ")
    assert total == 3

    items, total = listar(buscar="nadie")
    assert total == 0
    assert items == []


def test_listar_pagina_y_devuelve_el_total_completo():
    sesion = sesion_sqlite()

    for numero in range(1, 6):
        agregar_usuario(sesion, numero, f"user{numero}@test.com")

    sesion.commit()

    repositorio = SqlUsuarioRepository(sesion)

    items, total = repositorio.listar({
        "buscar": None,
        "estado": None,
        "id_rol": None,
        "pagina": 2,
        "por_pagina": 2,
    })

    assert total == 5
    assert [usuario.id_usuario for usuario in items] == [3, 4]
