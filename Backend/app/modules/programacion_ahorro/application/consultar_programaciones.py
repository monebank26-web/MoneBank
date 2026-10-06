from app.modules.programacion_ahorro.domain.entity.programacion_detalle import ProgramacionDetalle
from app.shared.exceptions.transaccion_errors import CuentaNoEncontrada


class ConsultarProgramacionesUseCase:

    def __init__(self, repository, cuenta_repository):
        self.repository = repository
        self.cuenta_repository = cuenta_repository

    def execute(self, id_usuario):

        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        filas = self.repository.obtener_detalles_por_cuenta(cuenta.id_cuenta)

        return [ProgramacionDetalle.desde_fila(fila) for fila in filas]