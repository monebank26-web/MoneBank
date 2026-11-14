from app.modules.programacion_ahorro.domain.entity.programacion_ahorro import ProgramacionAhorro
from app.modules.programacion_ahorro.domain.interface.programacion_repository import ProgramacionAhorroRepository
from app.shared.exceptions.ahorro_errors import (
    EstadoInvalido,
    ProgramacionNoEncontrada,
)
from app.shared.exceptions.common import CuentaNoEncontrada


class ActualizarEstadoUseCase:

    def __init__(
        self,
        repository: ProgramacionAhorroRepository,
        cuenta_repository,
        ahorro_repository,
    ):
        self.repository = repository
        self.cuenta_repository = cuenta_repository
        self.ahorro_repository = ahorro_repository

    def execute(self, id_usuario, programacion_id: int, nuevo_estado: str):

        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        if not ProgramacionAhorro.es_estado_valido(nuevo_estado):
            raise EstadoInvalido()

        programacion = self.repository.get_by_id(programacion_id)

        if not self._pertenece_al_usuario(programacion, cuenta):
            raise ProgramacionNoEncontrada()

        actualizada = self.repository.update_estado(programacion_id, nuevo_estado)

        if not actualizada:
            raise ProgramacionNoEncontrada()

        return actualizada

    def _pertenece_al_usuario(self, programacion, cuenta):
        if not programacion:
            return False

        ahorro = self.ahorro_repository.get_by_id(programacion.id_ahorro)

        return bool(ahorro) and ahorro.id_cuenta == cuenta.id_cuenta
