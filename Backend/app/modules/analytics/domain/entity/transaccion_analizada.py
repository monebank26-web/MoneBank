from datetime import date


class TransaccionAnalizada:

    MAX_DESCRIPCION = 80

    def __init__(
        self,
        id_transaccion,
        id_usuario,
        monto,
        tipo_transaccion,
        fecha,
        descripcion,
        nombre_categoria,
    ):
        self.id_transaccion = id_transaccion
        self.id_usuario = id_usuario
        self.monto = monto
        self.tipo_transaccion = tipo_transaccion
        self.fecha = fecha
        self.descripcion = descripcion
        self.nombre_categoria = nombre_categoria

    @classmethod
    def desde_fila_vista(cls, fila):
        return cls(
            id_transaccion=fila.id_transaccion,
            id_usuario=fila.id_usuario,
            monto=fila.monto,
            tipo_transaccion=fila.tipo_transaccion,
            fecha=fila.fecha,
            descripcion=fila.descripcion,
            nombre_categoria=fila.nombre_categoria,
        )

    def es_de_usuario(self, id_usuario):
        return self.id_usuario == id_usuario

    def fecha_relativa(self, hoy=None):
        hoy = hoy or date.today()

        a_fecha = getattr(self.fecha, "date", None)
        fecha_gasto = a_fecha() if callable(a_fecha) else self.fecha
        dias = (hoy - fecha_gasto).days

        if dias <= 0:
            return "hoy"
        if dias == 1:
            return "ayer"
        return f"hace {dias} días"

    def descripcion_resumida(self, max_caracteres=None):
        max_caracteres = max_caracteres or self.MAX_DESCRIPCION

        if not self.descripcion:
            return None

        texto = self.descripcion.strip()
        if len(texto) <= max_caracteres:
            return texto
        return texto[:max_caracteres].rstrip() + "..."

    def armar_contexto(
        self,
        total_gastado_mes,
        top_categorias,
        saldo_cuenta,
        hoy=None,
    ):
        return {
            "monto": round(float(self.monto)),
            "categoria": self.nombre_categoria,
            "fecha_relativa": self.fecha_relativa(hoy),
            "saldo_cuenta": round(float(saldo_cuenta or 0)),
            "total_gastado_mes": round(float(total_gastado_mes or 0)),
            "top_categorias": [
                {
                    "categoria": fila["nombre_categoria"],
                    "total": round(float(fila["total"])),
                }
                for fila in (top_categorias or [])
            ],
            "descripcion": self.descripcion_resumida(),
        }
