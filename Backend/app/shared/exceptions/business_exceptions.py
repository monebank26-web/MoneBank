class InvalidCredentialsException(Exception):
    status_code = 401
    description = "Credenciales incorrectas"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class AccountLockedException(Exception):
    status_code = 423
    description = "Cuenta bloqueada temporalmente por múltiples intentos fallidos"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class EmailAlreadyExistsException(Exception):
    status_code = 409
    description = "El correo ya está registrado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class EmailNotFoundException(Exception):
    status_code = 404
    description = "El correo no está registrado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class InvalidOrExpiredTokenException(Exception):
    status_code = 410
    description = "El token es inválido o ha expirado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class UsuarioNotFoundException(Exception):
    status_code = 404
    description = "Usuario no encontrado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class TransaccionesNoEncontrado(Exception):
    status_code = 404
    description = "No se encontraron transacciones"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class MontoInvalido(Exception):
    status_code = 400
    description = "El monto del gasto debe ser mayor a 0"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class FechaInvalida(Exception):
    status_code = 400
    description = "La fecha del gasto no es válida"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class CategoriaInvalida(Exception):
    status_code = 422
    description = "La categoría no existe en el catálogo"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class TipoTransaccionNoValido(Exception):
    status_code = 422
    description = "El tipo de transacción no existe en el catálogo"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class AhorroAsociadoNoValido(Exception):
    status_code = 422
    description = "El ahorro asociado no existe o no pertenece a la cuenta"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class CuentaNoEncontrada(Exception):
    status_code = 404
    description = "Cuenta no encontrada"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class CuentaNoPerteneceAlUsuario(Exception):
    status_code = 403
    description = "La cuenta no pertenece al usuario autenticado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class MetaNoEncontrada(Exception):
    status_code = 404
    description = "Meta no encontrada"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class PresupuestoNoEncontrado(Exception):
    status_code = 404
    description = "Presupuesto no encontrado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class PeriodoInvalido(Exception):
    status_code = 400
    description = "El período debe ser DIARIO, SEMANAL o MENSUAL"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class CategoriaNoExiste(Exception):
    status_code = 422
    description = "La categoría no existe en el catálogo"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class CategoriaNoCompatible(Exception):
    status_code = 422
    description = "La categoría no es compatible con el tipo de ahorro seleccionado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class FechaObjetivoRequerida(Exception):
    status_code = 400
    description = "Las metas requieren una fecha objetivo"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class FechaObjetivoPasada(Exception):
    status_code = 400
    description = "La fecha objetivo no puede ser en el pasado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class PresupuestoDuplicado(Exception):
    status_code = 422
    description = "Ya existe un presupuesto activo para esta categoría y período"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class EstadoInvalido(Exception):
    status_code = 400
    description = "El estado debe ser ACTIVO, PAUSADO o FINALIZADO"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class AhorroNoEncontrado(Exception):
    status_code = 404
    description = "Ahorro no encontrado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class SaldoInsuficiente(Exception):
    status_code = 400
    description = "Saldo insuficiente en la cuenta"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class ConsejoIANoDisponible(Exception):
    status_code = 503
    description = "El servicio de consejos de IA no está disponible en este momento"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class FrecuenciaInvalida(Exception):
    status_code = 400
    description = "La frecuencia debe ser DIARIA, SEMANAL, QUINCENAL, MENSUAL, TRIMESTRAL, SEMESTRAL o ANUAL"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class RangoFechasInvalido(Exception):
    status_code = 400
    description = "fecha_fin debe ser mayor o igual a fecha_inicio"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)