class ObtenerGraficas:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_usuario, periodo=None):
        return self.repository.obtener_datos_grafica(id_usuario, periodo)
