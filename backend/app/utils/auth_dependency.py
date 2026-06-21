from fastapi import HTTPException, status, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, ExpiredSignatureError
from typing import Dict
from app.utils.jwt_handler import verify_token
from app.logger import get_logger

logger = get_logger("auth_dependency")

bearer_scheme = HTTPBearer(auto_error=False, bearerFormat="JWT", scheme_name="BearerAuth")


def current_user(request: Request, credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)) -> Dict:
    """
    Dependency to get current authenticated user.

    Accepts a Bearer token via HTTP Authorization header and verifies the JWT.
    """
    auth_header = request.headers.get("Authorization")
    logger.debug(f"Authorization header received: {auth_header}")

    if not credentials or credentials.scheme.lower() != "bearer":
        logger.warning("Missing or invalid Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        payload = verify_token(token)
        logger.debug(f"Decoded JWT payload: {payload}")

        user_id = payload.get("user_id")
        email = payload.get("email")
        role = payload.get("role")

        if user_id is None or email is None or role is None:
            logger.warning("Token missing required claim(s): user_id=%s email=%s role=%s", user_id, email, role)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing required user claims",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"User authenticated successfully: user_id={user_id}, email={email}, role={role}")
        return payload

    except ExpiredSignatureError as e:
        logger.warning(f"JWT expired token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or malformed token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def admin_only(user: Dict = Security(current_user)) -> Dict:
    """
    Dependency to verify admin access.
    """
    role = user.get("role")

    if role != "ADMIN":
        logger.warning(f"Non-admin user {user.get('user_id')} attempted admin action")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    logger.debug(f"Admin user {user.get('user_id')} verified")
    return user

