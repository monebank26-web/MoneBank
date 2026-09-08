from decimal import Decimal
from app.shared.exceptions.business_exceptions import SaldoInsuficiente


def validar_saldo_para_asignacion(saldo_padre, monto):
    saldo = Decimal(str(saldo_padre or 0))
    valor = Decimal(str(monto))
    if valor <= 0:
        raise ValueError("El monto debe ser mayor que cero")
    if saldo < valor:
        raise SaldoInsuficiente("El saldo del padre no alcanza para la mesada o recompensa")
    return True
