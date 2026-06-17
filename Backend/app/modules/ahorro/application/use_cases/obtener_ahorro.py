class ObtenerAhorrosUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, db):
        return self.repository.get_all(db)