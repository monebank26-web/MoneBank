from datetime import date

from app.modules.ahorro.domain.entity.ahorro import Ahorro
from app.modules.chat_ia.domain.entity.historial_chat import HistorialChat
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


class EnviarMensajeChat:

    def __init__(
        self,
        cuenta_repository,
        ahorro_repository,
        transaccion_chat_repository,
        chat_ia_port,
    ):
        self.cuenta_repository = cuenta_repository
        self.ahorro_repository = ahorro_repository
        self.transaccion_chat_repository = transaccion_chat_repository
        self.chat_ia_port = chat_ia_port

    def execute(self, id_usuario, mensaje, historial_lista):
        contexto = self._armar_contexto(id_usuario)
        historial = HistorialChat(historial_lista)
        contenidos = historial.agregar({"rol": "user", "texto": mensaje})
        return self.chat_ia_port.generar_respuesta(contexto, contenidos)

    def _armar_contexto(self, id_usuario):
        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)
        if not cuenta:
            raise CuentaNoEncontrada()

        id_cuenta = cuenta.id_cuenta
        inicio_mes = date.today().replace(day=1)

        return {
            "saldo_actual": round(float(cuenta.saldo or 0)),
            "ingreso_mes": round(
                float(self.transaccion_chat_repository.sumar_ingresos(id_usuario, inicio_mes))
            ),
            "gasto_mes": round(
                float(self.transaccion_chat_repository.sumar_gastos(id_usuario, inicio_mes))
            ),
            "diferencia_mes": round(
                float(
                    self.transaccion_chat_repository.sumar_ingresos(id_usuario, inicio_mes)
                    - self.transaccion_chat_repository.sumar_gastos(id_usuario, inicio_mes)
                )
            ),
            "top_categorias": self._top_categorias(id_usuario, inicio_mes, 3),
            "metas_ahorro": self._metas(id_cuenta),
            "limites_activos": self._limites(id_cuenta),
        }

    def _top_categorias(self, id_usuario, inicio_mes, limite):
        categorias = self.transaccion_chat_repository.top_categorias(
            id_usuario, inicio_mes, limite
        )
        return [
            {
                "nombre_categoria": c["nombre_categoria"],
                "total": round(float(c["total"] or 0)),
            }
            for c in categorias
        ]

    def _metas(self, id_cuenta):
        metas = self.ahorro_repository.get_metas_activas(id_cuenta)
        resultado = []
        for meta in metas:
            nombre = meta.get("nombre") if isinstance(meta, dict) else getattr(meta, "nombre", None)
            objetivo = meta.get("monto_objetivo") if isinstance(meta, dict) else getattr(meta, "monto_objetivo", None)
            actual = meta.get("saldo_actual") if isinstance(meta, dict) else getattr(meta, "saldo_actual", None)
            resultado.append({
                "nombre": nombre,
                "monto_objetivo": round(float(objetivo or 0)),
                "saldo_actual": round(float(actual or 0)),
            })
        return resultado

    def _limites(self, id_cuenta):
        limites = self.ahorro_repository.get_by_cuenta_y_tipo(
            id_cuenta, Ahorro.TIPO_LIMITE
        )
        resultado = []
        for limite in limites:
            nombre = getattr(limite, "nombre", None)
            objetivo = getattr(limite, "monto_objetivo", None)
            periodo = getattr(limite, "periodo", None)
            resultado.append({
                "nombre": nombre,
                "monto_limite": round(float(objetivo or 0)),
                "periodo": periodo,
            })
        return resultado
