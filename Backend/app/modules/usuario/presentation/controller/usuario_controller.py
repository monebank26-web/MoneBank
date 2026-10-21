from fastapi import Depends, HTTPException

from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work
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
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.modules.usuario.presentation.schema.usuario_schema import (
    BloqueoUsuarioRequest,
    UsuarioCreate,
    UsuarioUpdate,
)


class UsuarioController:

    def __init__(
        self,
        repository: UsuarioRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.unit_of_work = unit_of_work

    def crear_usuario(self, usuario: UsuarioCreate):
        caso_uso = CrearUsuario(self.repository, self.unit_of_work.cuentas)
        resultado = caso_uso.execute(usuario.model_dump())
        self.unit_of_work.commit()
        return resultado

    def obtener_usuarios(self, current_user):
        return ObtenerUsuariosUseCase(self.repository).execute()

    def obtener_usuario_por_id(self, id_usuario: int, current_user):
        return ObtenerUsuarioPorIdUseCase(self.repository).execute(id_usuario)

    def actualizar_usuario(
        self,
        id_usuario: int,
        usuario: UsuarioUpdate,
        current_user,
    ):
        if current_user.id_usuario != id_usuario:
            raise HTTPException(
                status_code=403,
                detail="No puedes modificar otro usuario",
            )

        caso_uso = ActualizarUsuarioUseCase(self.repository)

        try:
            resultado = caso_uso.execute(
                id_usuario,
                usuario.model_dump(exclude_unset=True),
            )
            self.unit_of_work.commit()
            return resultado
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al actualizar usuario: {str(e)}",
            )

    def eliminar_usuario(self, id_usuario: int, current_user):
        caso_uso = EliminarUsuarioUseCase(self.repository)
        resultado = caso_uso.execute(id_usuario)
        self.unit_of_work.commit()
        return resultado

    def bloquear_usuario(
        self,
        id_usuario: int,
        datos: BloqueoUsuarioRequest,
        current_user,
    ):
        caso_uso = BloquearUsuario(self.repository)
        resultado = caso_uso.execute(id_usuario, datos.motivo)
        self.unit_of_work.commit()
        return resultado


def get_usuario_controller(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> UsuarioController:
    return UsuarioController(unit_of_work.usuarios, unit_of_work)
