from datetime import date, datetime, timezone
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.modules.usuario.infrastructure.model.usuario_model import UsuarioModel
from app.modules.control_parental.infrastructure.model.control_parental_model import ControlParentalModel
from app.modules.control_parental.infrastructure.model.solicitud_control_parental_model import SolicitudControlParentalModel
from app.modules.control_parental.domain.entity.control_parental import ControlParental
from app.modules.control_parental.domain.entity.solicitud_control_parental import SolicitudControlParental
from app.modules.control_parental.domain.interface.control_parental_repository import ControlParentalRepository
from app.modules.control_parental.infrastructure.model.control_parental_model import  PermisoParentalModel
from app.modules.cuenta.infrastructure.model.cuenta_model import CuentaModel
from app.modules.transaccion.infrastructure.model.transaccion_model import TransaccionModel
from app.modules.control_parental.infrastructure.model.mesada_parental_model import MesadaParentalModel

class SqlControlParentalRepository:
    def __init__(self, db: Session): 
        self.db = db
    def buscar_usuario_por_correo(self, correo):
        return self.db.query(UsuarioModel).filter(UsuarioModel.correo.ilike(correo)).first()
    def buscar_vinculacion_activa(self, padre_id, hijo_id):
        model = self.db.query(ControlParentalModel).filter(
            ControlParentalModel.id_usuario_parental == padre_id,
            ControlParentalModel.id_usuario_dependiente == hijo_id,
            ControlParentalModel.estado == "ACTIVO",
        ).first()
        return self._to_entity(model) if model else None
    def guardar_vinculacion(self, entity):
        model = ControlParentalModel(
            permiso_monitoreo=entity.permiso_monitoreo,
            fecha_inicio=(
                entity.fecha_inicio.date()
                if isinstance(entity.fecha_inicio, datetime)
                else entity.fecha_inicio
            ),
            fecha_fin=None,
            estado=entity.estado,
            id_usuario_parental=entity.id_usuario_parental,
            id_usuario_dependiente=entity.id_usuario_dependiente,
        )

        self.db.add(model)


        self.db.flush()

        permisos_iniciales = [
            ("CONSULTAR_PERFIL", True),
            ("CONSULTAR_SALDO", True),
            ("CONSULTAR_TRANSACCIONES", True),
            ("CONSULTAR_AHORROS", True),
            ("ASIGNAR_MESADA", True),
            ("GESTIONAR_BOLSILLOS", False),
            ("GESTIONAR_METAS", False),
            ("ASIGNAR_RECOMPENSAS", False),
            ("BLOQUEAR_GASTOS", False),
        ]

        for nombre_permiso, permitido in permisos_iniciales:
            permiso = PermisoParentalModel(
                id_control=model.id_control,
                nombre_permiso=nombre_permiso,
                permitido=permitido,
                fecha_actualizacion=datetime.utcnow(),
            )

            self.db.add(permiso)

        self.db.commit()
        self.db.refresh(model)

        return self._to_entity(model)

    def actualizar_vinculacion(self, entity):
        model = (
            self.db.query(ControlParentalModel)
            .filter(
                ControlParentalModel.id_control
                == entity.id_control
            )
            .first()
        )

        if not model:
            return None

        model.estado = entity.estado
        model.fecha_fin = (
            entity.fecha_fin.date()
            if isinstance(entity.fecha_fin, datetime)
            else entity.fecha_fin
        )

    
        if entity.estado != "ACTIVO":
            self.db.query(PermisoParentalModel).filter(
                PermisoParentalModel.id_control
                == entity.id_control
            ).update(
                {
                    "permitido": False,
                    "fecha_actualizacion": datetime.utcnow(),
                },
                synchronize_session=False,
            )

        self.db.commit()
        self.db.refresh(model)

        return self._to_entity(model)

    def crear_solicitud(self, entity):
        model = SolicitudControlParentalModel(
            id_usuario_solicitante=entity.id_usuario_solicitante,
            id_usuario_destino=entity.id_usuario_destino,
            id_control=entity.id_control,
            tipo_operacion=entity.tipo_operacion,
            correo_confirmacion=entity.correo_confirmacion,
            nombre_confirmacion=entity.nombre_confirmacion,
            token_hash=entity.token_hash,
            fecha_expiracion=entity.fecha_expiracion,
            intentos_fallidos=entity.intentos_fallidos,
            usado=entity.usado,
            estado=entity.estado,
        )
        self.db.add(model); self.db.commit(); self.db.refresh(model)
        return self._to_solicitud(model)
    def actualizar_solicitud(self, entity):
        model = self.db.query(SolicitudControlParentalModel).filter(SolicitudControlParentalModel.id_solicitud == entity.id_solicitud).first()
        if not model: return None
        model.usado = entity.usado; model.estado = entity.estado; model.intentos_fallidos = entity.intentos_fallidos
        self.db.commit(); self.db.refresh(model)
        return self._to_solicitud(model)
    def buscar_solicitud_vigente(self, token_hash, operacion):
        model = self.db.query(SolicitudControlParentalModel).filter(
            SolicitudControlParentalModel.token_hash == token_hash,
            SolicitudControlParentalModel.tipo_operacion == operacion,
            SolicitudControlParentalModel.estado == "PENDIENTE",
            SolicitudControlParentalModel.usado.is_(False),
            SolicitudControlParentalModel.fecha_expiracion > datetime.now(timezone.utc),
        ).first()
        return self._to_solicitud(model) if model else None
    def cancelar_solicitudes_pendientes(self, solicitante_id, destino_id, operacion):
        self.db.query(SolicitudControlParentalModel).filter(
            SolicitudControlParentalModel.id_usuario_solicitante == solicitante_id,
            SolicitudControlParentalModel.id_usuario_destino == destino_id,
            SolicitudControlParentalModel.tipo_operacion == operacion,
            SolicitudControlParentalModel.estado == "PENDIENTE",
        ).update({"estado": "CANCELADA", "usado": True})
        self.db.commit()
    def listar_vinculaciones(self, usuario_id):
        rows = self.db.query(ControlParentalModel).filter(
            ((ControlParentalModel.id_usuario_parental == usuario_id) | (ControlParentalModel.id_usuario_dependiente == usuario_id)),
            ControlParentalModel.estado == "ACTIVO",
        ).all()
        return [self._to_entity(row) for row in rows]
    @staticmethod
    def _to_entity(model):
        return ControlParental(model.id_control, model.id_usuario_parental, model.id_usuario_dependiente, model.permiso_monitoreo, model.estado, model.fecha_inicio, model.fecha_fin)
    @staticmethod
    def _to_solicitud(model):
        if not model: return None
        return SolicitudControlParental(model.id_solicitud, model.id_usuario_solicitante, model.id_usuario_destino, model.tipo_operacion, model.token_hash, model.fecha_expiracion, model.correo_confirmacion, model.nombre_confirmacion, model.id_control, model.intentos_fallidos, model.usado, model.estado)


    def listar_hijos(self, id_padre):
        rows = (
            self.db.query(ControlParentalModel, UsuarioModel, CuentaModel)
            .join(UsuarioModel, UsuarioModel.id_usuario == ControlParentalModel.id_usuario_dependiente)
            .outerjoin(CuentaModel, CuentaModel.id_usuario == UsuarioModel.id_usuario)
            .filter(ControlParentalModel.id_usuario_parental == id_padre,
                    ControlParentalModel.estado == "ACTIVO")
            .all()
        )
        return [self._hijo_dict(control, usuario, cuenta) for control, usuario, cuenta in rows]

    def obtener_vinculo(self, id_padre, id_hijo):
        return (
            self.db.query(ControlParentalModel)
            .filter(ControlParentalModel.id_usuario_parental == id_padre,
                    ControlParentalModel.id_usuario_dependiente == id_hijo,
                    ControlParentalModel.estado == "ACTIVO")
            .first()
        )

    def listar_permisos(self, id_control):
        return (self.db.query(PermisoParentalModel)
                .filter(PermisoParentalModel.id_control == id_control)
                .order_by(PermisoParentalModel.nombre_permiso).all())

    def actualizar_permisos(self, id_control, permisos):
        actuales = {p.nombre_permiso: p for p in self.listar_permisos(id_control)}
        for nombre, permitido in permisos.items():
            if nombre not in actuales:
                raise ValueError(f"Permiso no configurado: {nombre}")
            actuales[nombre].permitido = bool(permitido)
            actuales[nombre].fecha_actualizacion = datetime.utcnow()
        self.db.commit()
        return self.listar_permisos(id_control)

    def obtener_resumen_hijo(self, id_hijo):
        cuenta = self.db.query(CuentaModel).filter(CuentaModel.id_usuario == id_hijo).first()
        usuario = self.db.query(UsuarioModel).filter(UsuarioModel.id_usuario == id_hijo).first()
        return {
            "id_usuario": id_hijo,
            "nombres": usuario.nombres if usuario else "",
            "apellidos": usuario.apellidos if usuario else "",
            "correo": usuario.correo if usuario else "",
            "saldo": cuenta.saldo if cuenta else 0,
            "estado_cuenta": cuenta.estado if cuenta else "SIN_CUENTA",
        }

    def obtener_transacciones_hijo(self, id_hijo, limite=20):
        cuenta = self.db.query(CuentaModel).filter(CuentaModel.id_usuario == id_hijo).first()
        if not cuenta:
            return []
        return (self.db.query(TransaccionModel)
                .filter(TransaccionModel.id_cuenta == cuenta.id_cuenta)
                .order_by(desc(TransaccionModel.fecha))
                .limit(limite).all())

    @staticmethod
    def _hijo_dict(control, usuario, cuenta):
        return {
            "id_control": control.id_control,
            "id_usuario": usuario.id_usuario,
            "nombres": usuario.nombres,
            "apellidos": usuario.apellidos,
            "correo": usuario.correo,
            "saldo": cuenta.saldo if cuenta else 0,
            "estado_cuenta": cuenta.estado if cuenta else "SIN_CUENTA",
            "permiso_monitoreo": control.permiso_monitoreo,
        }

class SqlMesadaParentalRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_vinculo_activo(self, id_padre: int, id_hijo: int):
        return self.db.query(ControlParentalModel).filter(
            ControlParentalModel.id_usuario_parental == id_padre,
            ControlParentalModel.id_usuario_dependiente == id_hijo,
            ControlParentalModel.estado == "ACTIVO",
        ).first()

    def permiso_activo(self, id_control: int, nombre: str):
        permiso = self.db.query(PermisoParentalModel).filter(
            PermisoParentalModel.id_control == id_control,
            PermisoParentalModel.nombre_permiso == nombre,
        ).first()
        return bool(permiso and permiso.permitido)

    def obtener_cuentas(self, id_padre: int, id_hijo: int):
        padre = self.db.query(CuentaModel).filter(CuentaModel.id_usuario == id_padre).first()
        hijo = self.db.query(CuentaModel).filter(CuentaModel.id_usuario == id_hijo).first()
        return padre, hijo

    def obtener_activa(self, id_control: int):
        return self.db.query(MesadaParentalModel).filter(
            MesadaParentalModel.id_control == id_control,
            MesadaParentalModel.estado == "ACTIVA",
        ).first()

    def crear(self, model):
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def guardar(self):
        self.db.commit()

    @staticmethod
    def model_to_dict(model):
        return {
            "id_mesada": model.id_mesada,
            "id_control": model.id_control,
            "id_cuenta_padre": model.id_cuenta_padre,
            "id_cuenta_hijo": model.id_cuenta_hijo,
            "monto": model.monto,
            "frecuencia": model.frecuencia,
            "fecha_inicio": model.fecha_inicio,
            "fecha_fin": model.fecha_fin,
            "estado": model.estado,
        }
