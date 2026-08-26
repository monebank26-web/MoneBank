from math import ceil

from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)


class ObtenerHistorialUseCase:

    def __init__(self, repository: TransaccionRepository):
        self.repository = repository

    def execute(self, usuario_id, filtros):
        items, total = self.repository.find_historial(usuario_id, filtros)
        return {
            "items": items,
            "total": total,
            "pagina": filtros["pagina"],
            "por_pagina": filtros["por_pagina"],
            "total_paginas": (
                ceil(total / filtros["por_pagina"]) if total else 0
            ),
        }

