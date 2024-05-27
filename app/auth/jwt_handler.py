import time
import jwt
from decouple import config
from fastapi import Depends, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from ..config.logger_config import logger

security = HTTPBearer()

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


async def jwt_filter(token: HTTPAuthorizationCredentials = Depends(security)):
    logger.info(f'Inside JWT Filter: {token.credentials}')
    payload = decode_access_token(token.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return payload


def get_jwt_response(token: str) -> dict:
    return {
        "access_token": token
    }


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload if payload['expires'] >= time.time() else False
    except jwt.ExpiredSignatureError:
        logger.info(f'JWT Token expired')
        return None
    except jwt.InvalidTokenError:
        logger.info(f'JWT Token invalid')
        return None


def sign_jwt(username: str, role: str):
    payload = {
        "username": username,
        "role": role,
        "expires": time.time() + 3600
    }
    return get_jwt_response(jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM))
