from abc import ABC, abstractmethod

class ControlParentalRepository(ABC):
    @abstractmethod
    def buscar_usuario_por_correo(self, correo): ...
    @abstractmethod
    def buscar_vinculacion_activa(self, padre_id, hijo_id): ...
    @abstractmethod
    def guardar_vinculacion(self, vinculacion): ...
    @abstractmethod
    def actualizar_vinculacion(self, vinculacion): ...
    @abstractmethod
    def buscar_solicitud_vigente(self, token_hash, operacion): ...
    @abstractmethod
    def crear_solicitud(self, solicitud): ...
    @abstractmethod
    def actualizar_solicitud(self, solicitud): ...
    @abstractmethod
    def cancelar_solicitudes_pendientes(self, solicitante_id, destino_id, operacion): ...
    @abstractmethod
    def listar_vinculaciones(self, usuario_id): ...
    @abstractmethod
    def listar_hijos(self, id_padre):
        raise NotImplementedError

    @abstractmethod
    def obtener_vinculo(self, id_padre, id_hijo):
        raise NotImplementedError

    @abstractmethod
    def listar_permisos(self, id_control):
        raise NotImplementedError

    @abstractmethod
    def actualizar_permisos(self, id_control, permisos):
        raise NotImplementedError

    @abstractmethod
    def obtener_resumen_hijo(self, id_hijo):
        raise NotImplementedError

    @abstractmethod
    def obtener_transacciones_hijo(self, id_hijo, limite=20):
        raise NotImplementedError

