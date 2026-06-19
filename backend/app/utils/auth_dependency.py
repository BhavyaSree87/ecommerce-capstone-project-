from fastapi import HTTPException, status, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from typing import Dict
from app.utils.jwt_handler import verify_token
from app.logger import get_logger

logger = get_logger("auth_dependency")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token", scopes={})


def current_user(token: str = Security(oauth2_scheme)) -> Dict:
    """
    Dependency to get current authenticated user
    
    Integrates with FastAPI OAuth2PasswordBearer for Swagger UI support.
    Automatically extracts and validates JWT token from Authorization header.
    
    Args:
        token: JWT token extracted by OAuth2PasswordBearer
        
    Returns:
        Decoded JWT payload containing user info (user_id, email, role)
        
    Raises:
        HTTPException: 401 if token is invalid, expired, or missing user_id
    """
    try:
        payload = verify_token(token)
        user_id: int = payload.get("user_id")
        
        if user_id is None:
            logger.warning("Token missing user_id claim")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user information",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.debug(f"User {user_id} authenticated successfully")
        return payload
        
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def admin_only(user: Dict = Security(current_user)) -> Dict:
    """
    Dependency to verify admin access
    
    Args:
        user: User data from current_user dependency
        
    Returns:
        Decoded JWT payload if user is admin
        
    Raises:
        HTTPException: If user is not admin (403 Forbidden)
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

