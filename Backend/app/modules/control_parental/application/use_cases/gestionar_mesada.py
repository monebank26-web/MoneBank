from app.modules.control_parental.domain.entity.mesada_parental import (
    FRECUENCIAS_VALIDAS,
)


class GestionarMesada:
    def __init__(self, repository):
        self.repository = repository

    def _obtener_vinculo_y_validar_permiso(
        self,
        id_padre,
        id_hijo,
    ):
        vinculo = self.repository.obtener_vinculo_activo(
            id_padre,
            id_hijo,
        )

        if not vinculo:
            raise PermissionError(
                "No existe un vínculo parental activo"
            )

        tiene_permiso = self.repository.permiso_activo(
            vinculo.id_control,
            "ASIGNAR_MESADA",
        )

        if not tiene_permiso:
            raise PermissionError(
                "El permiso de asignar mesada está desactivado"
            )

        return vinculo

    def actualizar(
        self,
        id_padre,
        id_hijo,
        data,
    ):
        vinculo = (
            self._obtener_vinculo_y_validar_permiso(
                id_padre,
                id_hijo,
            )
        )

        mesada = self.repository.obtener_activa(
            vinculo.id_control
        )

        if not mesada:
            raise ValueError(
                "No existe una mesada activa para este hijo"
            )

        cuenta_padre, cuenta_hijo = (
            self.repository.obtener_cuentas(
                id_padre,
                id_hijo,
            )
        )

        if not cuenta_padre or not cuenta_hijo:
            raise ValueError(
                "No se encontraron las cuentas "
                "del padre y del hijo"
            )

        monto = data.get(
            "monto",
            mesada.monto,
        )

        frecuencia = data.get(
            "frecuencia",
            mesada.frecuencia,
        )

        fecha_inicio = data.get(
            "fecha_inicio",
            mesada.fecha_inicio,
        )

        fecha_fin = data.get(
            "fecha_fin",
            mesada.fecha_fin,
        )

        monto = float(monto)

        if monto <= 0:
            raise ValueError(
                "El monto debe ser mayor que cero"
            )

        frecuencia = frecuencia.upper()

        if frecuencia not in FRECUENCIAS_VALIDAS:
            raise ValueError(
                "La frecuencia de la mesada no es válida"
            )

        if (
            fecha_fin is not None
            and fecha_fin < fecha_inicio
        ):
            raise ValueError(
                "La fecha final no puede ser anterior "
                "a la fecha inicial"
            )

        if float(cuenta_padre.saldo or 0) < monto:
            raise ValueError(
                "Saldo insuficiente para configurar "
                "la mesada"
            )

        mesada.monto = monto
        mesada.frecuencia = frecuencia
        mesada.fecha_inicio = fecha_inicio
        mesada.fecha_fin = fecha_fin

        self.repository.guardar()

        return mesada

    def cancelar(
        self,
        id_padre,
        id_hijo,
    ):
        vinculo = (
            self._obtener_vinculo_y_validar_permiso(
                id_padre,
                id_hijo,
            )
        )

        mesada = self.repository.obtener_activa(
            vinculo.id_control
        )

        if not mesada:
            raise ValueError(
                "No existe una mesada activa para este hijo"
            )

        mesada.estado = "CANCELADA"

        self.repository.guardar()

        return mesada
