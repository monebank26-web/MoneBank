from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.responses import ErrorResponse
from app.shared.exceptions.business_exceptions import (
    TransaccionesNoEncontrado,
    MontoInvalido,
    FechaInvalida,
    CategoriaInvalida,
    TipoTransaccionNoValido,
    AhorroAsociadoNoValido,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
)


def register_transaccion_exception_handlers(app: FastAPI):

    @app.exception_handler(TransaccionesNoEncontrado)
    async def transacciones_no_encontrado_handler(request: Request, exc: TransaccionesNoEncontrado):
        return JSONResponse(
            status_code=TransaccionesNoEncontrado.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(MontoInvalido)
    async def monto_invalido_handler(request: Request, exc: MontoInvalido):
        return JSONResponse(
            status_code=MontoInvalido.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(FechaInvalida)
    async def fecha_invalida_handler(request: Request, exc: FechaInvalida):
        return JSONResponse(
            status_code=FechaInvalida.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(CategoriaInvalida)
    async def categoria_invalida_handler(request: Request, exc: CategoriaInvalida):
        return JSONResponse(
            status_code=CategoriaInvalida.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(TipoTransaccionNoValido)
    async def tipo_transaccion_no_valido_handler(request: Request, exc: TipoTransaccionNoValido):
        return JSONResponse(
            status_code=TipoTransaccionNoValido.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(AhorroAsociadoNoValido)
    async def ahorro_asociado_no_valido_handler(request: Request, exc: AhorroAsociadoNoValido):
        return JSONResponse(
            status_code=AhorroAsociadoNoValido.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(CuentaNoEncontrada)
    async def cuenta_no_encontrada_handler(request: Request, exc: CuentaNoEncontrada):
        return JSONResponse(
            status_code=CuentaNoEncontrada.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(CuentaNoPerteneceAlUsuario)
    async def cuenta_no_pertenece_al_usuario_handler(request: Request, exc: CuentaNoPerteneceAlUsuario):
        return JSONResponse(
            status_code=CuentaNoPerteneceAlUsuario.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )
