from fastapi import APIRouter, Depends

from app.modules.auth.presentation.schemas.register_response import RegisterResponse
from app.modules.auth.application.use_cases.register_user import RegisterUserUseCase
from app.modules.auth.presentation.schemas.register_request import RegisterRequest

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    responseModel=RegisterResponse
)
def register(
    request: RegisterRequest,
    use_case: RegisterUserUseCase = Depends()
):
    return use_case.execute(request)
