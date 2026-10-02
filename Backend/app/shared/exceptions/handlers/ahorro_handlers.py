from fastapi import FastAPI

from app.shared.exceptions.ahorro_errors import (
    AhorroNoEncontrado,
    CategoriaNoCompatible,
    CategoriaNoExiste,
    EstadoInvalido,
    FechaCobroInvalida,
    FechaObjetivoPasada,
    FechaObjetivoRequerida,
    FrecuenciaInvalida,
    MetaNoEncontrada,
    PeriodoInvalido,
    PresupuestoDuplicado,
    PresupuestoNoEncontrado,
    ProgramacionDuplicada,
    ProgramacionNoEncontrada,
    RangoFechasInvalido,
)
from app.shared.exceptions.handlers._helpers import registrar_error_business


def register_ahorro_exception_handlers(app: FastAPI):
    registrar_error_business(app, MetaNoEncontrada, 404)
    registrar_error_business(app, PresupuestoNoEncontrado, 404)
    registrar_error_business(app, PresupuestoDuplicado, 422)
    registrar_error_business(app, PeriodoInvalido, 400)
    registrar_error_business(app, CategoriaNoExiste, 422)
    registrar_error_business(app, CategoriaNoCompatible, 422)
    registrar_error_business(app, FechaObjetivoRequerida, 400)
    registrar_error_business(app, FechaObjetivoPasada, 400)
    registrar_error_business(app, EstadoInvalido, 400)
    registrar_error_business(app, AhorroNoEncontrado, 404)
    registrar_error_business(app, ProgramacionNoEncontrada, 404)
    registrar_error_business(app, ProgramacionDuplicada, 409)
    registrar_error_business(app, FechaCobroInvalida, 400)
    registrar_error_business(app, FrecuenciaInvalida, 400)
    registrar_error_business(app, RangoFechasInvalido, 400)