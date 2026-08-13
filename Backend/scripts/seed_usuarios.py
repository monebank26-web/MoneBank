from datetime import date

from app.core.database.connection import SessionLocal
from app.core.security.PasswordHasher import PasswordHasher
from app.modules.usuario.application.use_cases.crear_usuario import CrearUsuario
from app.modules.usuario.infrastructure.model.usuario_model import UsuarioModel


USUARIOS = [
    {
        "nombres": "brayan",
        "apellidos": "reyes",
        "correo": "bryan@gmail.com",
        "contrasena": "1234",
        "fecha_creacion": date(2026, 6, 16),
        "estado": "ACTIVO",
        "id_rol": 1,
        "id_tipo_usuario": 3,
    },
    {
        "nombres": "David",
        "apellidos": "Camacho",
        "correo": "David@gmail.com",
        "contrasena": "123456789",
        "fecha_creacion": date(2026, 6, 16),
        "estado": "ACTIVO",
        "id_rol": 1,
        "id_tipo_usuario": 1,
    },
    {
        "nombres": "daniel",
        "apellidos": "castro",
        "correo": "Daniflow@gmail.com",
        "contrasena": "123456789",
        "fecha_creacion": date(2026, 6, 16),
        "estado": "ACTIVO",
        "id_rol": 1,
        "id_tipo_usuario": 1,
    },
    {
        "nombres": "supapa",
        "apellidos": "Sin apellido",
        "correo": "Dw@gmail.com",
        "contrasena": "123456789",
        "fecha_creacion": date(2026, 6, 16),
        "estado": "ACTIVO",
        "id_rol": 1,
        "id_tipo_usuario": 1,
    },
    {
        "nombres": "teto",
        "apellidos": "lindarte",
        "correo": "tetocanticus@gmail.com",
        "contrasena": "12345",
        "fecha_creacion": date(2026, 6, 17),
        "estado": "ACTIVO",
        "id_rol": 1,
        "id_tipo_usuario": 3,
    },
    {
        "nombres": "triple",
        "apellidos": "t",
        "correo": "t@gmail.com",
        "contrasena": "6767",
        "fecha_creacion": date(2026, 6, 17),
        "estado": "ACTIVO",
        "id_rol": 1,
        "id_tipo_usuario": 1,
    },
    {
        "nombres": "Nanifoods",
        "apellidos": "Sin apellido",
        "correo": "nanifoods@gmail.com",
        "contrasena": "12345",
        "fecha_creacion": date(2026, 6, 17),
        "estado": "ACTIVO",
        "id_rol": 1,
        "id_tipo_usuario": 1,
    },
]


def registrar_o_actualizar():
    db = SessionLocal()
    caso_uso = CrearUsuario()
    actualizados = []
    creados = []

    try:
        for datos in USUARIOS:
            existe = (
                db.query(UsuarioModel)
                .filter(UsuarioModel.correo == datos["correo"])
                .first()
            )

            if existe:
                existe.contrasena = PasswordHasher.hash(datos["contrasena"])
                existe.estado = datos["estado"]
                existe.id_rol = datos["id_rol"]
                existe.id_tipo_usuario = datos["id_tipo_usuario"]
                actualizados.append(datos["correo"])
            else:
                datos_registro = {
                    key: value
                    for key, value in datos.items()
                }
                caso_uso.execute(db, datos_registro)
                creados.append(datos["correo"])

        db.commit()

        print(f"Usuarios actualizados (password re-hasheada): {actualizados}")
        print(f"Usuarios creados: {creados}")

    finally:
        db.close()


def listar_usuarios():
    db = SessionLocal()

    try:
        usuarios = (
            db.query(UsuarioModel)
            .order_by(UsuarioModel.id_usuario)
            .all()
        )

        print("\n=== USUARIOS EN BD ===")
        print(
            f"{'ID':<4} {'Nombres':<12} {'Apellidos':<14} "
            f"{'Correo':<28} {'Hash':<20} {'Rol':<4} {'Tipo':<5}"
        )
        print("-" * 100)

        for u in usuarios:
            hash_corto = (u.contrasena[:17] + "...") if u.contrasena else ""
            print(
                f"{u.id_usuario:<4} {u.nombres:<12} {u.apellidos:<14} "
                f"{u.correo:<28} {hash_corto:<20} {u.id_rol:<4} {u.id_tipo_usuario:<5}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    registrar_o_actualizar()
    listar_usuarios()
