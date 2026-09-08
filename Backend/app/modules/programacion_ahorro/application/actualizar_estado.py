from app.modules.programacion_ahorro.domain.entity.programacion_ahorro import ProgramacionAhorro
from app.modules.programacion_ahorro.domain.interface.programacion_repository import ProgramacionAhorroRepository
from app.shared.exceptions.business_exceptions import (
    CuentaNoEncontrada,
    EstadoInvalido,
    ProgramacionNoEncontrada,
)


class ActualizarEstadoUseCase:

    def __init__(self, repository: ProgramacionAhorroRepository, cuenta_repository):
        self.repository = repository
        self.cuenta_repository = cuenta_repository

    def execute(self, id_usuario, programacion_id: int, nuevo_estado: str):

        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        if not ProgramacionAhorro.es_estado_valido(nuevo_estado):
            raise EstadoInvalido()

        programacion = self.repository.update_estado(programacion_id, nuevo_estado)

        if not programacion:
            raise ProgramacionNoEncontrada()

        return programacion