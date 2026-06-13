@router.post("/register")
def register(
    request: RegisterRequest,
    use_case: RegisterUserUseCase = Depends()
):
    return use_case.execute(request)