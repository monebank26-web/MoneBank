from fastapi import APIRouter, Depends

from app.core.security.auth import get_current_user, require_rol
from app.core.security.roles import ROL_ADMIN

from app.modules.usuario.presentation.controller.usuario_controller import (
    UsuarioController,
    get_usuario_controller,
)
from app.modules.usuario.presentation.schema.usuario_schema import (
    BloqueoUsuarioRequest,
    BloqueoUsuarioResponse,
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(
    usuario: UsuarioCreate,
    controller: UsuarioController = Depends(get_usuario_controller),
):
    return controller.crear_usuario(usuario)


@router.get("/")
def obtener_usuarios(
    current_user: object = Depends(require_rol(ROL_ADMIN)),
    controller: UsuarioController = Depends(get_usuario_controller),
):
    return controller.obtener_usuarios(current_user)


@router.get("/{id_usuario}")
def obtener_usuario_por_id(
    id_usuario: int,
    current_user: object = Depends(get_current_user),
    controller: UsuarioController = Depends(get_usuario_controller),
):
    return controller.obtener_usuario_por_id(id_usuario, current_user)


@router.put("/{id_usuario}", response_model=UsuarioResponse)
def actualizar_usuario(
    id_usuario: int,
    usuario: UsuarioUpdate,
    current_user: object = Depends(get_current_user),
    controller: UsuarioController = Depends(get_usuario_controller),
):
    return controller.actualizar_usuario(id_usuario, usuario, current_user)


@router.delete("/{id_usuario}")
def eliminar_usuario(
    id_usuario: int,
    current_user: object = Depends(require_rol(ROL_ADMIN)),
    controller: UsuarioController = Depends(get_usuario_controller),
):
    return controller.eliminar_usuario(id_usuario, current_user)


@router.put("/{id_usuario}/bloquear", response_model=BloqueoUsuarioResponse)
def bloquear_usuario(
    id_usuario: int,
    datos: BloqueoUsuarioRequest,
    current_user: object = Depends(require_rol(ROL_ADMIN)),
    controller: UsuarioController = Depends(get_usuario_controller),
):
    return controller.bloquear_usuario(id_usuario, datos, current_user)
