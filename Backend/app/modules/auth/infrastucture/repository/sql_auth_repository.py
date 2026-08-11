from app.modules.auth.domain.interface.auth_repository import AuthRepository
from app.modules.usuario.infrastucture.model import UsuarioModel


class SqlAuthRepository(AuthRepository):

    def login(self, db, correo):
        return (
            db.query(UsuarioModel)
            .filter(UsuarioModel.correo == correo)
            .first()
        )