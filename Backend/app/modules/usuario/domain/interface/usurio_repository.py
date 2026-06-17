from abc import ABC, abstractmethod

class UsuarioRepository(ABC):

    @abstractmethod
    def create(self, db, usuario_data):
        pass

    @abstractmethod
    def get_all(self, db):
        pass

    @abstractmethod
    def get_by_id(self, db, usuario_id):
        pass

    @abstractmethod
    def update(self, db, usuario_id, usuario_data):
        pass

    @abstractmethod
    def delete(self, db, usuario_id):
        pass

    @abstractmethod
    def login(self, db, correo, contrasena):
        pass