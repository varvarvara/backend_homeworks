from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import InvalidTokenException
from app.core.security import decode_access_token

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise InvalidTokenException()

    subject = payload.get("sub")
    if subject is None:
        raise InvalidTokenException()

    return payload
