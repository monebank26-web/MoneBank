from abc import ABC, abstractmethod

class UsuarioRepository(ABC):

    @abstractmethod
    def create(self, db, usuario_data):
        pass

    @abstractmethod
    def exists_by_email(self, db, correo):
        pass

    @abstractmethod
    def get_all(self, db):
        pass

    @abstractmethod
    def get_by_id(self, usuario_id):
        pass

    @abstractmethod
    def update(self, usuario_id, usuario_data):
        pass

    @abstractmethod
    def delete(self, db, usuario_id):
        pass

    @abstractmethod
    def get_by_email(self, correo):
        pass

    @abstractmethod
    def update_auth_fields(self, usuario_id, intentos_fallidos, bloqueado_hasta):
        pass