class AppError(Exception):
    """Base application error with HTTP mapping."""

    status_code: int = 500
    code: str = "APP_ERROR"

    def __init__(self, message: str, *, code: str | None = None, status_code: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code
        if status_code is not None:
            self.status_code = status_code


class NotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, code=self.code, status_code=self.status_code)


class ValidationAppError(AppError):
    status_code = 422
    code = "VALIDATION_ERROR"

    def __init__(self, message: str) -> None:
        super().__init__(message, code=self.code, status_code=self.status_code)


class ConflictError(AppError):
    status_code = 409
    code = "CONFLICT"

    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(message, code=self.code, status_code=self.status_code)


class ExternalServiceError(AppError):
    status_code = 502
    code = "EXTERNAL_SERVICE_ERROR"

    def __init__(self, message: str = "Upstream service error") -> None:
        super().__init__(message, code=self.code, status_code=self.status_code)
