from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
from jose import jwt, JWTError, ExpiredSignatureError
from app.config import get_settings
from app.logger import get_logger

logger = get_logger("jwt_handler")
settings = get_settings()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Dictionary containing claims to encode
        expires_delta: Optional custom expiry time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=settings.access_token_expire_hours)
    
    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )
        logger.debug(f"JWT token created for user: {data.get('user_id')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create JWT token: {e}")
        raise


def verify_token(token: str) -> Dict:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        logger.debug(f"JWT token verified successfully for user: {payload.get('user_id')}")
        return payload
    except ExpiredSignatureError as e:
        logger.warning(f"JWT verification failed - expired token: {e}")
        raise
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise
