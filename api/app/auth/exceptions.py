class AuthError(Exception):
    def __init__(self, error, status_code) -> None:
        self.error = error
        self.status_code = status_code

class HeaderMissingError(AuthError):
    def __init__(self) -> None:
        error = {"code": "authorization_header_missing",
                 "description": "Authorization header is expected"}
        super().__init__(error, 401)
        
class InvalidHeaderError(AuthError):
    def __init__(self) -> None:
        error = {"code": "invalid_header",
                 "description": "invalid header"}
        super().__init__(error, 401)
        
class InvalidClaimsError(AuthError):
    def __init__(self) -> None:
        error = {"code": "invalid_claims",
                 "description": "incorrect claims, please check the audience and issuer"}
        super().__init__(error, 401)

class TokenExpiredError(AuthError):
    def __init__(self) -> None:
        error = {"code": "token_expired",
                 "description": "token is expired"}
        super().__init__(error, 401)