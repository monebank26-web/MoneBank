class ObtenerUsuariosUseCase:

    PAGINA_POR_DEFECTO = 1
    POR_PAGINA_POR_DEFECTO = 10

    def __init__(self, repository):
        self.repository = repository

    def execute(self, filtros=None):
        filtros = dict(filtros or {})
        filtros["pagina"] = filtros.get("pagina") or self.PAGINA_POR_DEFECTO
        filtros["por_pagina"] = (
            filtros.get("por_pagina") or self.POR_PAGINA_POR_DEFECTO
        )

        items, total = self.repository.listar(filtros)

        return {
            "items": items,
            "total": total,
            "pagina": filtros["pagina"],
            "por_pagina": filtros["por_pagina"],
        }
