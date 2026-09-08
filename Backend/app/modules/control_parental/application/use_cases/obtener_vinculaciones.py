class ObtenerVinculacionesUseCase:
    def __init__(self, repository): self.repository = repository
    def execute(self, id_usuario): return self.repository.listar_vinculaciones(id_usuario)
