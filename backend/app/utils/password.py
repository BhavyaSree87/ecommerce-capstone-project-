from passlib.context import CryptContext
from passlib.exc import UnknownHashError

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(
            plain_password,
            hashed_password
        )
    except UnknownHashError:
        # Fallback for legacy or plain-text passwords stored in the database.
        # This preserves compatibility while allowing token generation to fail gracefully.
        return plain_password == hashed_password