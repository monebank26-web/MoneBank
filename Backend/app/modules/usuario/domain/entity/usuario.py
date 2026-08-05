
class Usuario:

    def __init__(
        self,
        id_usuario,
        nombres,
        apellidos,
        correo,
        contrasena,
        estado,
        id_rol,
        id_tipo_usuario,
        fecha_creacion=None
    ):
        self.id_usuario = id_usuario
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.contrasena = contrasena
        self.estado = estado
        self.id_rol = id_rol
        self.id_tipo_usuario = id_tipo_usuario
        self.fecha_creacion = fecha_creacion