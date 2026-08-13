from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.security.auth import get_current_user, require_rol
from app.core.security.roles import ROL_ADMIN

from app.modules.usuario.infrastructure.repository.sql_usuario_repository import SqlUsuarioRepository
from app.modules.usuario.application.use_cases.crear_usuario import CrearUsuario
from app.modules.usuario.application.use_cases.obtener_usuario import ObtenerUsuariosUseCase
from app.modules.usuario.application.use_cases.obtener_usuario_por_id import ObtenerUsuarioPorIdUseCase
from app.modules.usuario.application.use_cases.actualizar_usuarios import ActualizarUsuarioUseCase
from app.modules.usuario.application.use_cases.eliminar_usuario import EliminarUsuarioUseCase

from app.modules.usuario.presentation.schema.usuario_schema import (
    UsuarioCreate,
    UsuarioResponse
)

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):

    caso_uso = CrearUsuario(SqlUsuarioRepository())

    return caso_uso.execute(
        db,
        usuario.model_dump()
    )

@router.get("/")
def obtener_usuarios(
    db: Session = Depends(get_db),
    current_user: object = Depends(require_rol(ROL_ADMIN))
):
    caso_uso = ObtenerUsuariosUseCase(
        SqlUsuarioRepository()
    )


    return caso_uso.execute(db)

@router.get("/{id_usuario}")
def obtener_usuario_por_id(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: object = Depends(get_current_user)
):

    caso_uso = ObtenerUsuarioPorIdUseCase(
        SqlUsuarioRepository()
    )

    return caso_uso.execute(
        db,
        id_usuario
    )

@router.put("/{id_usuario}")
def actualizar_usuario(
    id_usuario: int,
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: object = Depends(get_current_user)
):

    caso_uso = ActualizarUsuarioUseCase(
        SqlUsuarioRepository()
    )

    return caso_uso.execute(
        db,
        id_usuario,
        usuario.model_dump()
    )

@router.delete("/{id_usuario}")
def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: object = Depends(require_rol(ROL_ADMIN))
):

    caso_uso = EliminarUsuarioUseCase(
        SqlUsuarioRepository()
    )

    return caso_uso.execute(
        db,
        id_usuario
    )
