from fastapi import Depends, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from jose import JWTError
from jose.exceptions import ExpiredSignatureError

from app.core.database.connection import get_db
from app.core.security.JwtManager import JwtManager
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.modules.usuario.infrastructure.repository.sql_usuario_repository import SqlUsuarioRepository
from app.shared.constants.estados import es_bloqueado, es_inactivo
from app.shared.exceptions.auth_errors import (
    CuentaBloqueadaException,
    CuentaInactivaException,
    TokenExpiradoException,
    TokenInvalidoException,
)


security = HTTPBearer(auto_error=False)


def get_usuario_repository(
    db=Depends(get_db),
) -> UsuarioRepository:
    return SqlUsuarioRepository(db)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    repository: UsuarioRepository = Depends(get_usuario_repository),
    response: Response = None,
):

    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Token no proporcionado"
        )

    token = credentials.credentials

    try:
        payload = JwtManager.decode_token(token)
    except ExpiredSignatureError:
        raise TokenExpiradoException()
    except JWTError:
        raise TokenInvalidoException()

    usuario = repository.get_by_id(int(payload["sub"]))

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    if es_bloqueado(usuario.estado):
        raise CuentaBloqueadaException()

    if es_inactivo(usuario.estado):
        raise CuentaInactivaException()

    if response is not None and JwtManager.needs_renewal(payload):
        response.headers["X-Token-Renovado"] = JwtManager.renew_token(payload)

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
