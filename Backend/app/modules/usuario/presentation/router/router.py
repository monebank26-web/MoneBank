from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security.auth import get_current_user, require_rol
from app.core.security.roles import ROL_ADMIN
from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work

from app.modules.usuario.infrastructure.repository.sql_usuario_repository import SqlUsuarioRepository
from app.modules.usuario.application.use_cases.crear_usuario import CrearUsuario
from app.modules.usuario.application.use_cases.obtener_usuario import ObtenerUsuariosUseCase
from app.modules.usuario.application.use_cases.obtener_usuario_por_id import ObtenerUsuarioPorIdUseCase
from app.modules.usuario.application.use_cases.actualizar_usuarios import ActualizarUsuarioUseCase
from app.modules.usuario.application.use_cases.eliminar_usuario import EliminarUsuarioUseCase
from app.modules.usuario.application.use_cases.bloquear_usuario import BloquearUsuario

from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository

from app.modules.usuario.presentation.schema.usuario_schema import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
    BloqueoUsuarioRequest,
    BloqueoUsuarioResponse,
)


from app.core.database.connection import get_db



router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


def get_usuario_repository(
    db: Session = Depends(get_db)
) -> UsuarioRepository:
    return SqlUsuarioRepository(db)


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(
    usuario: UsuarioCreate,
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
):
    caso_uso = CrearUsuario(unit_of_work.usuarios, unit_of_work.cuentas)
    resultado = caso_uso.execute(usuario.model_dump())
    unit_of_work.commit()
    return resultado


@router.get("/")
def obtener_usuarios(
    repository: UsuarioRepository = Depends(get_usuario_repository),
    current_user: object = Depends(require_rol(ROL_ADMIN)),
):
    caso_uso = ObtenerUsuariosUseCase(repository)
    return caso_uso.execute()


@router.get("/{id_usuario}")
def obtener_usuario_por_id(
    id_usuario: int,
    repository: UsuarioRepository = Depends(get_usuario_repository),
    current_user: object = Depends(get_current_user),
):
    caso_uso = ObtenerUsuarioPorIdUseCase(repository)
    return caso_uso.execute(id_usuario)


@router.put("/{id_usuario}", response_model=UsuarioResponse)
def actualizar_usuario(
    id_usuario: int,
    usuario: UsuarioUpdate,
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    current_user: object = Depends(get_current_user),
):
    if current_user.id_usuario != id_usuario:
        raise HTTPException(
            status_code=403,
            detail="No puedes modificar otro usuario"
        )

    caso_uso = ActualizarUsuarioUseCase(unit_of_work.usuarios)

    try:
        resultado = caso_uso.execute(
            id_usuario,
            usuario.model_dump(exclude_unset=True)
        )
        unit_of_work.commit()
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar usuario: {str(e)}"
        )

@router.delete("/{id_usuario}")
def eliminar_usuario(
    id_usuario: int,
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    current_user: object = Depends(require_rol(ROL_ADMIN)),
):
    caso_uso = EliminarUsuarioUseCase(unit_of_work.usuarios)
    resultado = caso_uso.execute(id_usuario)
    unit_of_work.commit()
    return resultado


@router.put("/{id_usuario}/bloquear", response_model=BloqueoUsuarioResponse)
def bloquear_usuario(
    id_usuario: int,
    datos: BloqueoUsuarioRequest,
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    current_user: object = Depends(require_rol(ROL_ADMIN)),
):
    caso_uso = BloquearUsuario(unit_of_work.usuarios)
    resultado = caso_uso.execute(id_usuario, datos.motivo)
    unit_of_work.commit()
    return resultado
