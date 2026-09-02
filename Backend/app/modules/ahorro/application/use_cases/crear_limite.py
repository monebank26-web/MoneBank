from app.modules.ahorro.domain.entity.ahorro import Ahorro
from app.shared.exceptions.business_exceptions import (
    CategoriaNoCompatible,
    CategoriaNoExiste,
    CuentaNoEncontrada,
    MontoInvalido,
    PeriodoInvalido,
    PresupuestoDuplicado,
)


class CrearLimite:

    def __init__(self, repository, cuenta_repository):
        self.repository = repository
        self.cuenta_repository = cuenta_repository

    def execute(self, limite_data, id_usuario):

        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        categoria = self.repository.get_categoria(
            limite_data["id_categoria"]
        )

        if not categoria:
            raise CategoriaNoExiste()

        if categoria.tipo_categoria != "GASTO":
            raise CategoriaNoCompatible()

        if limite_data["monto_limite"] <= 0:
            raise MontoInvalido()

        periodo = limite_data["periodo"]

        if not Ahorro.es_periodo_valido(periodo):
            raise PeriodoInvalido()

        existentes = self.repository.get_by_cuenta_y_tipo(
            cuenta.id_cuenta, Ahorro.TIPO_LIMITE
        )

        duplicado = any(
            otro.id_categoria == categoria.id_categoria
            and otro.periodo == periodo
            and otro.estado == Ahorro.ESTADO_ACTIVO
            for otro in existentes
        )

        if duplicado:
            raise PresupuestoDuplicado()

        tipo_limite = self.repository.get_tipo_ahorro(Ahorro.TIPO_LIMITE)

        nombre = limite_data.get("nombre") or (
            f"Límite {categoria.nombre_categoria} ({periodo})"
        )

        return self.repository.create({
            "nombre": nombre,
            "monto_objetivo": limite_data["monto_limite"],
            "saldo_inicial": 0,
            "estado": Ahorro.ESTADO_ACTIVO,
            "fecha_objetivo": None,
            "periodo": periodo,
            "id_tipo_ahorro": tipo_limite.id_tipo_ahorro,
            "id_categoria": categoria.id_categoria,
            "id_cuenta": cuenta.id_cuenta,
        })
