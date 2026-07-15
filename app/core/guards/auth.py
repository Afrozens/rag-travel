from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Extrae y valida el JWT del header Authorization.
    Retorna el user_id (sub) del token.

    TODO: Implementar validación real con python-jose.
    """
    token = credentials.credentials
    # Placeholder: en una implementación real se decodifica y valida el JWT.
    if not token or token == "invalid":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Retorna un user_id dummy para desarrollo
    return "user-placeholder"
