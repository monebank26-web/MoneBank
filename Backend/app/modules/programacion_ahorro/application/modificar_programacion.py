from app.modules.programacion_ahorro.domain.entity.programacion_ahorro import ProgramacionAhorro
from app.modules.programacion_ahorro.domain.interface.programacion_repository import ProgramacionAhorroRepository
from app.shared.exceptions.ahorro_errors import (
    FrecuenciaInvalida,
    ProgramacionFinalizada,
    ProgramacionNoEncontrada,
)
from app.shared.exceptions.common import CuentaNoEncontrada, MontoInvalido


class ModificarProgramacion:

    def __init__(
        self,
        repository: ProgramacionAhorroRepository,
        cuenta_repository,
        ahorro_repository,
    ):
        self.repository = repository
        self.cuenta_repository = cuenta_repository
        self.ahorro_repository = ahorro_repository

    def execute(
        self,
        id_usuario,
        programacion_id: int,
        monto_periodico,
        frecuencia: str,
    ):

        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        programacion = self.repository.get_by_id(programacion_id)

        if not self._pertenece_al_usuario(programacion, cuenta):
            raise ProgramacionNoEncontrada()

        if programacion.estado == ProgramacionAhorro.ESTADO_FINALIZADA:
            raise ProgramacionFinalizada()

        if not ProgramacionAhorro.es_frecuencia_valida(frecuencia):
            raise FrecuenciaInvalida()

        if monto_periodico is None or monto_periodico <= 0:
            raise MontoInvalido()

        actualizada = self.repository.update_periodicidad(
            programacion_id,
            monto_periodico,
            frecuencia,
        )

        if not actualizada:
            raise ProgramacionNoEncontrada()

        return actualizada

    def _pertenece_al_usuario(self, programacion, cuenta):
        if not programacion:
            return False

        ahorro = self.ahorro_repository.get_by_id(programacion.id_ahorro)

        return bool(ahorro) and ahorro.id_cuenta == cuenta.id_cuenta
