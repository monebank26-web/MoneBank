from app.modules.control_parental.domain.entity.mesada_parental import MesadaParental
from app.modules.control_parental.infrastructure.model.mesada_parental_model import MesadaParentalModel


class ConfigurarMesada:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_padre: int, id_hijo: int, data: dict):
        vinculo = self.repository.obtener_vinculo_activo(id_padre, id_hijo)
        if not vinculo:
            raise PermissionError("No existe un vínculo parental activo")

        if not self.repository.permiso_activo(vinculo.id_control, "ASIGNAR_MESADA"):
            raise PermissionError("El permiso de asignar mesada está desactivado")

        if self.repository.obtener_activa(vinculo.id_control):
            raise ValueError("El hijo ya tiene una mesada activa")

        cuenta_padre, cuenta_hijo = self.repository.obtener_cuentas(id_padre, id_hijo)
        if not cuenta_padre or not cuenta_hijo:
            raise ValueError("El padre y el hijo deben tener una cuenta activa")

        entidad = MesadaParental(
            id_mesada=None,
            id_control=vinculo.id_control,
            id_cuenta_padre=cuenta_padre.id_cuenta,
            id_cuenta_hijo=cuenta_hijo.id_cuenta,
            monto=data["monto"],
            frecuencia=data["frecuencia"].upper(),
            fecha_inicio=data["fecha_inicio"],
            fecha_fin=data.get("fecha_fin"),
        )
        entidad.validar_creacion(cuenta_padre.saldo)

        model = MesadaParentalModel(
            id_control=entidad.id_control,
            id_cuenta_padre=entidad.id_cuenta_padre,
            id_cuenta_hijo=entidad.id_cuenta_hijo,
            monto=entidad.monto,
            frecuencia=entidad.frecuencia,
            fecha_inicio=entidad.fecha_inicio,
            fecha_fin=entidad.fecha_fin,
            estado=entidad.estado,
        )
        return self.repository.crear(model)
