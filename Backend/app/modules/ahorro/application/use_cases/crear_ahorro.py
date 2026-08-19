class CrearAhorro:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, ahorro_data):
        return self.repository.create(ahorro_data)
