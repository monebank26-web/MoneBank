from app.modules.analytics.domain.entity.transaccion_analizada import (
    TransaccionAnalizada
)
from app.shared.exceptions.business_exceptions import (
    CuentaNoEncontrada,
    TransaccionesNoEncontrado,
)


class ObtenerConsejoIA:

    def __init__(self, analytics_repository, cuenta_repository, consejo_ia_port):
        self.analytics_repository = analytics_repository
        self.cuenta_repository = cuenta_repository
        self.consejo_ia_port = consejo_ia_port

    def execute(self, id_usuario, id_transaccion):
        fila = self.analytics_repository.find_transaccion(
            id_usuario, id_transaccion
        )

        if fila is None:
            raise TransaccionesNoEncontrado()

        transaccion = TransaccionAnalizada.desde_fila_vista(fila)

        stats = self.analytics_repository.calcular_stats_mes(id_usuario)

        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)
        if not cuenta:
            raise CuentaNoEncontrada()

        contexto = transaccion.armar_contexto(
            stats["total_gastado_mes"],
            stats["top_categorias"],
            cuenta.saldo,
        )

        return self.consejo_ia_port.generar_consejo(contexto)
