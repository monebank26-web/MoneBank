from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work
from app.core.security.auth import get_current_user, require_rol
from app.core.security.roles import ROL_ADMIN
from app.shared.constants.estados import PATRON_ESTADO_USUARIO
from app.shared.exceptions.auth_errors import EmailAlreadyExistsException
from app.shared.exceptions.common import UsuarioNotFoundException

from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.modules.usuario.infrastructure.repository.sql_usuario_repository import (
    SqlUsuarioRepository,
)
from app.modules.usuario.application.use_cases.actualizar_usuarios import (
    ActualizarUsuarioUseCase,
)
from app.modules.usuario.application.use_cases.bloquear_usuario import BloquearUsuario
from app.modules.usuario.application.use_cases.crear_usuario import CrearUsuario
from app.modules.usuario.application.use_cases.eliminar_usuario import (
    EliminarUsuarioUseCase,
)
from app.modules.usuario.application.use_cases.obtener_usuario import (
    ObtenerUsuariosUseCase,
)
from app.modules.usuario.application.use_cases.obtener_usuario_por_id import (
    ObtenerUsuarioPorIdUseCase,
)
from app.modules.usuario.presentation.schema.usuario_schema import (
    BloqueoUsuarioRequest,
    BloqueoUsuarioResponse,
    UsuarioCreate,
    UsuarioListResponse,
    UsuarioResponse,
    UsuarioUpdate,
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


def get_usuario_repository(
    db: Session = Depends(get_db)
) -> UsuarioRepository:
    return SqlUsuarioRepository(db)


def _puede_gestionar(current_user, id_usuario) -> bool:
    """El administrador gestiona a cualquiera; cada usuario, a sí mismo."""
    return (
        current_user.id_rol == ROL_ADMIN
        or current_user.id_usuario == id_usuario
    )


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(
    usuario: UsuarioCreate,
    repository: UsuarioRepository = Depends(get_usuario_repository),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
):
    caso_uso = CrearUsuario(repository, unit_of_work.cuentas)
    resultado = caso_uso.execute(usuario.model_dump())
    unit_of_work.commit()
    return resultado


@router.get("/", response_model=UsuarioListResponse)
def obtener_usuarios(
    buscar: Optional[str] = Query(
        None,
        max_length=100,
        description="Busca por nombres, apellidos o correo",
    ),
    estado: Optional[str] = Query(
        None,
        pattern=PATRON_ESTADO_USUARIO,
        description="Filtra por estado del usuario",
    ),
    id_rol: Optional[int] = Query(None, ge=1),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=100),
    repository: UsuarioRepository = Depends(get_usuario_repository),
    current_user: object = Depends(require_rol(ROL_ADMIN)),
):
    caso_uso = ObtenerUsuariosUseCase(repository)

    return caso_uso.execute({
        "buscar": buscar,
        "estado": estado,
        "id_rol": id_rol,
        "pagina": pagina,
        "por_pagina": por_pagina,
    })


@router.get("/{id_usuario}", response_model=UsuarioResponse)
def obtener_usuario_por_id(
    id_usuario: int,
    repository: UsuarioRepository = Depends(get_usuario_repository),
    current_user: object = Depends(get_current_user),
):
    if not _puede_gestionar(current_user, id_usuario):
        raise HTTPException(
            status_code=403,
            detail="No puedes ver otro usuario"
        )

    caso_uso = ObtenerUsuarioPorIdUseCase(repository)
    usuario = caso_uso.execute(id_usuario)

    if not usuario:
        raise UsuarioNotFoundException()

    return usuario


@router.put("/{id_usuario}", response_model=UsuarioResponse)
def actualizar_usuario(
    id_usuario: int,
    usuario: UsuarioUpdate,
    repository: UsuarioRepository = Depends(get_usuario_repository),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    current_user: object = Depends(get_current_user),
):
    if not _puede_gestionar(current_user, id_usuario):
        raise HTTPException(
            status_code=403,
            detail="No puedes modificar otro usuario"
        )

    caso_uso = ActualizarUsuarioUseCase(
        repository,
        unit_of_work.registros_accion_admin,
    )

    try:
        resultado = caso_uso.execute(
            id_usuario,
            usuario.model_dump(exclude_unset=True),
            current_user.id_usuario,
        )
        # Un solo commit: la edición y su fila de auditoría son atómicas.
        unit_of_work.commit()
    except EmailAlreadyExistsException:
        unit_of_work.rollback()
        raise
    except Exception:
        unit_of_work.rollback()
        raise

    return resultado


@router.delete("/{id_usuario}")
def eliminar_usuario(
    id_usuario: int,
    repository: UsuarioRepository = Depends(get_usuario_repository),
    current_user: object = Depends(require_rol(ROL_ADMIN)),
):
    caso_uso = EliminarUsuarioUseCase(repository)
    return caso_uso.execute(id_usuario)


@router.put("/{id_usuario}/bloquear", response_model=BloqueoUsuarioResponse)
def bloquear_usuario(
    id_usuario: int,
    datos: BloqueoUsuarioRequest,
    repository: UsuarioRepository = Depends(get_usuario_repository),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    current_user: object = Depends(require_rol(ROL_ADMIN)),
):
    caso_uso = BloquearUsuario(repository)
    resultado = caso_uso.execute(id_usuario, datos.motivo)
    # El repositorio ya no confirma: la ruta es la dueña del commit.
    unit_of_work.commit()

    return resultado
