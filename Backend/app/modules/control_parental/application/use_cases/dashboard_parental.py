class AccesoParentalNoAutorizado(Exception):
    status_code = 403

    def __init__(self, detail="No tienes autorización parental para este usuario"):
        self.message = detail
        super().__init__(detail)


class ListarHijosParentales:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_padre):
        return self.repository.listar_hijos(id_padre)


class ObtenerResumenHijo:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_padre, id_hijo):
        vinculo = self.repository.obtener_vinculo(id_padre, id_hijo)
        if not vinculo:
            raise AccesoParentalNoAutorizado()
        permisos = {p.nombre_permiso: p.permitido for p in self.repository.listar_permisos(vinculo.id_control)}
        if not permisos.get("CONSULTAR_SALDO", False):
            raise AccesoParentalNoAutorizado("El permiso de consultar saldo está desactivado")
        resumen = self.repository.obtener_resumen_hijo(id_hijo)
        resumen["id_control"] = vinculo.id_control
        resumen["permisos"] = permisos
        return resumen


class ObtenerTransaccionesHijo:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_padre, id_hijo, limite=20):
        vinculo = self.repository.obtener_vinculo(id_padre, id_hijo)
        if not vinculo:
            raise AccesoParentalNoAutorizado()
        permisos = {p.nombre_permiso: p.permitido for p in self.repository.listar_permisos(vinculo.id_control)}
        if not permisos.get("CONSULTAR_TRANSACCIONES", False):
            raise AccesoParentalNoAutorizado("El permiso de consultar transacciones está desactivado")
        return self.repository.obtener_transacciones_hijo(id_hijo, limite)


class ObtenerPermisosHijo:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_padre, id_hijo):
        vinculo = self.repository.obtener_vinculo(id_padre, id_hijo)
        if not vinculo:
            raise AccesoParentalNoAutorizado()
        return self.repository.listar_permisos(vinculo.id_control)


class ActualizarPermisosHijo:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_padre, id_hijo, permisos):
        vinculo = self.repository.obtener_vinculo(id_padre, id_hijo)
        if not vinculo:
            raise AccesoParentalNoAutorizado()
        return self.repository.actualizar_permisos(vinculo.id_control, permisos)
