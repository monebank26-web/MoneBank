from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from jose import JWTError

from app.core.database.connection import get_db
from app.core.security.JwtManager import JwtManager
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.modules.usuario.infrastructure.repository.sql_usuario_repository import SqlUsuarioRepository


security = HTTPBearer(auto_error=False)


def get_usuario_repository(
    db=Depends(get_db),
) -> UsuarioRepository:
    return SqlUsuarioRepository(db)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    repository: UsuarioRepository = Depends(get_usuario_repository),
):

    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Token no proporcionado"
        )

    token = credentials.credentials

    try:
        payload = JwtManager.decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )

    usuario = repository.get_by_id(int(payload["sub"]))

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    return usuario


def require_rol(*roles):

    def depender(current_user=Depends(get_current_user)):
        if current_user.id_rol not in roles:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para esta acción"
            )
        return current_user

    return depender
