from fastapi import HTTPException, status


class UnauthorisedException(HTTPException):
    """Exception raised for authorization errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message or "Access token is missing or invalid",
            headers={"WWW-Authenticate": "Bearer"}
        )


class ForbiddenException(HTTPException):
    """Exception raised for authorization errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message or "You do not have permission to perform this action",
            headers={"WWW-Authenticate": "Bearer"}
        )
