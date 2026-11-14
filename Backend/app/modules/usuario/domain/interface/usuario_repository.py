from abc import ABC, abstractmethod


class UsuarioRepository(ABC):

    @abstractmethod
    def create(self, usuario_data):
        pass

    @abstractmethod
    def exists_by_email(self, correo, excluir_id_usuario=None):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def listar(self, filtros):
        pass

    @abstractmethod
    def get_by_id(self, usuario_id):
        pass

    @abstractmethod
    def update(self, usuario_id, usuario_data):
        pass

    @abstractmethod
    def delete(self, usuario_id):
        pass

    @abstractmethod
    def get_by_email(self, correo):
        pass

    @abstractmethod
    def update_auth_fields(self, usuario_id, intentos_fallidos, bloqueado_hasta):
        pass

    @abstractmethod
    def update_password(self, usuario_id, nuevo_hash):
        pass

    @abstractmethod
    def contar_admins_activos(self, excluir_id_usuario=None):
        pass
