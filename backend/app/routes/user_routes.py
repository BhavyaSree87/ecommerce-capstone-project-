from fastapi import APIRouter, Depends, HTTPException
from app.database.db import get_connection
from app.utils.auth_dependency import current_user, admin_only

router = APIRouter()


@router.get("/all", dependencies=[Depends(admin_only)])
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ID, NAME, EMAIL, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE FROM USERS")
        rows = cursor.fetchall()

        def split_name(full_name):
            if not full_name:
                return "", ""
            parts = full_name.split()
            first_name = parts[0]
            last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
            return first_name, last_name

        return [
            {
                "id": row[0],
                "username": row[1],
                "name": row[1],
                "email": row[2],
                "role": row[3],
                "mobile": row[4],
                "address": row[5],
                "city": row[6],
                "state": row[7],
                "pincode": row[8],
                "first_name": split_name(row[1])[0],
                "last_name": split_name(row[1])[1],
                "created_at": None,
            }
            for row in rows
        ]
    finally:
        cursor.close()
        conn.close()


@router.get("/{user_id}")
def get_user(user_id: int, user=Depends(current_user)):
    
    if user.get("role") != "ADMIN" and user.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ID, NAME, EMAIL, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE FROM USERS WHERE ID = :id", {"id": user_id})
        data = cursor.fetchone()
        if not data:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": data[0], "name": data[1], "email": data[2], "role": data[3], "mobile": data[4], "address": data[5], "city": data[6], "state": data[7], "pincode": data[8]}
    finally:
        cursor.close()
        conn.close()


@router.put("/update/{user_id}")
def update_user(user_id: int, payload: dict, user=Depends(current_user)):
    if user.get("role") != "ADMIN" and user.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Email required")
        cursor.execute("UPDATE USERS SET EMAIL = :email WHERE ID = :id", {"email": email, "id": user_id})
        conn.commit()
        return {"message": "User Updated Successfully"}
    finally:
        cursor.close()
        conn.close()


@router.delete("/delete/{user_id}")
def delete_user(user_id: int, user=Depends(admin_only)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM USERS WHERE ID = :id", {"id": user_id})
        conn.commit()
        return {"message": "User Deleted Successfully"}
    finally:
        cursor.close()
        conn.close()