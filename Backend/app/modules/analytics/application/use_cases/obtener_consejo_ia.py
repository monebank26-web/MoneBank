from app.modules.analytics.domain.entity.transaccion_analizada import (
    TransaccionAnalizada
)
from app.shared.exceptions.business_exceptions import TransaccionesNoEncontrado


class ObtenerConsejoIA:

    def __init__(self, analytics_repository, consejo_ia_port):
        self.analytics_repository = analytics_repository
        self.consejo_ia_port = consejo_ia_port

    def execute(self, id_usuario, id_transaccion):
        fila = self.analytics_repository.find_transaccion(
            id_usuario, id_transaccion
        )

        if fila is None:
            raise TransaccionesNoEncontrado()

        transaccion = TransaccionAnalizada.desde_fila_vista(fila)

        stats = self.analytics_repository.calcular_stats_mes(id_usuario)
        saldo = self.analytics_repository.get_saldo_cuenta(fila.id_cuenta)

        contexto = transaccion.armar_contexto(
            stats["total_gastado_mes"],
            stats["top_categorias"],
            saldo,
        )

        return self.consejo_ia_port.generar_consejo(contexto)
