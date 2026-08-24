from app.core.security.PasswordHasher import PasswordHasher
from app.core.security.roles import ROL_USUARIO, INDEPENDIENTE
from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.shared.exceptions.business_exceptions import EmailAlreadyExistsException


class CrearUsuario:

    def __init__(self, repository: UsuarioRepository, cuenta_repository: CuentaRepository):
        self.repository = repository
        self.cuenta_repository = cuenta_repository

    def execute(self, usuario_data):

        if self.repository.exists_by_email(usuario_data["correo"]):
            raise EmailAlreadyExistsException()

        usuario_data["contrasena"] = PasswordHasher.hash(
            usuario_data["contrasena"]
        )

        usuario_data["estado"] = "ACTIVO"
        usuario_data["id_rol"] = ROL_USUARIO
        usuario_data["id_tipo_usuario"] = INDEPENDIENTE

        usuario = self.repository.create(usuario_data)

        self.cuenta_repository.create({
            "saldo": 0,
            "estado": "ACTIVA",
            "id_usuario": usuario.id_usuario,
        })

        return usuario
