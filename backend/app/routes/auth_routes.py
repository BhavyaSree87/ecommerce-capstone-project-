from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import UserRegister, UserLogin, TokenResponse
from app.database.db import get_connection
from app.utils.password import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.services.auth_service import register_user
from app.config import get_settings
from app.logger import get_logger

logger = get_logger("auth_routes")
router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    settings = get_settings()
    try:
        hashed_password = hash_password(user.password)
        user.password = hashed_password

        try:
            row, user_dict = register_user(user)
        except Exception as e:
            import traceback
            logger.error(f"Error during register_user: {e}")
            traceback.print_exc()
            if isinstance(e, ValueError) and "Email already registered" in str(e):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
            raise

        if not row:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch newly created user")

        jwt_payload = {"user_id": row[0], "email": row[2], "role": row[3]}
        logger.debug(f"JWT payload created for user {row[0]}")

        try:
            token = create_access_token(jwt_payload)
        except Exception as e:
            import traceback
            logger.error(f"Error during create_access_token: {e}")
            traceback.print_exc()
            raise

        logger.info(f"User {row[0]} registered and authenticated successfully")
        expires_in = settings.access_token_expire_hours * 3600

        return {"access_token": token, "token_type": "bearer", "expires_in": expires_in, "user": user_dict}
    except Exception:
        import traceback
        traceback.print_exc()
        raise


def authenticate_user(email: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT ID, NAME, EMAIL, PASSWORD, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE FROM USERS WHERE EMAIL = :email",
            {"email": email},
        )
        db_user = cursor.fetchone()

        if not db_user:
            return None

        if not verify_password(password, db_user[3]):
            return None

        return db_user
    finally:
        cursor.close()
        conn.close()


@router.post("/token", response_model=TokenResponse)
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = authenticate_user(form_data.username, form_data.password)
    if not db_user:
        logger.warning(f"Token request failed for user: {form_data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    jwt_payload = {"user_id": db_user[0], "email": db_user[2], "role": db_user[4]}
    token = create_access_token(jwt_payload)

    user_dict = {
        "id": db_user[0],
        "name": db_user[1],
        "email": db_user[2],
        "role": db_user[4],
        "mobile": db_user[5],
        "address": db_user[6],
        "city": db_user[7],
        "state": db_user[8],
        "pincode": db_user[9]
    }
    settings = get_settings()
    expires_in = settings.access_token_expire_hours * 3600

    return {"access_token": token, "token_type": "bearer", "expires_in": expires_in, "user": user_dict}


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT ID, NAME, EMAIL, PASSWORD, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE FROM USERS WHERE EMAIL = :email",
            {"email": user.email},
        )
        db_user = cursor.fetchone()

        if not db_user:
            logger.warning(f"Login attempt failed: user with email {user.email} not found")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        hashed = db_user[3]
        if not verify_password(user.password, hashed):
            logger.warning(f"Login attempt failed: invalid password for {user.email}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        logger.debug(f"Password verified for user {user.email}")

        jwt_payload = {"user_id": db_user[0], "email": db_user[2], "role": db_user[4]}
        logger.debug(f"JWT payload created for user {db_user[0]}")

        try:
            token = create_access_token(jwt_payload)
        except Exception as e:
            import traceback
            logger.error(f"Error during create_access_token: {e}")
            traceback.print_exc()
            raise

        user_dict = {
            "id": db_user[0],
            "name": db_user[1],
            "email": db_user[2],
            "role": db_user[4],
            "mobile": db_user[5],
            "address": db_user[6],
            "city": db_user[7],
            "state": db_user[8],
            "pincode": db_user[9]
        }

        logger.info(f"User {db_user[0]} logged in successfully")
        settings = get_settings()
        expires_in = settings.access_token_expire_hours * 3600

        return {"access_token": token, "token_type": "bearer", "expires_in": expires_in, "user": user_dict}
    finally:
        cursor.close()
        conn.close()