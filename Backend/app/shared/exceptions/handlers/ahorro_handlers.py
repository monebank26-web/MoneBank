from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.responses import ErrorResponse
from app.shared.exceptions.business_exceptions import (
    MetaNoEncontrada,
    PresupuestoNoEncontrado,
    PeriodoInvalido,
    CategoriaNoExiste,
    CategoriaNoCompatible,
    FechaObjetivoRequerida,
    FechaObjetivoPasada,
)


def register_ahorro_exception_handlers(app: FastAPI):

    @app.exception_handler(MetaNoEncontrada)
    async def meta_no_encontrada_handler(request: Request, exc: MetaNoEncontrada):
        return JSONResponse(
            status_code=MetaNoEncontrada.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(PresupuestoNoEncontrado)
    async def presupuesto_no_encontrado_handler(request: Request, exc: PresupuestoNoEncontrado):
        return JSONResponse(
            status_code=PresupuestoNoEncontrado.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(PeriodoInvalido)
    async def periodo_invalido_handler(request: Request, exc: PeriodoInvalido):
        return JSONResponse(
            status_code=PeriodoInvalido.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(CategoriaNoExiste)
    async def categoria_no_existe_handler(request: Request, exc: CategoriaNoExiste):
        return JSONResponse(
            status_code=CategoriaNoExiste.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(CategoriaNoCompatible)
    async def categoria_no_compatible_handler(request: Request, exc: CategoriaNoCompatible):
        return JSONResponse(
            status_code=CategoriaNoCompatible.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(FechaObjetivoRequerida)
    async def fecha_objetivo_requerida_handler(request: Request, exc: FechaObjetivoRequerida):
        return JSONResponse(
            status_code=FechaObjetivoRequerida.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(FechaObjetivoPasada)
    async def fecha_objetivo_pasada_handler(request: Request, exc: FechaObjetivoPasada):
        return JSONResponse(
            status_code=FechaObjetivoPasada.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )
