from app.shared.exceptions.base import BusinessError


class MetaNoEncontrada(BusinessError):
    message = "Meta no encontrada"


class PresupuestoNoEncontrado(BusinessError):
    message = "Presupuesto no encontrado"


class PeriodoInvalido(BusinessError):
    message = "El período debe ser DIARIO, SEMANAL o MENSUAL"


class CategoriaNoExiste(BusinessError):
    message = "La categoría no existe en el catálogo"


class CategoriaNoCompatible(BusinessError):
    message = "La categoría no es compatible con el tipo de ahorro seleccionado"


class FechaObjetivoRequerida(BusinessError):
    message = "Las metas requieren una fecha objetivo"


class FechaObjetivoPasada(BusinessError):
    message = "La fecha objetivo no puede ser en el pasado"


class PresupuestoDuplicado(BusinessError):
    message = "Ya existe un presupuesto activo para esta categoría y período"


class EstadoInvalido(BusinessError):
    message = "El estado debe ser ACTIVA, PAUSADA o FINALIZADA"


class AhorroNoEncontrado(BusinessError):
    message = "Ahorro no encontrado"


class ProgramacionNoEncontrada(BusinessError):
    message = "Programación de ahorro no encontrada"


class FrecuenciaInvalida(BusinessError):
    message = "La frecuencia debe ser DIARIA, SEMANAL, QUINCENAL, MENSUAL, TRIMESTRAL, SEMESTRAL o ANUAL"


class RangoFechasInvalido(BusinessError):
    message = "fecha_fin debe ser mayor o igual a fecha_inicio"