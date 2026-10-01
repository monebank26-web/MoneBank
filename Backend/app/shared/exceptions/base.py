class BusinessError(Exception):
    message = "Error de negocio"

    def __init__(self, message: str = None):
        super().__init__(message or self.message)