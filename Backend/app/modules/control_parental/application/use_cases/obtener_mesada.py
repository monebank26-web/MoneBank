class ObtenerMesada:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_padre: int, id_hijo: int):
        vinculo = self.repository.obtener_vinculo_activo(id_padre, id_hijo)
        if not vinculo:
            raise PermissionError("No existe un vínculo parental activo")

        if not self.repository.permiso_activo(vinculo.id_control, "ASIGNAR_MESADA"):
            raise PermissionError("El permiso de asignar mesada está desactivado")

        return self.repository.obtener_activa(vinculo.id_control)
