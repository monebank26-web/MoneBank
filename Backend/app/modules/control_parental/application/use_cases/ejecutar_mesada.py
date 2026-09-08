from datetime import date

from app.modules.control_parental.domain.entity.ejecucion_mesada import (
    EjecucionMesada,
)


class EjecutarMesada:
    def __init__(self, repository):
        self.repository = repository

    def execute(
        self,
        id_padre: int,
        id_hijo: int,
        fecha: date | None = None,
    ):
        fecha_ejecucion = fecha or date.today()

        # Validar vínculo
        vinculo = self.repository.vinculo_activo(
            id_padre,
            id_hijo,
        )

        if not vinculo:
            raise PermissionError(
                "No existe un vínculo parental activo"
            )

        # Validar permiso
        if not self.repository.permiso_activo(
            vinculo.id_control
        ):
            raise PermissionError(
                "El permiso de asignar mesada está desactivado"
            )

        # Buscar mesada activa
        mesada = (
            self.repository.mesada_activa_bloqueada(
                vinculo.id_control
            )
        )

        if not mesada:
            raise ValueError(
                "No existe una mesada activa para este hijo"
            )

        # Validar que no se haya ejecutado en el período
        periodo = EjecucionMesada.periodo(
            fecha_ejecucion
        )

        ejecucion_existente = (
            self.repository.ejecucion_periodo(
                mesada.id_mesada,
                periodo,
            )
        )

        if ejecucion_existente:
            raise ValueError(
                "La mesada ya fue ejecutada para este período"
            )

        # Bloquear y consultar cuentas
        cuenta_padre, cuenta_hijo = (
            self.repository.cuentas_bloqueadas(
                mesada.id_cuenta_padre,
                mesada.id_cuenta_hijo,
            )
        )

        if not cuenta_padre or not cuenta_hijo:
            raise ValueError(
                "No se encontraron las cuentas de la mesada"
            )

        # Reglas de negocio
        EjecucionMesada.validar(
            mesada,
            cuenta_padre.saldo,
            fecha_ejecucion,
        )

        proxima = EjecucionMesada.siguiente_fecha(
            fecha_ejecucion,
            mesada.frecuencia,
        )

        # Obtener tipos reales del catálogo
        tipo_salida = (
            self.repository.obtener_tipo_transaccion(
                "GASTO"
            )
        )

        tipo_entrada = (
            self.repository.obtener_tipo_transaccion(
                "INGRESO"
            )
        )

        # Obtener categorías reales
        categoria_salida = (
            self.repository.obtener_categoria(
                "Mesada parental enviada",
                "GASTO",
            )
        )

        categoria_entrada = (
            self.repository.obtener_categoria(
                "Mesada parental recibida",
                "INGRESO",
            )
        )

        if not tipo_salida:
            raise ValueError(
                "No existe el tipo de transacción GASTO"
            )

        if not tipo_entrada:
            raise ValueError(
                "No existe el tipo de transacción INGRESO"
            )

        if not categoria_salida:
            raise ValueError(
                "No existe la categoría de salida de mesada"
            )

        if not categoria_entrada:
            raise ValueError(
                "No existe la categoría de entrada de mesada"
            )

        try:
            return self.repository.ejecutar(
                mesada=mesada,
                cuenta_padre=cuenta_padre,
                cuenta_hijo=cuenta_hijo,
                periodo=periodo,
                proxima=proxima,
                id_tipo_salida=(
                    tipo_salida.id_tipo_transaccion
                ),
                id_tipo_entrada=(
                    tipo_entrada.id_tipo_transaccion
                ),
                id_categoria_salida=(
                    categoria_salida.id_categoria
                ),
                id_categoria_entrada=(
                    categoria_entrada.id_categoria
                ),
            )

        except Exception:
            self.repository.rollback()
            raise
