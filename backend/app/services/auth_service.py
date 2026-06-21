from typing import Optional, Tuple, Dict
from app.schemas.user_schema import UserRegister
from app.database.db import get_connection


def register_user(user: UserRegister) -> Tuple[Optional[Tuple], Optional[Dict]]:
    """Insert a new user into the database and return the DB row and a dict representation.

    Returns (db_row_tuple, user_dict)
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Debug: log the parameters that will be used for insertion (do not log raw password)
        try:
            logger = __import__('app.logger', fromlist=['get_logger']).get_logger('auth_service')
            logger.debug("register_user called with email=%s name=%s mobile=%s city=%s state=%s pincode=%s",
                         user.email, user.name, user.mobile, user.city, user.state, user.pincode)
        except Exception:
            pass
        # Check duplicate email
        cursor.execute("SELECT COUNT(1) FROM USERS WHERE EMAIL = :email", {"email": user.email})
        if cursor.fetchone()[0] > 0:
            raise ValueError("Email already registered")

        hashed_password = None
        # Hashing should be done by caller to avoid circular imports; caller can pass hashed password if needed.
        try:
            cursor.execute(
            """
            INSERT INTO USERS (ID, NAME, EMAIL, PASSWORD, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE)
            VALUES (USER_SEQ.NEXTVAL, :name, :email, :password, :role, :mobile, :address, :city, :state, :pincode)
            """,
            {
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "role": "CUSTOMER",
                "mobile": user.mobile,
                "address": user.address,
                "city": user.city,
                "state": user.state,
                "pincode": user.pincode,
            },
            )
            conn.commit()
        except Exception as exc:
            # Log SQL parameters and traceback for debugging
            try:
                import traceback
                tb = traceback.format_exc()
                logger = __import__('app.logger', fromlist=['get_logger']).get_logger('auth_service')
                logger.error("Error executing INSERT for user %s: %s\nTraceback:\n%s", user.email, exc, tb)
            except Exception:
                pass
            raise

        # Fetch the newly created user (select commonly used fields)
        cursor.execute(
            "SELECT ID, NAME, EMAIL, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE FROM USERS WHERE EMAIL = :email",
            {"email": user.email},
        )
        row = cursor.fetchone()

        if not row:
            return None, None

        user_dict = {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "role": row[3],
            "mobile": row[4],
            "address": row[5],
            "city": row[6],
            "state": row[7],
            "pincode": row[8],
        }

        return row, user_dict
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass
