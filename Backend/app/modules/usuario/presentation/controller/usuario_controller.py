from typing import Optional

from fastapi import Depends, HTTPException

from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work
from app.core.security.roles import ROL_ADMIN
from app.modules.usuario.application.use_cases.actualizar_usuarios import (
    ActualizarUsuarioUseCase,
)
from app.modules.usuario.application.use_cases.bloquear_usuario import BloquearUsuario
from app.modules.usuario.application.use_cases.crear_usuario import CrearUsuario
from app.modules.usuario.application.use_cases.inactivar_usuario import (
    InactivarUsuario,
)
from app.modules.usuario.application.use_cases.obtener_usuario import (
    ObtenerUsuariosUseCase,
)
from app.modules.usuario.application.use_cases.obtener_usuario_por_id import (
    ObtenerUsuarioPorIdUseCase,
)
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.modules.usuario.presentation.schema.usuario_schema import (
    BloqueoUsuarioRequest,
    UsuarioCreate,
    UsuarioUpdate,
)
from app.shared.exceptions.auth_errors import EmailAlreadyExistsException
from app.shared.exceptions.common import UsuarioNotFoundException


class UsuarioController:

    def __init__(
        self,
        repository: UsuarioRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.unit_of_work = unit_of_work

    def _puede_gestionar(self, current_user, id_usuario) -> bool:
        """El administrador gestiona a cualquiera; cada usuario, a sí mismo."""
        return (
            current_user.id_rol == ROL_ADMIN
            or current_user.id_usuario == id_usuario
        )

    def crear_usuario(self, usuario: UsuarioCreate):
        caso_uso = CrearUsuario(self.repository, self.unit_of_work.cuentas)

        try:
            resultado = caso_uso.execute(usuario.model_dump())
            self.unit_of_work.commit()
        except Exception:
            self.unit_of_work.rollback()
            raise

        return resultado

    def obtener_usuarios(self, current_user, filtros: Optional[dict] = None):
        caso_uso = ObtenerUsuariosUseCase(self.repository)

        return caso_uso.execute(filtros or {})

    def obtener_usuario_por_id(self, id_usuario: int, current_user):
        if not self._puede_gestionar(current_user, id_usuario):
            raise HTTPException(
                status_code=403,
                detail="No puedes ver otro usuario"
            )

        caso_uso = ObtenerUsuarioPorIdUseCase(self.repository)
        usuario = caso_uso.execute(id_usuario)

        if not usuario:
            raise UsuarioNotFoundException()

        return usuario

    def actualizar_usuario(
        self,
        id_usuario: int,
        usuario: UsuarioUpdate,
        current_user,
    ):
        if not self._puede_gestionar(current_user, id_usuario):
            raise HTTPException(
                status_code=403,
                detail="No puedes modificar otro usuario"
            )

        caso_uso = ActualizarUsuarioUseCase(
            self.repository,
            self.unit_of_work.registros_accion_admin,
        )

        try:
            resultado = caso_uso.execute(
                id_usuario,
                usuario.model_dump(exclude_unset=True),
                current_user.id_usuario,
            )
            # Un solo commit: la edición y su fila de auditoría son atómicas.
            self.unit_of_work.commit()
        except EmailAlreadyExistsException:
            self.unit_of_work.rollback()
            raise
        except Exception:
            self.unit_of_work.rollback()
            raise

        return resultado

    def eliminar_usuario(self, id_usuario: int, current_user):
        caso_uso = InactivarUsuario(
            self.repository,
            self.unit_of_work.registros_accion_admin,
        )

        try:
            caso_uso.execute(
                id_usuario,
                id_admin=current_user.id_usuario,
            )
            self.unit_of_work.commit()
        except Exception:
            self.unit_of_work.rollback()
            raise

        # La entidad trae `contrasena`; el endpoint solo expone este mensaje.
        return {"mensaje": "Usuario desactivado correctamente"}

    def bloquear_usuario(
        self,
        id_usuario: int,
        datos: BloqueoUsuarioRequest,
        current_user,
    ):
        caso_uso = BloquearUsuario(
            self.repository,
            self.unit_of_work.registros_accion_admin,
        )

        try:
            resultado = caso_uso.execute(
                id_usuario,
                datos.motivo,
                id_admin=current_user.id_usuario,
            )
            self.unit_of_work.commit()
        except Exception:
            self.unit_of_work.rollback()
            raise

        return resultado


def get_usuario_controller(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> UsuarioController:
    return UsuarioController(unit_of_work.usuarios, unit_of_work)
