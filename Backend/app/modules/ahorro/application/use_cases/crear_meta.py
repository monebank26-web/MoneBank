from datetime import date

from app.modules.ahorro.domain.entity.ahorro import Ahorro
from app.shared.exceptions.business_exceptions import (
    CategoriaNoCompatible,
    CategoriaNoExiste,
    CuentaNoEncontrada,
    FechaObjetivoPasada,
    FechaObjetivoRequerida,
    SaldoInsuficiente,
)


class CrearMeta:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, meta_data, id_usuario):

        cuenta = self.repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        categoria = self.repository.get_categoria(
            meta_data["id_categoria"]
        )

        if not categoria:
            raise CategoriaNoExiste()

        if categoria.tipo_categoria != "AHORRO":
            raise CategoriaNoCompatible()

        fecha_objetivo = meta_data.get("fecha_objetivo")

        if not fecha_objetivo:
            raise FechaObjetivoRequerida()

        meta = Ahorro(
            id_ahorro=None,
            nombre=meta_data["nombre"],
            monto_objetivo=meta_data["monto_objetivo"],
            saldo_actual=meta_data.get("saldo_inicial") or 0,
            estado=Ahorro.ESTADO_ACTIVO,
            fecha_objetivo=fecha_objetivo,
        )

        if not meta.es_fecha_objetivo_valida():
            raise FechaObjetivoPasada()

        saldo_inicial = meta_data.get("saldo_inicial") or 0

        if saldo_inicial > cuenta.saldo:
            raise SaldoInsuficiente()

        tipo_meta = self.repository.get_tipo_ahorro(Ahorro.TIPO_META)

        meta_data["id_cuenta"] = cuenta.id_cuenta
        meta_data["id_tipo_ahorro"] = tipo_meta.id_tipo_ahorro
        meta_data["estado"] = Ahorro.ESTADO_ACTIVO

        return self.repository.create(meta_data)
