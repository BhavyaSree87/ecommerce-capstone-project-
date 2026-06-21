from fastapi import APIRouter, HTTPException, Request, status
from app.schemas.user_schema import UserRegister, UserLogin, TokenResponse
from app.database.db import get_connection
from app.utils.password import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.services.auth_service import register_user
from app.config import get_settings
from app.logger import get_logger

logger = get_logger("auth_routes")
router = APIRouter()


async def get_token_credentials(request: Request) -> dict:
    """Parse token credentials from form or JSON body."""
    content_type = request.headers.get("content-type", "").split(";")[0].strip().lower()

    if content_type == "application/json":
        try:
            body = await request.json()
        except Exception:
            body = {}
        return {
            "username": body.get("username") or body.get("email"),
            "password": body.get("password"),
        }

    try:
        form = await request.form()
    except Exception:
        return {"username": None, "password": None}

    return {
        "username": form.get("username") or form.get("email"),
        "password": form.get("password"),
    }


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    settings = get_settings()
    try:
        # Debug: log incoming registration payload (without printing password in plain)
        try:
            logger.info(f"Register payload received: name=%s email=%s mobile=%s city=%s state=%s pincode=%s",
                        user.name, user.email, user.mobile, user.city, user.state, user.pincode)
        except Exception:
            logger.debug("Failed to log register payload")

        hashed_password = hash_password(user.password)
        user.password = hashed_password

        try:
            # Debug: call register and capture any DB-level exceptions with details
            row, user_dict = register_user(user)
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            logger.error("Error during register_user: %s\nTraceback:\n%s", e, tb)
            # Re-raise a mapped HTTP error for duplicate emails
            if isinstance(e, ValueError) and "Email already registered" in str(e):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
            # Surface the error as Internal Server Error with a safe message
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

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
    except Exception as e:
        # Ensure unhandled exceptions are logged with traceback to the application logger
        logger.exception("Unhandled exception in register(): %s", e)
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
async def token(request: Request):
    credentials = await get_token_credentials(request)
    username = credentials.get("username")
    password = credentials.get("password")

    if not username or not password:
        logger.warning("Token request missing username or password")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username and password are required")

    db_user = authenticate_user(username, password)
    if not db_user:
        logger.warning("Token request failed for user: %s", username)
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
async def login(user: UserLogin, request: Request):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Log Origin and headers to help debug CORS issues from the browser
        try:
            origin = request.headers.get("origin")
            logger.info(f"Login request Origin: {origin}")
            # Optionally log a subset of headers
            hdrs = {k: v for k, v in request.headers.items() if k.lower() in ("origin", "host", "user-agent", "authorization", "content-type")}
            logger.debug(f"Login request headers: {hdrs}")
        except Exception:
            logger.exception("Failed to read request headers for login")
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