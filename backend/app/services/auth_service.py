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
        # Check duplicate email
        cursor.execute("SELECT COUNT(1) FROM USERS WHERE EMAIL = :email", {"email": user.email})
        if cursor.fetchone()[0] > 0:
            raise ValueError("Email already registered")

        hashed_password = None
        # Hashing should be done by caller to avoid circular imports; caller can pass hashed password if needed.
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
