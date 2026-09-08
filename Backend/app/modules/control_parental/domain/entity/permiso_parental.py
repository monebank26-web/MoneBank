class PermisoParental:
    NOMBRES = {
        "CONSULTAR_PERFIL",
        "CONSULTAR_SALDO",
        "CONSULTAR_TRANSACCIONES",
        "CONSULTAR_AHORROS",
        "GESTIONAR_BOLSILLOS",
        "GESTIONAR_METAS",
        "ASIGNAR_MESADA",
        "ASIGNAR_RECOMPENSAS",
        "BLOQUEAR_GASTOS",
    }

    def __init__(self, id_permiso, id_control, nombre_permiso, permitido):
        if nombre_permiso not in self.NOMBRES:
            raise ValueError("Permiso parental no reconocido")
        self.id_permiso = id_permiso
        self.id_control = id_control
        self.nombre_permiso = nombre_permiso
        self.permitido = bool(permitido)

    def cambiar_estado(self, permitido):
        self.permitido = bool(permitido)


class ControlParental:
    def __init__(self, id_control, id_usuario_parental, id_usuario_dependiente,
                 estado="ACTIVO"):
        self.id_control = id_control
        self.id_usuario_parental = id_usuario_parental
        self.id_usuario_dependiente = id_usuario_dependiente
        self.estado = estado

    def esta_activo(self):
        return self.estado == "ACTIVO"

    def pertenece_al_padre(self, id_usuario):
        return self.id_usuario_parental == id_usuario

    def incluye_al_hijo(self, id_usuario):
        return self.id_usuario_dependiente == id_usuario
