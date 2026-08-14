from abc import ABC, abstractmethod

class TransaccionRepository(ABC):

    @abstractmethod
    def find_by_usuario(
        self,
        usuario_id
    ):
        pass

    @abstractmethod
    def create(
        self,
        db,
        transaccion_data
    ):
        pass

    @abstractmethod
    def get_cuenta(
        self,
        db,
        id_cuenta
    ):
        pass

    @abstractmethod
    def existe_categoria(
        self,
        db,
        id_categoria
    ):
        pass

    @abstractmethod
    def descontar_saldo(
        self,
        db,
        id_cuenta,
        monto
    ):
        pass
