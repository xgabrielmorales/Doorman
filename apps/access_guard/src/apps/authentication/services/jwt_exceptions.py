class AuthJwtException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


class AuthJwtDecodeError(AuthJwtException):
    pass


class AuthJwtAccessTokenRequired(AuthJwtException):
    pass


class AuthJwtRefreshTokenRequired(AuthJwtException):
    pass


class InvalidHeaderError(AuthJwtException):
    pass
